#!/usr/bin/env python3
"""
Test script for Phase 9, Task 9.4: Playback Controls Integration

Tests:
1. Playback controls widget standalone
2. Player screen with integrated controls
3. Signal emission and state management
4. Button enable/disable logic
5. Track position updates
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtCore import QTimer

from src.ui.widgets.playback_controls import PlaybackControlsWidget
from src.ui.screens.player_screen import PlayerScreen


def test_playback_controls_widget():
    """Test 1: Playback controls widget standalone"""
    print("\n=== Test 1: Playback Controls Widget ===")
    
    widget = PlaybackControlsWidget()
    
    # Test initial state
    assert widget.is_playing == False, "Initial playing state should be False"
    assert widget.current_track == 0, "Initial track should be 0"
    assert widget.total_tracks == 0, "Initial total should be 0"
    print("[PASS] Initial state correct")
    
    # Test track position update
    widget.update_track_position(3, 8)
    assert widget.current_track == 3, "Track should be 3"
    assert widget.total_tracks == 8, "Total should be 8"
    assert widget.previous_btn.isEnabled() == True, "Previous should be enabled on track 3"
    assert widget.next_btn.isEnabled() == True, "Next should be enabled on track 3"
    print("[PASS] Track position update works")
    
    # Test first track (previous disabled)
    widget.update_track_position(1, 8)
    assert widget.previous_btn.isEnabled() == False, "Previous should be disabled on track 1"
    assert widget.next_btn.isEnabled() == True, "Next should be enabled on track 1"
    print("[PASS] First track - previous disabled")
    
    # Test last track (next disabled)
    widget.update_track_position(8, 8)
    assert widget.previous_btn.isEnabled() == True, "Previous should be enabled on track 8"
    assert widget.next_btn.isEnabled() == False, "Next should be disabled on last track"
    print("[PASS] Last track - next disabled")
    
    # Test playing state
    widget.set_playing(True)
    assert widget.is_playing == True, "Playing state should be True"
    assert widget.play_pause_btn.text() == "PAUSE", "Button text should be PAUSE"
    print("[PASS] Playing state management works")
    
    widget.set_playing(False)
    assert widget.is_playing == False, "Playing state should be False"
    assert widget.play_pause_btn.text() == "PLAY", "Button text should be PLAY"
    print("[PASS] Pause state management works")
    
    # Test reset
    widget.reset()
    assert widget.is_playing == False, "Reset should set playing to False"
    assert widget.current_track == 0, "Reset should set track to 0"
    print("[PASS] Reset works correctly")
    
    print("[OK] All playback controls widget tests passed\n")
    
    return widget


def test_player_screen_integration():
    """Test 2: Player screen with integrated controls"""
    print("\n=== Test 2: Player Screen Integration ===")
    
    screen = PlayerScreen()
    
    # Test that widgets exist
    assert screen.track_info is not None, "Track info widget should exist"
    assert screen.playback_controls is not None, "Playback controls should exist"
    print("[PASS] Widgets created successfully")
    
    # Test track update propagation
    screen.update_track("Scarlet Begonias", "SET I", 3, 8)
    assert screen.playback_controls.current_track == 3, "Controls should have track 3"
    assert screen.playback_controls.total_tracks == 8, "Controls should have 8 tracks"
    print("[PASS] Track updates propagate to controls")
    
    # Test playing state propagation
    screen.set_playing(True)
    assert screen.playback_controls.is_playing == True, "Controls should show playing"
    print("[PASS] Playing state propagates to controls")
    
    # Test clear
    screen.clear_track()
    assert screen.playback_controls.current_track == 0, "Clear should reset track"
    assert screen.playback_controls.is_playing == False, "Clear should stop playback"
    print("[PASS] Clear works correctly")
    
    print("[OK] All player screen integration tests passed\n")
    
    return screen


def test_signal_emission():
    """Test 3: Signal emission"""
    print("\n=== Test 3: Signal Emission ===")
    
    screen = PlayerScreen()
    
    # Track signal emissions
    signals_received = {
        'play_pause': False,
        'previous': False,
        'next': False,
        'skip_backward': False,
        'skip_forward': False,
        'browse': False
    }
    
    # Connect signals
    screen.play_pause_requested.connect(lambda: signals_received.update({'play_pause': True}))
    screen.previous_track_requested.connect(lambda: signals_received.update({'previous': True}))
    screen.next_track_requested.connect(lambda: signals_received.update({'next': True}))
    screen.skip_backward_30s_requested.connect(lambda: signals_received.update({'skip_backward': True}))
    screen.skip_forward_30s_requested.connect(lambda: signals_received.update({'skip_forward': True}))
    screen.browse_requested.connect(lambda: signals_received.update({'browse': True}))
    
    # Trigger signals programmatically
    screen.update_track("Dark Star", "SET II", 3, 8)  # Enable previous/next
    
    screen.playback_controls.play_pause_btn.click()
    assert signals_received['play_pause'] == True, "Play/pause signal should be emitted"
    print("[PASS] Play/pause signal emitted")
    
    screen.playback_controls.previous_btn.click()
    assert signals_received['previous'] == True, "Previous signal should be emitted"
    print("[PASS] Previous signal emitted")
    
    screen.playback_controls.next_btn.click()
    assert signals_received['next'] == True, "Next signal should be emitted"
    print("[PASS] Next signal emitted")
    
    # Test 30-second skip signals
    # Get the actual button widgets from the layout
    skip_container = screen.playback_controls.layout().itemAt(1).widget()
    skip_layout = skip_container.layout()
    rewind_btn = skip_layout.itemAt(1).widget()  # First button (rewind)
    skip_btn = skip_layout.itemAt(2).widget()    # Second button (skip)
    
    rewind_btn.click()
    assert signals_received['skip_backward'] == True, "Skip backward signal should be emitted"
    print("[PASS] Skip backward signal emitted")
    
    skip_btn.click()
    assert signals_received['skip_forward'] == True, "Skip forward signal should be emitted"
    print("[PASS] Skip forward signal emitted")
    
    print("[OK] All signal emission tests passed\n")


def run_interactive_test():
    """Run interactive test with GUI"""
    print("\n=== Interactive Test ===")
    print("Window will open with playback controls.")
    print("Test the following:")
    print("1. Click PLAY button (should change to PAUSE)")
    print("2. Click Previous/Next (should be disabled initially)")
    print("3. Wait for track updates (buttons will enable)")
    print("4. Try 30-second skip buttons")
    print("5. Watch console for signal output")
    print("6. Close window when done\n")
    
    app = QApplication(sys.argv)
    
    # Create tabbed interface
    window = QMainWindow()
    window.setWindowTitle("DeadStream - Task 9.4 Test Suite")
    window.setGeometry(100, 100, 1024, 600)
    window.setStyleSheet("QMainWindow { background-color: #000000; }")
    
    tabs = QTabWidget()
    tabs.setStyleSheet("""
        QTabWidget::pane {
            background-color: #000000;
            border: none;
        }
        QTabBar::tab {
            background-color: #1F2937;
            color: #FFFFFF;
            padding: 10px 20px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #374151;
        }
    """)
    
    # Tab 1: Standalone controls
    controls_widget = PlaybackControlsWidget()
    controls_widget.play_pause_clicked.connect(lambda: print("[TEST] Play/pause"))
    controls_widget.previous_clicked.connect(lambda: print("[TEST] Previous"))
    controls_widget.next_clicked.connect(lambda: print("[TEST] Next"))
    controls_widget.skip_backward_30s.connect(lambda: print("[TEST] Skip -30s"))
    controls_widget.skip_forward_30s.connect(lambda: print("[TEST] Skip +30s"))
    tabs.addTab(controls_widget, "Controls Widget")
    
    # Tab 2: Full player screen
    player_screen = PlayerScreen()
    player_screen.play_pause_requested.connect(lambda: print("[TEST] Player: Play/pause"))
    player_screen.previous_track_requested.connect(lambda: print("[TEST] Player: Previous"))
    player_screen.next_track_requested.connect(lambda: print("[TEST] Player: Next"))
    player_screen.skip_backward_30s_requested.connect(lambda: print("[TEST] Player: Skip -30s"))
    player_screen.skip_forward_30s_requested.connect(lambda: print("[TEST] Player: Skip +30s"))
    tabs.addTab(player_screen, "Player Screen")
    
    window.setCentralWidget(tabs)
    window.show()
    
    # Simulate track updates
    def update_track_1():
        print("\n[TEST] Simulating track 1 of 8 (Bertha)")
        controls_widget.update_track_position(1, 8)
        player_screen.update_track("Bertha", "SET I", 1, 8)
    
    def update_track_3():
        print("\n[TEST] Simulating track 3 of 8 (Scarlet Begonias)")
        controls_widget.update_track_position(3, 8)
        player_screen.update_track("Scarlet Begonias", "SET I", 3, 8)
    
    def update_track_8():
        print("\n[TEST] Simulating track 8 of 8 (One More Saturday Night)")
        controls_widget.update_track_position(8, 8)
        player_screen.update_track("One More Saturday Night", "ENCORE", 8, 8)
    
    # Schedule updates
    QTimer.singleShot(2000, update_track_1)
    QTimer.singleShot(5000, update_track_3)
    QTimer.singleShot(8000, update_track_8)
    
    return app.exec_()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("DeadStream - Phase 9, Task 9.4: Playback Controls Test")
    print("="*60)
    
    # Run automated tests
    try:
        # Create QApplication for widget tests
        app = QApplication(sys.argv)
        
        test_playback_controls_widget()
        test_player_screen_integration()
        test_signal_emission()
        
        print("\n" + "="*60)
        print("[OK] ALL AUTOMATED TESTS PASSED")
        print("="*60)
        
        # Ask if user wants interactive test
        print("\nRun interactive test? (y/n): ", end='')
        response = input().strip().lower()
        
        if response == 'y':
            exit_code = run_interactive_test()
            sys.exit(exit_code)
        else:
            print("\n[INFO] Skipping interactive test")
            print("[INFO] Task 9.4 testing complete")
            sys.exit(0)
            
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
