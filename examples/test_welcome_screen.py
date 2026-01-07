#!/usr/bin/env python3
"""
Test script for restyled Welcome Screen.

Tests:
1. Visual appearance (gradient background, centered layout)
2. Button functionality (all signals work)
3. Component library integration (PillButton, IconButton, Theme)
4. Touch-friendly sizing (60px+ targets)

Run on Raspberry Pi for full visual validation.
"""
import sys
import os

# Add project root to path (works on both macOS and Linux)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

from src.ui.screens.welcome_screen import WelcomeScreen


def main():
    """Run welcome screen test"""
    app = QApplication(sys.argv)
    
    print("=" * 60)
    print("DeadStream Welcome Screen Test")
    print("=" * 60)
    print()
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("DeadStream - Welcome Screen Test")
    window.resize(1024, 600)
    
    # Create welcome screen
    welcome = WelcomeScreen()
    window.setCentralWidget(welcome)
    
    # Connect signals for testing
    def on_browse():
        print("[PASS] Browse signal received!")
        print("       --> Would navigate to browse screen")
    
    def on_random():
        print("[PASS] Random show signal received!")
        print("       --> Would start random show playback")
    
    def on_settings():
        print("[PASS] Settings signal received!")
        print("       --> Would navigate to settings screen")
    
    welcome.browse_requested.connect(on_browse)
    welcome.random_show_requested.connect(on_random)
    welcome.settings_requested.connect(on_settings)
    
    # Show window
    window.show()
    
    # Print test instructions
    print("[INFO] Welcome Screen Test Running")
    print()
    print("Visual Checks:")
    print("  1. Purple gradient background (deep purple)")
    print("  2. Centered 'DeadStream' title (large, white, bold)")
    print("  3. Subtitle 'Grateful Dead Concert Player' (gray)")
    print("  4. Settings icon in top-right corner (transparent)")
    print("  5. Two centered buttons:")
    print("     - 'Find a Show' (blue)")
    print("     - 'Random Show' (gradient purple-to-blue)")
    print()
    print("Interaction Checks:")
    print("  - Click 'Find a Show' button")
    print("  - Click 'Random Show' button")
    print("  - Click settings icon (gear)")
    print()
    print("Size Checks:")
    print("  - Buttons should be at least 60px tall")
    print("  - Settings icon should be 60x60px")
    print("  - All touch targets easy to tap")
    print()
    print("Close window to end test.")
    print()
    
    # Auto-close after 60 seconds (optional)
    # QTimer.singleShot(60000, app.quit)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()