"""
UI Widgets Package for DeadStream

Reusable UI components for the application.

Current widgets in src/ui/widgets/:
- ShowListWidget: Scrollable list of show cards
- ShowCard: Individual show display card
- TrackInfoWidget: Now playing track information display

Note: Settings widgets (NetworkWidget, AudioWidget, etc.) are in 
src/settings/widgets/ and should be imported from there.

Future widgets:
- DatePicker
- VenueFilter
- YearSelector
- PlaybackControls
- ProgressBar
"""

# Import widgets from THIS package (src/ui/widgets/)
from .show_list import ShowListWidget, ShowCard
from .track_info import TrackInfoWidget

# Export widgets from this package
__all__ = [
    'ShowListWidget',
    'ShowCard',
    'TrackInfoWidget',
]
