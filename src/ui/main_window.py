#!/usr/bin/env python3
"""
DeadStream Main Window
Main application window with screen management
"""

import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QLabel, QPushButton
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette, QColor

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


class MainWindow(QMainWindow):
    """
    Main application window for DeadStream
    Manages screen transitions between Player, Browse, and Settings
    """
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.setWindowTitle("DeadStream - Grateful Dead Concert Player")
        self.setup_window_size()
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        main_layout.setSpacing(0)  # No spacing
        
        # Create stacked widget for screen management
        self.screen_stack = QStackedWidget()
        main_layout.addWidget(self.screen_stack)
        
        # Create placeholder screens (will be replaced in later tasks)
        self.create_placeholder_screens()
        
        # Start on player screen
        self.screen_stack.setCurrentIndex(0)
        
        print("[INFO] Main window initialized")
    
    def setup_window_size(self):
        """Configure window size based on environment"""
        # For development: windowed mode at target resolution
        # For production: fullscreen mode (Phase 12)
        
        # Get screen dimensions
        screen = self.screen()
        screen_geometry = screen.availableGeometry()
        
        # Target resolution: 1280x720 (7" touchscreen landscape)
        target_width = 1280
        target_height = 720
        
        # Ensure window fits on current screen
        window_width = min(target_width, screen_geometry.width() - 100)
        window_height = min(target_height, screen_geometry.height() - 100)
        
        # Center window
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        
        self.setGeometry(x, y, window_width, window_height)
        
        # Set minimum size to prevent too-small windows
        self.setMinimumSize(QSize(800, 480))
        
        print(f"[INFO] Window size: {window_width}x{window_height}")
        print(f"[INFO] Screen size: {screen_geometry.width()}x{screen_geometry.height()}")
    
    def apply_dark_theme(self):
        """Apply dark color scheme to the entire application"""
        palette = QPalette()
        
        # Background colors (matching UI spec)
        palette.setColor(QPalette.Window, QColor("#000000"))  # Black
        palette.setColor(QPalette.WindowText, QColor("#ffffff"))  # White
        palette.setColor(QPalette.Base, QColor("#111827"))  # Gray-900
        palette.setColor(QPalette.AlternateBase, QColor("#1f2937"))  # Gray-800
        palette.setColor(QPalette.Text, QColor("#ffffff"))  # White
        palette.setColor(QPalette.Button, QColor("#1f2937"))  # Gray-800
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))  # White
        palette.setColor(QPalette.Highlight, QColor("#2563eb"))  # Blue-600
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))  # White
        
        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor("#6b7280"))  # Gray-500
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#6b7280"))
        
        self.setPalette(palette)
        
        # Apply stylesheet for additional styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            
            QPushButton {
                background-color: #1f2937;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 16px;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background-color: #374151;
            }
            
            QPushButton:pressed {
                background-color: #4b5563;
            }
            
            QPushButton:disabled {
                background-color: #1f2937;
                color: #6b7280;
            }
            
            QLabel {
                color: #ffffff;
            }
        """)
        
        print("[INFO] Dark theme applied")
    
    def create_placeholder_screens(self):
        """
        Create placeholder screens for development
        These will be replaced with real screens in Phase 7-8
        """
        # Player screen placeholder
        player_screen = self.create_placeholder("Player Screen", 
                                               "Now Playing Interface\n(Phase 8)")
        self.screen_stack.addWidget(player_screen)
        
        # Browse screen placeholder
        browse_screen = self.create_placeholder("Browse Screen",
                                               "Find Shows\n(Phase 7)")
        self.screen_stack.addWidget(browse_screen)
        
        # Settings screen placeholder
        settings_screen = self.create_placeholder("Settings Screen",
                                                 "Device Configuration\n(Future Phase)")
        self.screen_stack.addWidget(settings_screen)
        
        print("[INFO] Placeholder screens created")
    
    def create_placeholder(self, title, subtitle):
        """Create a placeholder screen with title and navigation buttons"""
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            font-size: 18px;
            color: #9ca3af;
            margin-bottom: 30px;
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Navigation buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        # Only show relevant navigation buttons
        if "Player" in title:
            browse_btn = QPushButton("Browse Shows")
            browse_btn.setMinimumSize(200, 60)
            browse_btn.clicked.connect(lambda: self.switch_screen(1))
            button_layout.addWidget(browse_btn)
        
        elif "Browse" in title:
            player_btn = QPushButton("Back to Now Playing")
            player_btn.setMinimumSize(200, 60)
            player_btn.clicked.connect(lambda: self.switch_screen(0))
            button_layout.addWidget(player_btn)
            
            settings_btn = QPushButton("Settings")
            settings_btn.setMinimumSize(200, 60)
            settings_btn.clicked.connect(lambda: self.switch_screen(2))
            button_layout.addWidget(settings_btn)
        
        elif "Settings" in title:
            back_btn = QPushButton("Back to Browse")
            back_btn.setMinimumSize(200, 60)
            back_btn.clicked.connect(lambda: self.switch_screen(1))
            button_layout.addWidget(back_btn)
        
        layout.addLayout(button_layout)
        
        return screen
    
    def switch_screen(self, screen_index):
        """
        Switch to a different screen
        
        Args:
            screen_index: 0=Player, 1=Browse, 2=Settings
        """
        screen_names = ["Player", "Browse", "Settings"]
        if 0 <= screen_index < len(screen_names):
            self.screen_stack.setCurrentIndex(screen_index)
            print(f"[INFO] Switched to {screen_names[screen_index]} screen")
        else:
            print(f"[ERROR] Invalid screen index: {screen_index}")
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts for development/testing"""
        # ESC to exit fullscreen (when implemented)
        if event.key() == Qt.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
                print("[INFO] Exited fullscreen mode")
        
        # F11 to toggle fullscreen
        elif event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
                print("[INFO] Exited fullscreen mode")
            else:
                self.showFullScreen()
                print("[INFO] Entered fullscreen mode")
        
        # Numbers 1-3 to switch screens (for testing)
        elif event.key() == Qt.Key_1:
            self.switch_screen(0)  # Player
        elif event.key() == Qt.Key_2:
            self.switch_screen(1)  # Browse
        elif event.key() == Qt.Key_3:
            self.switch_screen(2)  # Settings


def main():
    """Test the main window"""
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    print("\n" + "="*50)
    print("DeadStream Main Window Test")
    print("="*50)
    print("Navigation:")
    print("  - Click buttons to switch screens")
    print("  - Press 1/2/3 keys to switch screens")
    print("  - Press F11 to toggle fullscreen")
    print("  - Press ESC to exit fullscreen")
    print("="*50 + "\n")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()