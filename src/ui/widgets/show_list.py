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
    QPushButton, QScrollArea, QFrame, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
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


class ShowItemWidget(QWidget):
    """Custom widget for displaying a show in the list with nice formatting"""

    def __init__(self, show_data, parent=None):
        """Initialize show item widget"""
        super().__init__(parent)
        self.show_data = show_data
        self.setup_ui()

    def setup_ui(self):
        """Create item layout with styled text"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Date - Large, bold (24px)
        date_label = QLabel(self.show_data['date'])
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: 700;
            }
        """)
        layout.addWidget(date_label)

        # Venue - Medium (18px)
        venue = self.show_data.get('venue', 'Unknown Venue')
        venue_label = QLabel(venue)
        venue_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: 500;
            }
        """)
        venue_label.setWordWrap(True)
        layout.addWidget(venue_label)

        # Location - Smaller, lighter (16px)
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
        location_label.setStyleSheet("""
            QLabel {
                color: #d1d5db;
                font-size: 16px;
            }
        """)
        layout.addWidget(location_label)

        # Metadata (rating and source) - 14px
        metadata_parts = []
        rating = self.show_data.get('avg_rating')
        if rating:
            metadata_parts.append(f"[*] {rating:.1f}/5.0")

        source = self.show_data.get('source', '')
        if source:
            metadata_parts.append(source.upper()[:3])

        if metadata_parts:
            metadata_label = QLabel(" | ".join(metadata_parts))
            metadata_label.setStyleSheet("""
                QLabel {
                    color: #9ca3af;
                    font-size: 14px;
                    font-weight: 600;
                }
            """)
            layout.addWidget(metadata_label)

        self.setLayout(layout)


class ShowListWidget(QWidget):
    """
    Scrollable list of shows using QListWidget

    Features:
    - Displays multiple shows in scrollable list
    - Touch-friendly scrolling
    - Loading state
    - Empty state
    - Automatic sizing
    - Clean list styling matching venue browser

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

        # Create QListWidget with venue browser styling
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #1f2937;
                color: white;
                border: 2px solid #374151;
                border-radius: 8px;
                padding: 4px;
            }
            QListWidget::item {
                border-bottom: 1px solid #374151;
                margin: 4px;
            }
            QListWidget::item:selected {
                background-color: #10b981;
                border-radius: 6px;
            }
            QListWidget::item:hover {
                background-color: #374151;
                border-radius: 6px;
            }
        """)

        # Connect selection signal
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self.on_item_clicked)

        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def load_shows(self, shows):
        """
        Load and display shows in list

        Args:
            shows: List of show dictionaries from database
        """
        # Clear existing items
        self.list_widget.clear()

        # Store shows
        self.shows = shows

        # Create list item for each show
        for show in shows:
            # Create list item
            item = QListWidgetItem(self.list_widget)

            # Store show data in item
            item.setData(Qt.UserRole, show)

            # Create custom widget for this show
            show_widget = ShowItemWidget(show)

            # Set item size to fit widget
            item.setSizeHint(QSize(0, 120))  # Height for custom widget

            # Add item to list
            self.list_widget.addItem(item)

            # Set custom widget for item
            self.list_widget.setItemWidget(item, show_widget)

    def clear_shows(self):
        """Remove all show items from list"""
        self.list_widget.clear()
        self.shows = []

    def on_item_clicked(self, item):
        """Handle item selection"""
        show_data = item.data(Qt.UserRole)
        if show_data:
            self.show_selected.emit(show_data)

    def set_empty_state(self, message="No shows found"):
        """
        Display empty state message

        Args:
            message: Message to display when no shows available
        """
        self.list_widget.clear()
        self.shows = []

        # Add single item with message
        item = QListWidgetItem(message)
        item.setFlags(Qt.NoItemFlags)  # Make it non-selectable
        item.setForeground(Qt.gray)
        self.list_widget.addItem(item)

    def set_loading_state(self):
        """Display loading message"""
        self.list_widget.clear()
        self.shows = []

        # Add single item with loading message
        item = QListWidgetItem("Loading shows...")
        item.setFlags(Qt.NoItemFlags)  # Make it non-selectable
        item.setForeground(Qt.lightGray)
        self.list_widget.addItem(item)