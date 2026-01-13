#!/usr/bin/env python3
"""
Example: Integrating Settings Manager with Theme Manager for UI
Demonstrates how to use both theme.py and settings_manager.py together.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.settings.settings_manager import SettingsManager
from src.ui.styles.theme import Theme


def demonstrate_theme_integration():
    """Show how to integrate settings with theme"""
    print("=" * 70)
    print("THEME + SETTINGS INTEGRATION EXAMPLE")
    print("=" * 70)

    # Get settings manager
    settings = SettingsManager()

    print("\n[1] Default Theme Constants (from theme.py):")
    print(f"  BG_PRIMARY: {Theme.BG_PRIMARY}")
    print(f"  ACCENT_YELLOW: {Theme.ACCENT_YELLOW}")
    print(f"  ACCENT_BLUE: {Theme.ACCENT_BLUE}")
    print(f"  TEXT_PRIMARY: {Theme.TEXT_PRIMARY}")

    print("\n[2] Current Theme Settings (from settings.yaml):")
    theme_colors = settings.get_theme_colors()
    print(f"  primary_bg: {theme_colors['primary_bg']}")
    print(f"  accent_yellow: {theme_colors['accent_yellow']}")
    print(f"  accent_blue: {theme_colors['accent_blue']}")
    print(f"  text_primary: {theme_colors['text_primary']}")

    print("\n[3] Font Settings:")
    font_family = settings.get('theme', 'font_family', Theme.FONT_FAMILY)
    font_multiplier = settings.get('theme', 'font_size_multiplier', 1.0)
    print(f"  Font Family: {font_family}")
    print(f"  Font Size Multiplier: {font_multiplier}")

    print("\n[4] Example: Generating Button Stylesheet with Theme:")
    # Use Theme constants
    button_style = Theme.get_button_style(Theme.ACCENT_YELLOW, Theme.TEXT_DARK)
    print("  Generated stylesheet for yellow button")
    print("  (First 200 chars):", button_style[:200].replace('\n', ' '))

    print("\n[5] Example: Scaling Font Sizes with Multiplier:")
    base_header_size = Theme.HEADER_LARGE
    scaled_header_size = int(base_header_size * font_multiplier)
    print(f"  Base header size: {base_header_size}px")
    print(f"  Scaled header size: {scaled_header_size}px")

    print("\n[6] Example: Using Custom Theme Colors:")
    # User might want custom colors
    custom_primary = settings.get('theme', 'primary_bg', Theme.BG_PRIMARY)
    custom_accent = settings.get('theme', 'accent_yellow', Theme.ACCENT_YELLOW)

    print(f"  Using primary background: {custom_primary}")
    print(f"  Using accent color: {custom_accent}")

    # Generate button with custom colors
    custom_button_style = Theme.get_button_style(custom_accent)
    print(f"  Generated custom button style")

    print("\n" + "=" * 70)
    print("HOW TO USE IN YOUR UI COMPONENTS:")
    print("=" * 70)
    print("""
    from src.settings.settings_manager import get_settings
    from src.ui.styles.theme import Theme

    # In your UI component __init__:
    settings = get_settings()

    # Get custom color or fall back to theme default
    bg_color = settings.get('theme', 'primary_bg', Theme.BG_PRIMARY)
    accent_color = settings.get('theme', 'accent_yellow', Theme.ACCENT_YELLOW)

    # Apply to widget
    self.setStyleSheet(f\"\"\"
        QWidget {{
            background-color: {bg_color};
        }}
    \"\"\")

    # Or use Theme helper with settings colors
    button_style = Theme.get_button_style(accent_color)
    my_button.setStyleSheet(button_style)

    # Scale fonts if user has custom multiplier
    font_multiplier = settings.get('theme', 'font_size_multiplier', 1.0)
    scaled_size = int(Theme.HEADER_LARGE * font_multiplier)
    """)

    print("=" * 70)


if __name__ == '__main__':
    demonstrate_theme_integration()
