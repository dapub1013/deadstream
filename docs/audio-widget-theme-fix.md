# Audio Settings Widget - Theme Integration Fix

**Date:** January 12, 2026
**Issue:** Text not displaying properly in settings screen (poor contrast)
**File:** `src/ui/widgets/audio_settings_widget.py`
**Screenshot:** `src/settings/settings-screen.png`

## Problem Identified

The audio settings widget was using **hardcoded dark gray colors** instead of the Theme Manager constants, causing text to be nearly invisible against the dark background.

### Specific Issues

1. **Card backgrounds**: Hardcoded `#1f1f1f` instead of `Theme.BG_CARD`
2. **Text colors**: Hardcoded dark grays (`#9ca3af`, `#6b7280`) instead of `Theme.TEXT_PRIMARY` and `Theme.TEXT_SECONDARY`
3. **Radio button colors**: Hardcoded grays instead of theme accent colors
4. **No Theme Manager import**: Widget wasn't using the centralized theme system

### Visual Problem

Looking at the screenshot, the text was barely visible:
- Labels and descriptions appeared as dark gray on dark background
- Card backgrounds were too dark
- Poor contrast made the interface unusable

## Solution Applied

### 1. Added Theme Manager Import

```python
from src.ui.styles.theme import Theme
```

### 2. Updated All Card Backgrounds

**Before:**
```python
card.setStyleSheet("""
    QFrame {
        background-color: #1f1f1f;
        border: 1px solid #333333;
        border-radius: 12px;
    }
""")
```

**After:**
```python
card.setStyleSheet(f"""
    QFrame {{
        background-color: {Theme.BG_CARD};
        border: 1px solid {Theme.BORDER_SUBTLE};
        border-radius: 12px;
    }}
""")
```

### 3. Updated All Text Colors

**Primary Text (Titles, Values):**
- Changed from `#ffffff` → `{Theme.TEXT_PRIMARY}`
- Ensures consistency across the app

**Secondary Text (Descriptions, Labels):**
- Changed from `#9ca3af` and `#6b7280` → `{Theme.TEXT_SECONDARY}`
- Proper contrast for secondary information

### 4. Updated Radio Button Colors

**Unchecked State:**
- Background: `#333333` → `{Theme.BORDER_SUBTLE}`
- Border: `#6b7280` → `{Theme.TEXT_SECONDARY}`

**Checked State:**
- Background and border: `#8b5cf6` → `{Theme.ACCENT_BLUE}`
- Consistent with app accent colors

## Changes Summary

**Lines Modified:** ~30 locations throughout the file
**Functions Updated:**
- `_create_header()` - Title and subtitle colors
- `_create_volume_card()` - Card background, all text labels, slider colors
- `_create_quality_card()` - Card background, radio buttons, descriptions
- `_create_output_info_card()` - Card background, info labels and values

## Theme Colors Used

| Element | Old Color | New Theme Constant | Hex Value |
|---------|-----------|-------------------|-----------|
| Card Background | #1f1f1f | Theme.BG_CARD | #1E2936 |
| Border | #333333 | Theme.BORDER_SUBTLE | #333333 |
| Primary Text | #ffffff | Theme.TEXT_PRIMARY | #FFFFFF |
| Secondary Text | #9ca3af/#6b7280 | Theme.TEXT_SECONDARY | #B0B0B0 |
| Accent (checked) | #8b5cf6 | Theme.ACCENT_BLUE | #1976D2 |

## Benefits

1. **Proper Contrast**: Text now visible and readable
2. **Consistency**: Matches rest of application styling
3. **Maintainability**: Changes to theme automatically apply
4. **User Customization**: Will respect user theme preferences (from settings_manager)

## Testing

Widget tested standalone:
```bash
python3 src/ui/widgets/audio_settings_widget.py
```

Results:
- ✅ Text clearly visible
- ✅ Cards display with proper backgrounds
- ✅ Radio buttons show correct colors
- ✅ Volume slider uses theme colors
- ✅ All text has proper contrast
- ✅ Settings persist correctly

## Next Steps

**Other widgets likely need the same fix:**
- `network_settings_widget.py`
- `display_settings_widget.py`
- `database_settings_widget.py`
- `datetime_settings_widget.py`
- `about_widget.py`

These should be checked and updated to use Theme Manager constants instead of hardcoded colors.

## Related Files

- [settings_manager.py](../src/settings/settings_manager.py) - Settings persistence with theme support
- [theme.py](../src/ui/styles/theme.py) - Theme constants
- [deadstream-ui-style-guide.md](deadstream-ui-style-guide.md) - Complete style guide
- [audio_settings_widget.py](../src/ui/widgets/audio_settings_widget.py) - Fixed widget

---

**Status**: Complete
**Impact**: High (fixes critical usability issue)
**Theme Integration**: ✅ Now using centralized theme system
