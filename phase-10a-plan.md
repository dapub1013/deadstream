# Phase 10A Implementation Plan: Core Component Library

**Phase**: 10A (UI Restyling Foundation)  
**Estimated Duration**: 4-6 hours  
**Status**: Not Started  
**Created**: January 6, 2026  
**Revised**: January 6, 2026

## Overview

Phase 10A establishes the foundation for the complete UI restyling based on design mockups. This phase creates a centralized Theme Manager and reusable component library that all screens will use, making the entire application easy to maintain and style.

### Why This Phase Exists

Before restyling individual screens, we need:
- **Centralized styling system** (Theme Manager) - one place to change colors, fonts, spacing
- **Reusable components** - consistent buttons, badges, and UI elements
- **Foundation for rapid iteration** - ability to experiment with different designs quickly
- **Zero technical debt** - properly architected from the start

This foundational work enables all subsequent phases (10B-10H) to move faster and maintain consistency.

### Core Philosophy

**Flexibility First**: Every styling decision should be easy to change later. The Theme Manager approach means:
- Change entire app color scheme in 30 seconds (edit one file)
- Adjust font sizes system-wide instantly
- Experiment with different designs without fear
- No hardcoded values scattered across codebase

---

## Task Breakdown

### Task 1: Theme Manager Implementation (1.5-2 hours)

#### Subtask 1.1: Create Theme Manager File (1-1.5 hours)
**File**: `src/ui/styles/theme.py`

**Purpose**: Single source of truth for all visual styling constants.

**Complete Implementation**: See Design System document, Section 3: Theme Manager for full code.

**Key Components**:

```python
class Theme:
    """
    Centralized theme manager for DeadStream UI.
    All styling constants in one place for easy updates.
    """
    
    # ============================================
    # BACKGROUND COLORS
    # ============================================
    BG_PRIMARY = "#2E2870"      # Deep purple - main background
    BG_PANEL_DARK = "#1A2332"   # Dark blue-gray - concert info
    BG_PANEL_BLACK = "#000000"  # Pure black - player panel
    BG_CARD = "#1E2936"         # Darker gray - list items
    
    # ============================================
    # ACCENT COLORS
    # ============================================
    ACCENT_YELLOW = "#FFD700"   # Primary CTA buttons
    ACCENT_GREEN = "#0F9D58"    # Selected/active state
    ACCENT_BLUE = "#1976D2"     # Secondary actions
    ACCENT_RED = "#FF0000"      # Destructive/exciting
    
    # ... (all colors, typography, spacing)
    
    # ============================================
    # HELPER METHODS
    # ============================================
    
    @classmethod
    def get_button_style(cls, bg_color, text_color=None):
        """Generate standard button stylesheet"""
        # ...
    
    @classmethod
    def get_list_style(cls):
        """Generate standard list widget stylesheet"""
        # ...
    
    @classmethod
    def get_global_stylesheet(cls):
        """Generate global application stylesheet"""
        # ...
```

**What to Include**:
1. All color constants (16 colors)
2. All typography constants (7 font sizes + weights + family)
3. All spacing constants (margins, padding, gaps)
4. All component size constants (buttons, icons, badges, controls)
5. Helper methods for generating stylesheets
6. Color manipulation utility (`_lighten_color()`)

**Reference**: Complete implementation in Design System document (`deadstream-design-system.md`), Section 3.

**Testing**:
- [ ] File imports without errors
- [ ] All constants accessible
- [ ] Helper methods return valid stylesheets
- [ ] Color manipulation works correctly

---

#### Subtask 1.2: Create Theme Test Script (0.5 hours)
**File**: `examples/test_theme.py`

**Purpose**: Quick visual test for experimenting with theme changes.

**Implementation**:
```python
"""
Quick visual test of theme colors and sizes.
Useful for experimenting with theme changes.
"""
import sys
sys.path.insert(0, '/path/to/deadstream')  # Adjust path

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                              QPushButton, QLabel)
from src.ui.styles.theme import Theme

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("Theme Test")
    window.resize(600, 500)
    window.setStyleSheet(Theme.get_global_stylesheet())
    
    layout = QVBoxLayout()
    layout.setSpacing(Theme.SPACING_MEDIUM)
    layout.setContentsMargins(
        Theme.MARGIN_LARGE,
        Theme.MARGIN_LARGE,
        Theme.MARGIN_LARGE,
        Theme.MARGIN_LARGE
    )
    
    # Test all button color variants
    button_variants = [
        ("Yellow Button", Theme.ACCENT_YELLOW, Theme.TEXT_DARK),
        ("Green Button", Theme.ACCENT_GREEN, Theme.TEXT_PRIMARY),
        ("Blue Button", Theme.ACCENT_BLUE, Theme.TEXT_PRIMARY),
        ("Red Button", Theme.ACCENT_RED, Theme.TEXT_PRIMARY),
    ]
    
    for text, bg_color, text_color in button_variants:
        btn = QPushButton(text)
        btn.setStyleSheet(Theme.get_button_style(bg_color, text_color))
        layout.addWidget(btn)
    
    # Test typography sizes
    typography_tests = [
        (Theme.HEADER_LARGE, "Header Large (48px)"),
        (Theme.HEADER_MEDIUM, "Header Medium (36px)"),
        (Theme.HEADER_SMALL, "Header Small (24px)"),
        (Theme.BODY_LARGE, "Body Large (20px)"),
        (Theme.BODY_MEDIUM, "Body Medium (16px)"),
        (Theme.BODY_SMALL, "Body Small (14px)"),
    ]
    
    for size, text in typography_tests:
        label = QLabel(text)
        label.setStyleSheet(f"font-size: {size}px; color: {Theme.TEXT_PRIMARY};")
        layout.addWidget(label)
    
    window.setLayout(layout)
    window.show()
    
    print("\n[INFO] Theme Test Window Opened")
    print("[INFO] Change values in src/ui/styles/theme.py and rerun to see updates")
    print("[INFO] Press Ctrl+C or close window to exit\n")
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

**Usage**:
```bash
# Run test to see all theme colors and sizes
python3 examples/test_theme.py

