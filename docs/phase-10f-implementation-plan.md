# Phase 10F Implementation Plan: Now Playing Bar Lite

**Objective:** Add persistent playback control bar at bottom of browse/settings screens  
**Execution:** Task-by-task (do not implement all at once)  
**Duration:** ~4 hours total across 6 tasks  
**Date Created:** January 12, 2026

---

## Design Specification

**Widget Requirements:**
- Height: 80px total (60px buttons + padding)
- Position: Bottom of screen, full width (1280px)
- Background: Pure black (matches player screen right panel)
- Layout: `[Track Info - expanding] [Prev] [Play/Pause] [Next]`
- Visibility: Show when audio loaded AND not on player screen

**Key Principle:** Reference `src/ui/styles/theme.py` for all styling - NO hardcoded values

---

## Task 10F.1: Create NowPlayingBar Widget

**File to Create:** `src/ui/widgets/now_playing_bar.py`

**Reference Files:**
- `src/ui/styles/theme.py` - All colors, spacing, typography
- `src/ui/components/icon_button.py` - For playback control buttons
- `src/ui/screens/player_screen.py` - Track info display patterns

**Widget Structure:**
```python
class NowPlayingBar(QWidget):
    """
    Minimal playback control bar for browse/settings screens.
    Shows track info and essential controls.
    """
    # Signals
    player_requested = pyqtSignal()  # User clicked bar to view player
    play_pause_clicked = pyqtSignal()
    next_clicked = pyqtSignal()
    previous_clicked = pyqtSignal()
```

**Layout:**
- Main horizontal layout with two sections
- Left: Track info (QLabel stack - title + show info)
- Right: Three IconButtons (prev, play/pause, next) at 60x60px

**Styling:**
- Use `Theme.BG_PLAYER_BLACK` for background
- Use `Theme.BORDER_PANEL` for top border
- Use `Theme.TEXT_PRIMARY` and `Theme.TEXT_SECONDARY` for labels
- Use `Theme.BODY_LARGE` and `Theme.BODY_SMALL` for font sizes
- Use `Theme.SPACING_*` constants for padding

**Mouse Interaction:**
- Entire widget clickable → emit `player_requested`
- Control buttons stop event propagation

**Acceptance Criteria:**
- [ ] Widget renders with correct layout
- [ ] All styling from Theme.py (zero hardcoded values)
- [ ] Buttons are 60x60px
- [ ] Signals defined and emit correctly
- [ ] Widget follows project patterns from player_screen.py

**Estimated Time:** 60 minutes

---

## Task 10F.2: Integrate with ResilientPlayer

**File to Modify:** `src/ui/widgets/now_playing_bar.py`

**Reference Files:**
- `src/audio/resilient_player.py` - Player interface
- `src/ui/screens/player_screen.py` - Player integration patterns (see `init_audio_integration()`)

**Methods to Add:**
```python
def set_player(self, player):
    """Connect to ResilientPlayer instance"""
    
def update_from_player(self):
    """Update UI from current player state - called by timer"""
    
def load_track_info(self, track_name, show_date, show_venue):
    """Set track and show information"""
```

**Integration Pattern:**
- Create QTimer (200ms interval, same as player_screen.py)
- Connect timer to `update_from_player()` method
- Read player state each update: `is_playing()`, `get_current_track_info()`
- Update play/pause button icon based on state
- Connect button signals to player methods

**Acceptance Criteria:**
- [ ] Widget connected to ResilientPlayer
- [ ] Timer-based updates working (200ms)
- [ ] Play/pause button shows correct icon
- [ ] Track info updates when track changes
- [ ] Controls affect playback correctly
- [ ] Follow patterns from player_screen.py

**Estimated Time:** 45 minutes

---

## Task 10F.3: Add to MainWindow Layout

**File to Modify:** `src/ui/main_window.py`

**Reference Files:**
- `src/ui/screen_manager.py` - Current screen tracking
- `src/ui/screens/player_screen.py` - Player reference

**Implementation Strategy:**
1. Create container widget (QWidget) with QVBoxLayout
2. Add ScreenManager to container (expand to fill)
3. Add NowPlayingBar to container (fixed 80px height)
4. Set container as central widget (replace direct ScreenManager)
5. Connect bar's `player_requested` signal to `show_player()`
6. Pass player reference to bar via `set_player()`

