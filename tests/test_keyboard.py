#!/usr/bin/env python3
"""
Test keyboard input handling for DeadStream UI
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from src.ui.main_window import MainWindow


def test_keyboard_shortcuts():
    """Test basic keyboard shortcuts"""
    print("\n" + "="*60)
    print("DeadStream Keyboard Input Test")
    print("="*60)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    print("\n[INFO] Main window created and displayed")
    print("[INFO] Testing keyboard shortcuts...")
    print("\nPress these keys to test:")
    print("  - Arrow keys (Up/Down/Left/Right)")
    print("  - Space (Play/Pause)")
    print("  - N (Next), P (Previous)")
    print("  - +/- (Volume)")
    print("  - M (Menu)")
    print("  - ESC (Back)")
    print("  - Q (Quit)")
    print("\nWatch the console for keyboard event messages")
    print("\n" + "="*60)
    
    # Start the application
    sys.exit(app.exec_())


if __name__ == '__main__':
    test_keyboard_shortcuts()