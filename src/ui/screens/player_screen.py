#!/usr/bin/env python3
"""
Player screen for DeadStream UI.
Shows now-playing interface with track info, playback controls, and setlist.

Phase 9, Task 9.3 - Full setlist display integrated
"""

# Path manipulation for imports (file in src/ui/screens/)
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import widgets
from src.ui.widgets.track_info import TrackInfoWidget
from src.ui.widgets.setlist import SetlistWidget


class PlayerScreen(QWidget):
    """
    Player screen with now-playing interface.
    
    Features:
    - Left panel: Concert info + scrollable setlist
    - Right panel: Track info + playback controls
    
    Signals:
        browse_requested: User wants to browse shows
        track_selected(int): User clicked a track in setlist
        favorite_toggled(bool): User toggled favorite status
    """
    
    # Signals
    browse_requested = pyqtSignal()
    track_selected = pyqtSignal(int)  # Track index (0-indexed)
    favorite_toggled = pyqtSignal(bool)  # Favorite status
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()
        
        # Widgets
        self.setlist = None
        self.track_info = None
        
        self.init_ui()
    
    def init_ui(self):
        """Set up the player screen UI"""
        # Main horizontal layout (split screen)
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left panel: Concert info + setlist (50%)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)  # Stretch factor 1
        
        # Right panel: Track info + controls (50%)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)  # Stretch factor 1
        
        self.setLayout(main_layout)
        
        # Set background
        self.setStyleSheet("""
            PlayerScreen {
                background-color: #000000;
            }
        """)
        
        print("[INFO] PlayerScreen initialized with setlist and track info widgets")
    
    def create_left_panel(self):
        """Create left panel (concert info + setlist)"""
        # Setlist widget handles everything for left panel
        self.setlist = SetlistWidget()
        
        # Connect signals
        self.setlist.track_selected.connect(self.on_track_selected)
        self.setlist.favorite_toggled.connect(self.on_favorite_toggled)
        
        return self.setlist
    
    def create_right_panel(self):
        """Create right panel (track info + controls)"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #000000;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Track info widget
        self.track_info = TrackInfoWidget()
        layout.addWidget(self.track_info)
        
        # Placeholder for playback controls
        controls_label = QLabel("Playback Controls")
        controls_label.setFont(QFont("Arial", 16, QFont.Bold))
        controls_label.setStyleSheet("color: #FFFFFF;")
        controls_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(controls_label)
        
        # Placeholder for progress bar
        progress_label = QLabel("Progress Bar\n(Task 9.5)")
        progress_label.setStyleSheet("""
            color: #9CA3AF;
            padding: 10px;
        """)
        progress_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(progress_label)
        
        # Placeholder for volume
        volume_label = QLabel("Volume Control\n(Task 9.7)")
        volume_label.setStyleSheet("""
            color: #9CA3AF;
            padding: 10px;
        """)
        volume_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(volume_label)
        
        # Browse shows button (bottom)
        browse_btn = QPushButton("Browse Shows")
        browse_btn.setMinimumSize(200, 50)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:pressed {
                background-color: #4B5563;
            }
        """)
        browse_btn.clicked.connect(self.on_browse_clicked)
        layout.addWidget(browse_btn)
        
        panel.setLayout(layout)
        return panel
    
    def on_browse_clicked(self):
        """Handle browse button click"""
        print("[INFO] Browse button clicked from Player screen")
        self.browse_requested.emit()
    
    def on_track_selected(self, track_index):
        """
        Handle track selection from setlist.
        
        Args:
            track_index (int): Index of selected track (0-indexed)
        """
        print(f"[INFO] PlayerScreen received track selection: {track_index}")
        self.track_selected.emit(track_index)
    
    def on_favorite_toggled(self, is_favorited):
        """
        Handle favorite toggle from setlist.
        
        Args:
            is_favorited (bool): True if favorited, False otherwise
        """
        print(f"[INFO] PlayerScreen received favorite toggle: {is_favorited}")
        self.favorite_toggled.emit(is_favorited)
    
    def load_concert(self, concert_title, location, source_type, rating, tracks):
        """
        Load a concert into the player.
        
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
        if self.setlist:
            self.setlist.load_concert(concert_title, location, source_type, rating, tracks)
            print(f"[INFO] Concert loaded into player: {concert_title}")
    
    def update_track(self, song_name, set_name, track_num, total_tracks):
        """
        Update current track information.
        
        Args:
            song_name (str): Name of the song
            set_name (str): Set indicator (e.g., "SET I", "SET II", "ENCORE")
            track_num (int): Current track number (1-indexed)
            total_tracks (int): Total number of tracks
        """
        # Update track info widget
        if self.track_info:
            self.track_info.update_track_info(song_name, set_name, track_num, total_tracks)
        
        # Highlight track in setlist (convert to 0-indexed)
        if self.setlist:
            self.setlist.set_current_track(track_num - 1)
    
    def clear_concert(self):
        """Clear current concert data"""
        if self.setlist:
            self.setlist.clear_concert()
        if self.track_info:
            self.track_info.clear_track_info()
        
        print("[INFO] Concert cleared from player")
    
    def clear_track(self):
        """Clear current track information"""
        if self.track_info:
            self.track_info.clear_track_info()


if __name__ == "__main__":
    """Test the player screen"""
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer
    
    app = QApplication(sys.argv)
    
    # Create player screen
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1280, 720)
    screen.setWindowTitle("DeadStream Player Screen - Task 9.3 Test")
    screen.show()
    
    # Load sample concert
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
    
    screen.load_concert(
        concert_title="1977/05/08 Barton Hall, Cornell University",
        location="Ithaca, NY",
        source_type="Soundboard",
        rating=4.8,
        tracks=sample_tracks
    )
    
    # Simulate track changes
    def update1():
        screen.update_track("Bertha", "SET I", 1, 17)
    
    def update2():
        screen.update_track("Scarlet Begonias", "SET II", 9, 17)
    
    def update3():
        screen.update_track("U.S. Blues", "ENCORE", 17, 17)
    
    QTimer.singleShot(1500, update1)
    QTimer.singleShot(3000, update2)
    QTimer.singleShot(5000, update3)
    
    # Connect signals for testing
    screen.track_selected.connect(lambda idx: print(f"[TEST] Track selected: {idx}"))
    screen.favorite_toggled.connect(lambda fav: print(f"[TEST] Favorite: {fav}"))
    
    sys.exit(app.exec_())
