#!/usr/bin/env python3
"""
About Widget for Settings Screen
Shows application information, version, and database statistics
"""

import sys
import os

# Add project root to path for imports (4 levels up from src/ui/widgets/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.database.queries import get_show_count


class AboutWidget(QWidget):
    """
    About page showing application information and statistics
    
    Features:
    - Application name and version
    - Build date
    - Device information
    - Database statistics (show count)
    - Credits and acknowledgments
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the About page UI"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        
        # Title
        title = QLabel("About")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Device information and version")
        subtitle.setStyleSheet("color: #9ca3af; font-size: 14px;")
        header_layout.addWidget(subtitle)
        
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        
        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 20, 0)
        content_layout.setSpacing(20)
        
        # Application info card
        app_card = self._create_info_card(
            "Grateful Dead Concert Player",
            [
                ("Version", "1.0.0"),
                ("Build Date", "2025.12.30"),
                ("Platform", "Raspberry Pi 4"),
                ("Display", "7-inch Touchscreen (1280x720)")
            ]
        )
        content_layout.addWidget(app_card)
        
        # Database statistics card
        try:
            show_count = get_show_count()
            db_stats = [
                ("Total Shows", f"{show_count:,}"),
                ("Date Range", "1965-1995"),
                ("Data Source", "Internet Archive"),
                ("Last Updated", "2025.12.21")
            ]
        except Exception as e:
            print(f"[ERROR] Failed to get database stats: {e}")
            db_stats = [
                ("Status", "Database Error"),
                ("Message", "Unable to load statistics")
            ]
        
        db_card = self._create_info_card("Database Statistics", db_stats)
        content_layout.addWidget(db_card)
        
        # Credits card
        credits_card = self._create_info_card(
            "Credits & Acknowledgments",
            [
                ("Recordings", "Internet Archive"),
                ("Tapers", "Grateful Dead recording community"),
                ("Developer", "DeadStream Project"),
                ("Framework", "PyQt5"),
                ("Audio Engine", "VLC Media Player")
            ]
        )
        content_layout.addWidget(credits_card)
        
        # Legal notice card
        legal_card = self._create_info_card(
            "Legal Notice",
            [
                ("License", "MIT License"),
                ("Usage", "Personal, non-commercial use"),
                ("Recordings", "Courtesy of Internet Archive"),
                ("Trademark", "Grateful Dead is a registered trademark")
            ]
        )
        content_layout.addWidget(legal_card)
        
        # Add stretch to push content to top
        content_layout.addStretch()
        
        # Set content widget to scroll area
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
    
    def _create_info_card(self, title, info_items):
        """
        Create an information card with title and key-value pairs
        
        Args:
            title: Card title
            info_items: List of (key, value) tuples
        
        Returns:
            QFrame containing the information card
        """
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Card title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: 600;")
        card_layout.addWidget(title_label)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #374151; max-height: 1px;")
        card_layout.addWidget(separator)
        
        # Info items
        for key, value in info_items:
            item_layout = QHBoxLayout()
            item_layout.setSpacing(20)
            
            # Key label (left-aligned)
            key_label = QLabel(key)
            key_label.setStyleSheet("color: #9ca3af; font-size: 14px;")
            key_label.setMinimumWidth(150)
            item_layout.addWidget(key_label)
            
            # Value label (left-aligned)
            value_label = QLabel(str(value))
            value_label.setStyleSheet("color: white; font-size: 14px;")
            value_label.setWordWrap(True)
            item_layout.addWidget(value_label, 1)
            
            card_layout.addLayout(item_layout)
        
        return card


# Standalone test
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create test window
    widget = AboutWidget()
    widget.setWindowTitle("About Widget Test")
    widget.setGeometry(100, 100, 600, 700)
    widget.setStyleSheet("background-color: #000000;")
    widget.show()
    
    sys.exit(app.exec_())