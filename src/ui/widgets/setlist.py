#!/usr/bin/env python3
"""
Setlist widget for DeadStream player screen.
Displays concert information and scrollable track list with set headers.

Phase 9, Task 9.3
"""

# Path manipulation for imports (file in src/ui/widgets/)
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QScrollArea, QFrame, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class SetlistWidget(QWidget):
    """
    Displays concert information and scrollable setlist.
    
    Features:
    - Concert header with metadata (title, location, badges)
    - Automatic set headers (SET I, SET II, ENCORE)
    - Track list with numbers, names, and durations
    - Current track highlighting
    - Click to jump to any track
    
    Signals:
        track_selected(int): Emitted when user clicks a track (0-indexed)
        favorite_toggled(bool): Emitted when favorite button is clicked
    """
    
    # Signals
    track_selected = pyqtSignal(int)  # Track index (0-indexed)
    favorite_toggled = pyqtSignal(bool)  # True if favorited, False if unfavorited
    
    def __init__(self):
        """Initialize setlist widget"""
        super().__init__()
        
        # Concert data
        self.concert_title = "No Concert Loaded"
        self.location = ""
        self.source_type = ""
        self.rating = 0.0
        self.track_count = 0
        self.is_favorited = False
        
        # Track data
        self.tracks = []  # List of track dicts
        self.current_track_index = -1
        
        # UI elements
        self.track_widgets = []  # Keep references to track widgets
        
        self.init_ui()
    
    def init_ui(self):
        """Set up the setlist display"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Concert header (fixed at top)
        header = self.create_concert_header()
        main_layout.addWidget(header)
        
        # Scrollable setlist area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1F2937;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #1F2937;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4B5563;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6B7280;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Container for setlist items
        self.setlist_container = QWidget()
        self.setlist_layout = QVBoxLayout()
        self.setlist_layout.setSpacing(0)
        self.setlist_layout.setContentsMargins(0, 0, 0, 0)
        self.setlist_container.setLayout(self.setlist_layout)
        
        scroll_area.setWidget(self.setlist_container)
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)
        
        print("[INFO] SetlistWidget initialized")
    
    def create_concert_header(self):
        """Create concert header with metadata"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-bottom: 2px solid #374151;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Top row: Title and favorite button
        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        
        # Concert title
        self.title_label = QLabel(self.concert_title)
        self.title_label.setWordWrap(True)
        title_font = QFont("Arial", 20, QFont.DemiBold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #FFFFFF;")
        top_row.addWidget(self.title_label, 1)
        
        # Favorite button
        self.favorite_btn = QPushButton()
        self.favorite_btn.setFixedSize(40, 40)
        self.update_favorite_button()
        self.favorite_btn.clicked.connect(self.on_favorite_clicked)
        top_row.addWidget(self.favorite_btn)
        
        layout.addLayout(top_row)
        
        # Location
        self.location_label = QLabel(self.location)
        location_font = QFont("Arial", 14)
        self.location_label.setFont(location_font)
        self.location_label.setStyleSheet("color: #9CA3AF;")
        layout.addWidget(self.location_label)
        
        # Metadata badges row
        badges_row = QHBoxLayout()
        badges_row.setSpacing(8)
        
        # Source type badge
        self.source_badge = QLabel(self.source_type)
        self.source_badge.setStyleSheet("""
            QLabel {
                background-color: #374151;
                color: #FFFFFF;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
            }
        """)
        badges_row.addWidget(self.source_badge)
        
        # Rating badge
        self.rating_badge = QLabel(f"[Star] {self.rating:.1f}/5.0")
        self.rating_badge.setStyleSheet("""
            QLabel {
                background-color: #374151;
                color: #FCD34D;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
            }
        """)
        badges_row.addWidget(self.rating_badge)
        
        # Track count badge
        self.count_badge = QLabel(f"{self.track_count} tracks")
        self.count_badge.setStyleSheet("""
            QLabel {
                background-color: #374151;
                color: #9CA3AF;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
            }
        """)
        badges_row.addWidget(self.count_badge)
        
        badges_row.addStretch()
        layout.addLayout(badges_row)
        
        header.setLayout(layout)
        return header
    
    def update_favorite_button(self):
        """Update favorite button appearance based on state"""
        if self.is_favorited:
            # Red filled heart
            self.favorite_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #EF4444;
                    font-size: 24px;
                }
                QPushButton:hover {
                    color: #DC2626;
                }
            """)
            self.favorite_btn.setText("[Heart]")  # Would be heart icon in production
        else:
            # Gray outline heart
            self.favorite_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #6B7280;
                    font-size: 24px;
                }
                QPushButton:hover {
                    color: #9CA3AF;
                }
            """)
            self.favorite_btn.setText("[Heart]")  # Would be heart icon in production
    
    def on_favorite_clicked(self):
        """Handle favorite button click"""
        self.is_favorited = not self.is_favorited
        self.update_favorite_button()
        self.favorite_toggled.emit(self.is_favorited)
        print(f"[INFO] Favorite toggled: {self.is_favorited}")
    
    def load_concert(self, concert_title, location, source_type, rating, tracks):
        """
        Load concert information and tracks.
        
        Args:
            concert_title (str): Format "YYYY/MM/DD [Venue Name]"
            location (str): Format "[City], [State]"
            source_type (str): "Soundboard", "Audience", or "Matrix"
            rating (float): Rating out of 5.0
            tracks (list): List of track dicts with keys:
                - title (str): Song name
                - duration (str): Duration in MM:SS format
                - set_name (str): "SET I", "SET II", or "ENCORE"
        """
        self.concert_title = concert_title
        self.location = location
        self.source_type = source_type
        self.rating = rating
        self.tracks = tracks
        self.track_count = len(tracks)
        
        # Update header
        self.title_label.setText(concert_title)
        self.location_label.setText(location)
        self.source_badge.setText(source_type)
        self.rating_badge.setText(f"[Star] {rating:.1f}/5.0")
        self.count_badge.setText(f"{self.track_count} tracks")
        
        # Build setlist
        self.build_setlist()
        
        print(f"[INFO] Loaded concert: {concert_title} ({self.track_count} tracks)")
    
    def build_setlist(self):
        """Build the setlist display with set headers and tracks"""
        # Clear existing tracks
        for i in reversed(range(self.setlist_layout.count())):
            widget = self.setlist_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        self.track_widgets = []
        
        if not self.tracks:
            # No tracks - show placeholder
            placeholder = QLabel("No tracks available")
            placeholder.setStyleSheet("""
                color: #6B7280;
                padding: 40px;
                font-size: 16px;
            """)
            placeholder.setAlignment(Qt.AlignCenter)
            self.setlist_layout.addWidget(placeholder)
            return
        
        # Track current set to insert headers
        current_set = None
        
        for idx, track in enumerate(self.tracks):
            # Insert set header if set changed
            if track.get('set_name') != current_set:
                current_set = track.get('set_name', '')
                if current_set:
                    header = self.create_set_header(current_set)
                    self.setlist_layout.addWidget(header)
            
            # Create track item
            track_widget = self.create_track_item(idx, track)
            self.setlist_layout.addWidget(track_widget)
            self.track_widgets.append(track_widget)
        
        # Add stretch at bottom
        self.setlist_layout.addStretch()
    
    def create_set_header(self, set_name):
        """
        Create a set header label.
        
        Args:
            set_name (str): "SET I", "SET II", or "ENCORE"
        
        Returns:
            QLabel: Styled set header
        """
        header = QLabel(set_name)
        header.setStyleSheet("""
            QLabel {
                background-color: #1F2937;
                color: #6B7280;
                padding: 12px 20px 8px 20px;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 2px;
            }
        """)
        return header
    
    def create_track_item(self, index, track):
        """
        Create a track list item.
        
        Args:
            index (int): Track index (0-indexed)
            track (dict): Track data with title, duration
        
        Returns:
            QFrame: Clickable track item
        """
        item = QFrame()
        item.setProperty("track_index", index)  # Store index for click handling
        item.setCursor(Qt.PointingHandCursor)
        item.setMinimumHeight(50)
        
        # Default style (non-highlighted)
        item.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-bottom: 1px solid #374151;
                padding: 8px 20px;
            }
            QFrame:hover {
                background-color: #111827;
            }
        """)
        
        # Track layout
        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Track number (fixed width for alignment)
        track_num = QLabel(f"{index + 1:02d}")
        track_num.setFixedWidth(30)
        track_num.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
        """)
        layout.addWidget(track_num)
        
        # Song name (takes remaining space)
        song_name = QLabel(track.get('title', 'Unknown Track'))
        song_name.setStyleSheet("""
            color: #FFFFFF;
            font-size: 15px;
        """)
        # Enable text elision if too long
        song_name.setTextInteractionFlags(Qt.NoTextInteraction)
        layout.addWidget(song_name, 1)
        
        # Duration (right-aligned)
        duration = QLabel(track.get('duration', '0:00'))
        duration.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
        """)
        duration.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(duration)
        
        item.setLayout(layout)
        
        # Make clickable
        item.mousePressEvent = lambda event, idx=index: self.on_track_clicked(idx)
        
        return item
    
    def on_track_clicked(self, track_index):
        """
        Handle track item click.
        
        Args:
            track_index (int): Index of clicked track (0-indexed)
        """
        print(f"[INFO] Track clicked: {track_index} - {self.tracks[track_index].get('title', 'Unknown')}")
        self.track_selected.emit(track_index)
        self.set_current_track(track_index)
    
    def set_current_track(self, track_index):
        """
        Highlight the current track.
        
        Args:
            track_index (int): Index of current track (0-indexed)
        """
        if track_index < 0 or track_index >= len(self.track_widgets):
            return
        
        # Remove highlight from previous track
        if 0 <= self.current_track_index < len(self.track_widgets):
            self.track_widgets[self.current_track_index].setStyleSheet("""
                QFrame {
                    background-color: #1F2937;
                    border-bottom: 1px solid #374151;
                    padding: 8px 20px;
                }
                QFrame:hover {
                    background-color: #111827;
                }
            """)
        
        # Highlight new current track
        self.track_widgets[track_index].setStyleSheet("""
            QFrame {
                background-color: #374151;
                border-bottom: 1px solid #4B5563;
                padding: 8px 20px;
            }
            QFrame:hover {
                background-color: #4B5563;
            }
        """)
        
        self.current_track_index = track_index
        
        print(f"[INFO] Current track set to: {track_index}")
    
    def clear_concert(self):
        """Clear all concert data and reset display"""
        self.concert_title = "No Concert Loaded"
        self.location = ""
        self.source_type = ""
        self.rating = 0.0
        self.track_count = 0
        self.tracks = []
        self.current_track_index = -1
        self.is_favorited = False
        
        # Update header
        self.title_label.setText(self.concert_title)
        self.location_label.setText(self.location)
        self.source_badge.setText("")
        self.rating_badge.setText("")
        self.count_badge.setText("0 tracks")
        self.update_favorite_button()
        
        # Clear setlist
        self.build_setlist()
        
        print("[INFO] Concert cleared")


if __name__ == "__main__":
    """Test the setlist widget"""
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create test window
    widget = SetlistWidget()
    widget.setGeometry(100, 100, 600, 800)
    widget.setWindowTitle("DeadStream Setlist Test")
    
    # Load sample concert data
    sample_tracks = [
        {"title": "Bertha", "duration": "6:14", "set_name": "SET I"},
        {"title": "Me and My Uncle", "duration": "3:12", "set_name": "SET I"},
        {"title": "Mr. Charlie", "duration": "3:43", "set_name": "SET I"},
        {"title": "Loser", "duration": "7:08", "set_name": "SET I"},
        {"title": "Beat It on Down the Line", "duration": "3:24", "set_name": "SET I"},
        {"title": "Sugaree", "duration": "7:23", "set_name": "SET I"},
        {"title": "Jack Straw", "duration": "4:54", "set_name": "SET I"},
        {"title": "Tennessee Jed", "duration": "7:42", "set_name": "SET I"},
        {"title": "Scarlet Begonias", "duration": "10:27", "set_name": "SET II"},
        {"title": "Fire on the Mountain", "duration": "12:05", "set_name": "SET II"},
        {"title": "Estimated Prophet", "duration": "9:18", "set_name": "SET II"},
        {"title": "Eyes of the World", "duration": "10:45", "set_name": "SET II"},
        {"title": "Drums", "duration": "7:33", "set_name": "SET II"},
        {"title": "Space", "duration": "8:21", "set_name": "SET II"},
        {"title": "Wharf Rat", "duration": "10:12", "set_name": "SET II"},
        {"title": "Around and Around", "duration": "7:54", "set_name": "SET II"},
        {"title": "U.S. Blues", "duration": "5:36", "set_name": "ENCORE"},
    ]
    
    widget.load_concert(
        concert_title="1977/05/08 Barton Hall, Cornell University",
        location="Ithaca, NY",
        source_type="Soundboard",
        rating=4.8,
        tracks=sample_tracks
    )
    
    # Simulate current track
    def update_current():
        widget.set_current_track(8)  # Scarlet Begonias
    
    from PyQt5.QtCore import QTimer
    QTimer.singleShot(1000, update_current)
    
    # Handle signals
    widget.track_selected.connect(lambda idx: print(f"[TEST] Track selected signal: {idx}"))
    widget.favorite_toggled.connect(lambda fav: print(f"[TEST] Favorite toggled signal: {fav}"))
    
    widget.show()
    sys.exit(app.exec_())
