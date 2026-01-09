#!/usr/bin/env python3
"""
Venue Browser Widget - Polished Placeholder (Phase 10E.4 Option B)

Displays a list of legendary Grateful Dead venues with show counts.
Clicking a venue triggers a search for shows at that venue.

This is a polished placeholder - full venue browser with state grouping,
advanced filtering, and search will be implemented in a future phase.

Features:
- List of 20+ legendary venues
- Show count per venue (from database)
- Click to see shows at venue
- Professional "Coming Soon" message for advanced features
- Touch-friendly layout (60px+ touch targets)
- Theme Manager integration

Signal Architecture:
- venue_selected(str): Emitted when user clicks a venue (emits venue name)

ASCII-only. No emojis or unicode characters.
"""

import sys
import os

# Path manipulation for subdirectory imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from src.ui.styles.theme import Theme
from src.database.queries import get_show_count_by_venue


class VenueBrowser(QWidget):
    """
    Polished placeholder for venue browsing.

    Displays legendary Grateful Dead venues with show counts.
    Clicking a venue emits a signal for the parent screen to handle.

    Signals:
        venue_selected(str): Emitted when user clicks a venue name
    """

    venue_selected = pyqtSignal(str)  # Emits venue name

    # Legendary Grateful Dead venues
    LEGENDARY_VENUES = [
        "Fillmore West",
        "Fillmore East",
        "Winterland Arena",
        "Capitol Theatre",
        "Barton Hall",
        "Red Rocks Amphitheatre",
        "Madison Square Garden",
        "The Warfield",
        "Greek Theatre",
        "Radio City Music Hall",
        "Nassau Coliseum",
        "The Spectrum",
        "Boston Garden",
        "Chicago Auditorium",
        "Memorial Auditorium",
        "Felt Forum",
        "Fox Theatre",
        "Paramount Theatre",
        "Avalon Ballroom",
        "Carousel Ballroom",
        "Fillmore Auditorium",
        "Shrine Auditorium",
        "Hollywood Bowl",
        "Cow Palace"
    ]

    def __init__(self, db_path=None, parent=None):
        """
        Initialize venue browser.

        Args:
            db_path: Path to shows database (optional, for show counts)
            parent: Parent widget
        """
        super().__init__(parent)
        self.db_path = db_path
        self.venue_data = {}  # venue_name -> show_count
        self._setup_ui()
        self._load_venue_data()

    def _setup_ui(self):
        """Create venue browser layout"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Theme.SPACING_LARGE, Theme.SPACING_LARGE,
                                       Theme.SPACING_LARGE, Theme.SPACING_LARGE)
        main_layout.setSpacing(Theme.SPACING_MEDIUM)

        # Header
        header_label = QLabel("Browse by Venue")
        header_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                padding-bottom: {Theme.SPACING_SMALL}px;
                border-bottom: 2px solid {Theme.BORDER_SUBTLE};
            }}
        """)
        main_layout.addWidget(header_label)

        # Description
        desc_label = QLabel("Select a legendary venue to see all shows performed there")
        desc_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
                padding: {Theme.SPACING_SMALL}px 0px;
            }}
        """)
        desc_label.setWordWrap(True)
        main_layout.addWidget(desc_label)

        # Venue list
        self.venue_list = QListWidget()
        self.venue_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {Theme.BG_CARD};
                border: 1px solid {Theme.BORDER_SUBTLE};
                border-radius: 8px;
                padding: {Theme.SPACING_SMALL}px;
                font-size: {Theme.BODY_MEDIUM}px;
            }}
            QListWidget::item {{
                padding: {Theme.SPACING_MEDIUM}px;
                border-bottom: 1px solid {Theme.BORDER_SUBTLE};
                border-radius: 4px;
                min-height: {Theme.BUTTON_HEIGHT}px;
            }}
            QListWidget::item:hover {{
                background-color: {Theme._lighten_color(Theme.BG_CARD, 10)};
            }}
            QListWidget::item:selected {{
                background-color: {Theme.ACCENT_BLUE};
                color: {Theme.TEXT_PRIMARY};
                font-weight: {Theme.WEIGHT_BOLD};
            }}
        """)
        self.venue_list.itemClicked.connect(self._on_venue_clicked)
        main_layout.addWidget(self.venue_list)

        # Coming soon message
        coming_soon_frame = QFrame()
        coming_soon_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_PANEL_DARK};
                border: 1px solid {Theme.ACCENT_BLUE};
                border-radius: 8px;
                padding: {Theme.SPACING_MEDIUM}px;
            }}
        """)
        coming_soon_layout = QVBoxLayout(coming_soon_frame)
        coming_soon_layout.setSpacing(Theme.SPACING_SMALL)

        coming_soon_title = QLabel("Full Venue Browser Coming Soon")
        coming_soon_title.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.ACCENT_BLUE};
            }}
        """)
        coming_soon_layout.addWidget(coming_soon_title)

        coming_soon_text = QLabel(
            "Future features will include:\n"
            "  - Venues grouped by state/region\n"
            "  - Search and filter capabilities\n"
            "  - Venue history and statistics\n"
            "  - Map view of tour routes"
        )
        coming_soon_text.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_SMALL}px;
                color: {Theme.TEXT_SECONDARY};
                line-height: 1.6;
            }}
        """)
        coming_soon_layout.addWidget(coming_soon_text)

        main_layout.addWidget(coming_soon_frame)

    def _load_venue_data(self):
        """Load venue list with show counts from database"""
        if not self.db_path:
            # No database - just show venues without counts
            self._populate_venue_list_simple()
            return

        try:
            # Get show counts for each venue
            for venue in self.LEGENDARY_VENUES:
                count = get_show_count_by_venue(self.db_path, venue)
                self.venue_data[venue] = count

            # Populate list with counts
            self._populate_venue_list_with_counts()
            print(f"[INFO] Loaded {len(self.venue_data)} legendary venues from database")

        except Exception as e:
            print(f"[ERROR] Failed to load venue data: {e}")
            # Fallback to simple list
            self._populate_venue_list_simple()

    def _populate_venue_list_simple(self):
        """Populate venue list without show counts"""
        self.venue_list.clear()

        for venue in sorted(self.LEGENDARY_VENUES):
            item = QListWidgetItem(venue)
            item.setData(Qt.UserRole, venue)

            # Style item
            font = QFont()
            font.setPointSize(Theme.BODY_MEDIUM)
            item.setFont(font)

            self.venue_list.addItem(item)

        print(f"[INFO] Populated venue list with {len(self.LEGENDARY_VENUES)} venues (no counts)")

    def _populate_venue_list_with_counts(self):
        """Populate venue list with show counts"""
        self.venue_list.clear()

        # Sort venues by show count (descending)
        sorted_venues = sorted(
            self.venue_data.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for venue, count in sorted_venues:
            if count > 0:  # Only show venues with shows
                # Format: "Fillmore West (57 shows)"
                item_text = f"{venue} ({count} show{'s' if count != 1 else ''})"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, venue)

                # Style item
                font = QFont()
                font.setPointSize(Theme.BODY_MEDIUM)
                item.setFont(font)

                self.venue_list.addItem(item)

        # If no venues have shows, fall back to simple list
        if self.venue_list.count() == 0:
            print("[WARN] No shows found for legendary venues, showing all venues")
            self._populate_venue_list_simple()

    def _on_venue_clicked(self, item):
        """Handle venue click"""
        venue_name = item.data(Qt.UserRole)
        if venue_name:
            print(f"[INFO] Venue selected: {venue_name}")
            self.venue_selected.emit(venue_name)

    def refresh(self):
        """Refresh venue list (reload data from database)"""
        print("[INFO] Refreshing venue browser...")
        self.venue_data.clear()
        self._load_venue_data()


# Standalone test code
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # Apply global theme
    app.setStyleSheet(Theme.get_global_stylesheet())

    # Test window
    window = QWidget()
    window.setWindowTitle("Venue Browser Test")
    window.setGeometry(100, 100, 900, 700)
    window.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")

    layout = QVBoxLayout(window)

    # Create VenueBrowser (without database for testing)
    browser = VenueBrowser()
    layout.addWidget(browser)

    # Test signal
    def on_venue_selected(venue):
        print(f"[TEST] Venue selected signal: {venue}")

    browser.venue_selected.connect(on_venue_selected)

    window.show()
    sys.exit(app.exec_())
