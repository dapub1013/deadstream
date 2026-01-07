# IconButton Component - Usage Guide

**Created:** January 7, 2026  
**Phase:** 10A Task 1.3  
**Status:** Complete

## Overview

The `IconButton` is a circular, touch-friendly button component for navigation icons and actions. Used for home, settings, search, and other icon-based controls throughout DeadStream.

## Features

- **Touch-Friendly:** 60px × 60px circular target
- **12 Built-in Icons:** Home, settings, search, back, forward, close, menu, random, play, pause, skip, star
- **4 Style Variants:** Solid, transparent, outline, accent
- **Automatic Styling:** Hover/pressed states built-in
- **Theme Integration:** All colors from Theme Manager
- **Perfect Circle:** Border radius creates circular appearance

## Basic Usage

```python
from src.ui.components.icon_button import IconButton

# Create a home button with transparent background
home_btn = IconButton(icon_type='home', variant='transparent')
home_btn.clicked.connect(self.go_home)
layout.addWidget(home_btn)
```

## Available Icons

### Navigation Icons
```python
home_btn = IconButton('home')         # House icon
back_btn = IconButton('back')         # Left arrow
forward_btn = IconButton('forward')   # Right arrow
```

### Action Icons
```python
settings_btn = IconButton('settings') # Gear icon
search_btn = IconButton('search')     # Magnifying glass
close_btn = IconButton('close')       # X icon
menu_btn = IconButton('menu')         # Hamburger menu
```

### Media Controls
```python
play_btn = IconButton('play')         # Play triangle
pause_btn = IconButton('pause')       # Pause bars
skip_btn = IconButton('skip')         # Next track
```

### Special Icons
```python
random_btn = IconButton('random')     # Dice/shuffle
star_btn = IconButton('star')         # Star rating
```

## Style Variants

### Solid (Default)
```python
btn = IconButton('settings', variant='solid')
```
- **Background:** Opaque dark gray (BG_CARD)
- **Text:** White
- **Use for:** Standard navigation buttons
- **Example:** Settings button on browse screen

### Transparent
```python
btn = IconButton('home', variant='transparent')
```
- **Background:** Semi-transparent (60% opacity)
- **Text:** White
- **Use for:** Floating buttons over content
- **Example:** Home button overlaid on images

### Outline
```python
btn = IconButton('search', variant='outline')
```
- **Background:** Transparent with border
- **Border:** Subtle gray, becomes white on hover
- **Text:** White
- **Use for:** Secondary actions, minimal design
- **Example:** Optional search button

### Accent
```python
btn = IconButton('play', variant='accent')
```
- **Background:** Yellow accent color
- **Text:** Dark
- **Use for:** Primary action emphasis
- **Example:** Play button as main CTA

## Dynamic Updates

Change icon or variant on-the-fly:

```python
# Create button
btn = IconButton('play', variant='accent')

# Change to pause when playing
btn.set_icon('pause')

# Or change the variant
btn.set_variant('solid')

# Set custom icon character
btn.set_custom_icon('♫')  # Music note
```

## Layout Patterns

### Header Navigation (Corners)
```python
header_layout = QHBoxLayout()

# Left corner - home
home_btn = IconButton('home', variant='transparent')
header_layout.addWidget(home_btn)

# Stretch to push next button to right
header_layout.addStretch()

# Right corner - settings
settings_btn = IconButton('settings', variant='transparent')
header_layout.addWidget(settings_btn)
```

### Action Bar (Centered Controls)
```python
controls_layout = QHBoxLayout()
controls_layout.addStretch()

back_btn = IconButton('back', variant='solid')
controls_layout.addWidget(back_btn)

play_btn = IconButton('play', variant='accent')
controls_layout.addWidget(play_btn)

forward_btn = IconButton('forward', variant='solid')
controls_layout.addWidget(forward_btn)

controls_layout.addStretch()
```

### Vertical Icon Stack
```python
sidebar_layout = QVBoxLayout()

icons = ['home', 'search', 'settings']
for icon_type in icons:
    btn = IconButton(icon_type, variant='solid')
    btn.clicked.connect(lambda checked, i=icon_type: self.on_nav(i))
    sidebar_layout.addWidget(btn)

sidebar_layout.addStretch()
```

