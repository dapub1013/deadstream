# Phase 10 Manual Test Checklist

**Purpose:** Pre-hardware testing checklist for Phase 11 integration
**Date:** January 9, 2026
**Status:** Ready for use
**Platform:** macOS (development) and Raspberry Pi 4 (production)

This checklist covers manual testing that cannot be automated. Complete all sections before beginning Phase 11 hardware integration.

---

## Testing Instructions

### Test Environment Setup

**macOS Development:**
```bash
cd /path/to/deadstream
source venv/bin/activate
python3 src/ui/main_window.py
```

**Raspberry Pi:**
```bash
ssh -X pi@raspberrypi
cd ~/deadstream
python3 src/ui/main_window.py
```

### Marking Tests

- ✓ = Pass
- ✗ = Fail (document issue)
- ~ = Partial pass (note concerns)
- N/A = Not applicable

---

## Section 1: Visual Consistency

### 1.1 Color Consistency

**Test:** All screens use Theme Manager colors (no hardcoded values)

- [ ] Welcome screen background is purple gradient
- [ ] Player screen left panel is navy blue (#1e2936)
- [ ] Player screen right panel is pure black (#000000)
- [ ] Browse screen uses purple background
- [ ] Settings screen uses purple background
- [ ] All text is white (#FFFFFF) or gray (#B0B0B0)
- [ ] All yellow accents use #FFD700
- [ ] All blue accents use #1976D2

**Notes:**
_______________________________________________________________________

### 1.2 Typography Consistency

**Test:** All text follows typography scale

- [ ] Headers use 48px, 36px, or 28px sizes
- [ ] Body text uses 20px, 16px, or 14px sizes
- [ ] All text uses Arial font
- [ ] Bold weights used for emphasis only
- [ ] Text is readable at arm's length

**Notes:**
_______________________________________________________________________

### 1.3 Spacing Consistency

**Test:** All spacing follows 8px grid

- [ ] Padding around screens is 48px
- [ ] Padding inside panels is 32px
- [ ] Spacing between buttons is 24px
- [ ] Spacing between sections is 32px+
- [ ] No arbitrary spacing values visible

**Notes:**
_______________________________________________________________________

---

## Section 2: Component Library

### 2.1 PillButton Component

**Test:** All PillButton variants work correctly

- [ ] Blue variant displays with blue background
- [ ] Yellow variant displays with yellow background
- [ ] Green variant displays with green background
- [ ] Red variant displays with red background
- [ ] Outline variant shows transparent with border
- [ ] All buttons are at least 60px tall
- [ ] Hover state shows brightness increase
- [ ] Click provides visual feedback

**Notes:**
_______________________________________________________________________

### 2.2 IconButton Component

**Test:** All IconButton types work correctly

- [ ] Home button (⌂) displays correctly
- [ ] Settings button (⚙) displays correctly
- [ ] Play button (▶) displays correctly
- [ ] Pause button displays correctly
- [ ] All icon buttons are at least 60px diameter
- [ ] Hover state increases opacity/brightness
- [ ] Buttons are circular (not oval)

**Notes:**
_______________________________________________________________________

### 2.3 Badge Components

**Test:** Badges display correctly

**SourceBadge:**
- [ ] "SBD" badge is yellow with dark text
- [ ] "AUD" badge is yellow with dark text
- [ ] Badge is 32px tall, pill-shaped
- [ ] Text is bold and readable

**RatingBadge:**
- [ ] Rating displays as circular badge
- [ ] Yellow background (#FFD700)
- [ ] Dark purple text (#2E2870)
- [ ] 40px diameter
- [ ] Rating format: "4.5" (one decimal)

**Notes:**
_______________________________________________________________________

### 2.4 ConcertListItem Component

**Test:** List items display correctly

- [ ] Date shows in MM/DD/YYYY format
- [ ] Venue name is bold, white text
- [ ] Location shows in gray text
- [ ] Rating badge appears on right
- [ ] Source badge appears on right
- [ ] Item height is at least 80px
- [ ] Hover state shows background change
- [ ] Click selects the show

**Notes:**
_______________________________________________________________________

---

## Section 3: Screen Functionality

### 3.1 Welcome Screen

**Test:** Welcome screen displays and navigates correctly

- [ ] Purple gradient background displays
- [ ] Logo/header centered vertically
- [ ] "Browse Shows" button visible (blue)
- [ ] "Surprise Me" button visible (yellow)
- [ ] Corner buttons visible (home, settings)
- [ ] Clicking "Browse Shows" → Browse screen
- [ ] Clicking "Surprise Me" → Random show screen
- [ ] Clicking home button → stays on welcome
- [ ] Clicking settings → Settings screen

**Notes:**
_______________________________________________________________________

### 3.2 Browse Screen

**Test:** Browse screen modes work correctly

**Layout:**
- [ ] Screen uses Theme colors
- [ ] Browse mode buttons display correctly
- [ ] Content area shows current mode
- [ ] Corner navigation buttons visible

**Top Rated Mode:**
- [ ] Shows list of top-rated concerts
- [ ] Concerts display with ratings
- [ ] List scrolls smoothly
- [ ] Clicking show → Player screen

**By Date Mode:**
- [ ] Date browser displays
- [ ] Calendar/date picker functional
- [ ] Selecting date shows concerts
- [ ] Shows for selected date display

**By Venue Mode:**
- [ ] Venue list displays
- [ ] Venues show with show counts
- [ ] Clicking venue shows concerts
- [ ] Venue concerts load correctly

**By Year Mode:**
- [ ] Year browser displays
- [ ] Years organized by decade
- [ ] Clicking year shows concerts
- [ ] Year concerts load correctly

**Search Mode:**
- [ ] Search input visible
- [ ] Can type search query
- [ ] Search results display
- [ ] Clicking result → Player screen

**Random Mode:**
- [ ] Random show displays
- [ ] "Try Another" loads new show
- [ ] "Play Show" → Player screen

**Notes:**
_______________________________________________________________________

### 3.3 Player Screen

**Test:** Player screen displays and controls work

**Layout:**
- [ ] Split screen layout (40% left, 60% right)
- [ ] Left panel navy blue background
- [ ] Right panel black background
- [ ] Concert info visible in left panel
- [ ] Playback controls in right panel

**Concert Info (Left Panel):**
- [ ] Date displays correctly
- [ ] Venue name displays (bold)
- [ ] Location displays (gray)
- [ ] Source badge displays
- [ ] Setlist displays if available
- [ ] Scrollable if setlist is long

**Playback Controls (Right Panel):**
- [ ] "NOW PLAYING" label visible
- [ ] Current song title displays
- [ ] Progress bar visible
- [ ] Time stamps (current/total) visible
- [ ] Play/pause button (90px, center)
- [ ] Previous track button (60px)
- [ ] Next track button (60px)
- [ ] Skip backward button (60px, outline)
- [ ] Skip forward button (60px, outline)
- [ ] Volume slider visible
- [ ] All buttons clickable

**Playback Functionality:**
- [ ] Play button starts playback
- [ ] Pause button pauses playback
- [ ] Previous track goes to previous song
- [ ] Next track goes to next song
- [ ] Skip backward goes back 30 seconds
- [ ] Skip forward goes forward 30 seconds
- [ ] Progress bar updates in real-time
- [ ] Clicking progress bar seeks to position
- [ ] Volume slider adjusts volume
- [ ] Current track highlights in setlist

**Notes:**
_______________________________________________________________________

### 3.4 Settings Screen

**Test:** Settings screen displays and persists values

**Layout:**
- [ ] Settings categories display
- [ ] Current category highlighted
- [ ] Settings content visible
- [ ] Corner navigation visible

**Network Settings:**
- [ ] Connection status displays
- [ ] "Check for Updates" button works

**Audio Settings:**
- [ ] Master volume slider works
- [ ] Volume changes apply immediately
- [ ] Audio output dropdown functional

**Display Settings:**
- [ ] Brightness slider works
- [ ] Screen timeout dropdown functional
- [ ] Changes persist after restart

**About Section:**
- [ ] App version displays
- [ ] Database statistics shown
- [ ] Credits/acknowledgments visible
- [ ] "Reset to Defaults" button works

**Persistence:**
- [ ] Change settings → restart app → settings retained
- [ ] Volume persists across sessions
- [ ] Brightness persists across sessions

**Notes:**
_______________________________________________________________________

---

## Section 4: Navigation Flow

### 4.1 Screen Transitions

**Test:** Navigation between screens works smoothly

- [ ] Welcome → Browse (smooth transition)
- [ ] Welcome → Settings (smooth transition)
- [ ] Browse → Player (smooth transition)
- [ ] Player → Browse (via home)
- [ ] Settings → Welcome (via home)
- [ ] Any screen → Settings (via corner button)
- [ ] Transitions < 500ms duration
- [ ] No screen flashing or glitches

**Notes:**
_______________________________________________________________________

### 4.2 Navigation Consistency

**Test:** Corner buttons work consistently

**Home Button:**
- [ ] Visible on all screens except welcome
- [ ] Always in same position (top-right)
- [ ] Always returns to welcome screen
- [ ] Same size/style everywhere

**Settings Button:**
- [ ] Visible on all screens except settings
- [ ] Always in same position (bottom-right)
- [ ] Always opens settings screen
- [ ] Same size/style everywhere

**Notes:**
_______________________________________________________________________

---

## Section 5: Touch Target Validation

### 5.1 Button Sizes

**Test:** All buttons meet minimum touch target size

**Primary Buttons (PillButton):**
- [ ] All ≥ 60px height
- [ ] Adequate width (≥ 200px)
- [ ] Easy to tap with finger

**Icon Buttons:**
- [ ] Standard buttons ≥ 60px diameter
- [ ] Play button ≥ 90px diameter
- [ ] Corner buttons ≥ 44px diameter
- [ ] All circular buttons are round

**List Items:**
- [ ] Concert list items ≥ 80px height
- [ ] Full width (easy to tap)
- [ ] Clear hit area

**Notes:**
_______________________________________________________________________

### 5.2 Spacing Between Elements

**Test:** Adequate spacing between touch targets

- [ ] Buttons have ≥ 16px spacing
- [ ] List items have visible dividers
- [ ] No overlapping touch areas
- [ ] No accidental tap targets nearby

**Notes:**
_______________________________________________________________________

### 5.3 Touch Feedback

**Test:** Visual feedback on all interactions

- [ ] Buttons brighten on hover/press
- [ ] List items highlight on tap
- [ ] Progress bar thumb visible when dragging
- [ ] All interactions feel responsive

**Notes:**
_______________________________________________________________________

---

## Section 6: Performance Testing

### 6.1 Load Times

**Test:** Screen loading is fast

- [ ] App startup < 5 seconds
- [ ] Welcome screen loads instantly
- [ ] Browse screen loads < 1 second
- [ ] Player screen loads < 3 seconds
- [ ] Settings screen loads < 1 second

**Notes:**
_______________________________________________________________________

### 6.2 Scrolling Performance

**Test:** Lists scroll smoothly

- [ ] Concert list scrolls smoothly (60fps target)
- [ ] Setlist scrolls smoothly
- [ ] Date browser scrolls smoothly
- [ ] No stuttering or lag
- [ ] Scroll position accurate

**Platform Specific:**
- [ ] macOS: Smooth 60fps scrolling
- [ ] Raspberry Pi: Acceptable 30fps+ scrolling

**Notes:**
_______________________________________________________________________

### 6.3 Memory Usage

**Test:** No memory leaks over extended use

- [ ] Run app for 10 minutes → memory stable
- [ ] Navigate between screens 20 times → memory stable
- [ ] Play 5 shows back-to-back → memory stable
- [ ] Memory usage < 500MB on Raspberry Pi

**Notes:**
_______________________________________________________________________

---

## Section 7: Error Handling

### 7.1 Network Errors

**Test:** App handles network issues gracefully

- [ ] No internet → informative error message
- [ ] Failed API request → retry or clear error
- [ ] Timeout → user-friendly message
- [ ] Network restored → app continues working

**Notes:**
_______________________________________________________________________

### 7.2 Database Errors

**Test:** App handles database issues gracefully

- [ ] Missing database → clear error message
- [ ] Corrupted data → skips and continues
- [ ] Empty results → "No shows found" message
- [ ] Invalid date → helpful error message

**Notes:**
_______________________________________________________________________

### 7.3 Playback Errors

**Test:** App handles playback issues gracefully

- [ ] Invalid URL → error message, suggest alternatives
- [ ] Stream unavailable → try next source
- [ ] Playback interrupted → resume or restart
- [ ] End of show → auto-play next or stop cleanly

**Notes:**
_______________________________________________________________________

---

## Section 8: Cross-Platform Testing

### 8.1 macOS Testing

**Test:** App works correctly on macOS

- [ ] Window size correct (1280x720)
- [ ] All fonts render correctly
- [ ] Colors accurate
- [ ] Mouse hover states work
- [ ] Keyboard shortcuts work
- [ ] Audio plays through CoreAudio

**Notes:**
_______________________________________________________________________

### 8.2 Raspberry Pi Testing

**Test:** App works correctly on Raspberry Pi

- [ ] Fullscreen mode works
- [ ] All fonts render correctly (no Unicode errors)
- [ ] Colors accurate on 7" display
- [ ] Touch events register correctly
- [ ] No lag in UI interactions
- [ ] Audio plays through ALSA/DAC
- [ ] Runs without crashes for 30+ minutes

**Notes:**
_______________________________________________________________________

---

## Section 9: Accessibility

### 9.1 Visual Accessibility

**Test:** UI is readable and clear

- [ ] Text has adequate contrast (4.5:1 minimum)
- [ ] Font sizes readable at arm's length
- [ ] Colors distinguishable
- [ ] No reliance on color alone

**Notes:**
_______________________________________________________________________

### 9.2 Touch Accessibility

**Test:** UI is usable with fingers

- [ ] All buttons large enough for fingers
- [ ] No precision required for any action
- [ ] Touch targets well-spaced
- [ ] No small controls

**Notes:**
_______________________________________________________________________

---

## Section 10: Edge Cases

### 10.1 Data Edge Cases

**Test:** App handles unusual data correctly

- [ ] Very long venue name → truncates cleanly
- [ ] Very long song title → truncates with ellipsis
- [ ] Show with no setlist → displays message
- [ ] Show with 100+ songs → scrolls properly
- [ ] Rating of 5.0 → displays correctly
- [ ] Rating of 1.0 → displays correctly

**Notes:**
_______________________________________________________________________

### 10.2 User Action Edge Cases

**Test:** App handles unusual user actions

- [ ] Rapid button clicking → no crashes
- [ ] Clicking during loading → no issues
- [ ] Back/forward rapidly → no crashes
- [ ] Changing settings during playback → continues
- [ ] Seeking during buffering → handles gracefully

**Notes:**
_______________________________________________________________________

---

## Final Checklist

### Pre-Hardware Integration Requirements

Before proceeding to Phase 11, ensure:

- [ ] All automated tests pass (`python3 tests/phase_10_integration_test.py`)
- [ ] All manual tests completed with no critical failures
- [ ] All visual consistency tests pass
- [ ] All components functional
- [ ] All screens functional
- [ ] Performance acceptable on Raspberry Pi
- [ ] Touch targets adequate
- [ ] Error handling comprehensive
- [ ] No memory leaks
- [ ] Cross-platform compatibility verified

### Critical Issues

**List any critical issues that must be fixed before Phase 11:**

1. _______________________________________________________________________
2. _______________________________________________________________________
3. _______________________________________________________________________

### Minor Issues

**List any minor issues that can be addressed later:**

1. _______________________________________________________________________
2. _______________________________________________________________________
3. _______________________________________________________________________

---

## Sign-Off

**Tester Name:** ___________________________________

**Date Tested:** ___________________________________

**Platform(s) Tested:** ___________________________________

**Overall Status:** [ ] Pass  [ ] Pass with minor issues  [ ] Fail

**Ready for Phase 11:** [ ] Yes  [ ] No

**Additional Notes:**
_______________________________________________________________________
_______________________________________________________________________
_______________________________________________________________________

---

## Appendix: Known Limitations

Document any known limitations or features not yet implemented:

- Venue browser may be placeholder (polished "Coming Soon" screen)
- Some animations may be disabled on Pi for performance
- Certain advanced features deferred to Phase 12

---

**Last Updated:** January 9, 2026
**Version:** 1.0
**Next Review:** After Phase 11 hardware integration
