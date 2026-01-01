#!/usr/bin/env python3
"""
Player screen for DeadStream UI.
Shows now-playing interface with track info, playback controls, and setlist.

Phase 9, Tasks 9.2 and 9.4 - Track info and playback controls integrated
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
from src.ui.widgets.playback_controls import PlaybackControlsWidget


class PlayerScreen(QWidget):
    """
    Player screen with now-playing interface.
    
    Features:
    - Left panel: Concert info + setlist (placeholder)
    - Right panel: Track info + playback controls
    
    Signals:
        browse_requested: User wants to browse shows
        play_pause_requested: User toggled play/pause
        previous_track_requested: User wants previous track
        next_track_requested: User wants next track
        skip_backward_30s_requested: User wants to skip back 30 seconds
        skip_forward_30s_requested: User wants to skip forward 30 seconds
    """
    
    # Signals
    browse_requested = pyqtSignal()
    play_pause_requested = pyqtSignal()
    previous_track_requested = pyqtSignal()
    next_track_requested = pyqtSignal()
    skip_backward_30s_requested = pyqtSignal()
    skip_forward_30s_requested = pyqtSignal()
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()
        
        # Widgets
        self.track_info = None
        self.playback_controls = None
        
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
        
        print("[INFO] PlayerScreen initialized with track info and playback controls")
    
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
        
        # Playback controls widget
        self.playback_controls = PlaybackControlsWidget()
        
        # Connect playback control signals
        self.playback_controls.play_pause_clicked.connect(self.on_play_pause)
        self.playback_controls.previous_clicked.connect(self.on_previous_track)
        self.playback_controls.next_clicked.connect(self.on_next_track)
        self.playback_controls.skip_backward_30s.connect(self.on_skip_backward)
        self.playback_controls.skip_forward_30s.connect(self.on_skip_forward)
        
        layout.addWidget(self.playback_controls)
        
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
    
    def on_play_pause(self):
        """Handle play/pause request"""
        print("[INFO] Play/pause requested from Player screen")
        self.play_pause_requested.emit()
    
    def on_previous_track(self):
        """Handle previous track request"""
        print("[INFO] Previous track requested from Player screen")
        self.previous_track_requested.emit()
    
    def on_next_track(self):
        """Handle next track request"""
        print("[INFO] Next track requested from Player screen")
        self.next_track_requested.emit()
    
    def on_skip_backward(self):
        """Handle skip backward 30s request"""
        print("[INFO] Skip backward 30s requested from Player screen")
        self.skip_backward_30s_requested.emit()
    
    def on_skip_forward(self):
        """Handle skip forward 30s request"""
        print("[INFO] Skip forward 30s requested from Player screen")
        self.skip_forward_30s_requested.emit()
    
    def update_track(self, song_name, set_name, track_num, total_tracks):
        """
        Update current track information.
        
        Args:
            song_name (str): Name of the song
            set_name (str): Set indicator (e.g., "SET I", "SET II", "ENCORE")
            track_num (int): Current track number (1-indexed)
            total_tracks (int): Total number of tracks
        """
        # Update track info display
        if self.track_info:
            self.track_info.update_track_info(song_name, set_name, track_num, total_tracks)
        
        # Update playback controls state
        if self.playback_controls:
            self.playback_controls.update_track_position(track_num, total_tracks)
    
    def set_playing(self, is_playing):
        """
        Update playing state.
        
        Args:
            is_playing (bool): Whether audio is currently playing
        """
        if self.playback_controls:
            self.playback_controls.set_playing(is_playing)
    
    def clear_track(self):
        """Clear current track information"""
        if self.track_info:
            self.track_info.clear_track_info()
        
        if self.playback_controls:
            self.playback_controls.reset()


if __name__ == "__main__":
    """Test the player screen"""
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer
    
    app = QApplication(sys.argv)
    
    # Create player screen
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("DeadStream Player Screen - Task 9.4")
    
    # Connect signals for testing
    screen.play_pause_requested.connect(lambda: print("[TEST] Play/pause signal received"))
    screen.previous_track_requested.connect(lambda: print("[TEST] Previous track signal received"))
    screen.next_track_requested.connect(lambda: print("[TEST] Next track signal received"))
    screen.skip_backward_30s_requested.connect(lambda: print("[TEST] Skip backward signal received"))
    screen.skip_forward_30s_requested.connect(lambda: print("[TEST] Skip forward signal received"))
    
    screen.show()
    
    # Simulate track changes with playback state
    def update1():
        print("[TEST] Loading track 1 of 8")
        screen.update_track("Bertha", "SET I", 1, 8)
        screen.set_playing(False)
    
    def start_playing():
        print("[TEST] Starting playback")
        screen.set_playing(True)
    
    def update2():
        print("[TEST] Moving to track 3")
        screen.update_track("Scarlet Begonias", "SET I", 3, 8)
    
    def update3():
        print("[TEST] Moving to track 8 (last track)")
        screen.update_track("One More Saturday Night", "ENCORE", 8, 8)
    
    # Schedule updates
    QTimer.singleShot(1000, update1)
    QTimer.singleShot(2000, start_playing)
    QTimer.singleShot(4000, update2)
    QTimer.singleShot(6000, update3)
    
    print("\n=== Player Screen Test (Task 9.4) ===")
    print("Track info widget shows current song/set")
    print("Playback controls update based on track position")
    print("Previous disabled on track 1, Next disabled on last track")
    print("Click controls to test signal emission")
    print("=====================================\n")
    
    sys.exit(app.exec_())
