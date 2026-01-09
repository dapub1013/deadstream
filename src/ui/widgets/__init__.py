"""
DeadStream UI Widgets Package

Phase 10D Update: Minimal imports to avoid errors.
Individual widgets are imported directly where needed.
"""

# Only import core Phase 10D restyled widgets
from .show_list import ShowListWidget
from .date_browser import DateBrowser  
from .search_widget import SearchWidget

__all__ = [
    'ShowListWidget',
    'DateBrowser',
    'SearchWidget',
]
