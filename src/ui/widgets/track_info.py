#!/usr/bin/env python3
"""
Track info widget for DeadStream player screen.
Displays current song name, set indicator, and track counter.

Phase 9, Task 9.2
"""

# Path manipulation for imports (file in src/ui/widgets/)
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont


class TrackInfoWidget(QWidget):
    """
    Displays current track information on the player screen.
    
    Shows:
    - "NOW PLAYING" label
    - Current song name (large, bold)
    - Set indicator (which set it's from)
    - Track counter (Track X of Y)
    
    Attributes:
        current_song (str): Name of the currently playing song
        current_set (str): Set indicator (SET I, SET II, ENCORE)
        track_number (int): Current track number
        total_tracks (int): Total number of tracks
    """
    
    def __init__(self):
        """Initialize track info widget"""
        super().__init__()
        self.current_song = "No Track Playing"
        self.current_set = ""
        self.track_number = 0
        self.total_tracks = 0
        
        self.init_ui()
    
    def init_ui(self):
        """Set up the track info display"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # "NOW PLAYING" label (small, gray, uppercase)
        self.now_playing_label = QLabel("NOW PLAYING")
        self.now_playing_label.setAlignment(Qt.AlignCenter)
        self.now_playing_label.setStyleSheet("""
            color: #9CA3AF;
            font-size: 14px;
            font-weight: normal;
            letter-spacing: 2px;
            text-transform: uppercase;
        """)
        layout.addWidget(self.now_playing_label)
        
        # Song name (3xl font, bold, white)
        self.song_label = QLabel(self.current_song)
        self.song_label.setAlignment(Qt.AlignCenter)
        self.song_label.setWordWrap(True)
        song_font = QFont("Arial", 30, QFont.Bold)
        self.song_label.setFont(song_font)
        self.song_label.setStyleSheet("""
            color: #FFFFFF;
            padding: 10px;
        """)
        layout.addWidget(self.song_label)
        
        # Set indicator (xl font, gray)
        self.set_label = QLabel(self.current_set)
        self.set_label.setAlignment(Qt.AlignCenter)
        set_font = QFont("Arial", 24)
        self.set_label.setFont(set_font)
        self.set_label.setStyleSheet("""
            color: #9CA3AF;
            padding: 5px;
        """)
        layout.addWidget(self.set_label)
        
        # Track counter (small text, centered, gray)
        self.track_counter_label = QLabel(self._format_track_counter())
        self.track_counter_label.setAlignment(Qt.AlignCenter)
        self.track_counter_label.setStyleSheet("""
            color: #9CA3AF;
            font-size: 16px;
            padding: 5px;
        """)
        layout.addWidget(self.track_counter_label)
        
        # Add stretch to center content vertically
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Dark background
        self.setStyleSheet("""
            TrackInfoWidget {
                background-color: #000000;
            }
        """)
    
    def _format_track_counter(self):
        """Format track counter string"""
        if self.track_number > 0 and self.total_tracks > 0:
            return f"Track {self.track_number} of {self.total_tracks}"
        return ""
    
    @pyqtSlot(str, str, int, int)
    def update_track_info(self, song_name, set_name, track_num, total):
        """
        Update the displayed track information.
        
        Args:
            song_name (str): Name of the song
            set_name (str): Set indicator (e.g., "SET I", "SET II", "ENCORE")
            track_num (int): Current track number (1-indexed)
            total (int): Total number of tracks
        """
        self.current_song = song_name
        self.current_set = set_name
        self.track_number = track_num
        self.total_tracks = total
        
        # Update labels
        self.song_label.setText(self.current_song)
        self.set_label.setText(self.current_set)
        self.track_counter_label.setText(self._format_track_counter())
        
        print(f"[INFO] Track info updated: {song_name} ({set_name}) - Track {track_num}/{total}")
    
    @pyqtSlot()
    def clear_track_info(self):
        """Clear track information (show default state)"""
        self.update_track_info("No Track Playing", "", 0, 0)
        print("[INFO] Track info cleared")


if __name__ == "__main__":
    """Test the track info widget"""
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create widget
    widget = TrackInfoWidget()
    widget.setGeometry(100, 100, 512, 400)
    widget.setWindowTitle("Track Info Widget Test")
    widget.show()
    
    # Simulate track changes after a delay
    from PyQt5.QtCore import QTimer
    
    def update1():
        widget.update_track_info("Scarlet Begonias", "SET I", 3, 8)
    
    def update2():
        widget.update_track_info("Fire on the Mountain", "SET I", 4, 8)
    
    def update3():
        widget.update_track_info("Dark Star", "SET II", 1, 6)
    
    def clear():
        widget.clear_track_info()
    
    QTimer.singleShot(1000, update1)
    QTimer.singleShot(3000, update2)
    QTimer.singleShot(5000, update3)
    QTimer.singleShot(7000, clear)
    
    sys.exit(app.exec_())