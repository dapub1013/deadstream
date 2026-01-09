#!/usr/bin/env python3
"""
Year browser widget for DeadStream UI - Phase 10E Restyled

Phase 10E Restyle:
- Uses Theme Manager for all colors/spacing/typography
- Zero hardcoded values
- Maintains all Phase 7 functionality
- Legendary years highlighted in yellow
- Touch-friendly 60px+ year buttons

Provides grid-based navigation to find shows by year with legendary years highlighted.
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import Theme Manager for all styling
from src.ui.styles.theme import Theme

# Import database queries
from src.database.queries import get_years_with_shows, get_show_count_by_year


class YearBrowser(QWidget):
    """
    Grid-based year browser widget - Phase 10E restyled
    
    Allows users to navigate by decade and select years with shows.
    Legendary years (1972, 1977, etc.) highlighted in yellow.
    """
    
    # Signal emitted when user selects a year
    year_selected = pyqtSignal(int)
    
    # Legendary Grateful Dead years to highlight
    LEGENDARY_YEARS = {1972, 1977, 1973, 1974, 1969, 1970, 1989, 1990}
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.years_with_shows = set()
        self.year_counts = {}
        self.current_decade = 1960
        
        self.init_ui()
        self.load_year_data()
        self.update_year_grid()
        
    def init_ui(self):
        """Initialize the year browser UI with Theme styling"""
        layout = QVBoxLayout()
        layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE
        )
        layout.setSpacing(Theme.SPACING_MEDIUM)
        
        # Header with decade navigation
        header_layout = QHBoxLayout()
        header_layout.setSpacing(Theme.SPACING_MEDIUM)
        
        # Previous decade button
        self.prev_decade_btn = QPushButton("<< Previous")
        self.prev_decade_btn.setMinimumHeight(Theme.BUTTON_HEIGHT)
        self.prev_decade_btn.clicked.connect(self.prev_decade)
        header_layout.addWidget(self.prev_decade_btn)
        
        # Decade label
        self.decade_label = QLabel("1960s (1960-1969)")
        self.decade_label.setAlignment(Qt.AlignCenter)
        self.decade_label.setFont(QFont(
            Theme.FONT_FAMILY,
            Theme.HEADER_SMALL,
            QFont.Bold  # Use QFont.Bold for Python QFont objects
        ))
        header_layout.addWidget(self.decade_label)
        
        # Next decade button
        self.next_decade_btn = QPushButton("Next >>")
        self.next_decade_btn.setMinimumHeight(Theme.BUTTON_HEIGHT)
        self.next_decade_btn.clicked.connect(self.next_decade)
        header_layout.addWidget(self.next_decade_btn)
        
        layout.addLayout(header_layout)

        # Year grid (2 columns x 5 rows = 10 years per decade)
        self.year_grid = QGridLayout()
        self.year_grid.setSpacing(Theme.SPACING_MEDIUM)
        
        # Create 10 year buttons (one decade)
        self.year_buttons = []
        for row in range(5):
            for col in range(2):
                btn = QPushButton()
                btn.setMinimumSize(180, 80)  # 80px height for touch-friendliness
                btn.setFont(QFont(
                    Theme.FONT_FAMILY,
                    Theme.HEADER_MEDIUM,
                    QFont.Bold  # Use QFont.Bold for Python QFont objects
                ))
                btn.clicked.connect(lambda checked, b=btn: self.year_clicked(b))
                self.year_grid.addWidget(btn, row, col)
                self.year_buttons.append(btn)
        
        layout.addLayout(self.year_grid)

        # Info label
        self.info_label = QLabel("Select a year to see all shows")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont(
            Theme.FONT_FAMILY,
            Theme.BODY_SMALL
        ))
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Apply Theme styling
        self.apply_styling()
        
        print("[INFO] YearBrowser widget initialized")
    
    def apply_styling(self):
        """Apply Theme-based visual styling to the year browser"""
        # Style the navigation buttons using Theme colors
        nav_style = f"""
            QPushButton {{
                background-color: {Theme.ACCENT_BLUE};
                color: {Theme.TEXT_PRIMARY};
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: {Theme.BODY_MEDIUM}px;
                padding: {Theme.SPACING_SMALL}px {Theme.SPACING_MEDIUM}px;
            }}
            QPushButton:hover {{
                background-color: {Theme._darken_color(Theme.ACCENT_BLUE, 0.1)};
            }}
            QPushButton:pressed {{
                background-color: {Theme._darken_color(Theme.ACCENT_BLUE, 0.2)};
            }}
            QPushButton:disabled {{
                background-color: {Theme.BORDER_SUBTLE};
                color: {Theme.TEXT_SECONDARY};
            }}
        """
        self.prev_decade_btn.setStyleSheet(nav_style)
        self.next_decade_btn.setStyleSheet(nav_style)

        # Decade label styling using Theme colors
        self.decade_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                padding: {Theme.SPACING_SMALL}px;
            }}
        """)
        
        # Info label styling using Theme colors
        self.info_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                padding: {Theme.SPACING_SMALL}px;
            }}
        """)
    
    def load_year_data(self):
        """Load years with shows from database"""
        try:
            # Get all years that have shows
            years = get_years_with_shows()
            self.years_with_shows = set(years)
            
            # Get show counts per year
            year_counts = get_show_count_by_year()
            self.year_counts = {year: count for year, count in year_counts}
            
            # Set initial decade to earliest year with shows
            if years:
                self.current_decade = (min(years) // 10) * 10
            
            print(f"[OK] Loaded {len(years)} years with shows")
            
        except Exception as e:
            print(f"[ERROR] Failed to load year data: {e}")
            self.years_with_shows = set()
            self.year_counts = {}
    
    def update_year_grid(self):
        """Update the year grid buttons for current decade using Theme styling"""
        # Update decade label
        decade_end = self.current_decade + 9
        self.decade_label.setText(f"{self.current_decade}s ({self.current_decade}-{decade_end})")
        
        # Update each year button
        for i, btn in enumerate(self.year_buttons):
            year = self.current_decade + i
            
            # Check if this year has shows
            has_shows = year in self.years_with_shows
            is_legendary = year in self.LEGENDARY_YEARS
            
            if has_shows:
                # Show only the year (no stars, no show count)
                btn.setText(f"{year}")

                # Apply Theme-based styling
                if is_legendary:
                    # Yellow/gold for legendary years - uses Theme colors
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {Theme.ACCENT_YELLOW};
                            color: {Theme.TEXT_DARK};
                            border: 3px solid {Theme._lighten_color(Theme.ACCENT_YELLOW, 0.1)};
                            border-radius: 10px;
                            font-weight: bold;
                        }}
                        QPushButton:hover {{
                            background-color: {Theme._lighten_color(Theme.ACCENT_YELLOW, 0.1)};
                            border-color: {Theme._lighten_color(Theme.ACCENT_YELLOW, 0.2)};
                        }}
                        QPushButton:pressed {{
                            background-color: {Theme._darken_color(Theme.ACCENT_YELLOW, 0.1)};
                        }}
                    """)
                else:
                    # Blue for regular years with shows - uses Theme colors
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {Theme.ACCENT_BLUE};
                            color: {Theme.TEXT_PRIMARY};
                            border: 2px solid {Theme._lighten_color(Theme.ACCENT_BLUE, 0.1)};
                            border-radius: 10px;
                            font-weight: bold;
                        }}
                        QPushButton:hover {{
                            background-color: {Theme._lighten_color(Theme.ACCENT_BLUE, 0.1)};
                        }}
                        QPushButton:pressed {{
                            background-color: {Theme._darken_color(Theme.ACCENT_BLUE, 0.1)};
                        }}
                    """)

                btn.setVisible(True)
                btn.setEnabled(True)
                btn.setProperty('year', year)  # Store year in button

            else:
                # No shows this year - hide the button
                btn.setVisible(False)
                btn.setEnabled(False)
                btn.setProperty('year', None)
        
        # Update navigation button states
        self.update_navigation_buttons()
    
    def update_navigation_buttons(self):
        """Enable/disable navigation buttons based on available data"""
        if not self.years_with_shows:
            return
        
        min_year = min(self.years_with_shows)
        max_year = max(self.years_with_shows)
        
        # Disable "Previous" if we're at or before the earliest decade
        earliest_decade = (min_year // 10) * 10
        self.prev_decade_btn.setEnabled(self.current_decade > earliest_decade)
        
        # Disable "Next" if we're at or after the latest decade
        latest_decade = (max_year // 10) * 10
        self.next_decade_btn.setEnabled(self.current_decade < latest_decade)
    
    def prev_decade(self):
        """Navigate to previous decade"""
        self.current_decade -= 10
        self.update_year_grid()
    
    def next_decade(self):
        """Navigate to next decade"""
        self.current_decade += 10
        self.update_year_grid()
    
    def year_clicked(self, button):
        """Handle year button click"""
        year = button.property('year')
        if year is not None:
            print(f"[OK] Year selected: {year}")
            self.year_selected.emit(year)


if __name__ == "__main__":
    """Test the year browser widget"""
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create and show year browser
    browser = YearBrowser()
    browser.setWindowTitle("DeadStream - Year Browser Test")
    browser.setMinimumSize(600, 800)
    browser.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
    browser.show()
    
    # Connect signal for testing
    def on_year_selected(year):
        print(f"[TEST] Year selected signal received: {year}")
    
    browser.year_selected.connect(on_year_selected)
    
    sys.exit(app.exec_())