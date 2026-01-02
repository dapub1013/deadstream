#!/usr/bin/env python3
"""
Test script for Phase 9, Task 9.5: Progress Bar with Seek

Tests:
1. Progress bar widget standalone
2. Player screen with integrated progress bar
3. Seek functionality
4. Time formatting
5. Progress updates
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtCore import QTimer

from src.ui.widgets.progress_bar import ProgressBarWidget
from src.ui.screens.player_screen import PlayerScreen


def test_time_formatting():
    """Test 1: Time formatting function"""
    print("\n=== Test 1: Time Formatting ===")
    
    # Test various time values
    test_cases = [
        (0, "0:00"),
        (30, "0:30"),
        (60, "1:00"),
        (90, "1:30"),
        (125, "2:05"),
        (420, "7:00"),
        (3661, "61:01"),  # Over 1 hour
        (-10, "0:00"),  # Negative (should clamp to 0)
    ]
    
    for seconds, expected in test_cases:
        result = ProgressBarWidget.format_time(seconds)
        assert result == expected, f"Expected {expected}, got {result} for {seconds}s"
        print(f"[PASS] {seconds}s -> {result}")
    
    print("[OK] All time formatting tests passed\n")


def test_progress_bar_widget():
    """Test 2: Progress bar widget standalone"""
    print("\n=== Test 2: Progress Bar Widget ===")
    
    widget = ProgressBarWidget()
    
    # Test initial state
    assert widget.current_time == 0, "Initial current_time should be 0"
    assert widget.total_duration == 0, "Initial total_duration should be 0"
    assert widget.is_seeking == False, "Initial is_seeking should be False"
    print("[PASS] Initial state correct")
    
    # Test set duration
    widget.set_duration(420)  # 7 minutes
    assert widget.total_duration == 420, "Duration should be 420"
    assert widget.duration_label.text() == "7:00", "Duration label should show 7:00"
    print("[PASS] Set duration works")
    
    # Test update position
    widget.update_position(125, 420)  # 2:05 / 7:00
    assert widget.current_time == 125, "Current time should be 125"
    assert widget.current_label.text() == "2:05", "Current label should show 2:05"
    # Slider should be at ~30% (125/420)
    expected_value = int((125 / 420) * 100)
    assert abs(widget.slider.value() - expected_value) <= 1, "Slider should be at ~30%"
    print("[PASS] Update position works")
    
    # Test reset
    widget.reset()
    assert widget.current_time == 0, "Reset should set current_time to 0"
    assert widget.total_duration == 0, "Reset should set total_duration to 0"
    assert widget.slider.value() == 0, "Reset should set slider to 0"
    assert widget.current_label.text() == "0:00", "Reset should set current label"
    assert widget.duration_label.text() == "0:00", "Reset should set duration label"
    print("[PASS] Reset works")
    
    print("[OK] All progress bar widget tests passed\n")
    
    return widget


def test_player_screen_integration():
    """Test 3: Player screen with integrated progress bar"""
    print("\n=== Test 3: Player Screen Integration ===")
    
    screen = PlayerScreen()
    
    # Test that widget exists
    assert screen.progress_bar is not None, "Progress bar widget should exist"
    print("[PASS] Progress bar widget created")
    
    # Test set duration
    screen.set_duration(420)
    assert screen.progress_bar.total_duration == 420, "Duration should propagate"
    print("[PASS] Set duration propagates to widget")
    
    # Test update progress
    screen.update_progress(125, 420)
    assert screen.progress_bar.current_time == 125, "Progress should propagate"
    print("[PASS] Progress updates propagate to widget")
    
    # Test clear
    screen.clear_track()
    assert screen.progress_bar.current_time == 0, "Clear should reset progress"
    print("[PASS] Clear resets progress bar")
    
    print("[OK] All player screen integration tests passed\n")
    
    return screen


def test_seek_functionality():
    """Test 4: Seek signal emission"""
    print("\n=== Test 4: Seek Functionality ===")
    
    screen = PlayerScreen()
    screen.set_duration(420)
    
    # Track seek signal
    seek_position = None
    
    def on_seek(pos):
        nonlocal seek_position
        seek_position = pos
    
    screen.seek_requested.connect(on_seek)
    
    # Simulate seek by manually triggering slider events
    # Set slider to 50% (should seek to 210s = 3:30)
    screen.progress_bar.is_seeking = True
    screen.progress_bar.slider.setValue(50)
    screen.progress_bar.on_slider_released()
    
    # Check that signal was emitted with correct value
    assert seek_position is not None, "Seek signal should be emitted"
    # Should be approximately 210s (50% of 420s)
    assert abs(seek_position - 210) <= 1, f"Seek position should be ~210s, got {seek_position}s"
    print(f"[PASS] Seek signal emitted with position {seek_position}s")
    
    print("[OK] All seek functionality tests passed\n")


def run_interactive_test():
    """Run interactive test with GUI"""
    print("\n=== Interactive Test ===")
    print("Window will open with progress bar.")
    print("Test the following:")
    print("1. Watch progress bar auto-update (simulated playback)")
    print("2. Drag slider to seek")
    print("3. Watch time labels update during seek")
    print("4. Release slider and check console for seek signal")
    print("5. Try both tabs (widget standalone and full player)")
    print("6. Close window when done\n")
    
    app = QApplication(sys.argv)
    
    # Create tabbed interface with timer cleanup
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.progress_timer = None
        
        def closeEvent(self, event):
            # Stop timer before closing
            if self.progress_timer:
                self.progress_timer.stop()
                print("[INFO] Timer stopped, closing window")
            event.accept()
    
    window = TestWindow()
    window.setWindowTitle("DeadStream - Task 9.5 Test Suite")
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
    
    # Tab 1: Standalone progress bar
    progress_widget = ProgressBarWidget()
    progress_widget.seek_requested.connect(
        lambda pos: print(f"[TEST] Widget seek: {pos}s ({progress_widget.format_time(pos)})")
    )
    tabs.addTab(progress_widget, "Progress Bar Widget")
    
    # Tab 2: Full player screen
    player_screen = PlayerScreen()
    player_screen.seek_requested.connect(
        lambda pos: print(f"[TEST] Player seek: {pos}s")
    )
    tabs.addTab(player_screen, "Player Screen")
    
    window.setCentralWidget(tabs)
    window.show()
    
    # Simulate track playback
    current_time = 0
    track_duration = 420  # 7 minutes
    
    def init_track():
        """Initialize track"""
        print("\n[TEST] Loading track (7:00 duration)")
        progress_widget.set_duration(track_duration)
        player_screen.set_duration(track_duration)
        player_screen.update_track("Scarlet Begonias", "SET I", 3, 8)
    
    def update_progress():
        """Update progress every second"""
        nonlocal current_time
        if current_time < track_duration:
            current_time += 1
            progress_widget.update_position(current_time, track_duration)
            player_screen.update_progress(current_time, track_duration)
    
    # Initialize after 1 second
    QTimer.singleShot(1000, init_track)
    
    # Update progress every second
    window.progress_timer = QTimer()
    window.progress_timer.timeout.connect(update_progress)
    window.progress_timer.start(1000)
    
    return app.exec_()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("DeadStream - Phase 9, Task 9.5: Progress Bar Test")
    print("="*60)
    
    # Run automated tests
    try:
        test_time_formatting()
        
        # Create QApplication for widget tests
        app = QApplication(sys.argv)
        
        test_progress_bar_widget()
        test_player_screen_integration()
        test_seek_functionality()
        
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
            print("[INFO] Task 9.5 testing complete")
            sys.exit(0)
            
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
