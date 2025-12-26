"""
Database Query Functions for DeadStream

This module provides functions to search and retrieve Grateful Dead shows
from the SQLite database. All functions return data in consistent formats
ready for use by the UI or other application components.

Query functions include:
- Search by identifier, date, date range, venue, year, state
- Get top rated shows
- Get shows on "this day in history"
- Statistical queries
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from .schema import DB_PATH


class DatabaseConnection:
    """Context manager for database connections"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        # Return rows as dictionaries instead of tuples
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


def row_to_dict(row: sqlite3.Row) -> Dict:
    """Convert SQLite Row object to dictionary"""
    return {key: row[key] for key in row.keys()}


# ============================================================================
# BASIC QUERIES - Get individual shows
# ============================================================================

def get_show_by_identifier(identifier: str) -> Optional[Dict]:
    """
    Get a specific show by its Archive.org identifier
    
    Args:
        identifier: Archive.org identifier (e.g., 'gd77-05-08.sbd.hicks.4982')
        
    Returns:
        Dictionary with show data, or None if not found
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT * FROM shows
            WHERE identifier = ?
        """, (identifier,))
        
        row = cursor.fetchone()
        return row_to_dict(row) if row else None


def get_show_by_date(date: str) -> List[Dict]:
    """
    Get all shows on a specific date
    
    Note: There may be multiple recordings of the same concert
    
    Args:
        date: Date in YYYY-MM-DD format (e.g., '1977-05-08')
        
    Returns:
        List of show dictionaries (may be empty)
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT * FROM shows
            WHERE date = ?
            ORDER BY avg_rating DESC
        """, (date,))
        
        return [row_to_dict(row) for row in cursor.fetchall()]


