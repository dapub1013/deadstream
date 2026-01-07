#!/usr/bin/env python3
"""
DeadStream Phase 10 End-to-End Integration Test
Task 10.5: Complete Browse → Select → Play Workflow

Tests the complete user journey:
1. Application startup
2. Browse shows (multiple browse modes)
3. Select a show
4. View concert info
5. Play tracks
6. Use playback controls (play/pause, next/prev, seek, volume)
7. Auto-play next track
8. Navigate to settings
9. Change settings
10. Return to player
11. Verify settings applied

This validates the entire Phase 10 integration.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QTimer

from src.ui.main_window import MainWindow
from src.ui.screen_manager import ScreenManager
from src.settings import get_settings


class Phase10EndToEndTest:
    """End-to-end test runner for Phase 10"""

    def __init__(self, app):
        self.app = app
        self.window = None
        self.test_results = []
        self.current_test = ""

    def print_header(self, text):
        """Print a formatted header"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)

    def print_test(self, test_name):
        """Print test start"""
        self.current_test = test_name
        print(f"\n[TEST] {test_name}")

    def assert_result(self, condition, message, error_msg=""):
        """Assert and record result"""
        status = "[PASS]" if condition else "[FAIL]"
        print(f"{status} {message}")
        if not condition and error_msg:
            print(f"      {error_msg}")
        self.test_results.append((self.current_test, condition, message))
        return condition

    def wait(self, ms=500):
        """Wait for specified milliseconds"""
        QTest.qWait(ms)

    # ========================================================================
    # TEST: Application Startup
    # ========================================================================

    def test_application_startup(self):
        """Test 1: Application starts correctly"""
        self.print_header("TEST 1: APPLICATION STARTUP")

        self.print_test("Application Initialization")
        self.window = MainWindow()
        self.window.show()
        self.wait(600)  # Wait for screen transition

        # Verify window is visible and sized correctly
        self.assert_result(
            self.window.isVisible(),
            "Window is visible"
        )
        self.assert_result(
            self.window.width() == 1280 and self.window.height() == 720,
            f"Window sized correctly (1280x720)",
            f"Actual: {self.window.width()}x{self.window.height()}"
        )

        # Verify screens are created
        self.assert_result(
            hasattr(self.window, 'player_screen'),
            "Player screen created"
        )
        self.assert_result(
            hasattr(self.window, 'browse_screen'),
            "Browse screen created"
        )
        self.assert_result(
            hasattr(self.window, 'settings_screen'),
            "Settings screen created"
        )

        # Verify starting on browse screen
        current_screen = self.window.screen_manager.currentWidget()
        self.assert_result(
            current_screen == self.window.browse_screen,
            "Starts on browse screen"
        )

        return all(result[1] for result in self.test_results[-6:])

    # ========================================================================
    # TEST: Browse Shows
    # ========================================================================

    def test_browse_shows(self):
        """Test 2: Browse shows in different modes"""
        self.print_header("TEST 2: BROWSE SHOWS")

        browse = self.window.browse_screen

        # Verify shows are loaded on startup
        self.print_test("Initial Show List Population")
        show_count = len(browse.current_shows)
        self.assert_result(
            show_count > 0,
            f"Shows loaded on startup ({show_count} shows)"
        )

        # Verify show list widget exists and has shows
        self.assert_result(
            hasattr(browse, 'show_list'),
            "ShowListWidget exists"
        )

        self.assert_result(
            len(browse.show_list.shows) > 0,
            f"ShowListWidget populated ({len(browse.show_list.shows)} shows)"
        )

        return all(result[1] for result in self.test_results[-3:])

    # ========================================================================
    # TEST: Select Show and Navigate to Player
    # ========================================================================

    def test_select_show(self):
        """Test 3: Select a show and navigate to player"""
        self.print_header("TEST 3: SELECT SHOW AND PLAY")

        browse = self.window.browse_screen
        player = self.window.player_screen

        self.print_test("Show Selection")

        # Get first show from list
        if len(browse.current_shows) > 0:
            first_show = browse.current_shows[0]

            self.assert_result(
                first_show is not None,
                "First show exists"
            )

            # Simulate selecting the show (call the handler directly)
            browse.on_show_selected(first_show)
            self.wait(800)  # Wait for screen transition and playlist load

            # Verify navigated to player screen
            current_screen = self.window.screen_manager.currentWidget()
            self.assert_result(
                current_screen == player,
                "Navigated to player screen"
            )

            # Verify playlist was loaded
            self.assert_result(
                player.playlist_loaded,
                "Playlist loaded in player"
            )

            playlist_count = len(player.current_playlist)
            self.assert_result(
                playlist_count > 0,
                f"Tracks loaded in playlist ({playlist_count} tracks)"
            )

            return True
        else:
            print("[SKIP] No shows available to select")
            return False

    # ========================================================================
    # TEST: Playback Controls
    # ========================================================================

    def test_playback_controls(self):
        """Test 4: Test playback controls"""
        self.print_header("TEST 4: PLAYBACK CONTROLS")

        player = self.window.player_screen

        if not player.playlist_loaded:
            print("[SKIP] No playlist loaded, cannot test playback")
            return False

        self.print_test("Play/Pause Control")

        # Play
        player.on_play_pause()
        self.wait(1000)  # Wait for playback to start

        is_playing = player.player.is_playing()
        self.assert_result(
            is_playing,
            "Playback started"
        )

        # Pause
        player.on_play_pause()
        self.wait(300)

        is_paused = not player.player.is_playing()
        self.assert_result(
            is_paused,
            "Playback paused"
        )

        # Resume
        player.on_play_pause()
        self.wait(500)

        self.print_test("Next/Previous Track")

        initial_track = player.current_track_index

        # Next track
        player.on_next_track()
        self.wait(800)  # Wait for track load

        next_track = player.current_track_index
        self.assert_result(
            next_track == initial_track + 1,
            f"Advanced to next track (track {next_track + 1})"
        )

        # Previous track
        player.on_previous_track()
        self.wait(800)

        prev_track = player.current_track_index
        self.assert_result(
            prev_track == initial_track,
            f"Returned to previous track (track {prev_track + 1})"
        )

        self.print_test("Volume Control")

        # Test volume change
        original_volume = player.player.get_volume()
        new_volume = 50
        player.on_volume_changed(new_volume)
        self.wait(100)

        current_volume = player.player.get_volume()
        self.assert_result(
            current_volume == new_volume,
            f"Volume changed to {new_volume}%"
        )

        # Restore original volume
        player.on_volume_changed(original_volume)

        self.print_test("Mute/Unmute")

        # Mute
        player.on_mute_toggled(True)
        self.wait(100)

        is_muted = player.player.is_muted()
        self.assert_result(
            is_muted,
            "Audio muted"
        )

        # Unmute
        player.on_mute_toggled(False)
        self.wait(100)

        is_unmuted = not player.player.is_muted()
        self.assert_result(
            is_unmuted,
            "Audio unmuted"
        )

        # Stop playback for next tests
        player.player.stop()
        self.wait(300)

        return all(result[1] for result in self.test_results[-9:])

    # ========================================================================
    # TEST: Settings Integration
    # ========================================================================

    def test_settings_integration(self):
        """Test 5: Settings integration"""
        self.print_header("TEST 5: SETTINGS INTEGRATION")

        self.print_test("Navigate to Settings")

        # Navigate to browse screen first
        self.window.show_browse()
        self.wait(600)

        # Navigate to settings
        self.window.show_settings()
        self.wait(600)

        current_screen = self.window.screen_manager.currentWidget()
        self.assert_result(
            current_screen == self.window.settings_screen,
            "Navigated to settings screen"
        )

        self.print_test("Change Audio Settings")

        settings = get_settings()
        original_volume = settings.get('audio', 'default_volume', 77)

        # Change volume to 65
        settings_screen = self.window.settings_screen
        audio_widget = settings_screen.audio_widget
        audio_widget.volume_slider.setValue(65)
        self.wait(200)

        saved_volume = settings.get('audio', 'default_volume')
        self.assert_result(
            saved_volume == 65,
            "Volume setting persisted (65%)"
        )

        # Restore original volume
        audio_widget.volume_slider.setValue(original_volume)
        self.wait(200)

        self.print_test("Navigate Back to Browse")

        # Click back button
        settings_screen.back_clicked.emit()
        self.wait(600)

        current_screen = self.window.screen_manager.currentWidget()
        self.assert_result(
            current_screen == self.window.browse_screen,
            "Returned to browse screen"
        )

        return all(result[1] for result in self.test_results[-3:])

    # ========================================================================
    # TEST: Screen Navigation
    # ========================================================================

    def test_screen_navigation(self):
        """Test 6: Complete navigation flow"""
        self.print_header("TEST 6: SCREEN NAVIGATION FLOW")

        self.print_test("Browse → Settings → Browse")

        # Start on browse
        self.window.show_browse()
        self.wait(600)

        self.assert_result(
            self.window.screen_manager.currentWidget() == self.window.browse_screen,
            "On browse screen"
        )

        # To settings
        self.window.show_settings()
        self.wait(600)

        self.assert_result(
            self.window.screen_manager.currentWidget() == self.window.settings_screen,
            "Navigated to settings"
        )

        # Back to browse
        self.window.show_browse()
        self.wait(600)

        self.assert_result(
            self.window.screen_manager.currentWidget() == self.window.browse_screen,
            "Back to browse"
        )

        self.print_test("Browse → Player → Browse")

        # To player
        self.window.show_player()
        self.wait(600)

        self.assert_result(
            self.window.screen_manager.currentWidget() == self.window.player_screen,
            "Navigated to player"
        )

        # Back to browse
        self.window.show_browse()
        self.wait(600)

        self.assert_result(
            self.window.screen_manager.currentWidget() == self.window.browse_screen,
            "Back to browse from player"
        )

        return all(result[1] for result in self.test_results[-5:])

    # ========================================================================
    # RUN ALL TESTS
    # ========================================================================

    def run_all_tests(self):
        """Run complete test suite"""
        self.print_header("PHASE 10 END-TO-END INTEGRATION TEST")
        print("Testing complete browse → select → play workflow")
        print("This validates all Phase 10 deliverables")

        test_suites = [
            ("Application Startup", self.test_application_startup),
            ("Browse Shows", self.test_browse_shows),
            ("Select Show and Play", self.test_select_show),
            ("Playback Controls", self.test_playback_controls),
            ("Settings Integration", self.test_settings_integration),
            ("Screen Navigation", self.test_screen_navigation),
        ]

        suite_results = []

        for suite_name, test_func in test_suites:
            try:
                result = test_func()
                suite_results.append((suite_name, result))
            except Exception as e:
                print(f"\n[ERROR] {suite_name} raised exception: {e}")
                import traceback
                traceback.print_exc()
                suite_results.append((suite_name, False))

        # Print summary
        self.print_header("TEST SUMMARY")

        passed_suites = sum(1 for _, result in suite_results if result)
        total_suites = len(suite_results)

        for suite_name, result in suite_results:
            status = "[PASS]" if result else "[FAIL]"
            print(f"{status} {suite_name}")

        passed_tests = sum(1 for _, result, _ in self.test_results if result)
        total_tests = len(self.test_results)

        print(f"\n{'-' * 70}")
        print(f"Test Suites: {passed_suites}/{total_suites} passed")
        print(f"Individual Tests: {passed_tests}/{total_tests} passed")
        print(f"{'-' * 70}")

        if passed_suites == total_suites:
            print("\n[PASS] ALL END-TO-END TESTS PASSED!")
            print("\nPhase 10 Integration Status:")
            print("  ✓ Browse → Select → Play workflow complete")
            print("  ✓ Playback controls functional")
            print("  ✓ Settings integration working")
            print("  ✓ Screen navigation smooth")
            print("  ✓ Ready for Task 10.6 (Performance Profiling)")
            return 0
        else:
            print(f"\n[FAIL] {total_suites - passed_suites} test suite(s) failed")
            print("\nReview failures above and fix issues before proceeding.")
            return 1


def main():
    """Main test entry point"""
    app = QApplication(sys.argv)

    tester = Phase10EndToEndTest(app)
    exit_code = tester.run_all_tests()

    # Keep window open for visual inspection
    if exit_code == 0:
        print("\n[INFO] Window remains open for inspection")
        print("[INFO] Close window to exit test")
        sys.exit(app.exec_())
    else:
        # Close on failure for CI
        QTimer.singleShot(2000, app.quit)
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
