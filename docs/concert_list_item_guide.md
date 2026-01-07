# ConcertListItem Component - Usage Guide

**Created:** January 7, 2026  
**Phase:** 10A Task 1.5  
**Status:** Complete

## Overview

The `ConcertListItem` is a complete list item widget for displaying concert information in browse screens. It combines date, venue, location, and badge components into a touch-friendly, interactive list item.

## Features

- **Complete Concert Display:** Date, venue, location all formatted
- **Badge Integration:** Shows rating and source badges
- **Touch-Friendly:** 80px minimum height
- **Interactive States:** Hover and press feedback
- **Click Signal:** Emits signal with full show data
- **Optional Divider:** Bottom border line
- **Responsive Layout:** Adapts to different content lengths

## Basic Usage

```python
from src.ui.components.concert_list_item import ConcertListItem

# Create list item
item = ConcertListItem({
    'date': '1977-05-08',
    'venue': 'Barton Hall, Cornell University',
    'location': 'Ithaca, NY',
    'rating': 4.8,
    'source': 'SBD'
})

# Connect to click handler
item.clicked.connect(self.on_show_selected)

# Add to layout
layout.addWidget(item)
```

## Show Data Dictionary

The component expects a dictionary with these keys:

### Required Keys

**date** (str)
- Concert date
- Format: 'YYYY-MM-DD' or any readable format
- Displayed in bold, large text
- Example: '1977-05-08'

**venue** (str)
- Venue name
- Can be multi-line (will wrap)
- Displayed in medium text
- Example: 'Barton Hall, Cornell University'

### Optional Keys

**location** (str)
- City, state, or country
- Displayed in small, gray text
- Example: 'Ithaca, NY'

**rating** (float)
- Concert rating 0.0 to 5.0
- Displays RatingBadge if present
- Example: 4.8

**source** (str)
- Recording source type
- Displays SourceBadge if present
- Values: 'SBD', 'AUD', 'MTX', 'FLAC', 'MP3'
- Example: 'SBD'

## Complete Example

```python
show_data = {
    'date': '1977-05-08',
    'venue': 'Barton Hall, Cornell University',
    'location': 'Ithaca, NY',
    'rating': 4.8,
    'source': 'SBD',
    # Additional data for your app
    'identifier': 'gd77-05-08.sbd.hicks.4982.sbeok.shnf',
    'year': 1977
}

item = ConcertListItem(show_data, show_divider=True)
item.clicked.connect(self.on_show_selected)
```

## Layout Structure

```
┌─────────────────────────────────────────────────┐
│ 1977-05-08                [SBD] [⭐ 4.8]       │  ← Top row: date + badges
│ Barton Hall, Cornell University                │  ← Venue (medium text)
│ Ithaca, NY                                      │  ← Location (small, gray)
├─────────────────────────────────────────────────┤  ← Optional divider
```

## Signal Handling

The `clicked` signal emits the complete show data dictionary:

```python
def on_show_selected(self, show_data):
    """Handle concert selection."""
    date = show_data['date']
    venue = show_data['venue']
    
    print(f"Selected: {date} - {venue}")
    
    # Load show in player
    self.player.load_show(show_data)
    
    # Switch to player screen
    self.show_player_screen()
```

## Creating a Concert List

### Simple Vertical List

```python
from PyQt5.QtWidgets import QVBoxLayout, QWidget

list_layout = QVBoxLayout()
list_layout.setSpacing(Theme.LIST_ITEM_SPACING)

concerts = get_concerts_from_database()

for concert in concerts:
    item = ConcertListItem(concert)
    item.clicked.connect(self.on_concert_selected)
    list_layout.addWidget(item)
```

### Scrollable List

```python
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

# Create scroll area
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)

# Container widget
container = QWidget()
layout = QVBoxLayout()
layout.setSpacing(Theme.LIST_ITEM_SPACING)

# Add concert items
for concert in concerts:
    item = ConcertListItem(concert)
    item.clicked.connect(self.on_concert_selected)
    layout.addWidget(item)

container.setLayout(layout)
scroll_area.setWidget(container)
```

### Dynamic List Updates

```python
# Update existing item
item.update_show_data({
    'date': '1977-05-08',
    'venue': 'Barton Hall',
    'location': 'Ithaca, NY',
    'rating': 4.9,  # Updated rating
    'source': 'SBD'
})

# Or clear and rebuild list
def refresh_list(self, new_concerts):
    """Refresh the concert list."""
    # Clear existing items
    while self.list_layout.count():
        item = self.list_layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
    
    # Add new items
    for concert in new_concerts:
        item = ConcertListItem(concert)
        item.clicked.connect(self.on_concert_selected)
        self.list_layout.addWidget(item)
```