### Grid of Icons
```python
grid = QGridLayout()

icons = [
    ['home', 'search', 'settings'],
    ['back', 'play', 'forward'],
    ['menu', 'random', 'close']
]

for row, icon_row in enumerate(icons):
    for col, icon_type in enumerate(icon_row):
        btn = IconButton(icon_type, variant='solid')
        grid.addWidget(btn, row, col)
```

## Integration with Existing Screens

### Welcome Screen
```python
from src.ui.components.icon_button import IconButton

# Add settings button to top-right
settings_btn = IconButton('settings', variant='transparent')
settings_btn.clicked.connect(self.show_settings)
# Position in top-right corner of layout
```

### Browse Screen
```python
# Home button (top-left)
home_btn = IconButton('home', variant='transparent')
home_btn.clicked.connect(self.go_home)

# Settings button (top-right)
settings_btn = IconButton('settings', variant='transparent')
settings_btn.clicked.connect(self.show_settings)

# Search button (if adding search feature)
search_btn = IconButton('search', variant='solid')
search_btn.clicked.connect(self.show_search)
```

### Player Screen
```python
# Media controls
play_pause_btn = IconButton('play', variant='accent')
skip_btn = IconButton('skip', variant='solid')

# Toggle play/pause icon
def toggle_playback():
    if self.is_playing:
        play_pause_btn.set_icon('pause')
    else:
        play_pause_btn.set_icon('play')
```

## Custom Icons

If you need an icon not in the built-in set:

```python
# Unicode character
custom_btn = IconButton('home')  # Start with any type
custom_btn.set_custom_icon('♫')  # Music note
custom_btn.set_custom_icon('↻')  # Circular arrow
custom_btn.set_custom_icon('⚙')  # Alternative gear

# When SVG support is added (future)
# custom_btn.set_icon_from_svg('path/to/icon.svg')
```

## Testing

Run the visual test to see all icons and variants:

```bash
# On Raspberry Pi (recommended)
python3 examples/test_icon_button.py

# On Mac (if PyQt5 installed)
python3 examples/test_icon_button.py
```

The test shows:
- All 12 icon types
- All 4 style variants
- Common layout patterns
- Interactive hover/pressed feedback

## Component Architecture

```
IconButton (extends QPushButton)
    |
    +-- Uses Theme Manager for colors/sizing
    +-- Implements circular border radius
    +-- Maps icon types to Unicode characters
    +-- Supports 4 style variants
    +-- Fixed 60px × 60px size
```

## Design Decisions

**Why 60px × 60px?**
- Meets touch target guidelines
- Large enough for accurate tapping
- Maintains circular appearance
- Consistent with button height

**Why Unicode instead of SVG?**
- Works immediately without asset files
- Simple, reliable, cross-platform
- Easy to test and iterate
- Can be replaced with SVG later

**Why circular design?**
- Distinguishes from rectangular buttons
- Icon-focused (no room for text)
- Modern, clean aesthetic
- Common pattern in mobile UIs

**Why 4 variants?**
- Solid: Standard, most common
- Transparent: Overlay on content
- Outline: Minimal, secondary
- Accent: Emphasis, call-to-action

## Known Limitations

1. **Unicode rendering:** Some icons may look different across platforms
   - Solution: SVG support planned for future
   
2. **Icon size:** Fixed at 32px (ICON_MEDIUM)
   - Solution: Could add size parameter if needed
   
3. **Color customization:** Limited to predefined variants
   - Solution: Could add custom color parameter if needed

## Future Enhancements

- SVG icon support for custom graphics
- Size variants (small, medium, large)
- Badge overlay (notification count)
- Tooltip on hover
- Animation effects (rotate, pulse)

## File Locations

```
deadstream/
├── src/ui/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── pill_button.py           [Previous component]
│   │   └── icon_button.py           [This component]
│   └── styles/
│       └── theme.py                  [Theme constants used]
└── examples/
    ├── test_pill_button.py
    └── test_icon_button.py           [Visual test demo]
```

---

**Phase 10A Task 1.3: Complete**  
Next: Task 1.4 - Badge components (RatingBadge, SourceBadge)