def get_random_show() -> Optional[Dict]:
    """
    Get a random show from the database
    
    Returns:
        Dictionary with show data
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT * FROM shows
            ORDER BY RANDOM()
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        return row_to_dict(row) if row else None


# ============================================================================
# DATE-BASED SEARCHES
# ============================================================================

def search_by_date_range(start_date: str, end_date: str) -> List[Dict]:
    """
    Get all shows within a date range
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        List of show dictionaries, sorted by date
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT * FROM shows
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC
        """, (start_date, end_date))
        
        return [row_to_dict(row) for row in cursor.fetchall()]


def search_by_year(year: int) -> List[Dict]:
    """
    Get all shows from a specific year
    
    Args:
        year: Year (e.g., 1977)
        
    Returns:
        List of show dictionaries, sorted by date
    """
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    return search_by_date_range(start_date, end_date)


def search_by_month(year: int, month: int) -> List[Dict]:
    """
    Get all shows from a specific month
    
    Args:
        year: Year (e.g., 1977)
        month: Month (1-12)
        
    Returns:
        List of show dictionaries, sorted by date
    """
    # Calculate last day of month
    if month == 12:
        end_month = 1
        end_year = year + 1
    else:
        end_month = month + 1
        end_year = year
    
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{end_year}-{end_month:02d}-01"
    
    return search_by_date_range(start_date, end_date)


def get_shows_by_month(year: int, month: int) -> List[Dict]:
    """
    Get all shows from a specific month.
    
    Args:
        year: Year (e.g., 1977)
        month: Month (1-12)
        
    Returns:
        List of show dictionaries, sorted by date
    """
    with DatabaseConnection() as cursor:
        # Calculate date range for month
        start_date = f"{year}-{month:02d}-01"
        
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        cursor.execute("""
            SELECT * FROM shows
            WHERE date >= ? AND date < ?
            ORDER BY date ASC
        """, (start_date, end_date))
        
        return [row_to_dict(row) for row in cursor.fetchall()]


def get_show_dates_for_year(year: int) -> List[str]:
    """
    Get all dates that have shows for a given year.
    Used by date browser to highlight dates in calendar.
    
    Args:
        year: Year to search (e.g., 1977)
        
    Returns:
        List of date strings in YYYY-MM-DD format
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT DISTINCT date FROM shows
            WHERE date LIKE ?
            ORDER BY date ASC
        """, (f"{year}%",))
        
        return [row[0] for row in cursor.fetchall()]


def get_on_this_day(month: int, day: int) -> List[Dict]:
    """
    Get all shows that occurred on this day in history (across all years)
    
    Args:
        month: Month (1-12)
        day: Day (1-31)
        
    Returns:
        List of show dictionaries, sorted by year (oldest first)
    """
    with DatabaseConnection() as cursor:
        # Use SQL pattern matching for MM-DD
        date_pattern = f"%-{month:02d}-{day:02d}"
        
        cursor.execute("""
            SELECT * FROM shows
            WHERE date LIKE ?
            ORDER BY date ASC
        """, (date_pattern,))
        
        return [row_to_dict(row) for row in cursor.fetchall()]


# ============================================================================
# VENUE-BASED SEARCHES
# ============================================================================

def search_by_venue(venue_name: str, exact_match: bool = False) -> List[Dict]:
    """
    Search for shows at a specific venue
    
    Args:
        venue_name: Venue name or partial name
        exact_match: If True, match exact name; if False, partial match
        
    Returns:
        List of show dictionaries, sorted by date
    """
    with DatabaseConnection() as cursor:
        if exact_match:
            cursor.execute("""
                SELECT * FROM shows
                WHERE venue = ?
                ORDER BY date ASC
            """, (venue_name,))
        else:
            # Case-insensitive partial match
            cursor.execute("""
                SELECT * FROM shows
                WHERE venue LIKE ?
                ORDER BY date ASC
            """, (f"%{venue_name}%",))
        
        return [row_to_dict(row) for row in cursor.fetchall()]


def search_by_state(state: str) -> List[Dict]:
    """
    Get all shows from a specific state
    
    Args:
        state: State abbreviation (e.g., 'CA', 'NY') or full name
        
    Returns:
        List of show dictionaries, sorted by date
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT * FROM shows
            WHERE state = ? OR state LIKE ?
            ORDER BY date ASC
        """, (state, f"%{state}%"))
        
        return [row_to_dict(row) for row in cursor.fetchall()]


def search_by_city(city: str) -> List[Dict]:
    """
    Get all shows from a specific city
    
    Args:
        city: City name (partial match supported)
        
    Returns:
        List of show dictionaries, sorted by date
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT * FROM shows
            WHERE city LIKE ?
            ORDER BY date ASC
        """, (f"%{city}%",))
        
        return [row_to_dict(row) for row in cursor.fetchall()]


# ============================================================================
# RATING-BASED SEARCHES
# ============================================================================

def get_top_rated_shows(limit: int = 50, min_reviews: int = 5) -> List[Dict]:
    """
    Get the highest-rated shows
    
    Args:
        limit: Maximum number of shows to return
        min_reviews: Minimum number of reviews required (filters out unreviewed shows)
        
    Returns:
        List of show dictionaries, sorted by rating (highest first)
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT * FROM shows
            WHERE num_reviews >= ?
            ORDER BY avg_rating DESC, num_reviews DESC
            LIMIT ?
        """, (min_reviews, limit))
        
        return [row_to_dict(row) for row in cursor.fetchall()]


def get_top_rated_by_year(year: int, limit: int = 10) -> List[Dict]:
    """
    Get the highest-rated shows from a specific year
    
    Args:
        year: Year (e.g., 1977)
        limit: Maximum number of shows to return
        
    Returns:
        List of show dictionaries, sorted by rating
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT * FROM shows
            WHERE date LIKE ?
            ORDER BY avg_rating DESC, num_reviews DESC
            LIMIT ?
        """, (f"{year}%", limit))
        
        return [row_to_dict(row) for row in cursor.fetchall()]


# ============================================================================
# STATISTICAL QUERIES
# ============================================================================

def get_show_count() -> int:
    """Get total number of shows in database"""
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT COUNT(*) FROM shows")
        return cursor.fetchone()[0]


def get_show_count_by_year() -> List[Tuple[str, int]]:
    """
    Get show count for each year
    
    Returns:
        List of tuples: [(year, count), ...]
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT substr(date, 1, 4) as year, COUNT(*) as count
            FROM shows
            GROUP BY year
            ORDER BY year
        """)
        
        return [(row[0], row[1]) for row in cursor.fetchall()]


def get_venue_count() -> int:
    """Get number of unique venues"""
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT COUNT(DISTINCT venue) FROM shows
            WHERE venue IS NOT NULL
        """)
        return cursor.fetchone()[0]


