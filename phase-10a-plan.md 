# Phase 10A Implementation Plan: UX Pivot & Browse Shows Redesign

**Phase**: 10A (new sub-phase)
**Estimated Duration**: 6-8 hours
**Status**: Not Started
**Created**: January 2, 2026

## Overview

Phase 10A addresses mid-project UX insights gained from actually using the DeadStream interface. This pivot refines the Browse Shows screen architecture, elevates Random Show to a killer feature, and implements a filters system for curated show discovery.

### Why This Phase Exists

After building sufficient functionality to use the interface hands-on, usage patterns revealed:
- Browse by Date feels like the most natural way to find shows (time machine effect)
- Random Show has huge potential but needs prominent placement and better UX
- Top-Rated Shows screen feels static and boring
- Filters (Wall of Sound, Dick's Picks, etc.) would unlock curated discovery

This phase acts on these insights before hardware integration, when UI changes are easier to implement.

### Core Philosophy

This is NOT scope creep - it's **refinement based on user feedback**. We're:
- Re-prioritizing existing features
- Simplifying the overall architecture
- Leveraging code we've already built
- Making the app more distinctively "Deadhead"

---

## Task Breakdown

### Task 1: Browse Shows Screen Redesign (3 hours)

#### Subtask 1.1: Create ShowCard Widget (1 hour)
**File**: `src/ui/widgets/show_card.py`

**Purpose**: Reusable widget for displaying show details with visual appeal.

**Requirements**:
- Display show date in large, vintage-inspired font (48pt, e.g., "May 8, 1977")
- Show venue name and location (24pt)
- Display setlist in scrollable area (10+ songs? scroll)
- Show audio quality badge with color coding:
  - Soundboard: Gold/yellow background
  - Score 9.0+: Green indicator
  - Score 8.0-8.9: Blue indicator
- Large "PLAY" button (always visible)
- "Try Another" button (hidden by default, shown only in Random mode)
- Responsive layout for 1280x720 landscape display
- Smooth fade-in animation (400ms) when content loads

**Signal Architecture**:
```python
class ShowCard(QWidget):
    play_clicked = pyqtSignal(str)  # Emits show identifier
    try_another_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._connect_signals()
    
    def load_show(self, show_data):
        """Populate card with show details"""
        pass
    
    def fade_in(self, show_data):
        """Animate card appearance with new show data"""
        pass
    
    def set_mode(self, mode):
        """Set card mode: 'default', 'random', 'date_selected'"""
        # Controls "Try Another" button visibility
        pass
    
    def show_loading(self):
        """Display loading state with animation"""
        pass
```

**Visual Design Notes**:
- Dark background consistent with existing UI
- High contrast text for readability on touchscreen
- Generous padding for touch targets (44px minimum)
- Consider using QFont with weight/style variations for hierarchy
- Loading state: spinning icon + "Finding you a show..." text

**Testing**:
- [ ] All show fields display correctly
- [ ] Fade-in animation is smooth (400ms duration)
- [ ] Buttons emit correct signals
- [ ] Setlist scrolling works for long lists
- [ ] Quality badge colors match criteria
- [ ] Responsive at 1280x720 resolution
- [ ] "Try Another" button only shows in random mode

---

#### Subtask 1.2: Refactor Browse Shows Screen Layout (1.5 hours)
**File**: `src/ui/screens/browse_shows_screen.py`

**Purpose**: Restructure Browse Shows as the primary navigation hub.

**Layout Changes**:

**Left Side - Navigation Panel (30% width)**:
```python
# Vertical button stack with visual priority:
1. Browse by Date
   - Larger size
   - Primary styling (brighter, more prominent)
   - Clear label: "Browse by Date"

2. Random Show
   - Medium size
   - Exciting color treatment
   - Optional: Skull icon or visual interest
   - Label: "Random Show"

3. Filters
   - Medium size
   - Secondary styling
   - Label: "Filters" (updates to "Filters: [active]" when filter applied)

4. Top-Rated (OPTIONAL - consider removing)
   - Smaller size
   - Tertiary styling
   - Or remove entirely if redundant with filters
```

**Right Side - ShowCard Display Area (70% width)**:
```python
# Dynamic display with multiple states:

DEFAULT STATE:
- Query most recent show from playback_history table
- Display as "Last Played" or "Now Playing"
- If no history: Welcome message with usage instructions
- ShowCard in 'default' mode (no "Try Another" button)

RANDOM STATE:
- Random show selected via button click
- ShowCard in 'random' mode ("Try Another" visible)
- Smooth transition animation

DATE_SELECTED STATE:
- Show chosen from Browse by Date flow
- ShowCard in 'date_selected' mode
- No "Try Another" button

FILTERED STATE:
- Random show matching active filter
- ShowCard in 'random' mode
- Filter name shown in UI context
```

**Signal Connections**:
```python
def _setup_signals(self):
    """Connect navigation signals"""
    self.browse_by_date_btn.clicked.connect(self._on_browse_by_date)
    self.random_show_btn.clicked.connect(self._on_random_show)
    self.filters_btn.clicked.connect(self._on_show_filters)
    
    # ShowCard signals
    self.show_card.play_clicked.connect(self._on_play_show)
    self.show_card.try_another_clicked.connect(self._on_random_show)

def _on_play_show(self, identifier):
    """Handle play request from ShowCard"""
    # Emit signal to main app or call player directly
    # Follow existing architecture patterns
    pass

def _on_random_show(self):
    """Handle Random Show button or Try Another"""
    self.show_card.show_loading()
    show = self.db.get_random_excellent_show(
        min_score=8.0,
        active_filter=self.current_filter
    )
    if show:
        self.show_card.fade_in(show)
        self.show_card.set_mode('random')
    else:
        self.show_card.show_error("No shows found matching criteria")
```

**Key Implementation Details**:
- Use QSplitter or custom layout for left/right split
- Ensure smooth transitions between ShowCard states
- Maintain state awareness (current_filter, last_mode, etc.)
- Handle edge cases (no playback history, no filtered results)

**Testing**:
- [ ] Navigation buttons visually prioritized correctly
- [ ] ShowCard updates on all navigation modes
- [ ] "Last Played" loads correctly on screen open
- [ ] Transitions between states are smooth
- [ ] No layout breaking at any screen state
- [ ] Signals properly connected and firing

---

#### Subtask 1.3: Update Browse by Date Flow (0.5 hours)
**File**: `src/ui/screens/browse_shows_screen.py`

**Purpose**: Keep user in Browse Shows context after date selection.

**Current Behavior** (if applicable):
- User selects Year → Month → Day
- App navigates away to show details or player

**New Behavior**:
- User selects Year → Month → Day
- Selected show loads in ShowCard (right side)
- User remains in Browse Shows screen
- Can play show or continue browsing

**Implementation**:
```python
def _on_date_selected(self, date_str):
    """
    Called when user completes date selection.
    
    Args:
        date_str: ISO format date string (YYYY-MM-DD)
    """
    # Query database for show on this date
    show = self.db.get_show_by_date(date_str)
    
    if show:
        # Load show in ShowCard
        self.show_card.fade_in(show)
        self.show_card.set_mode('date_selected')
    else:
        # Handle no show found
        self.show_card.show_error(f"No show found for {date_str}")
```

**Integration Notes**:
- Connect this to existing date browser widget
- May need to add signal to date browser: `date_selected = pyqtSignal(str)`
- Ensure date browser clears/resets appropriately

**Testing**:
- [ ] Date selection loads show in ShowCard
- [ ] User stays on Browse Shows screen
- [ ] Can select another date without issues
- [ ] "No show found" handled gracefully

---

### Task 2: Random Show Implementation (3 hours)

#### Subtask 2.1: Database Query Logic (0.5 hours)
**File**: `src/database/database.py`

**Purpose**: Add method to retrieve random high-quality shows.

**New Method**:
```python
def get_random_excellent_show(self, min_score=8.0, active_filter=None):
    """
    Get a random show with high recording quality.
    
    Args:
        min_score (float): Minimum recording_score threshold (default 8.0)
        active_filter (int): Optional filter_id to apply to query
        
    Returns:
        dict: Show data with all fields, or None if no shows match
        
    Example:
        >>> show = db.get_random_excellent_show(min_score=9.0)
        >>> print(show['date'], show['venue'])
        1977-05-08 Barton Hall, Cornell University
    """
    cursor = self.conn.cursor()
    
    # Base query
    query = """
        SELECT * FROM shows 
        WHERE recording_score >= ? 
    """
    params = [min_score]
    
    # Apply filter if provided
    if active_filter:
        filter_clause = self.get_filter_clause(active_filter)
        query += f" AND ({filter_clause})"
    
    # Randomize and limit
    query += " ORDER BY RANDOM() LIMIT 1"
    
    cursor.execute(query, params)
    row = cursor.fetchone()
    
    if row:
        return self._row_to_dict(row)
    return None
```

**Supporting Method**:
```python
def _row_to_dict(self, row):
    """
    Convert sqlite3.Row to dictionary.
    
    Args:
        row: sqlite3.Row object from query
        
    Returns:
        dict: Show data with column names as keys
    """
    if row is None:
        return None
    
    return {
        'identifier': row['identifier'],
        'date': row['date'],
        'venue': row['venue'],
        'city': row['city'],
        'state': row['state'],
        'recording_score': row['recording_score'],
        # ... other fields
    }
```

**Testing**:
- [ ] Returns different shows on repeated calls
- [ ] Respects min_score threshold
- [ ] Returns None when no shows match criteria
- [ ] Applies filters correctly when provided
- [ ] Handles database errors gracefully

---

#### Subtask 2.2: Random Show Button Logic (1 hour)
**File**: `src/ui/screens/browse_shows_screen.py`

**Purpose**: Implement Random Show button click handler with UX polish.

**Implementation**:
```python
def _on_random_show(self):
    """
    Handle Random Show button click or Try Another request.
    
    Fetches random high-quality show and displays in ShowCard.
    Shows loading state during query.
    """
    # Show loading indicator
    self.show_card.show_loading()
    
    # Query database
    # Note: Consider using QThread if query is slow (>100ms)
    show = self.db.get_random_excellent_show(
        min_score=8.0,
        active_filter=self.current_filter
    )
    
    if show:
        # Animate ShowCard update
        self.show_card.fade_in(show)
        self.show_card.set_mode('random')  # Shows "Try Another" button
    else:
        # Handle edge case: no shows meet criteria
        # This could happen with very restrictive filters
        self.show_card.show_error("No shows found matching criteria")
```

**UX Considerations**:
- Loading state should appear immediately on click
- If query takes >200ms, loading indicator is visible briefly
- Fade-in animation provides satisfying feedback
- "Try Another" button should appear after a slight delay (200ms?) to encourage reading the card

**Error Handling**:
```python
try:
    show = self.db.get_random_excellent_show(...)
except Exception as e:
    logger.error(f"Random show query failed: {e}")
    self.show_card.show_error("Unable to fetch random show")
```

**Testing**:
- [ ] Loading indicator appears on click
- [ ] Random show loads and displays
- [ ] "Try Another" button appears
- [ ] Clicking "Try Another" loads new random show
- [ ] Filter integration works correctly
- [ ] Error states handled gracefully

---

#### Subtask 2.3: Visual Polish (1.5 hours)
**File**: `src/ui/widgets/show_card.py`

**Purpose**: Add animations and visual refinements for professional feel.

**1. Loading State Animation**:
```python
def show_loading(self):
    """Display loading state with spinning animation"""
    # Create spinning icon (use QLabel with pixmap or QMovie)
    # Or use QPropertyAnimation on rotation property
    
    # Example with rotation:
    self.loading_label = QLabel("◉")  # Or use image
    self.loading_label.setAlignment(Qt.AlignCenter)
    
    self.rotation_animation = QPropertyAnimation(self.loading_label, b"rotation")
    self.rotation_animation.setDuration(1000)
    self.rotation_animation.setStartValue(0)
    self.rotation_animation.setEndValue(360)
    self.rotation_animation.setLoopCount(-1)  # Infinite loop
    self.rotation_animation.start()
    
    # Show "Finding you a show..." text
    self.loading_text = QLabel("Finding you a show...")
    self.loading_text.setAlignment(Qt.AlignCenter)
```

**2. Fade-In Animation**:
```python
def fade_in(self, show_data):
    """
    Animate show card appearance with opacity transition.
    
    Args:
        show_data (dict): Show information to display
    """
    # Stop any loading animation
    if hasattr(self, 'rotation_animation'):
        self.rotation_animation.stop()
    
    # Set up opacity effect
    self.opacity_effect = QGraphicsOpacityEffect()
    self.setGraphicsEffect(self.opacity_effect)
    
    # Create animation
    self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
    self.fade_animation.setDuration(400)  # 400ms
    self.fade_animation.setStartValue(0.0)
    self.fade_animation.setEndValue(1.0)
    self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    # Update content BEFORE starting animation
    self.load_show(show_data)
    
    # Start animation
    self.fade_animation.start()
```

**3. Typography Hierarchy**:
```python
def _setup_fonts(self):
    """Configure font hierarchy for show card"""
    # Date: Large, bold
    self.date_font = QFont("Arial", 48, QFont.Bold)
    
    # Venue: Medium, normal
    self.venue_font = QFont("Arial", 24, QFont.Normal)
    
    # Setlist: Small, normal
    self.setlist_font = QFont("Arial", 14, QFont.Normal)
    
    # Consider loading custom font if available:
    # QFontDatabase.addApplicationFont("fonts/VintageFont.ttf")
```

**4. Color Coding for Quality**:
```python
def _get_quality_badge_style(self, show_data):
    """
    Generate CSS style for quality badge.
    
    Args:
        show_data (dict): Show info including recording_score
        
    Returns:
        str: CSS style string
    """
    score = show_data.get('recording_score', 0)
    is_sbd = 'sbd' in show_data.get('identifier', '').lower()
    
    if is_sbd:
        # Soundboard: Gold background
        bg_color = "#FFD700"
        text_color = "#000000"
        label = "SOUNDBOARD"
    elif score >= 9.0:
        # Excellent: Green
        bg_color = "#2ECC71"
        text_color = "#FFFFFF"
        label = f"EXCELLENT ({score:.1f})"
    elif score >= 8.0:
        # Very Good: Blue
        bg_color = "#3498DB"
        text_color = "#FFFFFF"
        label = f"VERY GOOD ({score:.1f})"
    else:
        # Good: Gray
        bg_color = "#95A5A6"
        text_color = "#FFFFFF"
        label = f"GOOD ({score:.1f})"
    
    return f"""
        QLabel {{
            background-color: {bg_color};
            color: {text_color};
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}
    """, label
```

**5. Button Styling**:
```python
# Play button: Large, prominent
play_btn_style = """
    QPushButton {
        background-color: #E74C3C;
        color: white;
        font-size: 24px;
        font-weight: bold;
        padding: 16px 32px;
        border-radius: 8px;
        border: none;
    }
    QPushButton:hover {
        background-color: #C0392B;
    }
    QPushButton:pressed {
        background-color: #A93226;
    }
"""

# Try Another button: Secondary styling
try_another_style = """
    QPushButton {
        background-color: #34495E;
        color: white;
        font-size: 18px;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
    }
    QPushButton:hover {
        background-color: #2C3E50;
    }
"""
```

**Testing**:
- [ ] Loading animation spins smoothly
- [ ] Fade-in animation is smooth (400ms)
- [ ] Typography hierarchy is clear and readable
- [ ] Quality badges use correct colors
- [ ] Buttons have proper hover/press states
- [ ] All animations clean up properly (no memory leaks)

---

### Task 3: Filters System (2 hours)

#### Subtask 3.1: Database Schema & Migration (0.5 hours)
**Files**: 
- `database/schema.sql` (update)
- `database/migrations/add_filters_table.py` (new)

**Purpose**: Create filters table and seed with initial filter definitions.

**Schema Addition**:
```sql
-- Filters table for curated show discovery
CREATE TABLE IF NOT EXISTS filters (
    filter_id INTEGER PRIMARY KEY AUTOINCREMENT,
    filter_name TEXT NOT NULL,
    filter_description TEXT,
    filter_query TEXT NOT NULL,  -- SQL WHERE clause fragment
    filter_type TEXT,  -- Category: 'era', 'series', 'quality', 'venue'
    is_active INTEGER DEFAULT 0,  -- Currently selected filter (0=no, 1=yes)
    created_date TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Index for quick filtering
CREATE INDEX IF NOT EXISTS idx_filter_type ON filters(filter_type);
```

**Seed Data**:
```sql
-- Initial filter set
INSERT INTO filters (filter_name, filter_description, filter_query, filter_type) VALUES
    ('Wall of Sound', 
     'Shows from the legendary Wall of Sound era (1974)', 
     "strftime('%Y', date) = '1974'", 
     'era'),
    
    ('Dick''s Picks', 
     'Shows featured in the Dick''s Picks series',
     "identifier LIKE '%dp%' OR notes LIKE '%Dick''s Picks%'", 
     'series'),
    
    ('Soundboard Only', 
     'Only soundboard recordings (highest quality)',
     "identifier LIKE '%sbd%' OR identifier LIKE '%soundboard%'", 
     'quality'),
    
    ('1972', 
     'Shows from the consensus peak year',
     "strftime('%Y', date) = '1972'", 
     'era'),
    
    ('Europe ''72', 
     'European tour shows from spring 1972',
     "strftime('%Y-%m', date) BETWEEN '1972-04' AND '1972-05'", 
     'era'),
    
    ('Barton Hall Era',
     'Shows from the legendary May 1977 run',
     "strftime('%Y-%m', date) = '1977-05'",
     'era'),
    
    ('Excellent Quality',
     'Only the highest-rated recordings (9.0+)',
     'recording_score >= 9.0',
     'quality');
```

**Migration Script**: `database/migrations/add_filters_table.py`
```python
"""
Add filters table to database.

Created: 2026-01-02
Phase: 10A
"""

import sqlite3
import os

def migrate(db_path):
    """
    Add filters table and seed data.
    
    Args:
        db_path (str): Path to database file
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filters (
            filter_id INTEGER PRIMARY KEY AUTOINCREMENT,
            filter_name TEXT NOT NULL,
            filter_description TEXT,
            filter_query TEXT NOT NULL,
            filter_type TEXT,
            is_active INTEGER DEFAULT 0,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create index
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_filter_type 
        ON filters(filter_type)
    """)
    
    # Seed data (insert statements from above)
    # ...
    
    conn.commit()
    conn.close()
    print(f"Migration complete: filters table added to {db_path}")

if __name__ == '__main__':
    # Run migration on development database
    db_path = 'database/deadstream.db'
    migrate(db_path)
```

**Testing**:
- [ ] Migration runs without errors
- [ ] Filters table created with correct schema
- [ ] Seed data inserted correctly
- [ ] Index created successfully
- [ ] Can query filters table

---

#### Subtask 3.2: Filters Selection Dialog (1 hour)
**File**: `src/ui/dialogs/filter_dialog.py`

**Purpose**: Create modal dialog for selecting active filter.

**UI Layout**:
```python
class FilterDialog(QDialog):
    """
    Modal dialog for selecting show filters.
    
    Signals:
        filter_selected(int): Emitted when filter is chosen (filter_id)
        filter_cleared(): Emitted when "Clear Filter" is clicked
    """
    
    filter_selected = pyqtSignal(int)
    filter_cleared = pyqtSignal()
    
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.selected_filter = None
        
        self.setWindowTitle("Select Filter")
        self.setModal(True)
        self.resize(600, 500)
        
        self._setup_ui()
        self._load_filters()
    
    def _setup_ui(self):
        """Create dialog layout"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Filter Shows")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Filter groups (scrollable)
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.filters_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear Filter")
        clear_btn.clicked.connect(self._on_clear_filter)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def _load_filters(self):
        """Load and display available filters grouped by type"""
        # Query filters from database
        filters = self.db.get_all_filters()
        
        # Group by filter_type
        grouped = {}
        for f in filters:
            ftype = f['filter_type'] or 'Other'
            if ftype not in grouped:
                grouped[ftype] = []
            grouped[ftype].append(f)
        
        # Display each group
        for filter_type, filter_list in grouped.items():
            # Group header
            header = QLabel(filter_type.upper())
            header.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
            self.filters_layout.addWidget(header)
            
            # Filter buttons
            for f in filter_list:
                btn = self._create_filter_button(f)
                self.filters_layout.addWidget(btn)
    
    def _create_filter_button(self, filter_data):
        """
        Create clickable button for a filter.
        
        Args:
            filter_data (dict): Filter info from database
            
        Returns:
            QPushButton: Styled filter button
        """
        btn = QPushButton()
        btn.setCheckable(True)
        
        # Button text: name + description
        text = f"{filter_data['filter_name']}\n{filter_data['filter_description']}"
        btn.setText(text)
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 12px;
                background-color: #34495E;
                color: white;
                border: 2px solid #34495E;
                border-radius: 8px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #2C3E50;
                border-color: #3498DB;
            }
            QPushButton:checked {
                background-color: #3498DB;
                border-color: #3498DB;
            }
        """)
        
        # Connect click handler
        btn.clicked.connect(
            lambda checked, fid=filter_data['filter_id']: self._on_filter_clicked(fid)
        )
        
        return btn
    
    def _on_filter_clicked(self, filter_id):
        """Handle filter button click"""
        self.selected_filter = filter_id
        self.filter_selected.emit(filter_id)
        self.accept()
    
    def _on_clear_filter(self):
        """Handle clear filter button"""
        self.filter_cleared.emit()
        self.accept()
```

**Database Support Method** (add to `database.py`):
```python
def get_all_filters(self):
    """
    Retrieve all available filters.
    
    Returns:
        list: List of filter dictionaries
    """
    cursor = self.conn.cursor()
    cursor.execute("""
        SELECT filter_id, filter_name, filter_description, 
               filter_query, filter_type
        FROM filters
        ORDER BY filter_type, filter_name
    """)
    
    filters = []
    for row in cursor.fetchall():
        filters.append({
            'filter_id': row[0],
            'filter_name': row[1],
            'filter_description': row[2],
            'filter_query': row[3],
            'filter_type': row[4]
        })
    
    return filters
```

**Testing**:
- [ ] Dialog opens and displays all filters
- [ ] Filters grouped by type correctly
- [ ] Filter selection emits correct signal
- [ ] "Clear Filter" works as expected
- [ ] Dialog styling is consistent with app
- [ ] Buttons have proper hover/checked states

---

#### Subtask 3.3: Filter Application Logic (0.5 hours)
**Files**: 
- `src/ui/screens/browse_shows_screen.py`
- `src/database/database.py`

**Purpose**: Integrate filter selection with Random Show functionality.

**Browse Shows Screen Integration**:
```python
class BrowseShowsScreen(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_filter = None  # Track active filter
        # ... rest of init
    
    def _on_show_filters(self):
        """Open filter selection dialog"""
        dialog = FilterDialog(self.db, self)
        dialog.filter_selected.connect(self._on_filter_selected)
        dialog.filter_cleared.connect(self._on_filter_cleared)
        dialog.exec_()
    
    def _on_filter_selected(self, filter_id):
        """
        Handle filter selection.
        
        Args:
            filter_id (int): ID of selected filter
        """
        self.current_filter = filter_id
        
        # Update Filters button to show active filter
        filter_name = self.db.get_filter_name(filter_id)
        self.filters_btn.setText(f"Filters: {filter_name}")
        
        # Update button styling to indicate active filter
        self.filters_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                /* ... other styles ... */
            }
        """)
        
        # Optionally: Auto-trigger random show with new filter
        self._on_random_show()
    
    def _on_filter_cleared(self):
        """Handle filter being cleared"""
        self.current_filter = None
        
        # Reset Filters button
        self.filters_btn.setText("Filters")
        self.filters_btn.setStyleSheet("""
            /* Reset to default styling */
        """)
        
        # Optionally: Reload default state
        self._load_last_played()
```

**Database Helper Methods**:
```python
def get_filter_name(self, filter_id):
    """
    Get display name for a filter.
    
    Args:
        filter_id (int): Filter ID
        
    Returns:
        str: Filter name
    """
    cursor = self.conn.cursor()
    cursor.execute("SELECT filter_name FROM filters WHERE filter_id = ?", 
                   (filter_id,))
    result = cursor.fetchone()
    return result[0] if result else "Unknown"

def get_filter_clause(self, filter_id):
    """
    Get SQL WHERE clause for a filter.
    
    Args:
        filter_id (int): Filter ID
        
    Returns:
        str: SQL WHERE clause fragment (or "1=1" if invalid)
    """
    if filter_id is None:
        return "1=1"  # No filtering
    
    cursor = self.conn.cursor()
    cursor.execute("SELECT filter_query FROM filters WHERE filter_id = ?", 
                   (filter_id,))
    result = cursor.fetchone()
    
    return result[0] if result else "1=1"
```

**Testing**:
- [ ] Filter dialog opens from Filters button
- [ ] Selecting filter updates button text
- [ ] Active filter applied to Random Show queries
- [ ] Clear filter resets to default behavior
- [ ] Filter state persists across Random Show clicks
- [ ] Button styling indicates active filter

---

## Git Workflow

### Branch Strategy
```bash
# Main phase branch
git checkout -b phase-10a-ux-pivot

# Feature branches for each task
git checkout -b feature/showcard-widget        # Task 1.1
git checkout -b feature/browse-shows-redesign  # Task 1.2-1.3
git checkout -b feature/random-show            # Task 2
git checkout -b feature/filters-system         # Task 3
```

### Commit Message Format
Follow project standard:
```
<type>(<scope>): <short summary>

<detailed description>

Task X.Y of Phase 10A (N/M hours)
```

**Types**: `feat`, `fix`, `refactor`, `style`, `docs`, `test`

**Example**:
```
feat(browse): add ShowCard widget with animations

- Create ShowCard widget for displaying show details
- Implement fade-in animation on show load
- Add "Try Another" button for Random Show mode
- Style with vintage typography and quality badges
- Follow PyQt5 signal/slot architecture

Task 1.1 of Phase 10A (1/3 hours)
```

---

## Testing Checklist

### ShowCard Widget
- [ ] Displays all show information correctly
- [ ] Fade-in animation is smooth (400ms)
- [ ] Buttons emit correct signals
- [ ] Scrolling works for long setlists
- [ ] Quality badge colors match criteria (SBD=gold, 9.0+=green, 8.0+=blue)
- [ ] Responsive at 1280x720 resolution
- [ ] Loading animation works
- [ ] "Try Another" only shows in random mode

### Browse Shows Screen
- [ ] Navigation buttons properly prioritized visually
- [ ] ShowCard updates on all navigation modes
- [ ] "Last Played" loads correctly on startup
- [ ] Transitions between states are smooth
- [ ] No layout breaking at any screen state
- [ ] Date selection loads show in card
- [ ] Signals properly connected

### Random Show
- [ ] Returns different shows on repeated clicks
- [ ] Respects quality threshold (min_score=8.0)
- [ ] Loading indicator appears briefly
- [ ] "Try Another" button only shows in random mode
- [ ] Applies active filter correctly
- [ ] Handles "no results" gracefully

### Filters System
- [ ] Filter dialog displays all available filters
- [ ] Filters grouped by type
- [ ] Filter selection updates Random Show behavior
- [ ] Active filter shown in Filters button text
- [ ] "Clear Filter" returns to default behavior
- [ ] Filter queries execute without errors
- [ ] Migration script runs successfully

---

## Integration Notes

### How Tasks Connect

1. **Task 1** creates the foundation:
   - ShowCard widget is used by all other features
   - Browse Shows screen becomes the hub

2. **Task 2** builds on Task 1:
   - Random Show uses ShowCard widget
   - Integrates with Browse Shows screen layout

3. **Task 3** enhances Task 2:
   - Filters modify Random Show queries
   - Uses existing ShowCard display

### Potential Issues & Solutions

**Issue**: Loading feels slow on Random Show click
- **Solution**: Add 200ms minimum for loading animation (makes it feel intentional)
- **Solution**: Use QThread if database query takes >100ms

**Issue**: ShowCard text too small on touchscreen
- **Solution**: Test on actual 7" display, adjust font sizes
- **Solution**: Use generous padding (44px min for touch targets)

**Issue**: Filter queries returning no results
- **Solution**: Always test filters with `SELECT COUNT(*)` first
- **Solution**: Show helpful error: "No shows match this filter. Try another?"

**Issue**: Too many filters cluttering dialog
- **Solution**: Start with 5-7 curated filters
- **Solution**: Add more based on user feedback later

---

## Success Criteria

At completion of Phase 10A, you should have:

### Functionality
- [x] Browse Shows screen as primary navigation hub
- [x] Random Show as prominent, exciting feature
- [x] Filters system for curated discovery
- [x] ShowCard widget with smooth animations
- [x] All navigation modes working seamlessly

### Code Quality
- [x] Zero technical debt
- [x] All code following PEP 8 and project standards
- [x] Comprehensive docstrings and comments
- [x] Proper error handling throughout
- [x] Signal/slot architecture maintained

### User Experience
- [x] Smooth, professional animations
- [x] Clear visual hierarchy
- [x] Responsive touch targets (44px minimum)
- [x] Helpful error messages
- [x] Intuitive navigation flow

### Documentation
- [x] All code commented per project standards
- [x] Git commits with clear messages
- [x] Phase completion summary created
- [x] Lessons learned documented

---

## Working with Claude Code

### Recommended Handoff Pattern

When transitioning a task to Claude Code:

1. **Provide Clear Context**:
   ```
   Claude Code, please implement [task name] according to Phase 10A 
   specifications in /mnt/project/phase-10a-plan.md, Section [X].
   ```

2. **Reference Key Files**:
   - Always include: `07-project-guidelines.md`, `08-import-and-architecture-reference.md`
   - Include: `05-technical-decisions.md` for context
   - Include: Relevant existing files for patterns

3. **Specify Standards**:
   - PEP 8 compliance
   - PyQt5 signal/slot architecture
   - Project naming conventions
   - ASCII-only code (no unicode in source)

4. **Request Deliverables**:
   - File location
   - Brief testing instructions
   - Suggested commit message
   - Any integration notes

### Example Handoff (Task 1.1)

```
Claude Code, please implement the ShowCard widget according to Phase 10A 
Task 1.1 specifications.

Key requirements:
- Create src/ui/widgets/show_card.py
- Follow PyQt5 patterns from 08-import-and-architecture-reference.md
- Use signal/slot architecture (no direct player calls)
- Implement 400ms fade-in animation using QPropertyAnimation
- Follow PEP 8 and standards from 07-project-guidelines.md

When complete, provide:
1. File location
2. Brief testing instructions  
3. Suggested commit message

Include comprehensive docstrings and inline comments per project standards.
```

---

## Time Tracking

| Task | Estimated | Actual | Notes |
|------|-----------|--------|-------|
| 1.1 - ShowCard Widget | 1.0h | | |
| 1.2 - Browse Shows Layout | 1.5h | | |
| 1.3 - Date Flow Update | 0.5h | | |
| 2.1 - Database Query | 0.5h | | |
| 2.2 - Random Show Logic | 1.0h | | |
| 2.3 - Visual Polish | 1.5h | | |
| 3.1 - Database Schema | 0.5h | | |
| 3.2 - Filter Dialog | 1.0h | | |
| 3.3 - Filter Integration | 0.5h | | |
| **TOTAL** | **8.0h** | | |

---

## Next Steps After Phase 10A

1. **Create Phase Completion Summary** (`phase-10a-completion-summary.md`)
   - Time actual vs. estimated
   - What went well / challenges
   - Screenshots of new UI
   - Lessons learned

2. **Update Project Charter**
   - Mark Phase 10A complete
   - Adjust Phase 10B timeline if needed

3. **Merge to Main**
   ```bash
   git checkout main
   git merge phase-10a-ux-pivot
   git tag -a v0.10a -m "Phase 10A: UX Pivot Complete"
   git push origin main --tags
   ```

4. **Begin Phase 10B**
   - Error handling UI
   - Settings integration
   - End-to-end testing
   - Final polish

---

## Notes & Observations

(Use this section during implementation to capture thoughts, decisions, issues encountered, etc.)

---

**Created**: January 2, 2026
**Status**: Ready to Begin
**Estimated Completion**: 8 hours from start