## Interactive States

### Default State
- Background: BG_CARD color
- Normal appearance

### Hover State
- Background: Slightly lighter
- Cursor: Pointing hand
- Automatic on mouse enter

### Pressed State
- Background: Slightly darker
- Visual feedback while clicking
- Returns to hover on release

## Divider Options

Control the bottom divider line:

```python
# With divider (default)
item = ConcertListItem(show_data, show_divider=True)

# Without divider (for last item in list)
item = ConcertListItem(show_data, show_divider=False)

# Programmatic approach for lists
for idx, concert in enumerate(concerts):
    show_divider = (idx < len(concerts) - 1)
    item = ConcertListItem(concert, show_divider=show_divider)
```

## Integration with Browse Screen

```python
class BrowseScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.concert_items = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize browse screen."""
        # Create scrollable concert list
        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(Theme.LIST_ITEM_SPACING)
        
        # Populate with shows
        self.load_concerts()
    
    def load_concerts(self, filter_type='top_rated'):
        """Load concerts based on filter."""
        # Get shows from database
        if filter_type == 'top_rated':
            shows = get_top_rated_shows(limit=50)
        elif filter_type == 'by_date':
            shows = get_shows_by_date()
        
        # Clear existing
        self.clear_list()
        
        # Add new items
        for idx, show in enumerate(shows):
            show_divider = (idx < len(shows) - 1)
            item = ConcertListItem(show, show_divider=show_divider)
            item.clicked.connect(self.on_show_selected)
            self.list_layout.addWidget(item)
            self.concert_items.append(item)
    
    def on_show_selected(self, show_data):
        """Handle show selection."""
        # Load in player and switch screens
        self.parent().load_show(show_data)
        self.parent().show_player_screen()
```

## Testing

Run the visual test to see the component:

```bash
# On Raspberry Pi (recommended)
python3 examples/test_concert_list_item.py
```

The test shows:
- 12 concert items in scrollable list
- Various dates, venues, locations
- Different ratings and source types
- Interactive hover and click states
- Click feedback in status bar

## Design Decisions

### Why 80px Minimum Height?

- **Touch-Friendly:** Comfortable tapping target
- **Content Space:** Room for 3 lines of text + badges
- **Visual Balance:** Not cramped, not wasteful
- **Accessibility:** Meets touch target guidelines

### Why Hover States?

- **Visual Feedback:** User knows item is interactive
- **Familiar Pattern:** Standard for clickable lists
- **Touch Support:** Still works on touchscreens
- **Professional Feel:** Polished interaction

### Why Emit Full show_data?

- **Flexibility:** Handler can access any field
- **Future-Proof:** Can add fields without changing API
- **Simple:** One signal with all info
- **Standard Pattern:** Common in Qt/PyQt

### Why Optional Dividers?

- **Clean Bottom:** Last item doesn't need divider
- **Visual Separation:** Items clearly distinct
- **Professional Look:** Matches modern list UIs
- **Configurable:** Can disable if not wanted

## Component Architecture

```
ConcertListItem (extends QWidget)
    |
    +-- Uses RatingBadge component
    +-- Uses SourceBadge component
    +-- QVBoxLayout (main)
        |
        +-- QHBoxLayout (top row)
        |   +-- Date label
        |   +-- Stretch
        |   +-- Source badge (optional)
        |   +-- Rating badge (optional)
        |
        +-- Venue label
        +-- Location label (optional)
        +-- Divider line (optional)
    |
    +-- Mouse event handling
    +-- Hover/press states
    +-- Emits: clicked(dict) signal
```

## File Locations

```
deadstream/
├── src/ui/
│   └── components/
│       ├── pill_button.py           [Task 1.2]
│       ├── icon_button.py           [Task 1.3]
│       ├── rating_badge.py          [Task 1.4]
│       ├── source_badge.py          [Task 1.4]
│       └── concert_list_item.py     [NEW - Task 1.5]
└── examples/
    ├── test_pill_button.py
    ├── test_icon_button.py
    ├── test_badges.py
    └── test_concert_list_item.py    [NEW - Task 1.5]
```

---

**Phase 10A Task 1.5: Complete**  
**Component Library:** Ready for screen integration!

Next steps:
- Test all components together
- Start applying to actual screens (Phase 10B)
- Build remaining specialized components as needed