#!/usr/bin/env python3
"""
Main window for DeadStream application.
Integrates screen manager and navigation system.
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor

# Add project root to path
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from src.ui.screen_manager import ScreenManager
from src.ui.screens.welcome_screen import WelcomeScreen
from src.ui.screens.player_screen import PlayerScreen
from src.ui.screens.browse_screen import BrowseScreen
from src.ui.screens.settings_screen import SettingsScreen
from src.ui.screens.findashow_screen import FindAShowScreen
from src.ui.screens.randomshow_screen import RandomShowScreen
from src.ui.widgets.now_playing_bar import NowPlayingBar
from src.ui.transitions import TransitionType
from src.settings import get_settings


class MainWindow(QMainWindow):
    """
    Main application window with navigation system.
    Manages screen transitions and overall application state.
    """
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        print("[INFO] Initializing MainWindow")
        
        # Window setup
        self.setWindowTitle("DeadStream - Grateful Dead Concert Player")
        self.setup_dark_theme()
        self.setup_window_size()
        
        # Create screen manager
        self.screen_manager = ScreenManager()
        
        # Create screens
        self.create_screens()

        # Create container widget with screen manager and now playing bar
        self.create_container_with_bar()

        # Connect signals for navigation
        self.connect_navigation()

        # Initialize keyboard handler
        self._setup_keyboard_handler()

        # Show welcome screen on app launch (always start here)
        print("[INFO] Starting at welcome screen")
        # Use instant transition for initial screen (no animation on app launch)
        self.screen_manager.show_screen(ScreenManager.WELCOME_SCREEN, transition_type=TransitionType.INSTANT)

        print("[INFO] MainWindow initialization complete")
    
    def setup_dark_theme(self):
        """Apply dark theme to the application"""
        # Set dark palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(17, 24, 39))          # gray-900
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))   # white
        palette.setColor(QPalette.Base, QColor(31, 41, 55))            # gray-800
        palette.setColor(QPalette.AlternateBase, QColor(17, 24, 39))   # gray-900
        palette.setColor(QPalette.Text, QColor(255, 255, 255))         # white
        palette.setColor(QPalette.Button, QColor(55, 65, 81))          # gray-700
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))   # white
        
        self.setPalette(palette)
        
        # Apply stylesheet for additional styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #111827;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
            QLabel {
                color: white;
            }
        """)
        
        print("[INFO] Dark theme applied")
    
    def setup_window_size(self):
        """Set window size based on screen"""
        screen = QApplication.primaryScreen().geometry()

        # Development mode: windowed at 1280x720
        window_width = 1280
        window_height = 720

        # Ensure it fits on screen
        if screen.width() < window_width + 100:
            window_width = screen.width() - 100
        if screen.height() < window_height + 100:
            window_height = screen.height() - 100

        # Set fixed size for development (prevents resizing issues)
        self.setFixedSize(window_width, window_height)

        # Position in center of screen
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        self.move(x, y)

        print(f"[INFO] Window size set to {window_width}x{window_height}")

    def _toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        if self.isFullScreen():
            self.showNormal()
            # Return to fixed size for development
            self.setFixedSize(1280, 720)
            # Re-center window
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - 1280) // 2
            y = (screen.height() - 720) // 2
            self.move(x, y)
            print("[INFO] Exited fullscreen mode")
        else:
            # Remove size constraints for fullscreen
            self.setMinimumSize(0, 0)
            self.setMaximumSize(16777215, 16777215)
            self.showFullScreen()
            print("[INFO] Entered fullscreen mode")

    def create_screens(self):
        """Create and add all screens to the screen manager"""
        try:
            # Create screen instances
            self.welcome_screen = WelcomeScreen()
            self.player_screen = PlayerScreen()
            self.browse_screen = BrowseScreen()
            self.settings_screen = SettingsScreen()
            self.findashow_screen = FindAShowScreen()
            self.randomshow_screen = RandomShowScreen()

            # Add to screen manager
            self.screen_manager.add_screen(
                ScreenManager.WELCOME_SCREEN,
                self.welcome_screen
            )
            self.screen_manager.add_screen(
                ScreenManager.PLAYER_SCREEN,
                self.player_screen
            )
            self.screen_manager.add_screen(
                ScreenManager.BROWSE_SCREEN,
                self.browse_screen
            )
            self.screen_manager.add_screen(
                ScreenManager.SETTINGS_SCREEN,
                self.settings_screen
            )
            self.screen_manager.add_screen(
                ScreenManager.FINDASHOW_SCREEN,
                self.findashow_screen
            )
            self.screen_manager.add_screen(
                ScreenManager.RANDOMSHOW_SCREEN,
                self.randomshow_screen
            )

            print("[INFO] All screens created and added")

        except Exception as e:
            print(f"[ERROR] Failed to create screens: {e}")

    def create_container_with_bar(self):
        """
        Create container widget with ScreenManager and NowPlayingBar.

        Layout structure:
            Container (QWidget)
            ├── ScreenManager (expand to fill)
            └── NowPlayingBar (fixed 80px height)

        The container becomes the central widget instead of ScreenManager directly.
        """
        # Create container widget
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Add screen manager (expand to fill)
        container_layout.addWidget(self.screen_manager, stretch=1)

        # Create now playing bar
        self.now_playing_bar = NowPlayingBar()
        self.now_playing_bar.setVisible(False)  # Initially hidden

        # Connect bar signals
        self.now_playing_bar.player_requested.connect(self.show_player)
        self.now_playing_bar.play_pause_clicked.connect(self._handle_bar_play_pause)
        self.now_playing_bar.next_clicked.connect(self._handle_bar_next)
        self.now_playing_bar.previous_clicked.connect(self._handle_bar_previous)

        # Add now playing bar (fixed height)
        container_layout.addWidget(self.now_playing_bar, stretch=0)

        # Set container as central widget
        self.setCentralWidget(container)

        # Connect player to bar (if player_screen has player)
        if hasattr(self.player_screen, 'player') and self.player_screen.player:
            self.now_playing_bar.set_player(self.player_screen.player)
            print("[INFO] NowPlayingBar connected to ResilientPlayer")
        else:
            print("[WARN] player_screen.player not available yet, will connect later")

        # Set up track monitoring timer (checks for track changes every 1 second)
        self._last_track_name = None
        self._track_monitor_timer = QTimer()
        self._track_monitor_timer.timeout.connect(self._check_track_change)
        self._track_monitor_timer.start(1000)  # Check every 1 second

        print("[INFO] Container with NowPlayingBar created")

    def connect_navigation(self):
        """Connect navigation signals from screens to screen manager"""
        try:
            # Welcome screen navigation
            self.welcome_screen.browse_requested.connect(self.show_findashow)
            self.welcome_screen.random_show_requested.connect(self.on_random_show_requested)
            self.welcome_screen.settings_requested.connect(self.show_settings)

            # Player screen navigation
            self.player_screen.settings_requested.connect(self.show_settings_audio)
            self.player_screen.back_requested.connect(self.show_findashow)
            self.player_screen.home_requested.connect(self.show_welcome)

            # Browse screen navigation
            self.browse_screen.player_requested.connect(self.show_player)
            self.browse_screen.settings_requested.connect(self.show_settings)
            self.browse_screen.show_selected.connect(self.on_show_selected)

            # Settings screen navigation
            self.settings_screen.browse_requested.connect(self.show_browse)
            self.settings_screen.back_clicked.connect(self.show_welcome)

            # Find a Show screen navigation
            self.findashow_screen.date_selected.connect(self.on_date_selected)
            self.findashow_screen.home_requested.connect(self.show_welcome)
            self.findashow_screen.settings_requested.connect(self.show_settings)

            # Random Show screen navigation
            self.randomshow_screen.show_selected.connect(self.on_show_selected)
            self.randomshow_screen.home_requested.connect(self.show_welcome)
            self.randomshow_screen.settings_requested.connect(self.show_settings)

            # Screen manager change signal
            self.screen_manager.screen_changed.connect(self.on_screen_changed)

            print("[INFO] Navigation signals connected")

        except Exception as e:
            print(f"[ERROR] Failed to connect navigation: {e}")
    
    def _setup_keyboard_handler(self):
        """Set up keyboard shortcuts"""
        from src.ui.keyboard_handler import KeyboardHandler

        self.keyboard_handler = KeyboardHandler()

        # Connect navigation signals
        self.keyboard_handler.navigate_up.connect(self._handle_up)
        self.keyboard_handler.navigate_down.connect(self._handle_down)
        self.keyboard_handler.navigate_left.connect(self._handle_left)
        self.keyboard_handler.navigate_right.connect(self._handle_right)
        self.keyboard_handler.page_up.connect(self._handle_page_up)
        self.keyboard_handler.page_down.connect(self._handle_page_down)

        # Connect playback signals
        self.keyboard_handler.play_pause.connect(self._handle_play_pause)
        self.keyboard_handler.next_track.connect(self._handle_next)
        self.keyboard_handler.previous_track.connect(self._handle_previous)
        self.keyboard_handler.volume_up.connect(self._handle_volume_up)
        self.keyboard_handler.volume_down.connect(self._handle_volume_down)

        # Connect UI action signals
        self.keyboard_handler.back.connect(self._handle_back)
        self.keyboard_handler.select.connect(self._handle_select)
        self.keyboard_handler.menu.connect(self._handle_menu)
        self.keyboard_handler.quit_app.connect(self.close)

        print("[INFO] Keyboard handler configured")

    def show_welcome(self):
        """Navigate to welcome screen with fade transition"""
        self.screen_manager.show_screen(ScreenManager.WELCOME_SCREEN, transition_type=TransitionType.FADE)

    def show_player(self):
        """Navigate to player screen with fade transition"""
        self.screen_manager.show_screen(ScreenManager.PLAYER_SCREEN, transition_type=TransitionType.FADE)

    def show_browse(self):
        """Navigate to browse screen with fade transition"""
        self.screen_manager.show_screen(ScreenManager.BROWSE_SCREEN, transition_type=TransitionType.FADE)

    def show_settings(self):
        """Navigate to settings screen with fade transition"""
        self.screen_manager.show_screen(ScreenManager.SETTINGS_SCREEN, transition_type=TransitionType.FADE)

    def show_settings_audio(self):
        """Navigate to settings screen and show audio category"""
        self.screen_manager.show_screen(ScreenManager.SETTINGS_SCREEN, transition_type=TransitionType.FADE)
        # Switch to audio category after transition
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(350, lambda: self.settings_screen.show_category("audio"))

    def show_findashow(self):
        """Navigate to find a show screen with fade transition"""
        self.screen_manager.show_screen(ScreenManager.FINDASHOW_SCREEN, transition_type=TransitionType.FADE)

    def show_randomshow(self):
        """Navigate to random show screen with fade transition"""
        self.screen_manager.show_screen(ScreenManager.RANDOMSHOW_SCREEN, transition_type=TransitionType.FADE)

    def on_random_show_requested(self):
        """Handle random show request from welcome screen"""
        print("[INFO] Random show requested - loading random show into player")

        # Get a random show from the database
        from src.database.queries import get_random_show
        random_show = get_random_show()

        if not random_show:
            print("[WARNING] No random show found in database")
            return

        print(f"[INFO] Random show selected: {random_show.get('date', 'Unknown')} - {random_show.get('venue', 'Unknown')}")

        # Load the show into the player screen (without auto-play)
        self.player_screen.load_show(random_show, auto_play=False)

        # Update now playing bar with track info and visibility (audio now loaded)
        self.update_now_playing_bar_track_info()
        self.update_now_playing_bar_visibility()

        # Navigate to player screen
        self.show_player()

    def on_show_selected(self, show):
        """Handle show selection from browse screen"""
        print(f"[INFO] Loading show: {show.get('date', 'Unknown')} - {show.get('venue', 'Unknown')}")

        # Load the show into the player screen
        self.player_screen.load_show(show)

        # Update now playing bar with track info and visibility (audio now loaded)
        self.update_now_playing_bar_track_info()
        self.update_now_playing_bar_visibility()

        # Navigate to player screen
        self.show_player()

    def on_date_selected(self, date_str):
        """Handle date selection from find a show screen"""
        print(f"[INFO] Date selected from find a show screen: {date_str}")

        # Query database for shows on this date
        from src.database.queries import get_show_by_date
        shows = get_show_by_date(date_str)

        if not shows:
            print(f"[WARNING] No shows found for date: {date_str}")
            # Could show a message to the user here
            return

        if len(shows) == 1:
            # Single show found - load it directly
            print(f"[INFO] Found 1 show for {date_str}, loading it")
            self.on_show_selected(shows[0])
        else:
            # Multiple shows found - for now, load the first one
            # TODO: In the future, could show a selection dialog
            print(f"[INFO] Found {len(shows)} shows for {date_str}, loading first one")
            self.on_show_selected(shows[0])

    def on_screen_changed(self, screen_name):
        """
        Handle screen change events

        Args:
            screen_name: Name of the new screen
        """
        print(f"[INFO] Screen changed to: {screen_name}")

        # Update now playing bar visibility
        self.update_now_playing_bar_visibility()

        # Save current screen to settings for restoration on next launch
        settings = get_settings()
        screen_value_map = {
            ScreenManager.PLAYER_SCREEN: 'player',
            ScreenManager.BROWSE_SCREEN: 'browse',
            ScreenManager.SETTINGS_SCREEN: 'settings'
        }
        screen_value = screen_value_map.get(screen_name, 'browse')
        settings.set('app', 'last_screen', screen_value)

        # Update window title
        titles = {
            ScreenManager.WELCOME_SCREEN: "DeadStream - Grateful Dead Concert Player",
            ScreenManager.PLAYER_SCREEN: "DeadStream - Now Playing",
            ScreenManager.BROWSE_SCREEN: "DeadStream - Browse Shows",
            ScreenManager.SETTINGS_SCREEN: "DeadStream - Settings",
            ScreenManager.FINDASHOW_SCREEN: "DeadStream - Find a Show"
        }

        if screen_name in titles:
            self.setWindowTitle(titles[screen_name])
    
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        # Try keyboard handler first
        if not self.keyboard_handler.handle_key_press(event):
            # If keyboard handler didn't handle it, use legacy shortcuts
            # ESC to exit fullscreen
            if event.key() == Qt.Key_Escape:
                if self.isFullScreen():
                    self.showNormal()
                    print("[INFO] Exited fullscreen")
            
            # F11 to toggle fullscreen
            elif event.key() == Qt.Key_F11:
                if self.isFullScreen():
                    self.showNormal()
                    print("[INFO] Exited fullscreen")
                else:
                    self.showFullScreen()
                    print("[INFO] Entered fullscreen")
            
            # Pass event to parent
            else:
                super().keyPressEvent(event)
    
    # Navigation handlers
    def _handle_up(self):
        """Handle up key"""
        print("[INFO] Keyboard: Up pressed")
        # Forward to current view if it implements navigation
        current_widget = self.screen_manager.currentWidget()
        if hasattr(current_widget, 'handle_navigate_up'):
            current_widget.handle_navigate_up()
    
    def _handle_down(self):
        """Handle down key"""
        print("[INFO] Keyboard: Down pressed")
        current_widget = self.screen_manager.currentWidget()
        if hasattr(current_widget, 'handle_navigate_down'):
            current_widget.handle_navigate_down()
    
    def _handle_left(self):
        """Handle left key"""
        print("[INFO] Keyboard: Left pressed")
        current_widget = self.screen_manager.currentWidget()
        if hasattr(current_widget, 'handle_navigate_left'):
            current_widget.handle_navigate_left()
    
    def _handle_right(self):
        """Handle right key"""
        print("[INFO] Keyboard: Right pressed")
        current_widget = self.screen_manager.currentWidget()
        if hasattr(current_widget, 'handle_navigate_right'):
            current_widget.handle_navigate_right()
    
    def _handle_page_up(self):
        """Handle page up key"""
        print("[INFO] Keyboard: Page Up pressed")
        current_widget = self.screen_manager.currentWidget()
        if hasattr(current_widget, 'handle_page_up'):
            current_widget.handle_page_up()
    
    def _handle_page_down(self):
        """Handle page down key"""
        print("[INFO] Keyboard: Page Down pressed")
        current_widget = self.screen_manager.currentWidget()
        if hasattr(current_widget, 'handle_page_down'):
            current_widget.handle_page_down()
    
    # Playback handlers
    def _handle_play_pause(self):
        """Handle play/pause key"""
        print("[INFO] Keyboard: Play/Pause pressed")
        # This will be connected to audio player in later phase
    
    def _handle_next(self):
        """Handle next track key"""
        print("[INFO] Keyboard: Next track pressed")
        # This will be connected to audio player in later phase
    
    def _handle_previous(self):
        """Handle previous track key"""
        print("[INFO] Keyboard: Previous track pressed")
        # This will be connected to audio player in later phase
    
    def _handle_volume_up(self):
        """Handle volume up key"""
        print("[INFO] Keyboard: Volume up pressed")
        # This will be connected to audio player in later phase
    
    def _handle_volume_down(self):
        """Handle volume down key"""
        print("[INFO] Keyboard: Volume down pressed")
        # This will be connected to audio player in later phase
    
    # UI action handlers
    def _handle_back(self):
        """Handle back/escape key"""
        print("[INFO] Keyboard: Back pressed")
        # Go back in screen history if available
        if hasattr(self.screen_manager, 'go_back'):
            self.screen_manager.go_back()
        else:
            # Default behavior: go to player screen
            self.show_player()
    
    def _handle_select(self):
        """Handle select/enter key"""
        print("[INFO] Keyboard: Select pressed")
        current_widget = self.screen_manager.currentWidget()
        if hasattr(current_widget, 'handle_select'):
            current_widget.handle_select()
    
    def _handle_menu(self):
        """Handle menu toggle key"""
        print("[INFO] Keyboard: Menu pressed")
        # Toggle between player and settings
        current_screen = self.screen_manager.current_screen_name
        if current_screen == ScreenManager.PLAYER_SCREEN:
            self.show_settings()
        else:
            self.show_player()

    # Now Playing Bar methods

    def update_now_playing_bar_visibility(self):
        """
        Show bar only when audio loaded and not on player screen.

        Visibility logic:
            - Show: has_audio AND current_screen != player
            - Hide: no_audio OR current_screen == player
        """
        current_screen = self.screen_manager.current_screen_name

        # Check if player has media loaded (current_url is set when media is loaded)
        has_audio = False
        if hasattr(self.player_screen, 'player') and self.player_screen.player:
            has_audio = self.player_screen.player.current_url is not None

        # Show bar only if audio loaded AND not on player screen
        show_bar = has_audio and current_screen != ScreenManager.PLAYER_SCREEN

        self.now_playing_bar.setVisible(show_bar)

        if show_bar:
            print(f"[INFO] NowPlayingBar visible (audio loaded, on {current_screen})")
        else:
            print(f"[INFO] NowPlayingBar hidden (audio={has_audio}, screen={current_screen})")

    def update_now_playing_bar_track_info(self):
        """
        Update the now playing bar with current track information.

        Reads track info from player_screen and updates the bar display.
        Call this whenever a new track is loaded.
        """
        if not hasattr(self.player_screen, 'current_show') or not self.player_screen.current_show:
            print("[DEBUG] NowPlayingBar: No show loaded")
            return

        if not hasattr(self.player_screen, 'current_track_name'):
            print("[DEBUG] NowPlayingBar: No track name available")
            return

        # Get track info from player_screen
        track_name = self.player_screen.current_track_name
        show_date = self.player_screen.current_show.get('date', 'Unknown Date')
        show_venue = self.player_screen.current_show.get('venue', 'Unknown Venue')

        # Update the bar
        self.now_playing_bar.load_track_info(track_name, show_date, show_venue)
        print(f"[INFO] NowPlayingBar updated: {track_name} - {show_date}")

    def _check_track_change(self):
        """
        Monitor for track changes and update now playing bar accordingly.

        Called by timer every 1 second to detect track changes from:
        - Next/Previous buttons on player screen
        - Auto-advance when track ends
        - Any other track change mechanism
        """
        if not hasattr(self.player_screen, 'current_track_name'):
            return

        current_track = self.player_screen.current_track_name

        # Check if track has changed
        if current_track != self._last_track_name:
            self._last_track_name = current_track
            # Update bar with new track info
            self.update_now_playing_bar_track_info()

    def _handle_bar_play_pause(self):
        """Handle play/pause button click from now playing bar"""
        print("[INFO] NowPlayingBar: Play/pause clicked")
        if hasattr(self.player_screen, 'on_play_pause'):
            self.player_screen.on_play_pause()
        else:
            print("[WARN] player_screen.on_play_pause not available")

    def _handle_bar_next(self):
        """Handle next button click from now playing bar"""
        print("[INFO] NowPlayingBar: Next clicked")
        if hasattr(self.player_screen, 'on_next_track'):
            self.player_screen.on_next_track()
            # Update bar after track changes (give it a moment to load)
            QTimer.singleShot(500, self.update_now_playing_bar_track_info)
        else:
            print("[WARN] player_screen.on_next_track not available")

    def _handle_bar_previous(self):
        """Handle previous button click from now playing bar"""
        print("[INFO] NowPlayingBar: Previous clicked")
        if hasattr(self.player_screen, 'on_previous_track'):
            self.player_screen.on_previous_track()
            # Update bar after track changes (give it a moment to load)
            QTimer.singleShot(500, self.update_now_playing_bar_track_info)
        else:
            print("[WARN] player_screen.on_previous_track not available")


def main():
    """Main entry point for the application"""
    try:
        app = QApplication(sys.argv)
        
        print("[INFO] Starting DeadStream application")
        
        window = MainWindow()
        window.show()
        
        print("[INFO] Application window displayed")
        print("[INFO] Use buttons to navigate between screens")
        print("[INFO] Press F11 to toggle fullscreen, ESC to exit fullscreen")
        print("\n" + "="*60)
        print("KEYBOARD SHORTCUTS:")
        print("="*60)
        print("Navigation:")
        print("  Arrow Keys    - Navigate UI")
        print("  Page Up/Down  - Scroll lists")
        print("  Enter         - Select item")
        print("  Escape        - Go back")
        print("  M             - Toggle menu")
        print("\nPlayback:")
        print("  Space         - Play/Pause")
        print("  N             - Next track")
        print("  P             - Previous track")
        print("  +/-           - Volume up/down")
        print("\nSystem:")
        print("  Q             - Quit")
        print("  F11           - Toggle fullscreen")
        print("="*60 + "\n")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"[ERROR] Application failed to start: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
