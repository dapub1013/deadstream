#!/usr/bin/env python3
"""
Test script for Year Browser integration (Task 7.4)

Tests:
1. YearBrowser widget standalone
2. Integration with browse_screen
3. Signal connections
4. Database queries

Usage:
    python3 examples/test_year_browser.py
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

# Import components to test
from src.ui.widgets.year_browser import YearBrowser
from src.ui.screens.browse_screen import BrowseScreen
from src.database.queries import search_by_year, get_years_with_shows, get_show_count_by_year


def test_database_functions():
    """Test that database functions work correctly"""
    print("\n" + "=" * 70)
    print("TEST 1: Database Functions")
    print("=" * 70)
    
    # Test get_years_with_shows
    print("\n[TEST] Getting years with shows...")
    years = get_years_with_shows()
    print(f"[OK] Found {len(years)} years with shows")
    print(f"[INFO] Year range: {min(years)} to {max(years)}")
    
    # Test get_show_count_by_year
    print("\n[TEST] Getting show counts by year...")
    year_counts = get_show_count_by_year()
    print(f"[OK] Got counts for {len(year_counts)} years")
    
    # Find top 5 years by show count
    top_years = sorted(year_counts, key=lambda x: x[1], reverse=True)[:5]
    print("\n[INFO] Top 5 years by show count:")
    for year, count in top_years:
        print(f"  {year}: {count} shows")
    
    # Test search_by_year for a legendary year
    print("\n[TEST] Testing search_by_year(1977)...")
    shows_1977 = search_by_year(1977)
    print(f"[OK] Found {len(shows_1977)} shows from 1977")
    if shows_1977:
        print(f"[INFO] First show: {shows_1977[0]['date']} at {shows_1977[0]['venue']}")
        print(f"[INFO] Last show: {shows_1977[-1]['date']} at {shows_1977[-1]['venue']}")
    
    print("\n[PASS] All database tests passed")


def test_year_browser_widget(app):
    """Test YearBrowser widget standalone"""
    print("\n" + "=" * 70)
    print("TEST 2: YearBrowser Widget Standalone")
    print("=" * 70)
    
    # Create window
    window = QMainWindow()
    window.setWindowTitle("YearBrowser Widget Test")
    window.setGeometry(100, 100, 800, 700)
    
    # Create year browser
    year_browser = YearBrowser()
    
    # Connect signal to test
    def on_year_selected(year):
        print(f"\n[SIGNAL] year_selected emitted: {year}")
        shows = search_by_year(year)
        print(f"[INFO] This year has {len(shows)} shows")
    
    year_browser.year_selected.connect(on_year_selected)
    
    window.setCentralWidget(year_browser)
    
    print("\n[INFO] YearBrowser widget created")
    print("[INFO] Test the following:")
    print("  1. Click previous/next decade buttons")
    print("  2. Click 'Show All Years' button")
    print("  3. Click a year with shows (blue or gold)")
    print("  4. Verify legendary years are gold (1977, 1972, etc.)")
    print("  5. Verify disabled years are grayed out")
    
    return window


def test_browse_screen_integration(app):
    """Test YearBrowser integration in browse_screen"""
    print("\n" + "=" * 70)
    print("TEST 3: Browse Screen Integration")
    print("=" * 70)
    
    # Create browse screen
    browse_screen = BrowseScreen()
    browse_screen.setWindowTitle("Browse Screen - Year Browser Integration")
    browse_screen.setGeometry(100, 100, 1280, 720)
    
    # Connect show_selected signal
    def on_show_selected(show):
        print(f"\n[SIGNAL] show_selected emitted:")
        print(f"  Date: {show['date']}")
        print(f"  Venue: {show['venue']}")
        print(f"  Identifier: {show['identifier']}")
    
    browse_screen.show_selected.connect(on_show_selected)
    
    print("\n[INFO] Browse screen created with year browser")
    print("[INFO] Test the following:")
    print("  1. Click 'Browse by Year' button (purple)")
    print("  2. Year browser dialog should open")
    print("  3. Select a year")
    print("  4. Dialog should close and shows should load")
    print("  5. Verify header shows correct year and count")
    print("  6. Click a show to verify show_selected signal")
    
    return browse_screen


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("YEAR BROWSER TESTING SUITE - TASK 7.4")
    print("=" * 70)
    
    # Test database functions first (no GUI needed)
    test_database_functions()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Apply dark theme
    app.setStyleSheet("""
        QWidget {
            background-color: #111827;
            color: #f3f4f6;
        }
    """)
    
    # Create tab widget to show both tests
    main_window = QMainWindow()
    main_window.setWindowTitle("Year Browser Tests - Task 7.4")
    main_window.setGeometry(50, 50, 1280, 750)
    
    tabs = QTabWidget()
    
    # Tab 1: Standalone YearBrowser
    year_browser_window = test_year_browser_widget(app)
    tabs.addTab(year_browser_window.centralWidget(), "YearBrowser Widget")
    
    # Tab 2: Browse Screen Integration
    browse_screen = test_browse_screen_integration(app)
    tabs.addTab(browse_screen, "Browse Screen Integration")
    
    main_window.setCentralWidget(tabs)
    main_window.show()
    
    print("\n" + "=" * 70)
    print("TESTING INSTRUCTIONS")
    print("=" * 70)
    print("\nSwitch between tabs to test different components:")
    print("\nTab 1 - YearBrowser Widget:")
    print("  - Test navigation between decades")
    print("  - Verify legendary years are highlighted in gold")
    print("  - Click years to emit signals")
    print("\nTab 2 - Browse Screen Integration:")
    print("  - Click 'Browse by Year' (purple button)")
    print("  - Select a year from dialog")
    print("  - Verify shows load correctly")
    print("  - Check that legendary years show special formatting")
    print("\n[INFO] Close window or press Ctrl+C to exit")
    print("=" * 70)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
