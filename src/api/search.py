#!/usr/bin/env python3
"""
Internet Archive Search API

This module provides functions for searching the Grateful Dead collection.
It wraps the ArchiveClient to provide a simple functional interface.
"""

from typing import List, Dict, Optional
from .archive_client import ArchiveClient


# Create a shared client instance
_client = ArchiveClient()


def search_shows(query: str, 
                fields: str = 'identifier,title,date,venue,coverage,avg_rating',
                rows: int = 100,
                sort: str = 'date asc') -> List[Dict]:
    """
    Search for shows in the Grateful Dead collection.
    
    Args:
        query: Search query (e.g., 'date:1977-05-08' or 'year:1977')
        fields: Comma-separated list of fields to return
        rows: Maximum number of results
        sort: Sort order
        
    Returns:
        List of show dictionaries
        
    Example:
        shows = search_shows('date:1977-05-08')
        for show in shows:
            print(show['identifier'], show['date'])
    """
    return _client.search_shows(
        query=query,
        fields=fields,
        max_results=rows,
        sort=sort
    )


def search_by_date(date: str) -> List[Dict]:
    """
    Search for all shows on a specific date.
    
    Args:
        date: Date in YYYY-MM-DD format
        
    Returns:
        List of shows on that date
    """
    query = f'date:{date}'
    return search_shows(query)


def search_by_date_range(start_date: str, end_date: str) -> List[Dict]:
    """
    Search for shows within a date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        List of shows in date range
    """
    query = f'date:[{start_date} TO {end_date}]'
    return search_shows(query, rows=500)


def search_by_venue(venue_name: str, exact_match: bool = False) -> List[Dict]:
    """
    Search for shows at a specific venue.
    
    Args:
        venue_name: Name of venue
        exact_match: If True, match exact venue name
        
    Returns:
        List of shows at venue
    """
    if exact_match:
        query = f'venue:"{venue_name}"'
    else:
        query = f'venue:{venue_name}'
    
    return search_shows(query, rows=500)


def search_by_year(year: int) -> List[Dict]:
    """
    Search for all shows from a specific year.
    
    Args:
        year: Year (e.g., 1977)
        
    Returns:
        List of shows from that year
    """
    query = f'year:{year}'
    return search_shows(query, rows=500)


def search_by_month(year: int, month: int) -> List[Dict]:
    """
    Search for shows from a specific month.
    
    Args:
        year: Year (e.g., 1977)
        month: Month (1-12)
        
    Returns:
        List of shows from that month
    """
    # Format month as MM
    month_str = f"{month:02d}"
    query = f'date:{year}-{month_str}-*'
    return search_shows(query, rows=500)


# Example usage
if __name__ == '__main__':
    print("Testing search functions...\n")
    
    # Search for Cornell '77
    print("Searching for Cornell '77 (1977-05-08)...")
    shows = search_by_date('1977-05-08')
    print(f"Found {len(shows)} recordings")
    
    if shows:
        print("\nFirst result:")
        show = shows[0]
        print(f"  Identifier: {show.get('identifier')}")
        print(f"  Title: {show.get('title')}")
        print(f"  Date: {show.get('date')}")
        print(f"  Venue: {show.get('venue')}")
    
    # Search for May 1977
    print("\n\nSearching for May 1977...")
    shows = search_by_month(1977, 5)
    print(f"Found {len(shows)} shows in May 1977")
