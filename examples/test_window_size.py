#!/usr/bin/env python3
"""
Quick diagnostic to check window sizing
"""
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from src.ui.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()

def check_sizes():
    print("\n" + "=" * 70)
    print("WINDOW SIZE DIAGNOSTIC")
    print("=" * 70)
    print(f"Window size: {window.width()}x{window.height()}")
    print(f"Window position: ({window.x()}, {window.y()})")
    print(f"Window geometry: {window.geometry()}")
    print(f"Screen size: {app.primaryScreen().size()}")
    print(f"Screen available: {app.primaryScreen().availableGeometry()}")

    print("\n" + "-" * 70)
    print("SCREEN SIZES")
    print("-" * 70)
    current = window.screen_manager.currentWidget()
    print(f"Current screen: {type(current).__name__}")
    print(f"  Size: {current.width()}x{current.height()}")
    print(f"  Minimum size: {current.minimumSize()}")
    print(f"  Maximum size: {current.maximumSize()}")
    print(f"  Size policy: {current.sizePolicy().horizontalPolicy()}, {current.sizePolicy().verticalPolicy()}")

    print("\n" + "-" * 70)
    print("ALL SCREENS")
    print("-" * 70)
    for name, screen in [('player', window.player_screen), ('browse', window.browse_screen), ('settings', window.settings_screen)]:
        print(f"{name}: {screen.width()}x{screen.height()}")

    print("\n" + "=" * 70)
    if window.width() == 1280 and window.height() == 720:
        print("[PASS] Window is correctly sized at 1280x720")
    else:
        print(f"[FAIL] Window is {window.width()}x{window.height()} instead of 1280x720")
    print("=" * 70)

    # Keep window open for inspection
    print("\nWindow is open for inspection. Close window to exit.")

# Check sizes after window is shown and settled
QTimer.singleShot(500, check_sizes)

sys.exit(app.exec_())
