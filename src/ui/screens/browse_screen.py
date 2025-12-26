"""
Browse Screen for DeadStream

This screen allows users to browse and select Grateful Dead shows.

Initial implementation (Task 7.1):
- Displays top-rated shows by default
- Shows metadata (date, venue, location, rating)
- Touch-friendly show cards with play buttons
- Scrollable list

Future tasks will add:
- Date browser (7.2)
- Venue filter (7.3)
- Year selector (7.4)
- Search functionality (7.5)
- Random show button (7.6)
"""

import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import database queries
from src.database.queries import get_top_rated_shows

# Import show list widget
from src.ui.widgets.show_list import ShowListWidget


class BrowseScreen(QWidget):
    """
    Browse screen for finding and selecting shows
    
    Layout (from UI spec):
    - Left panel (40%): Navigation and browse modes (future)
    - Right panel (60%): Show list
    
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
        
        # Left Panel (40%) - Navigation (placeholder for now)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, stretch=4)
        
        # Right Panel (60%) - Show list
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, stretch=6)
        
        self.setLayout(main_layout)
    
    def create_left_panel(self):
        """
        Create left navigation panel
        
        Currently placeholder - will be enhanced in future tasks:
        - Task 7.2: Date browser
        - Task 7.3: Venue filter
        - Task 7.4: Year selector
        - Task 7.6: Random show button
        """
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
        
        # Placeholder text for future browse modes
        placeholder = QLabel("Browse modes coming in Tasks 7.2-7.6:\n\n" +
                            "- Date Browser\n" +
                            "- Venue Filter\n" +
                            "- Year Selector\n" +
                            "- Random Show\n\n" +
                            "For now, showing top-rated shows.")
        placeholder.setStyleSheet("""
            color: #9ca3af;
            font-size: 14px;
            line-height: 1.5;
        """)
        placeholder.setWordWrap(True)
        layout.addWidget(placeholder)
        
        layout.addStretch()
        
        # Stats section (shows count)
        from src.database.queries import get_show_count
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
    
    def create_right_panel(self):
        """Create right panel with show list"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #000000;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header section
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #1f2937;")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(24, 20, 24, 20)
        header_layout.setSpacing(8)
        
        # Title
        title = QLabel("Top Rated Shows")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Showing the highest-rated performances from the collection")
        subtitle.setStyleSheet("""
            color: #9ca3af;
            font-size: 14px;
        """)
        subtitle.setWordWrap(True)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_widget)
        
        # Show list widget
        self.show_list = ShowListWidget()
        self.show_list.show_selected.connect(self.on_show_selected)
        layout.addWidget(self.show_list, stretch=1)
        
        return panel
    
    def load_default_shows(self):
        """Load top-rated shows on startup"""
        try:
            # Set loading state
            self.show_list.set_loading_state()
            
            # Get top 50 rated shows (minimum 5 reviews to avoid unreviewed shows)
            shows = get_top_rated_shows(limit=50, min_reviews=5)
            
            if shows:
                self.current_shows = shows
                self.show_list.load_shows(shows)
                print(f"[INFO] Loaded {len(shows)} top-rated shows")
            else:
                self.show_list.set_empty_state("No rated shows found")
                print("[WARN] No shows found in database")
                
        except Exception as e:
            print(f"[ERROR] Failed to load shows: {e}")
            self.show_list.set_empty_state("Error loading shows")
    
    def on_show_selected(self, show_data):
        """
        Handle show selection
        
        Args:
            show_data: Dictionary with show information from database
        """
        print(f"\n[INFO] Show selected:")
        print(f"  Date: {show_data['date']}")
        print(f"  Venue: {show_data.get('venue', 'Unknown')}")
        print(f"  Identifier: {show_data['identifier']}")
        
        # Emit signal to main window for playback
        self.show_selected.emit(show_data)