#!/usr/bin/env python3
"""
Player screen for DeadStream UI.
Shows now-playing interface with track info, playback controls, and setlist.

Phase 9, Tasks 9.2, 9.4, and 9.5 - Track info, playback controls, and progress bar integrated
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
from src.ui.widgets.progress_bar import ProgressBarWidget


class PlayerScreen(QWidget):
    """
    Player screen with now-playing interface.
    
    Features:
    - Left panel: Concert info + setlist (placeholder)
    - Right panel: Track info + playback controls + progress bar
    
    Signals:
        browse_requested: User wants to browse shows
        play_pause_requested: User toggled play/pause
        previous_track_requested: User wants previous track
        next_track_requested: User wants next track
        skip_backward_30s_requested: User wants to skip back 30 seconds
        skip_forward_30s_requested: User wants to skip forward 30 seconds
        seek_requested: User seeked to position (int: seconds)
    """
    
    # Signals
    browse_requested = pyqtSignal()
    play_pause_requested = pyqtSignal()
    previous_track_requested = pyqtSignal()
    next_track_requested = pyqtSignal()
    skip_backward_30s_requested = pyqtSignal()
    skip_forward_30s_requested = pyqtSignal()
    seek_requested = pyqtSignal(int)  # Position in seconds
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()
        
        # Widgets
        self.track_info = None
        self.playback_controls = None
        self.progress_bar = None
        
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
        
        print("[INFO] PlayerScreen initialized with track info, playback controls, and progress bar")
    
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
        setlist_label = QLabel("Setlist (Task 9.3 - Complete)")
        setlist_label.setStyleSheet("""
            color: #9CA3AF;
            padding: 20px;
        """)
        layout.addWidget(setlist_label)
        
        layout.addStretch()
        panel.setLayout(layout)
        
        return panel
    
    def create_right_panel(self):
        """Create right panel (track info + controls + progress)"""
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
        
        # Progress bar widget
        self.progress_bar = ProgressBarWidget()
        
        # Connect progress bar signal
        self.progress_bar.seek_requested.connect(self.on_seek)
        
        layout.addWidget(self.progress_bar)
        
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
    
    def on_seek(self, position):
        """
        Handle seek request.
        
        Args:
            position (int): Seek position in seconds
        """
        print(f"[INFO] Seek requested to {position}s from Player screen")
        self.seek_requested.emit(position)
    
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
    
    def update_progress(self, current_seconds, total_seconds):
        """
        Update progress bar position.
        
        Args:
            current_seconds (int): Current playback position in seconds
            total_seconds (int): Total track duration in seconds
        """
        if self.progress_bar:
            self.progress_bar.update_position(current_seconds, total_seconds)
    
    def set_duration(self, total_seconds):
        """
        Set track duration (when track loads).
        
        Args:
            total_seconds (int): Total track duration in seconds
        """
        if self.progress_bar:
            self.progress_bar.set_duration(total_seconds)
    
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
        
        if self.progress_bar:
            self.progress_bar.reset()


if __name__ == "__main__":
    """Test the player screen"""
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer
    
    class TestApp(QApplication):
        def __init__(self, argv):
            super().__init__(argv)
            self.progress_timer = None
        
        def cleanup(self):
            if self.progress_timer:
                self.progress_timer.stop()
    
    app = TestApp(sys.argv)
    
    # Create player screen
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("DeadStream Player Screen - Task 9.5")
    
    # Connect signals for testing
    screen.play_pause_requested.connect(lambda: print("[TEST] Play/pause signal received"))
    screen.previous_track_requested.connect(lambda: print("[TEST] Previous track signal received"))
    screen.next_track_requested.connect(lambda: print("[TEST] Next track signal received"))
    screen.skip_backward_30s_requested.connect(lambda: print("[TEST] Skip backward signal received"))
    screen.skip_forward_30s_requested.connect(lambda: print("[TEST] Skip forward signal received"))
    screen.seek_requested.connect(lambda pos: print(f"[TEST] Seek signal received: {pos}s"))
    
    screen.show()
    
    # Simulate track playback
    current_time = 0
    track_duration = 420  # 7 minutes
    
    def load_track():
        """Simulate loading a track"""
        print("[TEST] Loading track: Scarlet Begonias (7:00)")
        screen.update_track("Scarlet Begonias", "SET I", 3, 8)
        screen.set_duration(track_duration)
        screen.set_playing(False)
    
    def start_playback():
        """Start playback simulation"""
        global current_time
        current_time = 0
        print("[TEST] Starting playback")
        screen.set_playing(True)
    
    def update_progress():
        """Update progress every second"""
        global current_time
        if current_time < track_duration:
            current_time += 1
            screen.update_progress(current_time, track_duration)
    
    # Schedule events
    QTimer.singleShot(1000, load_track)
    QTimer.singleShot(2000, start_playback)
    
    # Update progress every second
    app.progress_timer = QTimer()
    app.progress_timer.timeout.connect(update_progress)
    app.progress_timer.start(1000)
    
    # Cleanup on exit
    screen.destroyed.connect(app.cleanup)
    
    print("\n=== Player Screen Test (Task 9.5) ===")
    print("Track loads after 1 second")
    print("Playback starts after 2 seconds")
    print("Progress bar updates every second")
    print("Drag slider to test seek functionality")
    print("Watch console for seek output")
    print("=====================================\n")
    
    exit_code = app.exec_()
    app.cleanup()
    sys.exit(exit_code)
