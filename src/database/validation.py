"""
Data Validation Module for DeadStream

This module provides functions to validate show data quality, detect issues,
and generate reports about database health. Useful for ensuring data integrity
after updates and imports.

Validation checks include:
- Date format validation
- Required field completeness
- Duplicate detection
- Data quality scoring
- Database health reports
"""

import sqlite3
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from .schema import DB_PATH


class ValidationReport:
    """Container for validation results"""
    
    def __init__(self):
        self.total_shows = 0
        self.errors = []
        self.warnings = []
        self.stats = {}
    
    def add_error(self, show_id: str, message: str):
        """Add a critical error"""
        self.errors.append((show_id, message))
    
    def add_warning(self, show_id: str, message: str):
        """Add a warning (non-critical issue)"""
        self.warnings.append((show_id, message))
    
    def add_stat(self, key: str, value):
        """Add a statistic"""
        self.stats[key] = value
    
    def is_healthy(self) -> bool:
        """Check if database is in good health (few errors)"""
        error_rate = len(self.errors) / max(self.total_shows, 1)
        return error_rate < 0.01  # Less than 1% errors
    
    def print_report(self):
        """Print a formatted validation report"""
        print("\n" + "="*60)
        print("DATABASE VALIDATION REPORT")
        print("="*60)
        
        print(f"\nTotal shows validated: {self.total_shows:,}")
        
        # Statistics
        if self.stats:
            print("\nDatabase Statistics:")
            for key, value in sorted(self.stats.items()):
                if isinstance(value, float):
                    print(f"  {key}: {value:.1f}%")
                elif isinstance(value, str):
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {value:,}")
        
        # Errors
        print(f"\nCritical Errors: {len(self.errors)}")
        if self.errors:
            print("  First 10 errors:")
            for show_id, message in self.errors[:10]:
                print(f"    {show_id}: {message}")
            if len(self.errors) > 10:
                print(f"    ... and {len(self.errors) - 10} more")
        
        # Warnings
        print(f"\nWarnings: {len(self.warnings)}")
        if self.warnings:
            print("  First 10 warnings:")
            for show_id, message in self.warnings[:10]:
                print(f"    {show_id}: {message}")
            if len(self.warnings) > 10:
                print(f"    ... and {len(self.warnings) - 10} more")
        
        # Health status
        print("\n" + "="*60)
        if self.is_healthy():
            print("DATABASE STATUS: HEALTHY")
            if len(self.warnings) > 0:
                print(f"Note: {len(self.warnings)} warnings found (non-critical)")
        else:
            print("DATABASE STATUS: NEEDS ATTENTION")
            print(f"Error rate: {len(self.errors) / max(self.total_shows, 1) * 100:.2f}%")
        print("="*60)


# ============================================================================
# FIELD VALIDATION FUNCTIONS
# ============================================================================

