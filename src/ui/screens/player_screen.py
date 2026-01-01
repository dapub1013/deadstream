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
from src.ui.widgets.volume_control_widget import VolumeControlWidget
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
    volume_changed = pyqtSignal(int)  # Volume level (0-100)
    mute_toggled = pyqtSignal(bool)   # True=muted, False=unmuted
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()
        
        # Widgets
        self.track_info = None
        self.playback_controls = None
        self.progress_bar = None
        self.volume_control = None
        
        # Playlist state
        self.current_track_index = 0  # Current track (0-indexed)
        self.total_tracks = 0         # Total tracks in playlist
        self.playlist_loaded = False  # Whether a playlist is loaded
        
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
        
        # Volume control widget
        self.volume_control = VolumeControlWidget()
        
        # Connect volume control signals
        self.volume_control.volume_changed.connect(self.on_volume_changed)
        self.volume_control.mute_toggled.connect(self.on_mute_toggled)
        
        layout.addWidget(self.volume_control)
        
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
        if not self.playlist_loaded or self.total_tracks == 0:
            print("[WARN] No playlist loaded, cannot skip to previous track")
            return
        
        # Check if we're at the first track
        if self.current_track_index <= 0:
            print(f"[INFO] Already at first track (1/{self.total_tracks})")
            # Could restart current track here in the future
            return
        
        # Move to previous track
        self.current_track_index -= 1
        print(f"[INFO] Previous track requested: moving to track {self.current_track_index + 1}/{self.total_tracks}")
        
        # Emit signal for main app to load the track
        self.previous_track_requested.emit()
        
        # Update UI to reflect new track position
        self._update_navigation_state()
    
    def on_next_track(self):
        """Handle next track request"""
        if not self.playlist_loaded or self.total_tracks == 0:
            print("[WARN] No playlist loaded, cannot skip to next track")
            return
        
        # Check if we're at the last track
        if self.current_track_index >= self.total_tracks - 1:
            print(f"[INFO] Already at last track ({self.current_track_index + 1}/{self.total_tracks})")
            # Could loop back to first track here in the future
            return
        
        # Move to next track
        self.current_track_index += 1
        print(f"[INFO] Next track requested: moving to track {self.current_track_index + 1}/{self.total_tracks}")
        
        # Emit signal for main app to load the track
        self.next_track_requested.emit()
        
        # Update UI to reflect new track position
        self._update_navigation_state()
    
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
    
    def on_volume_changed(self, volume):
        """
        Handle volume change request.
        
        Args:
            volume (int): New volume level (0-100)
        """
        print(f"[INFO] Volume changed to {volume}% from Player screen")
        self.volume_changed.emit(volume)
    
    def on_mute_toggled(self, is_muted):
        """
        Handle mute toggle request.
        
        Args:
            is_muted (bool): True if muted, False if unmuted
        """
        print(f"[INFO] Mute {'ON' if is_muted else 'OFF'} from Player screen")
        self.mute_toggled.emit(is_muted)
    
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
    
    def set_volume(self, volume):
        """
        Set volume level.
        
        Args:
            volume (int): Volume level (0-100)
        """
        if self.volume_control:
            self.volume_control.set_volume(volume)
    
    def get_volume(self):
        """
        Get current volume level.
        
        Returns:
            int: Current volume (0-100), or 50 if volume control not initialized
        """
        if self.volume_control:
            return self.volume_control.get_volume()
        return 50
    
    def mute(self):
        """Mute audio"""
        if self.volume_control:
            self.volume_control.mute()
    
    def unmute(self):
        """Unmute audio"""
        if self.volume_control:
            self.volume_control.unmute()
    
    def toggle_mute(self):
        """Toggle mute state"""
        if self.volume_control:
            self.volume_control.toggle_mute()
    
    def is_muted(self):
        """
        Check if currently muted.
        
        Returns:
            bool: True if muted, False otherwise
        """
        if self.volume_control:
            return self.volume_control.is_currently_muted()
        return False
    
    def _update_navigation_state(self):
        """
        Update navigation button states based on current position.
        Disables previous button at first track, next button at last track.
        """
        if not self.playback_controls or not self.playlist_loaded:
            return
        
        # Update track position display
        self.playback_controls.update_track_position(
            self.current_track_index + 1,  # Display as 1-indexed
            self.total_tracks
        )
    
    def load_playlist(self, track_count):
        """
        Initialize playlist with given number of tracks.
        
        Args:
            track_count (int): Total number of tracks in playlist
        """
        self.total_tracks = track_count
        self.current_track_index = 0
        self.playlist_loaded = True
        
        print(f"[INFO] Playlist loaded with {track_count} tracks")
        
        # Update navigation state
        self._update_navigation_state()
    
    def get_current_track_index(self):
        """
        Get current track index (0-based).
        
        Returns:
            int: Current track index, or 0 if no playlist loaded
        """
        return self.current_track_index if self.playlist_loaded else 0
    
    def set_current_track(self, track_index):
        """
        Set current track index directly (for external playlist control).
        
        Args:
            track_index (int): Track index to set (0-based)
        """
        if not self.playlist_loaded:
            print("[WARN] Cannot set track: no playlist loaded")
            return
        
        if track_index < 0 or track_index >= self.total_tracks:
            print(f"[ERROR] Invalid track index: {track_index} (valid range: 0-{self.total_tracks - 1})")
            return
        
        self.current_track_index = track_index
        print(f"[INFO] Current track set to {track_index + 1}/{self.total_tracks}")
        
        # Update UI
        self._update_navigation_state()
    
    def clear_track(self):
        """Clear current track information and reset playlist state"""
        if self.track_info:
            self.track_info.clear_track_info()
        
        if self.playback_controls:
            self.playback_controls.reset()
        
        if self.progress_bar:
            self.progress_bar.reset()
        
        # Reset playlist state
        self.current_track_index = 0
        self.total_tracks = 0
        self.playlist_loaded = False
        
        print("[INFO] Track cleared and playlist state reset")


