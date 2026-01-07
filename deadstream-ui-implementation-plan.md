# DeadStream UI Restyling Implementation Plan

**Date:** January 6, 2026  
**Status:** Planning Phase  
**Target:** Restyle all screens to match mockup designs  
**Estimated Total Time:** 30-43 hours

---

## Executive Summary

This plan outlines the systematic approach to restyling the DeadStream application based on the complete mockup set. The work is divided into 8 sub-phases (10A through 10H), each building on the previous to ensure consistency and minimize rework.

**Key Principles:**
1. Build reusable components first
2. Test each component in isolation before integration
3. Apply to simplest screens first (Welcome) to validate approach
4. Progress to complex screens (Player) after patterns are proven
5. Maintain full functionality throughout (no broken features)

---

## Current State Assessment

### Existing Implementation

**Files Currently Present:**
```
src/ui/
├── screens/
│   ├── welcome_screen.py       # Needs: Full restyle
│   ├── browse_screen.py        # Needs: Sidebar nav, list items, badges
│   ├── player_screen.py        # Needs: Split layout, new controls
│   └── settings_screen.py      # Needs: Full restyle
│
├── main_window.py              # May need: Updated imports
└── screen_manager.py           # Minimal changes
```

**Current Styling Approach:**
- Basic PyQt5 default widgets
- Minimal custom styling
- No component library
- Inconsistent colors/fonts

**What Works Well:**
- Screen navigation system
- Database integration
- Audio playback engine
- Settings persistence

**What Needs Work:**
- Visual appearance (all screens)
- Touch-friendliness (button sizes)
- Component reusability
- Design consistency

### Gap Analysis

**Missing Components:**
1. PillButton (rounded action buttons)
2. IconButton (home, settings, search)
3. ConcertListItem (show metadata display)
4. SetlistWidget (scrollable setlist with sets)
5. RatingBadge (star ratings)
6. SourceBadge (SBD/AUD badges)
7. SeekableProgress (clickable progress bar)
8. DatePickerColumn (scrollable date selection)

**Missing Screens:**
1. Random Show screen (entirely new)

**Styling Needed:**
- Global color palette
- Typography system
- Component stylesheets
- Screen-specific layouts

---

## Phase 10A: Core Component Library

**Objective:** Build reusable UI components that all screens will use

**Estimated Time:** 4-6 hours

### Tasks

#### 1. Create Styling Infrastructure (1.5-2 hours)

**Primary Approach: Theme Manager (Recommended)**

**File to Create:**
```
src/ui/styles/
├── __init__.py
└── theme.py           # Consolidated theme manager (all styling constants)
```

**theme.py:**
Complete implementation provided in the Design System document, Section 3: Theme Manager.

This single file contains:
- All color constants (backgrounds, accents, text, borders)
- All typography constants (sizes, weights, family)
- All spacing constants (padding, margins, gaps)
- All component size constants (buttons, icons, badges)
- Helper methods for generating stylesheets
- Gradient generation
- Color manipulation utilities

**Benefits of Theme Manager:**
- Change entire app styling by editing one file
- Instant visual updates (colors, fonts, spacing)
- Autocomplete support in IDEs
- Single source of truth
- Easy experimentation with different themes

**Alternative Approach: Separate Files**

If you prefer separate files for organization:

```
src/ui/styles/
├── __init__.py
├── colors.py           # Color palette constants
├── typography.py       # Font sizes and weights
└── theme.py           # Imports and consolidates the above
```

**colors.py:**
```python
# Background Colors
BG_PRIMARY = "#2E2870"
BG_PANEL_DARK = "#1A2332"
BG_PANEL_BLACK = "#000000"
BG_CARD = "#1E2936"

# Accent Colors
ACCENT_YELLOW = "#FFD700"
ACCENT_GREEN = "#0F9D58"
ACCENT_BLUE = "#1976D2"
ACCENT_RED = "#FF0000"

# Text Colors
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#B0B0B0"
TEXT_DARK = "#1A1A1A"

# Borders
BORDER_SUBTLE = "#333333"
BORDER_PANEL = "#2A3F5F"

# Badges
BADGE_RATING = "#00BCD4"
BADGE_SOURCE = "#FFD700"

# Gradients
GRADIENT_START = "#9C27B0"
GRADIENT_END = "#2196F3"
```

**colors.py:**
```python
# Background Colors
BG_PRIMARY = "#2E2870"
BG_PANEL_DARK = "#1A2332"
BG_PANEL_BLACK = "#000000"
BG_CARD = "#1E2936"

# Accent Colors
ACCENT_YELLOW = "#FFD700"
ACCENT_GREEN = "#0F9D58"
ACCENT_BLUE = "#1976D2"
ACCENT_RED = "#FF0000"

# Text Colors
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#B0B0B0"
TEXT_DARK = "#1A1A1A"

# Borders
BORDER_SUBTLE = "#333333"
BORDER_PANEL = "#2A3F5F"

# Badges
BADGE_RATING = "#00BCD4"
BADGE_SOURCE = "#FFD700"

# Gradients
GRADIENT_START = "#9C27B0"
GRADIENT_END = "#2196F3"
```

**typography.py:**
```python
# Font Sizes
HEADER_LARGE = 48
HEADER_MEDIUM = 36
HEADER_SMALL = 24
BODY_LARGE = 20
BODY_MEDIUM = 16
BODY_SMALL = 14
META_TEXT = 12

# Font Weights
WEIGHT_BOLD = "bold"
WEIGHT_NORMAL = "normal"

# Font Family
FONT_FAMILY = "sans-serif"
```

**theme.py (consolidates the above):**
```python
from .colors import *
from .typography import *

class Theme:
    """Consolidated theme - all styling in one place"""
    # All constants imported from colors and typography
    # Plus spacing, component sizes, helper methods
```

**Recommendation:** Use the single-file Theme Manager approach (first option) unless you have specific reasons to separate concerns. The single file is simpler to maintain and easier to experiment with.

**Testing the Theme:**

Create a quick test script to visualize theme colors:

```python
# examples/test_theme.py
import sys
sys.path.insert(0, '/path/to/deadstream')

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from src.ui.styles.theme import Theme

app = QApplication(sys.argv)
window = QWidget()
window.setStyleSheet(Theme.get_global_stylesheet())

layout = QVBoxLayout()

# Test all button colors
for variant, color in [
    ("Yellow", Theme.ACCENT_YELLOW),
    ("Green", Theme.ACCENT_GREEN),
    ("Blue", Theme.ACCENT_BLUE),
    ("Red", Theme.ACCENT_RED),
]:
    btn = QPushButton(f"{variant} Button")
    btn.setStyleSheet(Theme.get_button_style(color))
    layout.addWidget(btn)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
```

Run this whenever you change theme colors to see instant results.

#### 2. Build PillButton Component (1 hour)

**File:** `src/ui/components/pill_button.py`

**Features:**
- Configurable color variants (yellow, green, blue, red, gradient)
- Touch-friendly sizing (minimum 60px height)
- Pressed state feedback
- Consistent rounded corners
- Uses Theme Manager for all styling

