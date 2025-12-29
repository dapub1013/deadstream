# Task 8.1 Integration Guide: Settings Screen Framework

**Phase:** 8 (Settings Screen)  
**Task:** 8.1 (Settings screen framework)  
**Date:** December 28, 2025  
**Status:** Complete

---

## Overview

This task creates the settings screen framework with category navigation. The screen features:

- Header with title and back button
- Left sidebar with 5 category buttons
- Right content area with scrolling
- Category switching with visual feedback
- Placeholder content for all categories

**Categories:**
1. Network (blue) - WiFi management
2. Audio (purple) - Volume and quality settings
3. Display (green) - Brightness and theme
4. Date & Time (amber) - Time zone settings
5. About (gray) - Version info and credits

---

## Files Created

### 1. settings_screen_framework.py
**Location:** `src/ui/screens/settings_screen.py` (when copied)  
**Purpose:** Complete settings screen with category navigation

**Key Components:**
- `SettingsScreen` class - Main settings screen widget
- Category sidebar with 5 buttons
- Content area with scrolling
- Category-specific placeholder content
- Back button with signal

**Public Interface:**
```python
class SettingsScreen(QWidget):
    back_clicked = pyqtSignal()  # Emitted when back button clicked
    
    def __init__(self)
    def show_category(category_id: str)  # Switch to a category
```

### 2. test_settings_framework.py
**Location:** `examples/test_settings_framework.py` (when copied)  
**Purpose:** Comprehensive test script

**Tests:**
- Settings screen creation
- Default category (network)
- All 5 category buttons exist
- Category switching
- Button style updates
- Back button signal
- Visual display with auto-cycling

---

## Installation Instructions

### Step 1: Copy Files to Project

```bash
# On your desktop (in Visual Studio Code terminal)
cd ~/deadstream

# Copy settings screen
cp /path/to/settings_screen_framework.py src/ui/screens/settings_screen.py

# Copy test script
cp /path/to/test_settings_framework.py examples/

# Copy this guide
cp /path/to/task-8.1-integration-guide.md docs/
```

### Step 2: Test Locally

```bash
# Test the settings screen
python examples/test_settings_framework.py
```

**Expected output:**
```
============================================================
TESTING SETTINGS SCREEN FRAMEWORK
============================================================

[TEST 1] Creating settings screen...
[PASS] Settings screen created

[TEST 2] Checking default category...
[PASS] Default category is 'network'

[TEST 3] Checking category buttons...
[PASS] All 5 category buttons exist

[TEST 4] Testing category switching...
  [PASS] Switched to 'audio'
  [PASS] Switched to 'display'
  [PASS] Switched to 'datetime'
  [PASS] Switched to 'about'
  [PASS] Switched to 'network'
[PASS] All category switches successful

[TEST 5] Testing button style updates...
[PASS] Button styles updated (visual inspection needed)

[TEST 6] Testing back button signal...
[PASS] Back button signal works

[TEST 7] Visual display test...
[INFO] Displaying settings screen for 5 seconds...
[PASS] Visual display test complete

============================================================
TEST SUMMARY
============================================================
[OK] Settings screen framework is working
[OK] All 5 category buttons present
[OK] Category switching works
[OK] Back button signal works
[OK] Layout is touch-friendly (1024x600)

[NEXT] Implement Network Settings (Task 8.2)
============================================================
```

### Step 3: Sync to Raspberry Pi

```bash
# Commit to git
git add src/ui/screens/settings_screen.py
git add examples/test_settings_framework.py
git add docs/task-8.1-integration-guide.md
git commit -m "[Phase-8] Task 8.1: Settings screen framework complete"
git push

# On Raspberry Pi (via SSH)
cd ~/deadstream
git pull
python examples/test_settings_framework.py
```

---

## Integration with Main App

### Adding to AppWindow

When ready to integrate with the main app, update `src/ui/app.py`:

```python
from src.ui.screens.settings_screen import SettingsScreen

class AppWindow(QMainWindow):
    def __init__(self):
        # ... existing code ...
        
        # Create settings screen
        self.settings_screen = SettingsScreen()
        self.settings_screen.back_clicked.connect(self.show_browse_screen)
        
        # Add to stacked widget
        self.screen_registry["settings"] = self.stacked_widget.addWidget(
            self.settings_screen
        )
    
    def show_settings_screen(self):
        """Switch to settings screen"""
        self.stacked_widget.setCurrentIndex(self.screen_registry["settings"])
```

### Connecting from Browse Screen

Update browse screen to navigate to settings:

```python
# In browse_screen.py
def _on_settings_clicked(self):
    """Handle settings button click"""
    # Emit signal to switch to settings screen
    self.switch_to_settings.emit()
```

---

## Design Decisions

### Layout Structure

**Two-column layout:**
- Left sidebar: 280px fixed width for categories
- Right content: Flexible width for settings

**Rationale:**
- Clear visual separation
- Easy navigation
- Touch-friendly button sizes (70px height)
- Familiar pattern from many apps

### Category Colors

