"""
UI Widgets Package for DeadStream

Reusable UI components for the application.

Current widgets:
- ShowListWidget: Scrollable list of show cards
- ShowCard: Individual show display card

Future widgets:
- DatePicker
- VenueFilter
- YearSelector
- PlaybackControls
- ProgressBar
"""

from .show_list import ShowListWidget, ShowCard
from .audio_settings_widget import AudioSettingsWidget

__all__ = [
    'ShowListWidget',
    'ShowCard',
    'DateBrowser',
    'YearBrowser',
    'SearchWidget',
    'NetworkSettingsWidget',
    'AboutWidget',
    'AudioSettingsWidget'  # Add this
]