# Make changes to theme.py
# Rerun test to see instant results
```

**Testing**:
- [ ] Script runs without errors
- [ ] All button colors display correctly
- [ ] All font sizes render properly
- [ ] Window uses theme background color
- [ ] Changes to theme.py reflect immediately on rerun

---

### Task 2: PillButton Component (1 hour)

#### Subtask 2.1: Create PillButton Class (45 min)
**File**: `src/ui/components/pill_button.py`

**Purpose**: Reusable rounded button with theme-based color variants.

**Implementation**:
```python
"""
PillButton - Large rounded button with theme-based styling.

Usage:
    from src.ui.components.pill_button import PillButton, ButtonVariant
    
    button = PillButton("Click Me", variant=ButtonVariant.YELLOW)
    button.clicked.connect(on_click_handler)
"""

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from src.ui.styles.theme import Theme

class ButtonVariant:
    """Button color variant constants"""
    YELLOW = 'yellow'
    GREEN = 'green'
    BLUE = 'blue'
    RED = 'red'
    GRADIENT = 'gradient'

class PillButton(QPushButton):
    """
    Large rounded button with theme-based styling.
    
    Features:
    - Multiple color variants (yellow, green, blue, red, gradient)
    - Touch-friendly sizing (80px height minimum)
    - Smooth press animation
    - Theme Manager integration
    
    Args:
        text (str): Button text
        variant (str): Color variant from ButtonVariant class
        parent (QWidget): Parent widget
    """
    
    def __init__(self, text, variant=ButtonVariant.YELLOW, parent=None):
        super().__init__(text, parent)
        
        # Map variants to theme colors
        self.color_map = {
            ButtonVariant.YELLOW: (Theme.ACCENT_YELLOW, Theme.TEXT_DARK),
            ButtonVariant.GREEN: (Theme.ACCENT_GREEN, Theme.TEXT_PRIMARY),
            ButtonVariant.BLUE: (Theme.ACCENT_BLUE, Theme.TEXT_PRIMARY),
            ButtonVariant.RED: (Theme.ACCENT_RED, Theme.TEXT_PRIMARY),
        }
        
        self.variant = variant
        self._opacity = 1.0  # For press animation
        
        # Apply styling
        self.apply_style()
        
        # Set minimum size from theme
        self.setMinimumSize(Theme.BUTTON_MIN_WIDTH, Theme.BUTTON_HEIGHT)
        
        # Enable hover events
        self.setMouseTracking(True)
    
    def apply_style(self):
        """Apply theme-based styling based on variant"""
        if self.variant == ButtonVariant.GRADIENT:
            # Special handling for gradient
            gradient = Theme.get_gradient()
            text_color = Theme.TEXT_PRIMARY
            
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {gradient};
                    color: {text_color};
                    border: none;
                    border-radius: {Theme.BUTTON_BORDER_RADIUS}px;
                    padding: {Theme.PADDING_MEDIUM}px {Theme.PADDING_LARGE}px;
                    font-size: {Theme.BODY_LARGE}px;
                    font-weight: {Theme.WEIGHT_BOLD};
                    min-height: {Theme.BUTTON_HEIGHT}px;
                }}
                QPushButton:hover {{
                    opacity: 0.95;
                }}
            """)
        else:
            # Standard color variants
            bg_color, text_color = self.color_map.get(
                self.variant,
                self.color_map[ButtonVariant.YELLOW]
            )
            self.setStyleSheet(Theme.get_button_style(bg_color, text_color))
    
    def set_variant(self, variant):
        """
        Change button color variant.
        
        Args:
            variant (str): New variant from ButtonVariant class
        """
        self.variant = variant
        self.apply_style()
    
    def mousePressEvent(self, event):
        """Override to add visual feedback on press"""
        # Slightly scale down on press
        self.setStyleSheet(self.styleSheet() + "opacity: 0.9;")
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Override to restore normal state"""
        self.apply_style()
        super().mouseReleaseEvent(event)
```

**Key Features**:
- 5 color variants (yellow, green, blue, red, gradient)
- Theme Manager integration (no hardcoded values)
- Touch-friendly sizing (80px height)
- Visual feedback on press
- Easy to change variant dynamically

**Testing**:
- [ ] All 5 variants display correct colors
- [ ] Button meets minimum size (300px × 80px)
- [ ] Press feedback visible
- [ ] Variant changes work (`set_variant()`)
- [ ] Text legible on all variants

---

#### Subtask 2.2: Create PillButton Test Script (15 min)
**File**: `examples/test_pill_button.py`

**Purpose**: Visual test for all button variants.

**Implementation**:
```python
"""Test PillButton component with all variants"""
import sys
sys.path.insert(0, '/path/to/deadstream')

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from src.ui.components.pill_button import PillButton, ButtonVariant
from src.ui.styles.theme import Theme

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("PillButton Test")
    window.resize(600, 600)
    window.setStyleSheet(Theme.get_global_stylesheet())
    
    layout = QVBoxLayout()
    layout.setSpacing(Theme.SPACING_LARGE)
    layout.setContentsMargins(Theme.MARGIN_LARGE, Theme.MARGIN_LARGE, 
                               Theme.MARGIN_LARGE, Theme.MARGIN_LARGE)
    
    # Title
    title = QLabel("PillButton Variants")
    title.setStyleSheet(f"font-size: {Theme.HEADER_MEDIUM}px; font-weight: bold;")
    layout.addWidget(title)
    
    # Test all variants
    variants = [
        (ButtonVariant.YELLOW, "Primary (Yellow)"),
        (ButtonVariant.GREEN, "Selected (Green)"),
        (ButtonVariant.BLUE, "Secondary (Blue)"),
        (ButtonVariant.RED, "Destructive (Red)"),
        (ButtonVariant.GRADIENT, "Gradient (Purple-Blue)"),
    ]
    
    for variant, label_text in variants:
        # Label
        label = QLabel(label_text)
        label.setStyleSheet(f"font-size: {Theme.BODY_MEDIUM}px;")
        layout.addWidget(label)
        
        # Button
        button = PillButton(f"Test {label_text}", variant=variant)
        button.clicked.connect(lambda checked, v=variant: on_button_click(v))
        layout.addWidget(button)
    
    layout.addStretch()
    window.setLayout(layout)
    window.show()
    
    print("\n[INFO] PillButton Test Window Opened")
    print("[INFO] Click buttons to test interaction")
    print("[INFO] Verify all colors match design mockups\n")
    
    sys.exit(app.exec_())

