#!/usr/bin/env python3
"""
Test script for Random Show Screen - Phase 10F

Tests the new random show screen in isolation without full app dependencies.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from src.ui.screens.randomshow_screen import RandomShowScreen
from src.ui.styles.theme import Theme


def test_random_show_screen():
    """Test the random show screen"""
    print("\n" + "="*60)
    print("Random Show Screen Test")
    print("="*60)

    app = QApplication(sys.argv)

    # Apply theme
    app.setStyleSheet(f"""
        QWidget {{
            background-color: {Theme.BG_PRIMARY};
            color: {Theme.TEXT_PRIMARY};
        }}
    """)

    # Create random show screen
    screen = RandomShowScreen()
    screen.setGeometry(100, 100, 1280, 720)
    screen.setWindowTitle("DeadStream - Random Show Screen Test")

    # Connect signals for testing
    def on_show_selected(show):
        print(f"\n[TEST] Show selected signal received:")
        print(f"  Date: {show.get('date', 'Unknown')}")
        print(f"  Venue: {show.get('venue', 'Unknown')}")
        print(f"  Location: {show.get('city', 'Unknown')}, {show.get('state', 'Unknown')}")
        if show.get('avg_rating'):
            print(f"  Rating: {show['avg_rating']:.1f}/5.0")

    def on_home_requested():
        print("\n[TEST] Home navigation requested")

    def on_settings_requested():
        print("\n[TEST] Settings navigation requested")

    screen.show_selected.connect(on_show_selected)
    screen.home_requested.connect(on_home_requested)
    screen.settings_requested.connect(on_settings_requested)

    # Show the screen
    screen.show()

    print("\n[INFO] Random Show screen displayed")
    print("[INFO] Testing features:")
    print("  - Random show should load automatically")
    print("  - Click 'Play Show' to test show selection")
    print("  - Click 'Try Again' to load a different show")
    print("  - Click home icon (top-right) to test navigation")
    print("  - Click settings icon (bottom-right) to test navigation")
    print("\n[INFO] Close window to exit test")

    # Auto-close after 30 seconds for automated testing
    def auto_close():
        print("\n[INFO] Auto-closing test after 30 seconds")
        app.quit()

    QTimer.singleShot(30000, auto_close)

    # Run the application
    exit_code = app.exec_()

    print("\n" + "="*60)
    print("Test completed")
    print("="*60)

    return exit_code


if __name__ == "__main__":
    sys.exit(test_random_show_screen())
