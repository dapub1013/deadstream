#!/usr/bin/env python3
"""
DeadStream Settings Screen Framework
Phase 8, Task 8.1-8.7: Settings screen framework with all categories
"""

import sys
import os


# Set up project root path (4 levels up from src/ui/screens/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import settings widgets
from src.ui.widgets.about_widget import AboutWidget
from src.ui.widgets.display_settings_widget import DisplaySettingsWidget 
from src.ui.widgets.network_settings_widget import NetworkSettingsWidget
from src.ui.widgets.audio_settings_widget import AudioSettingsWidget
from src.ui.widgets.database_settings_widget import DatabaseSettingsWidget
from src.ui.widgets.datetime_settings_widget import DateTimeSettingsWidget

class SettingsScreen(QWidget):
    """Settings screen with category navigation"""
    
    # Signal emitted when back to browse is clicked
    back_clicked = pyqtSignal()
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
            ("database", "Database", "#ef4444"),    # Red - NEW
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
        """Create the right content area with stacked widgets"""
        # Use QStackedWidget instead of clearing/recreating widgets
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: #121212;
                border: none;
            }
        """)
        
        # Create all setting widgets upfront
        # Network settings (implemented - Task 8.2)
        self.network_widget = NetworkSettingsWidget()
        self.content_stack.addWidget(self.network_widget)

        # Audio settings (implemented)
        self.audio_widget = AudioSettingsWidget()
        self.content_stack.addWidget(self.audio_widget)

        # Database settings (implemented - Task 8.7)
        self.database_widget = DatabaseSettingsWidget()
        self.content_stack.addWidget(self.database_widget)

        # Display settings (implemented)
        self.display_widget = DisplaySettingsWidget()
        self.content_stack.addWidget(self.display_widget)
        
        # Date & Time settings (implemented - Task 8.7)
        self.datetime_widget = DateTimeSettingsWidget()
        self.content_stack.addWidget(self.datetime_widget)
        
        # About page (implemented)
        self.about_widget = AboutWidget()
        self.content_stack.addWidget(self.about_widget)
        
        return self.content_stack
    
    def _create_placeholder_widget(self, title, description):
        """Create a placeholder widget for settings not yet implemented"""
        widget = QWidget()
        widget.setStyleSheet("background-color: #121212;")
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)
        
        label = QLabel(title)
        label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        layout.addWidget(label)
        
        placeholder = QLabel(description)
        placeholder.setStyleSheet("color: #999999; font-size: 16px;")
        layout.addWidget(placeholder)
        
        layout.addStretch()
        
        return widget
    
    def show_category(self, category_id):
        """Show content for the selected category"""
        self.current_category = category_id
        
        # Update button styles
        self.update_button_styles()
        
        # Switch to the appropriate widget in the stack
        if category_id == "network":
            self.content_stack.setCurrentWidget(self.network_widget)
        elif category_id == "audio":
            self.content_stack.setCurrentWidget(self.audio_widget)
        elif category_id == "database":
            self.content_stack.setCurrentWidget(self.database_widget)
        elif category_id == "display":
            self.content_stack.setCurrentWidget(self.display_widget)
        elif category_id == "datetime":
            self.content_stack.setCurrentWidget(self.datetime_widget)
        elif category_id == "about":
            self.content_stack.setCurrentWidget(self.about_widget)
    
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
    print("[INFO] All settings categories now complete - Task 8.7 ✓")
    print("[INFO] Press Ctrl+C to quit")
    
    sys.exit(app.exec_())