def on_button_click(variant):
    print(f"[CLICK] Button variant '{variant}' clicked")

if __name__ == '__main__':
    main()
```

**Testing**:
- [ ] All 5 button variants display
- [ ] Click detection works
- [ ] Colors match mockup colors
- [ ] Buttons are touch-friendly size
- [ ] Press animation visible

---

### Task 3: IconButton Component (45 min)

#### Subtask 3.1: Create IconButton Class (30 min)
**File**: `src/ui/components/icon_button.py`

**Purpose**: Circular icon button for navigation (home, settings, search).

**Implementation**:
```python
"""
IconButton - Circular button with icon for navigation.

Usage:
    from src.ui.components.icon_button import IconButton
    
    home_btn = IconButton(icon='home')
    home_btn.clicked.connect(on_home_clicked)
"""

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from src.ui.styles.theme import Theme
import os

# Fallback Unicode icons if assets not available
FALLBACK_ICONS = {
    'home': '⌂',
    'settings': '⚙',
    'search': '🔍',
}

class IconButton(QPushButton):
    """
    Circular icon button for navigation.
    
    Features:
    - 60px × 60px circular button
    - Semi-transparent background
    - SVG icon support with fallback
    - Theme Manager integration
    
    Args:
        icon (str): Icon name ('home', 'settings', 'search')
        parent (QWidget): Parent widget
    """
    
    def __init__(self, icon='home', parent=None):
        super().__init__(parent)
        
        self.icon_name = icon
        self.icon_path = f"src/ui/assets/icons/{icon}.svg"
        
        # Set up icon
        self._setup_icon()
        
        # Apply styling
        self.setFixedSize(Theme.ICON_BUTTON_SIZE, Theme.ICON_BUTTON_SIZE)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 0, 0, 0.5);
                border: none;
                border-radius: {Theme.ICON_BUTTON_SIZE // 2}px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 0, 0, 0.7);
            }}
            QPushButton:pressed {{
                background-color: rgba(0, 0, 0, 0.9);
            }}
        """)
    
    def _setup_icon(self):
        """Set up icon from SVG or use fallback"""
        if os.path.exists(self.icon_path):
            # Use SVG icon
            icon = QIcon(self.icon_path)
            self.setIcon(icon)
            self.setIconSize(QSize(Theme.ICON_SIZE, Theme.ICON_SIZE))
        else:
            # Use fallback Unicode
            fallback = FALLBACK_ICONS.get(self.icon_name, '?')
            self.setText(fallback)
            self.setStyleSheet(self.styleSheet() + f"""
                QPushButton {{
                    font-size: {Theme.HEADER_SMALL}px;
                    color: {Theme.TEXT_PRIMARY};
                }}
            """)
```

**Key Features**:
- Circular 60px × 60px button
- SVG icon support with Unicode fallback
- Semi-transparent background
- Hover/press states
- Theme Manager integration

**Testing**:
- [ ] Button is circular (60px × 60px)
- [ ] Uses SVG icon if available
- [ ] Falls back to Unicode if no SVG
- [ ] Hover state visible
- [ ] Press state visible

---

#### Subtask 3.2: Create IconButton Test Script (15 min)
**File**: `examples/test_icon_button.py`

**Purpose**: Visual test for all icon button types.

**Implementation**:
```python
"""Test IconButton component with all icon types"""
import sys
sys.path.insert(0, '/path/to/deadstream')

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from src.ui.components.icon_button import IconButton
from src.ui.styles.theme import Theme

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("IconButton Test")
    window.resize(400, 300)
    window.setStyleSheet(Theme.get_global_stylesheet())
    
    main_layout = QVBoxLayout()
    main_layout.setSpacing(Theme.SPACING_LARGE)
    main_layout.setContentsMargins(Theme.MARGIN_LARGE, Theme.MARGIN_LARGE,
                                    Theme.MARGIN_LARGE, Theme.MARGIN_LARGE)
    
    # Title
    title = QLabel("IconButton Types")
    title.setStyleSheet(f"font-size: {Theme.HEADER_MEDIUM}px; font-weight: bold;")
    main_layout.addWidget(title)
    
    # Icon buttons in row
    button_layout = QHBoxLayout()
    button_layout.setSpacing(Theme.SPACING_LARGE)
    
    icons = ['home', 'settings', 'search']
    for icon_name in icons:
        # Container for label + button
        container = QVBoxLayout()
        
        # Label
        label = QLabel(icon_name.capitalize())
        label.setAlignment(Qt.AlignCenter)
        container.addWidget(label)
        
        # Button
        button = IconButton(icon=icon_name)
        button.clicked.connect(lambda checked, i=icon_name: on_icon_click(i))
        container.addWidget(button)
        
        button_layout.addLayout(container)
    
    main_layout.addLayout(button_layout)
    main_layout.addStretch()
    
    window.setLayout(main_layout)
    window.show()
    
    print("\n[INFO] IconButton Test Window Opened")
    print("[INFO] Note: Using fallback Unicode icons (SVG assets not yet created)")
    print("[INFO] Click buttons to test interaction\n")
    
    sys.exit(app.exec_())

def on_icon_click(icon_name):
    print(f"[CLICK] {icon_name.capitalize()} button clicked")

if __name__ == '__main__':
    main()
```

**Testing**:
- [ ] All 3 icon types display
- [ ] Click detection works
- [ ] Buttons are circular
- [ ] Hover effect visible
- [ ] Size matches spec (60px × 60px)

---

### Task 4: Badge Components (1 hour)

#### Subtask 4.1: Create RatingBadge Class (30 min)
**File**: `src/ui/components/rating_badge.py`

**Purpose**: Display star rating with cyan background.

**Implementation**:
```python
"""
RatingBadge - Display show rating with stars.

Usage:
    from src.ui.components.rating_badge import RatingBadge
    
    badge = RatingBadge(4.5)
