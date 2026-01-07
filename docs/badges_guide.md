# Badge Components - Usage Guide

**Created:** January 7, 2026  
**Phase:** 10A Task 1.4  
**Status:** Complete

## Overview

Badge components provide compact, color-coded indicators for concert metadata. Two badge types are available:
- **RatingBadge:** Displays star ratings (⭐ 4.8)
- **SourceBadge:** Displays recording source type (SBD, AUD, MTX)

## Features

- **Compact Size:** 80px × 28px
- **Rounded Corners:** 14px radius
- **Color-Coded:** Different colors for different types
- **Bold Text:** Clear, readable at a glance
- **Theme Integration:** Uses Theme Manager colors

---

## RatingBadge

### Overview

Displays concert ratings with a star emoji and numerical value.

### Features

- **Cyan Background:** Distinctive rating color
- **Star Emoji:** ⭐ for visual recognition
- **Decimal Precision:** Shows one decimal place (4.8)
- **Range:** 0.0 to 5.0 stars

### Basic Usage

```python
from src.ui.components.rating_badge import RatingBadge

# Create badge
rating_badge = RatingBadge(4.8)
layout.addWidget(rating_badge)
```

### Dynamic Updates

```python
# Create badge
badge = RatingBadge(4.0)

# Update rating later
badge.update_rating(4.8)

# Get current rating
current_rating = badge.get_rating()  # Returns 4.8
```

### Visual Examples

```
⭐ 5.0  (Perfect rating)
⭐ 4.8  (Excellent)
⭐ 4.5  (Very good)
⭐ 4.0  (Good)
⭐ 3.5  (Average)
```

---

## SourceBadge

### Overview

Displays recording source type with color-coding for quick identification.

### Features

- **Color-Coded:** Different colors for different sources
- **Bold Text:** Uppercase abbreviations
- **5 Source Types:** SBD, AUD, MTX, FLAC, MP3

### Source Types and Colors

**SBD (Soundboard)**
- **Color:** Yellow/Gold background, dark text
- **Meaning:** Professional soundboard recording (highest quality)
- **Priority:** Preferred source type

**AUD (Audience)**
- **Color:** Blue background, white text
- **Meaning:** Audience recording from the crowd
- **Priority:** Standard quality

**MTX (Matrix)**
- **Color:** Green background, white text
- **Meaning:** Mixed blend of soundboard + audience
- **Priority:** Best of both worlds

**FLAC (Format)**
- **Color:** Purple background, white text
- **Meaning:** Lossless audio format indicator
- **Priority:** Format preference

**MP3 (Format)**
- **Color:** Orange background, dark text
- **Meaning:** Lossy audio format indicator
- **Priority:** Format alternative

### Basic Usage

```python
from src.ui.components.source_badge import SourceBadge

# Create badge
source_badge = SourceBadge('SBD')
layout.addWidget(source_badge)
```

### Dynamic Updates

```python
# Create badge
badge = SourceBadge('AUD')

# Change source type
badge.set_source('SBD')

# Get current source
current_source = badge.get_source()  # Returns 'SBD'
```

### Visual Examples

```
SBD  (Gold - premium soundboard)
AUD  (Blue - audience recording)
MTX  (Green - matrix blend)
FLAC (Purple - lossless format)
MP3  (Orange - lossy format)
```

---

## Combined Usage in Concert Lists

### Typical Pattern

Badges are most commonly used together in concert list items:

```python
from src.ui.components.rating_badge import RatingBadge
from src.ui.components.source_badge import SourceBadge

# Concert list item layout
item_layout = QHBoxLayout()

# Concert info (left)
info_layout = QVBoxLayout()
date_label = QLabel("1977-05-08")
venue_label = QLabel("Barton Hall, Cornell University")
info_layout.addWidget(date_label)
info_layout.addWidget(venue_label)
item_layout.addLayout(info_layout, stretch=1)

# Badges (right)
source_badge = SourceBadge('SBD')
item_layout.addWidget(source_badge)

rating_badge = RatingBadge(4.8)
item_layout.addWidget(rating_badge)
```

### Layout Result

```
┌─────────────────────────────────────────────────┐
│ 1977-05-08                    [SBD] [⭐ 4.8]   │
│ Barton Hall, Cornell University                │
└─────────────────────────────────────────────────┘
```

---

## Testing

