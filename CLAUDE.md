# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeadStream is a Raspberry Pi-based music player for streaming Grateful Dead concerts from the Internet Archive. Built with Python 3.9+, PyQt5, VLC, and SQLite, it features a touch-friendly interface, smart recording selection, and network-resilient audio playback.

**Current Status:** Phase 10 (Now Playing Screen) - Core functionality complete, integration and polish in progress.

## Essential Commands

### Development Setup
```bash
# Activate virtual environment (required before any Python commands)
source venv/bin/activate

# Run the application
python3 src/ui/main_window.py

# Run with X11 forwarding over SSH (for remote GUI testing)
ssh -X pi@raspberrypi
python3 src/ui/main_window.py
```

### Testing
```bash
# Run integration tests
python3 examples/test_phase8_integration.py
python3 examples/test_playback_controls.py

# Run navigation tests
python3 tests/test_navigation.py

# Run diagnostic tools (when debugging architecture issues)
python3 examples/test_mainwindow_diagnostic.py
```

### Database Management
```bash
# Initialize new database
python3 scripts/init_database.py

# Populate database with shows (~20 min, downloads ~12,000 shows)
python3 scripts/populate_database.py

# Update database with new shows
python3 scripts/update_database.py

# Validate database integrity
python3 scripts/validate_database.py
```

## Architecture Overview

### Three-Layer System Architecture

**1. Data Layer** (`src/database/`, `src/api/`)
- SQLite database with 12,268 Grateful Dead shows
- Internet Archive API integration with rate limiting
- Smart recording selection based on source type, format, and community ratings
- Database location: `data/shows.db`

**2. Audio Layer** (`src/audio/`)
- **ResilientPlayer**: Core playback with automatic retry and recovery
- **NetworkMonitor**: Detects connectivity issues
- **PositionTracker**: Throttled position updates (500ms intervals)
- **Platform-aware VLC**: Automatic macOS/Linux audio configuration via `vlc_config.py`
  - macOS: Auto-detect CoreAudio (development)
  - Linux: Force ALSA (`--aout=alsa`) for Raspberry Pi

**3. UI Layer** (`src/ui/`)
- PyQt5 event-driven architecture
- QStackedWidget with named screen registry ('player', 'browse', 'settings')
- 300ms fade animations between screens
- Keyboard shortcuts for development, touch-first design for production

### Key Components

**Screen Management:**
- `main_window.py`: Application container, navigation coordinator
- `screen_manager.py`: Handles screen transitions with animations
- `player_screen.py`: Now playing interface with playback controls
- `screens/browse_screen.py`: 6 browse modes (Top Rated, Date, Venue, Year, Search, Random)
- `screens/settings_screen.py`: Network, audio, display, database settings

**Smart Selection System:**
- `selection/scoring.py`: Weighted algorithm (source 35%, format 25%, rating 20%, lineage 10%, taper 10%)
- `selection/preferences.py`: User preference management (balanced, audiophile, crowd_favorite presets)
- `config/preferences.yaml`: Customizable scoring weights

## Critical Development Rules

### 1. Text Encoding - ASCII Only
**Never use Unicode characters (emojis, checkmarks, special symbols).** They cause syntax errors on Raspberry Pi.

```python
# CORRECT
print("[PASS] Test passed")
print("[FAIL] Test failed")
print("[INFO] Status update")

# WRONG - DO NOT USE
print("✓ Test passed")  # Syntax error
print("✗ Test failed")  # Syntax error
```

### 2. Always Use Platform-Aware VLC
**Never create VLC instances directly.** Always use `create_vlc_instance()` from `src.audio.vlc_config`.

```python
# CORRECT - Works on macOS and Linux
from src.audio.vlc_config import create_vlc_instance
instance = create_vlc_instance()
player = instance.media_player_new()

# WRONG - Platform-specific, will break
import vlc
instance = vlc.Instance('--aout=alsa')  # Only works on Linux
```

### 3. Import Patterns - Follow Project Structure

**File structure:**
```
src/
├── ui/
│   ├── main_window.py         # Top-level UI files
│   ├── player_screen.py
│   ├── screens/               # Subdirectory (needs path manipulation)
│   │   ├── browse_screen.py
│   │   └── settings_screen.py
│   └── widgets/               # Package with __init__.py
│       ├── show_list.py
│       └── network_settings_widget.py
```

**Import rules:**
- Files in `src/ui/`: Use imports directly
- Files in subdirectories (`src/ui/screens/`, `src/ui/widgets/`): Add path manipulation
- Always use full paths: `from src.module.file import Class`

```python
# For files in subdirectories (screens/, widgets/)
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now can import normally
from src.database.queries import get_shows
from src.ui.widgets.show_list import ShowListWidget
```

**Common import errors:**
- `ModuleNotFoundError: No module named 'src'` → Add path manipulation
- `ModuleNotFoundError: No module named 'screens'` → Use `src.ui.screens.module`
- Files that DON'T exist: `src/ui/theme.py`, `src/screens/` (not a package)

**See `docs/08-import-and-architecture-reference.md` for complete import patterns.**

### 4. Test URLs - Use Database, Never Hardcode
Archive.org URLs become invalid over time (404 errors). Always get test URLs from the database at runtime.

