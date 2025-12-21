#!/usr/bin/env python3
"""
Internet Archive API Client
Simple client for searching the Grateful Dead collection
"""

import requests
from typing import List, Dict, Optional


class ArchiveClient:
    """Client for Internet Archive Grateful Dead collection"""
    
    # API endpoints
    BASE_SEARCH_URL = "https://archive.org/advancedsearch.php"
    BASE_METADATA_URL = "https://archive.org/metadata"
    BASE_DOWNLOAD_URL = "https://archive.org/download"
    
    def __init__(self, timeout: int = 10):
        """
        Initialize the Archive client
        
        Args:
            timeout: Request timeout in seconds (default: 10)
        """
        self.timeout = timeout
    
    def search_shows(
        self, 
        query: str, 
        fields: str = 'identifier,title,date,venue,coverage,avg_rating',
        max_results: int = 100,
        sort: str = 'date asc'
    ) -> List[Dict]:
        """
        Search for shows in the Grateful Dead collection
        
        Args:
            query: Search query (e.g., 'date:1977-05-08' or 'year:1977')
            fields: Comma-separated list of fields to return
            max_results: Maximum number of results (default: 100)
            sort: Sort order (default: 'date asc')
        
        Returns:
            List of show dictionaries
        
        Raises:
            requests.exceptions.RequestException: On network errors
        """
        # Build the full query
        full_query = f'collection:GratefulDead AND {query}'
        
        # Set up parameters
        params = {
            'q': full_query,
            'fl': fields,
            'rows': max_results,
            'output': 'json',
            'sort': sort
        }
        
        # Make the request
        response = requests.get(
            self.BASE_SEARCH_URL,
            params=params,
            timeout=self.timeout
        )
        
        # Raise error for bad status codes
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Extract and return the shows
        return data['response']['docs']
    
    def get_show_count(self, query: str) -> int:
        """
        Get the total number of shows matching a query
        
        Args:
            query: Search query
        
        Returns:
            Total number of matching shows
        """
        params = {
            'q': f'collection:GratefulDead AND {query}',
            'rows': 0,  # We just want the count
            'output': 'json'
        }
        
        response = requests.get(
            self.BASE_SEARCH_URL,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        
        data = response.json()
        return data['response']['numFound']


# Convenience function for simple searches
def search_by_date(date: str) -> List[Dict]:
    """
    Quick search for shows on a specific date
    
    Args:
        date: Date in YYYY-MM-DD format (e.g., '1977-05-08')
    
    Returns:
        List of shows from that date
    """
    client = ArchiveClient()
    return client.search_shows(f'date:{date}')
