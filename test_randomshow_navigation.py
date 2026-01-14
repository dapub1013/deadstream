#!/usr/bin/env python3
"""
Test navigation to random show screen from welcome screen.
"""

import sys
sys.path.insert(0, '.')

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from src.ui.main_window import MainWindow
from src.ui.screen_manager import ScreenManager


def test_random_show_navigation():
    """Test navigation to random show screen"""
    print("\n" + "="*60)
    print("Random Show Navigation Test")
    print("="*60)

    app = QApplication(sys.argv)

    # Create main window
    print("\n[1] Creating main window...")
    window = MainWindow()
    window.show()
    QTest.qWait(500)  # Wait for window to render
    print("[PASS] Main window created")

    # Verify we're on welcome screen
    current = window.screen_manager.currentWidget()
    if current == window.welcome_screen:
        print("[PASS] Started on welcome screen")
    else:
        print("[FAIL] Not on welcome screen!")
        return False

    # Navigate to random show screen
    print("\n[2] Navigating to random show screen...")
    window.on_random_show_requested()
    QTest.qWait(600)  # Wait for transition

    # Verify we're on random show screen
    current = window.screen_manager.currentWidget()
    if current == window.randomshow_screen:
        print("[PASS] Navigated to random show screen")
    else:
        print(f"[FAIL] Expected random show screen, got: {current}")
        return False

    # Check screen components
    print("\n[3] Checking random show screen components...")

    if hasattr(window.randomshow_screen, 'random_show_widget'):
        print("[PASS] Has random_show_widget")
    else:
        print("[FAIL] Missing random_show_widget")
        return False

    if hasattr(window.randomshow_screen, 'home_button'):
        print("[PASS] Has home_button")
    else:
        print("[FAIL] Missing home_button")
        return False

    if hasattr(window.randomshow_screen, 'settings_button'):
        print("[PASS] Has settings_button")
    else:
        print("[FAIL] Missing settings_button")
        return False

    # Test home navigation
    print("\n[4] Testing home navigation...")
    window.randomshow_screen._on_home_clicked()
    QTest.qWait(600)

    current = window.screen_manager.currentWidget()
    if current == window.welcome_screen:
        print("[PASS] Home navigation works")
    else:
        print(f"[FAIL] Home navigation failed, current screen: {current}")
        return False

    # Navigate back to random show screen
    print("\n[5] Navigating back to random show screen...")
    window.on_random_show_requested()
    QTest.qWait(600)

    current = window.screen_manager.currentWidget()
    if current == window.randomshow_screen:
        print("[PASS] Can navigate back to random show screen")
    else:
        print("[FAIL] Cannot navigate back")
        return False

    # Test settings navigation
    print("\n[6] Testing settings navigation...")
    window.randomshow_screen._on_settings_clicked()
    QTest.qWait(600)

    current = window.screen_manager.currentWidget()
    if current == window.settings_screen:
        print("[PASS] Settings navigation works")
    else:
        print(f"[FAIL] Settings navigation failed, current screen: {current}")
        return False

    print("\n" + "="*60)
    print("All tests passed!")
    print("="*60)

    window.close()
    return True


if __name__ == "__main__":
    success = test_random_show_navigation()
    sys.exit(0 if success else 1)
