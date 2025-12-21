"""
Database initialization and connection management for DeadStream.

This module provides functions to:
- Initialize the database with proper schema
- Get database connections
- Verify database integrity

Usage:
    from src.database import init_database, get_connection
    
    # First time setup
    init_database()
    
    # Get connection for queries
    conn = get_connection()

Author: DeadStream Project
Created: December 2025
Phase: 3.2 - Database Initialization
"""

import sqlite3
import os
from pathlib import Path

from .schema import SCHEMA_SQL, get_schema_info


# Database file location (relative to project root)
DB_PATH = os.path.join(
    os.path.dirname(__file__),  # src/database/
    '..',                        # src/
    '..',                        # project root
    'data',                      # data/
    'shows.db'                   # shows.db
)


def get_db_path():
    """
    Get the absolute path to the database file.
    
    Returns:
        str: Absolute path to shows.db
    """
    return os.path.abspath(DB_PATH)


def ensure_data_directory():
    """
    Ensure the data/ directory exists.
    
    Creates the directory if it doesn't exist.
    """
    data_dir = os.path.dirname(get_db_path())
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    print(f"Data directory: {data_dir}")


def init_database(force=False):
    """
    Initialize the database with schema.
    
    Creates the database file and executes all schema SQL statements.
    Safe to call multiple times (uses IF NOT EXISTS).
    
    Args:
        force (bool): If True, delete existing database and recreate.
                     Default: False (preserve existing data)
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        sqlite3.Error: If database creation fails
    """
    db_path = get_db_path()
    
    print("=" * 60)
    print("DeadStream Database Initialization")
    print("=" * 60)
    print()
    
    # Ensure data directory exists
    ensure_data_directory()
    
    # Handle force flag
    if force and os.path.exists(db_path):
        print(f"Force flag set - deleting existing database...")
        os.remove(db_path)
        print(f"Deleted: {db_path}")
        print()
    
    # Check if database already exists
    db_exists = os.path.exists(db_path)
    if db_exists:
        print(f"Database already exists: {db_path}")
        print("Schema will be updated (IF NOT EXISTS protects existing data)")
    else:
        print(f"Creating new database: {db_path}")
    print()
    
    try:
        # Connect to database (creates file if doesn't exist)
        print("Connecting to database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("Connected")
        print()
        
        # Execute schema SQL
        print("Creating schema...")
        for i, sql in enumerate(SCHEMA_SQL, 1):
            # Get statement type for logging
            statement_type = sql.strip().split()[0:3]
            statement_desc = ' '.join(statement_type)
            
            print(f"  {i}. Executing: {statement_desc}...")
            cursor.execute(sql)
        
        # Commit changes
        conn.commit()
        print(f"\nExecuted {len(SCHEMA_SQL)} SQL statements")
        print()
        
        # Verify schema
        print("Verifying schema...")
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"  Tables: {tables}")
        
        # Check indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        print(f"  Indexes: {len(indexes)} created")
        
        # Get row count
        cursor.execute("SELECT COUNT(*) FROM shows")
        count = cursor.fetchone()[0]
        print(f"  Shows in database: {count}")
        print()
        
        # Close connection
        conn.close()
        
        # Success message
        print("=" * 60)
        print("DATABASE INITIALIZATION COMPLETE")
        print("=" * 60)
        print()
        print(f"Database location: {db_path}")
        print(f"Schema version: {get_schema_info()['version']}")
        print(f"Status: Ready for data population")
        print()
        
        return True
        
    except sqlite3.Error as e:
        print(f"\nERROR: Database initialization failed")
        print(f"SQLite error: {e}")
        return False
    except Exception as e:
        print(f"\nERROR: Unexpected error during initialization")
        print(f"Error: {e}")
        return False


def get_connection():
    """
    Get a connection to the database.
    
    Returns a connection object that can be used for queries.
    Caller is responsible for closing the connection.
    
    Returns:
        sqlite3.Connection: Database connection
    
    Raises:
        FileNotFoundError: If database doesn't exist (call init_database first)
        sqlite3.Error: If connection fails
    
    Example:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM shows LIMIT 10")
        shows = cursor.fetchall()
        conn.close()
    """
    db_path = get_db_path()
    
    # Check if database exists
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"Database not found: {db_path}\n"
            f"Run init_database() first to create the database."
        )
    
    # Connect and return
    try:
        conn = sqlite3.connect(db_path)
        # Enable foreign keys (good practice for future)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def verify_database():
    """
    Verify database integrity and display statistics.
    
    Checks that database exists, schema is correct, and displays
    basic statistics about the data.
    
    Returns:
        bool: True if database is valid, False otherwise
    """
    db_path = get_db_path()
    
    print("=" * 60)
    print("Database Verification")
    print("=" * 60)
    print()
    
    # Check file exists
    if not os.path.exists(db_path):
        print(f"ERROR: Database file not found: {db_path}")
        print("Run init_database() first.")
        return False
    
    print(f"Database: {db_path}")
    
    # Get file size
    size_bytes = os.path.getsize(db_path)
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    
    if size_mb >= 1:
        print(f"Size: {size_mb:.2f} MB")
    else:
        print(f"Size: {size_kb:.2f} KB")
    print()
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Integrity check
        print("Running integrity check...")
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()[0]
        if result == "ok":
            print("  Integrity: OK")
        else:
            print(f"  Integrity: FAILED - {result}")
            return False
        print()
        
        # Show statistics
        print("Database Statistics:")
        
        # Total shows
        cursor.execute("SELECT COUNT(*) FROM shows")
        total = cursor.fetchone()[0]
        print(f"  Total shows: {total:,}")
        
        if total > 0:
            # Date range
            cursor.execute("SELECT MIN(date), MAX(date) FROM shows")
            min_date, max_date = cursor.fetchone()
            print(f"  Date range: {min_date} to {max_date}")
            
            # Shows with ratings
            cursor.execute("SELECT COUNT(*) FROM shows WHERE avg_rating IS NOT NULL")
            rated = cursor.fetchone()[0]
            print(f"  Shows with ratings: {rated:,} ({rated/total*100:.1f}%)")
            
            # Average rating
            cursor.execute("SELECT AVG(avg_rating) FROM shows WHERE avg_rating IS NOT NULL")
            avg_rating = cursor.fetchone()[0]
            if avg_rating:
                print(f"  Average rating: {avg_rating:.2f}")
            
            # Top rated show
            cursor.execute("""
                SELECT date, venue, avg_rating 
                FROM shows 
                WHERE avg_rating IS NOT NULL 
                ORDER BY avg_rating DESC 
                LIMIT 1
            """)
            top_show = cursor.fetchone()
            if top_show:
                print(f"  Top rated: {top_show[0]} - {top_show[1]} ({top_show[2]})")
        
        print()
        
        # Schema info
        print(f"Schema version: {get_schema_info()['version']}")
        print()
        
        conn.close()
        
        print("=" * 60)
        print("VERIFICATION COMPLETE")
        print("=" * 60)
        print()
        
        return True
        
    except Exception as e:
        print(f"\nERROR: Verification failed")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    # When run directly, initialize database
    print("Running database initialization...\n")
    
    success = init_database()
    
    if success:
        print("Running verification...\n")
        verify_database()
