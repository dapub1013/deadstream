# DeadStream UI Style Guide

**Version:** 1.0  
**Date:** January 8, 2026  
**Project:** DeadStream - Grateful Dead Concert Player  
**Platform:** Raspberry Pi 4 with 7" touchscreen (1024x600)

This document captures all UI and design decisions made through Phase 10C to ensure consistency across the application.

---

## Design Philosophy

### Core Principles

1. **Minimal & Clean** - Remove visual noise, let the music be the focus
2. **Touch-First** - Design for fingers, not just mouse cursors
3. **Deadhead-Friendly** - Warm, inviting, psychedelic-inspired without being kitsch
4. **Professional** - Match quality of major music apps (Spotify, Apple Music)
5. **Functional Beauty** - Every element serves a purpose

### Visual Style

- **Aesthetic:** Modern with subtle retro influences
- **Mood:** Warm, inviting, focused on music
- **Complexity:** Simple, uncluttered interfaces
- **Animation:** Minimal - only when it aids comprehension

---

## Color Palette

### Primary Colors

```css
/* Background */
--bg-primary: #2E2870      /* Deep purple - main background */
--bg-gradient-end: #1a1a4a /* Darker purple - gradient end */
--bg-black: #000000        /* Pure black - player screen right panel */
--bg-navy: #1e2936         /* Navy blue - concert info panel */

/* Text */
--text-primary: #FFFFFF    /* White - main text */
--text-secondary: #B0B0B0  /* Gray - secondary text */

/* Accents */
--accent-yellow: #FFD700   /* Gold/yellow - highlights, badges */
--accent-blue: #1976D2     /* Blue - interactive elements */
```

### Transparency Levels

```css
/* Ghost buttons and overlays */
--overlay-subtle: rgba(255, 255, 255, 0.08)   /* 8% - barely visible */
--overlay-light: rgba(255, 255, 255, 0.16)    /* 16% - hover state */
--overlay-medium: rgba(255, 255, 255, 0.30)   /* 30% - selected state */

/* Icon opacity */
--icon-muted: rgba(255, 255, 255, 0.70)       /* 70% - resting state */
--icon-bright: rgba(255, 255, 255, 1.00)      /* 100% - hover/active */
```

### Color Usage Rules

