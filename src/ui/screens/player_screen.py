#!/usr/bin/env python3
"""
Player screen for DeadStream UI - Phase 10.2: Auto-Play Next Track

Shows now-playing interface with track info, playback controls, and setlist.
NOW WITH: Automatic track advancement when current track ends!

Phase 10, Task 10.2 - Auto-Play Next Track Implementation
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
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

# Import widgets
from src.ui.widgets.track_info import TrackInfoWidget
from src.ui.widgets.playback_controls import PlaybackControlsWidget
from src.ui.widgets.progress_bar import ProgressBarWidget
from src.ui.widgets.volume_control_widget import VolumeControlWidget

# Import audio engine
from src.audio.resilient_player import ResilientPlayer, PlayerState


class PlayerScreen(QWidget):
    """
    Player screen with now-playing interface.
    
    Features:
    - Track info display (song name, set)
    - Full playback controls (play/pause, prev/next, skip 30s)
    - Progress bar with seek
    - Volume control with mute
    - Auto-play next track when current track ends (NEW!)
    
    Signals:
        browse_requested: User wants to browse shows
    """
    
    # Signals
    browse_requested = pyqtSignal()  # Navigate to browse screen
    
    def __init__(self):
        super().__init__()
        
        # Playlist state
        self.current_playlist = []  # List of track dicts
        self.current_track_index = 0
        self.total_tracks = 0
        self.playlist_loaded = False
        
        # Create audio player
        self.player = ResilientPlayer()
        
        # NEW: Connect track end callback for auto-play
        self.player.on_track_ended = self.on_track_ended_auto_advance
        print("[INFO] Auto-play next track enabled")
        
        # Build UI
        self._build_ui()
        
        # Start UI update timer (200ms = 5 updates/second)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui_from_player)
        self.update_timer.start(200)
        
        print("[INFO] PlayerScreen initialized with auto-play")
    
    def _build_ui(self):
        """Build the player screen layout"""
        # Main horizontal layout (50/50 split)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left panel: Concert info + setlist (placeholder for now)
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #1F2937;")
        left_layout = QVBoxLayout()
        
        # Placeholder - will be ConcertInfoWidget in Phase 10.1
        concert_label = QLabel("Concert Info")
        concert_label.setStyleSheet("color: white; font-size: 24px; padding: 20px;")
        left_layout.addWidget(concert_label)
        
        # Placeholder for setlist
        setlist_label = QLabel("Setlist will appear here")
        setlist_label.setStyleSheet("color: #9CA3AF; padding: 20px;")
        left_layout.addWidget(setlist_label)
        
        left_panel.setLayout(left_layout)
        
        # Right panel: Now playing + controls
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #000000;")
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(40, 40, 40, 40)
        right_layout.setSpacing(30)
        
        # Track info widget
        self.track_info = TrackInfoWidget()
        right_layout.addWidget(self.track_info)
        
        # Playback controls widget
        self.playback_controls = PlaybackControlsWidget()
        right_layout.addWidget(self.playback_controls)
        
        # Progress bar widget
        self.progress_bar = ProgressBarWidget()
        right_layout.addWidget(self.progress_bar)
        
        # Volume control widget
        self.volume_control = VolumeControlWidget()
        right_layout.addWidget(self.volume_control)
        
        # Browse shows button
        browse_btn = QPushButton("Browse Shows")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 16px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        browse_btn.clicked.connect(self.browse_requested.emit)
        right_layout.addWidget(browse_btn)
        
        right_panel.setLayout(right_layout)
        
        # Add panels to main layout (50/50 split)
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        
        # Connect widget signals to handlers
        self._connect_signals()
    
    def _connect_signals(self):
        """Connect widget signals to player screen handlers"""
        # Playback controls
        self.playback_controls.play_pause_clicked.connect(self.on_play_pause)
        self.playback_controls.previous_clicked.connect(self.on_previous_track)
        self.playback_controls.next_clicked.connect(self.on_next_track)
        self.playback_controls.skip_backward_30s.connect(self.on_skip_backward)
        self.playback_controls.skip_forward_30s.connect(self.on_skip_forward)
        
        # Progress bar
        self.progress_bar.seek_requested.connect(self.on_seek)
        
        # Volume control
        self.volume_control.volume_changed.connect(self.on_volume_changed)
        self.volume_control.mute_toggled.connect(self.on_mute_toggled)
    
    # ========================================================================
    # UI UPDATE LOOP (200ms timer)
    # ========================================================================
    
    def update_ui_from_player(self):
        """Update UI widgets from player state - called every 200ms"""
        if not self.playlist_loaded:
            return
        
        # Get player state
        position_ms = self.player.get_position()
        duration_ms = self.player.get_duration()
        is_playing = self.player.is_playing()
        
        # Convert to seconds for widgets
        position_sec = position_ms / 1000.0
        duration_sec = duration_ms / 1000.0
        
        # Update progress bar
        self.progress_bar.update_progress(position_sec, duration_sec)
        
        # Update playback controls state
        self.playback_controls.update_state(
            is_playing,
            self.current_track_index + 1,  # Display as 1-based
            self.total_tracks
        )
        
        # FALLBACK: Polling-based track end detection
        # This catches cases where VLC event doesn't fire reliably
        if is_playing and duration_ms > 0:
            # Check if we're within 1 second of the end
            time_remaining = duration_ms - position_ms
            
            if time_remaining < 1000 and time_remaining >= 0:  # Last second
                if not hasattr(self, '_track_end_triggered'):
                    self._track_end_triggered = False
                
                if not self._track_end_triggered:
                    print("[POLLING] Detected track near end - triggering auto-advance")
                    self._track_end_triggered = True
                    # Schedule the callback to avoid blocking UI
                    from PyQt5.QtCore import QTimer
                    QTimer.singleShot(100, self.on_track_ended_auto_advance)
            elif time_remaining > 2000:
                # Reset trigger flag if we're not near the end
                # (handles seeks backward)
                self._track_end_triggered = False
    
    # ========================================================================
    # TRACK MANAGEMENT
    # ========================================================================
    
    def load_and_play_track(self, track_index):
        """
        Load and play a specific track from the playlist
        
        Args:
            track_index: Index of track to play (0-based)
        """
        if not self.playlist_loaded:
            print("[ERROR] Cannot play track - no playlist loaded")
            return
        
        if track_index < 0 or track_index >= self.total_tracks:
            print(f"[ERROR] Invalid track index: {track_index}")
            return
        
        # Reset track end trigger flag
        self._track_end_triggered = False
        
        # Get track data
        track = self.current_playlist[track_index]
        
        print(f"[INFO] Loading track {track_index + 1}/{self.total_tracks}")
        print(f"[INFO] Track: {track.get('title', 'Unknown')}")
        
        # Update current index
        self.current_track_index = track_index
        
        # Update track info widget
        track_title = track.get('title', 'Unknown Track')
        set_name = track.get('set', 'Unknown Set')
        self.track_info.update_track(track_title, set_name)
        
        # Load URL into player
        track_url = track.get('url', '')
        if not track_url:
            print("[ERROR] Track has no URL!")
            return
        
        self.player.load_url(track_url)
        
        # Start playback
        self.player.play()
        
        print(f"[PASS] Now playing: {track_title}")
    
    # ========================================================================
    # NEW: AUTO-PLAY NEXT TRACK
    # ========================================================================
    
    def on_track_ended_auto_advance(self):
        """
        Called automatically when current track ends (via VLC event)
        
        This is the callback registered with ResilientPlayer.on_track_ended
        It automatically advances to the next track if available.
        """
        print("[INFO] Track ended - auto-advancing to next track")
        
        # Check if there's a next track
        if self.current_track_index < self.total_tracks - 1:
            # Play next track
            next_index = self.current_track_index + 1
            print(f"[INFO] Auto-playing track {next_index + 1}/{self.total_tracks}")
            self.load_and_play_track(next_index)
        else:
            # End of playlist
            print("[INFO] Reached end of playlist - stopping playback")
            self.player.stop()
            # Could add: emit a signal, show "End of Show" message, etc.
    
    # ========================================================================
    # PLAYBACK CONTROL HANDLERS
    # ========================================================================
    
    def on_play_pause(self):
        """Handle play/pause button click"""
        if self.player.is_playing():
            self.player.pause()
            print("[INFO] Playback paused")
        else:
            self.player.play()
            print("[INFO] Playback resumed")
    
    def on_previous_track(self):
        """Handle previous track request"""
        if not self.playlist_loaded:
            print("[WARN] No playlist loaded")
            return
        
        # Check if we're more than 3 seconds into the track
        position_ms = self.player.get_position()
        if position_ms > 3000:  # 3 seconds
            # Restart current track
            print("[INFO] Restarting current track")
            self.player.seek(0)
        else:
            # Go to actual previous track
            if self.current_track_index > 0:
                prev_index = self.current_track_index - 1
                print(f"[INFO] Going to previous track: {prev_index + 1}/{self.total_tracks}")
                self.load_and_play_track(prev_index)
            else:
                print("[INFO] Already at first track")
    
    def on_next_track(self):
        """Handle next track request"""
        if not self.playlist_loaded:
            print("[WARN] No playlist loaded")
            return
        
        # Check if there's a next track
        if self.current_track_index < self.total_tracks - 1:
            next_index = self.current_track_index + 1
            print(f"[INFO] Skipping to next track: {next_index + 1}/{self.total_tracks}")
            self.load_and_play_track(next_index)
        else:
            print("[INFO] Already at last track")
    
    def on_skip_backward(self):
        """Handle 30s backward skip"""
        self.player.skip_backward(30)
        print("[INFO] Skipped backward 30 seconds")
    
    def on_skip_forward(self):
        """Handle 30s forward skip"""
        self.player.skip_forward(30)
        print("[INFO] Skipped forward 30 seconds")
    
    def on_seek(self, position):
        """Handle seek to position"""
        # Convert seconds to milliseconds
        position_ms = position * 1000
        self.player.seek(position_ms)
        print(f"[INFO] Seeked to {position} seconds")
    
    def on_volume_changed(self, volume):
        """Handle volume change"""
        self.player.set_volume(volume)
        print(f"[INFO] Volume changed to {volume}%")
    
    def on_mute_toggled(self, muted):
        """Handle mute toggle"""
        if muted:
            self.player.mute()
            print("[INFO] Audio muted")
        else:
            self.player.unmute()
            print("[INFO] Audio unmuted")
    
    # ========================================================================
    # PUBLIC API (called by MainWindow)
    # ========================================================================
    
    def load_show(self, show_data):
        """
        Load a show's playlist
        
        Args:
            show_data: Dictionary with show info including 'tracks' list
        """
        print(f"[INFO] Loading show: {show_data.get('identifier', 'unknown')}")
        
        # Extract playlist
        tracks = show_data.get('tracks', [])
        if not tracks:
            print("[ERROR] Show has no tracks!")
            return
        
        # Store playlist
        self.current_playlist = tracks
        self.total_tracks = len(tracks)
        self.playlist_loaded = True
        
        print(f"[INFO] Loaded {self.total_tracks} tracks")
        
        # Start playing first track
        self.current_track_index = 0
        self.load_and_play_track(0)
    
    # ========================================================================
    # CLEANUP
    # ========================================================================
    
    def closeEvent(self, event):
        """Clean up when screen is closed"""
        print("[INFO] PlayerScreen closing - cleaning up resources")
        
        # Stop update timer
        if self.update_timer:
            self.update_timer.stop()
            print("[INFO] UI update timer stopped")
        
        # Stop playback and cleanup player
        if self.player:
            self.player.stop()
            print("[INFO] Audio playback stopped")
        
        # Accept close event
        event.accept()


if __name__ == "__main__":
    """Test the player screen with auto-play next track"""
    from PyQt5.QtWidgets import QApplication
    from src.database.queries import get_show_by_date, get_top_rated_shows
    from src.api.metadata import get_metadata, extract_audio_files
    
    app = QApplication(sys.argv)
    
    # Create player screen
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("DeadStream Player - Task 10.2: Auto-Play Next Track")
    screen.show()
    
    # Load a test show with multiple tracks
    print("\n[TEST] Getting test show from database...")
    
    # Try Cornell '77 first
    shows = get_show_by_date('1977-05-08')
    
    if not shows:
        # Fallback to top-rated
        print("[TEST] Cornell not found, using top-rated show")
        shows = get_top_rated_shows(limit=1, min_reviews=5)
    
    if shows:
        show = shows[0]
        print(f"[TEST] Found show: {show['identifier']}")
        
        # Get metadata with tracks
        metadata = get_metadata(show['identifier'])
        audio_files = extract_audio_files(metadata)
        
        # Build track list (first 3 tracks for testing)
        test_tracks = []
        for i, audio in enumerate(audio_files[:3]):  # Just first 3 tracks
            test_tracks.append({
                'title': audio.get('title', f'Track {i+1}'),
                'url': f"https://archive.org/download/{show['identifier']}/{audio['name']}",
                'set': 'Set I',  # Simplified for test
                'duration': audio.get('length', 0)
            })
        
        # Create show data
        show_data = {
            'identifier': show['identifier'],
            'date': show['date'],
            'venue': show.get('venue', 'Unknown Venue'),
            'tracks': test_tracks
        }
        
        print(f"[TEST] Loading {len(test_tracks)} tracks for auto-play test")
        print("[TEST] Tracks will auto-advance when each one ends!")
        
        # Load show
        screen.load_show(show_data)
    else:
        print("[ERROR] Could not find test show!")
    
    sys.exit(app.exec_())
