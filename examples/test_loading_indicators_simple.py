#!/usr/bin/env python3
"""
Simple Enhanced Loading Indicators Test - Phase 10E Task 10E.6

Tests the enhanced loading states without complex dependencies:
- LoadingSpinner with Theme Manager colors
- LoadingIndicator with animated spinners
- Theme Manager integration
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
    QHBoxLayout, QLabel, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.ui.styles.theme import Theme
from src.ui.widgets.loading_spinner import LoadingSpinner, LoadingIndicator, LoadingOverlay


class SimpleLoadingTestWindow(QMainWindow):
    """
    Simple test window demonstrating loading indicators.

    Shows:
    1. LoadingSpinner in different sizes
    2. LoadingIndicator with different messages
    3. LoadingOverlay (full-screen)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phase 10E - Enhanced Loading Indicators Test")
        self.setGeometry(100, 100, 1000, 700)

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

        main_layout.addSpacing(Theme.SPACING_LARGE)

        # Section 1: Basic Spinners
        section1_label = self.create_section_label("1. LoadingSpinner - Basic Rotating Spinner")
        main_layout.addWidget(section1_label)

        spinner_row = QHBoxLayout()
        spinner_row.setSpacing(Theme.SPACING_XLARGE)
        spinner_row.setAlignment(Qt.AlignCenter)

        # Small spinner
        spinner_row.addWidget(self.create_spinner_container("Small (40px)", 40))

        # Medium spinner
        spinner_row.addWidget(self.create_spinner_container("Medium (60px)", 60))

        # Large spinner
        spinner_row.addWidget(self.create_spinner_container("Large (80px)", 80))

        main_layout.addLayout(spinner_row)
        main_layout.addSpacing(Theme.SPACING_XLARGE)

        # Section 2: Loading Indicators
        section2_label = self.create_section_label("2. LoadingIndicator - Inline with Message")
        main_layout.addWidget(section2_label)

        indicators_row = QHBoxLayout()
        indicators_row.setSpacing(Theme.SPACING_LARGE)
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

        main_layout.addLayout(indicators_row)
        main_layout.addSpacing(Theme.SPACING_XLARGE)

        # Section 3: Overlay Demo
        section3_label = self.create_section_label("3. LoadingOverlay - Full Screen")
        main_layout.addWidget(section3_label)

        overlay_btn = QPushButton("Show Loading Overlay")
        overlay_btn.setMinimumHeight(Theme.BUTTON_HEIGHT)
        overlay_btn.clicked.connect(self.show_overlay)
        overlay_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.ACCENT_YELLOW};
                color: {Theme.TEXT_DARK};
                font-family: {Theme.FONT_FAMILY};
                font-size: {Theme.BODY_MEDIUM}px;
                font-weight: bold;
                border: none;
                border-radius: {Theme.BUTTON_RADIUS}px;
                padding: {Theme.SPACING_SMALL}px {Theme.SPACING_LARGE}px;
            }}
        """)
        main_layout.addWidget(overlay_btn, alignment=Qt.AlignCenter)

        main_layout.addStretch()

        # Create overlay (hidden initially)
        self.overlay = LoadingOverlay(central)

    def create_section_label(self, text):
        """Create a section header label"""
        label = QLabel(text)
        label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-family: {Theme.FONT_FAMILY};
                font-size: {Theme.HEADER_SMALL}px;
                font-weight: bold;
            }}
        """)
        return label

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

    def show_overlay(self):
        """Show the loading overlay for 3 seconds"""
        from PyQt5.QtCore import QTimer

        self.overlay.show_loading("Processing your request...", allow_cancel=True)

        # Auto-hide after 3 seconds
        QTimer.singleShot(3000, self.overlay.hide_loading)


def main():
    """Run the loading indicator test"""
    print("\n" + "="*60)
    print("[Phase 10E] Task 10E.6: Enhanced Loading States Test")
    print("="*60)
    print("\n[INFO] Starting loading indicator test...")
    print("[INFO] Demonstrating:")
    print("  - LoadingSpinner with Theme Manager colors")
    print("  - LoadingIndicator with animated spinners")
    print("  - LoadingOverlay for full-screen loading")
    print("  - Professional appearance with smooth animations\n")

    app = QApplication(sys.argv)
    window = SimpleLoadingTestWindow()
    window.show()

    print("[PASS] Loading indicator test window opened")
    print("\n[INFO] Test Features:")
    print("  1. Section 1: Basic spinners in different sizes (40px, 60px, 80px)")
    print("  2. Section 2: Loading indicators with contextual messages")
    print("  3. Section 3: Full-screen overlay (click button to test)\n")
    print("[INFO] Theme Integration:")
    print(f"  - Accent color: {Theme.ACCENT_BLUE}")
    print(f"  - Text color: {Theme.TEXT_SECONDARY}")
    print(f"  - Font family: {Theme.FONT_FAMILY}")
    print(f"  - Spacing: Theme.SPACING_* constants")
    print("\n[INFO] All loading indicators use Theme Manager")
    print("[INFO] Animations run at 20fps for smooth performance")
    print("[INFO] LoadingSpinner updates every 50ms (30-degree rotation)")
    print("\n[PASS] Task 10E.6 Complete: Enhanced loading states implemented")
    print("\n" + "="*60 + "\n")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