```python
# CORRECT
from src.database.queries import get_show_by_date
from src.api.metadata import get_metadata, extract_audio_files

def get_test_url():
    """Get valid test URL from database"""
    shows = get_show_by_date('1977-05-08')  # Cornell '77
    if shows:
        metadata = get_metadata(shows[0]['identifier'])
        audio_files = extract_audio_files(metadata)
        if audio_files:
            return f"https://archive.org/download/{shows[0]['identifier']}/{audio_files[0]['name']}"
    return None

# WRONG - URL will eventually 404
test_url = "https://archive.org/download/gd77-05-08.../track.mp3"
```

### 5. PyQt5 Testing - Wait for Animations
`QApplication.processEvents()` is NOT sufficient for animated transitions. Use `QTest.qWait()`.

```python
from PyQt5.QtTest import QTest

# CORRECT
window.screen_manager.show_screen('settings')
QTest.qWait(600)  # Wait for 500ms animation + buffer
current = window.screen_manager.currentWidget()

# WRONG - Race condition
window.screen_manager.show_screen('settings')
QApplication.processEvents()  # Not enough for animations
```

### 6. Settings Architecture Patterns

**Settings Screen Structure:**
```python
# Buttons stored in dictionary
settings_screen.category_buttons['network']
settings_screen.category_buttons['audio']
settings_screen.category_buttons['display']

# Content widgets as attributes
settings_screen.network_widget
settings_screen.content_stack  # NOT details_stack
```

**Screen references:**
- Stored on MainWindow: `window.player_screen`, `window.browse_screen`, `window.settings_screen`
- Accessed via ScreenManager: `window.screen_manager.screens` dictionary

## Configuration Files

**Location:** `config/`
- `settings.yaml`: User preferences (network, audio, display, datetime)
- `preferences.yaml`: Recording selection weights
- `rate_limit_config.yaml`: Archive.org API rate limits

**Settings persistence:** Uses YAML with schema validation. Network settings, volume, brightness, etc. persist across sessions.

## Testing Guidelines

**Integration tests before declaring phase complete.** Unit tests defer to individual component validation.

**Common patterns:**
```python
# Wait for screen transitions
def wait_for_transition(ms=600):
    QTest.qWait(ms)

# Check widget existence before using
if not hasattr(screen, 'volume_slider'):
    print(f"[FAIL] Missing volume_slider attribute")
    return False
```

**Test file organization:**
- Integration tests: `examples/test_*.py`
- Navigation tests: `tests/test_*.py`
- Diagnostic tools: `examples/*_diagnostic.py`

**See `docs/09-testing-lessons-learned.md` for detailed testing patterns and common pitfalls.**

## Performance Targets

- Boot time: < 30 seconds to ready
- Search response: < 1 second
- Playback start: < 3 seconds from selection
- UI responsiveness: < 100ms for touch response
- Database query: < 100ms for typical searches

## Display Configuration

- **Resolution:** 1280x720 (landscape orientation)
- **Touch targets:** Minimum 60x60px (validated on 7" touchscreen)
- **Button sizing:** Primary 80x80px, Standard 60x60px, Secondary 50x50px
- **Development mode:** Windowed for desktop, fullscreen code ready for deployment

## Development Workflow

**Desktop development (macOS/Linux):**
1. Edit code in VS Code or preferred editor
2. Run with `python3 src/ui/main_window.py` in windowed mode
3. Use keyboard shortcuts for quick navigation
4. Test with mouse (PyQt5 auto-converts to touch events)

**Raspberry Pi testing:**
1. SSH with X11 forwarding: `ssh -X pi@raspberrypi`
2. Same commands work remotely
3. Audio outputs to Pi's headphone jack (ALSA)
4. Touch testing on physical touchscreen

**Cross-platform audio:** Same codebase automatically configures for macOS CoreAudio (dev) or Linux ALSA (production).

## Important Documentation References

Before implementing features, consult:
- `docs/07-project-guidelines.md`: Coding standards, critical rules
- `docs/08-import-and-architecture-reference.md`: File structure, import patterns, package organization
- `docs/09-testing-lessons-learned.md`: Testing patterns, PyQt5 gotchas, integration testing
- `docs/05-technical-decisions.md`: Architecture decisions, technology choices
- `docs/database-schema.md`: Database structure and query patterns

## Common Issues and Solutions

**"Architecture mismatch error on Apple Silicon Mac"**
- VLC is x86_64 but Mac is ARM: `brew uninstall vlc && brew install --cask vlc`

**"No audio on macOS during development"**
- Using Linux-specific `--aout=alsa`: Use `create_vlc_instance()` instead

**"ModuleNotFoundError: No module named 'X'"**
- Import path doesn't match structure: Check `docs/08-import-and-architecture-reference.md`

**"Screen transition test fails"**
- Not waiting for animation: Use `QTest.qWait(600)` after `show_screen()`

**"Archive.org returns 404"**
- Hardcoded URL is outdated: Use database-driven URL selection

## Phase-Specific Notes

**Current Phase (10):** Now Playing Screen implementation
- Player controls integrated with ResilientPlayer
- Progress bar with position tracking
- Auto-play next track functionality
- Error UI for playback failures

**Completed Phases:**
- Phase 1-3: Foundation, API, Database
- Phase 4: Audio playback engine with network resilience
- Phase 5: Smart recording selection algorithm
- Phase 6: PyQt5 UI framework with screen management
- Phase 7: Browse interface (6 modes)
- Phase 8: Settings screen with persistence
- Phase 9: Integration and polish

**Next Phases:**
- Phase 11: Hardware integration (DAC, touchscreen)
- Phase 12: Case design and assembly
- Phase 13: Final testing and documentation