**Implementation Example:**
```python
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from src.ui.styles.theme import Theme

class PillButton(QPushButton):
    """Large rounded button with theme-based styling"""
    
    def __init__(self, text, variant='yellow', parent=None):
        super().__init__(text, parent)
        
        # Map variants to theme colors
        self.color_map = {
            'yellow': (Theme.ACCENT_YELLOW, Theme.TEXT_DARK),
            'green': (Theme.ACCENT_GREEN, Theme.TEXT_PRIMARY),
            'blue': (Theme.ACCENT_BLUE, Theme.TEXT_PRIMARY),
            'red': (Theme.ACCENT_RED, Theme.TEXT_PRIMARY),
        }
        
        self.variant = variant
        self.apply_style()
        
        # Set minimum size from theme
        self.setMinimumSize(Theme.BUTTON_MIN_WIDTH, Theme.BUTTON_HEIGHT)
    
    def apply_style(self):
        """Apply theme-based styling"""
        bg_color, text_color = self.color_map.get(
            self.variant, 
            self.color_map['yellow']
        )
        
        # Use Theme helper method
        self.setStyleSheet(Theme.get_button_style(bg_color, text_color))
    
    def set_variant(self, variant):
        """Change button variant (color)"""
        self.variant = variant
        self.apply_style()
```

**Variants Needed:**
- Yellow (primary CTA)
- Green (secondary/selected)
- Blue (tertiary)
- Red (destructive)
- Gradient (purple-to-blue) - can be added as needed

**Test Script:**
```python
# examples/test_pill_button.py
# Display all 5 button variants
# Verify touch feedback
# Test with different text lengths
```

#### 3. Build IconButton Component (45 min)

**File:** `src/ui/components/icon_button.py`

**Features:**
- Circular background (60px × 60px)
- Icon support (SVG or Unicode)
- Semi-transparent background option
- Hover/press states

**Types Needed:**
- Home button (house icon)
- Settings button (gear icon)
- Search button (magnifying glass)

**Test Script:**
```python
# examples/test_icon_button.py
# Display all 3 icon button types
# Verify click detection
# Test background transparency
```

#### 4. Build Badge Components (1 hour)

**Files:**
- `src/ui/components/rating_badge.py`
- `src/ui/components/source_badge.py`

**RatingBadge:**
- Background: `Theme.BADGE_RATING` (cyan)
- Star icons + rating number
- Size: `Theme.BADGE_WIDTH × Theme.BADGE_HEIGHT` (60px × 30px)
- Border radius: `Theme.BADGE_BORDER_RADIUS` (15px)

**SourceBadge:**
- Background: `Theme.BADGE_SOURCE` (yellow)
- Text: "SBD", "AUD", "MTX"
- Size: `Theme.BADGE_WIDTH × Theme.BADGE_HEIGHT` (60px × 30px)
- Border radius: `Theme.BADGE_BORDER_RADIUS` (15px)

**Implementation Example:**
```python
from PyQt5.QtWidgets import QLabel
from src.ui.styles.theme import Theme

class RatingBadge(QLabel):
    """Star rating badge using theme styling"""
    
    def __init__(self, rating, parent=None):
        super().__init__(parent)
        self.rating = rating
        self.setText(f"★★★★★ {rating:.1f}")
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.BADGE_RATING};
                color: {Theme.TEXT_PRIMARY};
                border-radius: {Theme.BADGE_BORDER_RADIUS}px;
                padding: 5px 10px;
                font-size: {Theme.META_TEXT}px;
            }}
        """)
        
        self.setFixedSize(Theme.BADGE_WIDTH, Theme.BADGE_HEIGHT)
```

**Test Script:**
```python
# examples/test_badges.py
# Display various ratings (4.0, 4.5, 5.0)
# Display all source types (SBD, AUD, MTX)
```

#### 5. Build ConcertListItem Component (1-1.5 hours)

**File:** `src/ui/components/concert_list_item.py`

**Features:**
- Display date, venue, location
- Rating badge (right-aligned)
- Divider line at bottom
- Touch highlight state
- Emit signal when clicked

**Layout:**
```
┌────────────────────────────────────────────┐
│ 1977/05/08                      ★★★★★ 4.8 │
│ Barton Hall, Cornell University           │
│ Ithaca, NY                                 │
└────────────────────────────────────────────┘
```

**Test Script:**
```python
# examples/test_concert_list_item.py
# Display list of 10 shows
# Verify click detection
# Test rating badge display
```

#### 6. Create Component Test Suite (30 min)

**File:** `test_ui_components.py`

**Tests:**
- All button variants render correctly
- Icon buttons respond to clicks
- Badges display correct colors/text
- List items emit signals on click
- Component sizes meet touch targets (60px minimum)

### Deliverables

**Code:**
- 5 component files in `src/ui/components/`
- Theme manager in `src/ui/styles/` (1 file: theme.py, or 3-4 files if using separated approach)
- 5 test scripts in `examples/` (theme test + 4 component tests)

**Documentation:**
- Component usage examples
- Theme manager documentation
- Styling guidelines

**Validation:**
- All components tested in isolation
- Touch targets verified (60px+)
- Colors match mockups
- Theme test script runs successfully

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/ui-components

# Incremental commits
git add src/ui/styles/theme.py examples/test_theme.py
git commit -m "[Phase-10A] Task 10A.1: Add Theme Manager with all styling constants"

git add src/ui/components/pill_button.py examples/test_pill_button.py
git commit -m "[Phase-10A] Task 10A.2: Add PillButton component with theme integration"

git add src/ui/components/icon_button.py examples/test_icon_button.py
git commit -m "[Phase-10A] Task 10A.3: Add IconButton component for navigation"

