#!/usr/bin/env python3
"""
Test Script for Browse Screen and Show List Widget

This script validates:
- Show list widget displays shows correctly
- Show cards are formatted properly
- Touch targets are appropriate size (60x60px minimum)
- Browse screen layout works
- Database integration functions

Usage:
    python examples/test_browse_screen.py

Expected behavior:
- Window opens showing top-rated shows
- Shows display with date, venue, location, rating
- Clicking a show card prints show information
- Scrolling works smoothly
- Play buttons are touch-friendly
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from src.ui.screens.browse_screen import BrowseScreen


class TestWindow(QMainWindow):
    """Test window for browse screen"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeadStream Browse Screen Test")
        self.setGeometry(100, 100, 1024, 600)
        
        # Create browse screen
        self.browse_screen = BrowseScreen()
        self.browse_screen.show_selected.connect(self.on_show_selected)
        
        self.setCentralWidget(self.browse_screen)
    
    def on_show_selected(self, show_data):
        """Handle show selection from browse screen"""
        print("\n" + "="*60)
        print("[OK] Show selected successfully!")
        print("="*60)
        print(f"Date:       {show_data['date']}")
        print(f"Venue:      {show_data.get('venue', 'Unknown')}")
        print(f"Location:   {show_data.get('city', 'Unknown')}, {show_data.get('state', 'Unknown')}")
        print(f"Identifier: {show_data['identifier']}")
        print(f"Rating:     {show_data.get('avg_rating', 'N/A')}/5.0")
        print(f"Reviews:    {show_data.get('num_reviews', 'N/A')}")
        print(f"Source:     {show_data.get('source', 'Unknown')}")
        print("="*60)
        print("\n[INFO] In production, this would:")
        print("  1. Load show metadata from Archive.org")
        print("  2. Use ShowSelector to pick best recording")
        print("  3. Start playback with ResilientPlayer")
        print("  4. Switch to Player screen")
        print()


def main():
    """Run browse screen test"""
    print("\n" + "="*60)
    print("DeadStream Browse Screen Test")
    print("="*60)
    print("\nThis test validates:")
    print("  [*] Show list widget displays correctly")
    print("  [*] Show cards have proper formatting")
    print("  [*] Touch targets are 60x60px minimum")
    print("  [*] Database integration works")
    print("  [*] Scrolling is smooth")
    print("\nInstructions:")
    print("  1. Window will open showing top-rated shows")
    print("  2. Scroll through the list")
    print("  3. Click on a show card or Play button")
    print("  4. Check terminal for show details")
    print("  5. Close window when done (or press Q)")
    print("="*60 + "\n")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create and show test window
    window = TestWindow()
    window.show()
    
    print("[INFO] Window opened - showing browse screen")
    print("[INFO] Loading top-rated shows from database...")
    print("\n[READY] Click on shows to test selection")
    print("[READY] Press Q to quit\n")
    
    # Run application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()