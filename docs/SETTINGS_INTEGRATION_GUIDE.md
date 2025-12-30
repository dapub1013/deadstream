# Settings Integration Guide
**Phase 8, Task 8.4: Settings Persistence**

This guide shows how to integrate the SettingsManager with UI components.

## Overview

The `SettingsManager` provides centralized configuration storage using YAML files. Settings are automatically saved whenever changed and loaded on startup.

### File Location
- **Settings file:** `config/settings.yaml`
- **Source code:** `src/settings/settings_manager.py`

---

## Basic Usage

### Getting the Global Settings Instance

```python
from src.settings.settings_manager import get_settings

settings = get_settings()
```

The `get_settings()` function returns a singleton instance, so all parts of your app share the same settings object.

### Reading Settings

```python
# Get a single setting
volume = settings.get('audio', 'default_volume')  # Returns 75 (default)
brightness = settings.get('display', 'brightness')  # Returns 80 (default)

# Get a setting with custom default
timeout = settings.get('display', 'screen_timeout', default=600)

# Get all settings in a category
audio_settings = settings.get_category('audio')
# Returns: {'default_volume': 75, 'quality_preference': 'balanced', ...}
```

### Writing Settings

```python
# Set a single setting (auto-saves)
settings.set('audio', 'default_volume', 85)

# Set multiple settings in a category
new_audio = {
    'default_volume': 90,
    'quality_preference': 'audiophile',
    'auto_play_on_startup': True
}
settings.set_category('audio', new_audio)

# Reset a category to defaults
settings.reset_category('audio')

# Reset all settings
settings.reset_all()
```

---

## Settings Categories

### Network Settings
```python
# Access network settings
auto_connect = settings.get('network', 'auto_connect')  # True/False
last_ssid = settings.get('network', 'last_connected_ssid')  # String or None
prefer_5ghz = settings.get('network', 'prefer_5ghz')  # True/False

# Save WiFi connection
settings.set('network', 'last_connected_ssid', 'MyNetwork')
settings.set('network', 'auto_connect', True)
```

### Audio Settings
```python
# Get audio preferences
volume = settings.get('audio', 'default_volume')  # 0-100
quality = settings.get('audio', 'quality_preference')  # balanced/audiophile/crowd_favorite
autoplay = settings.get('audio', 'auto_play_on_startup')  # True/False
crossfade = settings.get('audio', 'crossfade_enabled')  # True/False

# Update audio settings
settings.set('audio', 'default_volume', 80)
settings.set('audio', 'quality_preference', 'audiophile')
```

### Display Settings
```python
# Get display preferences
brightness = settings.get('display', 'brightness')  # 0-100
auto_bright = settings.get('display', 'auto_brightness')  # True/False
timeout = settings.get('display', 'screen_timeout')  # seconds
theme = settings.get('display', 'theme')  # 'dark' or 'light'

# Update display settings
settings.set('display', 'brightness', 90)
settings.set('display', 'screen_timeout', 600)
```

### Date/Time Settings
```python
# Get datetime preferences
timezone = settings.get('datetime', 'timezone')  # e.g., 'America/New_York'
format_24h = settings.get('datetime', 'time_format_24h')  # True/False
date_format = settings.get('datetime', 'date_format')  # 'US' or 'International'

# Update datetime settings
settings.set('datetime', 'timezone', 'America/Los_Angeles')
settings.set('datetime', 'time_format_24h', True)
```

### App Settings
```python
# Get app preferences
last_screen = settings.get('app', 'last_screen')  # 'player', 'browse', 'settings'
show_splash = settings.get('app', 'show_splash')  # True/False
check_updates = settings.get('app', 'check_updates')  # True/False

# Update app settings
settings.set('app', 'last_screen', 'browse')
```

---

## UI Integration Examples

### Example 1: Network Settings Widget

```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLineEdit
from src.settings.settings_manager import get_settings

class NetworkSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Auto-connect checkbox
        self.auto_connect_cb = QCheckBox("Auto-connect on startup")
        self.auto_connect_cb.stateChanged.connect(self.on_auto_connect_changed)
        layout.addWidget(self.auto_connect_cb)
        
        # Prefer 5GHz checkbox
        self.prefer_5ghz_cb = QCheckBox("Prefer 5GHz networks")
        self.prefer_5ghz_cb.stateChanged.connect(self.on_prefer_5ghz_changed)
        layout.addWidget(self.prefer_5ghz_cb)
    
    def load_settings(self):
        """Load current settings into UI"""
        auto_connect = self.settings.get('network', 'auto_connect')
        self.auto_connect_cb.setChecked(auto_connect)
        
        prefer_5ghz = self.settings.get('network', 'prefer_5ghz')
        self.prefer_5ghz_cb.setChecked(prefer_5ghz)
    
    def on_auto_connect_changed(self, state):
        """Save auto-connect preference"""
        self.settings.set('network', 'auto_connect', bool(state))
    
    def on_prefer_5ghz_changed(self, state):
        """Save 5GHz preference"""
        self.settings.set('network', 'prefer_5ghz', bool(state))
```

### Example 2: Audio Settings with Slider

```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from src.settings.settings_manager import get_settings

class AudioSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Volume label
        self.volume_label = QLabel("Default Volume: 75")
        layout.addWidget(self.volume_label)
        
        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        layout.addWidget(self.volume_slider)
    
    def load_settings(self):
        """Load current volume setting"""
        volume = self.settings.get('audio', 'default_volume')
        self.volume_slider.setValue(volume)
        self.volume_label.setText(f"Default Volume: {volume}")
    
    def on_volume_changed(self, value):
        """Save volume setting and update label"""
        self.settings.set('audio', 'default_volume', value)
        self.volume_label.setText(f"Default Volume: {value}")
```

