#!/usr/bin/env python3
"""
Test script for the new DateSelectorWidget integration.
Verifies that the date selector loads properly and can switch to show lists.
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from src.ui.screens.browse_screen import BrowseScreen


def test_date_selector_integration():
    """Test that date selector widget integrates properly with browse screen"""
    print("\n" + "="*70)
    print("Testing Date Selector Integration")
    print("="*70)

    app = QApplication(sys.argv)

    # Create browse screen
    browse_screen = BrowseScreen()
    browse_screen.setGeometry(100, 100, 1280, 720)
    browse_screen.show()

    QTest.qWait(500)  # Wait for initial load

    # Test 1: Verify initial state is show list (page 0)
    print("\n[TEST 1] Verify initial state")
    if browse_screen.content_stack.currentIndex() == 0:
        print("[PASS] Initial state is show list view")
    else:
        print(f"[FAIL] Expected page 0, got {browse_screen.content_stack.currentIndex()}")
        return False

    # Test 2: Switch to date selector
    print("\n[TEST 2] Switch to date selector")
    browse_screen.show_date_browser()
    QTest.qWait(200)

    if browse_screen.content_stack.currentIndex() == 2:
        print("[PASS] Switched to date selector view (page 2)")
    else:
        print(f"[FAIL] Expected page 2, got {browse_screen.content_stack.currentIndex()}")
        return False

    # Test 3: Verify date selector widget exists and has data
    print("\n[TEST 3] Verify date selector widget")
    if hasattr(browse_screen, 'date_selector_widget'):
        print("[PASS] Date selector widget exists")
    else:
        print("[FAIL] Date selector widget not found")
        return False

    # Check that years loaded
    year_count = browse_screen.date_selector_widget.year_list.count()
    print(f"[INFO] Year list has {year_count} items")
    if year_count > 0:
        print(f"[PASS] Years loaded ({year_count} years)")
    else:
        print("[FAIL] No years loaded")
        return False

    # Test 4: Verify month and day lists are initially empty
    print("\n[TEST 4] Verify initial empty state of month/day")
    month_count = browse_screen.date_selector_widget.month_list.count()
    day_count = browse_screen.date_selector_widget.day_list.count()

    if month_count == 0 and day_count == 0:
        print("[PASS] Month and day lists are initially empty")
    else:
        print(f"[FAIL] Month list: {month_count}, Day list: {day_count}")
        return False

    # Test 5: Select a year and verify months load
    print("\n[TEST 5] Select year and verify months load")
    # Select the first year (most recent)
    first_year_item = browse_screen.date_selector_widget.year_list.item(0)
    browse_screen.date_selector_widget.year_list.setCurrentItem(first_year_item)
    browse_screen.date_selector_widget.on_year_selected(first_year_item)
    QTest.qWait(200)

    month_count = browse_screen.date_selector_widget.month_list.count()
    if month_count > 0:
        print(f"[PASS] Months loaded after year selection ({month_count} months)")
    else:
        print("[FAIL] No months loaded after year selection")
        return False

    # Test 6: Select a month and verify days load
    print("\n[TEST 6] Select month and verify days load")
    first_month_item = browse_screen.date_selector_widget.month_list.item(0)
    browse_screen.date_selector_widget.month_list.setCurrentItem(first_month_item)
    browse_screen.date_selector_widget.on_month_selected(first_month_item)
    QTest.qWait(200)

    day_count = browse_screen.date_selector_widget.day_list.count()
    if day_count > 0:
        print(f"[PASS] Days loaded after month selection ({day_count} days)")
    else:
        print("[FAIL] No days loaded after month selection")
        return False

    # Test 7: Select a day and verify button is enabled
    print("\n[TEST 7] Select day and verify select button")
    first_day_item = browse_screen.date_selector_widget.day_list.item(0)
    browse_screen.date_selector_widget.day_list.setCurrentItem(first_day_item)
    browse_screen.date_selector_widget.on_day_selected(first_day_item)
    QTest.qWait(200)

    if browse_screen.date_selector_widget.select_button.isEnabled():
        print("[PASS] Select button is enabled after full date selection")
    else:
        print("[FAIL] Select button is not enabled")
        return False

    # Test 8: Click select button and verify switch to show list
    print("\n[TEST 8] Click select and verify switch to show list")

    # Track when we switch pages
    switched = [False]

    def on_stack_changed():
        switched[0] = True

    browse_screen.content_stack.currentChanged.connect(on_stack_changed)

    # Click the select button
    QTest.mouseClick(browse_screen.date_selector_widget.select_button, Qt.LeftButton)
    QTest.qWait(500)  # Wait for shows to load

    if browse_screen.content_stack.currentIndex() == 0:
        print("[PASS] Switched back to show list view after date selection")
    else:
        print(f"[FAIL] Expected page 0, got {browse_screen.content_stack.currentIndex()}")
        return False

    # Test 9: Verify shows were loaded for the selected date
    print("\n[TEST 9] Verify shows loaded")
    show_count = browse_screen.show_list.list_widget.count()
    if show_count > 0:
        print(f"[PASS] Shows loaded for selected date ({show_count} shows)")
    else:
        print("[FAIL] No shows loaded for selected date")
        return False

    # Test 10: Verify header updated
    print("\n[TEST 10] Verify header updated")
    header_text = browse_screen.header_title.text()
    if "Shows on" in header_text:
        print(f"[PASS] Header updated: {header_text}")
    else:
        print(f"[FAIL] Header not updated properly: {header_text}")
        return False

    print("\n" + "="*70)
    print("[SUCCESS] All date selector integration tests passed!")
    print("="*70 + "\n")

    browse_screen.close()
    return True


if __name__ == "__main__":
    success = test_date_selector_integration()
    sys.exit(0 if success else 1)
