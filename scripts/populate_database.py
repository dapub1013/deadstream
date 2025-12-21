#!/usr/bin/env python3
"""
Database Population Script for DeadStream

This script fetches Grateful Dead show metadata from the Internet Archive
and populates the local SQLite database. It's designed to be safe to re-run
(idempotent inserts) and provides progress feedback during the process.

Usage:
    # Test mode (sample years only)
    python populate_database.py --test

    # Full population
    python populate_database.py --full

    # Specific year range
    python populate_database.py --years 1977-1980
"""

import sys
import os
import argparse
import sqlite3
import re
from datetime import datetime

# Add project root to path so we can import our modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.api.rate_limiter import ArchiveAPIClient
from src.database.schema import DB_PATH


class ShowValidator:
    """Validates and cleans show data before database insertion"""
    
    @staticmethod
    def validate_date(date_str):
        """Ensure date is in YYYY-MM-DD format"""
        if not date_str:
            return None
        
        # Try to parse the date
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            # Try to fix common formats
            if re.match(r'^\d{4}-\d{2}$', date_str):
                # Year-month only, add day
                date_str += '-01'
            elif re.match(r'^\d{4}$', date_str):
                # Year only, add month and day
                date_str += '-01-01'
            else:
                print(f"  Warning: Invalid date format: {date_str}")
                return None
        
        return date_str
    
    @staticmethod
    def parse_coverage(coverage_str):
        """Parse 'City, State' from coverage field"""
        if not coverage_str:
            return None, None
        
        # Coverage format is typically "City, State" or "City, State, Country"
        parts = [p.strip() for p in coverage_str.split(',')]
        
        if len(parts) >= 2:
            city = parts[0]
            state = parts[1]
            return city, state
        elif len(parts) == 1:
            # Just city, no state
            return parts[0], None
        
        return None, None
    
    @staticmethod
    def clean_show_data(raw_show):
        """
        Clean and validate a single show's data
        
        Args:
            raw_show: Dictionary from API response
            
        Returns:
            Dictionary ready for database insertion, or None if invalid
        """
        # Required field: identifier
        identifier = raw_show.get('identifier')
        if not identifier:
            print(f"  Warning: Show missing identifier, skipping")
            return None
        
        # Validate date
        date = ShowValidator.validate_date(raw_show.get('date'))
        if not date:
            print(f"  Warning: Show {identifier} has invalid date, skipping")
            return None
        
        # Parse city and state from coverage
        city, state = ShowValidator.parse_coverage(raw_show.get('coverage'))
        
        # Get venue
        venue = raw_show.get('venue', '').strip() or None
        
        # Get ratings (convert to float, default to 0.0)
        try:
            avg_rating = float(raw_show.get('avg_rating', 0.0))
        except (ValueError, TypeError):
            avg_rating = 0.0
        
        # Get review count (convert to int, default to 0)
        try:
            num_reviews = int(raw_show.get('num_reviews', 0))
        except (ValueError, TypeError):
            num_reviews = 0
        
        # Current timestamp for last_updated
        last_updated = datetime.now().isoformat()
        
        return {
            'identifier': identifier,
            'date': date,
            'venue': venue,
            'city': city,
            'state': state,
            'avg_rating': avg_rating,
            'num_reviews': num_reviews,
            'last_updated': last_updated
        }


