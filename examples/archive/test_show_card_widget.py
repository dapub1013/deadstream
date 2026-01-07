#!/usr/bin/env python3
"""
Test script for Phase 10A ShowCard widget

Tests all features:
- Basic initialization
- Loading show data
- Quality badge color coding (Soundboard/9.0+/8.0+)
- Mode switching (default/random/date_selected)
- Fade-in animation
- Loading state with spinner
- Error state
- Signal emissions

Usage:
    python3 examples/test_show_card_widget.py
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer
from src.ui.widgets.show_card import ShowCard
from src.ui.styles.button_styles import BG_BLACK, TEXT_WHITE


def run_tests():
    """Run comprehensive tests of ShowCard widget"""

    app = QApplication(sys.argv)

    # Test window
    window = QWidget()
    window.setWindowTitle("ShowCard Widget Test - Phase 10A")
    window.setGeometry(100, 100, 1280, 720)
    window.setStyleSheet(f"background-color: {BG_BLACK};")

    main_layout = QVBoxLayout(window)

    # Title
    title = QLabel("ShowCard Widget Tests")
    title.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 24px; font-weight: bold;")
    main_layout.addWidget(title)

    # ShowCard widget
    card = ShowCard()
    main_layout.addWidget(card)

    # Test buttons
    button_layout = QHBoxLayout()

    # Test data samples with multi-set setlists
    soundboard_show = {
        'identifier': 'gd1977-05-08.sbd.smith.97',
        'date': '1977-05-08',
        'venue': 'Barton Hall, Cornell University',
        'city': 'Ithaca',
        'state': 'NY',
        'recording_score': 9.5,
        'setlist': 'New Minglewood Blues, Loser, El Paso, They Love Each Other, Jack Straw, Deal, Lazy Lightning > Supplication; Scarlet Begonias > Fire on the Mountain, Estimated Prophet, St. Stephen > Not Fade Away > St. Stephen, Morning Dew; One More Saturday Night'
    }

    excellent_show = {
        'identifier': 'gd1972-05-03.aud.bertha.123',
        'date': '1972-05-03',
        'venue': 'Olympia Theatre',
        'city': 'Paris',
        'state': 'France',
        'recording_score': 9.2,
        'setlist': 'Bertha > Me and My Uncle, Mr. Charlie, Loser, Beat It On Down The Line, Sugaree, Jack Straw; China Cat Sunflower > I Know You Rider, Playing in the Band, Turn On Your Love Light; Casey Jones'
    }

    good_show = {
        'identifier': 'gd1974-06-16.aud.unknown',
        'date': '1974-06-16',
        'venue': 'Iowa State Fairgrounds',
        'city': 'Des Moines',
        'state': 'IA',
        'recording_score': 8.3,
        'setlist': 'U.S. Blues, Promised Land, Sugaree, Mexicali Blues, Tennessee Jed, El Paso; Row Jimmy, Big River, Ship of Fools, Playing in the Band'
    }

    # Button handlers
    def test_soundboard():
        print("[TEST] Loading soundboard show...")
        card.show_loading()
        QTimer.singleShot(1000, lambda: card.fade_in(soundboard_show))
        QTimer.singleShot(1500, lambda: card.set_mode('default'))

    def test_excellent():
        print("[TEST] Loading excellent quality show...")
        card.show_loading()
        QTimer.singleShot(1000, lambda: card.fade_in(excellent_show))
        QTimer.singleShot(1500, lambda: card.set_mode('random'))

    def test_good():
        print("[TEST] Loading good quality show...")
        card.show_loading()
        QTimer.singleShot(1000, lambda: card.fade_in(good_show))
        QTimer.singleShot(1500, lambda: card.set_mode('date_selected'))

    def test_loading():
        print("[TEST] Showing loading state...")
        card.show_loading()

    def test_error():
        print("[TEST] Showing error state...")
        card.show_error("No shows found matching criteria")

    # Signal handlers
    def on_play_clicked(identifier):
        print(f"[SIGNAL] play_clicked emitted: {identifier}")

    def on_try_another_clicked():
        print("[SIGNAL] try_another_clicked emitted")
        test_excellent()  # Load a new random show

    # Connect signals
    card.play_clicked.connect(on_play_clicked)
    card.try_another_clicked.connect(on_try_another_clicked)

    # Create test buttons
    btn_soundboard = QPushButton("Test Soundboard (Gold Badge)")
    btn_soundboard.clicked.connect(test_soundboard)
    button_layout.addWidget(btn_soundboard)

    btn_excellent = QPushButton("Test Excellent (Green Badge)")
    btn_excellent.clicked.connect(test_excellent)
    button_layout.addWidget(btn_excellent)

    btn_good = QPushButton("Test Good (Blue Badge)")
    btn_good.clicked.connect(test_good)
    button_layout.addWidget(btn_good)

    btn_loading = QPushButton("Test Loading")
    btn_loading.clicked.connect(test_loading)
    button_layout.addWidget(btn_loading)

    btn_error = QPushButton("Test Error")
    btn_error.clicked.connect(test_error)
    button_layout.addWidget(btn_error)

    main_layout.addLayout(button_layout)

    # Instructions
    instructions = QLabel(
        "Click buttons to test different states.\n"
        "In 'random' mode, the 'Try Another' button should be visible.\n"
        "Click PLAY to test play_clicked signal.\n"
        "Click Try Another to test try_another_clicked signal."
    )
    instructions.setStyleSheet(f"color: {TEXT_WHITE}; font-size: 14px;")
    instructions.setWordWrap(True)
    main_layout.addWidget(instructions)

    # Start with soundboard show
    print("[INFO] Starting ShowCard widget test")
    print("[INFO] Testing initial load with soundboard show...")
    test_soundboard()

    window.show()

    # Print test summary
    print("\n[INFO] ShowCard Widget Test Suite")
    print("[INFO] ================================")
    print("[PASS] Widget initialization")
    print("[INFO] Manual tests available:")
    print("  - Soundboard badge (gold/yellow)")
    print("  - Excellent badge (green, 9.0+)")
    print("  - Good badge (blue, 8.0+)")
    print("  - Loading state with spinner")
    print("  - Error state")
    print("  - Fade-in animation (400ms)")
    print("  - Mode switching (Try Another button visibility)")
    print("  - Signal emissions (play_clicked, try_another_clicked)")
    print("[INFO] Use UI buttons to test each feature")

    return app.exec_()


if __name__ == '__main__':
    sys.exit(run_tests())
