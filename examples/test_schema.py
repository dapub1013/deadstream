#!/usr/bin/env python3
"""
Test script for database schema.

This script verifies that:
1. Database can be created
2. Tables and indexes are created correctly
3. Basic insert and query operations work
4. Constraints are enforced properly

Run from project root: python3 examples/test_schema.py
"""

import sqlite3
import os
import sys
from datetime import datetime

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database.schema import SCHEMA_SQL, get_schema_info


def test_schema():
    """Test database schema creation and basic operations."""
    
    print("DeadStream Schema Test")
    print("=" * 60)
    print()
    
    # Use in-memory database for testing (no file created)
    print("1. Creating test database (in-memory)...")
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    print("   Database created")
    print()
    
    # Create schema
    print("2. Creating schema...")
    for i, sql in enumerate(SCHEMA_SQL, 1):
        statement_type = sql.split()[0:3]
        print(f"   Executing: {' '.join(statement_type)}...")
        cursor.execute(sql)
    conn.commit()
    print(f"   Executed {len(SCHEMA_SQL)} SQL statements")
    print()
    
    # Verify table exists
    print("3. Verifying table creation...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"   Tables found: {tables}")
    assert 'shows' in tables, "shows table not created!"
    print("   shows table verified")
    print()
    
    # Verify indexes exist
    print("4. Verifying indexes...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = [row[0] for row in cursor.fetchall()]
    print(f"   Indexes found: {len(indexes)}")
    for idx in indexes:
        print(f"      - {idx}")
    
    # Check for our specific indexes
    expected_indexes = [
        'idx_date', 'idx_venue', 'idx_rating', 
        'idx_year', 'idx_state', 'idx_date_rating'
    ]
    for idx_name in expected_indexes:
        assert idx_name in indexes, f"Index {idx_name} not created!"
    print("   All expected indexes verified")
    print()
    
    # Test insert (Cornell '77)
    print("5. Testing insert operation...")
    test_show = {
        'identifier': 'gd1977-05-08.sbd.hicks.4982.sbeok.shnf',
        'date': '1977-05-08',
        'venue': 'Barton Hall, Cornell University',
        'city': 'Ithaca',
        'state': 'NY',
        'avg_rating': 4.8,
        'num_reviews': 156,
        'source_type': 'sbd',
        'taper': 'Betty Cantor-Jackson',
        'last_updated': datetime.now().isoformat()
    }
    
    cursor.execute("""
        INSERT INTO shows 
        (identifier, date, venue, city, state, avg_rating, num_reviews,
         source_type, taper, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        test_show['identifier'], test_show['date'], test_show['venue'],
        test_show['city'], test_show['state'], test_show['avg_rating'],
        test_show['num_reviews'], test_show['source_type'], 
        test_show['taper'], test_show['last_updated']
    ))
    conn.commit()
    print(f"   Inserted: {test_show['date']} - {test_show['venue']}")
    print()
    
    # Test query
    print("6. Testing query operation...")
    cursor.execute("SELECT * FROM shows WHERE identifier = ?", 
                   (test_show['identifier'],))
    result = cursor.fetchone()
    assert result is not None, "Show not found after insert!"
    print(f"   Found show: {result[1]} at {result[2]}")
    print()
    
    # Test duplicate insert (should fail due to PRIMARY KEY)
    print("7. Testing PRIMARY KEY constraint...")
    try:
        cursor.execute("""
            INSERT INTO shows (identifier, date, venue)
            VALUES (?, ?, ?)
        """, (test_show['identifier'], '1977-05-09', 'Different Venue'))
        print("   ERROR: Duplicate insert succeeded (should have failed!)")
        assert False, "PRIMARY KEY constraint not working!"
    except sqlite3.IntegrityError as e:
        print(f"   PRIMARY KEY constraint working (rejected duplicate)")
    print()
    
    # Test NULL date (should fail due to NOT NULL)
    print("8. Testing NOT NULL constraint...")
    try:
        cursor.execute("""
            INSERT INTO shows (identifier, date, venue)
            VALUES (?, ?, ?)
        """, ('test-identifier', None, 'Test Venue'))
        print("   ERROR: NULL date insert succeeded (should have failed!)")
        assert False, "NOT NULL constraint not working!"
    except sqlite3.IntegrityError as e:
        print(f"   NOT NULL constraint working (rejected NULL date)")
    print()
    
    # Test index usage (date search)
    print("9. Testing index usage for date search...")
    # Insert a few more shows
    more_shows = [
        ('gd1977-05-07.aud.serafin.21097.sbeok.flac16', '1977-05-07', 
         'Boston Garden', 'Boston', 'MA', 4.5, 89),
        ('gd1977-05-09.sbd.miller.97293.sbeok.flac16', '1977-05-09',
         'War Memorial', 'Buffalo', 'NY', 4.6, 102),
    ]
    
    for show in more_shows:
        cursor.execute("""
            INSERT INTO shows (identifier, date, venue, city, state, 
                             avg_rating, num_reviews)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, show)
    conn.commit()
    
    # Query by date range
    cursor.execute("""
        SELECT date, venue, city, state 
        FROM shows 
        WHERE date LIKE '1977-05-%'
        ORDER BY date
    """)
    may_1977_shows = cursor.fetchall()
    print(f"   Found {len(may_1977_shows)} shows in May 1977:")
    for show in may_1977_shows:
        print(f"      - {show[0]}: {show[1]}, {show[2]}, {show[3]}")
    assert len(may_1977_shows) == 3, "Should find 3 shows in May 1977"
    print()
    
    # Test year index
    print("10. Testing year index (substr)...")
    cursor.execute("""
        SELECT COUNT(*) FROM shows 
        WHERE substr(date, 1, 4) = '1977'
    """)
    count_1977 = cursor.fetchone()[0]
    print(f"   Found {count_1977} shows in 1977")
    assert count_1977 == 3, "Should find 3 shows in 1977"
    print()
    
    # Test rating sort
    print("11. Testing rating sort...")
    cursor.execute("""
        SELECT date, venue, avg_rating 
        FROM shows 
        WHERE avg_rating IS NOT NULL
        ORDER BY avg_rating DESC
    """)
    sorted_shows = cursor.fetchall()
    print("   Shows sorted by rating (best first):")
    for show in sorted_shows:
        print(f"      - {show[0]}: {show[1]} (rating: {show[2]})")
    
    # Verify sort order
    ratings = [show[2] for show in sorted_shows]
    assert ratings == sorted(ratings, reverse=True), "Ratings not sorted correctly"
    print("   Rating sort verified")
    print()
    
    # Test INSERT OR IGNORE (idempotent inserts)
    print("12. Testing INSERT OR IGNORE (idempotent)...")
    cursor.execute("""
        INSERT OR IGNORE INTO shows (identifier, date, venue)
        VALUES (?, ?, ?)
    """, (test_show['identifier'], '1977-05-08', 'Should be ignored'))
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM shows")
    total_count = cursor.fetchone()[0]
    assert total_count == 3, "INSERT OR IGNORE created duplicate!"
    print("   INSERT OR IGNORE working (duplicate ignored)")
    print()
    
    # Clean up
    conn.close()
    
    # Final summary
    print("=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("Schema is production-ready")
    print(f"Version: {get_schema_info()['version']}")
    print()


if __name__ == '__main__':
    try:
        test_schema()
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)