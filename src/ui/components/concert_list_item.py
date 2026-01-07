"""
ConcertListItem - List item widget for displaying concert information.

Used in browse screen to display concert metadata with badges.
Touch-friendly with hover and press states.
"""

import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QCursor
from src.ui.styles.theme import Theme
from src.ui.components.rating_badge import RatingBadge
from src.ui.components.source_badge import SourceBadge


class ConcertListItem(QWidget):
    """
    List item widget for displaying concert information.
    
    Features:
        - Displays date, venue, and location
        - Shows rating and source badges
        - Touch-friendly with hover/press states
        - Emits signal when clicked
        - Optional divider line at bottom
    
    Layout:
        ┌────────────────────────────────────────────┐
        │ 1977-05-08              [SBD] [⭐ 4.8]    │
        │ Barton Hall, Cornell University           │
        │ Ithaca, NY                                 │
        └────────────────────────────────────────────┘
    
    Signals:
        clicked(dict): Emitted when item is clicked, passes show_data
    
    Example:
        item = ConcertListItem({
            'date': '1977-05-08',
            'venue': 'Barton Hall, Cornell University',
            'location': 'Ithaca, NY',
            'rating': 4.8,
            'source': 'SBD'
        })
        item.clicked.connect(self.on_show_selected)
    """
    
    # Signal emitted when item is clicked
    clicked = pyqtSignal(dict)
    
    def __init__(self, show_data, show_divider=True, parent=None):
        """
        Initialize ConcertListItem.
        
        Args:
            show_data (dict): Show information containing:
                - date (str): Concert date (e.g., '1977-05-08')
                - venue (str): Venue name
                - location (str, optional): City, State
                - rating (float, optional): Rating 0.0-5.0
                - source (str, optional): Source type (SBD, AUD, MTX)
            show_divider (bool): Whether to show bottom divider line
            parent (QWidget): Parent widget
        """
        super().__init__(parent)
        
        # Store show data
        self.show_data = show_data
        self.show_divider = show_divider
        
        # State tracking
        self.is_pressed = False
        
        # Initialize UI
        self._init_ui()
        
        # Set cursor
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Enable mouse tracking for hover
        self.setMouseTracking(True)
    
    def _init_ui(self):
        """Initialize the UI layout."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            Theme.LIST_ITEM_PADDING,
            Theme.LIST_ITEM_PADDING,
            Theme.LIST_ITEM_PADDING,
            Theme.LIST_ITEM_PADDING
        )
        main_layout.setSpacing(Theme.SPACING_SMALL)
        
        # Top row: Date + Badges
        top_row = QHBoxLayout()
        top_row.setSpacing(Theme.SPACING_MEDIUM)
        
        # Date label
        self.date_label = QLabel(self.show_data.get('date', 'Unknown Date'))
        self.date_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                background-color: transparent;
            }}
        """)
        top_row.addWidget(self.date_label)
        
        # Spacer to push badges to right
        top_row.addStretch()
        
        # Source badge (if available)
        if 'source' in self.show_data and self.show_data['source']:
            self.source_badge = SourceBadge(self.show_data['source'])
            top_row.addWidget(self.source_badge)
        else:
            self.source_badge = None
        
        # Rating badge (if available)
        if 'rating' in self.show_data and self.show_data['rating']:
            self.rating_badge = RatingBadge(self.show_data['rating'])
            top_row.addWidget(self.rating_badge)
        else:
            self.rating_badge = None
        
        main_layout.addLayout(top_row)
        
        # Venue label
        venue = self.show_data.get('venue', 'Unknown Venue')
        self.venue_label = QLabel(venue)
        self.venue_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_PRIMARY};
                background-color: transparent;
            }}
        """)
        self.venue_label.setWordWrap(True)
        main_layout.addWidget(self.venue_label)
        
        # Location label (if available)
        if 'location' in self.show_data and self.show_data['location']:
            self.location_label = QLabel(self.show_data['location'])
            self.location_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {Theme.BODY_SMALL}px;
                    color: {Theme.TEXT_SECONDARY};
                    background-color: transparent;
                }}
            """)
            main_layout.addWidget(self.location_label)
        else:
            self.location_label = None
        
        # Divider line (if enabled)
        if self.show_divider:
            divider = QFrame()
            divider.setFrameShape(QFrame.HLine)
            divider.setStyleSheet(f"""
                QFrame {{
                    background-color: {Theme.BORDER_SUBTLE};
                    max-height: 1px;
                    border: none;
                }}
            """)
            main_layout.addWidget(divider)
        
        self.setLayout(main_layout)
        
        # Set minimum height
        self.setMinimumHeight(Theme.LIST_ITEM_HEIGHT)
        
        # Apply default background
        self._update_background()
    
    def _update_background(self, hover=False, pressed=False):
        """Update background color based on state."""
        if pressed:
            bg_color = Theme._darken_color(Theme.BG_CARD, 10)
        elif hover:
            bg_color = Theme._lighten_color(Theme.BG_CARD, 5)
        else:
            bg_color = Theme.BG_CARD
        
        self.setStyleSheet(f"""
            ConcertListItem {{
                background-color: {bg_color};
                border-radius: 8px;
            }}
        """)
    
    def mousePressEvent(self, event):
        """Handle mouse press."""
        if event.button() == Qt.LeftButton:
            self.is_pressed = True
            self._update_background(pressed=True)
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        if event.button() == Qt.LeftButton and self.is_pressed:
            self.is_pressed = False
            self._update_background(hover=self.underMouse())
            
            # Emit clicked signal if release is over the widget
            if self.rect().contains(event.pos()):
                self.clicked.emit(self.show_data)
            
            event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def enterEvent(self, event):
        """Handle mouse enter (hover)."""
        if not self.is_pressed:
            self._update_background(hover=True)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave."""
        if not self.is_pressed:
            self._update_background(hover=False)
        super().leaveEvent(event)
    
    def update_show_data(self, show_data):
        """
        Update the displayed show information.
        
        Args:
            show_data (dict): New show information
        """
        self.show_data = show_data
        
        # Update labels
        self.date_label.setText(show_data.get('date', 'Unknown Date'))
        self.venue_label.setText(show_data.get('venue', 'Unknown Venue'))
        
        if self.location_label:
            if 'location' in show_data and show_data['location']:
                self.location_label.setText(show_data['location'])
                self.location_label.show()
            else:
                self.location_label.hide()
        
        # Update badges
        if self.rating_badge and 'rating' in show_data:
            self.rating_badge.update_rating(show_data['rating'])
        
        if self.source_badge and 'source' in show_data:
            self.source_badge.set_source(show_data['source'])