#!/usr/bin/env python3
"""
Touch Feedback Verification Test

Phase 10E, Task 10E.8
Tests all interactive components for proper touch feedback and size requirements.

Run this test to verify:
1. All buttons have proper press states
2. Touch targets meet 60px minimum
3. Visual feedback is immediate and clear
4. All interactive elements respond to clicks
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtTest import QTest

from src.ui.components.pill_button import PillButton
from src.ui.components.icon_button import IconButton
from src.ui.components.concert_list_item import ConcertListItem
from src.ui.styles.theme import Theme


class TouchFeedbackTest(QWidget):
    """Test widget to verify touch feedback on all interactive components."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Touch Feedback Verification Test - Phase 10E Task 10E.8")
        self.setGeometry(100, 100, 1280, 720)

        # Test results
        self.test_results = []

        self.init_ui()

    def init_ui(self):
        """Initialize the test UI."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("Touch Feedback Verification Test")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                padding: 10px;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Instructions
        instructions = QLabel(
            "Click each component to verify touch feedback.\n"
            "Press states should show darker color and subtle movement.\n"
            "Check console for detailed test results."
        )
        instructions.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
                padding: 10px;
            }}
        """)
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)

        # Scrollable test area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        test_widget = QWidget()
        test_layout = QVBoxLayout(test_widget)
        test_layout.setSpacing(30)

        # Test PillButtons
        test_layout.addWidget(self.create_pill_button_section())

        # Test IconButtons
        test_layout.addWidget(self.create_icon_button_section())

        # Test ConcertListItems
        test_layout.addWidget(self.create_list_item_section())

        # Test Results Section
        self.results_label = QLabel("Test Results: Pending...")
        self.results_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
                padding: 20px;
                background-color: {Theme.BG_CARD};
                border-radius: 8px;
            }}
        """)
        self.results_label.setWordWrap(True)
        test_layout.addWidget(self.results_label)

        scroll_area.setWidget(test_widget)
        main_layout.addWidget(scroll_area)

        # Set main layout
        self.setLayout(main_layout)

        # Apply theme background
        self.setStyleSheet(f"""
            TouchFeedbackTest {{
                background-color: {Theme.BG_PRIMARY};
            }}
        """)

        # Run automated tests after UI loads
        QTimer.singleShot(100, self.run_automated_tests)

    def create_pill_button_section(self):
        """Create section to test PillButton variants."""
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(16)

        # Section title
        title = QLabel("PillButton Variants")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(title)

        # Button row
        button_row = QHBoxLayout()
        button_row.setSpacing(Theme.BUTTON_SPACING)

        # Create all variants
        variants = [
            ('yellow', 'Yellow Variant'),
            ('green', 'Green Variant'),
            ('blue', 'Blue Variant'),
            ('red', 'Red Variant'),
            ('gradient', 'Gradient Variant')
        ]

        for variant, text in variants:
            btn = PillButton(text, variant=variant)
            btn.clicked.connect(lambda v=variant: self.on_button_clicked(f"PillButton ({v})"))
            button_row.addWidget(btn)

            # Verify size
            size = btn.minimumSize()
            self.verify_size(f"PillButton ({variant})", size.width(), size.height(), 120, 60)

        layout.addLayout(button_row)

        return section

    def create_icon_button_section(self):
        """Create section to test IconButton variants."""
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(16)

        # Section title
        title = QLabel("IconButton Variants")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(title)

        # Button row
        button_row = QHBoxLayout()
        button_row.setSpacing(Theme.BUTTON_SPACING)

        # Create all variants with different icons
        variants = [
            ('home', 'solid', 'Home (Solid)'),
            ('settings', 'transparent', 'Settings (Trans)'),
            ('search', 'outline', 'Search (Outline)'),
            ('play', 'accent', 'Play (Accent)')
        ]

        for icon, variant, label in variants:
            btn = IconButton(icon_type=icon, variant=variant)
            btn.clicked.connect(lambda l=label: self.on_button_clicked(f"IconButton {l}"))
            button_row.addWidget(btn)

            # Verify size
            size = btn.size()
            self.verify_size(f"IconButton ({icon}/{variant})", size.width(), size.height(), 60, 60)

        button_row.addStretch()
        layout.addLayout(button_row)

        return section

    def create_list_item_section(self):
        """Create section to test ConcertListItem."""
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(16)

        # Section title
        title = QLabel("ConcertListItem (Touch Target)")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(title)

        # Create test concert items
        test_shows = [
            {
                'date': '1977-05-08',
                'venue': 'Barton Hall, Cornell University',
                'location': 'Ithaca, NY',
                'rating': 4.8,
                'source': 'SBD'
            },
            {
                'date': '1972-05-03',
                'venue': 'Olympia Theatre',
                'location': 'Paris, France',
                'rating': 4.6,
                'source': 'AUD'
            },
            {
                'date': '1969-08-16',
                'venue': 'Woodstock Music Festival',
                'location': 'Bethel, NY',
                'rating': 4.5,
                'source': 'MATRIX'
            }
        ]

        for show in test_shows:
            item = ConcertListItem(show)
            item.clicked.connect(lambda s=show: self.on_list_item_clicked(s['date']))
            layout.addWidget(item)

            # Verify size
            size = item.minimumSize()
            self.verify_size(f"ConcertListItem ({show['date']})",
                           size.width(), size.height(), 0, 80)

        return section

    def verify_size(self, component_name, width, height, min_width, min_height):
        """Verify component meets size requirements."""
        width_ok = width >= min_width if min_width > 0 else True
        height_ok = height >= min_height

        status = "[PASS]" if (width_ok and height_ok) else "[FAIL]"
        result = f"{status} {component_name}: {width}x{height}px "
        result += f"(min: {min_width}x{min_height}px)"

        self.test_results.append(result)
        print(result)

        return width_ok and height_ok

    def on_button_clicked(self, button_name):
        """Handle button click for testing."""
        print(f"[INFO] {button_name} clicked - Touch feedback triggered")
        self.test_results.append(f"[INTERACTIVE] {button_name} clicked successfully")
        self.update_results_display()

    def on_list_item_clicked(self, show_date):
        """Handle list item click for testing."""
        print(f"[INFO] ConcertListItem ({show_date}) clicked - Press state triggered")
        self.test_results.append(f"[INTERACTIVE] List item ({show_date}) clicked successfully")
        self.update_results_display()

    def run_automated_tests(self):
        """Run automated size verification tests."""
        print("\n" + "="*60)
        print("AUTOMATED TOUCH FEEDBACK VERIFICATION")
        print("Phase 10E, Task 10E.8")
        print("="*60 + "\n")

        print("[INFO] Size Requirements:")
        print(f"  - PillButton: {Theme.BUTTON_MIN_WIDTH}x{Theme.BUTTON_HEIGHT}px")
        print(f"  - IconButton: {Theme.BUTTON_HEIGHT}x{Theme.BUTTON_HEIGHT}px")
        print(f"  - ConcertListItem: full width x {Theme.LIST_ITEM_HEIGHT}px")
        print(f"  - Minimum touch target (WCAG): 44x44px")
        print(f"  - DeadStream standard: 60x60px\n")

        # All size checks already done during UI creation
        print(f"\n[INFO] Total automated checks: {len(self.test_results)}")

        # Count passes and fails
        passes = sum(1 for r in self.test_results if '[PASS]' in r)
        fails = sum(1 for r in self.test_results if '[FAIL]' in r)

        print(f"[INFO] Passed: {passes}")
        print(f"[INFO] Failed: {fails}")

        if fails == 0:
            print("\n[PASS] All touch target size requirements met!")
            print("[INFO] Now test interactivity by clicking components above.")
        else:
            print(f"\n[FAIL] {fails} components failed size requirements!")

        print("="*60 + "\n")

        self.update_results_display()

    def update_results_display(self):
        """Update the results label with current test results."""
        passes = sum(1 for r in self.test_results if '[PASS]' in r)
        fails = sum(1 for r in self.test_results if '[FAIL]' in r)
        interactions = sum(1 for r in self.test_results if '[INTERACTIVE]' in r)

        results_text = f"Test Results:\n\n"
        results_text += f"Size Checks: {passes} passed, {fails} failed\n"
        results_text += f"Interactive Tests: {interactions} components clicked\n\n"
        results_text += "Click components above to test touch feedback.\n"
        results_text += "Check console for detailed results."

        self.results_label.setText(results_text)


def main():
    """Run the touch feedback verification test."""
    print("[INFO] Starting Touch Feedback Verification Test")
    print("[INFO] Phase 10E, Task 10E.8\n")

    app = QApplication(sys.argv)

    test_window = TouchFeedbackTest()
    test_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
