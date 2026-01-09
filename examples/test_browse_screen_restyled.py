#!/usr/bin/env python3
"""
Test script for Phase 10D restyled browse screen.

Tests:
- Browse screen with PillButton navigation
- Theme Manager integration
- Show list with ConcertListItem components
- Search widget with Theme styling
- Date browser with Theme styling
- All browse modes functional

Run from project root:
    python3 examples/test_browse_screen_restyled.py
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

# Import Phase 10D restyled components
from src.ui.styles.theme import Theme
from src.ui.screens.browse_screen import BrowseScreen


class TestWindow(QMainWindow):
    """Test window for browse screen"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phase 10D Browse Screen Test - Restyled with Theme Manager")
        self.setGeometry(100, 100, 1280, 720)
        
        # Create browse screen
        self.browse_screen = BrowseScreen()
        
        # Connect signals
        self.browse_screen.show_selected.connect(self.on_show_selected)
        self.browse_screen.player_requested.connect(self.on_player_requested)
        self.browse_screen.settings_requested.connect(self.on_settings_requested)
        
        # Set as central widget
        self.setCentralWidget(self.browse_screen)
        
        print("[TEST] Browse screen test window initialized")
        print("[TEST] Testing Phase 10D restyled components:")
        print("[TEST]   - Theme Manager colors/spacing")
        print("[TEST]   - PillButton navigation")
        print("[TEST]   - ConcertListItem show display")
        print("[TEST]   - Restyled search widget")
        print("[TEST]   - Restyled date browser")
    
    def on_show_selected(self, show):
        """Handle show selection"""
        print(f"\n[TEST] Show selected signal received:")
        print(f"[TEST]   Date: {show.get('date')}")
        print(f"[TEST]   Venue: {show.get('venue')}")
        print(f"[TEST]   Rating: {show.get('avg_rating')}")
        print(f"[TEST]   Source: {show.get('source')}")
    
    def on_player_requested(self):
        """Handle player navigation"""
        print("\n[TEST] Player requested signal received")
        print("[TEST] Would navigate to player screen")
    
    def on_settings_requested(self):
        """Handle settings navigation"""
        print("\n[TEST] Settings requested signal received")
        print("[TEST] Would navigate to settings screen")


def run_tests():
    """Run browse screen tests"""
    
    print("=" * 70)
    print("PHASE 10D BROWSE SCREEN TEST - RESTYLED")
    print("=" * 70)
    print()
    print("Testing Phase 10D restyled components:")
    print("  1. Theme Manager integration (zero hardcoded colors)")
    print("  2. PillButton navigation (blue, green, gradient variants)")
    print("  3. ConcertListItem for show lists")
    print("  4. Restyled search widget with PillButton")
    print("  5. Restyled date browser with Theme colors")
    print()
    print("Interactive Tests:")
    print("  - Click 'Top Rated' to see show list with ConcertListItem")
    print("  - Click 'Random Show' to see ShowCard display")
    print("  - Click 'Browse by Date' to see restyled calendar")
    print("  - Click 'Search Shows' to see restyled search interface")
    print("  - Click any show to emit show_selected signal")
    print()
    print("Expected Behavior:")
    print("  - All buttons use PillButton component")
    print("  - All colors from Theme Manager constants")
    print("  - Show lists use ConcertListItem with badges")
    print("  - Search button is yellow PillButton")
    print("  - Date browser uses Theme.ACCENT_BLUE")
    print("  - Zero hardcoded hex colors in any component")
    print()
    print("-" * 70)
    print()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Apply Theme global stylesheet
    app.setStyleSheet(Theme.get_global_stylesheet())
    
    # Create and show test window
    window = TestWindow()
    window.show()
    
    print("[TEST] Window displayed - begin interactive testing")
    print()
    
    # Run application
    return app.exec_()


if __name__ == '__main__':
    sys.exit(run_tests())
