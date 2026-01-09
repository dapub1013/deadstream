#!/usr/bin/env python3
"""
Test Enhanced Loading Indicators - Phase 10E Task 10E.6

Tests the enhanced loading states across all widgets:
- LoadingSpinner with Theme Manager colors
- LoadingIndicator in show lists
- LoadingIndicator in random show widget
- Animated spinner with proper styling

Phase 10E Enhancement:
- Replaced text-only "Loading..." with animated spinners
- Uses Theme Manager for all colors and spacing
- Professional appearance with smooth animations
- Consistent across all screens
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from src.ui.styles.theme import Theme
from src.ui.widgets.loading_spinner import LoadingSpinner, LoadingIndicator, LoadingOverlay
from src.ui.widgets.show_list import ShowListWidget
from src.ui.widgets.random_show_widget import RandomShowWidget


class LoadingIndicatorTestWindow(QMainWindow):
    """
    Test window demonstrating all loading indicator variants.

    Shows:
    1. LoadingSpinner (basic rotating spinner)
    2. LoadingIndicator (inline with message)
    3. LoadingOverlay (full-screen with optional cancel)
    4. ShowListWidget loading state
    5. RandomShowWidget loading state
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phase 10E - Enhanced Loading Indicators Test")
        self.setGeometry(100, 100, 1200, 800)

        # Set dark background
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {Theme.BG_PRIMARY};
            }}
        """)

        self.setup_ui()

    def setup_ui(self):
        """Set up the test UI"""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(Theme.SPACING_LARGE)
        main_layout.setContentsMargins(
            Theme.SPACING_XLARGE,
            Theme.SPACING_XLARGE,
            Theme.SPACING_XLARGE,
            Theme.SPACING_XLARGE
        )

        # Title
        title = QLabel("Enhanced Loading Indicators - Phase 10E")
        title_font = QFont()
        title_font.setFamily(Theme.FONT_FAMILY)
        title_font.setPointSize(Theme.HEADER_MEDIUM)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Animated spinners with Theme Manager styling")
        subtitle_font = QFont()
        subtitle_font.setFamily(Theme.FONT_FAMILY)
        subtitle_font.setPointSize(Theme.BODY_LARGE)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(Theme.SPACING_MEDIUM)

        # Demo tabs
        self.demo_stack = QStackedWidget()

        # Tab 1: Basic Spinners
        self.demo_stack.addWidget(self.create_spinner_demo())

        # Tab 2: Loading Indicators
        self.demo_stack.addWidget(self.create_indicator_demo())

        # Tab 3: Widget Integration
        self.demo_stack.addWidget(self.create_widget_demo())

        main_layout.addWidget(self.demo_stack, stretch=1)

        # Tab buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(Theme.SPACING_MEDIUM)

        btn1 = self.create_tab_button("Basic Spinners", 0)
        btn2 = self.create_tab_button("Loading Indicators", 1)
        btn3 = self.create_tab_button("Widget Integration", 2)

        button_layout.addWidget(btn1)
        button_layout.addWidget(btn2)
        button_layout.addWidget(btn3)

        main_layout.addLayout(button_layout)

    def create_tab_button(self, text, index):
        """Create a tab selection button"""
        btn = QPushButton(text)
        btn.setMinimumHeight(Theme.BUTTON_HEIGHT)
        btn.clicked.connect(lambda: self.demo_stack.setCurrentIndex(index))

        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.ACCENT_BLUE};
                color: {Theme.TEXT_PRIMARY};
                font-family: {Theme.FONT_FAMILY};
                font-size: {Theme.BODY_MEDIUM}px;
                font-weight: bold;
                border: none;
                border-radius: {Theme.BORDER_RADIUS_LARGE}px;
                padding: {Theme.SPACING_SMALL}px {Theme.SPACING_LARGE}px;
            }}
            QPushButton:hover {{
                background-color: {Theme.ACCENT_BLUE_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Theme.ACCENT_BLUE_PRESSED};
            }}
        """)

        return btn

    def create_spinner_demo(self):
        """Create demo of basic spinners"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(Theme.SPACING_XLARGE)

        # Title
        title = QLabel("LoadingSpinner - Basic Rotating Spinner")
        title.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-family: {Theme.FONT_FAMILY};
                font-size: {Theme.HEADER_SMALL}px;
                font-weight: bold;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Spinner row
        spinner_row = QHBoxLayout()
        spinner_row.setSpacing(Theme.SPACING_XLARGE)
        spinner_row.setAlignment(Qt.AlignCenter)

        # Small spinner
        small_container = self.create_spinner_container("Small (40px)", 40)
        spinner_row.addWidget(small_container)

        # Medium spinner
        medium_container = self.create_spinner_container("Medium (60px)", 60)
        spinner_row.addWidget(medium_container)

        # Large spinner
        large_container = self.create_spinner_container("Large (80px)", 80)
        spinner_row.addWidget(large_container)

        layout.addLayout(spinner_row)

        return widget

    def create_spinner_container(self, label_text, size):
        """Create a labeled spinner container"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(Theme.SPACING_SMALL)

        # Spinner
        spinner = LoadingSpinner(self, size=size)
        spinner.start()

        spinner_widget = QWidget()
        spinner_layout = QVBoxLayout(spinner_widget)
        spinner_layout.setAlignment(Qt.AlignCenter)
        spinner_layout.addWidget(spinner)

        layout.addWidget(spinner_widget)

        # Label
        label = QLabel(label_text)
        label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                font-family: {Theme.FONT_FAMILY};
                font-size: {Theme.BODY_SMALL}px;
            }}
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        return container

    def create_indicator_demo(self):
        """Create demo of loading indicators"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(Theme.SPACING_XLARGE)

        # Title
        title = QLabel("LoadingIndicator - Inline with Message")
        title.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-family: {Theme.FONT_FAMILY};
                font-size: {Theme.HEADER_SMALL}px;
                font-weight: bold;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Indicators row
        indicators_row = QHBoxLayout()
        indicators_row.setSpacing(Theme.SPACING_XLARGE)
        indicators_row.setAlignment(Qt.AlignCenter)

        # Loading shows
        ind1 = LoadingIndicator(self, message="Loading shows...")
        ind1.start()
        indicators_row.addWidget(ind1)

        # Loading random show
        ind2 = LoadingIndicator(self, message="Loading random show...")
        ind2.start()
        indicators_row.addWidget(ind2)

        # Searching
        ind3 = LoadingIndicator(self, message="Searching database...")
        ind3.start()
        indicators_row.addWidget(ind3)

        layout.addLayout(indicators_row)

        return widget

    def create_widget_demo(self):
        """Create demo of widgets using loading states"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(Theme.SPACING_MEDIUM)

        # Title
        title = QLabel("Widget Integration - Real Usage")
        title.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-family: {Theme.FONT_FAMILY};
                font-size: {Theme.HEADER_SMALL}px;
                font-weight: bold;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Widgets row
        widgets_row = QHBoxLayout()
        widgets_row.setSpacing(Theme.SPACING_LARGE)

        # ShowListWidget in loading state
        show_list_container = self.create_widget_container(
            "ShowListWidget",
            "Used in browse screen"
        )
        show_list = ShowListWidget()
        show_list.set_loading_state()
        show_list.setMinimumHeight(400)
        show_list_container.layout().addWidget(show_list)
        widgets_row.addWidget(show_list_container)

        # RandomShowWidget in loading state
        random_show_container = self.create_widget_container(
            "RandomShowWidget",
            "Used in random show mode"
        )
        random_show = RandomShowWidget()
        random_show.show_loading()
        random_show.setMinimumHeight(400)
        random_show_container.layout().addWidget(random_show)
        widgets_row.addWidget(random_show_container)

        layout.addLayout(widgets_row)

        return widget

    def create_widget_container(self, title_text, subtitle_text):
        """Create a container for widget demo"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(Theme.SPACING_SMALL)

        # Title
        title = QLabel(title_text)
        title.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-family: {Theme.FONT_FAMILY};
                font-size: {Theme.BODY_LARGE}px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel(subtitle_text)
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                font-family: {Theme.FONT_FAMILY};
                font-size: {Theme.BODY_SMALL}px;
            }}
        """)
        layout.addWidget(subtitle)

        return container


def main():
    """Run the loading indicator test"""
    print("\n" + "="*60)
    print("[Phase 10E] Task 10E.6: Enhanced Loading States Test")
    print("="*60)
    print("\n[INFO] Starting loading indicator test...")
    print("[INFO] Demonstrating:")
    print("  - LoadingSpinner with Theme Manager colors")
    print("  - LoadingIndicator with animated spinners")
    print("  - Integration in ShowListWidget and RandomShowWidget")
    print("  - Professional appearance with smooth animations\n")

    app = QApplication(sys.argv)
    window = LoadingIndicatorTestWindow()
    window.show()

    print("[PASS] Loading indicator test window opened")
    print("\n[INFO] Test Features:")
    print("  1. Tab 1: Basic spinners in different sizes")
    print("  2. Tab 2: Loading indicators with messages")
    print("  3. Tab 3: Real widget integration\n")
    print("[INFO] All loading indicators use Theme Manager")
    print("[INFO] Animations run at 20fps for smooth performance")
    print("\n" + "="*60 + "\n")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
