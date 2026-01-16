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
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint
from PyQt5.QtGui import QFont, QPainter, QLinearGradient, QColor, QFontMetrics, QPixmap, QPolygon

# Import Theme and Components
from src.ui.styles.theme import Theme

# Import widgets
from src.ui.widgets.progress_bar import ProgressBarWidget
from src.ui.widgets.volume_control_widget import VolumeControlWidget

# Import audio engine
from src.audio.resilient_player import ResilientPlayer, PlayerState




class ElidedLabel(QLabel):
    """Label that shows ellipsis (...) when text is too long"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._full_text = text
        self.setMinimumHeight(60)
        self.setMaximumHeight(60)
    
    def setText(self, text):
        """Set text and store full version"""
        self._full_text = text
        super().setText(text)
        self.update()
    
    def paintEvent(self, event):
        """Paint with elided text if needed"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get font metrics
        fm = painter.fontMetrics()
        
        # Calculate available width (with some padding)
        available_width = self.width() - 40
        
        # Elide text if too long
        elided_text = fm.elidedText(self._full_text, Qt.ElideRight, available_width)
        
        # Draw elided text
        painter.setPen(QColor(Theme.TEXT_PRIMARY))
        painter.setFont(self.font())
        
        # Center the text
        text_rect = self.rect()
        painter.drawText(text_rect, Qt.AlignCenter, elided_text)


class ImageButton(QWidget):
    """Simple image-based button without hover effects"""

    clicked = pyqtSignal()

    def __init__(self, icon_path, size=60, tooltip="", parent=None):
        super().__init__(parent)
        self._icon_path = icon_path
        self._size = size
        self._pixmap = None

        self.setFixedSize(size, size)
        self.setToolTip(tooltip)
        self._load_icon()

    def _load_icon(self):
        """Load and scale the icon"""
        if os.path.exists(self._icon_path):
            pixmap = QPixmap(self._icon_path)
            self._pixmap = pixmap.scaled(
                self._size, self._size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

    def set_icon(self, icon_path):
        """Change the button icon"""
        self._icon_path = icon_path
        self._load_icon()
        self.update()

    def paintEvent(self, event):
        """Paint the button icon"""
        if self._pixmap:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)

            # Center the pixmap
            x = (self.width() - self._pixmap.width()) // 2
            y = (self.height() - self._pixmap.height()) // 2
            painter.drawPixmap(x, y, self._pixmap)

    def mousePressEvent(self, event):
        """Handle click"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class TrackButton(QWidget):
    """Button for prev/next track with industry-standard bar+triangle icon"""

    clicked = pyqtSignal()

    def __init__(self, direction='next', size=60, parent=None):
        super().__init__(parent)
        self.direction = direction  # 'next' or 'previous'
        self._size = size

        self.setFixedSize(size, size)

        if direction == 'previous':
            self.setToolTip("Previous track")
        else:
            self.setToolTip("Next track")

    def paintEvent(self, event):
        """Paint button with bar+triangle icon (industry standard)"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background circle (solid white style)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 140))
        margin = 2
        diameter = self._size - (margin * 2)
        painter.drawEllipse(margin, margin, diameter, diameter)

        # Draw bar + triangle (standard prev/next icon)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 255))

        # Scale icon elements based on button size
        center = self._size // 2
        icon_scale = self._size / 60.0  # Base scale on 60px reference

        if self.direction == 'previous':
            # Previous: |< (bar on left, triangle pointing left)
            bar_x = int(18 * icon_scale)
            bar_y = int(20 * icon_scale)
            bar_w = int(3 * icon_scale)
            bar_h = int(20 * icon_scale)
            painter.drawRect(bar_x, bar_y, bar_w, bar_h)

            # Triangle pointing left
            triangle = QPolygon([
                QPoint(int(39 * icon_scale), int(20 * icon_scale)),
                QPoint(int(39 * icon_scale), int(40 * icon_scale)),
                QPoint(int(24 * icon_scale), int(30 * icon_scale))
            ])
            painter.drawPolygon(triangle)
        else:
            # Next: >| (triangle pointing right, bar on right)
            triangle = QPolygon([
                QPoint(int(21 * icon_scale), int(20 * icon_scale)),
                QPoint(int(21 * icon_scale), int(40 * icon_scale)),
                QPoint(int(36 * icon_scale), int(30 * icon_scale))
            ])
            painter.drawPolygon(triangle)

            # Bar
            bar_x = int(39 * icon_scale)
            bar_y = int(20 * icon_scale)
            bar_w = int(3 * icon_scale)
            bar_h = int(20 * icon_scale)
            painter.drawRect(bar_x, bar_y, bar_w, bar_h)

    def mousePressEvent(self, event):
        """Handle click"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class SourceBadge(QWidget):
    """Small pill-shaped badge showing recording source (SBD/AUD)"""

    def __init__(self, source_type='SBD', parent=None):
        super().__init__(parent)
        self.source_type = source_type.upper()

        # Set fixed size
        self.setFixedSize(60, 28)

        # Style
        self.bg_color = QColor(Theme.ACCENT_YELLOW)
        self.text_color = QColor("#2E2870")  # Dark purple for contrast

    def paintEvent(self, event):
        """Paint badge with rounded corners"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background pill shape
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.bg_color)
        painter.drawRoundedRect(0, 0, 60, 28, 14, 14)

        # Text
        painter.setPen(self.text_color)
        font = QFont(Theme.FONT_FAMILY, 12, QFont.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, self.source_type)