**Visibility Logic:**
```python
def update_now_playing_bar_visibility(self):
    """Show bar only when audio loaded and not on player screen"""
    current_screen = self.screen_manager.current_screen_name
    has_audio = self.player.has_media_loaded()
    
    show_bar = has_audio and current_screen != ScreenManager.PLAYER_SCREEN
    self.now_playing_bar.setVisible(show_bar)
```

**Call visibility update:**
- After screen changes (connect to `screen_manager.screen_changed`)
- After loading new show
- In `on_screen_changed()` method

**Acceptance Criteria:**
- [ ] Bar appears at bottom when audio loaded
- [ ] Bar hidden on player screen
- [ ] Bar hidden when no audio loaded
- [ ] Clicking bar navigates to player
- [ ] Container layout works correctly
- [ ] No layout issues or overlaps

**Estimated Time:** 30 minutes

---

## Task 10F.4: Handle Screen Layout Adjustments

**Files to Check:**
- `src/ui/screens/browse_screen.py`
- `src/ui/screens/settings_screen.py`

**Goal:** Verify screens don't overlap with 80px bar at bottom

**Approach:**
1. Test browse screen with bar visible
   - Verify show list scrolls without content hidden
   - Check bottom item fully visible above bar
   
2. Test settings screen with bar visible
   - Verify settings content scrollable
   - Check bottom setting not hidden

**If Overlap Issues Found:**
- Add bottom margin: `layout.setContentsMargins(0, 0, 0, 80)`
- Or adjust container layout to reserve space
- Or ensure QScrollArea handles it automatically

**Likely Outcome:** May not need any changes if QVBoxLayout in MainWindow handles it correctly

**Acceptance Criteria:**
- [ ] Browse screen content fully visible above bar
- [ ] Settings screen content fully visible above bar  
- [ ] Scrolling works correctly with bar present
- [ ] No content hidden behind bar
- [ ] Player screen uses full height (bar hidden)

**Estimated Time:** 45 minutes

---

## Task 10F.5: Create Test Script

**File to Create:** `examples/test_now_playing_bar.py`

**Reference Files:**
- `examples/test_player_screen.py` - Similar testing pattern
- `examples/get_test_url.py` - Get valid test URL from database

**Test Script Structure:**
```python
class TestWindow(QMainWindow):
    """Test window for NowPlayingBar widget"""
    
    def __init__(self):
        # Create ResilientPlayer
        # Create NowPlayingBar
        # Connect signals
        # Load test track
        # Show test UI
        
    def load_test_track(self):
        # Use get_test_url() pattern
        # Load audio into player
        # Set track info on bar
```

**Test Checklist:**
- Visual: 80px height, black background, proper spacing
- Visual: Track info displays correctly
- Visual: All buttons 60x60px
- Functional: Play/pause toggles icon
- Functional: Prev/next buttons work
- Functional: Clicking bar prints signal
- Integration: Real-time updates from player

**Acceptance Criteria:**
- [ ] Test script runs without errors
- [ ] All visual checks pass
- [ ] Playback controls functional
- [ ] Bar click navigation signal works
- [ ] Real-time updates working
- [ ] Follows 07-project-guidelines.md (ASCII only, no hardcoded URLs)

**Estimated Time:** 30 minutes

---

## Task 10F.6: Documentation

**File to Create:** `phase-10f-completion-summary.md`

**Reference Files:**
- `phase-10c-completion-summary.md` - Follow this structure
- `phase-10d-completion-summary.md` - Another good example

**Sections to Include:**
1. Executive Summary
2. Objectives Completed
3. Implementation Summary
4. Testing Results
5. Integration Points
6. Known Limitations
7. Git Workflow
8. Success Metrics

**Code Documentation:**
- Add comprehensive docstrings to NowPlayingBar class
- Document all signals
- Document all public methods
- Add usage examples

**Acceptance Criteria:**
- [ ] Completion summary created
- [ ] All code documented with docstrings
- [ ] Integration examples provided
- [ ] Testing results documented
- [ ] Git workflow documented
- [ ] Ready for phase review

**Estimated Time:** 30 minutes

---

## Critical Project Guidelines

**From 07-project-guidelines.md:**
1. **ASCII Only** - No unicode/emoji in code or print statements
2. **Theme Manager** - All styling from `src/ui/styles/theme.py`
3. **No Hardcoded URLs** - Use database for test URLs
4. **Platform-Aware VLC** - Use `create_vlc_instance()` from `src/audio/vlc_config.py`
5. **Import Patterns** - Follow structure in `08-import-and-architecture-reference.md`

