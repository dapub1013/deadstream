#!/usr/bin/env python3
"""
DeadStream Settings Screen
Phase 8, Task 8.1 & 8.2: Settings screen framework with network settings

This screen provides device configuration and preferences.
Categories: Network, Audio, Display, Date & Time, About
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class SettingsScreen(QWidget):
    """Settings screen with category navigation"""
    
    # Signal emitted when back to browse is clicked
    browse_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_category = "network"  # Default category
        self.init_ui()
    
    def init_ui(self):
        """Initialize the settings screen UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header with title and back button
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Content area (horizontal split: categories on left, content on right)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Left sidebar - Category buttons
        category_sidebar = self._create_category_sidebar()
        content_layout.addWidget(category_sidebar)
        
        # Right content area - Settings content
        self.content_area = self._create_content_area()
        content_layout.addWidget(self.content_area, stretch=1)
        
        main_layout.addLayout(content_layout)
        
        # Show initial category (Network)
        self.show_category("network")
    
    def _create_header(self):
        """Create the header with title and back button"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-bottom: 1px solid #333333;
            }
        """)
        header.setFixedHeight(80)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("""
            color: #ffffff;
            font-size: 32px;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Back button
        back_btn = QPushButton("Back to Browse")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: #ffffff;
                border: 2px solid #4b5563;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #6b7280;
            }
        """)
        back_btn.clicked.connect(self.browse_requested.emit)
        layout.addWidget(back_btn)
        
        return header
    
    def _create_category_sidebar(self):
        """Create the left sidebar with category buttons"""
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #0f0f0f;
                border-right: 1px solid #262626;
            }
        """)
        sidebar.setFixedWidth(300)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        
        # Category buttons
        self.category_buttons = {}
        
        categories = [
            ("network", "Network", "#2563eb"),
            ("audio", "Audio", "#7c3aed"),
            ("display", "Display", "#059669"),
            ("datetime", "Date & Time", "#dc2626"),
            ("about", "About", "#ea580c"),
        ]
        
        for category_id, label, color in categories:
            btn = QPushButton(f"  {label}")
            btn.setFixedHeight(60)
            btn.clicked.connect(lambda checked, c=category_id: self.show_category(c))
            self.category_buttons[category_id] = (btn, color)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return sidebar
    
    def _create_content_area(self):
        """Create the right content area"""
        content = QFrame()
        content.setStyleSheet("""
            QFrame {
                background-color: #0a0a0a;
            }
        """)
        
        # Use QVBoxLayout for content (will be populated by show_category)
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        return content
    
    def show_category(self, category):
        """Show content for selected category"""
        # Clear existing content
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Update current category
        self.current_category = category
        
        # Update button styles
        self._update_button_styles()
        
        # Load category content
        if category == "network":
            self._show_network_settings()
        elif category == "audio":
            self._show_audio_settings()
        elif category == "display":
            self._show_display_settings()
        elif category == "datetime":
            self._show_datetime_settings()
        elif category == "about":
            self._show_about()
    
    def _update_button_styles(self):
        """Update category button styles based on selection"""
        for category_id, (btn, color) in self.category_buttons.items():
            if category_id == self.current_category:
                # Selected state - colored background
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: #ffffff;
                        border: 2px solid {color};
                        border-radius: 10px;
                        font-size: 18px;
                        font-weight: 600;
                        text-align: left;
                        padding-left: 20px;
                    }}
                    QPushButton:hover {{
                        background-color: {color};
                    }}
                """)
            else:
                # Unselected state - dark background
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #1a1a1a;
                        color: #ffffff;
                        border: 2px solid #333333;
                        border-radius: 10px;
                        font-size: 18px;
                        font-weight: 600;
                        text-align: left;
                        padding-left: 20px;
                    }}
                    QPushButton:hover {{
                        background-color: #262626;
                        border-color: {color};
                    }}
                """)
    
    def _show_network_settings(self):
        """Show network settings content"""
        from src.ui.widgets.network_settings_widget import NetworkSettingsWidget
        
        network_widget = NetworkSettingsWidget()
        self.content_layout.addWidget(network_widget)
    
    def _show_audio_settings(self):
        """Show audio settings content"""
        # Placeholder - will be implemented in Task 8.5
        label = QLabel("Audio Settings")
        label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold; padding: 30px;")
        self.content_layout.addWidget(label)
        
        placeholder = QLabel("Volume, quality, and audio preferences (coming soon)")
        placeholder.setStyleSheet("color: #999999; font-size: 16px; padding: 0 30px;")
        self.content_layout.addWidget(placeholder)
        
        self.content_layout.addStretch()
    
    def _show_display_settings(self):
        """Show display settings content"""
        # Placeholder - will be implemented in Task 8.6
        label = QLabel("Display Settings")
        label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold; padding: 30px;")
        self.content_layout.addWidget(label)
        
        placeholder = QLabel("Brightness, theme, and display preferences (coming soon)")
        placeholder.setStyleSheet("color: #999999; font-size: 16px; padding: 0 30px;")
        self.content_layout.addWidget(placeholder)
        
        self.content_layout.addStretch()
    
    def _show_datetime_settings(self):
        """Show date & time settings content"""
        # Placeholder - will be implemented in Task 8.7
        label = QLabel("Date & Time Settings")
        label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold; padding: 30px;")
        self.content_layout.addWidget(label)
        
        placeholder = QLabel("Date, time, and timezone settings (coming soon)")
        placeholder.setStyleSheet("color: #999999; font-size: 16px; padding: 0 30px;")
        self.content_layout.addWidget(placeholder)
        
        self.content_layout.addStretch()
    
    def _show_about(self):
        """Show about page content"""
        # Placeholder - will be implemented in Task 8.3
        label = QLabel("About DeadStream")
        label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold; padding: 30px;")
        self.content_layout.addWidget(label)
        
        placeholder = QLabel("Version info, database stats, and credits (coming soon)")
        placeholder.setStyleSheet("color: #999999; font-size: 16px; padding: 0 30px;")
        self.content_layout.addWidget(placeholder)
        
        self.content_layout.addStretch()


# Standalone test
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    screen = SettingsScreen()
    screen.setStyleSheet("background-color: #0a0a0a;")
    screen.setWindowTitle("Settings Screen Test")
    screen.setGeometry(100, 100, 1280, 720)
    screen.show()
    
    print("[INFO] Settings screen test running")
    print("[INFO] Click category buttons to switch between settings")
    print("[INFO] Network settings should display WiFi info")
    print("[INFO] Other categories show placeholders")
    
    sys.exit(app.exec_())
