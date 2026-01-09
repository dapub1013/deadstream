#!/usr/bin/env python3
"""
Test script for VenueBrowser widget (Polished Placeholder).
Verifies Theme Manager integration and functionality.

Phase 10E - Task 10E.4 Option B: Venue Browser Placeholder
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

from src.ui.widgets.venue_browser import VenueBrowser
from src.ui.styles.theme import Theme


class TestWindow(QMainWindow):
    """Test window for VenueBrowser widget"""

    def __init__(self, with_database=False):
        super().__init__()
        self.setWindowTitle("VenueBrowser Placeholder Test - Phase 10E.4")
        self.setGeometry(100, 100, 1000, 800)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header
        header = QLabel("VenueBrowser Widget - Polished Placeholder Test")
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
        mode_text = "WITH DATABASE" if with_database else "WITHOUT DATABASE (placeholder mode)"
        instructions = QLabel(
            f"Test Mode: {mode_text}\n\n"
            "Test the VenueBrowser placeholder:\n"
            "1. List shows 20+ legendary Grateful Dead venues\n"
            "2. Venues are sorted by show count (if database available)\n"
            "3. Click a venue to test signal emission\n"
            "4. 'Coming Soon' message explains future features\n"
            "5. All styling uses Theme Manager constants"
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

        # VenueBrowser widget
        db_path = "data/shows.db" if with_database else None
        self.venue_browser = VenueBrowser(db_path=db_path)
        self.venue_browser.venue_selected.connect(self.on_venue_selected)
        layout.addWidget(self.venue_browser)

        # Result label
        self.result_label = QLabel("Click a venue to see signal emission")
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

        print("[INFO] VenueBrowser test window initialized")
        print(f"[INFO] Mode: {mode_text}")
        print("[INFO] Verify the following:")
        print("  - Header uses Theme.HEADER_MEDIUM")
        print("  - Description uses Theme.TEXT_SECONDARY")
        print("  - Venue list uses Theme.BG_CARD")
        print("  - List items are 60px+ tall (touch-friendly)")
        print("  - Selected items use Theme.ACCENT_BLUE")
        print("  - 'Coming Soon' box uses Theme.BG_PANEL_DARK with blue border")

    def on_venue_selected(self, venue_name):
        """Handle venue selection"""
        self.result_label.setText(f"Venue Selected: {venue_name}")
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
        print(f"[PASS] Venue selected signal received: {venue_name}")
        print(f"[INFO] Parent screen would now trigger search for shows at: {venue_name}")


def run_test():
    """Run the VenueBrowser placeholder test"""
    print("\n" + "="*60)
    print("VenueBrowser Widget Placeholder Test - Phase 10E.4")
    print("="*60)

    # Check for database
    db_exists = os.path.exists("data/shows.db")
    if db_exists:
        print("[INFO] Database found - will show venues with show counts")
        with_db = True
    else:
        print("[WARN] Database not found - will show venues without counts")
        with_db = False

    app = QApplication(sys.argv)

    # Apply global theme
    app.setStyleSheet(Theme.get_global_stylesheet())
    print("[PASS] Applied Theme.get_global_stylesheet()")

    # Create test window
    window = TestWindow(with_database=with_db)
    window.show()
    print("[PASS] Test window displayed")

    # Manual test checklist
    print("\n" + "="*60)
    print("MANUAL TEST CHECKLIST:")
    print("="*60)
    print("[   ] 1. Header displays 'Browse by Venue'")
    print("[   ] 2. Description text is readable and informative")
    print("[   ] 3. Venue list shows 20+ legendary venues")
    if with_db:
        print("[   ] 4. Venues show count (e.g., 'Fillmore West (57 shows)')")
        print("[   ] 5. Venues sorted by show count (most first)")
    else:
        print("[   ] 4. Venues listed alphabetically (no counts)")
    print("[   ] 6. List items are touch-friendly (60px+ tall)")
    print("[   ] 7. Hover state shows visual feedback")
    print("[   ] 8. Selected items highlight in blue")
    print("[   ] 9. 'Coming Soon' box displays future features")
    print("[   ] 10. All colors use Theme Manager constants")
    print("[   ] 11. Clicking venue emits signal (check result label)")
    print("[   ] 12. No hardcoded colors or sizes visible")
    print("="*60)
    print("\nClick on venues to test signal emission.")
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
