#!/usr/bin/env python3
"""
Test script for Phase 9 Task 9.2: Track info display

Tests:
1. Track info widget initialization
2. Track updates (song name, set, counter)
3. Track clearing
4. Long song names (truncation)
5. Various set types
6. Integration with player screen
"""

import sys
import os

# Ensure we can import from src/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest

from src.ui.widgets.track_info import TrackInfoWidget
from src.ui.screens.player_screen import PlayerScreen


def test_track_info_widget():
    """Test the track info widget standalone"""
    print("\n=== TEST 1: Track Info Widget ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    widget = TrackInfoWidget()
    widget.show()
    QTest.qWait(100)
    
    # Test 1: Initial state
    print("[TEST] Initial state...")
    assert widget.current_song == "No Track Playing", "Initial song incorrect"
    assert widget.current_set == "", "Initial set should be empty"
    assert widget.track_number == 0, "Initial track number should be 0"
    assert widget.total_tracks == 0, "Initial total should be 0"
    print("[PASS] Initial state correct")
    
    # Test 2: Update with typical track
    print("[TEST] Update with typical track...")
    widget.update_track_info("Scarlet Begonias", "SET I", 3, 8)
    QTest.qWait(100)
    assert widget.current_song == "Scarlet Begonias"
    assert widget.current_set == "SET I"
    assert widget.track_number == 3
    assert widget.total_tracks == 8
    assert "Track 3 of 8" in widget.track_counter_label.text()
    print("[PASS] Track update works correctly")
    
    # Test 3: Update with SET II
    print("[TEST] Update to SET II...")
    widget.update_track_info("Dark Star", "SET II", 1, 6)
    QTest.qWait(100)
    assert widget.current_song == "Dark Star"
    assert widget.current_set == "SET II"
    assert widget.track_number == 1
    print("[PASS] SET II update works")
    
    # Test 4: Update with ENCORE
    print("[TEST] Update to ENCORE...")
    widget.update_track_info("Johnny B. Goode", "ENCORE", 1, 1)
    QTest.qWait(100)
    assert widget.current_song == "Johnny B. Goode"
    assert widget.current_set == "ENCORE"
    assert "Track 1 of 1" in widget.track_counter_label.text()
    print("[PASS] ENCORE update works")
    
    # Test 5: Long song name
    print("[TEST] Long song name...")
    long_name = "Playing in the Band > Drums > Space > The Other One"
    widget.update_track_info(long_name, "SET II", 2, 6)
    QTest.qWait(100)
    assert widget.current_song == long_name
    # Word wrap should handle this
    print("[PASS] Long song name handled")
    
    # Test 6: Clear track info
    print("[TEST] Clear track info...")
    widget.clear_track_info()
    QTest.qWait(100)
    assert widget.current_song == "No Track Playing"
    assert widget.current_set == ""
    assert widget.track_number == 0
    assert widget.total_tracks == 0
    print("[PASS] Track info cleared successfully")
    
    widget.close()
    print("[PASS] All track info widget tests passed\n")


def test_player_screen_integration():
    """Test track info integration with player screen"""
    print("\n=== TEST 2: Player Screen Integration ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.show()
    QTest.qWait(200)
    
    # Test 1: Track info widget exists
    print("[TEST] Track info widget exists...")
    assert screen.track_info is not None, "Track info widget not initialized"
    print("[PASS] Track info widget properly initialized")
    
    # Test 2: Update track via player screen
    print("[TEST] Update track via player screen...")
    screen.update_track("China Cat Sunflower", "SET I", 5, 8)
    QTest.qWait(100)
    assert screen.track_info.current_song == "China Cat Sunflower"
    assert screen.track_info.current_set == "SET I"
    assert screen.track_info.track_number == 5
    print("[PASS] Track update via player screen works")
    
    # Test 3: Multiple updates
    print("[TEST] Multiple track updates...")
    tracks = [
        ("I Know You Rider", "SET I", 6, 8),
        ("Estimated Prophet", "SET II", 1, 6),
        ("Eyes of the World", "SET II", 2, 6),
    ]
    
    for song, set_name, num, total in tracks:
        screen.update_track(song, set_name, num, total)
        QTest.qWait(50)
        assert screen.track_info.current_song == song
    
    print("[PASS] Multiple updates work correctly")
    
    # Test 4: Clear track
    print("[TEST] Clear track via player screen...")
    screen.clear_track()
    QTest.qWait(100)
    assert screen.track_info.current_song == "No Track Playing"
    print("[PASS] Track clearing works")
    
    # Test 5: Browse button signal
    print("[TEST] Browse button signal...")
    signal_received = []
    screen.browse_requested.connect(lambda: signal_received.append(True))
    
    # Find browse button and click it
    for child in screen.findChildren(object):
        if hasattr(child, 'text') and 'Browse' in str(child.text()):
            QTest.mouseClick(child, 1)  # Left click
            break
    
    QTest.qWait(100)
    assert len(signal_received) > 0, "Browse signal not emitted"
    print("[PASS] Browse button signal works")
    
    screen.close()
    print("[PASS] All player screen integration tests passed\n")


def test_visual_layout():
    """Test visual layout and styling"""
    print("\n=== TEST 3: Visual Layout ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    widget = TrackInfoWidget()
    widget.show()
    QTest.qWait(100)
    
    # Update with sample data
    widget.update_track_info("Fire on the Mountain", "SET I", 4, 8)
    QTest.qWait(100)
    
    # Test 1: Labels exist
    print("[TEST] All labels exist...")
    assert widget.now_playing_label is not None
    assert widget.song_label is not None
    assert widget.set_label is not None
    assert widget.track_counter_label is not None
    print("[PASS] All labels exist")
    
    # Test 2: Text content correct
    print("[TEST] Label text correct...")
    assert widget.now_playing_label.text() == "NOW PLAYING"
    assert widget.song_label.text() == "Fire on the Mountain"
    assert widget.set_label.text() == "SET I"
    assert "Track 4 of 8" in widget.track_counter_label.text()
    print("[PASS] All label text correct")
    
    # Test 3: Alignment
    print("[TEST] Label alignment...")
    from PyQt5.QtCore import Qt
    assert widget.now_playing_label.alignment() == Qt.AlignCenter
    assert widget.song_label.alignment() == Qt.AlignCenter
    assert widget.set_label.alignment() == Qt.AlignCenter
    assert widget.track_counter_label.alignment() == Qt.AlignCenter
    print("[PASS] All labels centered")
    
    widget.close()
    print("[PASS] All visual layout tests passed\n")


def run_interactive_demo():
    """Run interactive demo showing track changes"""
    print("\n=== INTERACTIVE DEMO ===")
    print("Showing track info changes over 10 seconds...")
    
    app = QApplication(sys.argv)
    
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("DeadStream Player Screen - Track Info Demo")
    screen.show()
    
    # Schedule track changes
    tracks = [
        (1000, "China Cat Sunflower", "SET I", 1, 8),
        (2500, "I Know You Rider", "SET I", 2, 8),
        (4000, "Candyman", "SET I", 3, 8),
        (5500, "Dark Star", "SET II", 1, 6),
        (7000, "Playing in the Band", "SET II", 2, 6),
        (8500, "Johnny B. Goode", "ENCORE", 1, 1),
    ]
    
    for delay, song, set_name, num, total in tracks:
        QTimer.singleShot(delay, lambda s=song, se=set_name, n=num, t=total: 
                         screen.update_track(s, se, n, t))
    
    # Clear after 10 seconds
    QTimer.singleShot(10000, screen.clear_track)
    
    # Close after 12 seconds
    QTimer.singleShot(12000, app.quit)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("\n" + "="*60)
    print("PHASE 9 TASK 9.2: TRACK INFO DISPLAY TESTS")
    print("="*60)
    
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_interactive_demo()
    else:
        # Run automated tests
        try:
            test_track_info_widget()
            test_player_screen_integration()
            test_visual_layout()
            
            print("\n" + "="*60)
            print("ALL TESTS PASSED [OK]")
            print("="*60)
            print("\nRun with --demo flag to see interactive demo:")
            print("  python3 examples/test_track_info.py --demo")
            print()
            
        except AssertionError as e:
            print(f"\n[FAIL] Test failed: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"\n[FAIL] Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