"""

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from src.ui.styles.theme import Theme

class RatingBadge(QLabel):
    """
    Star rating badge with cyan background.
    
    Features:
    - Cyan background (#00BCD4)
    - Star symbols + rating number
    - 60px × 30px size
    - Theme Manager integration
    
    Args:
        rating (float): Rating value (0.0 to 5.0)
        parent (QWidget): Parent widget
    """
    
    def __init__(self, rating, parent=None):
        super().__init__(parent)
        
        self.rating = rating
        self.update_display()
        
        # Apply styling
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.BADGE_RATING};
                color: {Theme.TEXT_PRIMARY};
                border-radius: {Theme.BADGE_BORDER_RADIUS}px;
                padding: 5px 10px;
                font-size: {Theme.META_TEXT}px;
                font-weight: {Theme.WEIGHT_BOLD};
            }}
        """)
        
        self.setFixedSize(Theme.BADGE_WIDTH, Theme.BADGE_HEIGHT)
        self.setAlignment(Qt.AlignCenter)
    
    def update_display(self):
        """Update badge text with rating"""
        # Star symbols (5 stars)
        stars = "★★★★★"
        
        # Rating text
        rating_text = f"{self.rating:.1f}"
        
        self.setText(f"{stars} {rating_text}")
    
    def set_rating(self, rating):
        """
        Update rating value.
        
        Args:
            rating (float): New rating value
        """
        self.rating = rating
        self.update_display()
```

**Key Features**:
- Cyan background (Theme.BADGE_RATING)
- 5 star symbols + rating number
- 60px × 30px size
- Can update rating dynamically

**Testing**:
- [ ] Badge displays correctly
- [ ] Rating shows 1 decimal place
- [ ] Size matches spec (60px × 30px)
- [ ] Cyan background color correct
- [ ] `set_rating()` updates display

---

#### Subtask 4.2: Create SourceBadge Class (30 min)
**File**: `src/ui/components/source_badge.py`

**Purpose**: Display recording source type (SBD, AUD, MTX).

**Implementation**:
```python
"""
SourceBadge - Display recording source type.

Usage:
    from src.ui.components.source_badge import SourceBadge
    
    badge = SourceBadge("SBD")
"""

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from src.ui.styles.theme import Theme

class SourceBadge(QLabel):
    """
    Recording source badge with yellow background.
    
    Features:
    - Yellow background (#FFD700)
    - Source type text (SBD, AUD, MTX)
    - 60px × 30px size
    - Theme Manager integration
    
    Args:
        source_type (str): Source type ("SBD", "AUD", "MTX", or "Unknown")
        parent (QWidget): Parent widget
    """
    
    def __init__(self, source_type="Unknown", parent=None):
        super().__init__(parent)
        
        self.source_type = source_type.upper()
        self.setText(self.source_type)
        
        # Apply styling
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.BADGE_SOURCE};
                color: {Theme.TEXT_DARK};
                border-radius: {Theme.BADGE_BORDER_RADIUS}px;
                padding: 5px 10px;
                font-size: {Theme.BODY_SMALL}px;
                font-weight: {Theme.WEIGHT_BOLD};
            }}
        """)
        
        self.setFixedSize(Theme.BADGE_WIDTH, Theme.BADGE_HEIGHT)
        self.setAlignment(Qt.AlignCenter)
    
    def set_source_type(self, source_type):
        """
        Update source type.
        
        Args:
            source_type (str): New source type
        """
        self.source_type = source_type.upper()
        self.setText(self.source_type)
```

**Key Features**:
- Yellow background (Theme.BADGE_SOURCE)
- Dark text on yellow
- 60px × 30px size
- Can update source type dynamically

**Testing**:
- [ ] Badge displays correctly
- [ ] Text is uppercase
- [ ] Size matches spec (60px × 30px)
- [ ] Yellow background color correct
- [ ] Dark text legible on yellow
- [ ] `set_source_type()` updates display

---

#### Subtask 4.3: Create Badge Test Script (remaining time)
**File**: `examples/test_badges.py`

**Purpose**: Visual test for both badge types.

**Implementation**:
```python
"""Test RatingBadge and SourceBadge components"""
import sys
sys.path.insert(0, '/path/to/deadstream')

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from src.ui.components.rating_badge import RatingBadge
from src.ui.components.source_badge import SourceBadge
from src.ui.styles.theme import Theme

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("Badge Components Test")
    window.resize(500, 400)
    window.setStyleSheet(Theme.get_global_stylesheet())
    
    layout = QVBoxLayout()
    layout.setSpacing(Theme.SPACING_LARGE)
    layout.setContentsMargins(Theme.MARGIN_LARGE, Theme.MARGIN_LARGE,
                               Theme.MARGIN_LARGE, Theme.MARGIN_LARGE)
    
    # Title
    title = QLabel("Badge Components")
    title.setStyleSheet(f"font-size: {Theme.HEADER_MEDIUM}px; font-weight: bold;")
    layout.addWidget(title)
    
    # Rating Badges Section
    rating_label = QLabel("Rating Badges:")
    rating_label.setStyleSheet(f"font-size: {Theme.BODY_LARGE}px; margin-top: 20px;")
    layout.addWidget(rating_label)
    
    rating_row = QHBoxLayout()
    rating_row.setSpacing(Theme.SPACING_MEDIUM)
    for rating in [3.5, 4.0, 4.5, 5.0]:
        badge = RatingBadge(rating)
        rating_row.addWidget(badge)
    rating_row.addStretch()
    layout.addLayout(rating_row)
    
    # Source Badges Section
    source_label = QLabel("Source Badges:")
    source_label.setStyleSheet(f"font-size: {Theme.BODY_LARGE}px; margin-top: 20px;")
    layout.addWidget(source_label)
    
    source_row = QHBoxLayout()
    source_row.setSpacing(Theme.SPACING_MEDIUM)
    for source in ["SBD", "AUD", "MTX", "Unknown"]:
        badge = SourceBadge(source)
        source_row.addWidget(badge)
    source_row.addStretch()
    layout.addLayout(source_row)
    
    layout.addStretch()
    window.setLayout(layout)
    window.show()
    
    print("\n[INFO] Badge Components Test Window Opened")
    print("[INFO] Verify colors match design mockups:")
    print("  - Rating badges: Cyan background (#00BCD4)")
    print("  - Source badges: Yellow background (#FFD700)")
    print("[INFO] Verify size: 60px × 30px\n")
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

**Testing**:
- [ ] All rating badges display (3.5, 4.0, 4.5, 5.0)
- [ ] All source badges display (SBD, AUD, MTX, Unknown)
- [ ] Rating badges are cyan
- [ ] Source badges are yellow
- [ ] All badges are 60px × 30px
- [ ] Text is legible on both badge types

---

### Task 5: ConcertListItem Component (1-1.5 hours)

#### Subtask 5.1: Create ConcertListItem Class (1 hour)
**File**: `src/ui/components/concert_list_item.py`

**Purpose**: Reusable list item for displaying show information in browse screens.

**Implementation**:
```python
"""
ConcertListItem - List item for displaying show details.

