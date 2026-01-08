#!/usr/bin/env python3
"""
Player screen for DeadStream UI - Phase 10C Restyled Version.
Shows now-playing interface with track info, playback controls, and setlist.

Phase 10C - Player Screen Restyle
- Gradient background (paintEvent pattern)
- PillButton for "Browse Shows"
- IconButton integration for media controls
- Theme Manager styling throughout
"""

import sys
import os

# Path manipulation for imports (file in src/ui/screens/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPainter, QLinearGradient, QColor

# Import Theme and Components
from src.ui.styles.theme import Theme
from src.ui.components.pill_button import PillButton
from src.ui.components.icon_button import IconButton

# Import widgets
from src.ui.widgets.track_info import TrackInfoWidget
from src.ui.widgets.progress_bar import ProgressBarWidget
from src.ui.widgets.volume_control_widget import VolumeControlWidget

# Import audio engine
from src.audio.resilient_player import ResilientPlayer, PlayerState


class PlayerScreen(QWidget):
    """
    Player screen with now-playing interface - Phase 10C Restyled.
    
    Features:
    - Gradient purple background (via paintEvent)
    - Left panel: Concert info + setlist (placeholder)
    - Right panel: Track info + playback controls + progress bar
    - IconButton media controls
    - PillButton for browse navigation
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
        self.track_info = None
        self.play_pause_btn = None
        self.prev_btn = None
        self.next_btn = None
        self.skip_back_btn = None
        self.skip_forward_btn = None
        self.progress_bar = None
        self.volume_control = None
        self.browse_btn = None
        
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
    
    def paintEvent(self, event):
        """Paint the gradient background manually."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create linear gradient from top to bottom
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(Theme.BG_PRIMARY))  # #2E2870
        gradient.setColorAt(1, QColor("#1a1a4a"))  # darker purple
        
        painter.fillRect(self.rect(), gradient)
        super().paintEvent(event)
    
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
        
        print("[INFO] PlayerScreen initialized with Phase 10C styling")
    
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
    
    # ========================================================================
    # UI CREATION - LEFT PANEL
    # ========================================================================
    
    def create_left_panel(self):
        """Create left panel with concert info and setlist"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background: transparent;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_MEDIUM)
        layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_MEDIUM,
            Theme.SPACING_LARGE
        )
        
        # Concert header
        concert_label = QLabel("Concert Information")
        concert_label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: {Theme.HEADER_LARGE}px;
            font-weight: bold;
            background: transparent;
        """)
        layout.addWidget(concert_label)
        
        # Show details placeholder
        details_label = QLabel("No show loaded")
        details_label.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: {Theme.BODY_LARGE}px;
            background: transparent;
        """)
        layout.addWidget(details_label)
        
        # Setlist header
        setlist_label = QLabel("Setlist")
        setlist_label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: {Theme.BODY_LARGE}px;
            font-weight: bold;
            background: transparent;
            margin-top: {Theme.SPACING_LARGE}px;
        """)
        layout.addWidget(setlist_label)
        
        # Setlist scroll area (placeholder)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255, 255, 255, 0.3);
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: rgba(255, 255, 255, 0.5);
            }}
        """)
        
        setlist_content = QLabel("Track list will appear here...")
        setlist_content.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: {Theme.BODY_MEDIUM}px;
            background: transparent;
            padding: {Theme.SPACING_MEDIUM}px;
        """)
        scroll_area.setWidget(setlist_content)
        layout.addWidget(scroll_area, 1)
        
        panel.setLayout(layout)
        return panel
    
    # ========================================================================
    # UI CREATION - RIGHT PANEL
    # ========================================================================
    
    def create_right_panel(self):
        """Create right panel with track info and playback controls"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background: transparent;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_LARGE)
        layout.setContentsMargins(
            Theme.SPACING_MEDIUM,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE
        )
        
        # Track info widget (top)
        self.track_info = TrackInfoWidget()
        layout.addWidget(self.track_info)
        
        # Media controls (center)
        controls_widget = self.create_media_controls()
        layout.addWidget(controls_widget)
        
        # Progress bar
        self.progress_bar = ProgressBarWidget()
        self.progress_bar.seek_requested.connect(self.on_seek)
        layout.addWidget(self.progress_bar)
        
        # Volume control
        self.volume_control = VolumeControlWidget()
        self.volume_control.volume_changed.connect(self.on_volume_changed)
        self.volume_control.mute_toggled.connect(self.on_mute_toggled)
        layout.addWidget(self.volume_control)
        
        # Add spacer
        layout.addStretch()
        
        # Browse shows button (bottom)
        self.browse_btn = PillButton("Browse Shows", variant='blue')
        self.browse_btn.setMinimumWidth(300)
        self.browse_btn.clicked.connect(self.on_browse_clicked)
        layout.addWidget(self.browse_btn, alignment=Qt.AlignCenter)
        
        panel.setLayout(layout)
        return panel
    
    def create_media_controls(self):
        """Create media control buttons using IconButton"""
        controls_widget = QWidget()
        controls_widget.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_MEDIUM)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Primary controls row (play/pause + prev/next)
        primary_row = QHBoxLayout()
        primary_row.setSpacing(Theme.BUTTON_SPACING)
        
        # Previous track button
        self.prev_btn = IconButton('back', variant='solid')
        self.prev_btn.clicked.connect(self.on_previous_track)
        primary_row.addWidget(self.prev_btn)
        
        # Play/Pause button (larger, accent variant)
        self.play_pause_btn = IconButton('play', variant='accent')
        self.play_pause_btn.setFixedSize(80, 80)  # Larger for emphasis
        self.play_pause_btn.clicked.connect(self.on_play_pause)
        primary_row.addWidget(self.play_pause_btn)
        
        # Next track button
        self.next_btn = IconButton('forward', variant='solid')
        self.next_btn.clicked.connect(self.on_next_track)
        primary_row.addWidget(self.next_btn)
        
        layout.addLayout(primary_row)
        
        # Secondary controls row (skip back/forward)
        secondary_row = QHBoxLayout()
        secondary_row.setSpacing(Theme.BUTTON_SPACING)
        
        # Skip backward 30s
        self.skip_back_btn = IconButton('minus', variant='outline')
        self.skip_back_btn.clicked.connect(self.on_skip_backward)
        secondary_row.addWidget(self.skip_back_btn)
        
        # Label
        skip_label = QLabel("-30s / +30s")
        skip_label.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: {Theme.BODY_MEDIUM}px;
            background: transparent;
        """)
        skip_label.setAlignment(Qt.AlignCenter)
        secondary_row.addWidget(skip_label, 1)
        
        # Skip forward 30s
        self.skip_forward_btn = IconButton('plus', variant='outline')
        self.skip_forward_btn.clicked.connect(self.on_skip_forward)
        secondary_row.addWidget(self.skip_forward_btn)
        
        layout.addLayout(secondary_row)
        
        controls_widget.setLayout(layout)
        return controls_widget
    
    # ========================================================================
    # AUDIO PLAYER INTEGRATION
    # ========================================================================
    
    def update_ui_from_player(self):
        """Update UI with current playback state from audio player"""
        # Get current position and duration from player
        position_ms = self.player.get_position()
        duration_ms = self.player.get_duration()
        
        # Update progress bar
        if duration_ms > 0:
            position_seconds = position_ms // 1000
            duration_seconds = duration_ms // 1000
            self.progress_bar.update_position(position_seconds, duration_seconds)
        
        # Update play/pause button state
        state = self.player.get_state()
        is_playing = (state == PlayerState.PLAYING)
        
        # Update icon (play â–¶ or pause â¸)
        if is_playing:
            self.play_pause_btn.set_icon('pause')
        else:
            self.play_pause_btn.set_icon('play')
    
    def load_track_url(self, url, track_name="Unknown Track", set_name="", 
                      track_num=1, total_tracks=1, duration=0):
        """
        Load and play a track URL
        
        Args:
            url (str): Streaming URL for the track
            track_name (str): Name of the track
            set_name (str): Set name (SET I, SET II, ENCORE)
            track_num (int): Track number in set
            total_tracks (int): Total tracks in set
            duration (int): Track duration in seconds
        """
        try:
            # Update track info display
            self.track_info.update_track_info(
                track_name, 
                set_name, 
                track_num, 
                total_tracks
            )
            
            # Set progress bar duration
            if duration > 0:
                self.progress_bar.set_duration(duration)
            
            # Load URL into player
            success = self.player.load_url(url)
            
            if success:
                # Start playback
                self.player.play()
                
                # Store current track info
                self.current_track_url = url
                self.current_track_index = track_num - 1
                self.total_tracks = total_tracks
                self.playlist_loaded = True
                
                print(f"[INFO] Loaded track: {track_name} ({set_name})")
            else:
                print(f"[ERROR] Failed to load track: {track_name}")
        
        except Exception as e:
            print(f"[ERROR] Failed to load track: {e}")
    
    # ========================================================================
    # PLAYBACK CONTROL HANDLERS
    # ========================================================================
    
    def on_play_pause(self):
        """Handle play/pause button click"""
        state = self.player.get_state()
        
        if state == PlayerState.PLAYING:
            self.player.pause()
            print("[INFO] Playback paused")
        else:
            self.player.play()
            print("[INFO] Playback resumed")
    
    def on_previous_track(self):
        """Handle previous track request"""
        print("[INFO] Previous track clicked (not implemented - needs playlist integration)")
        # Phase 11: Implement full playlist navigation
    
    def on_next_track(self):
        """Handle next track request"""
        print("[INFO] Next track clicked (not implemented - needs playlist integration)")
        # Phase 11: Implement full playlist navigation
    
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
    
    def on_browse_clicked(self):
        """Handle browse button click"""
        print("[INFO] Browse button clicked")
        self.browse_requested.emit()
    
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
    """Test the restyled player screen"""
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer
    from src.database.queries import get_show_by_date, get_top_rated_shows
    from src.api.metadata import get_metadata, extract_audio_files
    
    app = QApplication(sys.argv)
    
    # Create player screen
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("DeadStream Player - Phase 10C Restyled")
    
    # Connect browse signal
    screen.browse_requested.connect(lambda: print("[TEST] Browse requested signal received"))
    
    # Load test show after 1 second
    def load_test_show():
        print("\n[TEST] Loading Cornell '77 for testing...")
        shows = get_show_by_date('1977-05-08')
        
        if shows:
            try:
                metadata = get_metadata(shows[0]['identifier'])
                audio_files = extract_audio_files(metadata)
                
                if audio_files:
                    # Load first track
                    first_track = audio_files[0]
                    url = f"https://archive.org/download/{shows[0]['identifier']}/{first_track['name']}"
                    
                    screen.load_track_url(
                        url=url,
                        track_name=first_track.get('title', 'Unknown'),
                        set_name="SET I",
                        track_num=1,
                        total_tracks=len(audio_files),
                        duration=0
                    )
                    print("[PASS] Test show loaded successfully")
                else:
                    print("[FAIL] No audio files found in show")
            except Exception as e:
                print(f"[ERROR] Failed to load test show: {e}")
        else:
            print("[FAIL] Could not find test show")
    
    screen.show()
    
    # Load test show after 1 second
    QTimer.singleShot(1000, load_test_show)
    
    # Test instructions
    print("\n" + "=" * 70)
    print("PHASE 10C PLAYER SCREEN RESTYLE TEST")
    print("=" * 70)
    print("Features:")
    print("  - Gradient purple background (paintEvent)")
    print("  - IconButton media controls (play, pause, skip)")
    print("  - PillButton for 'Browse Shows' (blue variant)")
    print("  - Theme Manager styling throughout")
    print("\nInteractions:")
    print("  - Play/Pause: Controls actual playback")
    print("  - Progress slider: Seeks to position")
    print("  - Volume slider: Changes volume")
    print("  - Mute button: Mutes/unmutes")
    print("  - Skip buttons: Skip 30s forward/backward")
    print("  - Browse Shows: Emits browse_requested signal")
    print("\nPress Ctrl+C to exit")
    print("=" * 70 + "\n")
    
    sys.exit(app.exec_())