if __name__ == "__main__":
    """Test the player screen with track navigation"""
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
    screen.setWindowTitle("DeadStream Player Screen - Task 9.6: Track Navigation")
    
    # Test playlist data
    test_playlist = [
        {"name": "China Cat Sunflower", "set": "SET I", "duration": 300},
        {"name": "I Know You Rider", "set": "SET I", "duration": 360},
        {"name": "Scarlet Begonias", "set": "SET I", "duration": 420},
        {"name": "Fire on the Mountain", "set": "SET I", "duration": 480},
        {"name": "Dark Star", "set": "SET II", "duration": 1200},
        {"name": "Playing in the Band", "set": "SET II", "duration": 900},
        {"name": "Uncle John's Band", "set": "ENCORE", "duration": 420},
    ]
    
    current_track_idx = 0
    current_time = 0
    is_playing = False
    
    def load_track(index):
        """Load a specific track from the test playlist"""
        global current_track_idx, current_time
        
        if index < 0 or index >= len(test_playlist):
            print(f"[TEST] Invalid track index: {index}")
            return
        
        current_track_idx = index
        current_time = 0
        
        track = test_playlist[index]
        print(f"\n[TEST] Loading track {index + 1}/{len(test_playlist)}: {track['name']}")
        
        # Update screen with track info
        screen.set_current_track(index)
        screen.update_track(
            track['name'],
            track['set'],
            index + 1,
            len(test_playlist)
        )
        screen.set_duration(track['duration'])
        screen.update_progress(0, track['duration'])
    
    def on_play_pause():
        """Toggle play/pause state"""
        global is_playing
        is_playing = not is_playing
        screen.set_playing(is_playing)
        print(f"[TEST] {'Playing' if is_playing else 'Paused'}")
    
    def on_next_track():
        """Handle next track button"""
        next_idx = current_track_idx + 1
        if next_idx < len(test_playlist):
            load_track(next_idx)
        else:
            print("[TEST] Already at last track")
    
    def on_previous_track():
        """Handle previous track button"""
        prev_idx = current_track_idx - 1
        if prev_idx >= 0:
            load_track(prev_idx)
        else:
            print("[TEST] Already at first track")
    
    def on_skip_backward():
        """Handle 30s backward skip"""
        global current_time
        current_time = max(0, current_time - 30)
        track = test_playlist[current_track_idx]
        screen.update_progress(current_time, track['duration'])
        print(f"[TEST] Skipped back 30s to {current_time}s")
    
    def on_skip_forward():
        """Handle 30s forward skip"""
        global current_time
        track = test_playlist[current_track_idx]
        current_time = min(track['duration'], current_time + 30)
        screen.update_progress(current_time, track['duration'])
        print(f"[TEST] Skipped forward 30s to {current_time}s")
    
    def on_seek(position):
        """Handle seek to position"""
        global current_time
        current_time = position
        print(f"[TEST] Seeked to {position}s")
    
    def update_progress():
        """Update progress every second during playback"""
        global current_time
        
        if not is_playing:
            return
        
        track = test_playlist[current_track_idx]
        
        if current_time < track['duration']:
            current_time += 1
            screen.update_progress(current_time, track['duration'])
        else:
            # Track finished, auto-advance to next
            print("\n[TEST] Track finished, auto-advancing...")
            on_next_track()
    
    # Connect signals
    screen.play_pause_requested.connect(on_play_pause)
    screen.previous_track_requested.connect(on_previous_track)
    screen.next_track_requested.connect(on_next_track)
    screen.skip_backward_30s_requested.connect(on_skip_backward)
    screen.skip_forward_30s_requested.connect(on_skip_forward)
    screen.seek_requested.connect(on_seek)
    screen.volume_changed.connect(lambda v: print(f"[TEST] Volume changed to {v}%"))
    screen.mute_toggled.connect(lambda m: print(f"[TEST] Mute {'ON' if m else 'OFF'}"))
    
    screen.show()
    
    # Initialize with playlist
    print("\n[TEST] Initializing playlist...")
    screen.load_playlist(len(test_playlist))
    
    # Load first track after 1 second
    QTimer.singleShot(1000, lambda: load_track(0))
    
    # Start playback after 2 seconds
    QTimer.singleShot(2000, lambda: on_play_pause())
    
    # Update progress every second
    app.progress_timer = QTimer()
    app.progress_timer.timeout.connect(update_progress)
    app.progress_timer.start(1000)
    
    # Cleanup on exit
    screen.destroyed.connect(app.cleanup)
    
    print("\n=== Player Screen Navigation + Volume Test (Tasks 9.6-9.7) ===")
    print("Test Playlist:")
    for i, track in enumerate(test_playlist):
        print(f"  {i + 1}. {track['name']} ({track['set']}) - {track['duration']}s")
    print("\nPlaylist loads after 1 second")
    print("First track plays after 2 seconds")
    print("Track auto-advances when finished")
    print("\nTest navigation buttons:")
    print("  - Previous: Go back one track")
    print("  - Next: Skip to next track")
    print("  - Previous at Track 1: Shows warning")
    print("  - Next at Track 7: Shows warning")
    print("\nTest volume controls:")
    print("  - Drag slider to change volume")
    print("  - Click speaker button to mute/unmute")
    print("  - Move slider while muted to unmute")
    print("=================================================================\n")
    
    exit_code = app.exec_()
    app.cleanup()
    sys.exit(exit_code)