Usage:
    from src.ui.components.concert_list_item import ConcertListItem
    
    item = ConcertListItem(
        date="1977-05-08",
        venue="Barton Hall, Cornell University",
        location="Ithaca, NY",
        rating=4.8
    )
    item.clicked.connect(on_show_clicked)
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from src.ui.components.rating_badge import RatingBadge
from src.ui.styles.theme import Theme

class ConcertListItem(QWidget):
    """
    List item widget for displaying concert information.
    
    Features:
    - Date, venue, location display
    - Rating badge (right-aligned)
    - Click detection
    - Theme Manager integration
    - Hover state
    
    Signals:
        clicked: Emitted when item is clicked
    
    Args:
        date (str): Show date (display format, e.g., "1977-05-08")
        venue (str): Venue name
        location (str): City, state
        rating (float): Show rating (0.0 to 5.0)
        show_data (dict): Complete show data (passed with clicked signal)
        parent (QWidget): Parent widget
    """
    
    clicked = pyqtSignal(dict)  # Emits show_data
    
    def __init__(self, date, venue, location, rating, show_data=None, parent=None):
        super().__init__(parent)
        
        self.show_data = show_data or {}
        
        # Apply styling
        self.setStyleSheet(f"""
            ConcertListItem {{
                background-color: {Theme.BG_CARD};
                border-bottom: 1px solid {Theme.BORDER_SUBTLE};
                padding: {Theme.LIST_ITEM_PADDING_V}px {Theme.LIST_ITEM_PADDING_H}px;
            }}
            ConcertListItem:hover {{
                background-color: #2A3A4A;
            }}
        """)
        
        self.setMinimumHeight(Theme.LIST_ITEM_HEIGHT)
        self.setCursor(Qt.PointingHandCursor)
        
        # Main layout (horizontal)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(
            Theme.PADDING_MEDIUM,
            Theme.PADDING_MEDIUM,
            Theme.PADDING_MEDIUM,
            Theme.PADDING_MEDIUM
        )
        
        # Left side: Date, venue, location
        left_layout = QVBoxLayout()
        left_layout.setSpacing(5)
        
        # Date label
        date_label = QLabel(date)
        date_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
            }}
        """)
        left_layout.addWidget(date_label)
        
        # Venue label
        venue_label = QLabel(venue)
        venue_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
            }}
        """)
        left_layout.addWidget(venue_label)
        
        # Location label
        location_label = QLabel(location)
        location_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
            }}
        """)
        left_layout.addWidget(location_label)
        
        main_layout.addLayout(left_layout)
        main_layout.addStretch()
        
        # Right side: Rating badge
        if rating and rating > 0:
            rating_badge = RatingBadge(rating)
            main_layout.addWidget(rating_badge)
    
    def mousePressEvent(self, event):
        """Emit clicked signal when item is clicked"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.show_data)
        super().mousePressEvent(event)
```

**Key Features**:
- 3-line layout (date, venue, location)
- Rating badge on right side
- Hover state (slightly lighter background)
- Click detection
- 80px minimum height
- Theme Manager integration

**Testing**:
- [ ] All labels display correctly
- [ ] Rating badge on right side
- [ ] Item height at least 80px
- [ ] Hover state visible
- [ ] Click emits signal with show data
- [ ] Colors match mockup

---

#### Subtask 5.2: Create ConcertListItem Test Script (30 min)
**File**: `examples/test_concert_list_item.py`

**Purpose**: Visual test with multiple show items.

**Implementation**:
```python
"""Test ConcertListItem component with sample data"""
import sys
sys.path.insert(0, '/path/to/deadstream')

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea
from src.ui.components.concert_list_item import ConcertListItem
from src.ui.styles.theme import Theme

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("ConcertListItem Test")
    window.resize(800, 600)
    window.setStyleSheet(Theme.get_global_stylesheet())
    
    # Scrollable area
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet(Theme.get_scrollbar_style())
    
    # Container for list items
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setSpacing(0)  # Items have borders, no extra spacing needed
    layout.setContentsMargins(0, 0, 0, 0)
    
    # Sample show data
    shows = [
        {
            'date': '1977-05-08',
            'venue': 'Barton Hall, Cornell University',
            'location': 'Ithaca, NY',
            'rating': 4.8
        },
        {
            'date': '1972-05-26',
            'venue': 'Lyceum Theatre',
            'location': 'London, England',
            'rating': 4.7
        },
        {
            'date': '1973-11-17',
            'venue': 'Pauley Pavilion, UCLA',
            'location': 'Los Angeles, CA',
            'rating': 4.6
        },
        {
            'date': '1974-06-18',
            'venue': 'Freedom Hall',
            'location': 'Louisville, KY',
            'rating': 4.5
        },
        {
            'date': '1977-05-09',
            'venue': 'Buffalo Memorial Auditorium',
            'location': 'Buffalo, NY',
            'rating': 4.4
        },
    ]
    
    # Create list items
    for show in shows:
        item = ConcertListItem(
            date=show['date'],
            venue=show['venue'],
            location=show['location'],
            rating=show['rating'],
            show_data=show
        )
        item.clicked.connect(lambda data: on_item_clicked(data))
        layout.addWidget(item)
    
    layout.addStretch()
    
    scroll.setWidget(container)
    
    # Main window layout
    main_layout = QVBoxLayout(window)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.addWidget(scroll)
    
    window.show()
    
    print("\n[INFO] ConcertListItem Test Window Opened")
    print("[INFO] Click items to test interaction")
    print("[INFO] Verify hover effects and rating badges\n")
    
    sys.exit(app.exec_())

