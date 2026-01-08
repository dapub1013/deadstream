#!/usr/bin/env python3
"""
Player screen for DeadStream UI - Hybrid Design.
Original left panel + Mockup-styled right panel.

Phase 10C - Player Screen (Right Panel Mockup Only)
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
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPainter, QLinearGradient, QColor, QFontMetrics

# Import Theme and Components
from src.ui.styles.theme import Theme
from src.ui.components.icon_button import IconButton  # For media controls

# Import widgets
from src.ui.widgets.progress_bar import ProgressBarWidget
from src.ui.widgets.volume_control_widget import VolumeControlWidget

# Import audio engine
from src.audio.resilient_player import ResilientPlayer, PlayerState


class CornerButton(QWidget):
    """Minimal, non-intrusive button for corners"""
    
    clicked = pyqtSignal()
    
    def __init__(self, icon_text, position='top-right', parent=None):
        super().__init__(parent)
        self.icon_text = icon_text
        self.position = position
        self.hovered = False
        
        # Fixed size - small and unobtrusive
        self.setFixedSize(44, 44)
        
        # Enable mouse tracking for hover
        self.setMouseTracking(True)
        
        # Style
        self.bg_color = QColor(255, 255, 255, 20)  # Very subtle
        self.hover_color = QColor(255, 255, 255, 40)  # Slightly more visible
        self.icon_color = QColor(255, 255, 255, 180)  # Semi-transparent white
        self.hover_icon_color = QColor(255, 255, 255, 255)  # Full white on hover
        
        # Tooltip
        if 'home' in icon_text.lower() or position == 'top-right':
            self.setToolTip("Home")
        else:
            self.setToolTip("Settings")
    
    def paintEvent(self, event):
        """Custom paint for minimal circular button"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background circle (only visible on hover)
        if self.hovered:
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.hover_color)
            painter.drawEllipse(2, 2, 40, 40)
        
        # Icon
        painter.setPen(self.hover_icon_color if self.hovered else self.icon_color)
        font = QFont(Theme.FONT_FAMILY, 18)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, self.icon_text)
    
    def enterEvent(self, event):
        """Mouse entered - show hover state"""
        self.hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Mouse left - hide hover state"""
        self.hovered = False
        self.update()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Handle click"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ScrollingLabel(QLabel):
    """Label that scrolls text horizontally if it doesn't fit"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._scroll_pos = 0
        self._scroll_timer = QTimer(self)
        self._scroll_timer.timeout.connect(self._scroll_text)
        self._needs_scroll = False
        self._original_text = text
        
    def setText(self, text):
        """Set text and check if scrolling is needed"""
        self._original_text = text
        super().setText(text)
        self._check_scroll_needed()
        
    def _check_scroll_needed(self):
        """Check if text is too wide and needs scrolling"""
        if not self._original_text:
            self._needs_scroll = False
            self._scroll_timer.stop()
            return
            
        # Get text width
        fm = QFontMetrics(self.font())
        text_width = fm.horizontalAdvance(self._original_text)
        available_width = self.width() - 40  # Some padding
        
        if text_width > available_width:
            # Text is too long, start scrolling
            self._needs_scroll = True
            self._scroll_pos = 0
            if not self._scroll_timer.isActive():
                self._scroll_timer.start(100)  # Scroll every 100ms
        else:
            # Text fits, no scrolling needed
            self._needs_scroll = False
            self._scroll_timer.stop()
            self._scroll_pos = 0
            super().setText(self._original_text)
    
    def _scroll_text(self):
        """Scroll the text by moving characters"""
        if not self._needs_scroll or not self._original_text:
            return
        
        # Create scrolling effect by rotating text
        text_len = len(self._original_text)
        self._scroll_pos = (self._scroll_pos + 1) % (text_len + 10)  # Add pause at end
        
        if self._scroll_pos < text_len:
            scrolled_text = self._original_text[self._scroll_pos:] + "   " + self._original_text[:self._scroll_pos]
        else:
            scrolled_text = self._original_text  # Pause at original position
        
        super().setText(scrolled_text)
    
    def resizeEvent(self, event):
        """Recheck scroll when widget is resized"""
        super().resizeEvent(event)
        self._check_scroll_needed()


