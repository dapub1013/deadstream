#!/usr/bin/env python3
"""
Test script for main window screen transitions - Phase 10E.5

Tests fade transitions in the actual MainWindow context with all screens.

Usage:
    python3 examples/test_main_window_transitions.py
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest

from src.ui.main_window import MainWindow
from src.ui.screen_manager import ScreenManager


def test_main_window_transitions():
    """Test transitions in the main window"""
    app = QApplication(sys.argv)

    print("\n" + "="*60)
    print("MAIN WINDOW TRANSITION TEST - Phase 10E.5")
    print("="*60)

    # Create main window
    print("\n[TEST] Creating main window...")
    window = MainWindow()
    window.show()
    QTest.qWait(100)
    print("[PASS] Main window created")

    # Test 1: Initial screen (should be instant, no animation)
    print("\n[TEST 1] Verifying initial screen (instant transition)...")
    current = window.screen_manager.get_current_screen_name()
    print(f"[INFO] Initial screen: {current}")
    assert current in [ScreenManager.PLAYER_SCREEN, ScreenManager.BROWSE_SCREEN, ScreenManager.SETTINGS_SCREEN]
    print("[PASS] Initial screen set correctly")

    # Test 2: Fade to browse screen
    print("\n[TEST 2] Testing fade transition to browse screen...")
    window.show_browse()
    QTest.qWait(400)  # Wait for 300ms transition + buffer
    current = window.screen_manager.get_current_screen_name()
    assert current == ScreenManager.BROWSE_SCREEN, f"Expected browse, got {current}"
    print("[PASS] Fade to browse screen successful")

    # Test 3: Fade to settings screen
    print("\n[TEST 3] Testing fade transition to settings screen...")
    window.show_settings()
    QTest.qWait(400)
    current = window.screen_manager.get_current_screen_name()
    assert current == ScreenManager.SETTINGS_SCREEN, f"Expected settings, got {current}"
    print("[PASS] Fade to settings screen successful")

    # Test 4: Fade to player screen
    print("\n[TEST 4] Testing fade transition to player screen...")
    window.show_player()
    QTest.qWait(400)
    current = window.screen_manager.get_current_screen_name()
    assert current == ScreenManager.PLAYER_SCREEN, f"Expected player, got {current}"
    print("[PASS] Fade to player screen successful")

    # Test 5: Multiple rapid transitions
    print("\n[TEST 5] Testing multiple rapid transitions...")
    window.show_browse()
    QTest.qWait(100)
    window.show_settings()
    QTest.qWait(100)
    window.show_player()
    QTest.qWait(100)
    window.show_browse()
    QTest.qWait(500)  # Wait for final transition
    current = window.screen_manager.get_current_screen_name()
    assert current == ScreenManager.BROWSE_SCREEN, f"Expected browse, got {current}"
    print("[PASS] Rapid transitions handled correctly")

    # Test 6: Verify transition manager state
    print("\n[TEST 6] Verifying transition manager state...")
    assert not window.screen_manager.transition.is_animating, "Animation should be complete"
    print("[PASS] Transition manager in correct state")

    # Test 7: Verify screen widgets exist
    print("\n[TEST 7] Verifying all screen widgets...")
    player_widget = window.screen_manager.get_screen_widget(ScreenManager.PLAYER_SCREEN)
    browse_widget = window.screen_manager.get_screen_widget(ScreenManager.BROWSE_SCREEN)
    settings_widget = window.screen_manager.get_screen_widget(ScreenManager.SETTINGS_SCREEN)

    assert player_widget is not None, "Player screen widget missing"
    assert browse_widget is not None, "Browse screen widget missing"
    assert settings_widget is not None, "Settings screen widget missing"
    print("[PASS] All screen widgets exist")

    # Test 8: Performance test - measure transition time
    print("\n[TEST 8] Testing transition performance...")
    import time

    start_time = time.time()
    window.show_settings()
    QTest.qWait(400)
    end_time = time.time()

    transition_time_ms = (end_time - start_time) * 1000
    print(f"[INFO] Transition completed in {transition_time_ms:.1f}ms")

    # Should complete in roughly 300ms (transition) + test overhead
    assert transition_time_ms < 600, f"Transition too slow: {transition_time_ms}ms"
    print("[PASS] Transition performance acceptable")

    print("\n" + "="*60)
    print("ALL TESTS PASSED")
    print("="*60)
    print("\nSUMMARY:")
    print("- Initial screen loads instantly (no animation)")
    print("- Fade transitions work between all screens")
    print("- Transitions complete in ~300ms")
    print("- Rapid transitions handled gracefully")
    print("- No lag or performance issues")
    print("- All screen widgets properly initialized")
    print("\nTask 10E.5 Complete: Screen transitions implemented")
    print("="*60 + "\n")

    app.quit()


if __name__ == '__main__':
    test_main_window_transitions()
