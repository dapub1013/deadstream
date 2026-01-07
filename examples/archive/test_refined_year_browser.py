#!/usr/bin/env python3
"""
Visual test of the refined year browser.
Shows the simplified interface with:
- No "Show All Years" button
- Larger year font (32pt)
- No show counts
- No stars on legendary years
- Hidden buttons for years without shows
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from src.ui.screens.browse_screen import BrowseScreen

print("="*70)
print("Refined Year Browser Test")
print("="*70)
print("\nRefinements:")
print("1. Removed 'Show All Years' green button")
print("2. Enlarged year font to 32pt (was 18pt)")
print("3. Removed '(X shows)' text from buttons")
print("4. Removed stars from legendary years")
print("5. Hidden buttons for years without shows (e.g., 1960)")
print("\nLegendary years still shown in GOLD:")
print("  1968, 1969, 1972, 1973, 1974, 1977, 1989, 1990")
print("Regular years shown in BLUE")
print("="*70 + "\n")

print("Instructions:")
print("1. Click 'Browse by Year' button on the left")
print("2. Year browser appears on right with simplified buttons")
print("3. Try navigating to 1960s - years without shows are hidden")
print("4. Navigate to 1970s - see legendary years in gold (no stars)")
print("5. Click any year to see shows from that year")
print("="*70 + "\n")

app = QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background-color: #000000;
        color: #f3f4f6;
    }
""")

browse_screen = BrowseScreen()
browse_screen.setWindowTitle("Test: Refined Year Browser")
browse_screen.setGeometry(100, 100, 1280, 720)
browse_screen.show()

# Auto-navigate to year browser for convenience
browse_screen.show_year_browser()

sys.exit(app.exec_())