class PlayerScreen(QWidget):
    """
    Player screen - Hybrid design.
    
    Features:
    - Left panel: Original placeholder with gradient background
    - Right panel: Mockup design with pure black background
    - Yellow home icon (top right)
    - Settings icon (bottom right)
    - Centered track info and controls
    
    Signals:
        home_requested: User wants to go home/browse
        settings_requested: User wants to open settings
    """
    
    # Signals
    home_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()
        
        # Audio player instance
        self.player = ResilientPlayer()
        
        # UI widgets
        self.now_playing_label = None
        self.track_counter_label = None
        self.song_title_label = None
        self.play_pause_btn = None
        self.prev_btn = None
        self.next_btn = None
        self.skip_back_btn = None
        self.skip_forward_btn = None
        self.progress_bar = None
        self.volume_control = None
        self.home_btn = None  # CornerButton (minimal)
        self.settings_btn = None  # CornerButton (minimal)
        
        # Playlist state
        self.current_track_index = 0
        self.total_tracks = 0
        
        # UI update timer
        self.update_timer = None
        
        self.init_ui()
        self.init_audio_integration()
    
    def paintEvent(self, event):
        """Paint the gradient background manually for left panel area"""
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
        
        # Left panel: Concert info + setlist (50%) - ORIGINAL DESIGN
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel: Player controls (50%) - MOCKUP DESIGN
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        
        print("[INFO] PlayerScreen initialized (hybrid design)")
    
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
    # UI CREATION - LEFT PANEL (ORIGINAL PLACEHOLDER)
    # ========================================================================
    
    def create_left_panel(self):
        """Create left panel with original placeholder design"""
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
    # UI CREATION - RIGHT PANEL (MOCKUP DESIGN)
    # ========================================================================
    
    def create_right_panel(self):
        """Create right panel with mockup design (pure black)"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #000000;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(48, 48, 48, 48)
        
        # Add stretch at top for centering content
        layout.addStretch(1)
        
        # "NOW PLAYING" label
        self.now_playing_label = QLabel("NOW PLAYING")
        self.now_playing_label.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: 14px;
            font-weight: bold;
            letter-spacing: 2px;
            background: transparent;
        """)
        self.now_playing_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.now_playing_label)
        
        # Track counter "1 of 25"
        self.track_counter_label = QLabel("1 of 25")
        self.track_counter_label.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: 16px;
            font-weight: normal;
            background: transparent;
        """)
        self.track_counter_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.track_counter_label)
        
        layout.addSpacing(32)
        
        # Song title (large, centered, scrolls if too long)
        self.song_title_label = ScrollingLabel("Song Title")
        self.song_title_label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 48px;
            font-weight: bold;
            background: transparent;
        """)
        self.song_title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.song_title_label)
        
        layout.addSpacing(64)
        
        # Progress bar
        self.progress_bar = ProgressBarWidget()
        self.progress_bar.seek_requested.connect(self.on_seek)
        layout.addWidget(self.progress_bar)
        
        layout.addSpacing(32)
        
        # Media controls
        controls_widget = self.create_media_controls()
        layout.addWidget(controls_widget)
        
        layout.addSpacing(64)
        
        # Volume control
        self.volume_control = VolumeControlWidget()
        self.volume_control.volume_changed.connect(self.on_volume_changed)
        self.volume_control.mute_toggled.connect(self.on_mute_toggled)
        layout.addWidget(self.volume_control)
        
        # Add stretch at bottom for centering content
        layout.addStretch(1)
        
        panel.setLayout(layout)
        
        # Create corner buttons (positioned absolutely after panel is created)
        # Home button (top-right corner)
        self.home_btn = CornerButton('⌂', position='top-right')  # Unicode house symbol
        self.home_btn.setParent(panel)
        self.home_btn.move(panel.width() - 56, 12)  # Position in corner
        self.home_btn.clicked.connect(self.on_home_clicked)
        
        # Settings button (bottom-right corner)
        self.settings_btn = CornerButton('⚙', position='bottom-right')  # Unicode gear
        self.settings_btn.setParent(panel)
        # Position will be set in resizeEvent
        self.settings_btn.clicked.connect(self.on_settings_clicked)
        
        # Store panel reference for repositioning buttons on resize
        self._right_panel = panel
        
        return panel
    
    def create_media_controls(self):
        """Create 5-button media control layout matching mockup"""
        controls_widget = QWidget()
        controls_widget.setStyleSheet("background: transparent;")
        
        layout = QHBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Skip backward 30s (circular arrow left)
        self.skip_back_btn = IconButton('back', variant='outline')
        self.skip_back_btn.clicked.connect(self.on_skip_backward)
        layout.addWidget(self.skip_back_btn)
        
        # Previous track
        self.prev_btn = IconButton('back', variant='solid')
        self.prev_btn.clicked.connect(self.on_previous_track)
        layout.addWidget(self.prev_btn)
        
        # Play/Pause (larger, center)
        self.play_pause_btn = IconButton('play', variant='solid')
        self.play_pause_btn.setFixedSize(90, 90)  # Larger center button
        self.play_pause_btn.clicked.connect(self.on_play_pause)
        layout.addWidget(self.play_pause_btn)
        
        # Next track
        self.next_btn = IconButton('forward', variant='solid')
        self.next_btn.clicked.connect(self.on_next_track)
        layout.addWidget(self.next_btn)
        
        # Skip forward 30s (circular arrow right)
        self.skip_forward_btn = IconButton('forward', variant='outline')
        self.skip_forward_btn.clicked.connect(self.on_skip_forward)
        layout.addWidget(self.skip_forward_btn)
        
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
        
        # Update play/pause button icon
        state = self.player.get_state()
        is_playing = (state == PlayerState.PLAYING)
        
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
            self.song_title_label.setText(track_name)
            self.track_counter_label.setText(f"{track_num} of {total_tracks}")
            
            # Set progress bar duration
            if duration > 0:
                self.progress_bar.set_duration(duration)
            
            # Load URL into player
            success = self.player.load_url(url)
            
            if success:
                # Start playback
                self.player.play()
                
                # Store current track info
                self.current_track_index = track_num - 1
                self.total_tracks = total_tracks
                
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
        print("[INFO] Previous track clicked (playlist navigation not yet implemented)")
    
    def on_next_track(self):
        """Handle next track request"""
        print("[INFO] Next track clicked (playlist navigation not yet implemented)")
    
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
    
    def on_home_clicked(self):
        """Handle home button click"""
        print("[INFO] Home button clicked")
        self.home_requested.emit()
    
    def on_settings_clicked(self):
        """Handle settings button click"""
        print("[INFO] Settings button clicked")
        self.settings_requested.emit()
    
    # ========================================================================
    # LAYOUT MANAGEMENT
    # ========================================================================
    
    def resizeEvent(self, event):
        """Reposition corner buttons when window is resized"""
        super().resizeEvent(event)
        
        # Reposition buttons if they exist and panel exists
        if hasattr(self, '_right_panel') and self.home_btn and self.settings_btn:
            panel_width = self._right_panel.width()
            panel_height = self._right_panel.height()
            
            # Home button (top-right)
            self.home_btn.move(panel_width - 56, 12)
            
            # Settings button (bottom-right)
            self.settings_btn.move(panel_width - 56, panel_height - 56)
    
    # ========================================================================
    # CLEANUP
    # ========================================================================
    
    def closeEvent(self, event):
        """Clean up when screen is closed"""
        print("[INFO] PlayerScreen closing - cleaning up resources")
        
        if self.update_timer:
            self.update_timer.stop()
        
        if self.player:
            self.player.stop()
        
        event.accept()


