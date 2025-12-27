#!/usr/bin/env python3
"""
Browse Screen for DeadStream - WITH YEAR SELECTOR

This version includes Tasks 7.1-7.4.

Completed features:
- Task 7.1: Show list view with top-rated shows
- Task 7.2: Date browser (calendar-based browsing)
- Task 7.3: Venue filter
- Task 7.4: Year selector (NEW)

Future tasks:
- Task 7.5: Search functionality
- Task 7.6: Random show button
"""

import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QDialog, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import database queries
from src.database.queries import (
    get_top_rated_shows, get_most_played_venues, 
    search_by_venue, get_show_by_date, search_by_year, get_show_count
)

# Import widgets
from src.ui.widgets.show_list import ShowListWidget
from src.ui.widgets.date_browser import DateBrowser
from src.ui.widgets.year_browser import YearBrowser


class BrowseScreen(QWidget):
    """
    Browse screen for finding and selecting shows
    
    Layout (from UI spec):
    - Left panel (40%): Navigation and browse modes
    - Right panel (60%): Show list with header
    
    Browse modes:
    - Top Rated (default)
    - Browse by Date (Task 7.2)
    - Browse by Venue (Task 7.3)
    - Browse by Year (Task 7.4 - NEW)
    
    Signals:
    - show_selected: Emitted when user selects a show to play
    """
    
    show_selected = pyqtSignal(dict)  # Emits show dictionary
    
    def __init__(self, parent=None):
        """Initialize browse screen"""
        super().__init__(parent)
        self.current_shows = []
        self.setup_ui()
        self.load_default_shows()
    
    def setup_ui(self):
        """Create browse screen layout"""
        # Main horizontal layout (left panel + right panel)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left Panel (40%) - Navigation
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, stretch=4)
        
        # Right Panel (60%) - Show list
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, stretch=6)
        
        self.setLayout(main_layout)
    
    def create_left_panel(self):
        """Create left navigation panel with browse modes"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-right: 2px solid #374151;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Header
        header = QLabel("Browse Shows")
        header.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
        """)
        layout.addWidget(header)
        
        # Browse mode buttons
        self.create_browse_mode_buttons(layout)
        
        layout.addStretch()
        
        # Stats section
        show_count = get_show_count()
        
        stats_label = QLabel(f"{show_count:,} shows available")
        stats_label.setStyleSheet("""
            color: #6b7280;
            font-size: 14px;
            padding: 12px;
            background-color: #111827;
            border-radius: 8px;
        """)
        layout.addWidget(stats_label)
        
        return panel
    
    def create_browse_mode_buttons(self, layout):
        """Create buttons for different browse modes"""
        
        # Top Rated (default view)
        top_rated_btn = QPushButton("Top Rated Shows")
        top_rated_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 16px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #6b7280;
            }
        """)
        top_rated_btn.clicked.connect(self.load_default_shows)
        layout.addWidget(top_rated_btn)
        
        # Date Browser (Task 7.2)
        date_btn = QPushButton("Browse by Date")
        date_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 16px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        date_btn.clicked.connect(self.show_date_browser)
        layout.addWidget(date_btn)
        
        # Venue Browser (Task 7.3)
        venue_btn = QPushButton("Browse by Venue")
        venue_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 16px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        venue_btn.clicked.connect(self.show_venue_browser)
        layout.addWidget(venue_btn)
        
        # Year Browser (Task 7.4 - NEW)
        year_btn = QPushButton("Browse by Year")
        year_btn.setStyleSheet("""
            QPushButton {
                background-color: #a855f7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 16px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #9333ea;
            }
            QPushButton:pressed {
                background-color: #7e22ce;
            }
        """)
        year_btn.clicked.connect(self.show_year_browser)
        layout.addWidget(year_btn)
    
    def create_right_panel(self):
        """Create right panel with header and show list"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #000000;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header section (we'll update the labels when loading shows)
        self.header_widget = QWidget()
        self.header_widget.setStyleSheet("background-color: #1f2937;")
        header_layout = QVBoxLayout(self.header_widget)
        header_layout.setContentsMargins(24, 20, 24, 20)
        header_layout.setSpacing(8)
        
        # Title label (will be updated)
        self.header_title = QLabel("Top Rated Shows")
        self.header_title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(self.header_title)
        
        # Subtitle label (will be updated)
        self.header_subtitle = QLabel("Showing the highest-rated performances from the collection")
        self.header_subtitle.setStyleSheet("""
            color: #9ca3af;
            font-size: 14px;
        """)
        self.header_subtitle.setWordWrap(True)
        header_layout.addWidget(self.header_subtitle)
        
        layout.addWidget(self.header_widget)
        
        # Show list widget (from Task 7.1)
        self.show_list = ShowListWidget()
        self.show_list.show_selected.connect(self.on_show_selected)
        
        layout.addWidget(self.show_list, stretch=1)
        
        return panel
    
    def update_header(self, title, subtitle):
        """Update the header labels"""
        self.header_title.setText(title)
        self.header_subtitle.setText(subtitle)
    
    # ========================================================================
    # BROWSE MODE HANDLERS
    # ========================================================================
    
    def load_default_shows(self):
        """Load top-rated shows (default view)"""
        try:
            self.show_list.set_loading_state()
            
            shows = get_top_rated_shows(limit=50, min_reviews=5)
            
            if shows:
                self.current_shows = shows
                self.update_header(
                    "Top Rated Shows",
                    f"Showing {len(shows)} highest-rated performances"
                )
                self.show_list.load_shows(shows)
                print(f"[OK] Loaded {len(shows)} top-rated shows")
            else:
                self.update_header("No Shows Found", "No rated shows in database")
                self.show_list.set_empty_state("No rated shows found")
                print("[WARN] No shows found in database")
                
        except Exception as e:
            print(f"[ERROR] Failed to load shows: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", "Failed to load shows")
            self.show_list.set_empty_state("Error loading shows")
    
    def show_date_browser(self):
        """Show date browser dialog (Task 7.2)"""
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Browse by Date")
        dialog.setModal(True)
        dialog.setMinimumSize(800, 600)
        
        # Apply dark theme
        dialog.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
        """)
        
        # Layout
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add date browser widget
        date_browser = DateBrowser()
        
        # Connect date selection signal
        def on_date_selected(date_str):
            """Handle date selection from calendar"""
            dialog.accept()
            self.load_shows_by_date(date_str)
        
        date_browser.date_selected.connect(on_date_selected)
        layout.addWidget(date_browser)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        close_btn.clicked.connect(dialog.reject)
        layout.addWidget(close_btn)
        
        # Show dialog
        dialog.exec_()
    
    def show_venue_browser(self):
        """Show venue browser dialog (Task 7.3)"""
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Browse by Venue")
        dialog.setModal(True)
        dialog.setMinimumSize(600, 700)
        
        # Apply dark theme
        dialog.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
        """)
        
        # Layout
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Select a Venue")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Subtitle
        subtitle = QLabel("Showing most-played venues")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #9ca3af; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Get venues
        venues = get_most_played_venues(limit=100)
        
        # Venue list
        venue_list = QListWidget()
        venue_list.setStyleSheet("""
            QListWidget {
                background-color: #1f2937;
                border: 1px solid #374151;
                border-radius: 8px;
                color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #374151;
            }
            QListWidget::item:hover {
                background-color: #374151;
            }
            QListWidget::item:selected {
                background-color: #3b82f6;
            }
        """)
        
        for venue_name, show_count in venues:
            item = QListWidgetItem(f"{venue_name} ({show_count} shows)")
            item.setData(Qt.UserRole, venue_name)  # Store venue name
            venue_list.addItem(item)
        
        layout.addWidget(venue_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        close_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(close_btn)
        
        button_layout.addStretch()
        
        select_btn = QPushButton("Select Venue")
        select_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
        """)
        select_btn.setEnabled(False)  # Disabled until selection
        
        def on_selection_changed():
            """Enable button when venue selected"""
            select_btn.setEnabled(venue_list.currentItem() is not None)
        
        venue_list.itemSelectionChanged.connect(on_selection_changed)
        
        def on_select():
            """Load shows for selected venue"""
            current_item = venue_list.currentItem()
            if current_item:
                venue_name = current_item.data(Qt.UserRole)
                dialog.accept()
                self.load_shows_by_venue(venue_name)
        
        select_btn.clicked.connect(on_select)
        venue_list.itemDoubleClicked.connect(lambda: on_select())  # Double-click to select
        
        button_layout.addWidget(select_btn)
        layout.addLayout(button_layout)
        
        # Show dialog
        dialog.exec_()
    
    def show_year_browser(self):
        """Show year browser dialog (Task 7.4 - NEW)"""
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Browse by Year")
        dialog.setModal(True)
        dialog.setMinimumSize(800, 700)
        
        # Apply dark theme
        dialog.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
        """)
        
        # Layout
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add year browser widget
        year_browser = YearBrowser()
        
        # Connect year selection signal
        def on_year_selected(year):
            """Handle year selection from grid"""
            dialog.accept()
            self.load_shows_by_year(year)
        
        year_browser.year_selected.connect(on_year_selected)
        layout.addWidget(year_browser)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        close_btn.clicked.connect(dialog.reject)
        layout.addWidget(close_btn)
        
        # Show dialog
        dialog.exec_()
    
    def load_shows_by_date(self, date_str):
        """Load and display shows from a specific date (Task 7.2)"""
        
        try:
            self.show_list.set_loading_state()
            
            # Get shows for this date
            shows = get_show_by_date(date_str)
            
            if not shows:
                # No shows found
                self.update_header(
                    "No Shows Found",
                    f"No shows on {date_str}"
                )
                self.show_list.set_empty_state(f"No shows on {date_str}")
                return
            
            # Update header
            self.update_header(
                f"Shows on {date_str}",
                f"{len(shows)} recording(s) from this date"
            )
            
            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows
            
            print(f"[OK] Loaded {len(shows)} shows from {date_str}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load date shows: {e}")
            self.update_header("Error", f"Failed to load shows for {date_str}")
            self.show_list.set_empty_state("Error loading shows")
    
    def load_shows_by_venue(self, venue_name):
        """Load and display shows from a specific venue (Task 7.3)"""
        
        try:
            self.show_list.set_loading_state()
            
            # Get shows for this venue
            shows = search_by_venue(venue_name, exact_match=False)
            
            if not shows:
                # No shows found
                self.update_header(
                    "No Shows Found",
                    f"No shows found at {venue_name}"
                )
                self.show_list.set_empty_state(f"No shows at {venue_name}")
                return
            
            # Update header
            self.update_header(
                f"{len(shows)} Shows at {venue_name}",
                "Sorted by date (oldest to newest)"
            )
            
            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows
            
            print(f"[OK] Loaded {len(shows)} shows from {venue_name}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load venue shows: {e}")
            self.update_header("Error", f"Failed to load shows for {venue_name}")
            self.show_list.set_empty_state("Error loading shows")
    
    def load_shows_by_year(self, year):
        """Load and display shows from a specific year (Task 7.4 - NEW)"""
        
        try:
            self.show_list.set_loading_state()
            
            # Get shows for this year
            shows = search_by_year(year)
            
            if not shows:
                # No shows found
                self.update_header(
                    "No Shows Found",
                    f"No shows from {year}"
                )
                self.show_list.set_empty_state(f"No shows from {year}")
                return
            
            # Update header - include legendary year indicator
            from src.ui.widgets.year_browser import YearBrowser
            is_legendary = year in YearBrowser.LEGENDARY_YEARS
            
            if is_legendary:
                title = f"[LEGENDARY] {year} ({len(shows)} shows)"
            else:
                title = f"{year} ({len(shows)} shows)"
            
            self.update_header(
                title,
                "All shows from this year, sorted by date"
            )
            
            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows
            
            print(f"[OK] Loaded {len(shows)} shows from {year}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load year shows: {e}")
            self.update_header("Error", f"Failed to load shows for {year}")
            self.show_list.set_empty_state("Error loading shows")
    
    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================
    
    def on_show_selected(self, show):
        """Handle show selection from list"""
        print(f"[INFO] Show selected: {show['date']} - {show['venue']}")
        self.show_selected.emit(show)


# Test code
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Apply dark theme
    app.setStyleSheet("""
        QWidget {
            background-color: #000000;
            color: #f3f4f6;
        }
    """)
    
    screen = BrowseScreen()
    screen.setWindowTitle("Browse Screen Test - WITH YEAR BROWSER")
    screen.setGeometry(100, 100, 1280, 720)
    screen.show()
    
    sys.exit(app.exec_())
