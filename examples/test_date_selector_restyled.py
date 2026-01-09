#!/usr/bin/env python3
"""
Test script for restyled DateSelectorWidget.
Verifies that Theme Manager integration works correctly.

Phase 10E - Task 10E.2: Date Selector Restyle
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

from src.ui.widgets.date_selector import DateSelectorWidget
from src.ui.styles.theme import Theme


class TestWindow(QMainWindow):
    """Test window for DateSelectorWidget"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DateSelector Restyle Test - Phase 10E.2")
        self.setGeometry(100, 100, 1200, 700)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header
        header = QLabel("DateSelector Widget - Theme Manager Integration Test")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                padding: {Theme.SPACING_MEDIUM}px;
                background-color: {Theme.BG_PANEL_DARK};
                border-radius: 8px;
            }}
        """)
        layout.addWidget(header)

        # Test instructions
        instructions = QLabel(
            "Test the restyled DateSelector:\n"
            "1. All colors should use Theme Manager constants\n"
            "2. Selected items should highlight in blue\n"
            "3. Status label should change color when date is selected\n"
            "4. Button should enable only when full date is selected"
        )
        instructions.setAlignment(Qt.AlignLeft)
        instructions.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_SMALL}px;
                color: {Theme.TEXT_SECONDARY};
                padding: {Theme.SPACING_SMALL}px;
                background-color: {Theme.BG_CARD};
                border-radius: 8px;
            }}
        """)
        layout.addWidget(instructions)

        # Date selector widget
        self.date_selector = DateSelectorWidget()
        self.date_selector.date_selected.connect(self.on_date_selected)
        layout.addWidget(self.date_selector)

        # Result label
        self.result_label = QLabel("No date selected yet")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
                padding: {Theme.SPACING_MEDIUM}px;
                background-color: {Theme.BG_CARD};
                border-radius: 8px;
            }}
        """)
        layout.addWidget(self.result_label)

        print("[INFO] DateSelector test window initialized")
        print("[INFO] Verify the following:")
        print("  - Columns use Theme.BG_CARD and Theme.BORDER_SUBTLE")
        print("  - Headers use Theme.BODY_LARGE and Theme.TEXT_PRIMARY")
        print("  - List items use Theme.ACCENT_BLUE when selected")
        print("  - Status label uses Theme.BG_CARD (unselected) and Theme.ACCENT_BLUE (selected)")
        print("  - Button uses Theme.get_button_style()")

    def on_date_selected(self, date_str):
        """Handle date selection"""
        self.result_label.setText(f"Selected Date: {date_str}")
        self.result_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                padding: {Theme.SPACING_MEDIUM}px;
                background-color: {Theme.ACCENT_GREEN};
                border-radius: 8px;
            }}
        """)
        print(f"[PASS] Date selected signal received: {date_str}")


def run_test():
    """Run the DateSelector restyle test"""
    print("\n" + "="*60)
    print("DateSelector Widget Restyle Test - Phase 10E.2")
    print("="*60)

    app = QApplication(sys.argv)

    # Apply global theme
    app.setStyleSheet(Theme.get_global_stylesheet())
    print("[PASS] Applied Theme.get_global_stylesheet()")

    # Create test window
    window = TestWindow()
    window.show()
    print("[PASS] Test window displayed")

    # Manual test checklist
    print("\n" + "="*60)
    print("MANUAL TEST CHECKLIST:")
    print("="*60)
    print("[   ] 1. Three columns (Year/Month/Day) display correctly")
    print("[   ] 2. Column headers have proper styling (Theme colors)")
    print("[   ] 3. List items are readable with good contrast")
    print("[   ] 4. Hover state shows visual feedback")
    print("[   ] 5. Selected items highlight in blue (Theme.ACCENT_BLUE)")
    print("[   ] 6. Status label shows correct text for each state:")
    print("         - 'Select a year to begin' (gray background)")
    print("         - '[Year] - Select a month' (gray background)")
    print("         - '[Month Year] - Select a day' (gray background)")
    print("         - 'Selected: [Full Date]' (blue background)")
    print("[   ] 7. Button is disabled until full date selected")
    print("[   ] 8. Button uses Theme button styling")
    print("[   ] 9. All spacing looks consistent")
    print("[   ] 10. No hardcoded color values visible")
    print("="*60)
    print("\nInteract with the widget to complete the checklist.")
    print("Press Ctrl+C to exit.\n")

    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        run_test()
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
