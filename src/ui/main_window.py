#!/usr/bin/env python3
"""
Main window for DeadStream application.
Integrates screen manager and navigation system.
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

# Add project root to path
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from src.ui.screen_manager import ScreenManager
from src.ui.screens.player_screen import PlayerScreen
from src.ui.screens.browse_screen import BrowseScreen
from src.ui.screens.settings_screen import SettingsScreen
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
        
        # Set screen manager as central widget
        self.setCentralWidget(self.screen_manager)
        
        # Connect signals for navigation
        self.connect_navigation()
        
        # Initialize keyboard handler
        self._setup_keyboard_handler()

        # Restore last screen from settings (default to browse)
        settings = get_settings()
        last_screen = settings.get('app', 'last_screen', 'browse')
        print(f"[INFO] Restoring last screen from settings: {last_screen}")

        # Map setting value to screen constant
        screen_map = {
            'player': ScreenManager.PLAYER_SCREEN,
            'browse': ScreenManager.BROWSE_SCREEN,
            'settings': ScreenManager.SETTINGS_SCREEN
        }
        initial_screen = screen_map.get(last_screen, ScreenManager.BROWSE_SCREEN)
        self.screen_manager.show_screen(initial_screen)

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
    
    def create_screens(self):
        """Create and add all screens to the screen manager"""
        try:
            # Create screen instances
            self.player_screen = PlayerScreen()
            self.browse_screen = BrowseScreen()
            self.settings_screen = SettingsScreen()
            
            # Add to screen manager
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
            
            print("[INFO] All screens created and added")
            
        except Exception as e:
            print(f"[ERROR] Failed to create screens: {e}")
    
    def connect_navigation(self):
        """Connect navigation signals from screens to screen manager"""
        try:
            # Player screen navigation
            self.player_screen.browse_requested.connect(self.show_browse)
            
            # Browse screen navigation
            self.browse_screen.player_requested.connect(self.show_player)
            self.browse_screen.settings_requested.connect(self.show_settings)
            self.browse_screen.show_selected.connect(self.on_show_selected)
            
            # Settings screen navigation
            self.settings_screen.browse_requested.connect(self.show_browse)
            self.settings_screen.back_clicked.connect(self.show_browse)
            
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
    
    def show_player(self):
        """Navigate to player screen"""
        self.screen_manager.show_screen(ScreenManager.PLAYER_SCREEN)

    def show_browse(self):
        """Navigate to browse screen"""
        self.screen_manager.show_screen(ScreenManager.BROWSE_SCREEN)

    def show_settings(self):
        """Navigate to settings screen"""
        self.screen_manager.show_screen(ScreenManager.SETTINGS_SCREEN)

    def on_show_selected(self, show):
        """Handle show selection from browse screen"""
        print(f"[INFO] Loading show: {show.get('date', 'Unknown')} - {show.get('venue', 'Unknown')}")

        # Load the show into the player screen
        self.player_screen.load_show(show)

        # Navigate to player screen
        self.show_player()
    
    def on_screen_changed(self, screen_name):
        """
        Handle screen change events

        Args:
            screen_name: Name of the new screen
        """
        print(f"[INFO] Screen changed to: {screen_name}")

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
            ScreenManager.PLAYER_SCREEN: "DeadStream - Now Playing",
            ScreenManager.BROWSE_SCREEN: "DeadStream - Browse Shows",
            ScreenManager.SETTINGS_SCREEN: "DeadStream - Settings"
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
