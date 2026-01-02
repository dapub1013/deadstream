"""
UI Widgets Package for DeadStream

Reusable UI components for the application.

Current widgets in src/ui/widgets/:
- ShowListWidget: Scrollable list of show cards
- ShowCard: Individual show display card (browse list)
- Phase10AShowCard: Enhanced show card with animations (Phase 10A)
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
from .show_card import ShowCard as Phase10AShowCard

# Export widgets from this package
__all__ = [
    'ShowListWidget',
    'ShowCard',
    'Phase10AShowCard',
    'TrackInfoWidget',
]
from src.ui.widgets.setlist import SetlistWidget
from .concert_info import ConcertInfoWidget