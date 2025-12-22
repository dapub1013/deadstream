#!/usr/bin/env python3
"""
Database Validation Script for DeadStream

Run data quality checks and generate reports about database health.

Usage:
    # Run full validation report
    python validate_database.py

    # Quick check only
    python validate_database.py --quick

    # Check for duplicates
    python validate_database.py --duplicates
"""

import sys
import os
import argparse

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.database.validation import (
    validate_database,
    generate_quality_report,
    find_duplicate_identifiers,
    find_duplicate_shows
)


def quick_check():
    """Run a quick validation check"""
    print("\n" + "="*60)
    print("QUICK DATABASE CHECK")
    print("="*60)
    
    report = validate_database()
    
    print(f"\nTotal shows: {report.total_shows:,}")
    print(f"Critical errors: {len(report.errors)}")
    print(f"Warnings: {len(report.warnings)}")
    
    if report.is_healthy():
        print("\nStatus: Database is healthy!")
    else:
        print("\nStatus: Database needs attention")
        print(f"Error rate: {len(report.errors) / max(report.total_shows, 1) * 100:.2f}%")
    
    print("="*60)


def check_duplicates():
    """Check for duplicate identifiers and shows"""
    print("\n" + "="*60)
    print("DUPLICATE CHECK")
    print("="*60)
    
    # Check for duplicate identifiers (shouldn't happen)
    dup_ids = find_duplicate_identifiers()
    
    if dup_ids:
        print(f"\nCRITICAL: Found {len(dup_ids)} duplicate identifier(s)!")
        for identifier, count in dup_ids:
            print(f"  {identifier}: {count} copies")
    else:
        print("\nNo duplicate identifiers found (good!)")
    
    # Check for multiple recordings of same show
    dup_shows = find_duplicate_shows()
    
    if dup_shows:
        print(f"\nFound {len(dup_shows)} show(s) with multiple recordings:")
        print("(This is normal - same concert, different recordings)")
        for i, (date, venue, count) in enumerate(dup_shows[:10], 1):
            print(f"  {i}. {date} - {venue}: {count} recordings")
        
        if len(dup_shows) > 10:
            print(f"  ... and {len(dup_shows) - 10} more")
    else:
        print("\nNo duplicate shows found")
    
    print("="*60)


def full_report():
    """Generate full data quality report"""
    generate_quality_report()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Validate DeadStream database and check data quality'
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Quick check only (faster)'
    )
    
    parser.add_argument(
        '--duplicates',
        action='store_true',
        help='Check for duplicates only'
    )
    
    args = parser.parse_args()
    
    if args.quick:
        quick_check()
    elif args.duplicates:
        check_duplicates()
    else:
        # Full report
        full_report()


if __name__ == '__main__':
    main()
