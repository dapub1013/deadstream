"""
Internet Archive API module

Provides functions for searching and retrieving Grateful Dead shows.
"""

from .metadata import get_metadata, get_show_info, extract_audio_files
from .search import search_shows, search_by_date, search_by_year, search_by_venue

__all__ = [
    'get_metadata',
    'get_show_info', 
    'extract_audio_files',
    'search_shows',
    'search_by_date',
    'search_by_year',
    'search_by_venue',
]
