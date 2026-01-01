#!/usr/bin/env python3
"""
Player screen for DeadStream UI.
Shows now-playing interface with track info, playback controls, and setlist.

Phase 9, Task 9.2 - Track info display integrated
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

# Import track info widget
from src.ui.widgets.track_info import TrackInfoWidget


class PlayerScreen(QWidget):
    """
    Player screen with now-playing interface.
    
    Features:
    - Left panel: Concert info + setlist (placeholder)
    - Right panel: Track info + playback controls
    
    Signals:
        browse_requested: User wants to browse shows
    """
    
    # Signals
    browse_requested = pyqtSignal()
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()
        
        # Track info widget
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
        
        print("[INFO] PlayerScreen initialized with track info widget")
    
    def create_left_panel(self):
        """Create left panel (concert info + setlist)"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-right: 1px solid #374151;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Placeholder for concert info
        concert_label = QLabel("Concert Info")
        concert_label.setFont(QFont("Arial", 18, QFont.Bold))
        concert_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(concert_label)
        
        # Placeholder for setlist
        setlist_label = QLabel("Setlist will appear here\n(Task 9.3)")
        setlist_label.setStyleSheet("""
            color: #9CA3AF;
            padding: 20px;
        """)
        layout.addWidget(setlist_label)
        
        layout.addStretch()
        panel.setLayout(layout)
        
        return panel
    
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
    
    def update_track(self, song_name, set_name, track_num, total_tracks):
        """
        Update current track information.
        
        Args:
            song_name (str): Name of the song
            set_name (str): Set indicator (e.g., "SET I", "SET II", "ENCORE")
            track_num (int): Current track number (1-indexed)
            total_tracks (int): Total number of tracks
        """
        if self.track_info:
            self.track_info.update_track_info(song_name, set_name, track_num, total_tracks)
    
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
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("DeadStream Player Screen")
    screen.show()
    
    # Simulate track changes
    def update1():
        screen.update_track("Scarlet Begonias", "SET I", 3, 8)
    
    def update2():
        screen.update_track("Fire on the Mountain", "SET I", 4, 8)
    
    def update3():
        screen.update_track("Dark Star", "SET II", 1, 6)
    
    QTimer.singleShot(1000, update1)
    QTimer.singleShot(3000, update2)
    QTimer.singleShot(5000, update3)
    
    sys.exit(app.exec_())