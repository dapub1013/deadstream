#!/usr/bin/env python3
"""
Browse Screen for DeadStream - WITH SEARCH AND RANDOM SHOW

This version includes Tasks 7.1-7.6 (COMPLETE Phase 7).

Completed features:
- Task 7.1: Show list view with top-rated shows
- Task 7.2: Date browser (calendar-based browsing)
- Task 7.3: Venue filter
- Task 7.4: Year selector
- Task 7.5: Search functionality
- Task 7.6: Random show button (NEW)
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
    get_show_count, get_random_show
)

# Import widgets
from src.ui.widgets.show_list import ShowListWidget
from src.ui.widgets.date_browser import DateBrowser
from src.ui.widgets.year_browser import YearBrowser
from src.ui.widgets.search_widget import SearchWidget


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
    - Search Shows (Task 7.5)
    - Random Show (Task 7.6 - NEW)
    
    Signals:
    - show_selected: Emitted when user selects a show to play
    """
    
# Navigation signals
    show_selected = pyqtSignal(dict)  # Emits show dictionary
    player_requested = pyqtSignal()   # Navigate to player
    settings_requested = pyqtSignal() # Navigate to settings

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
        """Create left panel with browse mode buttons"""
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
        
        # Title
        title = QLabel("Browse Shows")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding-bottom: 8px;
                border-bottom: 2px solid #374151;
            }
        """)
        layout.addWidget(title)
        
        # Add browse mode buttons
        browse_buttons = self.create_browse_mode_buttons()
        layout.addLayout(browse_buttons)
        
        # Add stretch to push buttons to top
        layout.addStretch()
        
        # Navigation buttons at bottom
        nav_layout = self.create_navigation_buttons()
        layout.addLayout(nav_layout)
        
        return panel
    
    def create_browse_mode_buttons(self):
        """Create buttons for different browse modes"""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # Top Rated (default)
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
                background-color: #1f2937;
            }
        """)
        top_rated_btn.setMinimumHeight(60)
        top_rated_btn.clicked.connect(self.load_default_shows)
        layout.addWidget(top_rated_btn)
        
        # Browse by Date
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
        date_btn.setMinimumHeight(60)
        date_btn.clicked.connect(self.show_date_browser)
        layout.addWidget(date_btn)
        
        # Browse by Venue
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
        venue_btn.setMinimumHeight(60)
        venue_btn.clicked.connect(self.show_venue_browser)
        layout.addWidget(venue_btn)
        
        # Browse by Year
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
        year_btn.setMinimumHeight(60)
        year_btn.clicked.connect(self.show_year_browser)
        layout.addWidget(year_btn)
        
        # Search Shows (Task 7.5)
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
        search_btn.setMinimumHeight(60)
        search_btn.clicked.connect(self.show_search_dialog)
        layout.addWidget(search_btn)
        
        # Random Show (Task 7.6 - NEW)
        random_btn = QPushButton("Random Show")
        random_btn.setStyleSheet("""
            QPushButton {
                background-color: #ec4899;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 16px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #db2777;
            }
            QPushButton:pressed {
                background-color: #be185d;
            }
        """)
        random_btn.setMinimumHeight(60)
        random_btn.clicked.connect(self.load_random_show)
        layout.addWidget(random_btn)
        
        return layout
    
    def create_right_panel(self):
        """Create right panel with show list"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #111827;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Header widget (separate from ShowListWidget!)
        self.header_widget = QWidget()
        header_layout = QVBoxLayout(self.header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)
        
        # Title label
        self.header_title = QLabel("Top Rated Shows")
        self.header_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(self.header_title)
        
        # Subtitle label
        self.header_subtitle = QLabel("Shows with 5+ reviews")
        self.header_subtitle.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                font-size: 16px;
            }
        """)
        header_layout.addWidget(self.header_subtitle)
        
        layout.addWidget(self.header_widget)
        
        # Show list widget
        self.show_list = ShowListWidget()
        self.show_list.show_selected.connect(self.on_show_selected)
        layout.addWidget(self.show_list)
        
        return panel

    def create_navigation_buttons(self):
        """Create navigation buttons (Player, Settings)"""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # Back to Player button
        player_btn = QPushButton("Back to Player")
        player_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: 2px solid #4b5563;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #6b7280;
            }
        """)
        player_btn.setMinimumHeight(50)
        player_btn.clicked.connect(self.player_requested.emit)
        layout.addWidget(player_btn)
        
        # Settings button
        settings_btn = QPushButton("Settings")
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: 2px solid #4b5563;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #6b7280;
            }
        """)
        settings_btn.setMinimumHeight(50)
        settings_btn.clicked.connect(self.settings_requested.emit)
        layout.addWidget(settings_btn)
        
        return layout

    def update_header(self, title, subtitle):
        """Update header title and subtitle"""
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
        
            self.update_header(
                "Top Rated Shows",
                f"{len(shows)} shows with 5+ reviews"
            )
        
            self.show_list.load_shows(shows)
            self.current_shows = shows
        
            print(f"[OK] Loaded {len(shows)} top-rated shows")
        
        except Exception as e:
            print(f"[ERROR] Failed to load top rated shows: {e}")
            import traceback
            traceback.print_exc()

    def show_date_browser(self):
        """Show date browser dialog (Task 7.2)"""
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Browse by Date")
        dialog.setModal(True)
        dialog.setMinimumSize(400, 500)
        
        # Apply dark theme
        dialog.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add date browser widget
        date_browser = DateBrowser()
        date_browser.date_selected.connect(lambda date: (
            dialog.accept(),
            self.load_shows_by_date(date)
        ))
        layout.addWidget(date_browser)
        
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
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:enabled {
                background-color: #10b981;
                color: white;
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
            QPushButton:hover:enabled {
                background-color: #059669;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("Select a Venue")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Venue list
        venue_list = QListWidget()
        
        # Load venues
        venues = get_most_played_venues(limit=100)
        for venue_name, show_count in venues:
            item = QListWidgetItem(f"{venue_name} ({show_count} shows)")
            item.setData(Qt.UserRole, venue_name)
            venue_list.addItem(item)
        
        layout.addWidget(venue_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Select button
        select_btn = QPushButton("Load Shows")
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
        venue_list.itemDoubleClicked.connect(lambda: on_select())
        
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
        dialog.setMinimumSize(600, 500)
        
        # Apply dark theme
        dialog.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add year browser widget
        year_browser = YearBrowser()
        year_browser.year_selected.connect(lambda year: (
            dialog.accept(),
            self.load_shows_by_year(year)
        ))
        layout.addWidget(year_browser)
        
        # Show dialog
        dialog.exec_()
    
    def show_search_dialog(self):
        """Show search dialog (Task 7.5)"""
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Search Shows")
        dialog.setModal(True)
        dialog.setMinimumSize(600, 500)
        
        # Apply dark theme
        dialog.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add search widget
        search_widget = SearchWidget()
        search_widget.search_executed.connect(lambda results: (
            dialog.accept(),
            self.load_search_results(results)
        ))
        layout.addWidget(search_widget)
        
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
            import traceback
            traceback.print_exc()
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
            import traceback
            traceback.print_exc()
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
            import traceback
            traceback.print_exc()
            self.update_header("Error", f"Failed to load shows for {year}")
            self.show_list.set_empty_state("Error loading shows")
    
    def load_search_results(self, results):
        """Load and display search results (Task 7.5)"""
        
        try:
            # Update header
            if not results:
                self.update_header(
                    "No Results",
                    "No shows matched your search criteria"
                )
                self.show_list.set_empty_state("Try different search criteria")
                return
            
            self.update_header(
                f"Search Results ({len(results)} shows)",
                "Sorted by rating (best first)"
            )
            
            # Load shows into list
            self.show_list.load_shows(results)
            self.current_shows = results
            
            print(f"[OK] Loaded {len(results)} search results")
            
        except Exception as e:
            print(f"[ERROR] Failed to load search results: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", "Failed to load search results")
            self.show_list.set_empty_state("Error loading shows")
    
    def load_random_show(self):
        """Load a random show (Task 7.6 - NEW)"""
        
        try:
            self.show_list.set_loading_state()
            
            # Get a random show
            show = get_random_show()
            
            if not show:
                # No show found
                self.update_header(
                    "No Shows Found",
                    "No shows in database"
                )
                self.show_list.set_empty_state("Database appears empty")
                return
            
            # Update header
            self.update_header(
                "Random Show",
                f"{show['date']} at {show['venue']}, {show['city']}, {show['state']}"
            )
            
            # Load single show as a list
            self.show_list.load_shows([show])
            self.current_shows = [show]
            
            print(f"[OK] Loaded random show: {show['date']} - {show['venue']}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load random show: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", "Failed to load random show")
            self.show_list.set_empty_state("Error loading show")
    
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
    screen.setWindowTitle("Browse Screen Test - WITH RANDOM SHOW")
    screen.setGeometry(100, 100, 1280, 720)
    screen.show()
    
    sys.exit(app.exec_())
