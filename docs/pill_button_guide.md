# PillButton Component - Usage Guide

**Created:** January 7, 2026  
**Phase:** 10A Task 1.2  
**Status:** Complete

## Overview

The `PillButton` is a touch-friendly, rounded button component with configurable color variants. It's the primary button style for all DeadStream screens.

## Features

- **Touch-Friendly:** 60px minimum height for easy tapping
- **5 Color Variants:** Yellow, Green, Blue, Red, Gradient
- **Automatic Styling:** Hover/pressed states built-in
- **Theme Integration:** All colors from Theme Manager
- **Flexible Sizing:** Adapts to text length, minimum 120px width

## Basic Usage

```python
from src.ui.components.pill_button import PillButton

# Create a yellow primary button
btn = PillButton("Find a Show", variant='yellow')
btn.clicked.connect(self.on_find_show)
layout.addWidget(btn)
```

## Color Variants

### Yellow (Primary CTA)
```python
btn = PillButton("Primary Action", variant='yellow')
```
- **Use for:** Main call-to-action buttons
- **Colors:** Gold background (#FFD700), dark text
- **Example:** "Find a Show", "Start Listening"

### Green (Selected/Active)
```python
btn = PillButton("Selected", variant='green')
```
- **Use for:** Selected states, confirmation actions
- **Colors:** Green background (#0F9D58), white text
- **Example:** "Playing Now", "Active Filter"

### Blue (Secondary Action)
```python
btn = PillButton("Secondary Action", variant='blue')
```
- **Use for:** Secondary actions, navigation
- **Colors:** Blue background (#1976D2), white text
- **Example:** "Browse", "Settings"

### Red (Destructive/Exciting)
```python
btn = PillButton("Skip Show", variant='red')
```
- **Use for:** Destructive actions, exciting features
- **Colors:** Red background (#FF0000), white text
- **Example:** "Skip", "Random Show"

### Gradient (Special Effect)
```python
btn = PillButton("Special Feature", variant='gradient')
```
- **Use for:** Special features, premium actions
- **Colors:** Purple to blue gradient, white text
- **Example:** "Surprise Me", "Featured Concert"

## Dynamic Variant Switching

Change button color on-the-fly:

```python
# Create button
btn = PillButton("Toggle Mode", variant='yellow')

# Change variant based on state
if selected:
    btn.set_variant('green')
else:
    btn.set_variant('yellow')
```

## Disabled State

```python
btn = PillButton("Not Available", variant='yellow')
btn.setEnabled(False)  # Grayed out, no interaction
```

## Layout Examples

### Vertical Stack
```python
layout = QVBoxLayout()
layout.setSpacing(Theme.BUTTON_SPACING)  # 16px between buttons

btn1 = PillButton("Option 1", variant='yellow')
btn2 = PillButton("Option 2", variant='blue')
btn3 = PillButton("Option 3", variant='green')

layout.addWidget(btn1)
layout.addWidget(btn2)
layout.addWidget(btn3)
```

### Horizontal Row
```python
layout = QHBoxLayout()
layout.setSpacing(Theme.BUTTON_SPACING)

back_btn = PillButton("Back", variant='blue')
next_btn = PillButton("Next", variant='yellow')

layout.addWidget(back_btn)
layout.addWidget(next_btn)
```

### Centered Single Button
```python
layout = QVBoxLayout()
layout.addStretch()

btn = PillButton("Get Started", variant='yellow')
btn.setFixedWidth(300)  # Optional: set specific width

layout.addWidget(btn, alignment=Qt.AlignCenter)
layout.addStretch()
```

## Integration with Existing Screens

### Welcome Screen
```python
from src.ui.components.pill_button import PillButton

# Replace existing buttons
find_show_btn = PillButton("Find a Show", variant='yellow')
find_show_btn.clicked.connect(self.on_browse)

random_show_btn = PillButton("Random Show", variant='red')
random_show_btn.clicked.connect(self.on_random_show)
```

### Browse Screen
```python
# Replace mode buttons with PillButton
top_rated_btn = PillButton("Top Rated", variant='green')
by_date_btn = PillButton("By Date", variant='blue')
by_venue_btn = PillButton("By Venue", variant='blue')
```

### Player Screen
```python
# Replace control buttons
play_btn = PillButton("Play", variant='green')
skip_btn = PillButton("Skip", variant='red')
```

## Testing

Run the visual test to see all variants:

```bash
# On Mac (if PyQt5 installed)
python3 examples/test_pill_button.py

# On Raspberry Pi
ssh pi@raspberrypi
cd ~/deadstream
python3 examples/test_pill_button.py
```

The test shows:
- All 5 color variants
- Normal vs disabled states
- Short vs long text handling
- Hover and pressed effects

## Component Architecture

```
PillButton (extends QPushButton)
    |
    +-- Uses Theme Manager for colors/sizing
    +-- Implements hover/pressed states
    +-- Enforces minimum touch target (60px height)
    +-- Supports dynamic variant switching
```

## Next Steps

Now that PillButton is complete, you can:

1. **Continue with Phase 10A** - Build remaining components:
   - IconButton (Task 1.3)
   - ConcertListItem (Task 1.4)
   - Additional components as needed

2. **Start Phase 10B** - Apply PillButton to Welcome Screen

3. **Test Integration** - Verify button works in actual screens

## Design Decisions

**Why 60px height?**
- Meets accessibility guidelines for touch targets
- Easy to tap on 7-inch screen
- Comfortable for both mouse and touch

**Why minimum 120px width?**
- Prevents tiny buttons with short text
- Maintains consistent button presence
- Looks balanced on screen

**Why rounded corners (30px)?**
- "Pill" shape is friendly and modern
- Distinguishes from flat Material Design
- Matches mockup aesthetic

## File Locations

```
deadstream/
├── src/ui/
│   ├── components/
│   │   ├── __init__.py
│   │   └── pill_button.py          [Component implementation]
│   └── styles/
│       └── theme.py                 [Theme constants used]
└── examples/
    └── test_pill_button.py          [Visual test demo]
```

---

**Phase 10A Task 1.2: Complete**  
Next: Task 1.3 - IconButton component