def on_item_clicked(show_data):
    date = show_data.get('date', 'Unknown')
    venue = show_data.get('venue', 'Unknown')
    print(f"[CLICK] Show clicked: {date} - {venue}")

if __name__ == '__main__':
    main()
```

**Testing**:
- [ ] All 5 show items display
- [ ] Scrolling works smoothly
- [ ] Hover effect on all items
- [ ] Click detection works
- [ ] Rating badges display correctly
- [ ] Layout doesn't break with long venue names

---

### Task 6: Component Integration Test (30 min)

#### Subtask 6.1: Create Integration Test Script
**File**: `test_ui_components.py` (project root)

**Purpose**: Comprehensive test of all components together.

**Implementation**:
```python
"""
Integration test for all Phase 10A UI components.

Tests:
- Theme Manager
- PillButton (all variants)
- IconButton (all types)
- RatingBadge
- SourceBadge
- ConcertListItem

Run with: python3 test_ui_components.py
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QScrollArea, QTabWidget)
from PyQt5.QtCore import Qt

# Import all components
from src.ui.styles.theme import Theme
from src.ui.components.pill_button import PillButton, ButtonVariant
from src.ui.components.icon_button import IconButton
from src.ui.components.rating_badge import RatingBadge
from src.ui.components.source_badge import SourceBadge
from src.ui.components.concert_list_item import ConcertListItem

class ComponentTestWindow(QWidget):
    """Test window showing all components"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phase 10A Component Integration Test")
        self.resize(900, 700)
        self.setStyleSheet(Theme.get_global_stylesheet())
        
        # Create tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {Theme.BORDER_SUBTLE};
                background-color: {Theme.BG_PRIMARY};
            }}
            QTabBar::tab {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                padding: 10px 20px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {Theme.ACCENT_GREEN};
            }}
        """)
        
        # Add tabs
        tabs.addTab(self.create_buttons_tab(), "Buttons")
        tabs.addTab(self.create_badges_tab(), "Badges")
        tabs.addTab(self.create_list_items_tab(), "List Items")
        tabs.addTab(self.create_theme_info_tab(), "Theme Info")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(tabs)
    
    def create_buttons_tab(self):
        """Tab showing all button types"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(Theme.SPACING_LARGE)
        layout.setContentsMargins(Theme.MARGIN_LARGE, Theme.MARGIN_LARGE,
                                   Theme.MARGIN_LARGE, Theme.MARGIN_LARGE)
        
        # PillButtons
        pill_label = QLabel("PillButton Variants:")
        pill_label.setStyleSheet(f"font-size: {Theme.HEADER_SMALL}px; font-weight: bold;")
        layout.addWidget(pill_label)
        
        for variant in [ButtonVariant.YELLOW, ButtonVariant.GREEN, 
                       ButtonVariant.BLUE, ButtonVariant.RED, ButtonVariant.GRADIENT]:
            btn = PillButton(f"{variant.capitalize()} Button", variant=variant)
            btn.clicked.connect(lambda checked, v=variant: print(f"[CLICK] {v} button"))
            layout.addWidget(btn)
        
        layout.addSpacing(Theme.SPACING_XL)
        
        # IconButtons
        icon_label = QLabel("IconButton Types:")
        icon_label.setStyleSheet(f"font-size: {Theme.HEADER_SMALL}px; font-weight: bold;")
        layout.addWidget(icon_label)
        
        icon_row = QHBoxLayout()
        icon_row.setSpacing(Theme.SPACING_LARGE)
        for icon in ['home', 'settings', 'search']:
            btn = IconButton(icon=icon)
            btn.clicked.connect(lambda checked, i=icon: print(f"[CLICK] {i} icon"))
            icon_row.addWidget(btn)
        icon_row.addStretch()
        layout.addLayout(icon_row)
        
        layout.addStretch()
        return widget
    
    def create_badges_tab(self):
        """Tab showing all badge types"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(Theme.SPACING_LARGE)
        layout.setContentsMargins(Theme.MARGIN_LARGE, Theme.MARGIN_LARGE,
                                   Theme.MARGIN_LARGE, Theme.MARGIN_LARGE)
        
        # Rating badges
        rating_label = QLabel("Rating Badges:")
        rating_label.setStyleSheet(f"font-size: {Theme.HEADER_SMALL}px; font-weight: bold;")
        layout.addWidget(rating_label)
        
        rating_row = QHBoxLayout()
        rating_row.setSpacing(Theme.SPACING_MEDIUM)
        for rating in [3.5, 4.0, 4.5, 4.8, 5.0]:
            badge = RatingBadge(rating)
            rating_row.addWidget(badge)
        rating_row.addStretch()
        layout.addLayout(rating_row)
        
        layout.addSpacing(Theme.SPACING_XL)
        
        # Source badges
        source_label = QLabel("Source Badges:")
        source_label.setStyleSheet(f"font-size: {Theme.HEADER_SMALL}px; font-weight: bold;")
        layout.addWidget(source_label)
        
        source_row = QHBoxLayout()
        source_row.setSpacing(Theme.SPACING_MEDIUM)
        for source in ["SBD", "AUD", "MTX", "Matrix", "Unknown"]:
            badge = SourceBadge(source)
            source_row.addWidget(badge)
        source_row.addStretch()
        layout.addLayout(source_row)
        
        layout.addStretch()
        return widget
    
    def create_list_items_tab(self):
        """Tab showing list items"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(Theme.get_scrollbar_style())
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Sample shows
        shows = [
            ('1977-05-08', 'Barton Hall, Cornell University', 'Ithaca, NY', 4.8),
            ('1972-05-26', 'Lyceum Theatre', 'London, England', 4.7),
            ('1973-11-17', 'Pauley Pavilion, UCLA', 'Los Angeles, CA', 4.6),
            ('1974-06-18', 'Freedom Hall', 'Louisville, KY', 4.5),
            ('1977-05-09', 'Buffalo Memorial Auditorium', 'Buffalo, NY', 4.4),
        ]
        
        for date, venue, location, rating in shows:
            item = ConcertListItem(date, venue, location, rating)
            item.clicked.connect(lambda data: print(f"[CLICK] Show: {data}"))
            layout.addWidget(item)
        
        layout.addStretch()
        scroll.setWidget(container)
        return scroll
    
    def create_theme_info_tab(self):
        """Tab showing theme constants"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(Theme.SPACING_SMALL)
        layout.setContentsMargins(Theme.MARGIN_LARGE, Theme.MARGIN_LARGE,
                                   Theme.MARGIN_LARGE, Theme.MARGIN_LARGE)
        
        title = QLabel("Theme Constants")
        title.setStyleSheet(f"font-size: {Theme.HEADER_SMALL}px; font-weight: bold;")
        layout.addWidget(title)
        
        # Show key theme values
        info_text = f"""