def get_most_played_venues(limit: int = 20) -> List[Tuple[str, int]]:
    """
    Get venues with the most shows
    
    Args:
        limit: Maximum number of venues to return
        
    Returns:
        List of tuples: [(venue_name, show_count), ...]
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT venue, COUNT(*) as count
            FROM shows
            WHERE venue IS NOT NULL
            GROUP BY venue
            ORDER BY count DESC
            LIMIT ?
        """, (limit,))
        
        return [(row[0], row[1]) for row in cursor.fetchall()]


def get_shows_by_state_stats() -> List[Tuple[str, int]]:
    """
    Get show count for each state
    
    Returns:
        List of tuples: [(state, count), ...] sorted by count descending
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT state, COUNT(*) as count
            FROM shows
            WHERE state IS NOT NULL
            GROUP BY state
            ORDER BY count DESC
        """)
        
        return [(row[0], row[1]) for row in cursor.fetchall()]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_date_range() -> Tuple[str, str]:
    """
    Get the earliest and latest show dates in the database
    
    Returns:
        Tuple of (earliest_date, latest_date) in YYYY-MM-DD format
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT MIN(date), MAX(date) FROM shows
        """)
        row = cursor.fetchone()
        return (row[0], row[1])


def get_years_with_shows() -> List[int]:
    """
    Get list of all years that have shows
    
    Returns:
        List of years as integers, sorted
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT DISTINCT substr(date, 1, 4) as year
            FROM shows
            ORDER BY year
        """)
        
        return [int(row[0]) for row in cursor.fetchall()]


# ============================================================================
# COMBINED SEARCH (for future search UI)
# ============================================================================

def search_shows(
    query: Optional[str] = None,
    year: Optional[int] = None,
    venue: Optional[str] = None,
    state: Optional[str] = None,
    min_rating: Optional[float] = None,
    limit: Optional[int] = None
) -> List[Dict]:
    """
    Flexible search with multiple criteria (all optional)
    
    Args:
        query: Text search in venue or city
        year: Filter by year
        venue: Filter by venue (partial match)
        state: Filter by state
        min_rating: Minimum average rating
        limit: Maximum results to return
        
    Returns:
        List of show dictionaries matching all criteria
    """
    conditions = []
    params = []
    
    if year:
        conditions.append("date LIKE ?")
        params.append(f"{year}%")
    
    if venue:
        conditions.append("venue LIKE ?")
        params.append(f"%{venue}%")
    
    if state:
        conditions.append("state = ?")
        params.append(state)
    
    if query:
        conditions.append("(venue LIKE ? OR city LIKE ?)")
        params.extend([f"%{query}%", f"%{query}%"])
    
    if min_rating:
        conditions.append("avg_rating >= ?")
        params.append(min_rating)
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    limit_clause = f"LIMIT {limit}" if limit else ""
    
    with DatabaseConnection() as cursor:
        cursor.execute(f"""
            SELECT * FROM shows
            WHERE {where_clause}
            ORDER BY date DESC
            {limit_clause}
        """, params)
        
        return [row_to_dict(row) for row in cursor.fetchall()]

    """
    Get all dates that have shows for a given year.
    
    Args:
        year: Year to search (e.g., 1977)
        
    Returns:
        List of date strings in YYYY-MM-DD format
    """
    with DatabaseConnection() as cursor:
        cursor.execute("""
            SELECT DISTINCT date FROM shows
            WHERE date LIKE ?
            ORDER BY date ASC
        """, (f"{year}%",))
        
        return [row[0] for row in cursor.fetchall()]