#!/usr/bin/env python3
"""
Test navigation system for DeadStream UI.
Tests screen transitions and signal connections.
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from src.ui.screen_manager import ScreenManager
from src.ui.player_screen import PlayerScreen
from src.ui.browse_screen import BrowseScreen
from src.ui.settings_screen import SettingsScreen


def test_screen_manager_creation():
    """Test creating screen manager"""
    print("\n[TEST] Creating ScreenManager...")
    try:
        manager = ScreenManager()
        print("[PASS] ScreenManager created successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to create ScreenManager: {e}")
        return False


def test_add_screens():
    """Test adding screens to manager"""
    print("\n[TEST] Adding screens to manager...")
    try:
        manager = ScreenManager()
        
        # Create screens
        player = PlayerScreen()
        browse = BrowseScreen()
        settings = SettingsScreen()
        
        # Add screens
        manager.add_screen(ScreenManager.PLAYER_SCREEN, player)
        manager.add_screen(ScreenManager.BROWSE_SCREEN, browse)
        manager.add_screen(ScreenManager.SETTINGS_SCREEN, settings)
        
        # Verify
        if len(manager.screens) != 3:
            print(f"[FAIL] Expected 3 screens, got {len(manager.screens)}")
            return False
        
        print(f"[PASS] Successfully added {len(manager.screens)} screens")
        return True
        
    except Exception as e:
        print(f"[FAIL] Failed to add screens: {e}")
        return False


def test_screen_transitions():
    """Test navigating between screens"""
    print("\n[TEST] Testing screen transitions...")
    try:
        manager = ScreenManager()
        
        # Add screens
        manager.add_screen(ScreenManager.PLAYER_SCREEN, PlayerScreen())
        manager.add_screen(ScreenManager.BROWSE_SCREEN, BrowseScreen())
        manager.add_screen(ScreenManager.SETTINGS_SCREEN, SettingsScreen())
        
        # Test transitions
        transitions = [
            (ScreenManager.PLAYER_SCREEN, "Player"),
            (ScreenManager.BROWSE_SCREEN, "Browse"),
            (ScreenManager.SETTINGS_SCREEN, "Settings"),
            (ScreenManager.PLAYER_SCREEN, "Player again")
        ]
        
        for screen_name, description in transitions:
            success = manager.show_screen(screen_name)
            if not success:
                print(f"[FAIL] Failed to show {description} screen")
                return False
            
            current = manager.get_current_screen_name()
            if current != screen_name:
                print(f"[FAIL] Screen mismatch: expected {screen_name}, got {current}")
                return False
        
        print("[PASS] All screen transitions successful")
        return True
        
    except Exception as e:
        print(f"[FAIL] Screen transition test failed: {e}")
        return False


def test_navigation_signals():
    """Test that navigation signals are emitted"""
    print("\n[TEST] Testing navigation signals...")
    try:
        received_signals = []
        
        def signal_handler(screen_name):
            received_signals.append(screen_name)
        
        manager = ScreenManager()
        manager.screen_changed.connect(signal_handler)
        
        # Add screens
        manager.add_screen(ScreenManager.PLAYER_SCREEN, PlayerScreen())
        manager.add_screen(ScreenManager.BROWSE_SCREEN, BrowseScreen())
        
        # Navigate
        manager.show_screen(ScreenManager.BROWSE_SCREEN)
        
        # Verify signal was emitted
        if ScreenManager.BROWSE_SCREEN not in received_signals:
            print("[FAIL] Screen change signal not emitted")
            return False
        
        print("[PASS] Navigation signals working correctly")
        return True
        
    except Exception as e:
        print(f"[FAIL] Signal test failed: {e}")
        return False


def main():
    """Run all navigation tests"""
    print("=" * 60)
    print("DeadStream Navigation System Tests")
    print("=" * 60)
    
    # Create QApplication (required for PyQt5)
    app = QApplication(sys.argv)
    
    # Run tests
    results = []
    results.append(test_screen_manager_creation())
    results.append(test_add_screens())
    results.append(test_screen_transitions())
    results.append(test_navigation_signals())
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n[SUCCESS] All navigation tests passed!")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())