Run the visual test to see all badge types:

```bash
# On Raspberry Pi (recommended)
python3 examples/test_badges.py

# On Mac (if PyQt5 installed)
python3 examples/test_badges.py
```

The test shows:
- All rating values (5.0 down to 3.0)
- All source types (SBD, AUD, MTX, FLAC, MP3)
- Combined badge displays
- Simulated concert list with badges

---

## Integration Examples

### Browse Screen - Concert List Item

```python
class ConcertListItem(QWidget):
    def __init__(self, show_data, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        
        # Show info
        info = QVBoxLayout()
        date = QLabel(show_data['date'])
        venue = QLabel(show_data['venue'])
        info.addWidget(date)
        info.addWidget(venue)
        layout.addLayout(info, stretch=1)
        
        # Badges
        if show_data.get('source'):
            source = SourceBadge(show_data['source'])
            layout.addWidget(source)
        
        if show_data.get('rating'):
            rating = RatingBadge(show_data['rating'])
            layout.addWidget(rating)
        
        self.setLayout(layout)
```

### Player Screen - Now Playing Info

```python
class NowPlayingInfo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout()
        
        # Show title
        title = QLabel("1977-05-08 - Barton Hall")
        layout.addWidget(title)
        
        # Badges row
        badges_layout = QHBoxLayout()
        
        self.source_badge = SourceBadge('SBD')
        badges_layout.addWidget(self.source_badge)
        
        self.rating_badge = RatingBadge(4.8)
        badges_layout.addWidget(self.rating_badge)
        
        badges_layout.addStretch()
        
        layout.addLayout(badges_layout)
        self.setLayout(layout)
```

### Random Show - Quality Indicator

```python
def show_random_show(self, show_data):
    """Display random show with quality indicators."""
    
    # Source badge shows recording quality
    source = show_data.get('source', 'AUD')
    self.source_badge.set_source(source)
    
    # Rating shows community feedback
    rating = show_data.get('rating', 0.0)
    self.rating_badge.update_rating(rating)
    
    # Color-coding helps users quickly assess quality
    # Gold SBD + high rating = premium show
    # Blue AUD + lower rating = standard show
```

---

## Design Decisions

### Why Two Separate Badge Components?

**Separation of concerns:**
- RatingBadge: User ratings (community feedback)
- SourceBadge: Technical metadata (recording quality)
- Different data sources, different update patterns

**Different styling needs:**
- Rating: Always cyan (consistent)
- Source: Color-coded by type (variable)

### Why 80px × 28px?

- **Compact:** Doesn't dominate list items
- **Readable:** Large enough for touch screens
- **Consistent:** Matches other UI element sizes
- **Stackable:** Can place side-by-side easily

### Why Color-Coding for Source?

- **Quick Recognition:** Gold = premium quality at a glance
- **Visual Hierarchy:** Yellow/gold draws attention to best recordings
- **Accessibility:** Color + text (not color-only)
- **Industry Standard:** Soundboard > Audience is universal

### Star Emoji vs Multiple Stars?

**Single star + number:**
- More compact (⭐ 4.8 vs ⭐⭐⭐⭐⭐)
- Precise (shows 4.8, not just 5)
- Cleaner design
- Less visual clutter

---

## Component Architecture

```
RatingBadge (extends QLabel)
    |
    +-- Uses Theme.BADGE_RATING color
    +-- Fixed 80px × 28px size
    +-- Displays: "⭐ X.X"
    +-- Method: update_rating(float)

SourceBadge (extends QLabel)
    |
    +-- Color maps for each source type
    +-- Fixed 80px × 28px size
    +-- Displays: "SBD", "AUD", etc.
    +-- Method: set_source(str)
```

---

## File Locations

```
deadstream/
├── src/ui/
│   ├── components/
│   │   ├── pill_button.py        [Task 1.2]
│   │   ├── icon_button.py        [Task 1.3]
│   │   ├── rating_badge.py       [NEW - Task 1.4]
│   │   └── source_badge.py       [NEW - Task 1.4]
│   └── styles/
│       └── theme.py               [Updated with BADGE_WIDTH]
└── examples/
    ├── test_pill_button.py
    ├── test_icon_button.py
    └── test_badges.py             [NEW - Task 1.4]
```

---

**Phase 10A Task 1.4: Complete**  
Next: Continue with more components or start applying to screens