#!/usr/bin/env python3
"""
Year browser widget for DeadStream UI.
Provides grid-based navigation to find shows by year with legendary years highlighted.

Phase 7, Task 7.4: Implement year selector
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGridLayout, QScrollArea, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

from src.database.queries import get_years_with_shows, get_show_count_by_year


class YearBrowser(QWidget):
    """
    Grid-based year browser widget.
    Allows users to navigate by decade and select years with shows.
    Highlights legendary years (1972, 1977, 1989, 1990, etc.)
    
    Signals:
        year_selected(int): Emitted when user selects a year
    """
    
    # Signals
    year_selected = pyqtSignal(int)  # year as integer
    
    # Legendary years (iconic eras in Dead history)
    LEGENDARY_YEARS = {
        1968, 1969,  # Early psychedelic era
        1972, 1973, 1974,  # Peak improvisational years
        1977,  # The year - widely considered peak Dead
        1989, 1990,  # Brent era renaissance
    }
    
    def __init__(self):
        """Initialize the year browser"""
        super().__init__()
        
        # Store years that have shows
        self.years_with_shows = set()
        self.year_counts = {}
        
        # Current decade being displayed
        self.current_decade = 1970
        
        self.init_ui()
        self.load_year_data()
        self.update_year_grid()
    
    def init_ui(self):
        """Set up the year browser UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Decade navigation header
        header_layout = QHBoxLayout()
        
        # Previous decade button
        self.prev_decade_btn = QPushButton("< Previous")
        self.prev_decade_btn.setMinimumSize(120, 50)
        self.prev_decade_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.prev_decade_btn.clicked.connect(self.previous_decade)
        header_layout.addWidget(self.prev_decade_btn)
        
        # Decade label (center)
        self.decade_label = QLabel()
        self.decade_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.decade_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.decade_label, 1)
        
        # Next decade button
        self.next_decade_btn = QPushButton("Next >")
        self.next_decade_btn.setMinimumSize(120, 50)
        self.next_decade_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.next_decade_btn.clicked.connect(self.next_decade)
        header_layout.addWidget(self.next_decade_btn)
        
        layout.addLayout(header_layout)

        # Year grid (2 columns x 5 rows = 10 years per decade)
        self.year_grid = QGridLayout()
        self.year_grid.setSpacing(10)
        
        # Create 10 year buttons (one decade)
        self.year_buttons = []
        for row in range(5):
            for col in range(2):
                btn = QPushButton()
                btn.setMinimumSize(180, 80)
                btn.setFont(QFont("Arial", 32, QFont.Bold))  # Larger font for year
                btn.clicked.connect(lambda checked, b=btn: self.year_clicked(b))
                self.year_grid.addWidget(btn, row, col)
                self.year_buttons.append(btn)
        
        layout.addLayout(self.year_grid)

        # Info label
        self.info_label = QLabel("Select a year to see all shows")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont("Arial", 12))
        self.info_label.setStyleSheet("color: #d1d5db;")
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Apply styling
        self.apply_styling()
        
        print("[INFO] YearBrowser widget initialized")
    
    def apply_styling(self):
        """Apply visual styling to the year browser"""
        # Style the navigation buttons
        nav_style = """
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """
        self.prev_decade_btn.setStyleSheet(nav_style)
        self.next_decade_btn.setStyleSheet(nav_style)

        # Decade label styling
        self.decade_label.setStyleSheet("color: white;")
    
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
        """Update the year grid buttons for current decade"""
        # Update decade label
        decade_end = self.current_decade + 9
        self.decade_label.setText(f"{self.current_decade}s ({self.current_decade}-{decade_end})")
        
        # Update each year button
        for i, btn in enumerate(self.year_buttons):
            year = self.current_decade + i
            
            # Check if this year has shows
            has_shows = year in self.years_with_shows
            is_legendary = year in self.LEGENDARY_YEARS
            show_count = self.year_counts.get(year, 0)
            
            if has_shows:
                # Show only the year (no stars, no show count)
                btn.setText(f"{year}")

                # Enabled style - different colors for legendary vs regular
                if is_legendary:
                    # Gold/amber for legendary years
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #f59e0b;
                            color: #000000;
                            border: 3px solid #fbbf24;
                            border-radius: 10px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #fbbf24;
                            border-color: #fcd34d;
                        }
                        QPushButton:pressed {
                            background-color: #d97706;
                        }
                    """)
                else:
                    # Blue for regular years with shows
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #3b82f6;
                            color: white;
                            border: 2px solid #60a5fa;
                            border-radius: 10px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #60a5fa;
                        }
                        QPushButton:pressed {
                            background-color: #2563eb;
                        }
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
        
        min_decade = (min_year // 10) * 10
        max_decade = (max_year // 10) * 10
        
        # Disable prev if at earliest decade
        self.prev_decade_btn.setEnabled(self.current_decade > min_decade)
        
        # Disable next if at latest decade
        self.next_decade_btn.setEnabled(self.current_decade < max_decade)
    
    def previous_decade(self):
        """Navigate to previous decade"""
        self.current_decade -= 10
        self.update_year_grid()
        print(f"[INFO] Navigated to {self.current_decade}s")
    
    def next_decade(self):
        """Navigate to next decade"""
        self.current_decade += 10
        self.update_year_grid()
        print(f"[INFO] Navigated to {self.current_decade}s")

    def year_clicked(self, button):
        """Handle year button click"""
        year = button.property('year')
        
        if year is not None:
            show_count = self.year_counts.get(year, 0)
            print(f"[OK] Year {year} selected ({show_count} shows)")
            
            # Update info label
            self.info_label.setText(f"Selected: {year} ({show_count} shows)")
            
            # Emit signal
            self.year_selected.emit(year)


# Test code
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    
    # Apply dark theme
    app.setStyleSheet("""
        QWidget {
            background-color: #111827;
            color: #f3f4f6;
        }
    """)
    
    window = QMainWindow()
    window.setWindowTitle("Year Browser Test")
    window.setGeometry(100, 100, 800, 700)
    
    year_browser = YearBrowser()
    
    # Connect signal to test
    def on_year_selected(year):
        print(f"[TEST] Year selected signal received: {year}")
    
    year_browser.year_selected.connect(on_year_selected)
    
    window.setCentralWidget(year_browser)
    window.show()
    
    sys.exit(app.exec_())
