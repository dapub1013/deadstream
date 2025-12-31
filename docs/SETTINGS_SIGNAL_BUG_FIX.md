# Phase 8 Bug Fix: SettingsScreen Signal Issue

**Issue Found During Task 8.8 Testing**  
**Date:** December 30, 2025  
**Severity:** Minor (cosmetic error, not functional)

---

## Problem

MainWindow tries to connect to `SettingsScreen.browse_requested` signal but SettingsScreen only has `back_clicked` signal.

**Error Message:**
```
[ERROR] Failed to connect navigation: 'SettingsScreen' object has no attribute 'browse_requested'
```

**Location:** `src/ui/main_window.py` line in `connect_navigation()` method

---

## Root Cause

In `src/ui/screens/settings_screen.py`:
```python
class SettingsScreen(QWidget):
    """Settings screen with category navigation"""
    
    # Signal emitted when back to browse is clicked
    back_clicked = pyqtSignal()  # <-- Only this signal exists
```

But `src/ui/main_window.py` tries to connect:
```python
def connect_navigation(self):
    """Connect navigation signals from screens to screen manager"""
    try:
        # ...
        
        # Settings screen navigation
        self.settings_screen.browse_requested.connect(self.show_browse)  # <-- Signal doesn't exist!
```

---

## Impact

**Functional:** NONE - Navigation still works via nav bar  
**User Experience:** None visible to user  
**Console:** Error message appears but doesn't break functionality

---

## Fix Options

### Option 1: Add the missing signal to SettingsScreen (Recommended)

**File:** `src/ui/screens/settings_screen.py`

Add the signal after `back_clicked`:

```python
class SettingsScreen(QWidget):
    """Settings screen with category navigation"""
    
    # Signals
    back_clicked = pyqtSignal()
    browse_requested = pyqtSignal()  # <-- ADD THIS
```

Then emit it when user wants to go to browse (if you add a browse button later).

### Option 2: Remove the connection attempt from MainWindow

**File:** `src/ui/main_window.py`

Comment out or remove the line:

```python
def connect_navigation(self):
    """Connect navigation signals from screens to screen manager"""
    try:
        # Player screen navigation
        self.player_screen.browse_requested.connect(self.show_browse)
        
        # Browse screen navigation
        self.browse_screen.player_requested.connect(self.show_player)
        self.browse_screen.settings_requested.connect(self.show_settings)
        
        # Settings screen navigation
        # self.settings_screen.browse_requested.connect(self.show_browse)  # <-- COMMENT OUT
        
        # Screen manager change signal
        self.screen_manager.screen_changed.connect(self.on_screen_changed)
```

### Option 3: Use back_clicked instead of browse_requested

**File:** `src/ui/main_window.py`

Change the connection to use the signal that exists:

```python
        # Settings screen navigation
        self.settings_screen.back_clicked.connect(self.show_browse)  # <-- Use back_clicked
```

---

## Recommendation

**Use Option 1** for consistency with other screens.

All three screens should have the same navigation signals:
- PlayerScreen has `browse_requested` ✓
- BrowseScreen has `player_requested` and `settings_requested` ✓
- SettingsScreen should have `browse_requested` and `player_requested`

This makes the navigation system symmetric and predictable.

---

## Testing After Fix

After applying Option 1:

```bash
cd ~/deadstream
python3 test_phase8_integration.py
```

Should show:
```
[INFO] Navigation signals connected  # <-- No error message
```

---

## When to Fix

**Priority:** Low - can be deferred to Phase 9 polish

**Why it's low priority:**
1. Doesn't affect functionality
2. Navigation works via nav bar
3. SettingsScreen doesn't currently have a "go to browse" button
4. Console error only visible during development

**When to address:**
- During Phase 9 integration
- When adding back/navigation buttons to settings
- During final code cleanup before v1.0

---

## Related Files

- `src/ui/screens/settings_screen.py` - Where signal should be added
- `src/ui/main_window.py` - Where connection is attempted
- `src/ui/player_screen.py` - Reference for how signals are done
- `src/ui/screens/browse_screen.py` - Reference for navigation signals

---

**Document Status:** Reference only - fix deferred to Phase 9
