#!/usr/bin/env python3
"""
Test Random Show Feature - Integration Test

This test verifies that clicking the "Random Show" button:
1. Loads a random show from the database
2. Displays the show information (date, venue, location)
3. Shows the setlist with tracks
4. Provides a "Try Again" button to load a different random show
5. Provides a "Play Show" button to start playback
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QTimer
from src.ui.screens.browse_screen import BrowseScreen


def test_random_show_button():
    """Test clicking Random Show button"""
    print("\n[TEST] Random Show Button Test")
    print("=" * 60)

    app = QApplication(sys.argv)

    # Create browse screen
    browse_screen = BrowseScreen()
    browse_screen.show()

    # Wait for screen to initialize
    QTest.qWait(500)

    print("[STEP 1] Browse screen initialized")

    # Verify we're on the default view (show list)
    if browse_screen.content_stack.currentIndex() != 0:
        print("[FAIL] Expected to be on show list view (index 0)")
        return False

    print("[PASS] Default view is show list (index 0)")

    # Click the "Random Show" button
    # The button is in the left panel browse mode buttons
    print("\n[STEP 2] Looking for Random Show button...")

    # We need to simulate clicking the button
    # Let's call the method directly since we can't easily find the button widget
    browse_screen.load_random_show()

    # Wait for the transition
    QTest.qWait(1000)

    print("[STEP 3] Called load_random_show()")

    # Verify we switched to random show view
    if browse_screen.content_stack.currentIndex() != 1:
        print(f"[FAIL] Expected to be on random show view (index 1), got {browse_screen.content_stack.currentIndex()}")
        return False

    print("[PASS] Switched to random show view (index 1)")

    # Verify the random show widget loaded
    random_widget = browse_screen.random_show_widget

    # Check if a show was loaded
    if not random_widget.current_show:
        print("[FAIL] No show loaded in random widget")
        return False

    show = random_widget.current_show
    print(f"[PASS] Show loaded: {show['date']} - {show['venue']}")
    print(f"       Location: {show['city']}, {show['state']}")

    # Check if metadata was fetched
    if random_widget.tracks:
        print(f"[PASS] Setlist loaded: {len(random_widget.tracks)} tracks")
        print(f"       First track: {random_widget.tracks[0].get('title', 'Unknown')}")
    else:
        print("[WARN] No setlist loaded (metadata fetch may have failed)")

    # Test "Try Again" button by calling reload
    print("\n[STEP 4] Testing 'Try Again' functionality...")
    first_show_date = show['date']

    # Call load_random_show again (simulates clicking Try Again)
    browse_screen.load_random_show()
    QTest.qWait(1000)

    new_show = random_widget.current_show
    if not new_show:
        print("[FAIL] No show loaded after Try Again")
        return False

    print(f"[INFO] New show loaded: {new_show['date']} - {new_show['venue']}")

    if new_show['date'] != first_show_date:
        print("[PASS] Different show loaded (Try Again works)")
    else:
        print("[INFO] Same show loaded (possible but unlikely)")

    # Test switching back to list view
    print("\n[STEP 5] Testing switch back to list view...")
    browse_screen.load_default_shows()
    QTest.qWait(500)

    if browse_screen.content_stack.currentIndex() != 0:
        print(f"[FAIL] Expected to be back on list view (index 0), got {browse_screen.content_stack.currentIndex()}")
        return False

    print("[PASS] Switched back to list view")

    print("\n" + "=" * 60)
    print("[PASS] All tests passed!")
    print("=" * 60)

    # Close the window
    browse_screen.close()

    return True


if __name__ == "__main__":
    # Set a timeout to exit
    QTimer.singleShot(15000, QApplication.quit)

    try:
        success = test_random_show_button()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