**Existing Patterns to Follow:**
- Signal/slot architecture (see player_screen.py)
- Timer-based UI updates (200ms interval)
- IconButton for playback controls (60x60px standard)
- Theme Manager for all styling
- Widget-based architecture

---

## Git Commit Pattern

```bash
git commit -m "[Phase-10F] Task 10F.X: Brief description of what was done"
```

**Example:**
```bash
git commit -m "[Phase-10F] Task 10F.1: Create NowPlayingBar widget with layout and controls"
```

---

## Timeline Summary

| Task | Description | Time |
|------|-------------|------|
| 10F.1 | Create NowPlayingBar widget | 60 min |
| 10F.2 | Integrate with ResilientPlayer | 45 min |
| 10F.3 | Add to MainWindow layout | 30 min |
| 10F.4 | Screen layout adjustments | 45 min |
| 10F.5 | Create test script | 30 min |
| 10F.6 | Documentation | 30 min |
| **Total** | | **240 min (4 hours)** |

---

## Success Criteria Summary

**Phase 10F is complete when:**
- [ ] All 6 tasks completed and committed
- [ ] Bar displays on browse/settings screens when audio loaded
- [ ] Bar hidden on player screen
- [ ] All playback controls work correctly
- [ ] Clicking bar navigates to player
- [ ] Zero hardcoded styling (100% Theme Manager)
- [ ] Test script passes all checks
- [ ] Works on both macOS and Raspberry Pi
- [ ] Documentation complete
- [ ] Zero technical debt

---

## Functional Requirements

**The Now Playing Bar must:**
1. Display current track name and show information
2. Provide play/pause, next, and previous controls
3. Update in real-time as playback state changes
4. Navigate to full player screen when clicked
5. Only appear when audio is loaded
6. Hide automatically on player screen
7. Not obstruct content on browse/settings screens

---

## Visual Requirements

**The Now Playing Bar must:**
1. Be 80px total height
2. Use 60x60px buttons (touch-friendly)
3. Have black background matching player screen
4. Use Theme Manager colors throughout
5. Display clear, readable track information
6. Show proper play/pause icon state
7. Have professional, polished appearance

---

## Technical Requirements

**The implementation must:**
1. Use zero hardcoded values (100% Theme Manager)
2. Follow PyQt5 signal/slot architecture
3. Update efficiently via 200ms timer
4. Have no performance impact on UI
5. Work cross-platform (macOS + Raspberry Pi)
6. Follow all guidelines in 07-project-guidelines.md
7. Maintain zero technical debt

---

## Notes for Claude Code

**Start with:** Task 10F.1 only - create the widget with proper layout and styling

**After each task:**
1. Test the implementation
2. Verify acceptance criteria
3. Commit with proper message
4. Request next task

**Reference existing code liberally:**
- Don't reinvent patterns that already exist
- Follow the player_screen.py approach for player integration
- Use IconButton component (already exists)
- Use Theme constants (already defined)

**Do not:**
- Implement multiple tasks at once
- Hardcode any styling values
- Skip testing before moving to next task
- Deviate from established project patterns

---

## Risk Assessment

**Low Risk:**
- Widget creation (straightforward PyQt5)
- Player integration (existing patterns)
- Theme styling (established system)

**Medium Risk:**
- Layout adjustments (may need iteration to get right)
- Visibility logic (edge cases to handle)
- Screen overlap prevention (needs careful testing)

**Mitigation:**
- Test each task individually before moving forward
- Use existing PlayerScreen as reference implementation
- Validate on actual hardware early and often
- Keep V1 scope minimal (can enhance in Phase 12)

---

## After Phase 10F

With the now playing bar complete, the application will have:
- Full playback control from any screen
- Quick navigation back to full player
- Professional music player UX
- Ready for hardware integration (Phase 11)

**Next Phases:**
- **Phase 11:** Hardware Integration (touchscreen + DAC)
- **Phase 12:** Final Polish & Features
- **Phase 13:** Documentation & Release

---

## Context for AI Assistant

**Project:** DeadStream - Grateful Dead concert player on Raspberry Pi  
**Current State:** Phase 10 (UI Polish) - 85% complete  
**Display:** 7-inch touchscreen, 1280x720 landscape orientation  
**Framework:** PyQt5 with custom Theme Manager system  
**Audio:** ResilientPlayer with VLC backend  

**Key Project Principles:**
- Quality over speed (zero technical debt)
- Follow established patterns
- Test before moving forward
- Document as you go

---

**Ready to begin with Task 10F.1**

**This document should be referenced before starting each task to ensure proper implementation approach and acceptance criteria are met.**