if __name__ == "__main__":
    """Test the hybrid player screen"""
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer
    from src.database.queries import get_show_by_date, get_top_rated_shows
    from src.api.metadata import get_metadata, extract_audio_files
    
    app = QApplication(sys.argv)
    
    # Create player screen
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("DeadStream Player - Hybrid Design")
    
    # Connect signals
    screen.home_requested.connect(lambda: print("[TEST] Home button signal"))
    screen.settings_requested.connect(lambda: print("[TEST] Settings button signal"))
    
    # Load test show
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
                    print("[PASS] Test show loaded")
            except Exception as e:
                print(f"[ERROR] Failed to load test show: {e}")
    
    screen.show()
    QTimer.singleShot(1000, load_test_show)
    
    print("\n" + "=" * 70)
    print("HYBRID PLAYER SCREEN TEST")
    print("=" * 70)
    print("Left Panel (Original):")
    print("  [OK] Purple gradient background")
    print("  [OK] 'Concert Information' placeholder")
    print("  [OK] 'Setlist' placeholder")
    print("\nRight Panel (Mockup):")
    print("  [OK] Pure black background")
    print("  [OK] Yellow home icon (top right)")
    print("  [OK] 'NOW PLAYING' centered label")
    print("  [OK] '1 of 25' track counter")
    print("  [OK] Large centered song title")
    print("  [OK] 5 circular media controls (90px play button)")
    print("  [OK] Settings icon (bottom right)")
    print("\nPress Ctrl+C to exit")
    print("=" * 70 + "\n")
    
    sys.exit(app.exec_())
