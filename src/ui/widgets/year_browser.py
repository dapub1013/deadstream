#!/usr/bin/env python3
"""
Year Browser Widget for DeadStream
Task 7.4: Create year selector

Allows users to browse shows by decade and year with expandable sections.
Matches UI design specification for "Browse by Year" mode.

Features:
- Legendary Years section (top 5 iconic years)
- Browse by Decade (expandable decade headers with year lists)
- Purple theme (matching UI spec)
- Only one decade expanded at a time
- Scroll position maintained when expanding/collapsing
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from src.database.queries import (
    search_by_year,
    get_show_count,
    search_by_date_range
)


class YearBrowser(QWidget):
    """
    Widget for browsing shows by year
    
    Layout:
    1. Header with title and description
    2. Legendary Years section (top 5)
    3. Browse by Decade section (expandable)
    
    Signals:
    - year_selected: Emitted when user selects a year (int)
    """
    
    year_selected = pyqtSignal(int)  # Emits year number
    
    # Legendary years with special notes
    LEGENDARY_YEARS = [
        (1977, "The peak! Peak Dead with peak Keith"),
        (1972, "Europe '72 tour - legendary"),
        (1969, "Primal Dead - raw power"),
        (1973, "Sublime jams and experimentation"),
        (1974, "Wall of Sound era")
    ]
    
    # Decade definitions (start_year, end_year, label)
    DECADES = [
        (1990, 1995, "1990s"),
        (1980, 1989, "1980s"),
        (1970, 1979, "1970s"),
        (1965, 1969, "1960s")
    ]
    
    def __init__(self, parent=None):
        """Initialize year browser"""
        super().__init__(parent)
        self.expanded_decade = None  # Track which decade is expanded
        self.decade_widgets = {}     # Store decade widget references
        self.setup_ui()
    
    def setup_ui(self):
        """Create the year browser layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #111827;
            }
        """)
        
        # Content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Section 1: Legendary Years
        legendary_section = self.create_legendary_years_section()
        content_layout.addWidget(legendary_section)
        
        # Section 2: Browse by Decade
        decades_section = self.create_decades_section()
        content_layout.addWidget(decades_section)
        
        # Add stretch at bottom
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def create_header(self):
        """Create header with title and subtitle"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-bottom: 1px solid #374151;
            }
        """)
        
        layout = QVBoxLayout(header)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title with clock icon (using text)
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        icon_label = QLabel("[CLOCK]")
        icon_label.setStyleSheet("color: #a78bfa; font-size: 20px; font-weight: bold;")
        title_layout.addWidget(icon_label)
        
        title = QLabel("Browse by Year")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # Subtitle
        subtitle = QLabel("Legendary years and shows organized by decade")
        subtitle.setStyleSheet("color: #9ca3af; font-size: 14px; margin-top: 5px;")
        layout.addWidget(subtitle)
        
        return header
    
    def create_legendary_years_section(self):
        """Create the legendary years section"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Section header
        header = QLabel("[STAR] Legendary Years")
        header.setStyleSheet("""
            color: #fbbf24;
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 10px;
            background-color: #1f2937;
            border-radius: 8px 8px 0 0;
        """)
        layout.addWidget(header)
        
        # Create card for each legendary year
        for year, note in self.LEGENDARY_YEARS:
            year_card = self.create_legendary_year_card(year, note)
            layout.addWidget(year_card)
        
        return section
    
    def create_legendary_year_card(self, year, note):
        """Create a card for a legendary year"""
        card = QFrame()
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
                padding: 15px;
            }
            QFrame:hover {
                background-color: #374151;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # Year and show count
        top_row = QHBoxLayout()
        
        year_label = QLabel(str(year))
        year_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        top_row.addWidget(year_label)
        
        top_row.addStretch()
        
        # Get show count for this year
        try:
            shows = search_by_year(year)
            show_count = len(shows)
            count_label = QLabel(f"{show_count} shows")
            count_label.setStyleSheet("color: #9ca3af; font-size: 14px;")
            top_row.addWidget(count_label)
        except Exception as e:
            print(f"[ERROR] Failed to get show count for {year}: {e}")
        
        layout.addLayout(top_row)
        
        # Special note
        note_label = QLabel(note)
        note_label.setStyleSheet("color: #a78bfa; font-size: 14px; font-style: italic;")
        layout.addWidget(note_label)
        
        # Browse button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        browse_btn = QPushButton(f"Browse {year} ->")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #7c3aed;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6d28d9;
            }
        """)
        browse_btn.clicked.connect(lambda: self.select_year(year))
        btn_layout.addWidget(browse_btn)
        
        layout.addLayout(btn_layout)
        
        return card
    
    def create_decades_section(self):
        """Create the browse by decade section with expandable headers"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Section header
        header = QLabel("[CALENDAR] By Decade")
        header.setStyleSheet("""
            color: #fbbf24;
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 10px;
            background-color: #1f2937;
            border-radius: 8px 8px 0 0;
        """)
        layout.addWidget(header)
        
        # Create expandable decade headers
        for start_year, end_year, label in self.DECADES:
            decade_widget = self.create_decade_widget(start_year, end_year, label)
            self.decade_widgets[label] = decade_widget
            layout.addWidget(decade_widget)
        
        return section
    
    def create_decade_widget(self, start_year, end_year, label):
        """Create an expandable decade widget"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Decade header (clickable)
        header = self.create_decade_header(start_year, end_year, label)
        layout.addWidget(header)
        
        # Year list (initially hidden)
        year_list = self.create_year_list(start_year, end_year)
        year_list.setVisible(False)
        year_list.setProperty('decade_label', label)
        layout.addWidget(year_list)
        
        # Store references
        container.setProperty('header', header)
        container.setProperty('year_list', year_list)
        container.setProperty('decade_label', label)
        
        return container
    
    def create_decade_header(self, start_year, end_year, label):
        """Create clickable decade header"""
        header = QFrame()
        header.setCursor(Qt.PointingHandCursor)
        header.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
                padding: 15px;
            }
            QFrame:hover {
                background-color: #374151;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Chevron icon (will rotate when expanded)
        chevron = QLabel(">")
        chevron.setStyleSheet("color: #a78bfa; font-size: 18px; font-weight: bold;")
        chevron.setProperty('is_expanded', False)
        layout.addWidget(chevron)
        
        # Decade label
        decade_label = QLabel(label)
        decade_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(decade_label)
        
        layout.addStretch()
        
        # Show count for decade
        try:
            start_date = f"{start_year}-01-01"
            end_date = f"{end_year}-12-31"
            shows = search_by_date_range(start_date, end_date)
            count_label = QLabel(f"{len(shows)} shows")
            count_label.setStyleSheet("color: #9ca3af; font-size: 14px;")
            layout.addWidget(count_label)
        except Exception as e:
            print(f"[ERROR] Failed to get show count for {label}: {e}")
        
        # Store decade info
        header.setProperty('decade_label', label)
        header.setProperty('chevron', chevron)
        
        # Make clickable
        header.mousePressEvent = lambda e: self.toggle_decade(label)
        
        return header
    
    def create_year_list(self, start_year, end_year):
        """Create list of years in a decade"""
        year_list = QFrame()
        year_list.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border-radius: 0 0 8px 8px;
            }
        """)
        
        layout = QVBoxLayout(year_list)
        layout.setContentsMargins(40, 10, 15, 15)
        layout.setSpacing(8)
        
        # Create year button for each year
        for year in range(end_year, start_year - 1, -1):
            year_btn = self.create_year_button(year)
            layout.addWidget(year_btn)
        
        return year_list
    
    def create_year_button(self, year):
        """Create a button for a specific year"""
        btn_frame = QFrame()
        btn_frame.setCursor(Qt.PointingHandCursor)
        btn_frame.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 6px;
                padding: 10px;
            }
            QFrame:hover {
                background-color: #374151;
            }
        """)
        
        layout = QHBoxLayout(btn_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Year
        year_label = QLabel(str(year))
        year_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(year_label)
        
        layout.addStretch()
        
        # Show count
        try:
            shows = search_by_year(year)
            count_label = QLabel(f"{len(shows)} shows")
            count_label.setStyleSheet("color: #9ca3af; font-size: 14px;")
            layout.addWidget(count_label)
        except Exception as e:
            print(f"[ERROR] Failed to get show count for {year}: {e}")
        
        # Browse arrow
        arrow = QLabel("->")
        arrow.setStyleSheet("color: #a78bfa; font-size: 16px; font-weight: bold; margin-left: 10px;")
        layout.addWidget(arrow)
        
        # Make clickable
        btn_frame.mousePressEvent = lambda e: self.select_year(year)
        
        return btn_frame
    
    def toggle_decade(self, decade_label):
        """Toggle decade expansion (only one at a time)"""
        try:
            decade_widget = self.decade_widgets.get(decade_label)
            if not decade_widget:
                return
            
            header = decade_widget.property('header')
            year_list = decade_widget.property('year_list')
            chevron = header.property('chevron')
            
            # Check if this decade is already expanded
            is_currently_expanded = year_list.isVisible()
            
            # Collapse all decades first
            for label, widget in self.decade_widgets.items():
                widget_header = widget.property('header')
                widget_year_list = widget.property('year_list')
                widget_chevron = widget_header.property('chevron')
                
                widget_year_list.setVisible(False)
                widget_chevron.setText(">")
                widget_chevron.setProperty('is_expanded', False)
            
            # If this decade wasn't expanded, expand it now
            if not is_currently_expanded:
                year_list.setVisible(True)
                chevron.setText("v")
                chevron.setProperty('is_expanded', True)
                self.expanded_decade = decade_label
                print(f"[INFO] Expanded decade: {decade_label}")
            else:
                self.expanded_decade = None
                print(f"[INFO] Collapsed decade: {decade_label}")
                
        except Exception as e:
            print(f"[ERROR] Failed to toggle decade {decade_label}: {e}")
    
    def select_year(self, year):
        """Emit signal when year is selected"""
        print(f"[INFO] Year selected: {year}")
        self.year_selected.emit(year)


# Test the widget
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create test window
    browser = YearBrowser()
    browser.setGeometry(100, 100, 800, 600)
    browser.setWindowTitle("Year Browser Test")
    
    # Connect signal
    browser.year_selected.connect(lambda y: print(f"[SIGNAL] Year selected: {y}"))
    
    browser.show()
    
    sys.exit(app.exec_())
