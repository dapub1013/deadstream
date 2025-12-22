#!/usr/bin/env python3
"""
Database Update Script for DeadStream

This script checks for new Grateful Dead shows added to the Internet Archive
since the last database update and adds them to the local database.

Much faster than full population - only fetches new shows.

Usage:
    # Update with shows from last 7 days
    python update_database.py

    # Update with shows from specific date onwards
    python update_database.py --since 2024-12-01

    # Check what would be updated (dry run)
    python update_database.py --dry-run
"""

import sys
import os
import argparse
import sqlite3
from datetime import datetime, timedelta

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.api.rate_limiter import ArchiveAPIClient
from src.database.schema import DB_PATH


class DatabaseUpdater:
    """Handles checking for and inserting new shows"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.api_client = ArchiveAPIClient(requests_per_second=2.0)
        
        # Statistics
        self.stats = {
            'new_shows_found': 0,
            'new_shows_inserted': 0,
            'shows_skipped': 0,
            'errors': 0
        }
    
    def get_last_update_date(self):
        """
        Get the most recent last_updated timestamp from database
        
        Returns:
            Date string in YYYY-MM-DD format, or None if database is empty
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT MAX(last_updated) FROM shows
            """)
            
            result = cursor.fetchone()[0]
            conn.close()
            
            if result:
                # Convert ISO timestamp to date only
                # Format: 2025-12-21T16:30:45.123456 -> 2025-12-21
                return result.split('T')[0]
            else:
                return None
                
        except sqlite3.Error as e:
            print(f"Error reading database: {e}")
            return None
    
    def fetch_new_shows(self, since_date):
        """
        Fetch shows added to Archive.org since the given date
        
        Args:
            since_date: Date string in YYYY-MM-DD format
            
        Returns:
            List of show dictionaries from API
        """
        # Archive.org's publicdate field tracks when items were added
        # We query for items added on or after the since_date
        query = f'collection:GratefulDead AND publicdate:[{since_date} TO null]'
        fields = 'identifier,date,venue,coverage,avg_rating,num_reviews,publicdate'
        
        try:
            print(f"Querying Archive.org for shows added since {since_date}...")
            
            response = self.api_client.search(
                query=query,
                fields=fields,
                rows=1000  # Should be enough for updates
            )
            
            # Extract docs from response
            if isinstance(response, dict) and 'response' in response:
                results = response['response'].get('docs', [])
            elif isinstance(response, list):
                results = response
            else:
                print("Warning: Unexpected API response format")
                results = []
            
            return results
            
        except Exception as e:
            print(f"Error fetching updates: {e}")
            self.stats['errors'] += 1
            return []
    
    def clean_show_data(self, raw_show):
        """
        Clean and validate show data (similar to populate script)
        
        Args:
            raw_show: Dictionary from API
            
        Returns:
            Cleaned dictionary or None if invalid
        """
        import re
        
        # Required: identifier
        identifier = raw_show.get('identifier')
        if not identifier:
            return None
        
        # Clean date (handle ISO format with time)
        date = raw_show.get('date', '')
        if 'T' in date:
            date = date.split('T')[0]
        
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            # Try to fix
            if re.match(r'^\d{4}-\d{2}$', date):
                date += '-01'
            elif re.match(r'^\d{4}$', date):
                date += '-01-01'
            else:
                return None
        
        # Parse coverage for city/state
        coverage = raw_show.get('coverage', '')
        if coverage:
            parts = [p.strip() for p in coverage.split(',')]
            city = parts[0] if len(parts) >= 1 else None
            state = parts[1] if len(parts) >= 2 else None
        else:
            city = None
            state = None
        
        # Get other fields
        venue = raw_show.get('venue', '').strip() or None
        
        try:
            avg_rating = float(raw_show.get('avg_rating', 0.0))
        except (ValueError, TypeError):
            avg_rating = 0.0
        
        try:
            num_reviews = int(raw_show.get('num_reviews', 0))
        except (ValueError, TypeError):
            num_reviews = 0
        
        return {
            'identifier': identifier,
            'date': date,
            'venue': venue,
            'city': city,
            'state': state,
            'avg_rating': avg_rating,
            'num_reviews': num_reviews,
            'last_updated': datetime.now().isoformat()
        }
    
    def insert_show(self, conn, show_data):
        """
        Insert a show using idempotent INSERT OR IGNORE
        
        Args:
            conn: SQLite connection
            show_data: Dictionary of show data
            
        Returns:
            True if inserted, False if already exists
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
            
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"  Error inserting {show_data['identifier']}: {e}")
            self.stats['errors'] += 1
            return False
    
    def update_database(self, since_date=None, dry_run=False):
        """
        Main update function
        
        Args:
            since_date: Date to check from (YYYY-MM-DD), or None for auto-detect
            dry_run: If True, don't actually insert, just show what would happen
        """
        print("\n" + "="*60)
        print("DATABASE UPDATE")
        print("="*60)
        
        # Determine since date
        if since_date is None:
            # Auto-detect from database
            last_update = self.get_last_update_date()
            
            if last_update:
                print(f"Last database update: {last_update}")
                since_date = last_update
            else:
                # Database is empty or no updates - use 7 days ago as default
                since_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                print(f"No previous updates found, checking last 7 days")
        
        print(f"Checking for shows added since: {since_date}")
        
        if dry_run:
            print("\n*** DRY RUN MODE - No changes will be made ***\n")
        
        # Fetch new shows
        new_shows = self.fetch_new_shows(since_date)
        self.stats['new_shows_found'] = len(new_shows)
        
        print(f"Found {len(new_shows)} show(s) added to Archive.org since {since_date}")
        
        if len(new_shows) == 0:
            print("\nDatabase is up to date - no new shows to add!")
            print("="*60)
            return
        
        if dry_run:
            print("\nShows that would be added:")
            for i, show in enumerate(new_shows[:10], 1):
                clean = self.clean_show_data(show)
                if clean:
                    venue = clean['venue'] or 'Unknown venue'
                    print(f"  {i}. {clean['date']} - {venue} ({clean['identifier']})")
            
            if len(new_shows) > 10:
                print(f"  ... and {len(new_shows) - 10} more")
            
            print("\nRun without --dry-run to add these shows.")
            print("="*60)
            return
        
        # Insert new shows
        print("\nInserting new shows...")
        
        conn = sqlite3.connect(self.db_path)
        
        try:
            for raw_show in new_shows:
                # Clean data
                clean_data = self.clean_show_data(raw_show)
                
                if clean_data is None:
                    self.stats['shows_skipped'] += 1
                    continue
                
                # Insert
                if self.insert_show(conn, clean_data):
                    self.stats['new_shows_inserted'] += 1
                    venue = clean_data['venue'] or 'Unknown'
                    print(f"  Added: {clean_data['date']} - {venue}")
                else:
                    # Already exists
                    self.stats['shows_skipped'] += 1
            
            # Commit all inserts
            conn.commit()
            
        finally:
            conn.close()
        
        # Final statistics
        print("\n" + "="*60)
        print("UPDATE COMPLETE")
        print("="*60)
        print(f"Shows found on Archive.org: {self.stats['new_shows_found']}")
        print(f"New shows inserted:         {self.stats['new_shows_inserted']}")
        print(f"Shows skipped (duplicates): {self.stats['shows_skipped']}")
        print(f"Errors encountered:         {self.stats['errors']}")
        
        if self.stats['new_shows_inserted'] > 0:
            print(f"\n{self.stats['new_shows_inserted']} new show(s) added to database!")
        else:
            print("\nDatabase already up to date!")
        
        print("="*60)


def main():
    """Main entry point with argument parsing"""
    
    parser = argparse.ArgumentParser(
        description='Update DeadStream database with new shows from Archive.org'
    )
    
    parser.add_argument(
        '--since',
        type=str,
        metavar='YYYY-MM-DD',
        help='Check for shows added since this date (default: auto-detect from database)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without making changes'
    )
    
    args = parser.parse_args()
    
    # Validate since date format if provided
    if args.since:
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', args.since):
            print(f"Error: Invalid date format: {args.since}")
            print("Use format: YYYY-MM-DD (e.g., 2024-12-01)")
            sys.exit(1)
    
    # Create updater and run
    updater = DatabaseUpdater()
    updater.update_database(since_date=args.since, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
