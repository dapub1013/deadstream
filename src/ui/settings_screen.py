#!/usr/bin/env python3
"""
Settings Screen for DeadStream
Provides device configuration interface with category navigation

Author: DeadStream Development Team
Phase: 8, Task: 8.2 (Updated)
"""

import os
import sys

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from src.ui.widgets.network_settings_widget import NetworkSettingsWidget


class SettingsScreen(QWidget):
    """
    Settings screen with category navigation
    
    Layout:
    - Left panel (40%): Category buttons
    - Right panel (60%): Selected category content
    
    Categories:
    - Network (WiFi management)
    - Audio (volume, quality) - placeholder
    - Display (brightness, theme) - placeholder
    - Date & Time (system time) - placeholder
    - About (version, info)
    """
    
    # Signal emitted when user wants to go back
    browse_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_category = "network"
        self.setup_ui()
    
    # ========================================================================
    # UI SETUP
    # ========================================================================
    
    def setup_ui(self):
        """Initialize the settings screen UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left panel: Category navigation (40%)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 4)
        
        # Right panel: Category content (60%)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 6)
    
    def create_left_panel(self):
        """Create left navigation panel with category buttons"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-right: 2px solid #374151;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Header
        header = QLabel("Settings")
        header.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
        """)
        layout.addWidget(header)
        
        subtitle = QLabel("Device configuration and preferences")
        subtitle.setStyleSheet("""
            color: #9ca3af;
            font-size: 14px;
        """)
        layout.addWidget(subtitle)
        
        # Spacing
        layout.addSpacing(20)
        
        # Category buttons
        self.create_category_buttons(layout)
        
        layout.addStretch()
        
        # Back button
        back_btn = QPushButton("Back to Browse")
        back_btn.setFixedHeight(50)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
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
        
        return panel
    
    def create_category_buttons(self, layout):
        """Create category navigation buttons"""
        
        # Define categories with their colors
        categories = [
            ("network", "Network", "#3b82f6"),      # Blue
            ("audio", "Audio", "#10b981"),          # Green
            ("display", "Display", "#8b5cf6"),      # Purple
            ("datetime", "Date & Time", "#f59e0b"), # Amber
            ("about", "About", "#6b7280")           # Gray
        ]
        
        self.category_buttons = {}
        
        for cat_id, cat_name, color in categories:
            btn = QPushButton(cat_name)
            btn.setFixedHeight(60)
            btn.setCursor(Qt.PointingHandCursor)
            
            # Store category ID with button
            btn.setProperty("category", cat_id)
            btn.setProperty("color", color)
            
            # Connect click handler
            btn.clicked.connect(lambda checked, c=cat_id: self.select_category(c))
            
            # Store button reference
            self.category_buttons[cat_id] = btn
            
            layout.addWidget(btn)
        
        # Set initial selection
        self.update_category_buttons()
    
    def update_category_buttons(self):
        """Update button styles based on selected category"""
        for cat_id, btn in self.category_buttons.items():
            color = btn.property("color")
            
            if cat_id == self.current_category:
                # Selected state
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 16px;
                        font-weight: bold;
                        text-align: left;
                        padding-left: 20px;
                    }}
                """)
            else:
                # Unselected state
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #374151;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 16px;
                        font-weight: bold;
                        text-align: left;
                        padding-left: 20px;
                    }}
                    QPushButton:hover {{
                        background-color: #4b5563;
                    }}
                    QPushButton:pressed {{
                        background-color: {color};
                    }}
                """)
    
    def create_right_panel(self):
        """Create right panel with stacked widgets for each category"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #111827;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Stacked widget for different categories
        self.content_stack = QStackedWidget()
        
        # Add category widgets
        self.content_stack.addWidget(self.create_network_widget())     # 0
        self.content_stack.addWidget(self.create_placeholder("Audio"))  # 1
        self.content_stack.addWidget(self.create_placeholder("Display")) # 2
        self.content_stack.addWidget(self.create_placeholder("Date & Time")) # 3
        self.content_stack.addWidget(self.create_placeholder("About"))  # 4
        
        layout.addWidget(self.content_stack)
        
        return panel
    
    # ========================================================================
    # CATEGORY WIDGETS
    # ========================================================================
    
    def create_network_widget(self):
        """Create network settings widget"""
        return NetworkSettingsWidget()
    
    def create_placeholder(self, category_name):
        """Create placeholder widget for unimplemented categories"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel(f"{category_name} Settings")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        # Placeholder message
        message = QLabel(
            f"The {category_name} settings will be implemented in a future task.\n\n"
            "This is a placeholder for now."
        )
        message.setStyleSheet("""
            color: #9ca3af;
            font-size: 16px;
        """)
        message.setWordWrap(True)
        layout.addWidget(message)
        
        layout.addStretch()
        
        return widget
    
    # ========================================================================
    # CATEGORY NAVIGATION
    # ========================================================================
    
    def select_category(self, category):
        """Handle category selection"""
        if category == self.current_category:
            return
        
        print(f"[INFO] Switching to {category} settings")
        
        self.current_category = category
        
        # Update button styles
        self.update_category_buttons()
        
        # Switch content
        category_index = {
            "network": 0,
            "audio": 1,
            "display": 2,
            "datetime": 3,
            "about": 4
        }
        
        self.content_stack.setCurrentIndex(category_index[category])


# Test code
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create test window
    window = QWidget()
    window.setWindowTitle("Settings Screen Test")
    window.setGeometry(100, 100, 1280, 720)
    
    layout = QVBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)
    
    # Add settings screen
    settings = SettingsScreen()
    layout.addWidget(settings)
    
    window.show()
    sys.exit(app.exec_())
