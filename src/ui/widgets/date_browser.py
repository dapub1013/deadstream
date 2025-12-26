#!/usr/bin/env python3
"""
Date browser widget for DeadStream UI.
Provides calendar-style navigation to find shows by date.

Phase 7, Task 7.2: Implement date browser
"""
import sys
import os
from datetime import datetime, timedelta
from calendar import monthrange

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGridLayout, QScrollArea, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QPalette, QColor

from src.database.queries import get_shows_by_month, get_show_dates_for_year


class DateBrowser(QWidget):
    """
    Calendar-style date browser widget.
    Allows users to navigate by month/year and select dates with shows.
    
    Signals:
        date_selected(str): Emitted when user selects a date (format: YYYY-MM-DD)
    """
    
    # Signals
    date_selected = pyqtSignal(str)  # date in YYYY-MM-DD format
    
    def __init__(self):
        """Initialize the date browser"""
        super().__init__()
        
        # Current viewing date (not selected date)
        self.current_date = datetime.now()
        
        # Store dates that have shows (will be populated)
        self.show_dates = set()
        
        self.init_ui()
        self.load_show_dates()
        self.update_calendar()
    
    def init_ui(self):
        """Set up the date browser UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Month/Year header with navigation
        header_layout = QHBoxLayout()
        
        # Previous month button
        self.prev_month_btn = QPushButton("<")
        self.prev_month_btn.setMinimumSize(50, 50)
        self.prev_month_btn.setFont(QFont("Arial", 18, QFont.Bold))
        self.prev_month_btn.clicked.connect(self.previous_month)
        header_layout.addWidget(self.prev_month_btn)
        
        # Month/Year label (center)
        self.month_year_label = QLabel()
        self.month_year_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.month_year_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.month_year_label, 1)
        
        # Next month button
        self.next_month_btn = QPushButton(">")
        self.next_month_btn.setMinimumSize(50, 50)
        self.next_month_btn.setFont(QFont("Arial", 18, QFont.Bold))
        self.next_month_btn.clicked.connect(self.next_month)
        header_layout.addWidget(self.next_month_btn)
        
        layout.addLayout(header_layout)
        
        # Today button
        today_btn = QPushButton("Today")
        today_btn.setMinimumHeight(40)
        today_btn.clicked.connect(self.go_to_today)
        layout.addWidget(today_btn)
        
        # Weekday headers
        weekday_layout = QHBoxLayout()
        weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for day in weekdays:
            label = QLabel(day)
            label.setFont(QFont("Arial", 12, QFont.Bold))
            label.setAlignment(Qt.AlignCenter)
            weekday_layout.addWidget(label)
        layout.addLayout(weekday_layout)
        
        # Calendar grid (7 columns x 6 rows max)
        self.calendar_grid = QGridLayout()
        self.calendar_grid.setSpacing(5)
        
        # Create 42 day buttons (6 weeks max)
        self.day_buttons = []
        for row in range(6):
            for col in range(7):
                btn = QPushButton()
                btn.setMinimumSize(60, 60)
                btn.setFont(QFont("Arial", 14))
                btn.clicked.connect(lambda checked, b=btn: self.day_clicked(b))
                self.calendar_grid.addWidget(btn, row, col)
                self.day_buttons.append(btn)
        
        layout.addLayout(self.calendar_grid)
        
        # Info label
        self.info_label = QLabel("Select a date to see shows")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Apply styling
        self.apply_styling()
        
        print("[INFO] DateBrowser widget initialized")
    
    def apply_styling(self):
        """Apply visual styling to the date browser"""
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
        self.prev_month_btn.setStyleSheet(nav_style)
        self.next_month_btn.setStyleSheet(nav_style)
        
        # Style the today button
        today_style = """
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """
        # Find and style the today button
        for widget in self.findChildren(QPushButton):
            if widget.text() == "Today":
                widget.setStyleSheet(today_style)
    
    def load_show_dates(self):
        """Load all dates that have shows from the database"""
        try:
            # Get all show dates for current year
            year = self.current_date.year
            dates = get_show_dates_for_year(year)
            
            # Convert to set of date strings (YYYY-MM-DD)
            self.show_dates = set(dates)
            
            print(f"[INFO] Loaded {len(self.show_dates)} show dates for {year}")
        except Exception as e:
            print(f"[ERROR] Failed to load show dates: {e}")
            self.show_dates = set()
    
    def update_calendar(self):
        """Update the calendar display for current month"""
        year = self.current_date.year
        month = self.current_date.month
        
        # Update header label
        month_name = self.current_date.strftime("%B %Y")
        self.month_year_label.setText(month_name)
        
        # Get first day of month and number of days
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()  # 0 = Monday, 6 = Sunday
        # Convert to Sunday = 0 format
        first_weekday = (first_weekday + 1) % 7
        
        num_days = monthrange(year, month)[1]
        
        # Get shows for this month
        try:
            month_shows = get_shows_by_month(year, month)
            show_days = set(int(show['date'].split('-')[2]) for show in month_shows)
        except Exception as e:
            print(f"[WARN] Could not load shows for {year}-{month}: {e}")
            show_days = set()
        
        # Update all day buttons
        day_num = 1
        for i, btn in enumerate(self.day_buttons):
            # Clear button
            btn.setText("")
            btn.setEnabled(False)
            
            # If this position is within the month
            if i >= first_weekday and day_num <= num_days:
                btn.setText(str(day_num))
                btn.setEnabled(True)
                
                # Store the date in the button
                date_str = f"{year:04d}-{month:02d}-{day_num:02d}"
                btn.setProperty("date", date_str)
                
                # Style based on whether there are shows
                if day_num in show_days:
                    # Date has shows - make it prominent
                    btn.setStyleSheet("""
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
                    """)
                else:
                    # No shows - subtle style
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #374151;
                            color: #9ca3af;
                            border: none;
                            border-radius: 8px;
                        }
                        QPushButton:hover {
                            background-color: #4b5563;
                        }
                    """)
                
                # Highlight today
                today = datetime.now()
                if year == today.year and month == today.month and day_num == today.day:
                    btn.setStyleSheet(btn.styleSheet() + """
                        QPushButton {
                            border: 3px solid #10b981;
                        }
                    """)
                
                day_num += 1
            else:
                # Outside current month - hide button
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: none;
                    }
                """)
        
        # Update info label
        if show_days:
            self.info_label.setText(f"{len(show_days)} date(s) with shows this month")
        else:
            self.info_label.setText("No shows this month")
    
    def day_clicked(self, button):
        """Handle day button click"""
        date_str = button.property("date")
        if date_str:
            print(f"[INFO] Date selected: {date_str}")
            self.date_selected.emit(date_str)
    
    def previous_month(self):
        """Navigate to previous month"""
        # Go back one month
        if self.current_date.month == 1:
            self.current_date = datetime(self.current_date.year - 1, 12, 1)
        else:
            self.current_date = datetime(self.current_date.year, self.current_date.month - 1, 1)
        
        # Reload show dates if year changed
        self.load_show_dates()
        self.update_calendar()
        print(f"[INFO] Navigated to {self.current_date.strftime('%B %Y')}")
    
    def next_month(self):
        """Navigate to next month"""
        # Go forward one month
        if self.current_date.month == 12:
            self.current_date = datetime(self.current_date.year + 1, 1, 1)
        else:
            self.current_date = datetime(self.current_date.year, self.current_date.month + 1, 1)
        
        # Reload show dates if year changed
        self.load_show_dates()
        self.update_calendar()
        print(f"[INFO] Navigated to {self.current_date.strftime('%B %Y')}")
    
    def go_to_today(self):
        """Jump to current month"""
        self.current_date = datetime.now()
        self.load_show_dates()
        self.update_calendar()
        print("[INFO] Navigated to today")
    
    def go_to_date(self, year, month):
        """
        Navigate to a specific month/year
        
        Args:
            year: Year to navigate to
            month: Month to navigate to (1-12)
        """
        self.current_date = datetime(year, month, 1)
        self.load_show_dates()
        self.update_calendar()
        print(f"[INFO] Navigated to {year}-{month:02d}")
