#!/usr/bin/env python3
"""Quick visual test - click Browse by Year to see inline view"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from src.ui.screens.browse_screen import BrowseScreen

print("="*70)
print("Quick Test: Browse by Year - Inline Interface")
print("="*70)
print("\nInstructions:")
print("1. Click 'Browse by Year' button on the left panel")
print("2. Year browser will appear on the right side (NOT in a dialog)")
print("3. Navigate decades using Previous/Next buttons")
print("4. Click any year to load shows from that year")
print("5. Show list will appear with selected year's shows")
print("\nLegendary years (gold): 1968, 1969, 1972-1974, 1977, 1989-1990")
print("="*70 + "\n")

app = QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background-color: #000000;
        color: #f3f4f6;
    }
""")

browse_screen = BrowseScreen()
browse_screen.setWindowTitle("Test: Browse by Year (Inline)")
browse_screen.setGeometry(100, 100, 1280, 720)
browse_screen.show()

sys.exit(app.exec_())
