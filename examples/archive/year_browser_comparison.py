#!/usr/bin/env python3
"""
Year Browser Refinement Comparison

This script documents the changes made to the year browser interface.
Run this to see the final refined version.
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from src.ui.widgets.year_browser import YearBrowser

print("="*70)
print("Year Browser Refinement - Before vs After")
print("="*70)

print("\n[CHANGE 1] 'Show All Years' Button")
print("  BEFORE: Green button below decade navigation")
print("  AFTER:  Removed completely")

print("\n[CHANGE 2] Year Font Size")
print("  BEFORE: 18pt Arial Bold")
print("  AFTER:  32pt Arial Bold")

print("\n[CHANGE 3] Button Text Content")
print("  BEFORE: '1977\\n(421 shows)'")
print("  AFTER:  '1977'")

print("\n[CHANGE 4] Legendary Year Stars")
print("  BEFORE: 'STAR 1977 STAR\\n(421 shows)'")
print("  AFTER:  '1977' (still gold color)")

print("\n[CHANGE 5] Years Without Shows")
print("  BEFORE: Gray disabled button '1960\\n(no shows)'")
print("  AFTER:  Button hidden completely")

print("\n[CHANGE 6] Legend Section")
print("  BEFORE: 'STAR = Legendary Year' + 'Number shows available'")
print("  AFTER:  Removed completely")

print("\n" + "="*70)
print("RESULT: Cleaner, simpler, more readable interface")
print("="*70)

print("\nLegendary Years (shown in GOLD):")
print("  - 1968, 1969 (Early psychedelic era)")
print("  - 1972, 1973, 1974 (Peak improvisational years)")
print("  - 1977 (The legendary year)")
print("  - 1989, 1990 (Brent era renaissance)")

print("\nRegular Years (shown in BLUE):")
print("  - All other years with shows")

print("\n" + "="*70)
print("Opening year browser widget for visual inspection...")
print("="*70 + "\n")

app = QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background-color: #111827;
        color: #f3f4f6;
    }
""")

year_browser = YearBrowser()

# Connect signal for testing
def on_year_selected(year):
    print(f"\n[INFO] Year {year} selected!")
    from src.database.queries import get_show_count_by_year
    year_counts = dict(get_show_count_by_year())
    show_count = year_counts.get(year, 0)
    is_legendary = year in YearBrowser.LEGENDARY_YEARS
    legendary_text = " (LEGENDARY)" if is_legendary else ""
    print(f"       {show_count} shows from {year}{legendary_text}")

year_browser.year_selected.connect(on_year_selected)

# Start at 1970s to show legendary years
year_browser.current_decade = 1970
year_browser.update_year_grid()

year_browser.setWindowTitle("Refined Year Browser (1970s)")
year_browser.setGeometry(200, 100, 600, 600)
year_browser.show()

print("Instructions:")
print("- Notice large 32pt year numbers")
print("- Gold buttons are legendary years (no stars)")
print("- Blue buttons are regular years")
print("- Navigate to 1960s to see hidden buttons (years without shows)")
print("- Click any year to select it")

sys.exit(app.exec_())
