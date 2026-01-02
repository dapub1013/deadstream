#!/usr/bin/env python3
"""
Test script for year browser integration in browse screen.
Verifies that year browser appears inline on the right panel.
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

print("[INFO] Testing year browser integration...")

# Initialize application
app = QApplication(sys.argv)

# Import browse screen
from src.ui.screens.browse_screen import BrowseScreen

# Create browse screen instance
browse_screen = BrowseScreen()

print("[PASS] Browse screen created successfully")

# Verify content stack has correct number of pages
expected_pages = 4  # 0: list view, 1: random show, 2: date selector, 3: year browser
actual_pages = browse_screen.content_stack.count()

if actual_pages == expected_pages:
    print(f"[PASS] Content stack has {expected_pages} pages")
else:
    print(f"[FAIL] Content stack has {actual_pages} pages, expected {expected_pages}")
    sys.exit(1)

# Verify year browser widget exists
if hasattr(browse_screen, 'year_browser_widget'):
    print("[PASS] year_browser_widget attribute exists")
else:
    print("[FAIL] year_browser_widget attribute missing")
    sys.exit(1)

# Verify initial state (should be on list view - page 0)
initial_index = browse_screen.content_stack.currentIndex()
if initial_index == 0:
    print(f"[PASS] Initial view is list view (page {initial_index})")
else:
    print(f"[FAIL] Initial view is page {initial_index}, expected 0")
    sys.exit(1)

# Simulate clicking "Browse by Year" button
print("\n[INFO] Simulating 'Browse by Year' button click...")
browse_screen.show_year_browser()

# Process events
QTest.qWait(100)

# Verify we switched to year browser view (page 3)
current_index = browse_screen.content_stack.currentIndex()
if current_index == 3:
    print(f"[PASS] Switched to year browser view (page {current_index})")
else:
    print(f"[FAIL] Current view is page {current_index}, expected 3")
    sys.exit(1)

# Verify year browser widget is visible
current_widget = browse_screen.content_stack.currentWidget()
if current_widget == browse_screen.year_browser_widget:
    print("[PASS] Year browser widget is currently visible")
else:
    print("[FAIL] Wrong widget is visible")
    sys.exit(1)

# Verify year browser has loaded data
if len(browse_screen.year_browser_widget.years_with_shows) > 0:
    num_years = len(browse_screen.year_browser_widget.years_with_shows)
    print(f"[PASS] Year browser loaded {num_years} years with shows")
else:
    print("[FAIL] Year browser has no data")
    sys.exit(1)

# Test year selection (simulate clicking 1977)
print("\n[INFO] Testing year selection (1977)...")
browse_screen.year_browser_widget.current_decade = 1970
browse_screen.year_browser_widget.update_year_grid()
QTest.qWait(100)

# Find button for 1977 (should be index 7: 1970, 1971, ..., 1977)
year_1977_button = browse_screen.year_browser_widget.year_buttons[7]
if year_1977_button.property('year') == 1977:
    print("[PASS] Found 1977 button")

    # Simulate click
    year_1977_button.click()
    QTest.qWait(100)

    # Should have switched back to list view (page 0)
    current_index = browse_screen.content_stack.currentIndex()
    if current_index == 0:
        print("[PASS] Switched back to list view after year selection")
    else:
        print(f"[FAIL] Current view is page {current_index}, expected 0")
        sys.exit(1)

    # Verify header was updated
    header_text = browse_screen.header_title.text()
    if "1977" in header_text:
        print(f"[PASS] Header updated: '{header_text}'")
    else:
        print(f"[FAIL] Header not updated: '{header_text}'")
        sys.exit(1)
else:
    print(f"[FAIL] Button 7 has year {year_1977_button.property('year')}, expected 1977")
    sys.exit(1)

print("\n" + "="*60)
print("[PASS] All year browser integration tests passed!")
print("="*60)

sys.exit(0)
