#!/usr/bin/env python3
"""
Demo script for Browse Screen UI

This script demonstrates the Browse Screen functionality.
Run this to test the browse interface on desktop or Pi.

Usage:
    # Desktop
    python3 examples/demo_browse_ui.py
    
    # Raspberry Pi
    ssh -X david@192.168.4.27
    cd ~/deadstream
    python3 examples/demo_browse_ui.py
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Import browse screen
from src.ui.screens.browse_screen import BrowseScreen


def main():
    """Run browse screen demo"""
    
    print("=" * 60)
    print("BROWSE SCREEN DEMO")
    print("=" * 60)
    print()
    print("Testing browse screen functionality...")
    print()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create browse screen
    browse = BrowseScreen()
    browse.setWindowTitle("DeadStream - Browse Screen Demo")
    browse.resize(1024, 600)  # 7" screen resolution
    
    # Connect show selection signal
    def on_show_selected(show):
        print(f"\n[INFO] Show selected:")
        print(f"  Date: {show['date']}")
        print(f"  Venue: {show.get('venue', 'Unknown')}")
        print(f"  City: {show.get('city', 'Unknown')}")
        print(f"  State: {show.get('state', 'Unknown')}")
        if show.get('avg_rating'):
            print(f"  Rating: {show['avg_rating']:.1f}/5.0")
        print()
    
    browse.show_selected.connect(on_show_selected)
    
    # Show window
    browse.show()
    
    print("[OK] Browse screen loaded")
    print()
    print("CONTROLS:")
    print("  - Click 'Top Rated Shows' to see top-rated list")
    print("  - Click 'Browse by Date' to browse by date")
    print("  - Click 'Browse by Venue' to filter by venue")
    print("  - Click any show's play button to select it")
    print("  - Close window or press Ctrl+Q to quit")
    print()
    print("=" * 60)
    print()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)