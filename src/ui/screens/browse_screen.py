#!/usr/bin/env python3
"""
Browse Screen for DeadStream - COMPLETE WITH ALL BROWSE MODES

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
# This file is in src/ui/screens/, so go up three levels to get to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
    search_by_venue, get_show_by_date, search_by_year
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
    - Browse by Year (Task 7.4)
    
    Signals:
    - show_selected: Emitted when user selects a show to play
    """
    
    show_selected = pyqtSignal(dict)  # Emits show dictionary
    
    def __init__(self, parent=None):
        """Initialize browse screen"""
        super().__init__(parent)
        self.current_shows = []
        self.current_mode = 'top_rated'
        self.setup_ui()
        self.load_default_shows()
    
    def setup_ui(self):
        """Create browse screen layout"""
        # Main horizontal layout (left panel + right panel)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left Panel (40%) - Navigation
        self.left_panel = self.create_left_panel()
        main_layout.addWidget(self.left_panel, stretch=4)
        
        # Right Panel (60%) - Show list
        self.right_panel = self.create_right_panel()
        main_layout.addWidget(self.right_panel, stretch=6)
        
        self.setLayout(main_layout)
    
    def create_left_panel(self):
        """Create left navigation panel with browse modes"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-right: 1px solid #374151;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Browse Shows")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        layout.addWidget(title)
        
        # Spacing
        layout.addSpacing(10)
        
        # Browse mode buttons
        browse_label = QLabel("BROWSE BY")
        browse_label.setStyleSheet("""
            color: #9ca3af;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 1px;
        """)
        layout.addWidget(browse_label)
        
        # Date button
        self.date_btn = QPushButton("[CALENDAR] Date")
        self.date_btn.setStyleSheet(self.get_browse_button_style('date'))
        self.date_btn.clicked.connect(self.show_date_browser)
        layout.addWidget(self.date_btn)
        
        # Venue button
        self.venue_btn = QPushButton("[MAP] Venue")
        self.venue_btn.setStyleSheet(self.get_browse_button_style('venue'))
        self.venue_btn.clicked.connect(self.show_venue_browser)
        layout.addWidget(self.venue_btn)
        
        # Year button (NEW - Task 7.4)
        self.year_btn = QPushButton("[CLOCK] Year")
        self.year_btn.setStyleSheet(self.get_browse_button_style('year'))
        self.year_btn.clicked.connect(self.show_year_browser)
        layout.addWidget(self.year_btn)
        
        # Add stretch to push buttons to top
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self):
        """Create right panel with show list"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #111827;
            }
        """)
        
        self.right_panel_layout = QVBoxLayout(panel)
        self.right_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.right_panel_layout.setSpacing(0)
        
        # Show list widget (starts with top-rated shows)
        self.show_list = ShowListWidget()
        self.show_list.show_selected.connect(self.on_show_selected)
        self.right_panel_layout.addWidget(self.show_list)
        
        return panel
    
    def get_browse_button_style(self, button_type):
        """Get style for browse mode button"""
        # Color mapping for different browse types
        colors = {
            'date': '#3b82f6',      # blue
            'venue': '#10b981',     # green
            'year': '#7c3aed',      # purple
        }
        
        color = colors.get(button_type, '#3b82f6')
        
        return f"""
            QPushButton {{
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {color};
            }}
        """
    
    def clear_right_panel(self):
        """Clear the right panel to add new content"""
        # Remove all widgets from right panel
        while self.right_panel_layout.count():
            item = self.right_panel_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    # ========================================================================
    # BROWSE MODE HANDLERS
    # ========================================================================
    
    def load_default_shows(self):
        """Load top-rated shows (default view)"""
        try:
            shows = get_top_rated_shows(limit=50, min_reviews=5)
            
            # Just load shows directly - ShowListWidget handles its own display
            self.show_list.load_shows(shows)
            self.current_shows = shows
            self.current_mode = 'top_rated'
            
            print(f"[OK] Loaded {len(shows)} top-rated shows")
            
        except Exception as e:
            print(f"[ERROR] Failed to load top-rated shows: {e}")
            import traceback
            traceback.print_exc()
    
    def show_date_browser(self):
        """Show date browser widget (Task 7.2)"""
        print("[INFO] Switching to date browse mode")
        
        try:
            # Clear right panel
            self.clear_right_panel()
            
            # Create date browser widget
            date_browser = DateBrowser()
            date_browser.date_selected.connect(self.load_shows_by_date)
            
            # Add to right panel
            self.right_panel_layout.addWidget(date_browser)
            
            self.current_mode = 'date'
            
        except Exception as e:
            print(f"[ERROR] Failed to show date browser: {e}")
    
    def show_venue_browser(self):
        """Show venue browser dialog (Task 7.3)"""
        print("[INFO] Opening venue browser dialog")
        
        try:
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
                }
                QPushButton:hover {
                    background-color: #4b5563;
                }
            """)
            
            layout = QVBoxLayout(dialog)
            
            # Title
            title = QLabel("Select a Venue")
            title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
            layout.addWidget(title)
            
            # Venue list
            venue_list = QListWidget()
            
            # Load venues from database
            venues = get_most_played_venues(limit=50)
            
            for venue_name, show_count in venues:
                item = QListWidgetItem(f"{venue_name} ({show_count} shows)")
                item.setData(Qt.UserRole, venue_name)
                venue_list.addItem(item)
            
            layout.addWidget(venue_list)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            close_btn = QPushButton("Cancel")
            close_btn.setStyleSheet("background-color: #6b7280;")
            close_btn.clicked.connect(dialog.reject)
            button_layout.addWidget(close_btn)
            
            select_btn = QPushButton("Load Shows")
            select_btn.setStyleSheet("background-color: #10b981;")
            select_btn.setEnabled(False)
            
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
            
        except Exception as e:
            print(f"[ERROR] Failed to show venue browser: {e}")
    
    def show_year_browser(self):
        """Show year browser widget (Task 7.4 - NEW)"""
        print("[INFO] Switching to year browse mode")
        
        try:
            # Clear right panel
            self.clear_right_panel()
            
            # Create year browser widget
            year_browser = YearBrowser()
            year_browser.year_selected.connect(self.load_shows_by_year)
            
            # Add to right panel
            self.right_panel_layout.addWidget(year_browser)
            
            self.current_mode = 'year'
            
            print("[OK] Year browser displayed")
            
        except Exception as e:
            print(f"[ERROR] Failed to show year browser: {e}")
    
    # ========================================================================
    # DATA LOADING HANDLERS
    # ========================================================================
    
    def load_shows_by_date(self, date_str):
        """Load and display shows from a specific date (Task 7.2)"""
        print(f"[INFO] Loading shows for date: {date_str}")
        
        try:
            # Get shows for this date
            shows = get_show_by_date(date_str)
            
            if not shows:
                print(f"[INFO] No shows found for {date_str}")
                # Load empty list
                self.show_list.load_shows([])
                return
            
            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows
            
            print(f"[OK] Loaded {len(shows)} shows from {date_str}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load date shows: {e}")
            import traceback
            traceback.print_exc()
            self.show_list.load_shows([])
    
    def load_shows_by_venue(self, venue_name):
        """Load and display shows from a specific venue (Task 7.3)"""
        print(f"[INFO] Loading shows for venue: {venue_name}")
        
        try:
            # Get shows for this venue
            shows = search_by_venue(venue_name, exact_match=False)
            
            if not shows:
                print(f"[INFO] No shows found at {venue_name}")
                self.show_list.load_shows([])
                return
            
            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows
            self.current_mode = 'venue'
            
            print(f"[OK] Loaded {len(shows)} shows from {venue_name}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load venue shows: {e}")
            import traceback
            traceback.print_exc()
            self.show_list.load_shows([])
    
    def load_shows_by_year(self, year):
        """Load and display shows from a specific year (Task 7.4 - NEW)"""
        print(f"[INFO] Loading shows for year: {year}")
        
        try:
            # Get shows for this year
            shows = search_by_year(year)
            
            if not shows:
                print(f"[INFO] No shows found for {year}")
                self.show_list.load_shows([])
                return
            
            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows
            self.current_mode = 'year'
            
            print(f"[OK] Loaded {len(shows)} shows from {year}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load year shows: {e}")
            import traceback
            traceback.print_exc()
            self.show_list.load_shows([])
    
    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================
    
    def on_show_selected(self, show_data):
        """Handle show selection from list"""
        print(f"\n[INFO] Show selected:")
        print(f"  Date: {show_data['date']}")
        print(f"  Venue: {show_data.get('venue', 'Unknown')}")
        print(f"  Identifier: {show_data['identifier']}")
        
        # Emit signal to parent
        self.show_selected.emit(show_data)


# Test the screen standalone
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create test window
    screen = BrowseScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("Browse Screen Test - All Modes")
    screen.show()
    
    # Connect signal
    screen.show_selected.connect(
        lambda show: print(f"[TEST] Show selected signal: {show['date']}")
    )
    
    sys.exit(app.exec_())
