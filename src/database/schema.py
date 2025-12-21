"""
Database schema definition for DeadStream.

This module defines the SQLite database structure for storing Grateful Dead
show information. The schema is designed to support browsing and searching
shows by date, venue, year, and rating.

Schema Design Philosophy:
- Shows-only table for Phase 3 (tracks deferred to Phase 4)
- Minimal fields for initial population (lazy load additional metadata)
- Indexes on common search fields for performance
- Simple, maintainable structure

Author: DeadStream Project
Created: December 2025
Phase: 3.1 - Database Schema Design
"""
import os

# Database file path
# Location: ~/deadstream/data/shows.db
DB_PATH = os.path.join(
    os.path.dirname(__file__),  # src/database/
    '..',  # src/
    '..',  # deadstream/
    'data',
    'shows.db'
)

# SQL statement to create the shows table
CREATE_SHOWS_TABLE = """
CREATE TABLE IF NOT EXISTS shows (
    -- Primary identifier from Internet Archive
    -- Example: 'gd1977-05-08.sbd.hicks.4982.sbeok.shnf'
    identifier TEXT PRIMARY KEY,
    
    -- Show date in YYYY-MM-DD format
    -- Example: '1977-05-08'
    date TEXT NOT NULL,
    
    -- Venue name
    -- Example: 'Barton Hall, Cornell University'
    venue TEXT,
    
    -- City where show took place
    -- Parsed from 'coverage' field in API response
    -- Example: 'Ithaca'
    city TEXT,
    
    -- State abbreviation
    -- Parsed from 'coverage' field in API response
    -- Example: 'NY'
    state TEXT,
    
    -- Community rating (0.0 to 5.0)
    -- Used for sorting and displaying top shows
    -- NULL if no ratings exist
    avg_rating REAL,
    
    -- Number of community reviews
    -- Indicates popularity and data reliability
    -- NULL if no reviews exist
    num_reviews INTEGER,
    
    -- Recording source type: 'sbd', 'aud', or 'matrix'
    -- Initially NULL, lazy loaded when needed for selection (Phase 5)
    source_type TEXT,
    
    -- Name of taper who recorded the show
    -- Initially NULL, lazy loaded when needed
    -- Example: 'Charlie Miller'
    taper TEXT,
    
    -- Timestamp of last database update for this show
    -- ISO 8601 format: 'YYYY-MM-DDTHH:MM:SS'
    -- Example: '2025-12-20T15:30:00'
    last_updated TEXT
);
"""

# Indexes for common search patterns
# These make queries fast by allowing SQLite to quickly find matching rows

# Index on date - for browsing by specific date or date range
CREATE_DATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_date ON shows(date);
"""

# Index on venue - for browsing shows at specific venues
CREATE_VENUE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_venue ON shows(venue);
"""

# Index on rating - for sorting by rating and finding top shows
CREATE_RATING_INDEX = """
CREATE INDEX IF NOT EXISTS idx_rating ON shows(avg_rating);
"""

# Index on year - for browsing by year
# Uses substr(date, 1, 4) to extract year from 'YYYY-MM-DD' format
# Example: '1977-05-08' -> '1977'
CREATE_YEAR_INDEX = """
CREATE INDEX IF NOT EXISTS idx_year ON shows(substr(date, 1, 4));
"""

# Index on state - for browsing by location
CREATE_STATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_state ON shows(state);
"""

# Combined index on date and rating - for "best shows of date/year" queries
CREATE_DATE_RATING_INDEX = """
CREATE INDEX IF NOT EXISTS idx_date_rating ON shows(date, avg_rating DESC);
"""

# List of all SQL statements needed to create the database
# Executed in order by the initialization function
SCHEMA_SQL = [
    CREATE_SHOWS_TABLE,
    CREATE_DATE_INDEX,
    CREATE_VENUE_INDEX,
    CREATE_RATING_INDEX,
    CREATE_YEAR_INDEX,
    CREATE_STATE_INDEX,
    CREATE_DATE_RATING_INDEX
]


def get_schema_version():
    """
    Return the current schema version.
    
    This version number should be incremented whenever the schema changes.
    Used for database migrations in future phases.
    
    Returns:
        str: Schema version in format 'X.Y'
    """
    return "1.0"


def get_schema_info():
    """
    Return human-readable information about the schema.
    
    Useful for documentation and debugging.
    
    Returns:
        dict: Schema information including version, tables, and indexes
    """
    return {
        "version": get_schema_version(),
        "tables": ["shows"],
        "indexes": [
            "idx_date",
            "idx_venue", 
            "idx_rating",
            "idx_year",
            "idx_state",
            "idx_date_rating"
        ],
        "primary_keys": ["shows.identifier"],
        "foreign_keys": [],  # None in Phase 3 (will add tracks table in Phase 4)
        "estimated_size": "5-10 MB for ~15,000 shows"
    }


if __name__ == "__main__":
    # Print schema information when run directly
    import json
    
    print("DeadStream Database Schema")
    print("=" * 50)
    print()
    print("Schema Information:")
    print(json.dumps(get_schema_info(), indent=2))
    print()
    print("SQL Statements:")
    print("-" * 50)
    for i, sql in enumerate(SCHEMA_SQL, 1):
        print(f"\n{i}. {sql.split('(')[0].strip()}")
        print(sql)
