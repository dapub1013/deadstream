#!/usr/bin/env python3
"""
Test script for About Widget
Tests the About page independently before integration
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from about_widget import AboutWidget


def main():
    """Test the About widget"""
    print("[INFO] Starting About Widget test...")
    
    app = QApplication(sys.argv)
    
    # Create widget
    widget = AboutWidget()
    widget.setWindowTitle("About Widget - DeadStream")
    widget.setGeometry(100, 100, 700, 800)
    widget.setStyleSheet("background-color: #000000;")
    
    print("[INFO] About widget created")
    print("[INFO] Window size: 700x800")
    print("[INFO] Testing features:")
    print("  - Application information display")
    print("  - Database statistics")
    print("  - Credits section")
    print("  - Legal notice")
    print("  - Scrollable content area")
    print()
    print("[INFO] Visual Test Checklist:")
    print("  [ ] Title 'About' visible at top")
    print("  [ ] Subtitle 'Device information and version' visible")
    print("  [ ] Application info card shows version 1.0.0")
    print("  [ ] Database statistics card shows show count")
    print("  [ ] Credits card lists Internet Archive and tapers")
    print("  [ ] Legal notice card shows license information")
    print("  [ ] Content is scrollable if needed")
    print("  [ ] All text is readable (white on dark background)")
    print("  [ ] Cards have proper spacing and padding")
    print()
    print("[INFO] Displaying widget...")
    
    widget.show()
    
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
