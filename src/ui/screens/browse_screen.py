#!/usr/bin/env python3
"""
Browse Screen for DeadStream - COMPLETE WITH SEARCH (Tasks 7.1-7.5)

This screen allows users to browse and select Grateful Dead shows.

Completed features:
- Task 7.1: Show list view with top-rated shows
- Task 7.2: Date browser (calendar-based browsing)
- Task 7.3: Venue filter
- Task 7.4: Year selector
- Task 7.5: Search functionality (NEW)

Future tasks:
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
    search_by_venue, get_show_by_date, search_by_year,
    search_shows  # Task 7.5 - NEW
)

# Import widgets
from src.ui.widgets.show_list import ShowListWidget
from src.ui.widgets.date_browser import DateBrowser
from src.ui.widgets.year_browser import YearBrowser
from src.ui.widgets.search_widget import SearchWidget  # Task 7.5 - NEW


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
    - Browse by Year (Task 7.4)
    - Search (Task 7.5 - NEW)
    
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
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("Browse Shows")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        # Browse mode buttons
        browse_layout = self.create_browse_mode_buttons()
        layout.addLayout(browse_layout)
        
        layout.addStretch()
        
        return panel
    
    def create_browse_mode_buttons(self):
        """Create browse mode button list"""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
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
        
        # Year Browser (Task 7.4)
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
        
        # Search (Task 7.5 - NEW)
        search_btn = QPushButton("Search Shows")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 16px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #d97706;
            }
            QPushButton:pressed {
                background-color: #b45309;
            }
        """)
        search_btn.clicked.connect(self.show_search_dialog)
        layout.addWidget(search_btn)
        
        return layout
    
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
        
        # Show list widget
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
        dialog.setMinimumSize(600, 500)
        
        # Apply dark theme
        dialog.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
            QLabel {
                color: white;
            }
            QListWidget {
                background-color: #1f2937;
                color: white;
                border: 2px solid #374151;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #374151;
            }
            QListWidget::item:selected {
                background-color: #10b981;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #374151;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
        """)
        
        # Layout
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Select a Venue")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Top venues by number of shows")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #9ca3af;")
        layout.addWidget(subtitle)
        
        # Venue list
        venue_list = QListWidget()
        
        try:
            # Get most played venues
            venues = get_most_played_venues(limit=50)
            
            for venue_data in venues:
                venue_name = venue_data['venue']
                show_count = venue_data['show_count']
                city = venue_data.get('city', 'Unknown')
                state = venue_data.get('state', '')
                
                # Format item text
                item_text = f"{venue_name} - {city}, {state} ({show_count} shows)"
                
                # Create list item
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, venue_name)  # Store venue name for retrieval
                venue_list.addItem(item)
            
            print(f"[OK] Loaded {len(venues)} venues")
            
        except Exception as e:
            print(f"[ERROR] Failed to load venues: {e}")
        
        layout.addWidget(venue_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        close_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(close_btn)
        
        # Select button
        select_btn = QPushButton("View Shows")
        select_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
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
        
        # Enable button when venue selected
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
        """Show year browser dialog (Task 7.4)"""
        
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
    
    def show_search_dialog(self):
        """Show search dialog (Task 7.5 - NEW)"""
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Search Shows")
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
        
        # Add search widget
        search_widget = SearchWidget()
        
        # Connect search signal
        def on_search(search_params):
            """Handle search submission"""
            dialog.accept()
            self.load_search_results(search_params)
        
        search_widget.search_submitted.connect(on_search)
        layout.addWidget(search_widget)
        
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
        """Load and display shows from a specific year (Task 7.4)"""
        
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
    
    def load_search_results(self, search_params):
        """Load and display search results (Task 7.5 - NEW)"""
        
        try:
            self.show_list.set_loading_state()
            
            # Get shows using search_shows function
            shows = search_shows(
                query=search_params.get('query'),
                year=search_params.get('year'),
                venue=None,  # Not using venue filter in search widget
                state=search_params.get('state'),
                min_rating=search_params.get('min_rating'),
                limit=100
            )
            
            if not shows:
                # No results
                self.update_header(
                    "No Results Found",
                    "No shows matching your search criteria"
                )
                self.show_list.set_empty_state("Try different search terms")
                print("[INFO] Search returned no results")
                return
            
            # Build subtitle from search parameters
            subtitle_parts = []
            if search_params.get('query'):
                subtitle_parts.append(f"Query: '{search_params['query']}'")
            if search_params.get('year'):
                subtitle_parts.append(f"Year: {search_params['year']}")
            if search_params.get('state'):
                subtitle_parts.append(f"State: {search_params['state']}")
            if search_params.get('min_rating'):
                subtitle_parts.append(f"Rating: {search_params['min_rating']}+")
            
            subtitle = " | ".join(subtitle_parts) if subtitle_parts else "All shows"
            
            # Update header
            self.update_header(
                f"Search Results ({len(shows)} shows)",
                subtitle
            )
            
            # Load shows
            self.show_list.load_shows(shows)
            self.current_shows = shows
            
            print(f"[OK] Loaded {len(shows)} search results")
            
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Search Error", "Failed to search shows")
            self.show_list.set_empty_state("Error during search")
    
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
    screen.setWindowTitle("Browse Screen Test - WITH SEARCH (Tasks 7.1-7.5)")
    screen.setGeometry(100, 100, 1280, 720)
    screen.show()
    
    sys.exit(app.exec_())
