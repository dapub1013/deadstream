#!/usr/bin/env python3
"""
Test script for restyled ShowCard widget.
Verifies that Theme Manager integration works correctly.

Phase 10E - Task 10E.3: Show Card Restyle
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer

from src.ui.widgets.show_card import ShowCard
from src.ui.styles.theme import Theme


class TestWindow(QMainWindow):
    """Test window for ShowCard widget"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShowCard Restyle Test - Phase 10E.3")
        self.setGeometry(100, 100, 900, 800)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Header
        header = QLabel("ShowCard Widget - Theme Manager Integration Test")
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
            "Test the restyled ShowCard:\n"
            "1. Click 'Load Show' to see card with Theme colors\n"
            "2. Check quality badge uses Theme accent colors\n"
            "3. Verify buttons use Theme.get_button_style()\n"
            "4. Test 'Try Another' button visibility in random mode\n"
            "5. Click PLAY to test signal emission"
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

        # Control buttons
        button_layout = QVBoxLayout()
        button_layout.setSpacing(Theme.SPACING_SMALL)

        self.load_button = QPushButton("Load Show (Soundboard)")
        self.load_button.setStyleSheet(Theme.get_button_style(Theme.ACCENT_BLUE))
        self.load_button.setMinimumHeight(Theme.BUTTON_HEIGHT_SMALL)
        self.load_button.clicked.connect(self.load_soundboard_show)
        button_layout.addWidget(self.load_button)

        self.load_excellent_button = QPushButton("Load Excellent Show (9.0+)")
        self.load_excellent_button.setStyleSheet(Theme.get_button_style(Theme.ACCENT_GREEN))
        self.load_excellent_button.setMinimumHeight(Theme.BUTTON_HEIGHT_SMALL)
        self.load_excellent_button.clicked.connect(self.load_excellent_show)
        button_layout.addWidget(self.load_excellent_button)

        self.load_good_button = QPushButton("Load Good Show (8.0+)")
        self.load_good_button.setStyleSheet(Theme.get_button_style(Theme.ACCENT_YELLOW, Theme.TEXT_DARK))
        self.load_good_button.setMinimumHeight(Theme.BUTTON_HEIGHT_SMALL)
        self.load_good_button.clicked.connect(self.load_good_show)
        button_layout.addWidget(self.load_good_button)

        self.toggle_mode_button = QPushButton("Toggle Random Mode (Show/Hide Try Another)")
        self.toggle_mode_button.setStyleSheet(Theme.get_button_style(Theme.BORDER_SUBTLE))
        self.toggle_mode_button.setMinimumHeight(Theme.BUTTON_HEIGHT_SMALL)
        self.toggle_mode_button.clicked.connect(self.toggle_mode)
        button_layout.addWidget(self.toggle_mode_button)

        layout.addLayout(button_layout)

        # ShowCard widget
        self.show_card = ShowCard()
        self.show_card.play_clicked.connect(self.on_play_clicked)
        self.show_card.try_another_clicked.connect(self.on_try_another_clicked)
        layout.addWidget(self.show_card)

        # Result label
        self.result_label = QLabel("No actions yet")
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

        self.current_mode = 'default'

        print("[INFO] ShowCard test window initialized")
        print("[INFO] Verify the following:")
        print("  - Card uses Theme.BG_CARD for background")
        print("  - Date uses Theme.HEADER_LARGE (48px)")
        print("  - Venue uses Theme.HEADER_SMALL (24px)")
        print("  - Quality badges use Theme.ACCENT_* colors")
        print("  - PLAY button uses Theme.ACCENT_RED")
        print("  - Try Another button uses Theme.BORDER_SUBTLE")

    def load_soundboard_show(self):
        """Load a soundboard show"""
        show_data = {
            'identifier': 'gd1977-05-08.sbd.smith.97.sbeok.flac16',
            'date': '1977-05-08',
            'venue': 'Barton Hall, Cornell University',
            'city': 'Ithaca',
            'state': 'NY',
            'recording_score': 9.5,
            'setlist': 'New Minglewood Blues, Loser, El Paso, They Love Each Other, Jack Straw, Deal; Scarlet Begonias > Fire on the Mountain, Estimated Prophet, St. Stephen > Not Fade Away > St. Stephen, Morning Dew; One More Saturday Night'
        }
        self.show_card.show_loading()
        QTimer.singleShot(500, lambda: self.show_card.fade_in(show_data))
        self.result_label.setText("Loaded: Cornell '77 (Soundboard - should be YELLOW badge)")
        print("[PASS] Loaded soundboard show")

    def load_excellent_show(self):
        """Load an excellent-rated show"""
        show_data = {
            'identifier': 'gd1972-09-24.aud.smith.flac16',
            'date': '1972-09-24',
            'venue': 'Palace Theater',
            'city': 'Waterbury',
            'state': 'CT',
            'recording_score': 9.2,
            'setlist': 'Greatest Story Ever Told, Sugaree, Me and My Uncle, Mexicali Blues, Deal; China Cat Sunflower > I Know You Rider, Big River, Tennessee Jed, Playing in the Band; Johnny B. Goode'
        }
        self.show_card.show_loading()
        QTimer.singleShot(500, lambda: self.show_card.fade_in(show_data))
        self.result_label.setText("Loaded: Waterbury '72 (Excellent 9.2 - should be GREEN badge)")
        print("[PASS] Loaded excellent show")

    def load_good_show(self):
        """Load a good-rated show"""
        show_data = {
            'identifier': 'gd1980-12-28.aud.flac16',
            'date': '1980-12-28',
            'venue': 'Oakland Auditorium Arena',
            'city': 'Oakland',
            'state': 'CA',
            'recording_score': 8.3,
            'setlist': 'Feel Like a Stranger, Althea, Little Red Rooster, Cassidy, Deal; Lost Sailor > Saint of Circumstance, Terrapin Station > Drums > Not Fade Away > Black Peter > Around and Around; U.S. Blues'
        }
        self.show_card.show_loading()
        QTimer.singleShot(500, lambda: self.show_card.fade_in(show_data))
        self.result_label.setText("Loaded: Oakland '80 (Very Good 8.3 - should be BLUE badge)")
        print("[PASS] Loaded good show")

    def toggle_mode(self):
        """Toggle between default and random mode"""
        if self.current_mode == 'default':
            self.current_mode = 'random'
            self.show_card.set_mode('random')
            self.result_label.setText("Mode: Random (Try Another button should be VISIBLE)")
            print("[INFO] Switched to random mode")
        else:
            self.current_mode = 'default'
            self.show_card.set_mode('default')
            self.result_label.setText("Mode: Default (Try Another button should be HIDDEN)")
            print("[INFO] Switched to default mode")

    def on_play_clicked(self, identifier):
        """Handle play button click"""
        self.result_label.setText(f"PLAY clicked - Show: {identifier}")
        self.result_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                padding: {Theme.SPACING_MEDIUM}px;
                background-color: {Theme.ACCENT_RED};
                border-radius: 8px;
            }}
        """)
        print(f"[PASS] Play signal received: {identifier}")

        # Reset after 2 seconds
        QTimer.singleShot(2000, self.reset_result_label)

    def on_try_another_clicked(self):
        """Handle try another button click"""
        self.result_label.setText("TRY ANOTHER clicked - Load next random show")
        self.result_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                padding: {Theme.SPACING_MEDIUM}px;
                background-color: {Theme.ACCENT_BLUE};
                border-radius: 8px;
            }}
        """)
        print("[PASS] Try Another signal received")

        # Reset after 2 seconds
        QTimer.singleShot(2000, self.reset_result_label)

    def reset_result_label(self):
        """Reset result label to default style"""
        self.result_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
                padding: {Theme.SPACING_MEDIUM}px;
                background-color: {Theme.BG_CARD};
                border-radius: 8px;
            }}
        """)


def run_test():
    """Run the ShowCard restyle test"""
    print("\n" + "="*60)
    print("ShowCard Widget Restyle Test - Phase 10E.3")
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
    print("[   ] 1. Card background uses Theme.BG_CARD")
    print("[   ] 2. Date label uses Theme.HEADER_LARGE (48px)")
    print("[   ] 3. Venue label uses Theme.HEADER_SMALL (24px)")
    print("[   ] 4. Location uses Theme.TEXT_SECONDARY color")
    print("[   ] 5. Quality badge colors:")
    print("         - Soundboard: Theme.ACCENT_YELLOW (gold)")
    print("         - Excellent (9.0+): Theme.ACCENT_GREEN")
    print("         - Very Good (8.0+): Theme.ACCENT_BLUE")
    print("[   ] 6. Setlist container uses Theme.BG_PANEL_DARK")
    print("[   ] 7. PLAY button uses Theme.ACCENT_RED")
    print("[   ] 8. Try Another button uses Theme.BORDER_SUBTLE")
    print("[   ] 9. Try Another button shows/hides in random mode")
    print("[   ] 10. Buttons use Theme.get_button_style() (hover/pressed states)")
    print("[   ] 11. Loading state uses Theme colors")
    print("[   ] 12. All spacing uses Theme.SPACING_* constants")
    print("[   ] 13. No hardcoded color values visible")
    print("="*60)
    print("\nClick the test buttons to verify functionality.")
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
