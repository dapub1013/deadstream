#!/usr/bin/env python3
"""
Test Settings Manager
Phase 8, Task 8.4: Comprehensive test of settings persistence

Tests all major functionality of the SettingsManager class.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.settings.settings_manager import SettingsManager, get_settings
import tempfile
import shutil


def test_basic_operations():
    """Test basic get/set operations"""
    print("\n" + "=" * 60)
    print("TEST 1: Basic Get/Set Operations")
    print("=" * 60)
    
    # Create temp config for testing
    temp_dir = tempfile.mkdtemp()
    temp_config = os.path.join(temp_dir, 'test_settings.yaml')
    
    try:
        manager = SettingsManager(config_path=temp_config)
        
        # Test getting default values
        print("\n[TEST] Getting default values:")
        volume = manager.get('audio', 'default_volume')
        print(f"  Default volume: {volume}")
        assert volume == 75, "Default volume should be 75"
        print("  [PASS] Default volume correct")
        
        brightness = manager.get('display', 'brightness')
        print(f"  Default brightness: {brightness}")
        assert brightness == 80, "Default brightness should be 80"
        print("  [PASS] Default brightness correct")
        
        # Test setting values
        print("\n[TEST] Setting new values:")
        success = manager.set('audio', 'default_volume', 90)
        assert success, "Set should succeed"
        print("  [PASS] Volume set successfully")
        
        # Verify value was saved
        new_volume = manager.get('audio', 'default_volume')
        assert new_volume == 90, "Volume should be 90"
        print(f"  [PASS] New volume verified: {new_volume}")
        
        # Test persistence by creating new instance
        print("\n[TEST] Testing persistence:")
        manager2 = SettingsManager(config_path=temp_config)
        persisted_volume = manager2.get('audio', 'default_volume')
        assert persisted_volume == 90, "Volume should persist"
        print(f"  [PASS] Volume persisted: {persisted_volume}")
        
        print("\n[OK] All basic operations passed")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def test_category_operations():
    """Test category-level operations"""
    print("\n" + "=" * 60)
    print("TEST 2: Category Operations")
    print("=" * 60)
    
    temp_dir = tempfile.mkdtemp()
    temp_config = os.path.join(temp_dir, 'test_settings.yaml')
    
    try:
        manager = SettingsManager(config_path=temp_config)
        
        # Test getting full category
        print("\n[TEST] Getting audio category:")
        audio = manager.get_category('audio')
        print(f"  Keys: {list(audio.keys())}")
        assert 'default_volume' in audio, "Should contain default_volume"
        assert 'quality_preference' in audio, "Should contain quality_preference"
        print("  [PASS] Category retrieved correctly")
        
        # Test setting full category
        print("\n[TEST] Setting category:")
        new_audio = {
            'default_volume': 95,
            'quality_preference': 'audiophile',
            'auto_play_on_startup': True,
            'crossfade_enabled': True,
        }
        success = manager.set_category('audio', new_audio)
        assert success, "Set category should succeed"
        print("  [PASS] Category set successfully")
        
        # Verify changes
        updated_audio = manager.get_category('audio')
        assert updated_audio['default_volume'] == 95, "Volume should be updated"
        assert updated_audio['quality_preference'] == 'audiophile', "Preference should be updated"
        print("  [PASS] Category changes verified")
        
        # Test reset category
        print("\n[TEST] Resetting category:")
        success = manager.reset_category('audio')
        assert success, "Reset should succeed"
        
        reset_audio = manager.get_category('audio')
        print(f"  Debug: reset_audio = {reset_audio}")
        print(f"  Debug: default_volume = {reset_audio.get('default_volume')}")
        assert reset_audio['default_volume'] == 75, f"Should be back to default (75), but got {reset_audio['default_volume']}"
        print("  [PASS] Category reset successfully")
        
        print("\n[OK] All category operations passed")
        
    finally:
        shutil.rmtree(temp_dir)


def test_validation():
    """Test settings validation"""
    print("\n" + "=" * 60)
    print("TEST 3: Settings Validation")
    print("=" * 60)
    
    temp_dir = tempfile.mkdtemp()
    temp_config = os.path.join(temp_dir, 'test_settings.yaml')
    
    try:
        manager = SettingsManager(config_path=temp_config)
        
        # Test valid settings
        print("\n[TEST] Validating default settings:")
        warnings = manager.validate_settings()
        assert len(warnings) == 0, "Default settings should be valid"
        print("  [PASS] No warnings for defaults")
        
        # Test invalid volume
        print("\n[TEST] Testing invalid volume:")
        manager.set('audio', 'default_volume', 150)
        warnings = manager.validate_settings()
        assert len(warnings) > 0, "Should warn about invalid volume"
        print(f"  [PASS] Validation caught error: {warnings[0]}")
        
        # Fix and revalidate
        manager.set('audio', 'default_volume', 80)
        warnings = manager.validate_settings()
        assert len(warnings) == 0, "Fixed settings should be valid"
        print("  [PASS] Fixed settings validated")
        
        print("\n[OK] All validation tests passed")
        
    finally:
        shutil.rmtree(temp_dir)


def test_export_import():
    """Test export and import functionality"""
    print("\n" + "=" * 60)
    print("TEST 4: Export/Import")
    print("=" * 60)
    
    temp_dir = tempfile.mkdtemp()
    config1 = os.path.join(temp_dir, 'settings1.yaml')
    config2 = os.path.join(temp_dir, 'settings2.yaml')
    export_file = os.path.join(temp_dir, 'backup.yaml')
    
    try:
        # Create settings and modify them
        print("\n[TEST] Creating custom settings:")
        manager1 = SettingsManager(config_path=config1)
        manager1.set('audio', 'default_volume', 88)
        manager1.set('display', 'brightness', 95)
        print("  [PASS] Custom settings created")
        
        # Export settings
        print("\n[TEST] Exporting settings:")
        success = manager1.export_settings(export_file)
        assert success, "Export should succeed"
        assert os.path.exists(export_file), "Export file should exist"
        print(f"  [PASS] Settings exported to {export_file}")
        
        # Create new manager with defaults
        print("\n[TEST] Creating new manager:")
        manager2 = SettingsManager(config_path=config2)
        default_volume = manager2.get('audio', 'default_volume')
        assert default_volume == 75, "Should start with defaults"
        print("  [PASS] New manager has defaults")
        
        # Import exported settings
        print("\n[TEST] Importing settings:")
        success = manager2.import_settings(export_file)
        assert success, "Import should succeed"
        
        imported_volume = manager2.get('audio', 'default_volume')
        assert imported_volume == 88, "Should have imported value"
        
        imported_brightness = manager2.get('display', 'brightness')
        assert imported_brightness == 95, "Should have imported value"
        print("  [PASS] Settings imported correctly")
        
        print("\n[OK] All export/import tests passed")
        
    finally:
        shutil.rmtree(temp_dir)


def test_global_instance():
    """Test global settings instance"""
    print("\n" + "=" * 60)
    print("TEST 5: Global Instance")
    print("=" * 60)
    
    print("\n[TEST] Getting global instance:")
    settings1 = get_settings()
    settings2 = get_settings()
    
    # Should be same instance
    assert settings1 is settings2, "Should return same instance"
    print("  [PASS] Global instance working")
    
    # Changes through one should reflect in other
    settings1.set('audio', 'default_volume', 77)
    volume = settings2.get('audio', 'default_volume')
    assert volume == 77, "Should see changes through same instance"
    print("  [PASS] Changes visible through both references")
    
    print("\n[OK] Global instance tests passed")


def test_merge_with_defaults():
    """Test that old config files get merged with new defaults"""
    print("\n" + "=" * 60)
    print("TEST 6: Merge with Defaults (Version Upgrades)")
    print("=" * 60)
    
    temp_dir = tempfile.mkdtemp()
    temp_config = os.path.join(temp_dir, 'test_settings.yaml')
    
    try:
        # Create manager and modify one setting
        print("\n[TEST] Creating config with subset of settings:")
        manager1 = SettingsManager(config_path=temp_config)
        manager1.set('audio', 'default_volume', 82)
        
        # Manually load and truncate the YAML (simulate old version)
        import yaml
        with open(temp_config, 'r') as f:
            data = yaml.safe_load(f)
        
        # Remove some categories (simulate old config missing new features)
        if 'datetime' in data:
            del data['datetime']
        
        with open(temp_config, 'w') as f:
            yaml.safe_dump(data, f)
        
        print("  [PASS] Simulated old config file")
        
        # Load with new manager
        print("\n[TEST] Loading old config with new manager:")
        manager2 = SettingsManager(config_path=temp_config)
        
        # Should have custom setting
        volume = manager2.get('audio', 'default_volume')
        assert volume == 82, "Should preserve custom settings"
        print(f"  [PASS] Custom setting preserved: {volume}")
        
        # Should have new default category
        timezone = manager2.get('datetime', 'timezone')
        assert timezone is not None, "Should have datetime settings"
        print(f"  [PASS] Missing category filled with defaults: {timezone}")
        
        print("\n[OK] Merge with defaults passed")
        
    finally:
        shutil.rmtree(temp_dir)


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print(" " * 15 + "SETTINGS MANAGER TEST SUITE")
    print("=" * 70)
    
    try:
        test_basic_operations()
        test_category_operations()
        test_validation()
        test_export_import()
        test_global_instance()
        test_merge_with_defaults()
        
        print("\n" + "=" * 70)
        print(" " * 20 + "ALL TESTS PASSED!")
        print("=" * 70)
        print("\n[OK] Settings manager is ready for production use")
        
        return True
        
    except AssertionError as e:
        print(f"\n[FAIL] Test assertion failed: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
