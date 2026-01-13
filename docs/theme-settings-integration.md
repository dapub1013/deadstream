# Theme Settings Integration

**Date:** January 12, 2026
**File:** `src/settings/settings_manager.py`
**Related Files:**
- `src/ui/styles/theme.py` - Theme constants and styling
- `config/settings.yaml` - Persisted settings
- `docs/deadstream-ui-style-guide.md` - UI design reference

## Overview

Successfully integrated theme management into the DeadStream settings system, allowing user-customizable UI colors and fonts to persist across application sessions.

## Changes Made

### 1. Settings Manager Updates

Added a new `theme` category to the default settings structure with the following properties:

```python
'theme': {
    'color_scheme': 'default',  # default, custom
    'primary_bg': '#2E2870',    # Deep purple background
    'accent_yellow': '#FFD700',  # Gold accent
    'accent_blue': '#1976D2',    # Blue accent
    'accent_green': '#0F9D58',   # Green accent
    'text_primary': '#FFFFFF',   # White text
    'text_secondary': '#B0B0B0', # Gray text
    'font_family': 'sans-serif',
    'font_size_multiplier': 1.0,  # Scale all fonts
}
```

### 2. New Methods Added

#### `get_theme_colors() -> Dict[str, str]`
Returns all theme colors as a dictionary for easy access.

```python
colors = manager.get_theme_colors()
# Returns: {'primary_bg': '#2E2870', 'accent_yellow': '#FFD700', ...}
```

#### `apply_custom_theme(colors: Dict[str, str]) -> bool`
Apply custom theme colors with validation.

```python
custom = {
    'primary_bg': '#1A1A2E',
    'accent_yellow': '#FFA500',
}
manager.apply_custom_theme(custom)
```

#### `reset_theme_to_default() -> bool`
Reset theme to default DeadStream colors.

```python
manager.reset_theme_to_default()
```

#### `_is_valid_hex_color(color: str) -> bool`
Static method to validate hex color format (#RRGGBB).

### 3. Enhanced Validation

Added validation for theme settings:
- Validates `color_scheme` is 'default' or 'custom'
- Validates `font_size_multiplier` is between 0.5 and 2.0
- Validates all color values are proper hex format (#RRGGBB)
- Handles legacy string values for backwards compatibility

### 4. Test Scripts Created

#### `examples/test_theme_settings.py`
Comprehensive test of theme settings functionality:
- Get/set theme colors
- Apply custom themes
- Validate color formats
- Reset to defaults

#### `examples/test_theme_ui_integration.py`
Demonstrates integration between settings_manager and Theme class:
- Shows how to use both systems together
- Example code for UI components
- Font scaling examples

## Integration with Theme.py

The settings manager works alongside `src/ui/styles/theme.py`:

- **Theme.py** provides the default constants and styling helpers
- **Settings Manager** allows users to override defaults with custom preferences
- UI components can query settings first, falling back to Theme constants

### Example Usage in UI Components

```python
from src.settings.settings_manager import get_settings
from src.ui.styles.theme import Theme

# Get settings
settings = get_settings()

# Get custom color or fall back to theme default
bg_color = settings.get('theme', 'primary_bg', Theme.BG_PRIMARY)
accent_color = settings.get('theme', 'accent_yellow', Theme.ACCENT_YELLOW)

# Apply to widget
widget.setStyleSheet(f"""
    QWidget {{
        background-color: {bg_color};
        color: {accent_color};
    }}
""")

# Scale fonts if user has custom multiplier
font_multiplier = settings.get('theme', 'font_size_multiplier', 1.0)
scaled_size = int(Theme.HEADER_LARGE * font_multiplier)
```

## Settings Persistence

Theme settings are automatically persisted to `config/settings.yaml`:

```yaml
theme:
  color_scheme: default
  primary_bg: '#2E2870'
  accent_yellow: '#FFD700'
  accent_blue: '#1976D2'
  accent_green: '#0F9D58'
  text_primary: '#FFFFFF'
  text_secondary: '#B0B0B0'
  font_family: sans-serif
  font_size_multiplier: 1.0
```

## Benefits

1. **User Customization**: Users can customize app colors to their preference
2. **Accessibility**: Font size multiplier allows scaling for better readability
3. **Persistence**: Theme preferences saved and restored across sessions
4. **Validation**: Ensures only valid color values are accepted
5. **Backwards Compatible**: Works with existing settings files
6. **Easy Integration**: Simple API for UI components to use

## Future Enhancements

Potential additions for future development:

1. **Preset Themes**: Add multiple built-in color schemes (light mode, high contrast, etc.)
2. **Theme Import/Export**: Allow users to share custom themes
3. **Live Preview**: Real-time theme preview in settings screen
4. **Gradient Support**: Custom gradient backgrounds
5. **Per-Component Overrides**: Allow specific components to have custom colors

## Testing

All functionality tested and validated:

- ✅ Theme colors load from defaults
- ✅ Custom theme colors can be applied
- ✅ Invalid colors are rejected with validation
- ✅ Settings persist across sessions
- ✅ Validation catches malformed values
- ✅ Reset to defaults works correctly
- ✅ Integration with Theme.py verified

## Related Documentation

- [UI Style Guide](deadstream-ui-style-guide.md) - Complete design system
- [UI Implementation Plan](../deadstream-ui-implementation-plan.md) - Phased rollout
- [Settings Manager](../src/settings/settings_manager.py) - Code documentation
- [Theme Manager](../src/ui/styles/theme.py) - Theme constants

---

**Status**: Complete
**Phase**: 10 (UI Restyling)
**Next Steps**: Implement theme selection UI in settings screen
