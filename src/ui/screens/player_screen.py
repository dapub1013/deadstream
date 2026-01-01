#!/usr/bin/env python3
"""
Player screen for DeadStream UI - Minimal Integration.
Shows now-playing interface with track info, playback controls, and setlist.

Phase 9, Task 9.8 - ResilientPlayer Integration (Verified Methods Only)
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
from src.ui.widgets.concert_info import ConcertInfoWidget

# Import audio engine
from src.audio.resilient_player import ResilientPlayer, PlayerState


class PlayerScreen(QWidget):
    """
    Player screen with now-playing interface.
    
    Features:
    - Left panel: Concert info + setlist (placeholder)
    - Right panel: Track info + playback controls + progress bar
    - Integrated with ResilientPlayer audio engine
    
    Signals:
        browse_requested: User wants to browse shows
    """
    
    # Signals
    browse_requested = pyqtSignal()
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()
        
        # Audio player instance
        self.player = ResilientPlayer()
        
        # UI widgets
        self.concert_info = None
        self.track_info = None
        self.playback_controls = None
        self.progress_bar = None
        self.volume_control = None
        
        # Playlist state
        self.current_track_index = 0
        self.total_tracks = 0
        self.playlist_loaded = False
        
        # Current track data
        self.current_track_url = None
        
        # UI update timer
        self.update_timer = None
        
        self.init_ui()
        self.init_audio_integration()
    
    def init_ui(self):
        """Set up the player screen UI"""
        # Main horizontal layout (split screen)
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left panel: Concert info + setlist (50%)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel: Track info + controls (50%)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        
        # Set background
        self.setStyleSheet("""
            PlayerScreen {
                background-color: #000000;
            }
        """)
        
        print("[INFO] PlayerScreen initialized with ResilientPlayer integration")
    
    def init_audio_integration(self):
        """Initialize audio engine integration"""
        # Set initial volume from player
        initial_volume = self.player.get_volume()
        if self.volume_control:
            self.volume_control.set_volume(initial_volume)
        
        # Create UI update timer (200ms = 5 updates per second)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui_from_player)
        self.update_timer.start(200)
        
        print(f"[INFO] Audio integration initialized - Volume: {initial_volume}%")
    
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
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Concert info widget (NEW - Task 10.1)
        self.concert_info = ConcertInfoWidget()
        layout.addWidget(self.concert_info)
        
        # Setlist widget (from Phase 9)
        self.setlist = SetlistWidget()
        self.setlist.track_clicked.connect(self.on_track_clicked)
        layout.addWidget(self.setlist, 1)  # Give setlist remaining space
        
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
        
        # Connect progress bar signal (VERIFIED: seek_requested exists)
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
    
    # ========================================================================
    # AUDIO PLAYER INTEGRATION
    # ========================================================================
    
    def update_ui_from_player(self):
        """Update UI with current playback state from audio player"""
        # Get current position and duration from player
        position_ms = self.player.get_position()
        duration_ms = self.player.get_duration()
        
        # Update progress bar (VERIFIED METHOD: update_position)
        if duration_ms > 0:
            position_seconds = position_ms // 1000
            duration_seconds = duration_ms // 1000
            self.progress_bar.update_position(position_seconds, duration_seconds)
        
        # Update play/pause button state (VERIFIED METHOD: set_playing)
        state = self.player.get_state()
        is_playing = (state == PlayerState.PLAYING)
        if self.playback_controls:
            self.playback_controls.set_playing(is_playing)
    
    def load_show(self, show_data):
        """
        Load and play a concert
        
        Args:
            show_data (dict): Show dictionary from browse screen
        """
        print(f"[INFO] Loading show: {show_data.get('date')} - {show_data.get('venue')}")
        
        # Store show data
        self.current_show = show_data
        
        # Load concert info (NEW - Task 10.1)
        self.concert_info.load_concert_info(show_data)
        
        # Fetch full show metadata from Archive.org
        # (This will be implemented in future integration tasks)
        # For now, create a sample track list
        
        # TODO: Replace with actual API call to fetch tracks
        sample_tracks = [
            {
                'title': 'Help on the Way',
                'duration': '5:23',
                'set_name': 'SET I',
                'url': 'https://archive.org/download/...'
            },
            {
                'title': 'Slipknot!',
                'duration': '7:45',
                'set_name': 'SET I',
                'url': 'https://archive.org/download/...'
            },
            # ... more tracks
        ]
        
        # Load setlist
        self.setlist.load_setlist(sample_tracks)
        
        # Update concert info track count (NEW - Task 10.1)
        self.concert_info.set_track_count(len(sample_tracks))
        
        # Load first track
        if sample_tracks:
            self.load_track(0)
        
        print(f"[OK] Show loaded: {len(sample_tracks)} tracks")

    def load_track_url(self, url, track_name="Unknown Track", set_name="", track_num=1, total_tracks=1, duration=0):
        """
        Load and play a track URL
        
        Args:
            url (str): Streaming URL for the track
            track_name (str): Name of the track
            set_name (str): Set name (SET I, SET II, ENCORE)
            track_num (int): Track number (1-indexed)
            total_tracks (int): Total tracks in playlist
            duration (int): Track duration in seconds (for display)
        """
        print(f"[INFO] Loading track: {track_name}")
        
        # Store current track info
        self.current_track_url = url
        self.current_track_index = track_num - 1  # Convert to 0-indexed
        self.total_tracks = total_tracks
        self.playlist_loaded = True
        
        # Update track info widget (VERIFIED METHOD: update_track_info with 4 args)
        if self.track_info:
            self.track_info.update_track_info(
                song_name=track_name,
                set_name=set_name,
                track_num=track_num,
                total=total_tracks
            )
        
        # Update playback controls (VERIFIED METHOD: update_track_position)
        if self.playback_controls:
            self.playback_controls.update_track_position(track_num, total_tracks)
        
        # Set duration in progress bar (VERIFIED METHOD: set_duration)
        if duration > 0 and self.progress_bar:
            self.progress_bar.set_duration(duration)
        
        # Load URL into player
        if self.player.load_url(url):
            print("[PASS] Track URL loaded successfully")
            
            # Start playback
            self.player.play()
        else:
            print("[FAIL] Failed to load track URL")
    
    # ========================================================================
    # PLAYBACK CONTROL HANDLERS
    # ========================================================================
    
    def on_browse_clicked(self):
        """Handle browse button click"""
        print("[INFO] Browse button clicked")
        self.browse_requested.emit()
    
    def on_play_pause(self):
        """Handle play/pause request - directly control player"""
        state = self.player.get_state()
        
        if state == PlayerState.PLAYING:
            self.player.pause()
            print("[INFO] Playback paused")
        else:
            self.player.play()
            print("[INFO] Playback started")
    
    def on_previous_track(self):
        """Handle previous track request"""
        print("[INFO] Previous track clicked (not implemented - needs playlist integration)")
        # Phase 10: Implement full playlist navigation
    
    def on_next_track(self):
        """Handle next track request"""
        print("[INFO] Next track clicked (not implemented - needs playlist integration)")
        # Phase 10: Implement full playlist navigation
    
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
    """Test the player screen with ResilientPlayer integration"""
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer
    from src.database.queries import get_show_by_date, get_top_rated_shows
    from src.api.metadata import get_metadata, extract_audio_files
    
    app = QApplication(sys.argv)
    
    # Create player screen
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("DeadStream Player - Task 9.8: Minimal Integration")
    
    def load_test_show():
        """Load Cornell '77 as test show"""
        print("\n[TEST] Loading Cornell '77 from database...")
        shows = get_show_by_date('1977-05-08')
        
        if not shows:
            print("[TEST] Cornell '77 not found, trying top rated shows...")
            shows = get_top_rated_shows(limit=1, min_reviews=5)
        
        if shows:
            show = shows[0]
            identifier = show['identifier']
            print(f"[TEST] Found show: {identifier}")
            
            # Get metadata
            print("[TEST] Fetching show metadata...")
            metadata = get_metadata(identifier)
            audio_files = extract_audio_files(metadata)
            
            if audio_files:
                total_tracks = len(audio_files)
                print(f"[TEST] Playlist has {total_tracks} tracks")
                
                # Load first track
                first_track = audio_files[0]
                track_name = first_track.get('title', first_track.get('name', 'Unknown Track'))
                track_url = f"https://archive.org/download/{identifier}/{first_track['name']}"
                
                # Parse track length (MM:SS format)
                track_length_str = first_track.get('length', '300')
                try:
                    track_length = int(float(track_length_str))
                except ValueError:
                    if ':' in track_length_str:
                        parts = track_length_str.split(':')
                        if len(parts) == 2:
                            minutes = int(parts[0])
                            seconds = int(parts[1])
                            track_length = minutes * 60 + seconds
                        else:
                            track_length = 300
                    else:
                        track_length = 300
                
                print(f"[TEST] Loading: {track_name} ({track_length}s)")
                
                # Load and play using minimal verified API
                screen.load_track_url(
                    url=track_url,
                    track_name=track_name,
                    set_name="SET I",
                    track_num=1,
                    total_tracks=total_tracks,
                    duration=track_length
                )
                
                print("[PASS] Test show loaded and playing!")
            else:
                print("[FAIL] No audio files found in show")
        else:
            print("[FAIL] Could not find test show")
    
    screen.show()
    
    # Load test show after 1 second
    QTimer.singleShot(1000, load_test_show)
    
    # Test instructions
    print("\n" + "=" * 70)
    print("MINIMAL PLAYER INTEGRATION TEST (Task 9.8)")
    print("=" * 70)
    print("Using ONLY verified widget methods:")
    print("  - TrackInfoWidget.update_track_info(song, set, num, total)")
    print("  - PlaybackControlsWidget.set_playing(bool)")
    print("  - PlaybackControlsWidget.update_track_position(num, total)")
    print("  - ProgressBarWidget.update_position(current, total)")
    print("  - ProgressBarWidget.set_duration(seconds)")
    print("  - VolumeControlWidget.set_volume(0-100)")
    print("\nINTERACTIONS:")
    print("  - Play/Pause: Controls actual playback")
    print("  - Progress slider: Seeks to position")
    print("  - Volume slider: Changes volume")
    print("  - Mute button: Mutes/unmutes")
    print("  - Skip buttons: Skip 30s forward/backward")
    print("\nPress Ctrl+C to exit")
    print("=" * 70 + "\n")
    
    sys.exit(app.exec_())
