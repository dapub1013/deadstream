#!/usr/bin/env python3
"""
Concert Info Widget for DeadStream Player Screen

Displays concert metadata at the top of the left panel:
- Concert title (date + venue)
- Location (city, state)
- Source type badge (Soundboard/Audience/Matrix)
- Rating badge
- Track count badge
- Favorite button (deferred to future phase)

Part of Phase 10, Task 10.1: Concert Info Widget
"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class ConcertInfoWidget(QFrame):
    """
    Concert information header widget
    
    Displays:
    - Concert title (YYYY/MM/DD [Venue Name])
    - Location (City, State)
    - Metadata badges (source type, rating, track count)
    - Favorite button (future feature)
    
    Signals:
        favorite_toggled: Emitted when user toggles favorite status
    """
    
    # Signals
    favorite_toggled = pyqtSignal(bool)  # True = favorited, False = unfavorited
    
    def __init__(self, parent=None):
        """Initialize concert info widget"""
        super().__init__(parent)
        
        # Data storage
        self.concert_title = ""
        self.location = ""
        self.source_type = ""
        self.rating = 0.0
        self.track_count = 0
        self.is_favorite = False
        
        # UI components
        self.title_label = None
        self.location_label = None
        self.source_badge = None
        self.rating_badge = None
        self.count_badge = None
        self.favorite_button = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create concert info UI"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top row: Title and favorite button
        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        
        # Concert title
        self.title_label = QLabel("No concert loaded")
        self.title_label.setWordWrap(True)
        title_font = QFont("Arial", 20, QFont.DemiBold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #FFFFFF;")
        top_row.addWidget(self.title_label, 1)
        
        # Favorite button (placeholder - functionality deferred)
        self.favorite_button = QPushButton("[Heart]")
        self.favorite_button.setFixedSize(50, 50)
        self.favorite_button.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: #9CA3AF;
                border: none;
                border-radius: 25px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
            QPushButton:pressed {
                background-color: #1F2937;
            }
        """)
        self.favorite_button.clicked.connect(self.on_favorite_clicked)
        self.favorite_button.setEnabled(False)  # Disabled for Phase 10 (add in Phase 12)
        top_row.addWidget(self.favorite_button)
        
        main_layout.addLayout(top_row)
        
        # Location label
        self.location_label = QLabel("")
        location_font = QFont("Arial", 16)
        self.location_label.setFont(location_font)
        self.location_label.setStyleSheet("color: #9CA3AF;")
        main_layout.addWidget(self.location_label)
        
        # Metadata badges row
        badges_row = QHBoxLayout()
        badges_row.setSpacing(10)
        badges_row.setContentsMargins(0, 10, 0, 0)
        
        # Source type badge
        self.source_badge = QLabel("")
        self.source_badge.setStyleSheet("""
            QLabel {
                background-color: #374151;
                color: #E5E7EB;
                padding: 6px 12px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: 600;
            }
        """)
        badges_row.addWidget(self.source_badge)
        
        # Rating badge
        self.rating_badge = QLabel("")
        self.rating_badge.setStyleSheet("""
            QLabel {
                background-color: #374151;
                color: #FCD34D;
                padding: 6px 12px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: 600;
            }
        """)
        badges_row.addWidget(self.rating_badge)
        
        # Track count badge
        self.count_badge = QLabel("")
        self.count_badge.setStyleSheet("""
            QLabel {
                background-color: #374151;
                color: #9CA3AF;
                padding: 6px 12px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: 600;
            }
        """)
        badges_row.addWidget(self.count_badge)
        
        badges_row.addStretch()
        main_layout.addLayout(badges_row)
        
        # Set frame styling
        self.setStyleSheet("""
            ConcertInfoWidget {
                background-color: #1F2937;
                border-bottom: 2px solid #374151;
            }
        """)
        
        self.setLayout(main_layout)
        
        print("[INFO] ConcertInfoWidget initialized")
    
    def load_concert_info(self, show_data):
        """
        Load concert information from show data
        
        Args:
            show_data (dict): Show dictionary with keys:
                - date (str): Show date in YYYY-MM-DD format
                - venue (str): Venue name
                - city (str): City name
                - state (str): State abbreviation
                - source (str): "Soundboard", "Audience", or "Matrix"
                - avg_rating (float): Average rating (0-5.0)
                - track_count (int): Number of tracks (optional)
        
        Example show_data:
            {
                'date': '1977-05-08',
                'venue': 'Barton Hall, Cornell University',
                'city': 'Ithaca',
                'state': 'NY',
                'source': 'Soundboard',
                'avg_rating': 4.8,
                'num_reviews': 234
            }
        """
        # Extract data
        date = show_data.get('date', 'Unknown Date')
        venue = show_data.get('venue', 'Unknown Venue')
        city = show_data.get('city', 'Unknown City')
        state = show_data.get('state', 'Unknown State')
        source = show_data.get('source', 'Unknown')
        rating = show_data.get('avg_rating', 0.0)
        
        # Format concert title: "YYYY/MM/DD [Venue Name]"
        # Convert YYYY-MM-DD to YYYY/MM/DD
        if date and date != 'Unknown Date':
            date_parts = date.split('-')
            if len(date_parts) == 3:
                formatted_date = f"{date_parts[0]}/{date_parts[1]}/{date_parts[2]}"
            else:
                formatted_date = date
        else:
            formatted_date = date
        
        self.concert_title = f"{formatted_date} {venue}"
        self.location = f"{city}, {state}"
        self.source_type = source
        self.rating = rating
        
        # Update labels
        self.title_label.setText(self.concert_title)
        self.location_label.setText(self.location)
        
        # Update badges
        self.source_badge.setText(source)
        
        # Rating badge with star
        if rating > 0:
            self.rating_badge.setText(f"[Star] {rating:.1f}/5.0")
            self.rating_badge.setVisible(True)
        else:
            self.rating_badge.setText("[Star] No rating")
            self.rating_badge.setVisible(True)
        
        # Track count will be updated separately via set_track_count()
        
        print(f"[INFO] Loaded concert info: {self.concert_title}")
    
    def set_track_count(self, count):
        """
        Update track count badge
        
        Args:
            count (int): Number of tracks in concert
        """
        self.track_count = count
        
        if count == 1:
            self.count_badge.setText("1 track")
        else:
            self.count_badge.setText(f"{count} tracks")
        
        self.count_badge.setVisible(count > 0)
    
    def clear(self):
        """Clear concert info (reset to empty state)"""
        self.concert_title = ""
        self.location = ""
        self.source_type = ""
        self.rating = 0.0
        self.track_count = 0
        self.is_favorite = False
        
        self.title_label.setText("No concert loaded")
        self.location_label.setText("")
        self.source_badge.setText("")
        self.source_badge.setVisible(False)
        self.rating_badge.setText("")
        self.rating_badge.setVisible(False)
        self.count_badge.setText("")
        self.count_badge.setVisible(False)
        
        # Reset favorite button
        self.update_favorite_button()
    
    def on_favorite_clicked(self):
        """Handle favorite button click (deferred to Phase 12)"""
        # Toggle favorite state
        self.is_favorite = not self.is_favorite
        
        # Update button appearance
        self.update_favorite_button()
        
        # Emit signal
        self.favorite_toggled.emit(self.is_favorite)
        
        print(f"[INFO] Favorite toggled: {self.is_favorite}")
    
    def update_favorite_button(self):
        """Update favorite button appearance based on state"""
        if self.is_favorite:
            # Favorited - red heart
            self.favorite_button.setStyleSheet("""
                QPushButton {
                    background-color: #DC2626;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 25px;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background-color: #EF4444;
                }
                QPushButton:pressed {
                    background-color: #B91C1C;
                }
            """)
        else:
            # Not favorited - gray heart
            self.favorite_button.setStyleSheet("""
                QPushButton {
                    background-color: #374151;
                    color: #9CA3AF;
                    border: none;
                    border-radius: 25px;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background-color: #4B5563;
                }
                QPushButton:pressed {
                    background-color: #1F2937;
                }
            """)


