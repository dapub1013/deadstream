#!/usr/bin/env python3
"""
Diagnostic test for browse_screen.py
Shows import errors and helps debug issues
"""

import sys
import os

# Add project root to path
# This script is in examples/, so go up one level to get to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

print("=" * 60)
print("BROWSE SCREEN DIAGNOSTIC TEST")
print("=" * 60)
print(f"Project root: {PROJECT_ROOT}")
print(f"Python path: {sys.path[0]}")
print()

# Test imports one by one
print("Testing imports...")
print("-" * 60)

try:
    from PyQt5.QtWidgets import QApplication
    print("[OK] PyQt5.QtWidgets")
except ImportError as e:
    print(f"[FAIL] PyQt5.QtWidgets: {e}")
    print("\nInstall PyQt5 with: pip3 install PyQt5")
    sys.exit(1)

try:
    from src.database.queries import get_top_rated_shows, search_by_year
    print("[OK] Database queries")
except ImportError as e:
    print(f"[FAIL] Database queries: {e}")
    sys.exit(1)

try:
    from src.ui.widgets.show_list import ShowListWidget
    print("[OK] ShowListWidget")
except ImportError as e:
    print(f"[FAIL] ShowListWidget: {e}")
    print("\nMake sure src/ui/widgets/show_list.py exists")
    sys.exit(1)

try:
    from src.ui.widgets.date_browser import DateBrowser
    print("[OK] DateBrowser")
except ImportError as e:
    print(f"[FAIL] DateBrowser: {e}")
    print("\nMake sure src/ui/widgets/date_browser.py exists")
    sys.exit(1)

try:
    from src.ui.widgets.year_browser import YearBrowser
    print("[OK] YearBrowser")
except ImportError as e:
    print(f"[FAIL] YearBrowser: {e}")
    print("\nMake sure src/ui/widgets/year_browser.py exists")
    print("Copy from: cp ~/Downloads/year_browser.py src/ui/widgets/")
    sys.exit(1)

print()
print("All imports successful!")
print("-" * 60)
print()

# Try to create the browse screen
print("Creating BrowseScreen widget...")
try:
    from src.ui.screens.browse_screen import BrowseScreen
    
    app = QApplication(sys.argv)
    
    screen = BrowseScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("Browse Screen Test - Task 7.4")
    
    print("[OK] BrowseScreen created successfully")
    print()
    print("Displaying window...")
    print("(Close the window to exit)")
    print()
    
    screen.show()
    
    sys.exit(app.exec_())
    
except Exception as e:
    print(f"[FAIL] Error creating BrowseScreen: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