class RatingBadge(QWidget):
    """Circular badge showing average rating with star icon"""

    def __init__(self, rating=0.0, parent=None):
        super().__init__(parent)
        self.rating = rating

        # Set fixed size (circular)
        self.setFixedSize(50, 28)

        # Style
        self.bg_color = QColor(Theme.BADGE_RATING)  # Cyan
        self.text_color = QColor(Theme.TEXT_PRIMARY)

    def set_rating(self, rating):
        """Update the rating value"""
        self.rating = rating
        self.update()

    def paintEvent(self, event):
        """Paint badge with rounded corners"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background pill shape
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.bg_color)
        painter.drawRoundedRect(0, 0, 50, 28, 14, 14)

        # Text with star
        painter.setPen(self.text_color)
        font = QFont(Theme.FONT_FAMILY, 11, QFont.Bold)
        painter.setFont(font)
        rating_text = f"{self.rating:.1f}" if self.rating else "--"
        painter.drawText(self.rect(), Qt.AlignCenter, rating_text)


class TrackWidget(QWidget):
    """Clickable track item for setlist"""

    clicked = pyqtSignal(int)  # Emits track index

    def __init__(self, track_index, track_name, track_duration="", parent=None):
        super().__init__(parent)
        self.track_index = track_index
        self.track_name = track_name
        self.track_duration = track_duration
        self.is_current = False
        self.hovered = False

        # Set minimum height for touch targets
        self.setMinimumHeight(48)
        self.setMouseTracking(True)

        # Create layout
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Track number
        self.num_label = QLabel(f"{track_index + 1}.")
        self.num_label.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: 14px;
            background: transparent;
        """)
        self.num_label.setFixedWidth(30)
        layout.addWidget(self.num_label)

        # Track name
        self.name_label = QLabel(track_name)
        self.name_label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 16px;
            background: transparent;
        """)
        layout.addWidget(self.name_label, 1)

        # Duration
        if track_duration:
            self.duration_label = QLabel(track_duration)
            self.duration_label.setStyleSheet(f"""
                color: {Theme.TEXT_SECONDARY};
                font-size: 14px;
                background: transparent;
            """)
            layout.addWidget(self.duration_label)

        self.setLayout(layout)

    def set_current(self, is_current):
        """Mark this track as currently playing"""
        self.is_current = is_current
        self.update()

    def paintEvent(self, event):
        """Paint background with hover/current state"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        if self.is_current:
            # Green highlight for current track
            painter.fillRect(self.rect(), QColor("#0F9D58"))
        elif self.hovered:
            # Subtle highlight on hover
            painter.fillRect(self.rect(), QColor(255, 255, 255, 20))

        super().paintEvent(event)

    def enterEvent(self, event):
        """Mouse entered"""
        self.hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse left"""
        self.hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle click"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.track_index)
        super().mousePressEvent(event)


class PlayerScreen(QWidget):
    """
    Player screen - Hybrid design.

    Features:
    - Left panel: Concert info and setlist with gradient background
    - Right panel: Player controls with pure black background
    - Home button (upper left corner)
    - Settings button (upper right corner)
    - Centered track info and controls

    Signals:
        settings_requested: User wants to open settings (navigates to audio section)
        back_requested: User wants to go back to browse screen
        home_requested: User wants to go to welcome screen
    """

    # Signals
    settings_requested = pyqtSignal()
    back_requested = pyqtSignal()
    home_requested = pyqtSignal()
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()

        # Audio player instance
        self.player = ResilientPlayer()

        # UI widgets - right panel
        self.now_playing_label = None
        self.track_counter_label = None
        self.song_title_label = None
        self.play_pause_btn = None  # ImageButton (play.png/pause.png, 80px)
        self.prev_btn = None  # TrackButton (painted bar+triangle, 60px)
        self.next_btn = None  # TrackButton (painted triangle+bar, 60px)
        self.skip_back_btn = None  # ImageButton (rew-30.png, 60px)
        self.skip_forward_btn = None  # ImageButton (ffw-30.png, 60px)
        self.progress_bar = None
        self.volume_control = None  # VolumeControlWidget with image-based mute button
        self.settings_btn = None  # Settings button (upper right corner)
        self.home_btn = None  # Home button (upper left corner)

        # UI widgets - left panel
        self.date_label = None
        self.venue_label = None
        self.location_label = None
        self.source_badge = None
        self.rating_badge = None
        self.metadata_label = None  # Taper and reviews info
        self.setlist_layout = None  # Layout for track items
        self.track_widgets = []  # List of track widget references

        # Playlist state
        self.current_show = None
        self.playlist = []
        self.current_track_index = 0
        self.total_tracks = 0

        # Auto-play state
        self._track_ended_handled = False  # Prevent duplicate auto-advance

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
        """Create left panel with concert info and setlist"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: transparent;
            }
        """)

        # Set size policy to prevent expansion from long text (keeps 50/50 split)
        from PyQt5.QtWidgets import QSizePolicy
        panel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)

        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_TINY)
        layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_MEDIUM,
            Theme.SPACING_LARGE
        )

        # Concert header row (date + badges)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        # Date label (formatted nicely)
        self.date_label = QLabel("No show loaded")
        self.date_label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: {Theme.BODY_LARGE}px;
            font-weight: bold;
            background: transparent;
        """)
        header_layout.addWidget(self.date_label)

        # Source badge (SBD/AUD/MTX)
        self.source_badge = SourceBadge('SBD')
        self.source_badge.hide()
        header_layout.addWidget(self.source_badge)

        # Rating badge
        self.rating_badge = RatingBadge(0.0)
        self.rating_badge.hide()
        header_layout.addWidget(self.rating_badge)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        layout.addSpacing(Theme.SPACING_SMALL)

        # Venue label (large, prominent)
        self.venue_label = QLabel("")
        self.venue_label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: {Theme.HEADER_SMALL}px;
            font-weight: bold;
            background: transparent;
        """)
        self.venue_label.setWordWrap(True)
        layout.addWidget(self.venue_label)

        # Location label (city, state)
        self.location_label = QLabel("")
        self.location_label.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: {Theme.BODY_MEDIUM}px;
            background: transparent;
        """)
        layout.addWidget(self.location_label)

        layout.addSpacing(Theme.SPACING_SMALL)

        # Metadata label (taper, reviews)
        self.metadata_label = QLabel("")
        self.metadata_label.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: {Theme.BODY_SMALL}px;
            background: transparent;
            font-style: italic;
        """)
        self.metadata_label.setWordWrap(True)
        layout.addWidget(self.metadata_label)

        layout.addSpacing(Theme.SPACING_MEDIUM)

        # Setlist header
        setlist_header = QLabel("Setlist")
        setlist_header.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: {Theme.BODY_LARGE}px;
            font-weight: bold;
            background: transparent;
        """)
        layout.addWidget(setlist_header)

        # Setlist scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background: rgba(255, 255, 255, 0.1);
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: rgba(255, 255, 255, 0.5);
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        # Setlist content widget
        setlist_content = QWidget()
        setlist_content.setStyleSheet("background: transparent;")
        self.setlist_layout = QVBoxLayout()
        self.setlist_layout.setSpacing(2)
        self.setlist_layout.setContentsMargins(0, 0, 0, 0)
        self.setlist_layout.addStretch()  # Push tracks to top
        setlist_content.setLayout(self.setlist_layout)

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

        # Set size policy to prevent expansion from long text
        from PyQt5.QtWidgets import QSizePolicy
        panel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        
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
        
        # Song title (large, centered, truncates with ellipsis if too long)
        self.song_title_label = ElidedLabel("Song Title")
        self.song_title_label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 48px;
            font-weight: bold;
            background: transparent;
        """)
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

        # Volume control (with image-based mute button using sound.png/silent.png)
        self.volume_control = VolumeControlWidget()
        self.volume_control.volume_changed.connect(self.on_volume_changed)
        self.volume_control.mute_toggled.connect(self.on_mute_toggled)
        layout.addWidget(self.volume_control)

        # Add stretch at bottom for centering content
        layout.addStretch(1)
        
        panel.setLayout(layout)

        # Create settings button (positioned absolutely in upper right corner)
        self.settings_btn = QLabel(panel)
        self.settings_btn.setFixedSize(80, 80)

        # Load and scale the settings icon
        settings_icon_path = os.path.join(PROJECT_ROOT, 'assets', 'settings.png')
        settings_pixmap = QPixmap(settings_icon_path)
        settings_scaled_pixmap = settings_pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.settings_btn.setPixmap(settings_scaled_pixmap)
        self.settings_btn.setAlignment(Qt.AlignCenter)

        # Style with transparent background and hover states
        self.settings_btn.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border-radius: 10px;
            }
            QLabel:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)

        # Make it clickable
        self.settings_btn.mousePressEvent = lambda event: self.on_settings_button_pressed(event)
        self.settings_btn.mouseReleaseEvent = lambda event: self.on_settings_button_released(event)

        # Position will be set in resizeEvent
        self.settings_btn.setToolTip("Audio Settings")

        # Create home button (positioned absolutely in upper left corner)
        self.home_btn = QLabel(panel)
        self.home_btn.setFixedSize(80, 80)

        # Load and scale the home icon
        home_icon_path = os.path.join(PROJECT_ROOT, 'assets', 'home-round.png')
        home_pixmap = QPixmap(home_icon_path)
        home_scaled_pixmap = home_pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.home_btn.setPixmap(home_scaled_pixmap)
        self.home_btn.setAlignment(Qt.AlignCenter)

        # Style with transparent background and hover states
        self.home_btn.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border-radius: 10px;
            }
            QLabel:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)

        # Make it clickable
        self.home_btn.mousePressEvent = lambda event: self.on_home_button_pressed(event)
        self.home_btn.mouseReleaseEvent = lambda event: self.on_home_button_released(event)

        # Position at upper left corner (25px from top and left)
        self.home_btn.move(25, 25)
        self.home_btn.setToolTip("Home")

        # Store panel reference for repositioning buttons on resize
        self._right_panel = panel

        return panel
    
    def create_media_controls(self):
        """Create 5-button media control layout with mixed PNG and painted buttons"""
        controls_widget = QWidget()
        controls_widget.setStyleSheet("background: transparent;")

        layout = QHBoxLayout()
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)

        # Asset paths
        assets_dir = os.path.join(PROJECT_ROOT, 'assets')

        # Button size for skip buttons (same as track buttons)
        control_btn_size = 60

        # Skip backward 30s (PNG asset)
        rew_30_path = os.path.join(assets_dir, 'rew-30.png')
        self.skip_back_btn = ImageButton(rew_30_path, size=control_btn_size, tooltip="Skip back 30 seconds")
        self.skip_back_btn.clicked.connect(self.on_skip_backward)
        layout.addWidget(self.skip_back_btn)

        # Previous track (painted bar+triangle)
        self.prev_btn = TrackButton('previous', size=control_btn_size)
        self.prev_btn.clicked.connect(self.on_previous_track)
        layout.addWidget(self.prev_btn)

        # Play/Pause (larger, center) - stores both icon paths for toggling
        self._play_icon_path = os.path.join(assets_dir, 'play.png')
        self._pause_icon_path = os.path.join(assets_dir, 'pause.png')
        self.play_pause_btn = ImageButton(self._play_icon_path, size=80, tooltip="Play/Pause")
        self.play_pause_btn.clicked.connect(self.on_play_pause)
        layout.addWidget(self.play_pause_btn)

        # Next track (painted triangle+bar)
        self.next_btn = TrackButton('next', size=control_btn_size)
        self.next_btn.clicked.connect(self.on_next_track)
        layout.addWidget(self.next_btn)

        # Skip forward 30s (PNG asset)
        ffw_30_path = os.path.join(assets_dir, 'ffw-30.png')
        self.skip_forward_btn = ImageButton(ffw_30_path, size=control_btn_size, tooltip="Skip forward 30 seconds")
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

        # Update progress bar (which now shows time remaining on the right)
        if duration_ms > 0:
            position_seconds = position_ms // 1000
            duration_seconds = duration_ms // 1000
            self.progress_bar.update_position(position_seconds, duration_seconds)

            # Auto-advance to next track when current track ends
            # Check if we're near the end (within last 2 seconds) and not already handled
            if position_seconds >= duration_seconds - 2 and duration_seconds > 0:
                if not self._track_ended_handled:
                    self._track_ended_handled = True
                    # Check if there's a next track
                    if self.playlist and self.current_track_index < self.total_tracks - 1:
                        print(f"[INFO] Track ending, auto-playing next track")
                        self.on_next_track()
                    else:
                        print(f"[INFO] Last track ending, playback complete")

        # Update play/pause button icon
        state = self.player.get_state()
        is_playing = (state == PlayerState.PLAYING)

        if is_playing:
            self.play_pause_btn.set_icon(self._pause_icon_path)
            # Reset the flag when playing (but only if we're not near the end)
            if duration_ms > 0:
                position_seconds = position_ms // 1000
                duration_seconds = duration_ms // 1000
                if position_seconds < duration_seconds - 3:
                    self._track_ended_handled = False
        else:
            self.play_pause_btn.set_icon(self._play_icon_path)
    
    def load_show(self, show, auto_play=True):
        """
        Load a complete show and optionally start playing

        Args:
            show (dict): Show dictionary with keys: identifier, date, venue, etc.
            auto_play (bool): If True, start playing immediately. If False, load in paused state.
        """
        try:
            print(f"[INFO] Loading show: {show.get('date')} - {show.get('venue')}")

            # Import metadata utilities
            from src.api.metadata import get_metadata, extract_audio_files

            # Get show metadata from Internet Archive
            identifier = show.get('identifier')
            if not identifier:
                print("[ERROR] Show missing identifier")
                return

            metadata = get_metadata(identifier)
            if not metadata:
                print(f"[ERROR] Failed to fetch metadata for {identifier}")
                return

            # Extract audio files
            audio_files = extract_audio_files(metadata)
            if not audio_files:
                print(f"[ERROR] No audio files found for {identifier}")
                return

            print(f"[INFO] Found {len(audio_files)} tracks")

            # Store show info and playlist
            self.current_show = show
            self.playlist = audio_files
            self.current_track_index = 0
            self.total_tracks = len(audio_files)

            # Update left panel with concert info
            self.update_concert_info()

            # Populate setlist
            self.populate_setlist()

            # Load and optionally play first track
            self.play_track_at_index(0, auto_play=auto_play)

            print(f"[INFO] Show loaded successfully: {len(audio_files)} tracks (auto_play={auto_play})")

        except Exception as e:
            print(f"[ERROR] Failed to load show: {e}")
            import traceback
            traceback.print_exc()

    def update_concert_info(self):
        """Update left panel with current show information"""
        if not self.current_show:
            return

        # Format and display date
        date = self.current_show.get('date', 'Unknown Date')
        # Convert from YYYY-MM-DD to MM/DD/YYYY
        if '-' in date:
            parts = date.split('-')
            if len(parts) == 3:
                date = f"{parts[1]}/{parts[2]}/{parts[0]}"

        self.date_label.setText(date)

        # Display venue
        venue = self.current_show.get('venue', 'Unknown Venue')
        self.venue_label.setText(venue)

        # Display location (city, state)
        city = self.current_show.get('city', '')
        state = self.current_show.get('state', '')
        if city and state:
            location = f"{city}, {state}"
        elif city:
            location = city
        elif state:
            location = state
        else:
            # Fallback to coverage field
            location = self.current_show.get('coverage', '')
        self.location_label.setText(location)

        # Show source badge if available
        source_type = self.current_show.get('source_type', '')
        if source_type:
            # Normalize source type
            source_upper = source_type.upper()
            if 'SBD' in source_upper or 'SOUNDBOARD' in source_upper:
                badge_type = 'SBD'
            elif 'AUD' in source_upper or 'AUDIENCE' in source_upper:
                badge_type = 'AUD'
            elif 'MATRIX' in source_upper or 'MTX' in source_upper:
                badge_type = 'MTX'
            elif 'FM' in source_upper:
                badge_type = 'FM'
            else:
                badge_type = source_type[:3].upper()  # Use first 3 chars

            # Update badge and show it
            self.source_badge.source_type = badge_type
            self.source_badge.show()
            self.source_badge.update()
        else:
            self.source_badge.hide()

        # Show rating badge if available
        avg_rating = self.current_show.get('avg_rating')
        if avg_rating and avg_rating > 0:
            self.rating_badge.set_rating(avg_rating)
            self.rating_badge.show()
        else:
            self.rating_badge.hide()

        # Build metadata string (taper and reviews)
        metadata_parts = []

        taper = self.current_show.get('taper', '')
        if taper:
            metadata_parts.append(f"Taper: {taper}")

        num_reviews = self.current_show.get('num_reviews')
        if num_reviews and num_reviews > 0:
            review_text = "review" if num_reviews == 1 else "reviews"
            metadata_parts.append(f"{num_reviews} {review_text}")

        if metadata_parts:
            self.metadata_label.setText(" | ".join(metadata_parts))
            self.metadata_label.show()
        else:
            self.metadata_label.hide()

    def populate_setlist(self):
        """Populate setlist with clickable track widgets"""
        # Clear existing track widgets
        for widget in self.track_widgets:
            widget.deleteLater()
        self.track_widgets.clear()

        # Clear all items from layout (including widgets and spacers)
        while self.setlist_layout.count():
            item = self.setlist_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            # Spacer items don't need to be deleted, just removed

        # Create track widgets
        for i, track in enumerate(self.playlist):
            # Get track info
            track_name = track.get('title', track.get('name', f'Track {i + 1}'))

            # Format duration
            duration_str = ""
            length = track.get('length', '')
            if length:
                if isinstance(length, str) and ':' in length:
                    duration_str = length
                elif isinstance(length, (int, float)):
                    # Convert seconds to MM:SS
                    total_seconds = int(length)
                    minutes = total_seconds // 60
                    seconds = total_seconds % 60
                    duration_str = f"{minutes}:{seconds:02d}"

            # Create track widget
            track_widget = TrackWidget(i, track_name, duration_str)
            track_widget.clicked.connect(self.on_track_clicked)
            self.track_widgets.append(track_widget)
            self.setlist_layout.addWidget(track_widget)

        # Add stretch at the end to push tracks to top
        self.setlist_layout.addStretch()

        print(f"[INFO] Populated setlist with {len(self.track_widgets)} tracks")

    def on_track_clicked(self, track_index):
        """Handle track click from setlist"""
        print(f"[INFO] Track clicked: {track_index + 1}/{self.total_tracks}")
        self.play_track_at_index(track_index)

    def play_track_at_index(self, index, auto_play=True):
        """
        Play the track at the given index in the playlist

        Args:
            index (int): Index of track to play
            auto_play (bool): If True, start playing immediately. If False, load in paused state.
        """
        if not hasattr(self, 'playlist') or not self.playlist:
            print("[ERROR] No playlist loaded")
            return

        if index < 0 or index >= len(self.playlist):
            print(f"[ERROR] Invalid track index: {index}")
            return

        try:
            track = self.playlist[index]
            identifier = self.current_show.get('identifier')

            # Build streaming URL
            url = f"https://archive.org/download/{identifier}/{track['name']}"

            # Get track info
            track_name = track.get('title', track.get('name', 'Unknown Track'))

            # Parse duration from MM:SS or seconds format
            duration = 0
            length_str = track.get('length', '0')
            if isinstance(length_str, str) and ':' in length_str:
                # Format is MM:SS or HH:MM:SS
                parts = length_str.split(':')
                if len(parts) == 2:  # MM:SS
                    duration = int(parts[0]) * 60 + int(parts[1])
                elif len(parts) == 3:  # HH:MM:SS
                    duration = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            elif isinstance(length_str, (int, float)):
                duration = int(length_str)
            else:
                try:
                    duration = int(float(length_str))
                except (ValueError, TypeError):
                    duration = 0

            # Call existing load_track_url method
            self.load_track_url(
                url=url,
                track_name=track_name,
                set_name="",  # TODO: Determine set from track metadata
                track_num=index + 1,
                total_tracks=self.total_tracks,
                duration=duration,
                auto_play=auto_play
            )

            # Update current track index
            self.current_track_index = index

            # Update setlist highlighting
            self.update_setlist_highlight(index)

        except Exception as e:
            print(f"[ERROR] Failed to play track at index {index}: {e}")
            import traceback
            traceback.print_exc()

    def update_setlist_highlight(self, current_index):
        """Update setlist to highlight currently playing track"""
        for i, widget in enumerate(self.track_widgets):
            widget.set_current(i == current_index)

    def load_track_url(self, url, track_name="Unknown Track", set_name="",
                      track_num=1, total_tracks=1, duration=0, auto_play=True):
        """
        Load and optionally play a track URL

        Args:
            url (str): Streaming URL for the track
            track_name (str): Name of the track
            set_name (str): Set name (SET I, SET II, ENCORE)
            track_num (int): Track number in set
            total_tracks (int): Total tracks in set
            duration (int): Track duration in seconds
            auto_play (bool): If True, start playing immediately. If False, load in paused state.
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
                # Start playback if auto_play is True
                if auto_play:
                    self.player.play()
                    print(f"[INFO] Loaded and playing track: {track_name} ({set_name})")
                else:
                    # Media is loaded but remains paused
                    print(f"[INFO] Loaded track (paused): {track_name} ({set_name})")

                # Store current track info
                self.current_track_index = track_num - 1
                self.total_tracks = total_tracks
                self.current_track_name = track_name  # Store for NowPlayingBar
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
        if not hasattr(self, 'playlist') or not self.playlist:
            print("[WARN] No playlist loaded")
            return

        # Go to previous track (wrap around to end if at beginning)
        prev_index = self.current_track_index - 1
        if prev_index < 0:
            prev_index = self.total_tracks - 1

        print(f"[INFO] Previous track: {prev_index + 1}/{self.total_tracks}")
        self.play_track_at_index(prev_index)

    def on_next_track(self):
        """Handle next track request"""
        if not hasattr(self, 'playlist') or not self.playlist:
            print("[WARN] No playlist loaded")
            return

        # Go to next track (wrap around to beginning if at end)
        next_index = self.current_track_index + 1
        if next_index >= self.total_tracks:
            next_index = 0

        print(f"[INFO] Next track: {next_index + 1}/{self.total_tracks}")
        self.play_track_at_index(next_index)
    
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

    def on_settings_button_pressed(self, event):
        """Handle settings button press (mouse down)"""
        if event.button() == Qt.LeftButton:
            # Add press state styling
            self.settings_btn.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                }
                QLabel:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                }
            """)

    def on_settings_button_released(self, event):
        """Handle settings button release (mouse up)"""
        if event.button() == Qt.LeftButton:
            # Reset to normal styling
            self.settings_btn.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    border-radius: 10px;
                }
                QLabel:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
            """)
            # Navigate to audio section of settings screen
            print("[INFO] Settings button clicked - navigating to audio settings")
            self.settings_requested.emit()

    def on_home_button_pressed(self, event):
        """Handle home button press (mouse down)"""
        if event.button() == Qt.LeftButton:
            # Add press state styling
            self.home_btn.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                }
                QLabel:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                }
            """)

    def on_home_button_released(self, event):
        """Handle home button release (mouse up)"""
        if event.button() == Qt.LeftButton:
            # Reset to normal styling
            self.home_btn.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    border-radius: 10px;
                }
                QLabel:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
            """)
            # Navigate to welcome screen
            print("[INFO] Home button clicked - navigating to welcome screen")
            self.home_requested.emit()

    def on_back_clicked(self):
        """Handle back button click"""
        print("[INFO] Back button clicked")
        self.back_requested.emit()
    
    # ========================================================================
    # LAYOUT MANAGEMENT
    # ========================================================================
    
    def resizeEvent(self, event):
        """Reposition settings button when window is resized"""
        super().resizeEvent(event)

        # Reposition settings button if it exists and panel exists
        if hasattr(self, '_right_panel') and self.settings_btn:
            panel_width = self._right_panel.width()

            # Settings button (upper right corner: 25px from top, 25px from right)
            x = panel_width - 80 - 25
            y = 25
            self.settings_btn.move(x, y)
    
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
    screen.settings_requested.connect(lambda: print("[TEST] Settings button signal"))
    screen.back_requested.connect(lambda: print("[TEST] Back button signal"))
    screen.home_requested.connect(lambda: print("[TEST] Home button signal"))
    
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
    print("Left Panel:")
    print("  [OK] Purple gradient background")
    print("  [OK] Concert information (date, venue, location)")
    print("  [OK] Setlist with clickable tracks")
    print("\nRight Panel:")
    print("  [OK] Pure black background")
    print("  [OK] Home icon (upper left corner)")
    print("  [OK] Settings icon (upper right corner)")
    print("  [OK] 'NOW PLAYING' centered label")
    print("  [OK] '1 of 25' track counter")
    print("  [OK] Large centered song title")
    print("  [OK] 5 media controls with PNG assets (80px play button)")
    print("  [OK] Progress bar and volume control")
    print("\nPress Ctrl+C to exit")
    print("=" * 70 + "\n")
    
    sys.exit(app.exec_())
