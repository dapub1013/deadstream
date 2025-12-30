#!/usr/bin/env python3
"""
DeadStream Settings Screen Framework
Phase 8, Task 8.1: Settings screen framework with category navigation

This creates the settings screen layout with category buttons and content area.
Categories: Network, Audio, Display, Date & Time, About
"""

import sys
import os

from src.ui.widgets.network_settings_widget import NetworkSettingsWidget

# Set up project root path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class SettingsScreen(QWidget):
    """Settings screen with category navigation"""
    
    # Signal emitted when back to browse is clicked
    back_clicked = pyqtSignal()
    
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
        
        # Back button
        back_btn = QPushButton("< Back to Browse")
        back_btn.setFixedSize(200, 60)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        back_btn.clicked.connect(self.back_clicked.emit)
        layout.addWidget(back_btn)
        
        # Title
        title = QLabel("Settings")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title, stretch=1)
        
        # Spacer to balance back button
        layout.addSpacing(200)
        
        return header
    
    def _create_category_sidebar(self):
        """Create the left sidebar with category buttons"""
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #0d0d0d;
                border-right: 1px solid #333333;
            }
        """)
        sidebar.setFixedWidth(280)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(15)
        
        # Category buttons
        self.category_buttons = {}
        
        categories = [
            ("network", "Network", "#3b82f6"),      # Blue
            ("audio", "Audio", "#8b5cf6"),          # Purple
            ("display", "Display", "#10b981"),      # Green
            ("datetime", "Date & Time", "#f59e0b"), # Amber
            ("about", "About", "#6b7280")           # Gray
        ]
        
        for category_id, label, color in categories:
            btn = self._create_category_button(category_id, label, color)
            self.category_buttons[category_id] = btn
            layout.addWidget(btn)
        
        # Stretch at bottom to push buttons to top
        layout.addStretch()
        
        return sidebar
    
    def _create_category_button(self, category_id, label, color):
        """Create a single category button"""
        btn = QPushButton(label)
        btn.setFixedHeight(70)
        btn.setProperty("category_id", category_id)
        btn.setProperty("base_color", color)
        
        # Set initial style (will be updated by update_button_styles)
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
        
        btn.clicked.connect(lambda: self.show_category(category_id))
        return btn
    
    def _create_content_area(self):
        """Create the right content area with scroll"""
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #121212;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #1a1a1a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #333333;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #444444;
            }
        """)
        
        # Content widget inside scroll area
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: #121212;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(40, 30, 40, 30)
        self.content_layout.setSpacing(20)
        
        scroll.setWidget(self.content_widget)
        return scroll
    
    def show_category(self, category_id):
        """Show content for the selected category"""
        self.current_category = category_id
        
        # Update button styles
        self.update_button_styles()
        
        # Clear existing content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add category-specific content
        if category_id == "network":
            self._show_network_settings()
        elif category_id == "audio":
            self._show_audio_settings()
        elif category_id == "display":
            self._show_display_settings()
        elif category_id == "datetime":
            self._show_datetime_settings()
        elif category_id == "about":
            self._show_about_page()
    
    def update_button_styles(self):
        """Update category button styles based on selection"""
        for category_id, btn in self.category_buttons.items():
            color = btn.property("base_color")
            is_selected = (category_id == self.current_category)
            
            if is_selected:
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
        # Placeholder - will be implemented later
        label = QLabel("Audio Settings")
        label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        self.content_layout.addWidget(label)
        
        placeholder = QLabel("Volume, quality, and audio preferences (placeholder)")
        placeholder.setStyleSheet("color: #999999; font-size: 16px;")
        self.content_layout.addWidget(placeholder)
        
        self.content_layout.addStretch()
    
    def _show_display_settings(self):
        """Show display settings content"""
        # Placeholder - will be implemented later
        label = QLabel("Display Settings")
        label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        self.content_layout.addWidget(label)
        
        placeholder = QLabel("Brightness, theme, and display preferences (placeholder)")
        placeholder.setStyleSheet("color: #999999; font-size: 16px;")
        self.content_layout.addWidget(placeholder)
        
        self.content_layout.addStretch()
    
    def _show_datetime_settings(self):
        """Show date & time settings content"""
        # Placeholder - will be implemented later
        label = QLabel("Date & Time Settings")
        label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        self.content_layout.addWidget(label)
        
        placeholder = QLabel("Time zone and date format preferences (placeholder)")
        placeholder.setStyleSheet("color: #999999; font-size: 16px;")
        self.content_layout.addWidget(placeholder)
        
        self.content_layout.addStretch()
    
    def _show_about_page(self):
        """Show about page content"""
        # Placeholder - will be implemented in Task 8.3
        label = QLabel("About DeadStream")
        label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        self.content_layout.addWidget(label)
        
        placeholder = QLabel("Version info and credits will be implemented in Task 8.3")
        placeholder.setStyleSheet("color: #999999; font-size: 16px;")
        self.content_layout.addWidget(placeholder)
        
        self.content_layout.addStretch()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create and show settings screen
    settings = SettingsScreen()
    settings.setWindowTitle("DeadStream Settings")
    settings.setGeometry(100, 100, 1024, 600)
    settings.setStyleSheet("background-color: #121212;")
    
    # Connect back button to close for testing
    settings.back_clicked.connect(app.quit)
    
    settings.show()
    
    print("[INFO] Settings screen framework loaded")
    print("[INFO] Current category:", settings.current_category)
    print("[INFO] Try clicking different category buttons")
    print("[INFO] Press Ctrl+C to quit")
    
    sys.exit(app.exec_())