git add src/ui/components/*badge.py examples/test_badges.py
git commit -m "[Phase-10A] Task 10A.4: Add RatingBadge and SourceBadge components"

git add src/ui/components/concert_list_item.py examples/test_concert_list_item.py
git commit -m "[Phase-10A] Task 10A.5: Add ConcertListItem component for browse screens"

git add test_ui_components.py
git commit -m "[Phase-10A] Task 10A.6: Add component integration test suite"

# Merge after full validation
git checkout main
git merge feature/ui-components
git push origin main
```

---

## Phase 10B: Welcome Screen Restyle

**Objective:** Apply new design to simplest screen to validate approach

**Estimated Time:** 2-3 hours

### Current Implementation

**File:** `src/ui/screens/welcome_screen.py`

**Current Features:**
- Two text buttons ("Browse Shows", "Random Show")
- Basic layout
- Default Qt styling

### New Design Requirements

**From Mockup (01-WELCOME.png):**
- Purple gradient background
- Steal Your Face logo (centered, top)
- Two large pill buttons (blue "find a show", yellow "surprise me")
- Bottom navigation icons (search, settings)

### Tasks

#### 1. Update Welcome Screen Layout (1 hour)

**Changes:**
- Apply purple gradient background
- Center logo at top third
- Update button arrangement (horizontal, centered)
- Add bottom navigation row

**Layout Structure:**
```python
QVBoxLayout (main)
├── Spacer (top)
├── QLabel (logo) - 200x200px
├── Spacer
├── QHBoxLayout (buttons)
│   ├── PillButton ("find a show") - Blue
│   └── PillButton ("surprise me") - Yellow
├── Spacer
└── QHBoxLayout (bottom nav)
    ├── Spacer
    ├── IconButton (search)
    ├── Spacer (fixed 100px)
    ├── IconButton (settings)
    └── Spacer
```

#### 2. Replace Buttons with Components (45 min)

**Before:**
```python
browse_button = QPushButton("Browse Shows")
random_button = QPushButton("Random Show")
```

**After:**
```python
from src.ui.components.pill_button import PillButton, ButtonVariant

browse_button = PillButton(
    text="find a show",
    variant=ButtonVariant.BLUE,
    min_width=350,
    min_height=90
)

random_button = PillButton(
    text="surprise me",
    variant=ButtonVariant.YELLOW,
    min_width=350,
    min_height=90
)
```

#### 3. Add Bottom Navigation (30 min)

**Add:**
```python
from src.ui.components.icon_button import IconButton

search_button = IconButton(icon="search")
settings_button = IconButton(icon="settings")

search_button.clicked.connect(self.on_search_clicked)
settings_button.clicked.connect(self.on_settings_clicked)
```

#### 4. Add Logo Asset (15 min)

**File:** `src/ui/assets/logos/steal_your_face.svg`

**Display:**
```python
logo_label = QLabel()
logo_pixmap = QPixmap("src/ui/assets/logos/steal_your_face.svg")
logo_label.setPixmap(logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio))
logo_label.setAlignment(Qt.AlignCenter)
```

#### 5. Apply Background Gradient (30 min)

**Stylesheet:**
```python
self.setStyleSheet(f"""
    WelcomeScreen {{
        background: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {BG_PRIMARY},
            stop:1 #1a1550
        );
    }}
""")
```

### Testing

**Test Script:** `examples/test_welcome_screen.py`

**Verify:**
- Logo displays correctly
- Both pill buttons work (navigate to browse/random)
- Button colors match mockup
- Bottom icons visible and clickable
- Background gradient renders properly

**Manual Checks:**
- Button sizes meet touch targets (>60px height)
- Text legible at arm's length
- Spacing matches mockup

### Git Workflow

```bash
git checkout -b feature/welcome-screen-restyle

# Add logo asset
git add src/ui/assets/logos/steal_your_face.svg
git commit -m "Add Steal Your Face logo asset"

# Update welcome screen
git add src/ui/screens/welcome_screen.py
git commit -m "Restyle welcome screen to match mockup"

# Add test
git add examples/test_welcome_screen.py
git commit -m "Add test script for welcome screen"

# Merge after validation
git checkout main
git merge feature/welcome-screen-restyle
git push origin main
```

---

## Phase 10C: Browse Screens Restyle

**Objective:** Implement sidebar navigation pattern and restyle all browse modes

**Estimated Time:** 4-6 hours

### Current Implementation

**File:** `src/ui/screens/browse_screen.py`

**Current Features:**
- Tab-based navigation (Top Rated, By Venue, By Year)
- List display for venues/shows
- Basic Qt list widgets

### New Design Requirements

**From Mockups:**
- Left sidebar (30% width) with vertical pill buttons
- Right content area (70% width)
- Three browse modes: Top Rated, By Venue, By Year
- Year mode has two sub-views: decade grid, show list

### Tasks

#### 1. Implement Sidebar Navigation Layout (1.5 hours)

**New Layout Structure:**
```python
QHBoxLayout (main)
├── QVBoxLayout (sidebar - 30%)
│   ├── Spacer (top)
│   ├── PillButton ("Top Rated")
│   ├── Spacer (20px)
│   ├── PillButton ("By Venue")
│   ├── Spacer (20px)
│   ├── PillButton ("By Year")
│   └── Spacer (bottom)
│
└── QVBoxLayout (content - 70%)
    ├── QLabel ("browse shows") - title
    ├── QStackedWidget (content modes)
    │   ├── VenueListView
    │   ├── YearDecadeView
    │   └── ShowListView
    └── Spacer
```

**Button Selection Logic:**
```python
def select_mode(self, mode_name):
    # Update button colors
    for name, button in self.mode_buttons.items():
        if name == mode_name:
            button.set_variant(ButtonVariant.GREEN)  # Selected
        else:
            button.set_variant(ButtonVariant.YELLOW)  # Normal
    
    # Switch content view
    self.content_stack.setCurrentWidget(self.views[mode_name])
```

#### 2. Restyle Venue List View (1 hour)

**Update VenueListView:**
- Use QListWidget with custom styling
- Each item uses custom stylesheet for colors/borders
- Add show count in gray text
- Divider lines between items

**List Item Stylesheet:**
```python
QListWidget {{
    background-color: {BG_CARD};
    border: none;
    border-radius: 10px;
}}

QListWidget::item {{
    padding: 15px 20px;
    border-bottom: 1px solid {BORDER_SUBTLE};
    color: {TEXT_PRIMARY};
}}

QListWidget::item:hover {{
    background-color: #2A3A4A;
}}
```

**Item Format:**
```
[Venue Name] ([Count] shows)
```

#### 3. Create Year Decade Grid View (1.5 hours)

**New Component:** `src/ui/components/year_grid.py`

**Features:**
- 2-column grid layout
- Year buttons (45% width each, 80px height)
- Some years highlighted with gradient
- PREV/NEXT navigation buttons
- Decade header (e.g., "1970s")

**Layout:**
```python
QVBoxLayout
├── QHBoxLayout (navigation)
│   ├── PillButton ("PREV") - Green, small
│   ├── QLabel ("1970s") - centered, 32px
│   └── PillButton ("NEXT") - Green, small
│
└── QGridLayout (years - 2 columns)
    ├── YearButton ("1970") - row 0, col 0
    ├── YearButton ("1971") - row 0, col 1
    ├── YearButton ("1972") - row 1, col 0 (gradient)
    └── ... (10 years total per decade)
```

**Year Button Logic:**
```python
# Highlight logic based on show count or rating
def is_highlighted(year):
    shows = get_shows_by_year(year)
    avg_rating = calculate_average_rating(shows)
    return avg_rating >= 4.3  # Threshold for highlighting
```

#### 4. Update Show List View (1 hour)

**Use ConcertListItem Component:**
```python
from src.ui.components.concert_list_item import ConcertListItem

# For each show
show_item = ConcertListItem(
    date=show['date'],
    venue=show['venue'],
    location=show['location'],
    rating=show['avg_rating']
)
show_item.clicked.connect(lambda s=show: self.load_show(s))

show_list.addWidget(show_item)
```

**List Styling:**
- Scrollable with custom scrollbar
- Divider lines between items
- Rating badges on right
- Touch highlight on press

#### 5. Add Corner Navigation Icons (30 min)

**Home and Settings Buttons:**
```python
# Top-right home button
home_button = IconButton(icon="home")
home_button.clicked.connect(self.return_home)

# Bottom-right settings button
settings_button = IconButton(icon="settings")
settings_button.clicked.connect(self.open_settings)
```

**Positioning:**
- Use absolute positioning or overlay layout
- Ensure buttons don't interfere with content

### Testing

**Test Script:** `examples/test_browse_screen.py`

**Verify:**
- All three modes switch correctly
- Sidebar buttons change color on selection
- Venue list displays and scrolls
- Year grid shows correct decade
- PREV/NEXT navigate decades
- Show list displays ratings
- Tapping show loads player screen
- Home/settings buttons work

### Git Workflow

```bash
git checkout -b feature/browse-screen-restyle

# Add year grid component
git add src/ui/components/year_grid.py examples/test_year_grid.py
git commit -m "Add YearGrid component for decade view"

# Update browse screen
git add src/ui/screens/browse_screen.py
git commit -m "Restyle browse screen with sidebar navigation"

# Add test
git add examples/test_browse_screen.py
git commit -m "Add comprehensive browse screen test"

# Merge after validation
git checkout main
git merge feature/browse-screen-restyle
git push origin main
```

---

## Phase 10D: Date Picker Restyle

**Objective:** Create three-column date picker matching mockup design

**Estimated Time:** 3-4 hours

### Current Implementation

**Likely:** Simple date selection, possibly dropdown or calendar widget

### New Design Requirements

**From Mockup (03-PICK-A-SHOW.png):**
- Title: "choose year, then month, then day"
- Three scrollable columns (Year, Month, Day)
- Selected items highlighted in green
- "Load Show" button at bottom (yellow)
- Home and settings icons in corners

### Tasks

#### 1. Create DatePickerColumn Component (1.5 hours)

**File:** `src/ui/components/date_picker_column.py`

**Features:**
- Scrollable list with large items (80px height)
- Green highlight for selected item
- 36px font for item text
- Smooth scrolling
- Emit signal on selection

**Layout:**
```python
QVBoxLayout
├── QLabel (header - "Year"/"Month"/"Day")
│   - 24px bold white
│   - 60px height
│   - Dark background
│
└── QListWidget (items)
    - 80px item height
    - 36px font
    - Green background for selected
    - Custom scrollbar
```

**Selection Logic:**
```python
class DatePickerColumn(QWidget):
    selection_changed = pyqtSignal(str)  # Emits selected value
    
    def __init__(self, header, items):
        # ...
        self.list_widget.currentItemChanged.connect(
            lambda current, previous: self.on_selection_changed(current)
        )
    
    def on_selection_changed(self, item):
        if item:
            self.selection_changed.emit(item.text())
```

#### 2. Build Date Picker Screen (1-1.5 hours)

**File:** `src/ui/screens/date_picker_screen.py` (new file)

**Layout:**
```python
QVBoxLayout (main)
├── QLabel ("choose year, then month, then day")
│   - 36px centered at top
│
├── QHBoxLayout (columns)
│   ├── DatePickerColumn ("Year", years_list)
│   ├── DatePickerColumn ("Month", months_list)
│   └── DatePickerColumn ("Day", days_list)
│
├── Spacer
│
├── PillButton ("Load Show") - Yellow
│   - Centered, 350px × 80px
│
└── Spacer
```

**Smart Day Filtering:**
```python
def update_day_column(self, year, month):
    """Filter days based on selected year/month"""
    import calendar
    
    # Get number of days in month
    if month and year:
        num_days = calendar.monthrange(int(year), month_to_num(month))[1]
        days = [f"{d:02d}" for d in range(1, num_days + 1)]
    else:
        days = [f"{d:02d}" for d in range(1, 32)]
    
    self.day_column.update_items(days)
```

#### 3. Integrate with Browse Screen (30 min)

**Navigation Flow:**
- Browse screen → "By Year" mode has option to "Pick a Date"
- OR: Main menu has "pick a show" that goes to date picker

**Add to screen_manager:**
```python
# In main_window.py
self.date_picker_screen = DatePickerScreen(self.db_path)
self.screen_manager.add_screen('date_picker', self.date_picker_screen)

# Connect load button
self.date_picker_screen.show_selected.connect(self.load_show_by_date)
```

#### 4. Add Corner Navigation (30 min)

**Same as browse screen:**
- Home button (top-right)
- Settings button (bottom-right)

#### 5. Handle "No Show" Case (30 min)

**Error Handling:**
```python
def load_show_by_date(self, year, month, day):
    date_str = f"{year}/{month}/{day}"
    shows = get_shows_by_date(date_str)
    
    if not shows:
        # Show error dialog
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"No shows found for {date_str}")
        msg.setWindowTitle("No Shows")
        msg.exec_()
    elif len(shows) == 1:
        # Load single show
        self.screen_manager.load_and_play_show(shows[0])
    else:
        # Multiple shows - display list for selection
        self.show_selection_list(shows)
```

### Testing

**Test Script:** `examples/test_date_picker.py`

**Verify:**
- Three columns display and scroll
- Selection highlights in green
- Month selection updates day count (e.g., February → 28/29 days)
- "Load Show" button works
- Handles dates with no shows gracefully
- Handles dates with multiple shows
- Home/settings buttons work

### Git Workflow

```bash
git checkout -b feature/date-picker-screen

# Add component
git add src/ui/components/date_picker_column.py examples/test_date_picker_column.py
git commit -m "Add DatePickerColumn component"

# Add screen
git add src/ui/screens/date_picker_screen.py
git commit -m "Add DatePickerScreen with three-column layout"

# Integration
git add src/ui/main_window.py
git commit -m "Integrate date picker screen into navigation"

# Test
git add examples/test_date_picker.py
git commit -m "Add date picker test script"

# Merge
git checkout main
git merge feature/date-picker-screen
git push origin main
```

---

## Phase 10E: Player Screen Restyle

**Objective:** Implement split-screen layout with polished playback controls

**Estimated Time:** 6-8 hours

### Current Implementation

**File:** `src/ui/screens/player_screen.py`

**Current Features:**
- Concert info display
- Setlist display
- Playback controls (play/pause, next, previous)
- Progress bar
- Volume control

### New Design Requirements

**From Mockup (02-PLAYER.png):**
- 50/50 split screen layout
- Left: Dark blue panel with concert info + setlist
- Right: Black panel with playback controls
- Enhanced controls (15s skip buttons)
- Larger, touch-friendly controls
- Source badge (SBD/AUD) next to concert header

### Tasks

#### 1. Implement Split-Screen Layout (1.5 hours)

**New Layout Structure:**
```python
QHBoxLayout (main - equal split)
├── QWidget (left_panel - 50%)
│   ├── Concert Info Header
│   ├── Setlist Widget (scrollable)
│   └── ...
│
└── QWidget (right_panel - 50%)
    ├── "NOW PLAYING" header
    ├── Song Title
    ├── Progress Bar
    ├── Playback Controls
    └── Volume Control
```

**Panel Styling:**
```python
# Left panel
left_panel.setStyleSheet(f"""
    QWidget {{
        background-color: {BG_PANEL_DARK};
        border-radius: 10px;
    }}
""")

# Right panel
right_panel.setStyleSheet(f"""
    QWidget {{
        background-color: {BG_PANEL_BLACK};
    }}
""")
```

#### 2. Enhance Concert Info Header (1 hour)

**Header Layout:**
```python
QVBoxLayout
├── QHBoxLayout (date row)
│   ├── QLabel (date - "12/28/1980")
│   ├── Spacer
│   └── SourceBadge ("SBD")
│
├── QLabel (venue - "Oakland Auditorium Arena")
└── QLabel (location - "Oakland, CA")
```

**Source Badge:**
```python
from src.ui.components.source_badge import SourceBadge

source_type = show.get('source_type', 'Unknown')
badge = SourceBadge(source_type)  # "SBD", "AUD", "MTX"
```

#### 3. Create Setlist Widget (1.5 hours)

**File:** `src/ui/components/setlist_widget.py`

**Features:**
- Display songs grouped by set
- Set headers ("Set I", "Set II", "Encore")
- Scrollable list
- Currently playing song highlighted
- Click to seek to song

**Layout:**
```python
QVBoxLayout (in QScrollArea)
├── QLabel ("Set I") - gray header
├── SongItem ("Mississippi Half Step...")
├── SongItem ("Franklin's Tower...")
├── ...
├── QLabel ("Set II") - gray header
├── SongItem ("Don't Ease Me In...")
├── ...
```

**Currently Playing Highlight:**
```python
def update_current_song(self, song_index):
    # Highlight current, unhighlight others
    for i, song_widget in enumerate(self.song_widgets):
        if i == song_index:
            song_widget.setStyleSheet(f"background-color: {ACCENT_GREEN};")
        else:
            song_widget.setStyleSheet("background-color: transparent;")
```

#### 4. Enhance Playback Controls (2 hours)

**Control Layout:**
```python
QHBoxLayout
├── IconButton (15s back) - 60×60px
├── IconButton (previous) - 60×60px
├── IconButton (play/pause) - 80×80px (larger)
├── IconButton (next) - 60×60px
└── IconButton (15s forward) - 60×60px
```

**15-Second Skip Buttons:**
```python
# Add to ResilientPlayer integration
def skip_backward_15s(self):
    current_time = self.player.get_time()
    new_time = max(0, current_time - 15000)  # -15 seconds in ms
    self.player.set_time(new_time)

def skip_forward_15s(self):
    current_time = self.player.get_time()
    duration = self.player.get_length()
    new_time = min(duration, current_time + 15000)  # +15 seconds in ms
    self.player.set_time(new_time)
```

**Play/Pause Button:**
- Larger size (80×80px)
- Toggle between play and pause icons
- Update based on player state

#### 5. Create Seekable Progress Bar (1.5 hours)

**File:** `src/ui/components/seekable_progress.py`

**Features:**
- Click anywhere to seek
- Drag thumb to seek
- Display current time / total time
- Update position every 200ms

**Implementation:**
```python
class SeekableProgressBar(QSlider):
    seek_requested = pyqtSignal(int)  # Emits position in ms
    
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setMinimum(0)
        self.setMaximum(1000)  # 0-1000 range
        
        # Style
        self.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 8px;
                background: #444444;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                width: 24px;
                height: 24px;
                background: white;
                border-radius: 12px;
                margin: -8px 0;
            }}
        """)
    
    def mousePressEvent(self, event):
        # Allow click to seek
        position = event.x() / self.width()
        value = int(position * self.maximum())
        self.setValue(value)
        self.seek_requested.emit(value)
        super().mousePressEvent(event)
```

**Time Labels:**
```python
QHBoxLayout
├── QLabel (current_time - "0:00")
├── SeekableProgressBar
└── QLabel (total_time - "7:42")
```

#### 6. Update Volume Control (30 min)

**Enhanced Styling:**
- Wider track (match progress bar width)
- Larger thumb with speaker icon
- Mute button on left
- Volume icon on thumb

**Layout:**
```python
QHBoxLayout
├── IconButton (mute) - speaker with X
├── QSlider (volume)
└── QLabel (volume icon on thumb)
```

#### 7. Add Corner Navigation (30 min)

**Home and Settings:**
- Same as other screens
- Home: Top-right of right panel
- Settings: Bottom-right of right panel

### Testing

**Test Script:** `examples/test_player_screen.py`

**Verify:**
- Split layout renders correctly (50/50)
- Concert info displays properly
- Source badge shows correct type
- Setlist scrolls and highlights current song
- All 5 playback buttons work
- 15s skip buttons seek correctly
- Progress bar updates in real-time
- Clicking progress bar seeks to position
- Volume slider adjusts volume
- Mute button works
- Home/settings buttons navigate correctly

**Integration Test:**
```python
# test_player_integration.py
# Load show from browse screen
# Verify all player data populated
# Test playback start/stop
# Test skip to next track
# Test seeking within track
```

### Git Workflow

```bash
git checkout -b feature/player-screen-restyle

# Components
git add src/ui/components/setlist_widget.py examples/test_setlist_widget.py
git commit -m "Add SetlistWidget component"

git add src/ui/components/seekable_progress.py examples/test_seekable_progress.py
git commit -m "Add SeekableProgressBar component with click-to-seek"

# Player screen
git add src/ui/screens/player_screen.py
git commit -m "Restyle player screen with split layout"

# Tests
git add examples/test_player_screen.py test_player_integration.py
git commit -m "Add player screen tests"

# Merge
git checkout main
git merge feature/player-screen-restyle
git push origin main
```

---

## Phase 10F: Random Show Screen

**Objective:** Create new screen for random show preview

**Estimated Time:** 3-4 hours

### New Screen Implementation

**File:** `src/ui/screens/random_show_screen.py` (new file)

### Design Requirements

**From Mockup (05-RANDOM-SHOW.png):**
- Concert header at top (date, venue, location)
- Large panel with full setlist
- Two action buttons at bottom ("roll tape", "try again")
- Home and settings icons

### Tasks

#### 1. Create Random Show Screen (2 hours)

**Layout:**
```python
QVBoxLayout (main)
├── QVBoxLayout (header)
│   ├── QLabel (date - "12/28/1980")
│   ├── QLabel (venue - "Oakland Auditorium Arena")
│   └── QLabel (location - "Oakland, CA")
│
├── QWidget (setlist_panel)
│   └── SetlistWidget (reuse from player screen)
│       - Full setlist display
│       - Scrollable
│       - Dark background
│
├── Spacer
│
└── QHBoxLayout (actions)
    ├── PillButton ("roll tape") - Red
    └── PillButton ("try again") - Gradient
```

**Random Show Selection Logic:**
```python
def load_random_show(self):
    """Select a random show from database"""
    from src.database.queries import get_random_show
    
    show = get_random_show(
        min_rating=4.0,      # Quality threshold
        source_types=['SBD'] # Prefer soundboards
    )
    
    self.display_show(show)
```

#### 2. Integrate with Welcome Screen (30 min)

**Update welcome_screen.py:**
```python
# "surprise me" button connects to random show screen
self.random_button.clicked.connect(
    lambda: self.screen_manager.show_random_show()
)
```

**In screen_manager:**
```python
def show_random_show(self):
    self.screens['random_show'].load_random_show()
    self.show_screen('random_show')
```

#### 3. Implement Action Buttons (1 hour)

**"roll tape" Button:**
```python
def on_roll_tape(self):
    """Load show into player and start playback"""
    self.screen_manager.load_and_play_show(self.current_show)
```

**"try again" Button:**
```python
def on_try_again(self):
    """Load a different random show"""
    self.load_random_show()
```

#### 4. Add Corner Navigation (30 min)

**Home and Settings:**
- Same pattern as other screens
- Home returns to welcome screen
- Settings opens settings screen

#### 5. Handle Edge Cases (30 min)

**Error Handling:**
```python
# No shows meeting criteria
if not show:
    # Show message and return to welcome
    msg = QMessageBox.information(
        self, "No Shows",
        "Could not find a random show. Try relaxing your filters."
    )
    self.screen_manager.show_screen('welcome')
    return

# API failure to get setlist
try:
    metadata = get_metadata(show['identifier'])
    setlist = extract_setlist(metadata)
except Exception as e:
    # Display show with "Setlist unavailable" message
    setlist = ["[Setlist information not available]"]
```

### Testing

**Test Script:** `examples/test_random_show_screen.py`

**Verify:**
- Random show loads on screen display
- Concert info displays correctly
- Setlist displays (or shows error message)
- "roll tape" loads player screen with show
- "try again" loads different show
- Shows vary on multiple tries
- Home/settings navigation works

**Edge Cases:**
- Database has no qualifying shows
- API fails to fetch metadata
- Show has no setlist data

### Git Workflow

```bash
git checkout -b feature/random-show-screen

# Create screen
git add src/ui/screens/random_show_screen.py
git commit -m "Add RandomShowScreen for surprise show selection"

# Integration
git add src/ui/main_window.py src/ui/screens/welcome_screen.py
git commit -m "Integrate random show screen with navigation"

# Tests
git add examples/test_random_show_screen.py
git commit -m "Add random show screen tests"

# Merge
git checkout main
git merge feature/random-show-screen
git push origin main
```

---

## Phase 10G: Settings Screen Restyle

**Objective:** Apply sidebar navigation pattern to settings screen

**Estimated Time:** 4-6 hours

### Current Implementation

**File:** `src/ui/screens/settings_screen.py`

**Current Features:**
- Category-based settings
- Persistence to JSON file
- Basic Qt widgets

### New Design Requirements

**Extrapolated from Design System:**
- Sidebar navigation (like browse screens)
- Category buttons (Network, Display, Audio, About)
- Right content area with settings controls
- Consistent styling with other screens

### Tasks

#### 1. Implement Sidebar Navigation (1.5 hours)

**Layout Structure:**
```python
QHBoxLayout (main)
├── QVBoxLayout (sidebar - 30%)
│   ├── Spacer
│   ├── PillButton ("Network")
│   ├── Spacer (20px)
│   ├── PillButton ("Display")
│   ├── Spacer (20px)
│   ├── PillButton ("Audio")
│   ├── Spacer (20px)
│   ├── PillButton ("About")
│   └── Spacer
│
└── QVBoxLayout (content - 70%)
    ├── QLabel (category title)
    ├── QStackedWidget (category content)
    │   ├── NetworkSettings
    │   ├── DisplaySettings
    │   ├── AudioSettings
    │   └── AboutScreen
    └── Spacer
```

**Category Selection:**
```python
def select_category(self, category_name):
    # Update sidebar button colors
    for name, button in self.category_buttons.items():
        if name == category_name:
            button.set_variant(ButtonVariant.GREEN)
        else:
            button.set_variant(ButtonVariant.YELLOW)
    
    # Show category content
    self.content_stack.setCurrentWidget(self.categories[category_name])
```

#### 2. Restyle Network Settings (1 hour)

**Settings:**
- Internet connection status (read-only display)
- "Check for Updates" button

**Layout:**
```python
QVBoxLayout
├── QLabel ("Network") - title
├── Spacer (20px)
│
├── QHBoxLayout (connection status)
│   ├── QLabel ("Internet Connection:")
│   └── QLabel (status - "Connected" / "Disconnected")
│       - Green text if connected
│       - Red text if disconnected
│
├── Spacer (30px)
│
├── QPushButton ("Check for Updates")
│   - Standard button (not pill)
│   - 200px wide
│
└── Spacer (fill remaining)
```

#### 3. Restyle Display Settings (1 hour)

**Settings:**
- Screen brightness (slider)
- Screen timeout (dropdown)

**Layout:**
```python
QVBoxLayout
├── QLabel ("Display") - title
├── Spacer (20px)
│
├── QLabel ("Brightness")
├── QSlider (brightness)
│   - 0-100 range
│   - Styled like volume slider
│
├── Spacer (30px)
│
├── QLabel ("Screen Timeout")
├── QComboBox (timeout options)
│   - Options: "1 minute", "5 minutes", "Never"
│
└── Spacer (fill)
```

#### 4. Restyle Audio Settings (1 hour)

**Settings:**
- Master volume (slider)
- Audio output device (dropdown)

**Layout:**
```python
QVBoxLayout
├── QLabel ("Audio") - title
├── Spacer (20px)
│
├── QLabel ("Master Volume")
├── QSlider (volume)
│   - 0-100 range
│   - Styled like player volume
│
├── Spacer (30px)
│
├── QLabel ("Audio Output")
├── QComboBox (output devices)
│   - Options: "Auto", "DAC", "HDMI", "Headphones"
│
└── Spacer (fill)
```

#### 5. Create About Screen (1 hour)

**Content:**
- App version
- Database statistics
- Credits
- Reset button

**Layout:**
```python
QVBoxLayout
├── QLabel ("About") - title
├── Spacer (20px)
│
├── QLabel ("DeadStream v1.0")
│   - 24px font
│
├── Spacer (10px)
│
├── QLabel ("Database: 12,268 shows")
│   - Gray text
│
├── Spacer (10px)
│
├── QLabel ("Created by [Your Name]")
│   - Gray text
│
├── Spacer (30px)
│
├── QTextEdit (credits/acknowledgments)
│   - Read-only
│   - Scrollable
│   - List of libraries, data sources, etc.
│
├── Spacer (fill)
│
└── QPushButton ("Reset to Defaults")
    - Red background (destructive action)
    - Confirmation dialog on click
```

#### 6. Add Corner Navigation (30 min)

**Home Button Only:**
- Top-right corner
- Returns to welcome screen
- No settings button (already on settings)

#### 7. Settings Persistence (30 min)

**Ensure all settings save/load:**
```python
def save_settings(self):
    """Save all settings to JSON file"""
    settings = {
        'brightness': self.brightness_slider.value(),
        'timeout': self.timeout_combo.currentText(),
        'volume': self.volume_slider.value(),
        'audio_output': self.output_combo.currentText()
    }
    
    with open(self.settings_file, 'w') as f:
        json.dump(settings, f, indent=2)

def load_settings(self):
    """Load settings from JSON file"""
    try:
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)
        
        self.brightness_slider.setValue(settings.get('brightness', 50))
        self.timeout_combo.setCurrentText(settings.get('timeout', '5 minutes'))
        # ... etc
    except FileNotFoundError:
        # Use defaults
        pass
```

### Testing

**Test Script:** `examples/test_settings_screen.py`

**Verify:**
- All category buttons switch content correctly
- Selected category highlighted in green
- All settings controls work (sliders, dropdowns)
- Settings persist across app restarts
- "Reset to Defaults" works (with confirmation)
- Home button returns to welcome

**Integration Test:**
```python
# test_settings_persistence.py
# Change all settings
# Close app
# Reopen app
# Verify settings retained
```

### Git Workflow

```bash
git checkout -b feature/settings-screen-restyle

# Restyle settings screen
git add src/ui/screens/settings_screen.py
git commit -m "Restyle settings screen with sidebar navigation"

# Tests
git add examples/test_settings_screen.py test_settings_persistence.py
git commit -m "Add settings screen tests"

# Merge
git checkout main
git merge feature/settings-screen-restyle
git push origin main
```

---

## Phase 10H: Final Polish

**Objective:** Add finishing touches, animations, and comprehensive testing

**Estimated Time:** 4-6 hours

### Tasks

#### 1. Add Screen Transition Animations (1.5 hours)

**Option 1: Fade Transition**
```python
class ScreenManager(QStackedWidget):
    def show_screen(self, screen_name, fade_duration=300):
        # Get widgets
        from_widget = self.currentWidget()
        to_widget = self.screens[screen_name]
        
        # Fade out current
        fade_out = QPropertyAnimation(from_widget, b"windowOpacity")
        fade_out.setDuration(fade_duration // 2)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        
        # Switch widget
        fade_out.finished.connect(lambda: self.setCurrentWidget(to_widget))
        
        # Fade in new
        fade_in = QPropertyAnimation(to_widget, b"windowOpacity")
        fade_in.setDuration(fade_duration // 2)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        
        # Start animations
        fade_out.start()
        fade_in.start()
```

**Option 2: Instant Switch (Simpler, More Reliable)**
```python
# Just switch immediately (no animation)
self.setCurrentWidget(to_widget)
```

**Decision:** Test both on Raspberry Pi, choose based on performance

#### 2. Implement Touch State Feedback (1 hour)

**Add pressed state to all buttons:**
```python
class PillButton(QPushButton):
    def __init__(self, text, variant):
        super().__init__(text)
        self.variant = variant
        self.normal_style = self.get_style(variant)
        self.pressed_style = self.get_pressed_style(variant)
        
        self.setStyleSheet(self.normal_style)
    
    def mousePressEvent(self, event):
        # Visual feedback on press
        self.setStyleSheet(self.pressed_style)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        # Restore normal style
        self.setStyleSheet(self.normal_style)
        super().mouseReleaseEvent(event)
    
    def get_pressed_style(self, variant):
        # Slightly darker/lighter + scale down
        return self.normal_style + """
            QPushButton {
                opacity: 0.9;
                transform: scale(0.98);
            }
        """
```

#### 3. Fine-Tune Spacing and Alignment (1 hour)

**Check all screens for:**
- Consistent margins (20px default)
- Proper centering of elements
- Equal spacing between buttons (20-30px)
- Comfortable touch targets (60px minimum)
- Text alignment (left, center, right as appropriate)

**Use layout inspection:**
```python
# Enable layout debugging (during development)
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_EnableHighDpiScaling)

# Show layout borders for debugging
app.setStyleSheet("* { border: 1px solid red; }")
```

#### 4. Integrate Icon Assets (1 hour)

**Add all icon files:**
```
src/ui/assets/icons/
├── home.svg
├── settings.svg
├── search.svg
├── play.svg
├── pause.svg
├── next.svg
├── previous.svg
├── seek_back.svg
├── seek_forward.svg
├── mute.svg
├── volume.svg
└── star.svg
```

**Update IconButton to use actual assets:**
```python
class IconButton(QPushButton):
    def __init__(self, icon_name):
        super().__init__()
        
        # Load icon from assets
        icon_path = f"src/ui/assets/icons/{icon_name}.svg"
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(32, 32))
        
        # Styling
        self.setFixedSize(60, 60)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 30px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.7);
            }
        """)
```

**Fallback to Unicode if no assets:**
```python
# Temporary until assets created
FALLBACK_ICONS = {
    'home': '⌂',
    'settings': '⚙',
    'search': '🔍',
    'play': '▶',
    'pause': '⏸',
    # ... etc
}

if not os.path.exists(icon_path):
    self.setText(FALLBACK_ICONS.get(icon_name, '?'))
```

#### 5. Cross-Screen Consistency Check (1 hour)

**Verify all screens have:**
- Same background colors
- Consistent button styling
- Same font sizes for similar elements
- Proper home/settings button placement
- Same navigation patterns

**Checklist:**
```
[ ] Welcome Screen
    [ ] Background gradient correct
    [ ] Logo centered and sized properly
    [ ] Buttons match mockup colors/sizes
    [ ] Bottom icons aligned correctly

[ ] Browse Screen (all 3 modes)
    [ ] Sidebar width 30%
    [ ] Content width 70%
    [ ] Selected button green
    [ ] List items styled consistently
    [ ] Home/settings in correct corners

[ ] Date Picker Screen
    [ ] Three columns equal width
    [ ] Title centered at top
    [ ] Load Show button centered bottom
    [ ] Green selection highlight

[ ] Player Screen
    [ ] 50/50 split layout
    [ ] Left panel dark blue
    [ ] Right panel black
    [ ] All controls touch-friendly
    [ ] Progress bar functional

[ ] Random Show Screen
    [ ] Header styled correctly
    [ ] Setlist panel displays properly
    [ ] Action buttons correct colors
    [ ] Navigation icons present

[ ] Settings Screen
    [ ] Sidebar matches browse screen
    [ ] Settings controls functional
    [ ] All categories accessible
```

#### 6. Raspberry Pi Touchscreen Testing (1.5 hours)

**Deploy to Pi and test:**
```bash
# SSH to Pi
ssh pi@raspberrypi

# Pull latest code
cd ~/deadstream
git pull

# Run on Pi with touchscreen
DISPLAY=:0 python3 src/ui/main_window.py
```

**Test on actual hardware:**
- Touch targets large enough?
- Text readable at arm's length?
- Colors accurate on Pi display?
- Performance acceptable (no lag)?
- Scrolling smooth?
- All buttons respond to touch?

**Common Issues:**
- Display scaling (may need to adjust for 7-inch screen)
- Touch calibration
- Font rendering differences
- Performance optimization

#### 7. Create Comprehensive Integration Test (1 hour)

**File:** `test_ui_integration.py`

**Test full user flows:**
```python
def test_welcome_to_player_flow():
    """Test: Welcome → Browse → Player"""
    # Launch app
    app, window = create_test_app()
    
    # Start at welcome
    assert window.screen_manager.current_screen() == 'welcome'
    
    # Click "find a show"
    window.welcome_screen.browse_button.click()
    wait_for_transition()
    
    # Should be at browse screen
    assert window.screen_manager.current_screen() == 'browse'
    
    # Select top-rated mode
    window.browse_screen.select_mode('top_rated')
    wait_for_transition()
    
    # Click first show
    first_show = window.browse_screen.show_list.item(0)
    first_show.clicked.emit(first_show.show_data)
    wait_for_transition()
    
    # Should be at player screen
    assert window.screen_manager.current_screen() == 'player'
    
    # Player should be playing
    assert window.player_screen.is_playing()

def test_random_show_flow():
    """Test: Welcome → Random Show → Player"""
    # ... similar test for random show

def test_date_picker_flow():
    """Test: Welcome → Browse → Date Picker → Player"""
    # ... test date selection flow

def test_settings_persistence():
    """Test: Settings save and load correctly"""
    # ... test all settings persist
```

### Deliverables

**Code:**
- Screen transition animations (if used)
- Touch state feedback on all buttons
- Icon assets integrated
- All spacing/alignment polished

**Testing:**
- Comprehensive integration test suite
- Raspberry Pi hardware validation
- Cross-screen consistency verified

**Documentation:**
- Update completion summary
- Document any Pi-specific tweaks
- Note performance optimizations

### Git Workflow

```bash
git checkout -b feature/final-polish

# Animations
git add src/ui/screen_manager.py
git commit -m "Add screen transition animations"

# Touch feedback
git add src/ui/components/*.py
git commit -m "Implement touch state feedback for all buttons"

# Icon integration
git add src/ui/assets/icons/*.svg src/ui/components/icon_button.py
git commit -m "Integrate SVG icon assets"

# Spacing fixes
git add src/ui/screens/*.py
git commit -m "Fine-tune spacing and alignment across all screens"

# Integration tests
git add test_ui_integration.py
git commit -m "Add comprehensive UI integration tests"

# Pi optimizations
git add src/ui/main_window.py
git commit -m "Optimize for Raspberry Pi touchscreen"

# Merge
git checkout main
git merge feature/final-polish
git push origin main
```

---

## Summary Timeline

**Estimated Total Time:** 30-43 hours

| Phase | Task | Estimated Time |
|-------|------|----------------|
| 10A | Core Component Library | 4-6 hours |
| 10B | Welcome Screen Restyle | 2-3 hours |
| 10C | Browse Screens Restyle | 4-6 hours |
| 10D | Date Picker Restyle | 3-4 hours |
| 10E | Player Screen Restyle | 6-8 hours |
| 10F | Random Show Screen | 3-4 hours |
| 10G | Settings Screen Restyle | 4-6 hours |
| 10H | Final Polish | 4-6 hours |

**Total:** 30-43 hours of focused development

---

## Success Criteria

Phase 10 (UI Restyling) is complete when:

**Functionality:**
- [ ] All existing features still work (no regressions)
- [ ] All screens navigate correctly
- [ ] Player plays shows from all entry points
- [ ] Settings persist correctly
- [ ] Random show generates properly

**Visual Design:**
- [ ] All screens match mockup designs
- [ ] Colors accurate to design system
- [ ] Font sizes consistent with specifications
- [ ] Spacing and alignment polished
- [ ] Icons integrated (or fallback Unicode working)
- [ ] Theme Manager implemented (easy to experiment with colors/fonts)

**Touch Interface:**
- [ ] All buttons meet 60px minimum touch target
- [ ] Touch feedback visible on all interactive elements
- [ ] Scrolling smooth and responsive
- [ ] No accidental activations

**Cross-Platform:**
- [ ] Works on macOS development environment
- [ ] Works on Raspberry Pi with touchscreen
- [ ] Display scales properly for 7-inch screen
- [ ] Performance acceptable on Pi hardware

**Testing:**
- [ ] All component tests pass
- [ ] All screen tests pass
- [ ] Integration test suite passes
- [ ] Manual testing on Pi complete

**Documentation:**
- [ ] Completion summary updated
- [ ] Design system documented
- [ ] Component library documented
- [ ] Known issues (if any) documented

---

## Risk Mitigation

**Potential Risks:**

1. **Performance on Raspberry Pi**
   - Mitigation: Test frequently on hardware, optimize as needed
   - Fallback: Reduce animations or effects if laggy

2. **Touch Calibration Issues**
   - Mitigation: Test with actual touchscreen early
   - Fallback: Ensure mouse also works for testing

3. **Icon Asset Delays**
   - Mitigation: Use Unicode fallbacks initially
   - Fallback: Temporary text labels until assets ready

4. **Scope Creep**
   - Mitigation: Stick to mockup designs, no extra features
   - Fallback: Mark "nice to have" features for post-launch

5. **Integration Breakage**
   - Mitigation: Keep existing functionality intact, test frequently
   - Fallback: Git branches allow easy rollback if needed

---

## Next Steps After Phase 10

**Once UI Restyling is Complete:**

1. **Phase 11: Hardware Integration**
   - Install touchscreen physically
   - Install DAC for audio
   - Configure Pi for kiosk mode
   - Test with actual hardware assembly

2. **Phase 12: Auto-Play Features**
   - Implement auto-play next track
   - Handle end-of-show scenarios
   - Queue management
   - Shuffle/repeat modes (if desired)

3. **Phase 13: Final Testing & Documentation**
   - End-to-end testing of all features
   - User documentation
   - Installation guide
   - Troubleshooting guide
   - Release preparation

---

## Document Maintenance

**Update this plan when:**
- Completing each phase (mark as done)
- Discovering additional work (adjust estimates)
- Finding better approaches (update tasks)
- Hitting blockers (document workarounds)

**Completion Tracking:**
- [ ] Phase 10A: Core Component Library
- [ ] Phase 10B: Welcome Screen Restyle
- [ ] Phase 10C: Browse Screens Restyle
- [ ] Phase 10D: Date Picker Restyle
- [ ] Phase 10E: Player Screen Restyle
- [ ] Phase 10F: Random Show Screen
- [ ] Phase 10G: Settings Screen Restyle
- [ ] Phase 10H: Final Polish

---

**This implementation plan provides a clear, step-by-step roadmap for restyling the entire DeadStream application to match the mockup designs.**
