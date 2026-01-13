#!/usr/bin/env python3
"""
Test script for theme settings integration.
Demonstrates how to manage theme colors through the settings manager.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.settings.settings_manager import SettingsManager


def test_theme_settings():
    """Test theme settings functionality"""
    print("=" * 70)
    print("THEME SETTINGS TEST")
    print("=" * 70)

    # Create settings manager
    manager = SettingsManager()

    # Test 1: Get default theme colors
    print("\n[TEST 1] Getting default theme colors:")
    colors = manager.get_theme_colors()
    for key, value in colors.items():
        print(f"  {key}: {value}")

    # Test 2: Get individual theme settings
    print("\n[TEST 2] Getting individual theme settings:")
    color_scheme = manager.get('theme', 'color_scheme')
    font_family = manager.get('theme', 'font_family')
    font_multiplier = manager.get('theme', 'font_size_multiplier')
    print(f"  Color Scheme: {color_scheme}")
    print(f"  Font Family: {font_family}")
    print(f"  Font Size Multiplier: {font_multiplier}")

    # Test 3: Apply custom theme
    print("\n[TEST 3] Applying custom theme colors:")
    custom_colors = {
        'primary_bg': '#1A1A2E',
        'accent_yellow': '#FFA500',
        'accent_blue': '#00B4D8',
    }
    success = manager.apply_custom_theme(custom_colors)
    print(f"  Custom theme applied: {success}")

    # Verify changes
    print("\n[TEST 4] Verifying custom theme colors:")
    updated_colors = manager.get_theme_colors()
    for key, value in updated_colors.items():
        if key in custom_colors:
            status = "[CHANGED]" if value == custom_colors[key] else "[UNCHANGED]"
            print(f"  {status} {key}: {value}")
        else:
            print(f"  [DEFAULT] {key}: {value}")

    # Test 5: Test invalid color validation
    print("\n[TEST 5] Testing invalid color validation:")
    invalid_colors = {
        'primary_bg': 'not-a-color',
        'accent_yellow': '#GGGGGG',
    }
    success = manager.apply_custom_theme(invalid_colors)
    print(f"  Invalid colors rejected: {not success}")

    # Test 6: Reset to defaults
    print("\n[TEST 6] Resetting theme to defaults:")
    success = manager.reset_theme_to_default()
    print(f"  Theme reset: {success}")

    # Verify reset
    reset_colors = manager.get_theme_colors()
    print(f"  Primary BG after reset: {reset_colors['primary_bg']}")
    print(f"  Accent Yellow after reset: {reset_colors['accent_yellow']}")

    # Test 7: Validate settings
    print("\n[TEST 7] Validating settings:")
    warnings = manager.validate_settings()
    if warnings:
        print("[WARN] Validation warnings found:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("[PASS] All settings valid")

    print("\n" + "=" * 70)
    print("THEME SETTINGS TEST COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    test_theme_settings()
