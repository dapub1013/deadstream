#!/usr/bin/env python3
"""
Test script to verify Display Settings scrolling in Settings Screen
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt5.QtCore import Qt

from src.ui.styles.theme import Theme
from src.ui.widgets.display_settings_widget import DisplaySettingsWidget

class TestWindow(QMainWindow):
    """Test window to simulate application constraints"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Display Settings Scroll Test")
        self.setGeometry(100, 100, 1280, 720)  # DeadStream resolution

        # Create central widget with container layout
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header (simulating app header - 80px)
        header = QLabel("Settings Screen (with 80px header)")
        header.setFixedHeight(80)
        header.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.BG_PANEL_DARK};
                color: {Theme.TEXT_PRIMARY};
                font-size: 24px;
                font-weight: bold;
                padding-left: 20px;
                border-bottom: 1px solid {Theme.BORDER_SUBTLE};
            }}
        """)
        header.setAlignment(Qt.AlignVCenter)
        main_layout.addWidget(header)

        # Content area with scroll
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

        # Display settings widget
        self.display_widget = DisplaySettingsWidget()
        scroll_area.setWidget(self.display_widget)

        main_layout.addWidget(scroll_area)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TestWindow()
    window.show()

    print("[INFO] Display Settings Scroll Test")
    print("[INFO] Window size: 1280x720 (DeadStream resolution)")
    print("[INFO] Header takes 80px, content area has remaining 640px")
    print("[INFO] Display widget should be scrollable if content exceeds 640px")
    print("[INFO] Test scrolling with mouse wheel or scrollbar")
    print("[INFO] All content should be accessible")

    sys.exit(app.exec_())