### Example 3: Remember Last Screen

```python
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from src.settings.settings_manager import get_settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        self.init_ui()
        self.restore_last_screen()
    
    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Add screens
        self.stacked_widget.addWidget(PlayerScreen())    # index 0
        self.stacked_widget.addWidget(BrowseScreen())    # index 1
        self.stacked_widget.addWidget(SettingsScreen())  # index 2
    
    def restore_last_screen(self):
        """Show the screen user was last viewing"""
        last_screen = self.settings.get('app', 'last_screen', 'browse')
        
        screen_map = {
            'player': 0,
            'browse': 1,
            'settings': 2
        }
        
        index = screen_map.get(last_screen, 1)  # Default to browse
        self.stacked_widget.setCurrentIndex(index)
    
    def show_screen(self, screen_name):
        """Show a screen and remember it"""
        screen_map = {
            'player': 0,
            'browse': 1,
            'settings': 2
        }
        
        index = screen_map.get(screen_name, 1)
        self.stacked_widget.setCurrentIndex(index)
        
        # Save as last screen
        self.settings.set('app', 'last_screen', screen_name)
```

### Example 4: Display Brightness Control

```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from src.settings.settings_manager import get_settings
import subprocess

class DisplaySettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Brightness label
        self.brightness_label = QLabel("Brightness: 80%")
        layout.addWidget(self.brightness_label)
        
        # Brightness slider
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(10, 100)  # Min 10% to keep visible
        self.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        layout.addWidget(self.brightness_slider)
    
    def load_settings(self):
        """Load current brightness setting"""
        brightness = self.settings.get('display', 'brightness')
        self.brightness_slider.setValue(brightness)
        self.update_brightness_label(brightness)
        self.apply_brightness(brightness)
    
    def on_brightness_changed(self, value):
        """Save and apply brightness"""
        self.settings.set('display', 'brightness', value)
        self.update_brightness_label(value)
        self.apply_brightness(value)
    
    def update_brightness_label(self, value):
        """Update label text"""
        self.brightness_label.setText(f"Brightness: {value}%")
    
    def apply_brightness(self, value):
        """Apply brightness to actual display (Raspberry Pi)"""
        try:
            # For Raspberry Pi touchscreen
            brightness_value = int((value / 100) * 255)
            subprocess.run([
                'bash', '-c',
                f'echo {brightness_value} > /sys/class/backlight/rpi_backlight/brightness'
            ])
        except Exception as e:
            print(f"[WARN] Could not apply brightness: {e}")
```

---

## Validation

Always validate settings before applying critical changes:

```python
settings = get_settings()

# Validate all settings
warnings = settings.validate_settings()
if warnings:
    for warning in warnings:
        print(f"[WARN] {warning}")
```

---

## Export/Import (Backup/Restore)

```python
settings = get_settings()

# Backup settings
success = settings.export_settings('/home/david/deadstream/backups/settings_backup.yaml')
if success:
    print("[OK] Settings backed up")

# Restore settings
success = settings.import_settings('/home/david/deadstream/backups/settings_backup.yaml')
if success:
    print("[OK] Settings restored")
```

---

## Default Settings Reference

```yaml
network:
  auto_connect: true
  last_connected_ssid: null
  prefer_5ghz: true

audio:
  default_volume: 75
  quality_preference: balanced  # balanced, audiophile, crowd_favorite
  auto_play_on_startup: false
  crossfade_enabled: false

display:
  brightness: 80
  auto_brightness: false
  screen_timeout: 300  # seconds
  theme: dark

datetime:
  timezone: America/New_York
  time_format_24h: false
  date_format: US  # US or International

app:
  last_screen: browse  # player, browse, settings
  show_splash: true
  check_updates: true
  last_update_check: null

version: 0.1.0
last_modified: <timestamp>
```

---

## Best Practices

1. **Use get_settings()** - Always use the global instance to ensure consistency
2. **Auto-save** - Settings save automatically on `set()` calls
3. **Provide defaults** - Always provide sensible defaults with `get()`
4. **Validate** - Validate settings before critical operations
5. **Handle errors** - Check return values from `set()` operations
6. **Update UI on load** - Call `load_settings()` in your widget's `__init__`
7. **Save on change** - Save settings immediately when user changes them

---

## Testing

Run the comprehensive test suite:

```bash
cd ~/deadstream
python3 examples/test_settings_manager.py
```

This tests:
- Basic get/set operations
- Category operations
- Validation
- Export/import
- Global instance
- Merge with defaults (version upgrades)

---

## Migration from Phase 5 Preferences

The Phase 5 `PreferenceManager` is still used for smart show selection weights. The new `SettingsManager` handles broader application configuration.

**When to use which:**
- **SettingsManager**: UI preferences, system configuration, network settings
- **PreferenceManager**: Show selection scoring weights only

Both systems use YAML and work together:
```python
# General app settings
from src.settings.settings_manager import get_settings
settings = get_settings()
volume = settings.get('audio', 'default_volume')

# Show selection preferences
from src.selection.preferences import PreferenceManager
prefs = PreferenceManager()
weights = prefs.get_weights()
```

---

**Task 8.4 Complete!**