# Test code
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    
    # Create test window
    window = QMainWindow()
    window.setWindowTitle("Concert Info Widget Test")
    window.setGeometry(100, 100, 640, 300)
    
    # Create widget
    widget = ConcertInfoWidget()
    
    # Load test data
    test_show = {
        'date': '1977-05-08',
        'venue': 'Barton Hall, Cornell University',
        'city': 'Ithaca',
        'state': 'NY',
        'source': 'Soundboard',
        'avg_rating': 4.8,
        'num_reviews': 234
    }
    
    widget.load_concert_info(test_show)
    widget.set_track_count(20)
    
    # Connect signal
    widget.favorite_toggled.connect(
        lambda favorited: print(f"[TEST] Favorite toggled: {favorited}")
    )
    
    # Set as central widget
    window.setCentralWidget(widget)
    window.show()
    
    print("\n" + "="*60)
    print("Concert Info Widget Test")
    print("="*60)
    print("\nTest concert loaded:")
    print(f"  Title:    {widget.concert_title}")
    print(f"  Location: {widget.location}")
    print(f"  Source:   {widget.source_type}")
    print(f"  Rating:   {widget.rating:.1f}/5.0")
    print(f"  Tracks:   {widget.track_count}")
    print("\nTry clicking the favorite button!")
    print("(Note: Button disabled for Phase 10, will enable in Phase 12)")
    print("="*60 + "\n")
    
    sys.exit(app.exec_())
