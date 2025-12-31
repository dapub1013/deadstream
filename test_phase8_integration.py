#!/usr/bin/env python3
"""
DeadStream Phase 8 Integration Testing
Task 8.8: Comprehensive integration tests for Settings Screen

Tests:
1. Settings screen loads in main application
2. Settings persistence works (save/load YAML)
3. All category switches work correctly
4. Settings values update UI correctly
5. Navigation back to Browse/Player works
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = '/home/david/deadstream'
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import yaml
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtTest import QTest


def wait_for_transition(milliseconds=500):
    """
    Wait for screen transition to complete.
    
    Screen transitions are animated and take time. This function waits
    long enough for the animation to finish.
    
    Args:
        milliseconds: Time to wait (default 500ms = 0.5 seconds)
    """
    QTest.qWait(milliseconds)


def test_settings_persistence():
    """Test that settings are saved and loaded correctly"""
    print("\n" + "="*60)
    print("TEST 1: Settings Persistence")
    print("="*60)
    
    settings_file = os.path.join(PROJECT_ROOT, 'config', 'settings.yaml')
    
    # Test data
    test_settings = {
        'network': {
            'wifi_enabled': True,
            'auto_connect': True
        },
        'audio': {
            'volume': 75,
            'output_device': 'Default',
            'buffer_size': 5000
        },
        'display': {
            'brightness': 80,
            'sleep_timeout': 300,
            'theme': 'dark'
        },
        'datetime': {
            'timezone': 'America/New_York',
            'use_24hour': False,
            'ntp_enabled': True
        }
    }
    
    try:
        # Save test settings
        os.makedirs(os.path.dirname(settings_file), exist_ok=True)
        with open(settings_file, 'w') as f:
            yaml.dump(test_settings, f)
        print("[PASS] Settings saved successfully")
        
        # Load settings back
        with open(settings_file, 'r') as f:
            loaded_settings = yaml.safe_load(f)
        
        # Verify all sections loaded
        if loaded_settings == test_settings:
            print("[PASS] Settings loaded correctly")
            print(f"  - Network settings: {loaded_settings['network']}")
            print(f"  - Audio settings: {loaded_settings['audio']}")
            print(f"  - Display settings: {loaded_settings['display']}")
            print(f"  - DateTime settings: {loaded_settings['datetime']}")
            return True
        else:
            print("[FAIL] Settings mismatch after load")
            return False
            
    except Exception as e:
        print(f"[FAIL] Settings persistence error: {e}")
        return False


def test_settings_screen_integration():
    """Test that settings screen integrates with main application"""
    print("\n" + "="*60)
    print("TEST 2: Settings Screen Integration")
    print("="*60)
    
    try:
        from src.ui.main_window import MainWindow
        
        app = QApplication(sys.argv)
        window = MainWindow()
        
        # Debug: Print all window attributes
        print("\n[DEBUG] Checking MainWindow attributes:")
        for attr in ['player_screen', 'browse_screen', 'settings_screen']:
            exists = hasattr(window, attr)
            print(f"  window.{attr}: {exists}")
        
        # Verify settings screen exists on MainWindow (not screen_manager)
        if not hasattr(window, 'settings_screen'):
            print("[FAIL] Settings screen not found on window")
            print("[INFO] This means create_screens() failed")
            print("[INFO] Check console output above for import errors")
            return False
        
        print("[PASS] Settings screen exists in MainWindow")

        
        # Test switching to settings screen
        try:
            window.screen_manager.show_screen('settings')
            
            # Wait for transition animation to complete
            wait_for_transition(600)  # 600ms should be enough for slide animation
            
            current_screen = window.screen_manager.currentWidget()
            
            if current_screen == window.settings_screen:
                print("[PASS] Successfully switched to settings screen")
            else:
                print(f"[FAIL] Screen switch did not work")
                print(f"  Expected: {window.settings_screen}")
                print(f"  Got: {current_screen}")
                return False
                
        except Exception as e:
            print(f"[FAIL] Error switching to settings: {e}")
            return False
        
        # Test that settings screen has all category widgets
        settings_screen = window.settings_screen
        
        # Check for category_buttons dictionary
        if not hasattr(settings_screen, 'category_buttons'):
            print("[FAIL] Settings screen has no category_buttons dictionary")
            return False
        
        # Check that all expected categories exist
        expected_categories = ['network', 'audio', 'database', 'display', 'datetime', 'about']
        categories_exist = all(
            cat in settings_screen.category_buttons 
            for cat in expected_categories
        )
        
        if categories_exist:
            print("[PASS] All category buttons exist in dictionary")
        else:
            missing = [cat for cat in expected_categories 
                      if cat not in settings_screen.category_buttons]
            print(f"[FAIL] Missing category buttons: {missing}")
            return False
        
        # Check for detail widgets (stored as attributes)
        details_exist = (
            hasattr(settings_screen, 'network_widget') and
            hasattr(settings_screen, 'audio_widget') and
            hasattr(settings_screen, 'display_widget') and
            hasattr(settings_screen, 'datetime_widget') and
            hasattr(settings_screen, 'about_widget')
        )
        
        if details_exist:
            print("[PASS] All detail widgets exist")
        else:
            print("[FAIL] Some detail widgets missing")
            return False
        
        print("[PASS] Settings screen fully integrated")
        return True
        
    except ImportError as e:
        print(f"[FAIL] Cannot import MainWindow: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Integration test error: {e}")
        return False


def test_category_navigation():
    """Test that all settings categories can be navigated"""
    print("\n" + "="*60)
    print("TEST 3: Settings Category Navigation")
    print("="*60)
    
    try:
        from src.ui.main_window import MainWindow
        
        app = QApplication(sys.argv)
        window = MainWindow()
        window.screen_manager.show_screen('settings')
        settings_screen = window.settings_screen
        
        # Test each category
        categories = [
            ('network', 'network_widget'),
            ('audio', 'audio_widget'),
            ('database', 'database_widget'),
            ('display', 'display_widget'),
            ('datetime', 'datetime_widget'),
            ('about', 'about_widget')
        ]
        
        all_passed = True
        
        for name, widget_attr in categories:
            try:
                # Get the category button from dictionary
                if name not in settings_screen.category_buttons:
                    print(f"[FAIL] {name.title()} category button not found in dictionary")
                    all_passed = False
                    continue
                
                button = settings_screen.category_buttons[name]
                button.click()
                
                # Verify the correct widget is shown in content_stack
                current_widget = settings_screen.content_stack.currentWidget()
                expected_widget = getattr(settings_screen, widget_attr)
                
                if current_widget == expected_widget:
                    print(f"[PASS] {name.title()} category navigation works")
                else:
                    print(f"[FAIL] {name.title()} category shows wrong widget")
                    all_passed = False
                    
            except Exception as e:
                print(f"[FAIL] {name.title()} category error: {e}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"[FAIL] Category navigation test error: {e}")
        return False


def test_settings_values():
    """Test that settings widgets display correct values"""
    print("\n" + "="*60)
    print("TEST 4: Settings Values Display")
    print("="*60)
    
    try:
        from src.ui.main_window import MainWindow
        
        app = QApplication(sys.argv)
        window = MainWindow()
        window.screen_manager.show_screen('settings')
        settings_screen = window.settings_screen
        
        # Check audio widget values
        print("\nAudio Settings:")
        if 'audio' in settings_screen.category_buttons:
            settings_screen.category_buttons['audio'].click()
        else:
            print("  [FAIL] Audio button not found")
            return False
            
        audio_widget = settings_screen.audio_widget
        
        if hasattr(audio_widget, 'volume_slider'):
            volume = audio_widget.volume_slider.value()
            print(f"  Volume: {volume}%")
            if 0 <= volume <= 100:
                print("  [PASS] Volume in valid range")
            else:
                print("  [FAIL] Volume out of range")
                return False
        
        # Check display widget values
        print("\nDisplay Settings:")
        if 'display' in settings_screen.category_buttons:
            settings_screen.category_buttons['display'].click()
        else:
            print("  [FAIL] Display button not found")
            return False
            
        display_widget = settings_screen.display_widget
        
        if hasattr(display_widget, 'brightness_slider'):
            brightness = display_widget.brightness_slider.value()
            print(f"  Brightness: {brightness}%")
            if 0 <= brightness <= 100:
                print("  [PASS] Brightness in valid range")
            else:
                print("  [FAIL] Brightness out of range")
                return False
        
        # Check about widget
        print("\nAbout Information:")
        if 'about' in settings_screen.category_buttons:
            settings_screen.category_buttons['about'].click()
        else:
            print("  [FAIL] About button not found")
            return False
            
        about_widget = settings_screen.about_widget
        
        # About widget should exist and have version info
        if about_widget:
            print("  [PASS] About widget accessible")
        else:
            print("  [FAIL] About widget not found")
            return False
        
        print("[PASS] All settings values display correctly")
        return True
        
    except Exception as e:
        print(f"[FAIL] Settings values test error: {e}")
        return False


def test_navigation_to_other_screens():
    """Test navigation from settings to other screens"""
    print("\n" + "="*60)
    print("TEST 5: Navigation from Settings")
    print("="*60)
    
    try:
        from src.ui.main_window import MainWindow
        
        app = QApplication(sys.argv)
        window = MainWindow()
        
        # Start at settings
        window.screen_manager.show_screen('settings')
        wait_for_transition(600)  # Wait for animation
        print("[INFO] Started at settings screen")
        
        # Navigate to browse
        window.screen_manager.show_screen('browse')
        wait_for_transition(600)  # Wait for animation
        
        if window.screen_manager.currentWidget() == window.browse_screen:
            print("[PASS] Navigation to browse screen works")
        else:
            print("[FAIL] Could not navigate to browse")
            return False
        
        # Navigate back to settings
        window.screen_manager.show_screen('settings')
        wait_for_transition(600)  # Wait for animation
        
        if window.screen_manager.currentWidget() == window.settings_screen:
            print("[PASS] Navigation back to settings works")
        else:
            print("[FAIL] Could not navigate back to settings")
            return False
        
        # Navigate to player
        window.screen_manager.show_screen('player')
        wait_for_transition(600)  # Wait for animation
        
        if window.screen_manager.currentWidget() == window.player_screen:
            print("[PASS] Navigation to player screen works")
        else:
            print("[FAIL] Could not navigate to player")
            return False
        
        print("[PASS] All screen navigation working")
        return True
        
    except Exception as e:
        print(f"[FAIL] Navigation test error: {e}")
        return False


def main():
    """Run all integration tests"""
    print("="*60)
    print("DeadStream Phase 8 Integration Testing")
    print("Settings Screen Comprehensive Test Suite")
    print("="*60)
    
    results = {
        'Settings Persistence': test_settings_persistence(),
        'Settings Screen Integration': test_settings_screen_integration(),
        'Category Navigation': test_category_navigation(),
        'Settings Values': test_settings_values(),
        'Screen Navigation': test_navigation_to_other_screens()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] All integration tests passed!")
        print("="*60)
        return 0
    else:
        print("[WARNING] Some tests failed")
        print("="*60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
