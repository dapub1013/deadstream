"""
NowPlayingBar - Minimal playback control bar for browse/settings screens.

Shows track info and essential controls (prev, play/pause, next).
Appears at bottom of screen when audio is loaded and not on player screen.

Phase 10F - Task 10F.1: Create NowPlayingBar Widget (COMPLETE)
Phase 10F - Task 10F.2: Integrate with ResilientPlayer (COMPLETE)
"""

import sys
import os

# Path manipulation for imports (file in src/ui/widgets/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QCursor, QIcon

from src.ui.styles.theme import Theme
from src.ui.components.icon_button import IconButton


class NowPlayingBar(QWidget):
    """
    Minimal playback control bar for browse/settings screens.
    Shows track info and essential controls.

    Design Specification:
        - Height: 80px total (60px buttons + padding)
        - Position: Bottom of screen, full width (1280px)
        - Background: Pure black (matches player screen right panel)
        - Layout: [Track Info - expanding] [Prev] [Play/Pause] [Next]
        - Visibility: Show when audio loaded AND not on player screen

    Signals:
        player_requested: User clicked bar to view player
        play_pause_clicked: User clicked play/pause button
        next_clicked: User clicked next button
        previous_clicked: User clicked previous button

    Usage:
        bar = NowPlayingBar()
        bar.set_player(resilient_player)
        bar.player_requested.connect(show_player_screen)
        bar.load_track_info("Scarlet Begonias", "1977-05-08", "Barton Hall")
    """

    # Signals
    player_requested = pyqtSignal()       # User clicked bar to view player
    play_pause_clicked = pyqtSignal()     # User clicked play/pause
    next_clicked = pyqtSignal()           # User clicked next
    previous_clicked = pyqtSignal()       # User clicked previous
    close_clicked = pyqtSignal()          # User clicked close to unload show

    def __init__(self, parent=None):
        """Initialize the now playing bar"""
        super().__init__(parent)

        # Player reference (set later)
        self.player = None

        # Timer for UI updates (200ms interval, same as player_screen.py)
        self.update_timer = None

        # Track info cache
        self._current_track_name = "No track loaded"
        self._current_show_date = ""
        self._current_show_venue = ""

        # Fixed height from spec
        self.setFixedHeight(80)

        # Set up UI
        self.init_ui()

        print("[INFO] NowPlayingBar widget created")

    def init_ui(self):
        """Set up the UI layout and styling"""
        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(
            10,  # left (10px margin-left for close button)
            10,  # top (10px margin-top for close button)
            Theme.SPACING_MEDIUM,  # right
            Theme.SPACING_SMALL    # bottom
        )
        main_layout.setSpacing(0)  # We'll handle spacing manually

        # Close button (20x20px) - upper-left with specific margins
        self.close_button = self._create_close_button()
        main_layout.addWidget(self.close_button, stretch=0, alignment=Qt.AlignTop)

        # Spacer for 20px margin-right of close button
        main_layout.addSpacing(20)

        # Left section: Track info (expanding)
        self.track_info_widget = self._create_track_info_section()
        main_layout.addWidget(self.track_info_widget, stretch=1)

        # Spacer between track info and controls
        main_layout.addSpacing(Theme.SPACING_MEDIUM)

        # Right section: Playback controls (fixed width)
        controls_layout = self._create_controls_section()
        main_layout.addLayout(controls_layout, stretch=0)

        # Apply black background with top border
        self.setStyleSheet(f"""
            NowPlayingBar {{
                background-color: {Theme.BG_PANEL_BLACK};
                border-top: 1px solid {Theme.BORDER_PANEL};
            }}
        """)

        # Make entire widget clickable (will emit player_requested)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def _create_track_info_section(self):
        """
        Create the track info display section.

        Returns:
            QWidget: Container with track title and show info labels
        """
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Theme.SPACING_TINY)

        # Track title label (large, bold, white)
        self.track_title_label = QLabel("No track loaded")
        font_title = QFont(Theme.FONT_FAMILY)
        font_title.setPixelSize(Theme.BODY_LARGE)
        font_title.setBold(True)
        self.track_title_label.setFont(font_title)
        self.track_title_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        layout.addWidget(self.track_title_label)

        # Show info label (smaller, gray)
        self.show_info_label = QLabel("")
        font_info = QFont(Theme.FONT_FAMILY)
        font_info.setPixelSize(Theme.BODY_SMALL)
        self.show_info_label.setFont(font_info)
        self.show_info_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        layout.addWidget(self.show_info_label)

        layout.addStretch()

        return container

    def _create_close_button(self):
        """
        Create the close button (20x20px) using close.png asset.

        Positioned in upper-left with:
        - 10px margin-top (handled by layout alignment)
        - 10px margin-left (handled by layout margins)
        - 20px margin-right (handled by content margins)

        Returns:
            QPushButton: Close button that emits close_clicked when pressed
        """
        close_btn = QPushButton()
        close_btn.setFixedSize(20, 20)

        # Load the close.png icon from assets
        icon_path = os.path.join(PROJECT_ROOT, 'assets', 'close.png')
        icon = QIcon(icon_path)
        close_btn.setIcon(icon)
        close_btn.setIconSize(QSize(20, 20))

        # Style: transparent background, no border
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
        """)

        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self._on_close_clicked)

        return close_btn

    def _create_controls_section(self):
        """
        Create the playback controls section.

        Returns:
            QHBoxLayout: Layout containing prev, play/pause, next buttons
        """
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(Theme.BUTTON_SPACING)
        controls_layout.setContentsMargins(0, 0, 0, 0)

        # Previous button (60x60px, solid variant)
        self.prev_button = IconButton('back', variant='solid')
        self.prev_button.clicked.connect(self._on_previous_clicked)
        controls_layout.addWidget(self.prev_button)

        # Play/Pause button (60x60px, accent variant for visibility)
        self.play_pause_button = IconButton('play', variant='accent')
        self.play_pause_button.clicked.connect(self._on_play_pause_clicked)
        controls_layout.addWidget(self.play_pause_button)

        # Next button (60x60px, solid variant)
        self.next_button = IconButton('forward', variant='solid')
        self.next_button.clicked.connect(self._on_next_clicked)
        controls_layout.addWidget(self.next_button)

        return controls_layout

    def set_player(self, player):
        """
        Connect to ResilientPlayer instance.

        This method:
        1. Stores the player reference
        2. Creates a QTimer for periodic UI updates (200ms interval)
        3. Connects timer to update_from_player() method

        Args:
            player: ResilientPlayer instance

        Usage:
            bar = NowPlayingBar()
            bar.set_player(resilient_player)
        """
        self.player = player

        # Create UI update timer (200ms = 5 updates per second, same as player_screen.py)
        if self.update_timer is None:
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.update_from_player)
            self.update_timer.start(200)  # 200ms interval
            print("[INFO] NowPlayingBar: Timer-based updates started (200ms)")
        else:
            print("[WARN] NowPlayingBar: Update timer already exists")

        print("[INFO] NowPlayingBar: Connected to ResilientPlayer")

    def update_from_player(self):
        """
        Update UI from current player state - called by timer every 200ms.

        This method:
        1. Reads player state (is_playing, is_paused, etc.)
        2. Updates play/pause button icon based on state
        3. Updates track info if needed (from cache)

        Note: Track info is set separately via load_track_info().
        This method only updates the play/pause icon state.
        """
        if self.player is None:
            return

        # Update play/pause button icon based on player state
        from src.audio.resilient_player import PlayerState

        state = self.player.get_state()
        is_playing = (state == PlayerState.PLAYING)

        # Update button icon
        if is_playing:
            self.play_pause_button.set_icon('pause')
        else:
            self.play_pause_button.set_icon('play')

    def load_track_info(self, track_name, show_date, show_venue):
        """
        Set track and show information.

        Args:
            track_name (str): Name of the current track
            show_date (str): Date of the show (e.g., "1977-05-08")
            show_venue (str): Venue name (e.g., "Barton Hall")
        """
        # Cache track info
        self._current_track_name = track_name
        self._current_show_date = show_date
        self._current_show_venue = show_venue

        # Update labels
        self.track_title_label.setText(track_name)
        self.show_info_label.setText(f"{show_date} - {show_venue}")

        print(f"[INFO] NowPlayingBar: Loaded track info - {track_name} ({show_date})")

    def mousePressEvent(self, event):
        """Handle mouse press on the bar itself (not on buttons)"""
        # Check if click was on a control button (don't navigate if so)
        click_pos = event.pos()

        # If click was on track info area (left side), navigate to player
        if click_pos.x() < self.track_info_widget.geometry().right():
            print("[INFO] NowPlayingBar: Clicked on track info, navigating to player")
            self.player_requested.emit()

        super().mousePressEvent(event)

    # Internal signal handlers

    def _on_play_pause_clicked(self):
        """
        Handle play/pause button click (internal).

        Emits play_pause_clicked signal which should be connected
        to player controls by the parent (e.g., MainWindow).

        Example connection in MainWindow:
            bar.play_pause_clicked.connect(self.toggle_playback)
        """
        print("[INFO] NowPlayingBar: Play/pause button clicked")
        self.play_pause_clicked.emit()

    def _on_next_clicked(self):
        """
        Handle next button click (internal).

        Emits next_clicked signal which should be connected
        to player controls by the parent (e.g., MainWindow).

        Example connection in MainWindow:
            bar.next_clicked.connect(self.player_screen.on_next_track)
        """
        print("[INFO] NowPlayingBar: Next button clicked")
        self.next_clicked.emit()

    def _on_previous_clicked(self):
        """
        Handle previous button click (internal).

        Emits previous_clicked signal which should be connected
        to player controls by the parent (e.g., MainWindow).

        Example connection in MainWindow:
            bar.previous_clicked.connect(self.player_screen.on_previous_track)
        """
        print("[INFO] NowPlayingBar: Previous button clicked")
        self.previous_clicked.emit()

    def _on_close_clicked(self):
        """
        Handle close button click (internal).

        Emits close_clicked signal which should be connected
        to unload the current show by the parent (e.g., MainWindow).

        Example connection in MainWindow:
            bar.close_clicked.connect(self.unload_show)
        """
        print("[INFO] NowPlayingBar: Close button clicked - unloading show")
        self.close_clicked.emit()
