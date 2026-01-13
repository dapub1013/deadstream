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

# Import Theme Manager (centralized styling)
from src.ui.styles.theme import Theme

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
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_PANEL_DARK};
                border-bottom: 1px solid {Theme.BORDER_SUBTLE};
            }}
        """)
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(Theme.SPACING_LARGE, 0, Theme.SPACING_LARGE, 0)

        # Back button
        back_btn = QPushButton("Back to Browse")
        back_btn.setFixedSize(200, Theme.BUTTON_HEIGHT)
        back_btn.setStyleSheet(Theme.get_button_style(Theme.ACCENT_BLUE))
        back_btn.clicked.connect(self.back_clicked.emit)
        layout.addWidget(back_btn)

        # Title
        title = QLabel("Settings")
        title.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
                background-color: transparent;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title, stretch=1)

        # Spacer to balance back button
        layout.addSpacing(200)

        return header
    
    def _create_category_sidebar(self):
        """Create the left sidebar with category buttons"""
        sidebar = QFrame()
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_PANEL_BLACK};
                border-right: 1px solid {Theme.BORDER_SUBTLE};
            }}
        """)
        sidebar.setFixedWidth(280)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(Theme.SPACING_LARGE, Theme.SPACING_XLARGE, Theme.SPACING_LARGE, Theme.SPACING_XLARGE)
        layout.setSpacing(Theme.BUTTON_SPACING)
        
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
        btn.setFixedHeight(Theme.BUTTON_HEIGHT)
        btn.setProperty("category_id", category_id)
        btn.setProperty("base_color", color)

        # Set initial unselected style (will be updated by update_button_styles)
        btn.setStyleSheet(self._get_unselected_button_style())

        btn.clicked.connect(lambda: self.show_category(category_id))
        return btn
    
    def _create_content_area(self):
        """Create the right content area with stacked widgets"""
        # Wrapper container for scroll area
        container = QWidget()
        container.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Scroll area to handle tall content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Theme.BG_PRIMARY};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {Theme.BG_PANEL_BLACK};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {Theme.BORDER_SUBTLE};
                border-radius: 6px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {Theme.TEXT_SECONDARY};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        # Use QStackedWidget for switching between settings categories
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {Theme.BG_PRIMARY};
                border: none;
            }}
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

        # Add stack to scroll area
        scroll_area.setWidget(self.content_stack)
        container_layout.addWidget(scroll_area)

        return container
    
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
    
    def _get_unselected_button_style(self):
        """Get the stylesheet for unselected category buttons"""
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.TEXT_SECONDARY};
                border: 1px solid {Theme.BORDER_SUBTLE};
                border-radius: {Theme.SPACING_SMALL}px;
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                text-align: left;
                padding: {Theme.SPACING_MEDIUM}px;
            }}
            QPushButton:hover {{
                background-color: {Theme.BORDER_SUBTLE};
                color: {Theme.TEXT_PRIMARY};
            }}
        """

    def update_button_styles(self):
        """Update category button styles based on selection"""
        for category_id, btn in self.category_buttons.items():
            color = btn.property("base_color")
            is_selected = (category_id == self.current_category)

            if is_selected:
                # Selected state - colored background (custom color per category)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: {Theme.TEXT_PRIMARY};
                        border: none;
                        border-radius: {Theme.SPACING_SMALL}px;
                        font-size: {Theme.BODY_LARGE}px;
                        font-weight: {Theme.WEIGHT_BOLD};
                        text-align: left;
                        padding: {Theme.SPACING_MEDIUM}px;
                    }}
                    QPushButton:hover {{
                        background-color: {Theme._lighten_color(color, 10)};
                    }}
                    QPushButton:pressed {{
                        background-color: {Theme._darken_color(color, 10)};
                    }}
                """)
            else:
                # Unselected state
                btn.setStyleSheet(self._get_unselected_button_style())


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create and show settings screen
    settings = SettingsScreen()
    settings.setWindowTitle("DeadStream Settings")
    settings.setGeometry(100, 100, 1024, 600)
    settings.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
    
    # Connect back button to close for testing
    settings.back_clicked.connect(app.quit)
    
    settings.show()
    
    print("[INFO] Settings screen framework loaded")
    print("[INFO] Current category:", settings.current_category)
    print("[INFO] Try clicking different category buttons")
    print("[INFO] All settings categories now complete - Task 8.7 ✓")
    print("[INFO] Press Ctrl+C to quit")
    
    sys.exit(app.exec_())
