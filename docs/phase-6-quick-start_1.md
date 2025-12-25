# Phase 6 Quick Start - Basic UI Framework

**Status:** Ready to Begin  
**Prerequisites:** All met ✅  
**Date Created:** December 24, 2025

---

## What Phase 6 Builds

**Objective:** Create the foundation PyQt5 touchscreen interface that will integrate all backend functionality built in Phases 1-5.

**Duration Estimate:** 2-3 weeks (likely ~1 week at current pace)

---

## What's Already Complete

✅ **Phase 1:** Raspberry Pi environment ready  
✅ **Phase 2:** Internet Archive API integration  
✅ **Phase 3:** Database with 12,268 shows  
✅ **Phase 4:** Audio playback engine  
✅ **Phase 5:** Smart show selection with user preferences

**Backend is 100% ready for UI integration.**

---

## Phase 6 Tasks Overview

### 6.1: Learn PyQt5 Fundamentals
- Basic window creation
- Widget fundamentals
- Layout managers
- Event handling
- Signal/slot connections

### 6.2: Create Main Window
- Application shell
- Window configuration for 7" screen
- Navigation structure
- Basic theming

### 6.3: Build Basic Navigation
- Screen stack management
- Navigation buttons
- Screen transitions
- Back button functionality

### 6.4: Test Touch Responsiveness
- Touch event handling
- Button sizing (60x60px standard)
- Gesture support
- Edge case testing

### 6.5: Implement Screen Transitions
- Smooth animations
- State preservation
- Loading indicators
- Error state handling

### 6.6: Add Keyboard Input (for testing)
- Keyboard shortcuts
- Development convenience
- Testing without touchscreen

---

## Available Resources

### Design Specifications
- **ui-design-specification.md** - Complete UI design
- **manual-override-ui-concept.md** - Manual selection UI
- **07-project-guidelines.md** - Coding standards

### Backend Integration Points
```python
# Show selection (Phase 5)
from selection.selector import ShowSelector
selector = ShowSelector()
best = selector.select_for_date('1977-05-08')

# Audio playback (Phase 4)
from audio.resilient_player import ResilientPlayer
player = ResilientPlayer()

# Database queries (Phase 3)
from database.queries import (
    get_show_by_identifier,
    get_shows_by_date_range,
    get_random_show
)
```

---

## Development Environment

### Testing Setup
```bash
# SSH to Pi for testing
ssh pi@deadstream.local

# Activate virtual environment
cd ~/deadstream
source venv/bin/activate

# Run PyQt5 apps
python src/ui/main_window.py
```

### Git Workflow
```bash
# Create Phase 6 feature branch
git checkout -b phase-6-ui-framework

# Regular commits
git add .
git commit -m "[PHASE-6] Task 6.1: PyQt5 basics learned"

# Push to remote
git push origin phase-6-ui-framework
```

---

## Key Technical Decisions

### Display Configuration
- **Resolution:** 1280x720 (landscape)
- **Target:** 7" Touch Display 2
- **Current:** HDMI monitor + mouse (until Phase 11)

### Button Standards
- **Size:** 60x60px for primary controls
- **Minimum:** 44x44px for secondary actions
- **Spacing:** 8-12px between elements

### PyQt5 Patterns
- **Layout:** QVBoxLayout, QHBoxLayout for structure
- **Widgets:** QPushButton, QLabel, QListWidget
- **Events:** Click, touch, keyboard
- **Styling:** QSS (Qt Style Sheets) for theming

---

## Integration Points from Previous Phases

### Database (Phase 3)
```python
# Example: Get shows for browse screen
shows = get_shows_by_year(1977)
for show in shows:
    print(f"{show['date']} - {show['venue']}")
```

### Smart Selection (Phase 5)
```python
# Automatic selection
selector = ShowSelector()
best_id = selector.select_for_date('1977-05-08')

# Manual selection with options
options = selector.get_options_for_date('1977-05-08')
# Display options in UI
# User selects one
chosen_id = options[user_choice]['identifier']
```

### Audio Playback (Phase 4)
```python
# Play selected show
player = ResilientPlayer()
player.load_show(identifier)
player.play()

# Control playback
player.pause()
player.set_volume(75)
player.skip_to_track(3)
```

---

## Success Criteria for Phase 6

- [ ] PyQt5 fundamentals understood and documented
- [ ] Main application window runs on Pi
- [ ] Basic navigation between screens works
- [ ] Touch events handled correctly (or mouse for now)
- [ ] Screen transitions smooth and intuitive
- [ ] Keyboard shortcuts work for development
- [ ] Code follows project guidelines
- [ ] All tests passing
- [ ] Documentation complete

---

## First Session Checklist

When starting Phase 6:

1. **Read Documentation**
   - Review `ui-design-specification.md`
   - Check `07-project-guidelines.md`
   - Skim PyQt5 basics tutorial

2. **Set Up Git**
   ```bash
   git checkout -b phase-6-ui-framework
   ```

3. **Create Directory Structure**
   ```bash
   mkdir -p src/ui
   mkdir -p src/ui/widgets
   mkdir -p src/ui/screens
   ```

4. **Start with Task 6.1**
   - Learn PyQt5 basics
   - Create simple "Hello World" window
   - Test on Pi via SSH + X11 forwarding or VNC

5. **Document Learning**
   - Take notes on PyQt5 concepts
   - Track gotchas and solutions
   - Update technical decisions as needed

---

## Common Gotchas to Watch For

### PyQt5 on Raspberry Pi
- Use system-installed PyQt5 (already in venv with --system-site-packages)
- Don't pip install PyQt5 (won't work on Pi)
- X11 forwarding can be slow - use VNC or test on physical screen

### Display Server
- Wayland is working well (verified in Phase 1)
- No changes needed from current setup

### Performance
- Keep UI updates to 60fps minimum
- Lazy load show lists (don't load all 12,000 at once)
- Use threading for database queries
- Cache frequently accessed data

---

## Resources

### Official Documentation
- PyQt5 Docs: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- Qt Documentation: https://doc.qt.io/qt-5/
- Python Qt Tutorial: https://realpython.com/python-pyqt-gui-calculator/

### Project Documentation
- `ui-design-specification.md` - Complete design reference
- `phase-5-completion-summary.md` - Smart selection integration
- `phase-4-completion-summary.md` - Audio playback integration
- `07-project-guidelines.md` - Coding standards

---

## Questions to Answer in Phase 6

- What's the best way to handle screen navigation?
- Should we use Qt Designer or code layouts directly?
- How do we handle screen rotation (if needed)?
- What's the optimal way to load show lists?
- How do we test touch without the touchscreen yet?

---

**Ready to Begin Phase 6!**  
All prerequisites complete. Backend systems tested and working.  
Time to build the user interface that brings it all together.

---

*Last Updated: December 24, 2025*  
*Next: Start Task 6.1 - Learn PyQt5 Fundamentals*
