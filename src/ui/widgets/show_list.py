"""
Show List Widget for DeadStream Browse Interface

This widget displays a scrollable list of Grateful Dead shows with:
- Date, venue, location
- Rating and review count
- Source type badge
- Touch-friendly tap targets (60x60px minimum)
- Proper formatting matching UI design spec

Can be used for all browse modes:
- All Shows
- Top Rated Shows
- Shows by Date
- Shows by Venue
- Shows by Year
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import centralized styles
from src.ui.styles.button_styles import (
    PRIMARY_BUTTON_STYLE, BLUE_600, BLUE_700, BLUE_800,
    TEXT_WHITE, TEXT_GRAY_400, TEXT_GRAY_500
)


class ShowCard(QFrame):
    """
    Individual show card widget
    
    Displays:
    - Date (large, bold)
    - Venue (medium)
    - Location (small, gray)
    - Rating (star + number)
    - Source badge (SBD/AUD/MTX)
    - Play button
    
    Signals:
    - play_requested: Emitted when card is clicked or Play button tapped
    """
    
    play_requested = pyqtSignal(dict)  # Emits show dictionary
    
    def __init__(self, show_data, parent=None):
        """
        Initialize show card
        
        Args:
            show_data: Dictionary from database with show information
            parent: Parent widget
        """
        super().__init__(parent)
        self.show_data = show_data
        self.setup_ui()
    
    def setup_ui(self):
        """Create card layout and widgets"""
        # Card styling - blue primary style like browse buttons
        self.setStyleSheet(f"""
            ShowCard {{
                background-color: {BLUE_600};
                border-radius: 8px;
                padding: 12px;
                border: none;
            }}
            ShowCard:hover {{
                background-color: {BLUE_700};
            }}
        """)
        
        # Make entire card clickable
        self.setCursor(Qt.PointingHandCursor)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # Left side: Show info (date, venue, location)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        # Date - large, bold (e.g., "1977-05-08")
        date_label = QLabel(self.show_data['date'])
        date_label.setStyleSheet(f"""
            color: {TEXT_WHITE};
            font-size: 20px;
            font-weight: 600;
        """)
        info_layout.addWidget(date_label)

        # Venue - medium (e.g., "Barton Hall, Cornell University")
        venue = self.show_data.get('venue', 'Unknown Venue')
        venue_label = QLabel(venue)
        venue_label.setStyleSheet(f"""
            color: {TEXT_WHITE};
            font-size: 16px;
        """)
        venue_label.setWordWrap(True)
        venue_label.setMaximumWidth(400)
        info_layout.addWidget(venue_label)

        # Location - small, lighter (e.g., "Ithaca, NY")
        city = self.show_data.get('city', '')
        state = self.show_data.get('state', '')
        if city and state:
            location = f"{city}, {state}"
        elif city:
            location = city
        elif state:
            location = state
        else:
            location = "Unknown Location"

        location_label = QLabel(location)
        location_label.setStyleSheet(f"""
            color: {TEXT_WHITE};
            font-size: 14px;
            opacity: 0.8;
        """)
        info_layout.addWidget(location_label)
        
        # Metadata badges (source type, rating)
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(8)
        
        # Source type badge (SBD/AUD/MTX) if available
        source = self.show_data.get('source', '')
        if source:
            source_badge = QLabel(source.upper()[:3])  # SBD, AUD, or MTX
            source_badge.setStyleSheet(f"""
                background-color: rgba(255, 255, 255, 0.2);
                color: {TEXT_WHITE};
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 600;
            """)
            badges_layout.addWidget(source_badge)

        # Rating badge (star + number)
        rating = self.show_data.get('avg_rating')
        if rating:
            rating_badge = QLabel(f"[*] {rating:.1f}/5.0")
            rating_badge.setStyleSheet(f"""
                color: {TEXT_WHITE};
                font-size: 14px;
                font-weight: 600;
            """)
            badges_layout.addWidget(rating_badge)
        
        badges_layout.addStretch()
        info_layout.addLayout(badges_layout)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Right side: Play button (darker blue to contrast with card)
        play_button = QPushButton("Play ->")
        play_button.setMinimumSize(100, 60)  # Touch-friendly
        play_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {BLUE_800};
                color: {TEXT_WHITE};
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                padding: 12px 20px;
            }}
            QPushButton:hover {{
                background-color: #1e3a8a;
            }}
            QPushButton:pressed {{
                background-color: #1e40af;
            }}
        """)
        play_button.clicked.connect(self.on_play_clicked)
        layout.addWidget(play_button, alignment=Qt.AlignVCenter)
        
        self.setLayout(layout)
    
    def on_play_clicked(self):
        """Handle play button click"""
        self.play_requested.emit(self.show_data)
    
    def mousePressEvent(self, event):
        """Make entire card clickable"""
        if event.button() == Qt.LeftButton:
            self.on_play_clicked()
        super().mousePressEvent(event)


class ShowListWidget(QWidget):
    """
    Scrollable list of show cards
    
    Features:
    - Displays multiple shows in scrollable list
    - Touch-friendly scrolling
    - Loading state
    - Empty state
    - Automatic sizing
    
    Signals:
    - show_selected: Emitted when user selects a show to play
    """
    
    show_selected = pyqtSignal(dict)  # Emits show dictionary
    
    def __init__(self, parent=None):
        """Initialize show list widget"""
        super().__init__(parent)
        self.shows = []
        self.setup_ui()
    
    def setup_ui(self):
        """Create list layout"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Scroll area for show cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #000000;
            }
            QScrollBar:vertical {
                background-color: #1f2937;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4b5563;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6b7280;
            }
        """)
        
        # Container widget for show cards
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(8)
        self.container_layout.setContentsMargins(16, 16, 16, 16)
        self.container_layout.addStretch()
        
        scroll_area.setWidget(self.container)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
    
    def load_shows(self, shows):
        """
        Load and display shows in list
        
        Args:
            shows: List of show dictionaries from database
        """
        # Clear existing cards
        self.clear_shows()
        
        # Store shows
        self.shows = shows
        
        # Create card for each show
        for show in shows:
            card = ShowCard(show)
            card.play_requested.connect(self.on_show_selected)
            
            # Insert before stretch
            self.container_layout.insertWidget(
                self.container_layout.count() - 1,
                card
            )
    
    def clear_shows(self):
        """Remove all show cards from list"""
        # Remove all widgets except the stretch at the end
        while self.container_layout.count() > 1:
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.shows = []
    
    def on_show_selected(self, show_data):
        """Handle show selection"""
        self.show_selected.emit(show_data)
    
    def set_empty_state(self, message="No shows found"):
        """
        Display empty state message
        
        Args:
            message: Message to display when no shows available
        """
        self.clear_shows()
        
        # Create centered empty state label
        empty_label = QLabel(message)
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet("""
            color: #6b7280;
            font-size: 18px;
            padding: 60px 20px;
        """)
        
        self.container_layout.insertWidget(0, empty_label)
    
    def set_loading_state(self):
        """Display loading message"""
        self.clear_shows()
        
        loading_label = QLabel("Loading shows...")
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet("""
            color: #9ca3af;
            font-size: 18px;
            padding: 60px 20px;
        """)
        
        self.container_layout.insertWidget(0, loading_label)