def validate_date_format(date_str: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a date is in YYYY-MM-DD format
    
    Args:
        date_str: Date string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not date_str:
        return False, "Date is empty"
    
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return False, f"Invalid date format: {date_str} (expected YYYY-MM-DD)"
    
    # Try to parse as actual date
    try:
        year, month, day = map(int, date_str.split('-'))
        
        if year < 1965 or year > 1995:
            return False, f"Date out of range: {date_str} (GD era: 1965-1995)"
        
        if month < 1 or month > 12:
            return False, f"Invalid month: {month}"
        
        if day < 1 or day > 31:
            return False, f"Invalid day: {day}"
        
        # Basic day-of-month validation
        if month in [4, 6, 9, 11] and day > 30:
            return False, f"Invalid day for month: {date_str}"
        
        if month == 2 and day > 29:
            return False, f"Invalid day for February: {date_str}"
        
        return True, None
        
    except ValueError:
        return False, f"Cannot parse date: {date_str}"


def validate_identifier(identifier: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that an identifier looks reasonable
    
    Args:
        identifier: Archive.org identifier
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not identifier:
        return False, "Identifier is empty"
    
    if len(identifier) < 5:
        return False, f"Identifier too short: {identifier}"
    
    # Should contain 'gd' for Grateful Dead
    if 'gd' not in identifier.lower():
        return False, f"Identifier doesn't contain 'gd': {identifier}"
    
    return True, None


def validate_rating(avg_rating: float, num_reviews: int) -> Tuple[bool, Optional[str]]:
    """
    Validate rating data
    
    Args:
        avg_rating: Average rating (0-5)
        num_reviews: Number of reviews
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if avg_rating < 0 or avg_rating > 5:
        return False, f"Rating out of range: {avg_rating} (expected 0-5)"
    
    if num_reviews < 0:
        return False, f"Negative review count: {num_reviews}"
    
    # Warning: rating without reviews is suspicious
    if avg_rating > 0 and num_reviews == 0:
        return True, "Has rating but no reviews (unusual)"
    
    return True, None


# ============================================================================
# DATABASE VALIDATION FUNCTIONS
# ============================================================================

def validate_show(show: Dict) -> List[str]:
    """
    Validate a single show's data
    
    Args:
        show: Show dictionary (from database)
        
    Returns:
        List of error/warning messages (empty if valid)
    """
    issues = []
    
    # Validate identifier
    valid, msg = validate_identifier(show.get('identifier', ''))
    if not valid:
        issues.append(f"IDENTIFIER: {msg}")
    
    # Validate date
    valid, msg = validate_date_format(show.get('date', ''))
    if not valid:
        issues.append(f"DATE: {msg}")
    
    # Validate rating
    avg_rating = show.get('avg_rating', 0.0)
    num_reviews = show.get('num_reviews', 0)
    valid, msg = validate_rating(avg_rating, num_reviews)
    if not valid:
        issues.append(f"RATING: {msg}")
    elif msg:  # Warning
        issues.append(f"WARNING: {msg}")
    
    # Check for missing optional but important fields
    if not show.get('venue'):
        issues.append("WARNING: Missing venue")
    
    if not show.get('city') and not show.get('state'):
        issues.append("WARNING: Missing location (city and state)")
    
    return issues


def validate_database(db_path: str = DB_PATH) -> ValidationReport:
    """
    Validate entire database
    
    Args:
        db_path: Path to database file
        
    Returns:
        ValidationReport with results
    """
    report = ValidationReport()
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all shows
        cursor.execute("SELECT * FROM shows")
        shows = cursor.fetchall()
        report.total_shows = len(shows)
        
        # Validate each show
        for row in shows:
            show = {key: row[key] for key in row.keys()}
            issues = validate_show(show)
            
            identifier = show.get('identifier', 'UNKNOWN')
            
            for issue in issues:
                if issue.startswith('WARNING:'):
                    report.add_warning(identifier, issue.replace('WARNING: ', ''))
                else:
                    report.add_error(identifier, issue)
        
        # Calculate statistics
        cursor.execute("SELECT COUNT(*) FROM shows WHERE venue IS NOT NULL")
        with_venue = cursor.fetchone()[0]
        report.add_stat("Shows with venue", with_venue)
        report.add_stat("Shows missing venue (%)", 
                       (report.total_shows - with_venue) / max(report.total_shows, 1) * 100)
        
        cursor.execute("SELECT COUNT(*) FROM shows WHERE city IS NOT NULL")
        with_city = cursor.fetchone()[0]
        report.add_stat("Shows with city", with_city)
        
        cursor.execute("SELECT COUNT(*) FROM shows WHERE state IS NOT NULL")
        with_state = cursor.fetchone()[0]
        report.add_stat("Shows with state", with_state)
        
        cursor.execute("SELECT COUNT(*) FROM shows WHERE avg_rating > 0")
        with_rating = cursor.fetchone()[0]
        report.add_stat("Shows with ratings", with_rating)
        report.add_stat("Shows rated (%)", 
                       with_rating / max(report.total_shows, 1) * 100)
        
        cursor.execute("SELECT AVG(avg_rating) FROM shows WHERE avg_rating > 0")
        avg_rating = cursor.fetchone()[0]
        if avg_rating:
            report.add_stat("Average rating (rated shows)", f"{avg_rating:.2f}")
        
        conn.close()
        
    except sqlite3.Error as e:
        report.add_error("DATABASE", f"Database error: {e}")
    
    return report


# ============================================================================
# DUPLICATE DETECTION
# ============================================================================

def find_duplicate_identifiers(db_path: str = DB_PATH) -> List[Tuple[str, int]]:
    """
    Find any duplicate identifiers (should never happen with PRIMARY KEY)
    
    Args:
        db_path: Path to database file
        
    Returns:
        List of tuples: [(identifier, count), ...]
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT identifier, COUNT(*) as count
        FROM shows
        GROUP BY identifier
        HAVING count > 1
    """)
    
    duplicates = [(row[0], row[1]) for row in cursor.fetchall()]
    conn.close()
    
    return duplicates


def find_duplicate_shows(db_path: str = DB_PATH) -> List[Tuple[str, str, int]]:
    """
    Find shows on the same date at the same venue (multiple recordings)
    
    Args:
        db_path: Path to database file
        
    Returns:
        List of tuples: [(date, venue, count), ...]
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT date, venue, COUNT(*) as count
        FROM shows
        WHERE venue IS NOT NULL
        GROUP BY date, venue
        HAVING count > 1
        ORDER BY count DESC, date DESC
        LIMIT 50
    """)
    
    duplicates = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
    conn.close()
    
    return duplicates


# ============================================================================
# DATA QUALITY REPORTS
# ============================================================================

def generate_quality_report(db_path: str = DB_PATH):
    """
    Generate a comprehensive data quality report
    
    Args:
        db_path: Path to database file
    """
    print("\n" + "="*60)
    print("DATA QUALITY REPORT")
    print("="*60)
    
    # Run validation
    report = validate_database(db_path)
    
    # Check for duplicate identifiers
    dup_ids = find_duplicate_identifiers(db_path)
    if dup_ids:
        print("\nDUPLICATE IDENTIFIERS FOUND (Critical!):")
        for identifier, count in dup_ids:
            print(f"  {identifier}: {count} copies")
    
    # Show some duplicate shows (multiple recordings)
    dup_shows = find_duplicate_shows(db_path)
    if dup_shows:
        print("\nShows with Multiple Recordings (Top 10):")
        for date, venue, count in dup_shows[:10]:
            print(f"  {date} - {venue}: {count} recordings")
        if len(dup_shows) > 10:
            print(f"  ... and {len(dup_shows) - 10} more")
    
    # Print main validation report
    report.print_report()


# ============================================================================
# CLEANUP FUNCTIONS
# ============================================================================

def remove_duplicate_identifiers(db_path: str = DB_PATH, dry_run: bool = True):
    """
    Remove duplicate identifiers (keeping the first one)
    
    Args:
        db_path: Path to database file
        dry_run: If True, don't actually delete, just show what would be removed
    """
    duplicates = find_duplicate_identifiers(db_path)
    
    if not duplicates:
        print("No duplicate identifiers found!")
        return
    
    print(f"\nFound {len(duplicates)} duplicate identifier(s):")
    for identifier, count in duplicates:
        print(f"  {identifier}: {count} copies")
    
    if dry_run:
        print("\nDry run mode - no changes made")
        print("Run with dry_run=False to remove duplicates")
        return
    
    # Remove duplicates (this shouldn't normally happen due to PRIMARY KEY)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for identifier, _ in duplicates:
        # Keep the one with the most complete data (most recent last_updated)
        cursor.execute("""
            DELETE FROM shows 
            WHERE identifier = ? 
            AND rowid NOT IN (
                SELECT rowid FROM shows 
                WHERE identifier = ?
                ORDER BY last_updated DESC 
                LIMIT 1
            )
        """, (identifier, identifier))
    
    conn.commit()
    removed = conn.total_changes
    conn.close()
    
    print(f"\nRemoved {removed} duplicate(s)")