Colors:
  - Primary BG: {Theme.BG_PRIMARY}
  - Accent Yellow: {Theme.ACCENT_YELLOW}
  - Accent Green: {Theme.ACCENT_GREEN}
  - Accent Blue: {Theme.ACCENT_BLUE}
  - Accent Red: {Theme.ACCENT_RED}

Typography:
  - Header Large: {Theme.HEADER_LARGE}px
  - Body Large: {Theme.BODY_LARGE}px
  - Body Medium: {Theme.BODY_MEDIUM}px

Sizes:
  - Button Height: {Theme.BUTTON_HEIGHT}px
  - Icon Button: {Theme.ICON_BUTTON_SIZE}px
  - Badge: {Theme.BADGE_WIDTH}×{Theme.BADGE_HEIGHT}px
  - List Item: {Theme.LIST_ITEM_HEIGHT}px

Spacing:
  - Small: {Theme.SPACING_SMALL}px
  - Medium: {Theme.SPACING_MEDIUM}px
  - Large: {Theme.SPACING_LARGE}px
        """
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet(f"font-size: {Theme.BODY_MEDIUM}px; font-family: monospace;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        return widget

def main():
    app = QApplication(sys.argv)
    
    window = ComponentTestWindow()
    window.show()
    
    print("\n" + "="*60)
    print("PHASE 10A COMPONENT INTEGRATION TEST")
    print("="*60)
    print("\n[INFO] Test window opened with all components")
    print("[INFO] Navigate through tabs to test each component type")
    print("[INFO] Click components to verify interaction")
    print("[INFO] Verify all colors match design mockups")
    print("\n[SUCCESS] If all components render correctly, Phase 10A is complete!")
    print("="*60 + "\n")
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
```

**Testing Checklist**:
- [ ] All tabs load without errors
- [ ] All button variants display correctly
- [ ] All icon buttons display correctly
- [ ] All badges display correctly
- [ ] All list items display correctly
- [ ] Theme info tab shows correct values
- [ ] Click interactions work on all components
- [ ] Colors match design mockups
- [ ] Sizes match specifications (60px touch targets, etc.)

---

## Git Workflow

### Branch Strategy
```bash
# Create main phase branch
git checkout main
git checkout -b feature/ui-components

# All work happens on this branch
# Use incremental commits for each task
```

### Commit Message Format
Follow project standard from `07-project-guidelines.md`:

```
[Phase-10A] Task X.X: Brief description

Detailed description of changes.

- What was added/changed
- Why the change was needed
- Any important notes

Estimated X hours, actual Y hours.
```

### Example Commits

```bash
# Task 1: Theme Manager
git add src/ui/styles/theme.py examples/test_theme.py
git commit -m "[Phase-10A] Task 10A.1: Add Theme Manager with all styling constants

Created centralized Theme Manager class with:
- All color constants (backgrounds, accents, text, borders)
- All typography constants (sizes, weights, family)
- All spacing constants (padding, margins, gaps)
- All component size constants (buttons, icons, badges)
- Helper methods for generating stylesheets
- Color manipulation utilities
- Quick test script for visual experimentation

This enables instant app-wide styling changes by editing a single file.

Estimated 2 hours, actual 1.5 hours."

# Task 2: PillButton
git add src/ui/components/pill_button.py examples/test_pill_button.py
git commit -m "[Phase-10A] Task 10A.2: Add PillButton component with theme integration

Created PillButton class with:
- 5 color variants (yellow, green, blue, red, gradient)
- Theme Manager integration (no hardcoded values)
- Touch-friendly sizing (80px height minimum)
- Visual press feedback
- Dynamic variant changing

Includes test script showing all variants.

Estimated 1 hour, actual 0.75 hours."

# Task 3: IconButton
git add src/ui/components/icon_button.py examples/test_icon_button.py
git commit -m "[Phase-10A] Task 10A.3: Add IconButton component for navigation

Created IconButton class with:
- Circular 60px button for home/settings/search
- SVG icon support with Unicode fallback
- Semi-transparent background with hover states
- Theme Manager integration

Includes test script showing all icon types.

Estimated 45 min, actual 40 min."

# Task 4: Badges
git add src/ui/components/*badge.py examples/test_badges.py
git commit -m "[Phase-10A] Task 10A.4: Add RatingBadge and SourceBadge components

Created two badge components:

RatingBadge:
- Cyan background for star ratings
- 5 stars + rating number display
- 60px × 30px size

SourceBadge:
- Yellow background for recording type
- SBD/AUD/MTX display
- 60px × 30px size

Both use Theme Manager for consistent styling.

Estimated 1 hour, actual 1 hour."

# Task 5: ConcertListItem
git add src/ui/components/concert_list_item.py examples/test_concert_list_item.py
git commit -m "[Phase-10A] Task 10A.5: Add ConcertListItem component for browse screens

Created ConcertListItem widget with:
- 3-line layout (date, venue, location)
- Rating badge on right side
- Hover state for touch feedback
- Click signal with show data
- Theme Manager integration
- 80px minimum height

Includes test script with sample show data.

Estimated 1.5 hours, actual 1.25 hours."

# Task 6: Integration Test
git add test_ui_components.py
git commit -m "[Phase-10A] Task 10A.6: Add component integration test suite

Created comprehensive test showing:
- All button types in one tab
- All badge types in one tab
- List items in scrollable tab
- Theme constants info tab

Serves as visual verification that Phase 10A is complete.

Estimated 30 min, actual 35 min."
```

### Merging to Main

```bash
# After all tests pass
git checkout main
git merge feature/ui-components

# Tag the release
git tag -a phase-10a-complete -m "Phase 10A: Core Component Library Complete"

# Push to remote
git push origin main --tags
```

---

## Testing Checklist

### Theme Manager
- [ ] `theme.py` file imports without errors
- [ ] All color constants accessible (`Theme.ACCENT_YELLOW`, etc.)
- [ ] All typography constants accessible (`Theme.BODY_LARGE`, etc.)
- [ ] All spacing constants accessible (`Theme.SPACING_MEDIUM`, etc.)
- [ ] `get_button_style()` returns valid stylesheet
- [ ] `get_list_style()` returns valid stylesheet
- [ ] `get_global_stylesheet()` returns valid stylesheet
- [ ] `get_gradient()` returns valid gradient string
- [ ] `_lighten_color()` correctly lightens colors
- [ ] Test script runs and displays all theme values

### PillButton Component
- [ ] All 5 variants render with correct colors
- [ ] Button text is legible on all variants
- [ ] Button height meets minimum (80px)
- [ ] Button width meets minimum (300px)
- [ ] Press animation visible
- [ ] `set_variant()` changes color correctly
- [ ] Click signal fires properly
- [ ] Test script shows all variants

### IconButton Component
- [ ] All 3 icons render (home, settings, search)
- [ ] Buttons are circular (60px × 60px)
- [ ] Uses SVG if available, Unicode fallback works
- [ ] Semi-transparent background visible
- [ ] Hover state darkens background
- [ ] Press state darkens further
- [ ] Click signal fires properly
- [ ] Test script shows all icon types

### Badge Components
- [ ] RatingBadge displays with cyan background
- [ ] Rating shows 1 decimal place (e.g., "4.5")
- [ ] RatingBadge is 60px × 30px
- [ ] SourceBadge displays with yellow background
- [ ] Source text is uppercase
- [ ] SourceBadge is 60px × 30px
- [ ] Text legible on both badge types
- [ ] `set_rating()` and `set_source_type()` work
- [ ] Test script shows various ratings and sources

### ConcertListItem Component
- [ ] Date displays in bold white
- [ ] Venue displays in bold white
- [ ] Location displays in gray
- [ ] Rating badge appears on right side
- [ ] Item height at least 80px
- [ ] Hover state changes background color
- [ ] Click emits signal with show data
- [ ] Cursor changes to pointer on hover
- [ ] Border between items visible
- [ ] Test script shows scrollable list

### Integration Test
- [ ] Test window opens without errors
- [ ] All 4 tabs load correctly
- [ ] Buttons tab shows all button types
- [ ] Badges tab shows all badge types
- [ ] List Items tab shows scrollable list
- [ ] Theme Info tab shows theme constants
- [ ] No console errors during interaction
- [ ] All colors match design mockups
- [ ] All sizes match specifications

---

## Success Criteria

Phase 10A is complete when:

### Code Quality
- [ ] All components follow PEP 8 standards
- [ ] All code uses ASCII-only (no Unicode characters)
- [ ] All imports follow patterns from `08-import-and-architecture-reference.md`
- [ ] All components have comprehensive docstrings
- [ ] No hardcoded colors, sizes, or spacing (all use Theme)
- [ ] Zero technical debt

### Functionality
- [ ] Theme Manager centralizes all styling constants
- [ ] All components use Theme Manager (no hardcoded values)
- [ ] All components emit proper signals
- [ ] All touch targets meet 60px minimum
- [ ] All components responsive at target resolution

### Testing
- [ ] All individual test scripts run successfully
- [ ] Integration test passes with all components
- [ ] Manual testing on macOS complete
- [ ] All checklist items marked complete

### Documentation
- [ ] All code has inline comments per project standards
- [ ] All commit messages follow format
- [ ] This plan updated with actual times
- [ ] Ready to begin Phase 10B

---

## Time Tracking

| Task | Description | Estimated | Actual | Notes |
|------|-------------|-----------|--------|-------|
| 10A.1 | Theme Manager + Test | 1.5-2h | | |
| 10A.2 | PillButton + Test | 1h | | |
| 10A.3 | IconButton + Test | 45min | | |
| 10A.4 | Badge Components + Test | 1h | | |
| 10A.5 | ConcertListItem + Test | 1-1.5h | | |
| 10A.6 | Integration Test | 30min | | |
| **TOTAL** | | **4-6h** | | |

---

## Next Steps After Phase 10A

1. **Update Project Documentation**
   - Mark Phase 10A complete in project charter
   - Update `phase-10-completion-summary.md` with progress

2. **Create Phase 10A Completion Summary**
   - Document actual time vs estimated
   - Note any challenges or lessons learned
   - List all files created

3. **Begin Phase 10B: Welcome Screen Restyle**
   - Use components created in 10A
   - Apply Theme Manager for all styling
   - Follow implementation plan

4. **Continuous Theme Experimentation**
   - Try different color schemes using Theme Manager
   - Adjust sizing if needed after Pi testing
   - Document any theme changes made

---

## Notes & Observations

### Design Decisions

**Why Theme Manager First?**
- Makes all subsequent phases faster
- Enables risk-free experimentation
- Easier to polish later
- Industry best practice

**Why These Components?**
- Used by all screens (maximum reuse)
- Foundation for entire UI redesign
- Touch-friendly from the start
- Consistent with mockup designs

### Benefits of This Approach

**Flexibility**:
- Change entire app color scheme in 30 seconds
- Adjust all font sizes instantly
- Experiment without fear of breaking things

**Maintainability**:
- One place to update styling
- No hunting for hardcoded values
- Self-documenting through constants

**Quality**:
- Professional, consistent look
- Touch-friendly by default
- Follows industry standards

---

**Created**: January 6, 2026  
**Revised**: January 6, 2026  
**Status**: Ready to Begin  
**Estimated Completion**: 4-6 hours from start  
**Foundation For**: Phases 10B-10H (all screen restyling)