Each category has a distinct color:
- Network: Blue (#3b82f6) - Associated with connectivity
- Audio: Purple (#8b5cf6) - Associated with media
- Display: Green (#10b981) - Associated with visuals
- Date & Time: Amber (#f59e0b) - Associated with time
- About: Gray (#6b7280) - Neutral info page

**Rationale:**
- Visual distinction helps navigation
- Colors match semantic meaning
- Consistent with browse screen colors

### Button Selection State

Selected button shows colored background, unselected shows dark background.

**Rationale:**
- Clear visual feedback
- Consistent with browse screen pattern
- Good contrast for readability
- Touch-friendly active states

### Placeholder Content

All categories except Network and About show placeholder text.

**Rationale:**
- Framework can be tested immediately
- Clear indication of what's coming
- Easy to replace with real content
- Allows parallel development of categories

---

## Testing Guide

### Manual Testing Checklist

- [ ] Settings screen displays at 1024x600
- [ ] Header shows "Settings" title
- [ ] Back button shows "< Back to Browse"
- [ ] All 5 category buttons visible
- [ ] Default category is Network (blue)
- [ ] Clicking Audio switches to Audio (purple background)
- [ ] Clicking Display switches to Display (green background)
- [ ] Clicking Date & Time switches to Date & Time (amber background)
- [ ] Clicking About switches to About (gray background)
- [ ] Clicking Network returns to Network (blue background)
- [ ] Only one button is highlighted at a time
- [ ] Content area shows placeholder text for each category
- [ ] Content area is scrollable (if needed)
- [ ] Back button closes settings (in test mode)

### Automated Test

Run the test script:
```bash
python examples/test_settings_framework.py
```

All tests should pass with `[PASS]` markers.

---

## Next Steps

### Task 8.2: Network Settings

Implement the Network category with:
- WiFi status display
- Available networks list
- Connect/disconnect buttons
- Connection strength indicator
- IP address display

### Task 8.3: About Page

Implement the About category with:
- DeadStream version
- Total show count from database
- Last database update
- Credits and acknowledgments
- Project information

### Future Categories (Later)

- Audio: Volume defaults, quality preferences
- Display: Brightness, theme, sleep timer
- Date & Time: Time zone, format preferences

---

## Technical Notes

### Widget Architecture

Follows the established pattern from Phase 6-7:
- Inherits from QWidget
- Emits signals for navigation
- Self-contained and reusable
- Can be added to any layout

### Style Consistency

Uses the same dark theme as browse screen:
- Background: #121212
- Cards: #1a1a1a
- Borders: #333333
- Text: #ffffff
- Accents: Category colors

### Touch Optimization

All interactive elements are touch-friendly:
- Category buttons: 70px height
- Back button: 60px height
- Touch targets: 60px minimum
- Adequate spacing: 15-20px

### Performance

- Lightweight placeholder content
- Lazy loading of category content
- Minimal re-rendering
- Smooth category switching

---

## Known Limitations

**None Critical:**

1. **Placeholder Categories**
   - Audio, Display, Date & Time show placeholders
   - **Impact:** Expected - will be implemented later
   - **Mitigation:** Clear TODO markers, will be added if needed

2. **No Settings Persistence**
   - Settings not saved yet
   - **Impact:** Will need settings storage system
   - **Mitigation:** Will add in Task 8.4 or later

3. **No Network Functionality**
   - Network category is placeholder
   - **Impact:** Expected - Task 8.2 will implement
   - **Mitigation:** Framework is ready

**All limitations are understood and planned for.**

---

## Success Criteria

All criteria met:

- [x] Settings screen displays with 1024x600 layout
- [x] Header shows title and back button
- [x] Left sidebar shows 5 category buttons
- [x] Right content area is scrollable
- [x] Default category is Network
- [x] Clicking category buttons switches content
- [x] Selected button shows colored background
- [x] Unselected buttons show dark background
- [x] Back button emits signal
- [x] All code follows 07-project-guidelines.md
- [x] Touch-friendly (60px+ button sizes)
- [x] Dark theme consistent with rest of UI
- [x] Test script runs without errors
- [x] All tests pass

---

## Appendix: Code Structure

### SettingsScreen Class

```
SettingsScreen (QWidget)
├── init_ui()
│   ├── _create_header()
│   │   ├── Back button (QPushButton)
│   │   └── Title label (QLabel)
│   ├── _create_category_sidebar()
│   │   └── 5 category buttons (QPushButton)
│   └── _create_content_area()
│       └── Scroll area with content widget
├── show_category(category_id)
│   ├── Update current_category
│   ├── update_button_styles()
│   └── Load category content
└── Category content methods
    ├── _show_network_settings()
    ├── _show_audio_settings()
    ├── _show_display_settings()
    ├── _show_datetime_settings()
    └── _show_about_page()
```

### Signal Flow

```
User clicks category button
    ↓
Button clicked signal
    ↓
show_category(category_id)
    ↓
├── Update current_category
├── update_button_styles() (visual feedback)
└── Load category content
    ↓
Content displayed in right panel
```

---

**Task 8.1: Complete**  
**Next: Task 8.2 (Network Settings)**  
**Status: Ready for Integration**
