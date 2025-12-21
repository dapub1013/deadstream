#!/usr/bin/env python3
"""
Test database initialization.

Verifies that database can be created, connected to, and queried.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import init_database, get_connection, verify_database


def test_database_init():
    """Test database initialization and basic operations."""
    
    print("Test 1: Initialize database")
    print("-" * 60)
    success = init_database()
    assert success, "Database initialization failed!"
    print()
    
    print("Test 2: Get connection")
    print("-" * 60)
    try:
        conn = get_connection()
        print("Connection obtained successfully")
        conn.close()
        print("Connection closed successfully")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    print()
    
    print("Test 3: Insert test show")
    print("-" * 60)
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO shows (identifier, date, venue, city, state, avg_rating, num_reviews)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('test-show-001', '1977-05-08', 'Barton Hall', 'Ithaca', 'NY', 4.8, 156))
    
    conn.commit()
    print("Test show inserted")
    
    # Query it back
    cursor.execute("SELECT * FROM shows WHERE identifier = ?", ('test-show-001',))
    show = cursor.fetchone()
    print(f"Retrieved: {show[1]} at {show[2]}")
    
    # Clean up test data
    cursor.execute("DELETE FROM shows WHERE identifier = ?", ('test-show-001',))
    conn.commit()
    print("Test show deleted")
    
    conn.close()
    print()
    
    print("Test 4: Verify database")
    print("-" * 60)
    success = verify_database()
    assert success, "Verification failed!"
    print()
    
    print("=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("Database is ready for data population (Phase 3.3)")


if __name__ == '__main__':
    test_database_init()
