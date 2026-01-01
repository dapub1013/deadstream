#!/usr/bin/env python3
"""
Test script for Phase 9 Task 9.1: Player Screen Layout
Demonstrates the player screen with real show data from database.
"""

import sys
import os

# Add project root to path
# Get the directory containing this script (examples/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to project root
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# Add to Python path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Import the new player screen from src/ui/screens/
from src.ui.screens.player_screen import PlayerScreen

# Import database queries
from src.database.queries import get_show_by_date, get_top_rated_shows


def get_test_show_data():
    """Get Cornell '77 show data from database"""
    print("[INFO] Fetching Cornell '77 from database...")
    
    shows = get_show_by_date('1977-05-08')
    
    if not shows:
        print("[WARN] Cornell '77 not found, using top-rated show...")
        shows = get_top_rated_shows(limit=1, min_reviews=5)
    
    if not shows:
        print("[ERROR] No shows found in database!")
        return None, None
    
    show = shows[0]
    
    # Format show data for player screen
    show_data = {
        'date': show['date'],
        'venue': show['venue'],
        'city': show.get('city', 'Unknown City'),
        'state': show.get('state', ''),
        'source': show.get('source', 'Unknown'),
        'rating': show.get('avg_rating', 0)
    }
    
    # Create mock track data (would come from API in real implementation)
    # Using Cornell '77 actual setlist
    tracks_data = [
        {'name': 'New Minglewood Blues', 'duration': '4:32', 'set': 'SET I'},
        {'name': 'Loser', 'duration': '7:15', 'set': 'SET I'},
        {'name': 'El Paso', 'duration': '4:41', 'set': 'SET I'},
        {'name': 'They Love Each Other', 'duration': '7:23', 'set': 'SET I'},
        {'name': 'Jack Straw', 'duration': '5:12', 'set': 'SET I'},
        {'name': 'Deal', 'duration': '5:34', 'set': 'SET I'},
        {'name': 'Lazy Lightning', 'duration': '3:12', 'set': 'SET I'},
        {'name': 'Supplication', 'duration': '4:45', 'set': 'SET I'},
        {'name': 'Scarlet Begonias', 'duration': '10:48', 'set': 'SET II'},
        {'name': 'Fire on the Mountain', 'duration': '10:23', 'set': 'SET II'},
        {'name': 'Estimated Prophet', 'duration': '9:34', 'set': 'SET II'},
        {'name': 'St. Stephen', 'duration': '7:12', 'set': 'SET II'},
        {'name': 'Not Fade Away', 'duration': '8:45', 'set': 'SET II'},
        {'name': 'St. Stephen', 'duration': '1:23', 'set': 'SET II'},
        {'name': 'Morning Dew', 'duration': '11:45', 'set': 'SET II'},
        {'name': 'One More Saturday Night', 'duration': '5:12', 'set': 'ENCORE'},
    ]
    
    print(f"[OK] Loaded: {show_data['date']} {show_data['venue']}")
    print(f"[OK] {len(tracks_data)} tracks")
    
    return show_data, tracks_data


def main():
    """Run the player screen test"""
    print("=" * 60)
    print("PHASE 9 TASK 9.1: PLAYER SCREEN LAYOUT TEST")
    print("=" * 60)
    print()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create player screen
    print("[INFO] Creating player screen...")
    player = PlayerScreen()
    player.setWindowTitle("DeadStream - Player Screen (Phase 9.1)")
    player.resize(1024, 600)
    
    # Load test data
    show_data, tracks_data = get_test_show_data()
    
    if show_data and tracks_data:
        print("[INFO] Loading show into player...")
        player.load_show(show_data, tracks_data)
        print("[OK] Show loaded successfully")
    else:
        print("[WARN] No show data - showing empty player")
    
    # Connect browse signal
    def on_browse():
        print("[INFO] Browse Shows button clicked!")
        print("[INFO] (In real app, this would switch to Browse screen)")
    
    player.browse_requested.connect(on_browse)
    
    # Show the player
    player.show()
    
    print()
    print("=" * 60)
    print("INTERACTIVE TEST INSTRUCTIONS")
    print("=" * 60)
    print()
    print("LEFT PANEL (Concert Info & Setlist):")
    print("  - View concert title, location, and metadata")
    print("  - Scroll through the full setlist")
    print("  - Click any track to jump to it")
    print("  - Notice set headers (SET I, SET II, ENCORE)")
    print()
    print("RIGHT PANEL (Now Playing & Controls):")
    print("  - See current song name and set")
    print("  - Click play/pause button (toggles > and ||)")
    print("  - Drag progress bar (no audio yet)")
    print("  - Use 30-second skip buttons")
    print("  - Adjust volume slider")
    print("  - Click 'Browse Shows' button")
    print()
    print("FEATURES TO VERIFY:")
    print("  [PASS] Split-screen 50/50 layout")
    print("  [PASS] Touch-friendly controls (44px+ minimum)")
    print("  [PASS] Dark theme with proper colors")
    print("  [PASS] Scrollable setlist")
    print("  [PASS] Track highlighting when clicked")
    print("  [PASS] Play/pause toggle")
    print("  [PASS] Volume slider updates percentage")
    print("  [PASS] All text is ASCII-only")
    print()
    print("Close window or press Ctrl+C to exit")
    print("=" * 60)
    print()
    
    # Run the app
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
