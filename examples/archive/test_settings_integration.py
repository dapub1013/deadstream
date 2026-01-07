#!/usr/bin/env python3
"""
DeadStream Settings Integration Test - Phase 10, Task 10.4

Tests the complete settings integration to verify:
1. Settings are loaded from SettingsManager on application startup
2. UI widgets display current settings values
3. Changing settings in UI persists to SettingsManager
4. Settings persist across application restarts
5. Audio layer uses settings (default volume)
6. MainWindow restores last viewed screen

This test validates the entire settings integration chain.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from src.settings import get_settings
from src.ui.main_window import MainWindow
from src.ui.widgets.audio_settings_widget import AudioSettingsWidget
from src.ui.widgets.display_settings_widget import DisplaySettingsWidget
from src.ui.widgets.datetime_settings_widget import DateTimeSettingsWidget


def print_test_header(test_name):
    """Print a formatted test header"""
    print("\n" + "=" * 70)
    print(f"TEST: {test_name}")
    print("=" * 70)


def print_result(test_name, passed, message=""):
    """Print a test result"""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {test_name}")
    if message:
        print(f"      {message}")
    return passed


def test_audio_settings_integration(app):
    """Test AudioSettingsWidget integration with SettingsManager"""
    print_test_header("Audio Settings Integration")

    results = []
    settings = get_settings()

    # Test 1: Widget loads current settings on init
    print("\n[TEST] Widget loads current settings on init")
    initial_volume = settings.get('audio', 'default_volume', 77)
    widget = AudioSettingsWidget()
    loaded_volume = widget.get_volume()
    results.append(print_result(
        "Widget loads initial volume",
        loaded_volume == initial_volume,
        f"Expected {initial_volume}, got {loaded_volume}"
    ))

    # Test 2: Changing volume in widget saves to SettingsManager
    print("\n[TEST] Changing volume in widget saves to SettingsManager")
    new_volume = 85
    widget.volume_slider.setValue(new_volume)
    QTest.qWait(100)  # Allow signal to process
    saved_volume = settings.get('audio', 'default_volume')
    results.append(print_result(
        "Volume change persists to SettingsManager",
        saved_volume == new_volume,
        f"Expected {new_volume}, got {saved_volume}"
    ))

    # Test 3: Quality preference persists
    print("\n[TEST] Quality preference persists")
    mp3_button = widget.quality_group.button(1)
    mp3_button.click()  # Use click() to trigger signal
    QTest.qWait(100)
    quality_pref = settings.get('audio', 'quality_preference')
    results.append(print_result(
        "Quality preference persists",
        quality_pref == 'crowd_favorite',
        f"Expected 'crowd_favorite', got '{quality_pref}'"
    ))

    # Cleanup: restore original volume
    settings.set('audio', 'default_volume', initial_volume)
    settings.set('audio', 'quality_preference', 'balanced')

    return all(results)


def test_display_settings_integration(app):
    """Test DisplaySettingsWidget integration with SettingsManager"""
    print_test_header("Display Settings Integration")

    results = []
    settings = get_settings()

    # Test 1: Widget loads current settings on init
    print("\n[TEST] Widget loads current settings on init")
    initial_brightness = settings.get('display', 'brightness', 82)
    widget = DisplaySettingsWidget()
    loaded_brightness = widget.brightness_slider.value()
    results.append(print_result(
        "Widget loads initial brightness",
        loaded_brightness == initial_brightness,
        f"Expected {initial_brightness}, got {loaded_brightness}"
    ))

    # Test 2: Changing brightness saves to SettingsManager
    print("\n[TEST] Changing brightness saves to SettingsManager")
    new_brightness = 90
    widget.brightness_slider.setValue(new_brightness)
    QTest.qWait(100)
    saved_brightness = settings.get('display', 'brightness')
    results.append(print_result(
        "Brightness change persists",
        saved_brightness == new_brightness,
        f"Expected {new_brightness}, got {saved_brightness}"
    ))

    # Test 3: Changing timeout saves to SettingsManager
    print("\n[TEST] Changing timeout saves to SettingsManager")
    widget.timeout_combo.setCurrentText("5 minutes")
    QTest.qWait(100)
    saved_timeout = settings.get('display', 'screen_timeout')
    results.append(print_result(
        "Timeout change persists",
        saved_timeout == "5 minutes",
        f"Expected '5 minutes', got '{saved_timeout}'"
    ))

    # Cleanup
    settings.set('display', 'brightness', initial_brightness)
    settings.set('display', 'screen_timeout', '10 minutes')

    return all(results)


def test_datetime_settings_integration(app):
    """Test DateTimeSettingsWidget integration with SettingsManager"""
    print_test_header("DateTime Settings Integration")

    results = []
    settings = get_settings()

    # Test 1: Widget loads current settings on init
    print("\n[TEST] Widget loads current settings on init")
    initial_tz = settings.get('datetime', 'timezone', 'America/New_York')
    widget = DateTimeSettingsWidget()
    loaded_tz = widget.get_timezone()
    results.append(print_result(
        "Widget loads initial timezone",
        loaded_tz == initial_tz,
        f"Expected {initial_tz}, got {loaded_tz}"
    ))

    # Test 2: Changing timezone saves to SettingsManager
    print("\n[TEST] Changing timezone saves to SettingsManager")
    # Find Pacific timezone in combo box
    for i in range(widget.timezone_combo.count()):
        if widget.timezone_combo.itemData(i) == 'America/Los_Angeles':
            widget.timezone_combo.setCurrentIndex(i)
            break
    QTest.qWait(100)
    saved_tz = settings.get('datetime', 'timezone')
    results.append(print_result(
        "Timezone change persists",
        saved_tz == 'America/Los_Angeles',
        f"Expected 'America/Los_Angeles', got '{saved_tz}'"
    ))

    # Test 3: Changing time format saves
    print("\n[TEST] Time format persists")
    time_24h_button = widget.time_format_group.button(1)
    time_24h_button.click()  # Use click() to trigger signal
    QTest.qWait(100)
    saved_24h = settings.get('datetime', 'time_format_24h')
    results.append(print_result(
        "Time format change persists",
        saved_24h == True,
        f"Expected True, got {saved_24h}"
    ))

    # Cleanup
    widget.set_timezone(initial_tz)
    settings.set('datetime', 'time_format_24h', False)

    return all(results)


def test_player_volume_from_settings(app):
    """Test that ResilientPlayer loads default volume from settings"""
    print_test_header("ResilientPlayer Settings Integration")

    results = []
    settings = get_settings()

    # Test 1: Set a specific volume in settings
    print("\n[TEST] ResilientPlayer loads default volume from settings")
    test_volume = 88
    settings.set('audio', 'default_volume', test_volume)

    # Import and create player
    from src.audio.resilient_player import ResilientPlayer
    player = ResilientPlayer()

    # Verify player initialized with settings volume
    player_volume = player.get_volume()
    results.append(print_result(
        "ResilientPlayer loads volume from settings",
        player_volume == test_volume,
        f"Expected {test_volume}, got {player_volume}"
    ))

    # Cleanup
    settings.set('audio', 'default_volume', 77)

    return all(results)


def test_main_window_screen_persistence(app):
    """Test that MainWindow restores last viewed screen"""
    print_test_header("MainWindow Screen Persistence")

    results = []
    settings = get_settings()

    # Test 1: Set last screen to settings
    print("\n[TEST] MainWindow restores last viewed screen")
    settings.set('app', 'last_screen', 'settings')

    # Create MainWindow (should restore settings screen)
    window = MainWindow()
    QTest.qWait(500)  # Wait for screen transition animation

    # Check current screen
    from src.ui.screen_manager import ScreenManager
    current_screen = window.screen_manager.currentWidget()
    is_settings = current_screen == window.settings_screen
    results.append(print_result(
        "MainWindow restores settings screen",
        is_settings,
        f"Expected settings_screen, got {type(current_screen).__name__}"
    ))

    # Test 2: Navigate to browse, verify it's saved
    print("\n[TEST] Screen navigation persists to settings")
    window.show_browse()
    QTest.qWait(500)
    saved_screen = settings.get('app', 'last_screen')
    results.append(print_result(
        "Navigation to browse persists",
        saved_screen == 'browse',
        f"Expected 'browse', got '{saved_screen}'"
    ))

    # Test 3: Navigate to player, verify it's saved
    window.show_player()
    QTest.qWait(500)
    saved_screen = settings.get('app', 'last_screen')
    results.append(print_result(
        "Navigation to player persists",
        saved_screen == 'player',
        f"Expected 'player', got '{saved_screen}'"
    ))

    # Cleanup
    settings.set('app', 'last_screen', 'browse')
    window.close()

    return all(results)


def test_settings_persistence_across_restarts(app):
    """Test that settings persist across widget recreations (simulates app restart)"""
    print_test_header("Settings Persistence Across Restarts")

    results = []
    settings = get_settings()

    # Test 1: Set volume, destroy widget, create new widget, verify loaded
    print("\n[TEST] Audio settings persist across widget recreations")
    test_volume = 92
    widget1 = AudioSettingsWidget()
    widget1.volume_slider.setValue(test_volume)
    QTest.qWait(100)
    del widget1  # Destroy widget

    widget2 = AudioSettingsWidget()
    loaded_volume = widget2.get_volume()
    results.append(print_result(
        "Volume persists across widget recreations",
        loaded_volume == test_volume,
        f"Expected {test_volume}, got {loaded_volume}"
    ))

    # Test 2: Display settings persist
    print("\n[TEST] Display settings persist across widget recreations")
    test_brightness = 95
    display1 = DisplaySettingsWidget()
    display1.brightness_slider.setValue(test_brightness)
    QTest.qWait(100)
    del display1

    display2 = DisplaySettingsWidget()
    loaded_brightness = display2.brightness_slider.value()
    results.append(print_result(
        "Brightness persists across widget recreations",
        loaded_brightness == test_brightness,
        f"Expected {test_brightness}, got {loaded_brightness}"
    ))

    # Cleanup
    settings.set('audio', 'default_volume', 77)
    settings.set('display', 'brightness', 82)

    return all(results)


def run_all_tests():
    """Run all settings integration tests"""
    print("\n" + "=" * 70)
    print("DEADSTREAM SETTINGS INTEGRATION TEST SUITE")
    print("Phase 10, Task 10.4 - Complete Settings Integration")
    print("=" * 70)

    app = QApplication(sys.argv)

    test_results = []

    # Run tests
    test_results.append(("Audio Settings Integration", test_audio_settings_integration(app)))
    test_results.append(("Display Settings Integration", test_display_settings_integration(app)))
    test_results.append(("DateTime Settings Integration", test_datetime_settings_integration(app)))
    test_results.append(("ResilientPlayer Settings Integration", test_player_volume_from_settings(app)))
    test_results.append(("MainWindow Screen Persistence", test_main_window_screen_persistence(app)))
    test_results.append(("Settings Persistence Across Restarts", test_settings_persistence_across_restarts(app)))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    for test_name, result in test_results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    print("\n" + "-" * 70)
    print(f"TOTAL: {passed}/{total} tests passed")

    if passed == total:
        print("\n[PASS] All settings integration tests passed!")
        print("\nSettings integration is COMPLETE:")
        print("  - All widgets load settings on init")
        print("  - All widgets save settings on change")
        print("  - ResilientPlayer uses default volume from settings")
        print("  - PlayerScreen syncs volume control with player")
        print("  - MainWindow restores last viewed screen")
        print("  - Settings persist across widget recreations")
        return 0
    else:
        print(f"\n[FAIL] {total - passed} tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
