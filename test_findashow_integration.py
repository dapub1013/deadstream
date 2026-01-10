#!/usr/bin/env python3
"""
Integration test for Find a Show -> Player Screen flow.
Tests that concerts properly load into the player when a date is selected.
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from src.ui.main_window import MainWindow


def test_findashow_to_player():
    """Test complete flow from Find a Show screen to Player screen"""

    print("\n" + "=" * 70)
    print("INTEGRATION TEST: Find a Show -> Player Screen")
    print("=" * 70)

    app = QApplication(sys.argv)

    # Step 1: Create main window
    print("\n[1] Creating MainWindow...")
    window = MainWindow()
    window.show()
    QTest.qWait(1000)

    current_screen = window.screen_manager.current_screen_name
    print(f"    Current screen: {current_screen}")
    assert current_screen == 'welcome', f"Expected welcome screen, got {current_screen}"

    # Step 2: Navigate to Find a Show
    print("\n[2] Navigating to Find a Show screen...")
    window.show_findashow()
    QTest.qWait(600)  # Wait for fade transition

    current_screen = window.screen_manager.current_screen_name
    print(f"    Current screen: {current_screen}")
    assert current_screen == 'findashow', f"Expected findashow screen, got {current_screen}"

    # Step 3: Select Cornell '77 date
    print("\n[3] Selecting date: 1977-05-08 (Cornell '77)...")
    window.findashow_screen.date_selected.emit('1977-05-08')
    QTest.qWait(2000)  # Wait for metadata fetch and transition

    # Step 4: Verify we're on player screen
    print("\n[4] Checking screen transition...")
    current_screen = window.screen_manager.current_screen_name
    print(f"    Current screen: {current_screen}")
    assert current_screen == 'player', f"Expected player screen, got {current_screen}"

    # Step 5: Verify show loaded into player
    print("\n[5] Verifying show loaded into player...")
    player = window.player_screen

    print(f"    current_show: {player.current_show is not None}")
    print(f"    playlist tracks: {len(player.playlist) if hasattr(player, 'playlist') else 0}")
    print(f"    total_tracks: {player.total_tracks}")
    print(f"    current_track_index: {player.current_track_index}")

    # Step 6: Verify UI updated
    print("\n[6] Verifying UI state...")
    print(f"    Song title: '{player.song_title_label.text()}'")
    print(f"    Track counter: '{player.track_counter_label.text()}'")
    print(f"    Player state: {player.player.get_state()}")

    # Step 7: Run assertions
    print("\n" + "=" * 70)
    print("VERIFICATION:")
    print("=" * 70)

    passed = True

    # Check show loaded
    if player.current_show is None:
        print("[FAIL] current_show is None - show not loaded")
        passed = False
    else:
        show_date = player.current_show.get('date')
        show_venue = player.current_show.get('venue')
        print(f"[PASS] Show loaded: {show_date} at {show_venue}")

    # Check playlist
    if not hasattr(player, 'playlist') or len(player.playlist) == 0:
        print("[FAIL] Playlist is empty - tracks not loaded")
        passed = False
    else:
        print(f"[PASS] Playlist loaded: {len(player.playlist)} tracks")

    # Check total_tracks
    if player.total_tracks == 0:
        print("[FAIL] total_tracks is 0")
        passed = False
    else:
        print(f"[PASS] total_tracks set: {player.total_tracks}")

    # Check UI updated
    if player.song_title_label.text() == "Song Title":
        print("[FAIL] Song title not updated from default")
        passed = False
    else:
        print(f"[PASS] Song title updated: '{player.song_title_label.text()}'")

    # Check track counter
    expected_counter = f"1 of {player.total_tracks}"
    if player.track_counter_label.text() != expected_counter:
        print(f"[WARN] Track counter shows '{player.track_counter_label.text()}', expected '{expected_counter}'")
    else:
        print(f"[PASS] Track counter updated: '{player.track_counter_label.text()}'")

    # Final result
    print("\n" + "=" * 70)
    if passed:
        print("[SUCCESS] All checks passed - flow works correctly!")
        print("=" * 70 + "\n")
        window.close()
        return 0
    else:
        print("[FAILURE] Some checks failed - flow has issues")
        print("=" * 70 + "\n")
        window.close()
        return 1


if __name__ == '__main__':
    exit_code = test_findashow_to_player()
    sys.exit(exit_code)