**Backgrounds:**
- Use purple gradient for placeholder/loading screens
- Use pure black (#000000) for focused content (player screen right panel)
- Use navy blue (#1e2936) for information panels (concert details)

**Text:**
- Always use white (#FFFFFF) for primary content
- Use gray (#B0B0B0) for labels, metadata, secondary info
- Never use colors below 60% opacity for text (readability)

**Accents:**
- Yellow (#FFD700) for source badges, highlights, importance
- Blue (#1976D2) for navigation buttons and CTAs
- Use sparingly - accents lose impact if overused

---

## Typography

### Font Family

```python
FONT_FAMILY = "Arial"  # System font for maximum compatibility
```

**Rationale:**
- Arial available on all platforms (macOS, Raspberry Pi OS)
- Clean, modern appearance
- Excellent readability at all sizes
- Good Unicode character support

### Font Scale

```python
# Headers
HEADER_LARGE = 48px    # Main titles, song names
HEADER_MEDIUM = 28px   # Venue names, section headers

# Body Text
BODY_LARGE = 20px      # Concert dates, primary info
BODY_MEDIUM = 16px     # Setlist items, secondary info
BODY_SMALL = 14px      # Labels, metadata

# UI Elements
BUTTON_TEXT = 16px     # Button labels
LABEL_TEXT = 14px      # Form labels, "NOW PLAYING"
```

### Font Weights

- **Bold (700):** Headers, song titles, emphasis
- **Normal (400):** Body text, most UI elements
- **Never use:** Light/thin weights (poor readability on screen)

### Typography Rules

1. **Hierarchy:** Larger = more important
2. **Alignment:** Center for focused content, left-align for lists
3. **Line Height:** 1.4-1.6 for body text (readability)
4. **Letter Spacing:** Normal (no tracking) except:
   - Labels like "NOW PLAYING": 2px letter-spacing (uppercase)

---

## Spacing System

### Base Unit

```python
BASE_UNIT = 8px  # All spacing is multiples of 8
```

### Spacing Scale

```python
SPACING_TINY = 8px      # 1 unit
SPACING_SMALL = 16px    # 2 units
SPACING_MEDIUM = 24px   # 3 units
SPACING_LARGE = 32px    # 4 units
SPACING_XLARGE = 48px   # 6 units
SPACING_XXLARGE = 64px  # 8 units
```

### Application

**Component Padding:**
- Small buttons: 16px padding
- Large panels: 32px padding
- Screens: 48px padding

**Vertical Spacing:**
- Related items: 16px apart
- Unrelated sections: 32px+ apart
- Screen sections: 48px+ apart

**Button Spacing:**
- Between buttons: 24px (3 units)
- Around button groups: 32px (4 units)

### Spacing Rules

1. **Consistency:** Use spacing scale values, never arbitrary numbers
2. **Rhythm:** Maintain consistent vertical rhythm (multiples of 8)
3. **Breathing Room:** Don't pack elements too tightly
4. **Touch Targets:** Minimum 60px buttons with 16px spacing

---

## Component Library

### Buttons

#### PillButton (Primary Action)

**Appearance:**
- Rounded pill shape (border-radius: 30px)
- Height: 60px
- Min width: 200px
- Font: 16px, bold

**Variants:**

```python
# Blue variant (default)
background: #1976D2
text: #FFFFFF
hover: Brightness +20%

# Yellow variant (accent)
background: #FFD700
text: #2E2870 (dark purple for contrast)
hover: Brightness +20%

# Outline variant
background: transparent
border: 2px solid #FFFFFF
text: #FFFFFF
hover: background rgba(255, 255, 255, 0.1)
```

**Usage:**
- Primary navigation ("Browse Shows")
- Important actions
- Screen transitions

#### IconButton (Media Controls)

**Appearance:**
- Circular button
- Solid or outline style
- Size: 60px or 90px (play button)
- Icon: Unicode characters or symbols

**Variants:**

```python
# Solid variant
background: rgba(255, 255, 255, 0.14)  # 14% white
icon: #FFFFFF
hover: rgba(255, 255, 255, 0.20)

# Outline variant
background: transparent
border: 2px solid rgba(255, 255, 255, 0.6)
icon: rgba(255, 255, 255, 0.7)
hover: border rgba(255, 255, 255, 1.0)

# Accent variant (yellow)
background: #FFD700
icon: #2E2870
hover: brightness +20%
```

**Icon Set:**
- Play: ▶
- Pause: ⏸ or ❚❚
- Stop: ⏹
- Home: ⌂
- Settings: ⚙
- Plus: +
- Minus: -

**Usage:**
- Media playback controls
- Standard UI actions

#### TrackButton (Previous/Next Track)

**Appearance:**
- Circular button, 60x60px
- Solid filled background
- Custom drawn bar+triangle icon

**Design:**

```python
# Previous track: |◀
background: rgba(255, 255, 255, 0.14)
icon: Black vertical bar (left) + left-pointing triangle
hover: rgba(255, 255, 255, 0.20)

# Next track: ▶|
background: rgba(255, 255, 255, 0.14)
icon: Right-pointing triangle + black vertical bar (right)
hover: rgba(255, 255, 255, 0.20)
```

**Icon Details:**
- Bar: 3px wide × 20px tall
- Triangle: 15px base × 10px height
- Icon color: #000000 (black on white circle)

**Usage:**
- Track navigation only
- Distinct from time skip buttons

#### SkipButton (Time Skip ±30s)

**Appearance:**
- Circular button, 60x60px
- Outline style (no fill)
- Circular arrow icon

**Design:**

```python
# Skip backward: ↺
background: transparent
border: 2px solid rgba(255, 255, 255, 0.6)
icon: ↺ (U+21BA - counterclockwise arrow)
hover: border rgba(255, 255, 255, 1.0)

# Skip forward: ↻
background: transparent
border: 2px solid rgba(255, 255, 255, 0.6)
icon: ↻ (U+21BB - clockwise arrow)
hover: border rgba(255, 255, 255, 1.0)
```

**Icon Details:**
- Circular arrows (not linear triangles)
- 24px font size (large for visibility)
- White color, semi-transparent at rest

**Usage:**
- Time scrubbing within current track
- Distinct from track navigation buttons

#### CornerButton (Minimal Navigation)

**Appearance:**
- Small circular button, 44x44px
- "Ghost" style - barely visible until hover
- Positioned in absolute corners

**Design:**

```python
# Default state
background: rgba(255, 255, 255, 0.08)  # Very subtle
icon: rgba(255, 255, 255, 0.70)
size: 44px

# Hover state
background: rgba(255, 255, 255, 0.16)  # More visible
icon: rgba(255, 255, 255, 1.00)
```

**Icons:**
- Home: ⌂ (U+2302)
- Settings: ⚙ (U+2699)

**Positioning:**
- 12px from edges (top/bottom/right)
- Always in corners (never inline)

**Usage:**
- Non-intrusive navigation
- Settings access
- Home button

### Badges

#### SourceBadge

**Appearance:**
- Small pill shape
- 32px height
- Yellow background
- Dark text

**Design:**

```python
background: #FFD700
text: #2E2870 (dark purple)
padding: 8px 16px
border-radius: 16px
font: 14px, bold
```

**Text Values:**
- "SBD" - Soundboard recording
- "AUD" - Audience recording
- "MATRIX" - Mixed sources
- "FM" - FM broadcast

**Usage:**
- Concert info displays
- Recording quality indicators
- Always visible, never hidden

#### RatingBadge

**Appearance:**
- Circular badge
- 40px diameter
- Yellow background
- Large rating number

**Design:**

```python
background: #FFD700
text: #2E2870
size: 40px circle
font: 18px, bold
```

**Display:**
- Rating value: 1.0 - 5.0
- Format: "4.5" (one decimal)
- Center-aligned

**Usage:**
- Show ratings
- Concert quality indication
- Sorting/filtering reference

### Lists

#### ConcertListItem

**Appearance:**
- Full-width card
- White text on transparent background
- Hover effect
- Touch-friendly height

**Layout:**

```
+--------------------------------------------------+
| 05/08/1977  [4.8]                          [SBD] |  <- Date, Rating, Source
| Cornell University - Barton Hall                 |  <- Venue (bold)
| Ithaca, NY                                       |  <- Location
+--------------------------------------------------+
```

**Spacing:**
- Item height: 80px minimum
- Padding: 16px all sides
- Gap between items: 1px border

**Design:**

```python
background: transparent
border-bottom: 1px solid rgba(255, 255, 255, 0.1)
hover: background rgba(255, 255, 255, 0.05)

# Date
font: 16px, normal
color: #B0B0B0 (gray)

# Venue
font: 18px, bold
color: #FFFFFF

# Location
font: 14px, normal
color: #B0B0B0
```

**Usage:**
- Browse screen concert listings
- Search results
- Favorites/history lists

### Form Elements

#### ProgressBarWidget

**Appearance:**
- Horizontal slider with timestamps
- Seekable by click/drag
- Real-time position updates

**Design:**

```python
# Track
height: 4px
background: rgba(255, 255, 255, 0.3)
border-radius: 2px

# Elapsed portion
background: #FFD700 (yellow)

# Scrubber handle
size: 16px circle
background: #FFD700
border: 2px solid #FFFFFF

# Timestamps
font: 14px, normal
color: #B0B0B0
```

**Layout:**

```
0:00 [========●--------] 7:42
```

**Usage:**
- Audio playback progress
- Seeking within tracks

#### VolumeControlWidget

**Appearance:**
- Horizontal slider with icons
- Mute button on left
- Volume icon on right

**Design:**

```python
# Layout
[🔇] [=========●--------] [🔊]

# Slider (same as progress bar)
height: 4px
background: rgba(255, 255, 255, 0.3)

# Volume level
background: #FFFFFF

# Icons
size: 24px
color: #FFFFFF
opacity: 0.7 (normal), 1.0 (hover)
```

**Usage:**
- Audio volume control
- Mute toggle

---

## Layout Patterns

### Screen Structure

```
+--------------------------------------------------+
|                    HEADER                        |
|  (Title, navigation, key info)                  |
+--------------------------------------------------+
|                                                  |
|                    CONTENT                       |
|  (Main screen content)                          |
|                                                  |
+--------------------------------------------------+
```

### Split Panel Layout

Used in player screen:

```
+------------------------+-------------------------+
|                        |                         |
|     LEFT PANEL         |     RIGHT PANEL         |
|   (Information)        |     (Controls)          |
|                        |                         |
+------------------------+-------------------------+
     40% width                 60% width
```

**Left Panel:**
- Concert details
- Setlist
- Metadata

**Right Panel:**
- Playback controls
- Current track
- Progress/volume

### Centered Content Layout

Used in welcome screen:

```
+--------------------------------------------------+
|                                                  |
|                  [Centered                       |
|                   Content]                       |
|                                                  |
+--------------------------------------------------+
```

**Rules:**
- Vertical centering with flex spacers
- Max content width: 600px
- Horizontal centering
- Adequate padding (48px minimum)

---

## Icon Design Guidelines

### Icon Style

**Principles:**
1. **Simple shapes** - Recognize at small sizes
2. **Consistent stroke width** - Visual harmony
3. **Unicode preferred** - No external dependencies
4. **Platform tested** - Works on Pi and Mac

### Icon Set

#### Media Controls

```python
# Playback
Play: ▶ or ▶️
Pause: ⏸ or ❚❚
Stop: ⏹

# Navigation
Previous Track: |◀ (custom drawn)
Next Track: ▶| (custom drawn)
Skip Backward: ↺ (U+21BA)
Skip Forward: ↻ (U+21BB)

# Utility
Home: ⌂ (U+2302)
Settings: ⚙ (U+2699)
```

#### UI Actions

```python
Add: +
Remove: -
Search: 🔍
Close: ×
Back: ◀
Forward: ▶
```

### Icon Semantics

**Circular Arrows (↺ ↻):**
- Meaning: Time scrubbing, replay
- Use: Skip ±30s buttons
- Style: Outline circles

**Bar+Triangle (|◀ ▶|):**
- Meaning: Track navigation
- Use: Previous/next track
- Style: Solid circles

**Simple Triangles (◀ ▶):**
- Meaning: General navigation
- Use: Back/forward in UI
- Style: Varies by context

---

## Interaction Patterns

### Hover Effects

**Buttons:**
```python
default → hover
background opacity: +20%
border opacity: +40% (if outline)
icon opacity: 70% → 100%
```

**List Items:**
```python
default → hover
background: transparent → rgba(255, 255, 255, 0.05)
```

**Timing:**
- Transition: 200ms ease-in-out
- No delay
- Subtle, not jarring

### Touch Targets

**Minimum Sizes:**
- Buttons: 60×60px (44px absolute minimum)
- List items: Full width × 80px height
- Controls: 60×60px

**Spacing:**
- Between touch targets: 16px minimum
- Safe area: 8px around each target

**Feedback:**
- Immediate visual response
- Hover state on tap/touch
- No delay in interaction

### State Indicators

**Selected:**
```python
background: rgba(255, 215, 0, 0.15)  # Yellow tint
border: 2px solid #FFD700 (optional)
```

**Disabled:**
```python
opacity: 0.5
pointer-events: none
```

**Loading:**
```python
# Show loading indicator
# Disable interaction
# Maintain layout
```

---

## Animation Guidelines

### When to Animate

✅ **Use animation for:**
- Button hover states (opacity/brightness)
- Modal/overlay entry/exit
- Loading indicators
- Focus indicators

❌ **Don't animate:**
- Text content
- Layout shifts
- Background changes
- Continuous loops (except loading)

### Animation Properties

**Duration:**
- Quick: 150ms (hover states)
- Standard: 200ms (most transitions)
- Slow: 300ms (modals, overlays)

**Easing:**
- ease-in-out (most cases)
- ease-out (entering)
- ease-in (exiting)

**Properties:**
- Opacity (cheap)
- Transform (cheap)
- Avoid: Width, height, position (expensive)

---

## Text Handling

### Truncation

**Method:** Ellipsis (...)

**Rules:**
1. Use Qt's `elidedText()` for automatic truncation
2. Truncate from the right (ElideRight)
3. Show full text in tooltips or detail views
4. Never truncate critical information

**Example:**
```
Short: "Scarlet Begonias"
Long: "Playing in the Band (Part 1 of 3 - Ex..."
```

### Wrapping

**Single-line elements:**
- Song titles (truncate)
- Labels (truncate)
- Buttons (never wrap)

**Multi-line elements:**
- Venue names (wrap at 2 lines)
- Descriptions (wrap as needed)
- Error messages (wrap as needed)

---

## Accessibility

### Visual Accessibility

**Contrast:**
- Text on dark: minimum 4.5:1 ratio
- White on purple: ✅ Passes
- Gray on purple: ✅ Passes WCAG AA
- Yellow on purple: ✅ Passes

**Font Size:**
- Minimum: 14px for body text
- Minimum: 16px for important actions
- Larger for primary content (48px song titles)

### Touch Accessibility

**Target Size:**
- Minimum: 44×44px (WCAG 2.1 Level AAA)
- Preferred: 60×60px
- Large actions: 90×90px (play button)

**Spacing:**
- Minimum: 8px between targets
- Preferred: 16px between targets

### Screen Reader Support

**Not implemented yet**, but considerations:

- All buttons have tooltips
- All images have alt text
- Semantic HTML/Qt structure
- Keyboard navigation support

---

## Platform Considerations

### Raspberry Pi

**Screen:**
- 7" diagonal, 1024×600 resolution
- Touchscreen (capacitive)
- Portrait or landscape orientation

**Constraints:**
- Limited CPU (avoid heavy animations)
- Touch-first (no hover on touch)
- Outdoor visibility (high contrast needed)

**Optimizations:**
- Fixed layouts (no complex reflow)
- Minimal transparency (performance)
- No continuous animations
- Large touch targets (60px+)

### macOS (Development)

**Screen:**
- Various sizes, high DPI
- Mouse + keyboard
- Development environment

**Benefits:**
- Faster iteration
- Easier debugging
- Hover states visible

**Cross-platform:**
- Same codebase for both
- Test on both platforms
- No platform-specific hacks

---

## Theme Manager Integration

### Using Theme Constants

**Always use Theme Manager:**

```python
from src.ui.styles.theme import Theme

# Colors
color: {Theme.TEXT_PRIMARY}
background: {Theme.BG_PRIMARY}

# Spacing
padding: {Theme.SPACING_LARGE}px
margin: {Theme.SPACING_MEDIUM}px

# Typography
font-size: {Theme.BODY_LARGE}px
```

**Never hardcode:**

```python
# ❌ Bad
color: #FFFFFF
padding: 32px
font-size: 20px

# ✅ Good
color: {Theme.TEXT_PRIMARY}
padding: {Theme.SPACING_LARGE}px
font-size: {Theme.BODY_LARGE}px
```

### Theme Manager Constants

**Complete reference:**

```python
# Colors
BG_PRIMARY = "#2E2870"
BG_GRADIENT_END = "#1a1a4a"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#B0B0B0"
ACCENT_YELLOW = "#FFD700"
ACCENT_BLUE = "#1976D2"

# Typography
FONT_FAMILY = "Arial"
HEADER_LARGE = 48
HEADER_MEDIUM = 28
BODY_LARGE = 20
BODY_MEDIUM = 16
BODY_SMALL = 14

# Spacing
SPACING_TINY = 8
SPACING_SMALL = 16
SPACING_MEDIUM = 24
SPACING_LARGE = 32
SPACING_XLARGE = 48
SPACING_XXLARGE = 64

# Component Sizes
BUTTON_HEIGHT = 60
BUTTON_SPACING = 24
TOUCH_TARGET_MIN = 44
```

---

## Code Style Guidelines

### Component Structure

**Standard pattern:**

```python
class MyComponent(QWidget):
    """Brief description"""
    
    # Signals
    signal_name = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Set up the UI"""
        # Create widgets
        # Set up layout
        # Apply styles
    
    def on_action(self):
        """Handle user action"""
        # Event handler
```

### Styling Methods

**Prefer stylesheets for static styles:**

```python
widget.setStyleSheet(f"""
    QWidget {{
        background-color: {Theme.BG_PRIMARY};
        color: {Theme.TEXT_PRIMARY};
    }}
""")
```

**Use QPainter for custom drawing:**

```python
def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    # Custom painting
```

### Documentation

**Always include:**
- Class docstring (what it does)
- Method docstrings (parameters, returns)
- Signal documentation
- Usage examples for complex components

---

## Design Checklist

### Before Creating a Component

- [ ] Check if existing component can be reused
- [ ] Use Theme Manager constants (no hardcoding)
- [ ] Consider touch target sizes (60px minimum)
- [ ] Plan hover/focus states
- [ ] Consider disabled state if applicable
- [ ] Test on both macOS and Raspberry Pi

### Before Finalizing a Screen

- [ ] Consistent spacing (use spacing scale)
- [ ] Clear visual hierarchy (size, weight, color)
- [ ] Adequate contrast (WCAG AA minimum)
- [ ] Touch targets 60px+ with 16px spacing
- [ ] No hardcoded colors/sizes
- [ ] Tested on target resolution (1024×600)
- [ ] Smooth interactions (no janky animations)
- [ ] Logical focus order (keyboard nav)

---

## Examples & Patterns

### Welcome Screen Pattern

```
+--------------------------------------------------+
|                                                  |
|                  [Centered]                      |
|                                                  |
|              DeadStream Logo                     |
|                                                  |
|           [Browse Shows Button]                  |
|                                                  |
+--------------------------------------------------+
```

**Key features:**
- Vertical centering with flex
- Large header (48px)
- Single primary action
- Purple gradient background

### Player Screen Pattern

```
+---------------------+----------------------------+
|  Concert Info       |      Playback Controls    |
|  - Date/Venue       |      - NOW PLAYING        |
|  - Source Badge     |      - Song Title         |
|  - Setlist          |      - Progress Bar       |
|                     |      - Media Controls     |
|                     |      - Volume             |
+---------------------+----------------------------+
    Gradient BG              Pure Black BG
```

**Key features:**
- Split panel (40/60)
- Different backgrounds (gradient/black)
- Information vs controls
- Corner navigation (ghost buttons)

### Browse Screen Pattern

*(To be implemented in Phase 10D)*

```
+--------------------------------------------------+
|  Search: [___________]  [Date Picker]  [Filter] |
+--------------------------------------------------+
|  Show List:                                      |
|  +--------------------------------------------+  |
|  | 05/08/1977 [4.8]                     [SBD]|  |
|  | Cornell University - Barton Hall          |  |
|  +--------------------------------------------+  |
|  | 12/31/1978 [4.6]                     [SBD]|  |
|  | Winterland Arena                          |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
```

**Key features:**
- Search bar prominent
- Filter controls
- Scrollable list
- Clear item hierarchy

---

## Common Pitfalls to Avoid

### ❌ Don't Do This

1. **Hardcode values**
   ```python
   # Bad
   color: #FFFFFF
   padding: 32px
   ```

2. **Tiny touch targets**
   ```python
   # Bad
   button.setFixedSize(30, 30)  # Too small!
   ```

3. **No hover feedback**
   ```python
   # Bad - no visual feedback
   button.setStyleSheet("background: blue;")
   ```

4. **Poor contrast**
   ```python
   # Bad
   color: #888888  # Too low contrast
   background: #666666
   ```

5. **Complex animations**
   ```python
   # Bad - performance issues
   for i in range(100):
       widget.move(i, 0)
       QApplication.processEvents()
   ```

### ✅ Do This Instead

1. **Use Theme Manager**
   ```python
   # Good
   color: {Theme.TEXT_PRIMARY}
   padding: {Theme.SPACING_LARGE}px
   ```

2. **Adequate touch targets**
   ```python
   # Good
   button.setFixedSize(60, 60)
   ```

3. **Clear feedback**
   ```python
   # Good
   button.setStyleSheet("""
       QPushButton { background: blue; }
       QPushButton:hover { background: lightblue; }
   """)
   ```

4. **Good contrast**
   ```python
   # Good
   color: {Theme.TEXT_PRIMARY}  # #FFFFFF
   background: {Theme.BG_PRIMARY}  # #2E2870
   ```

5. **Simple transitions**
   ```python
   # Good
   transition: opacity 200ms ease-in-out;
   ```

---

## Quick Reference

### Button Sizes

| Button Type | Size | Usage |
|------------|------|-------|
| CornerButton | 44×44px | Minimal navigation |
| IconButton | 60×60px | Standard controls |
| IconButton (play) | 90×90px | Primary action |
| PillButton | 60px tall | Main navigation |

### Spacing Quick Guide

| Space | Size | Usage |
|-------|------|-------|
| Tiny | 8px | Tight elements |
| Small | 16px | Related items |
| Medium | 24px | Button spacing |
| Large | 32px | Section spacing |
| XLarge | 48px | Panel padding |

### Color Quick Guide

| Color | Hex | Usage |
|-------|-----|-------|
| Purple | #2E2870 | Main background |
| Black | #000000 | Focused panels |
| White | #FFFFFF | Primary text |
| Gray | #B0B0B0 | Secondary text |
| Yellow | #FFD700 | Accents, badges |
| Blue | #1976D2 | CTAs, links |

---

## Maintenance

### Updating This Guide

When making design changes:

1. Document the change here first
2. Update Theme Manager if needed
3. Update affected components
4. Test on both platforms
5. Update this guide's version number

### Version History

- **1.0** (Jan 8, 2026) - Initial style guide
  - Phases 10A, 10B, 10C complete
  - Welcome screen and player screen styles
  - Custom button components documented

---

## Contact & Feedback

**Project Lead:** David  
**Repository:** github.com/[username]/deadstream  
**Documentation:** See `/docs` folder

For questions about design decisions or proposed changes, create an issue in the repository.

---

**Last Updated:** January 8, 2026  
**Status:** Living document - update with each phase  
**Next Review:** Phase 10D completion
