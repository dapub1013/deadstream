"""
Show List Widget for DeadStream Browse Interface - Phase 10D Restyled

Phase 10D Restyle:
- Uses Theme Manager for all colors/spacing
- Uses ConcertListItem component from Phase 10A
- Zero hardcoded values
- Maintains all Phase 7 functionality

Features:
- Scrollable list of Grateful Dead shows
- Date, venue, location display
- Rating and review count
- Source type badge
- Touch-friendly tap targets (60px minimum)

Can be used for all browse modes:
- All Shows
- Top Rated Shows
- Shows by Date
- Shows by Venue
- Shows by Year
- Search Results
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QFrame, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import Phase 10A components
from src.ui.styles.theme import Theme
from src.ui.components.concert_list_item import ConcertListItem
from src.ui.widgets.loading_spinner import LoadingIndicator


class ShowListWidget(QWidget):
    """
    Scrollable list of shows using ConcertListItem components - Phase 10D restyled

    Features:
    - Displays multiple shows in scrollable list
    - Touch-friendly scrolling
    - Loading state
    - Empty state
    - Automatic sizing
    - Uses Phase 10A ConcertListItem for each show

    Signals:
    - show_selected: Emitted when user selects a show to play
    """

    show_selected = pyqtSignal(dict)  # Emits show dictionary

    def __init__(self, parent=None):
        """Initialize show list widget"""
        super().__init__(parent)
        self.shows = []
        self.show_items = []  # Track ConcertListItem widgets
        self.setup_ui()

    def setup_ui(self):
        """Create list layout"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Theme.BG_PRIMARY};
                border: none;
            }}
        """)

        # Container widget for list items
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_MEDIUM,
            Theme.SPACING_LARGE,
            Theme.SPACING_MEDIUM
        )
        self.list_layout.setSpacing(Theme.SPACING_MEDIUM)
        self.list_layout.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.list_container)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def load_shows(self, shows):
        """
        Load and display shows in list

        Args:
            shows: List of show dictionaries from database
        """
        # Clear existing items
        self.clear_shows()

        # Store shows
        self.shows = shows

        # Create ConcertListItem for each show
        for i, show in enumerate(shows):
            # Prepare show data for ConcertListItem
            item_data = {
                'date': show.get('date', 'Unknown Date'),
                'venue': show.get('venue', 'Unknown Venue'),
                'location': self._format_location(show),
                'rating': show.get('avg_rating'),
                'source': show.get('source', '')
            }

            # Create ConcertListItem (Phase 10A component)
            show_divider = (i < len(shows) - 1)  # Show divider except for last item
            item = ConcertListItem(item_data, show_divider=show_divider)
            
            # Store original show data for signal emission
            item.original_show_data = show
            
            # Connect clicked signal
            item.clicked.connect(lambda data, s=show: self.on_item_clicked(s))

            # Add to layout
            self.list_layout.addWidget(item)
            self.show_items.append(item)

        print(f"[INFO] Loaded {len(shows)} shows into list")

    def _format_location(self, show):
        """Format location string from show data"""
        city = show.get('city', '')
        state = show.get('state', '')
        
        if city and state:
            return f"{city}, {state}"
        elif city:
            return city
        elif state:
            return state
        else:
            return ""

    def clear_shows(self):
        """Remove all show items from list"""
        # Remove all widgets from layout
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.shows = []
        self.show_items = []

    def on_item_clicked(self, show_data):
        """Handle item click - emit show_selected signal"""
        print(f"[INFO] Show clicked: {show_data.get('date')} - {show_data.get('venue')}")
        self.show_selected.emit(show_data)

    def set_empty_state(self, message="No shows found"):
        """
        Display empty state message

        Args:
            message: Message to display when no shows available
        """
        self.clear_shows()

        # Create empty state label
        empty_label = QFrame()
        empty_layout = QVBoxLayout(empty_label)
        empty_layout.setContentsMargins(
            Theme.SPACING_XLARGE,
            Theme.SPACING_XXLARGE,
            Theme.SPACING_XLARGE,
            Theme.SPACING_XXLARGE
        )
        empty_layout.setAlignment(Qt.AlignCenter)

        # Icon placeholder (using text since we can't use unicode)
        icon_label = QFont()
        icon_label.setPointSize(48)
        
        # Message text
        msg_label = QFont()
        msg_label.setPointSize(Theme.BODY_LARGE)
        
        message_widget = QFrame()
        message_widget.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_CARD};
                border-radius: 16px;
                padding: {Theme.SPACING_XLARGE}px;
            }}
        """)
        
        msg_layout = QVBoxLayout(message_widget)
        msg_layout.setAlignment(Qt.AlignCenter)
        msg_layout.setSpacing(Theme.SPACING_MEDIUM)
        
        # Large "No Results" text
        no_results = QFont()
        no_results.setFamily(Theme.FONT_FAMILY)
        no_results.setPointSize(Theme.HEADER_SMALL)
        no_results.setBold(True)
        
        from PyQt5.QtWidgets import QLabel
        title_label = QLabel("No Shows Found")
        title_label.setFont(no_results)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        msg_layout.addWidget(title_label)
        
        # Subtitle message
        subtitle = QFont()
        subtitle.setFamily(Theme.FONT_FAMILY)
        subtitle.setPointSize(Theme.BODY_MEDIUM)
        
        subtitle_label = QLabel(message)
        subtitle_label.setFont(subtitle)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        subtitle_label.setWordWrap(True)
        msg_layout.addWidget(subtitle_label)
        
        empty_layout.addWidget(message_widget)
        self.list_layout.addWidget(empty_label)

    def set_loading_state(self):
        """Display animated loading indicator"""
        self.clear_shows()

        # Create loading indicator with spinner
        loading_container = QFrame()
        loading_container_layout = QVBoxLayout(loading_container)
        loading_container_layout.setContentsMargins(
            Theme.SPACING_XLARGE,
            Theme.SPACING_XXLARGE,
            Theme.SPACING_XLARGE,
            Theme.SPACING_XXLARGE
        )
        loading_container_layout.setAlignment(Qt.AlignCenter)

        # Add animated loading indicator
        self.loading_indicator = LoadingIndicator(self, message="Loading shows...")
        self.loading_indicator.start()
        loading_container_layout.addWidget(self.loading_indicator)

        self.list_layout.addWidget(loading_container)


# Test code
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from src.database.queries import get_top_rated_shows
    
    app = QApplication(sys.argv)
    
    # Apply Theme global stylesheet
    app.setStyleSheet(Theme.get_global_stylesheet())
    
    # Create widget
    widget = ShowListWidget()
    widget.setWindowTitle("Show List Widget Test - Phase 10D Restyled")
    widget.resize(800, 600)
    
    # Test handler
    def handle_show_selected(show):
        print(f"\n[TEST] Show selected: {show['date']} - {show['venue']}")
    
    widget.show_selected.connect(handle_show_selected)
    
    # Load some test data
    try:
        shows = get_top_rated_shows(limit=20, min_reviews=5)
        if shows:
            widget.load_shows(shows)
            print(f"[TEST] Loaded {len(shows)} shows for testing")
        else:
            widget.set_empty_state("No shows in database")
            print("[TEST] No shows found - showing empty state")
    except Exception as e:
        print(f"[TEST] Error loading shows: {e}")
        widget.set_empty_state("Error loading test data")
    
    widget.show()
    sys.exit(app.exec_())
