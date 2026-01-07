"""
Test script for ConcertListItem component.

Displays a scrollable list of concert items with:
- Various dates, venues, and locations
- Different ratings and source types
- Interactive hover and click states
- Scrollable list view
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QScrollArea,
    QLabel
)
from PyQt5.QtCore import Qt
from src.ui.styles.theme import Theme
from src.ui.components.concert_list_item import ConcertListItem


class ConcertListDemo(QWidget):
    """Demo window showing ConcertListItem in a scrollable list."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("ConcertListItem Component Test")
        self.resize(700, 800)
        
        # Apply global theme
        self.setStyleSheet(Theme.get_global_stylesheet())
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(Theme.SPACING_LARGE)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Scroll area for concert list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {Theme.BG_PRIMARY};
            }}
        """)
        
        # Container for concert items
        list_container = QWidget()
        list_layout = QVBoxLayout()
        list_layout.setSpacing(Theme.LIST_ITEM_SPACING)
        list_layout.setContentsMargins(
            Theme.MARGIN_MEDIUM,
            Theme.MARGIN_SMALL,
            Theme.MARGIN_MEDIUM,
            Theme.MARGIN_MEDIUM
        )
        
        # Sample concert data
        concerts = self._get_sample_concerts()
        
        # Create concert list items
        for idx, concert in enumerate(concerts):
            # Show divider except for last item
            show_divider = (idx < len(concerts) - 1)
            
            item = ConcertListItem(concert, show_divider=show_divider)
            item.clicked.connect(self.on_concert_clicked)
            list_layout.addWidget(item)
        
        list_layout.addStretch()
        list_container.setLayout(list_layout)
        scroll_area.setWidget(list_container)
        
        main_layout.addWidget(scroll_area)
        
        # Status label
        self.status_label = QLabel("Click any concert to see details")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
                padding: {Theme.SPACING_MEDIUM}px;
                background-color: {Theme.BG_CARD};
            }}
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
    
    def _create_header(self):
        """Create header section."""
        header = QWidget()
        header.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme.BG_PANEL_DARK};
                padding: {Theme.SPACING_LARGE}px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_SMALL)
        
        # Title
        title = QLabel("ConcertListItem Component Demo")
        title.setStyleSheet(f"""
            font-size: {Theme.HEADER_MEDIUM}px;
            font-weight: {Theme.WEIGHT_BOLD};
            color: {Theme.TEXT_PRIMARY};
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Scrollable list with hover and click states")
        subtitle.setStyleSheet(f"""
            font-size: {Theme.BODY_LARGE}px;
            color: {Theme.TEXT_SECONDARY};
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        header.setLayout(layout)
        return header
    
    def _get_sample_concerts(self):
        """Get sample concert data for testing."""
        return [
            {
                'date': '1977-05-08',
                'venue': 'Barton Hall, Cornell University',
                'location': 'Ithaca, NY',
                'rating': 4.8,
                'source': 'SBD'
            },
            {
                'date': '1972-05-11',
                'venue': 'Olympia Theatre',
                'location': 'Paris, France',
                'rating': 4.5,
                'source': 'AUD'
            },
            {
                'date': '1974-05-19',
                'venue': 'Portland Memorial Coliseum',
                'location': 'Portland, OR',
                'rating': 4.3,
                'source': 'MTX'
            },
            {
                'date': '1973-11-10',
                'venue': 'Winterland Arena',
                'location': 'San Francisco, CA',
                'rating': 4.7,
                'source': 'SBD'
            },
            {
                'date': '1977-05-22',
                'venue': 'The Sportatorium',
                'location': 'Pembroke Pines, FL',
                'rating': 4.4,
                'source': 'AUD'
            },
            {
                'date': '1969-08-16',
                'venue': 'Woodstock Music & Art Fair',
                'location': 'Bethel, NY',
                'rating': 4.2,
                'source': 'SBD'
            },
            {
                'date': '1973-05-26',
                'venue': 'Kezar Stadium',
                'location': 'San Francisco, CA',
                'rating': 4.6,
                'source': 'MTX'
            },
            {
                'date': '1974-08-06',
                'venue': 'Roosevelt Stadium',
                'location': 'Jersey City, NJ',
                'rating': 4.5,
                'source': 'SBD'
            },
            {
                'date': '1972-09-27',
                'venue': 'Stanley Theatre',
                'location': 'Jersey City, NJ',
                'rating': 4.4,
                'source': 'AUD'
            },
            {
                'date': '1977-06-09',
                'venue': 'Winterland Arena',
                'location': 'San Francisco, CA',
                'rating': 4.8,
                'source': 'SBD'
            },
            {
                'date': '1973-12-02',
                'venue': 'Boston Music Hall',
                'location': 'Boston, MA',
                'rating': 4.3,
                'source': 'MTX'
            },
            {
                'date': '1971-08-06',
                'venue': 'Hollywood Palladium',
                'location': 'Los Angeles, CA',
                'rating': 4.1,
                'source': 'AUD'
            },
        ]
    
    def on_concert_clicked(self, show_data):
        """Handle concert item click."""
        date = show_data.get('date', 'Unknown')
        venue = show_data.get('venue', 'Unknown')
        rating = show_data.get('rating', 0.0)
        source = show_data.get('source', 'Unknown')
        
        self.status_label.setText(
            f"[INFO] Selected: {date} - {venue} | "
            f"Rating: {rating:.1f} | Source: {source}"
        )


def main():
    """Run the demo application."""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = app.font()
    font.setFamily(Theme.FONT_FAMILY)
    app.setFont(font)
    
    demo = ConcertListDemo()
    demo.show()
    
    print("\n" + "=" * 60)
    print("[INFO] ConcertListItem Component Demo")
    print("=" * 60)
    print("[INFO] Features demonstrated:")
    print("  - Scrollable concert list")
    print("  - Date, venue, and location display")
    print("  - Rating and source badges")
    print("  - Hover and click states")
    print("  - Touch-friendly 80px minimum height")
    print("\n[INFO] Interactions:")
    print("  - Hover over items to see highlight")
    print("  - Click items to see details in status bar")
    print("  - Scroll to see all 12 concerts")
    print("\n[INFO] Data displayed:")
    print("  - Concert date (bold, large)")
    print("  - Venue name (medium text)")
    print("  - Location (small, gray text)")
    print("  - Source badge (color-coded)")
    print("  - Rating badge (cyan with star)")
    print("\n[INFO] Press Ctrl+C or close window to exit")
    print("=" * 60 + "\n")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()