class DatabasePopulator:
    """Handles database population from Archive.org API"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.api_client = ArchiveAPIClient(requests_per_second=2.0)
        self.validator = ShowValidator()
        
        # Statistics
        self.stats = {
            'shows_fetched': 0,
            'shows_inserted': 0,
            'shows_skipped': 0,
            'errors': 0
        }
    
    def fetch_shows_for_year(self, year):
        """
        Fetch all shows for a given year from Archive.org
        
        Args:
            year: Integer year (e.g., 1977)
            
        Returns:
            List of show dictionaries from API
        """
        query = f'collection:GratefulDead AND year:{year}'
        fields = 'identifier,date,venue,coverage,avg_rating,num_reviews'
        
        try:
            results = self.api_client.search(
                query=query,
                fields=fields,
                rows=500  # Max per year should be < 500
            )
            return results
        except Exception as e:
            print(f"  Error fetching data for {year}: {e}")
            self.stats['errors'] += 1
            return []
    
    def insert_show(self, conn, show_data):
        """
        Insert a single show into the database using idempotent INSERT OR IGNORE
        
        Args:
            conn: SQLite connection
            show_data: Dictionary of show data
            
        Returns:
            True if inserted, False if already exists or error
        """
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO shows 
                (identifier, date, venue, city, state, avg_rating, num_reviews, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                show_data['identifier'],
                show_data['date'],
                show_data['venue'],
                show_data['city'],
                show_data['state'],
                show_data['avg_rating'],
                show_data['num_reviews'],
                show_data['last_updated']
            ))
            
            # Check if row was inserted (rowcount > 0) or ignored (rowcount == 0)
            inserted = cursor.rowcount > 0
            return inserted
            
        except sqlite3.Error as e:
            print(f"  Database error inserting {show_data['identifier']}: {e}")
            self.stats['errors'] += 1
            return False
    
    def populate_year(self, conn, year):
        """
        Populate database with all shows from a given year
        
        Args:
            conn: SQLite connection
            year: Integer year to process
        """
        print(f"\nProcessing {year}...", end=" ", flush=True)
        
        # Fetch shows from API
        raw_shows = self.fetch_shows_for_year(year)
        self.stats['shows_fetched'] += len(raw_shows)
        
        if not raw_shows:
            print("No shows found")
            return
        
        print(f"found {len(raw_shows)} shows", end=" ", flush=True)
        
        # Process and insert each show
        inserted_count = 0
        for raw_show in raw_shows:
            # Validate and clean data
            clean_data = self.validator.clean_show_data(raw_show)
            
            if clean_data is None:
                self.stats['shows_skipped'] += 1
                continue
            
            # Insert into database
            if self.insert_show(conn, clean_data):
                inserted_count += 1
                self.stats['shows_inserted'] += 1
            else:
                # Already exists (idempotent insert ignored it)
                self.stats['shows_skipped'] += 1
        
        # Commit after each year
        conn.commit()
        
        print(f"-> inserted {inserted_count}, skipped {len(raw_shows) - inserted_count}")
    
    def populate_database(self, start_year=1965, end_year=1995, test_mode=False):
        """
        Main population function - fetches and inserts all shows
        
        Args:
            start_year: First year to process (default 1965)
            end_year: Last year to process (default 1995)
            test_mode: If True, only process a few years for testing
        """
        if test_mode:
            print("\n" + "="*60)
            print("TEST MODE - Processing sample years only (1977-1978)")
            print("="*60)
            start_year = 1977
            end_year = 1978
        else:
            print("\n" + "="*60)
            print("FULL POPULATION MODE")
            print(f"Processing years {start_year}-{end_year}")
            print("="*60)
        
        # Connect to database
        try:
            conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"\nFatal error: Cannot connect to database: {e}")
            sys.exit(1)
        
        try:
            total_years = end_year - start_year + 1
            print(f"Target: {total_years} years")
            print(f"API Rate Limit: {self.api_client.requests_per_second} requests/second")
            print()
            
            # Process each year
            for year in range(start_year, end_year + 1):
                self.populate_year(conn, year)
                
                # Progress indicator
                years_done = year - start_year + 1
                progress_pct = (years_done / total_years) * 100
                print(f"Progress: {years_done}/{total_years} years ({progress_pct:.1f}%)")
            
            # Final statistics
            print("\n" + "="*60)
            print("POPULATION COMPLETE")
            print("="*60)
            print(f"Shows fetched from API: {self.stats['shows_fetched']}")
            print(f"Shows inserted to DB:   {self.stats['shows_inserted']}")
            print(f"Shows skipped:          {self.stats['shows_skipped']}")
            print(f"Errors encountered:     {self.stats['errors']}")
            
            # Final show count
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM shows")
            total_shows = cursor.fetchone()[0]
            print(f"\nTotal shows in database: {total_shows}")
            print("="*60)
            
        finally:
            conn.close()


def parse_year_range(year_range_str):
    """
    Parse year range string like '1977-1980' into (start, end)
    
    Args:
        year_range_str: String like '1977-1980' or '1977'
        
    Returns:
        Tuple of (start_year, end_year)
    """
    if '-' in year_range_str:
        parts = year_range_str.split('-')
        start = int(parts[0])
        end = int(parts[1])
        return start, end
    else:
        # Single year
        year = int(year_range_str)
        return year, year


def main():
    """Main entry point with argument parsing"""
    
    parser = argparse.ArgumentParser(
        description='Populate DeadStream database with Grateful Dead shows from Archive.org'
    )
    
    # Mode selection (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--test',
        action='store_true',
        help='Test mode: only process years 1977-1978 (quick test)'
    )
    mode_group.add_argument(
        '--full',
        action='store_true',
        help='Full mode: process all years 1965-1995'
    )
    mode_group.add_argument(
        '--years',
        type=str,
        metavar='START-END',
        help='Process specific year range (e.g., --years 1977-1980)'
    )
    
    args = parser.parse_args()
    
    # Create populator
    populator = DatabasePopulator()
    
    # Run appropriate mode
    if args.test:
        populator.populate_database(test_mode=True)
    elif args.full:
        populator.populate_database(start_year=1965, end_year=1995, test_mode=False)
    elif args.years:
        try:
            start, end = parse_year_range(args.years)
            populator.populate_database(start_year=start, end_year=end, test_mode=False)
        except ValueError:
            print(f"Error: Invalid year range format: {args.years}")
            print("Use format: --years 1977-1980 or --years 1977")
            sys.exit(1)


if __name__ == '__main__':
    main()
