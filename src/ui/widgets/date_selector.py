#!/usr/bin/env python3
"""
Date selector widget with month/day/year columns for DeadStream UI.
Provides an intuitive touch-friendly interface for selecting show dates.
"""
import sys
import os
from datetime import datetime
from calendar import monthrange

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from src.database.queries import get_show_count_by_year, get_shows_by_month
from src.ui.styles.theme import Theme


class DateSelectorWidget(QWidget):
    """
    Three-column date selector: Month | Day | Year
    Displays available shows and allows intuitive date selection.

    Signals:
        date_selected(str): Emitted when user selects a complete date (format: YYYY-MM-DD)
    """

    date_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        """Initialize the date selector"""
        super().__init__(parent)

        # Current selection state
        self.selected_year = None
        self.selected_month = None
        self.selected_day = None

        # Data cache
        self.year_data = {}  # year -> show_count
        self.month_data = {}  # (year, month) -> [days with shows]

        self.setup_ui()
        self.load_year_data()

    def setup_ui(self):
        """Set up the three-column layout"""
        # Make widget background transparent so app background shows through
        self.setStyleSheet("DateSelectorWidget { background-color: transparent; }")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE
        )
        main_layout.setSpacing(Theme.SPACING_SMALL)

        # Title/Instructions (matching mockup: "choose year, then month, then day")
        instructions = QLabel("choose year, then month, then day")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_NORMAL};
                color: {Theme.TEXT_PRIMARY};
                padding: {Theme.SPACING_LARGE}px 0px;
                background-color: transparent;
            }}
        """)
        main_layout.addWidget(instructions)

        # Three-column layout
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(Theme.SPACING_MEDIUM)

        # Year column
        year_column, year_layout = self.create_column("Year")
        self.year_list = QListWidget()
        self.year_list.itemClicked.connect(self.on_year_selected)
        self.style_list_widget(self.year_list)
        year_layout.addWidget(self.year_list)
        columns_layout.addWidget(year_column, stretch=1)

        # Month column
        month_column, month_layout = self.create_column("Month")
        self.month_list = QListWidget()
        self.month_list.itemClicked.connect(self.on_month_selected)
        self.style_list_widget(self.month_list)
        month_layout.addWidget(self.month_list)
        columns_layout.addWidget(month_column, stretch=1)

        # Day column
        day_column, day_layout = self.create_column("Day")
        self.day_list = QListWidget()
        self.day_list.itemClicked.connect(self.on_day_selected)
        self.style_list_widget(self.day_list)
        day_layout.addWidget(self.day_list)
        columns_layout.addWidget(day_column, stretch=1)

        main_layout.addLayout(columns_layout)

        # Add spacer before action button
        main_layout.addSpacing(Theme.SPACING_MEDIUM)

        # Action button with right margin to avoid scrollbar overlap
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, Theme.SPACING_LARGE, 0)  # Right margin

        self.select_button = QPushButton("Load Show")
        self.select_button.setStyleSheet(Theme.get_button_style(Theme.ACCENT_YELLOW, Theme.TEXT_DARK))
        self.select_button.setMinimumHeight(Theme.BUTTON_HEIGHT + 20)  # Larger for prominence
        self.select_button.setEnabled(False)
        self.select_button.clicked.connect(self.on_select_clicked)

        button_layout.addWidget(self.select_button)
        main_layout.addLayout(button_layout)

    def create_column(self, title):
        """Create a column container with title. Returns (widget, layout) tuple."""
        column = QFrame()
        column.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                border: none;
            }}
        """)

        layout = QVBoxLayout(column)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Theme.SPACING_SMALL)

        # Column title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFixedHeight(60)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.HEADER_SMALL}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                background-color: {Theme.BG_PANEL_DARK};
                border-radius: 8px;
            }}
        """)
        layout.addWidget(title_label)

        return column, layout

    def style_list_widget(self, list_widget):
        """Apply consistent styling to list widgets"""
        # Use object name to make selector more specific than global theme
        list_widget.setObjectName("datePickerList")
        list_widget.setStyleSheet(f"""
            QListWidget#datePickerList {{
                background-color: {Theme.BG_PANEL_DARK};
                color: {Theme.TEXT_PRIMARY};
                border: none;
                border-radius: 8px;
                padding: {Theme.SPACING_SMALL}px;
                font-size: {Theme.HEADER_MEDIUM}px;
            }}
            QListWidget#datePickerList::item {{
                padding: {Theme.SPACING_MEDIUM}px {Theme.SPACING_SMALL}px;
                border-radius: 8px;
                margin: {Theme.SPACING_TINY // 2}px 0px;
                min-height: {Theme.BUTTON_HEIGHT}px;
            }}
            QListWidget#datePickerList::item:hover {{
                background-color: rgba(255, 255, 255, 0.05);
            }}
            QListWidget#datePickerList::item:selected {{
                background-color: {Theme.ACCENT_GREEN};
                color: {Theme.TEXT_PRIMARY};
                font-weight: {Theme.WEIGHT_BOLD};
            }}
            QListWidget#datePickerList QScrollBar:vertical {{
                background-color: {Theme.BG_PANEL_DARK} !important;
                background: {Theme.BG_PANEL_DARK} !important;
                width: 16px;
                margin: 0px;
                border: none;
            }}
            QListWidget#datePickerList QScrollBar::handle:vertical {{
                background-color: rgba(255, 255, 255, 0.3);
                background: rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                min-height: 30px;
            }}
            QListWidget#datePickerList QScrollBar::handle:vertical:hover {{
                background-color: rgba(255, 255, 255, 0.5);
                background: rgba(255, 255, 255, 0.5);
            }}
            QListWidget#datePickerList QScrollBar::add-line:vertical,
            QListWidget#datePickerList QScrollBar::sub-line:vertical {{
                height: 0px;
                background-color: {Theme.BG_PANEL_DARK};
                background: {Theme.BG_PANEL_DARK};
            }}
            QListWidget#datePickerList QScrollBar::add-page:vertical,
            QListWidget#datePickerList QScrollBar::sub-page:vertical {{
                background-color: {Theme.BG_PANEL_DARK};
                background: {Theme.BG_PANEL_DARK};
            }}
        """)

    def load_year_data(self):
        """Load years with show counts from database"""
        try:
            year_counts = get_show_count_by_year()
            self.year_data = {year: count for year, count in year_counts}

            # Populate year list (reverse chronological order)
            years = sorted(self.year_data.keys(), reverse=True)
            for year in years:
                item = QListWidgetItem(f"{year}")
                item.setData(Qt.UserRole, int(year))
                item.setTextAlignment(Qt.AlignCenter)
                self.year_list.addItem(item)

            print(f"[INFO] Loaded {len(years)} years with shows")

        except Exception as e:
            print(f"[ERROR] Failed to load year data: {e}")
            import traceback
            traceback.print_exc()

    def load_month_data(self, year):
        """Load months for the selected year"""
        self.month_list.clear()
        self.day_list.clear()
        self.selected_month = None
        self.selected_day = None

        try:
            # Get all months that have shows for this year
            month_names = [
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"
            ]

            months_with_shows = []
            for month in range(1, 13):
                shows = get_shows_by_month(year, month)
                if shows:
                    months_with_shows.append((month, len(shows)))
                    # Cache the show data
                    self.month_data[(year, month)] = shows

            # Populate month list
            for month, count in months_with_shows:
                item = QListWidgetItem(f"{month_names[month-1]}")
                item.setData(Qt.UserRole, month)
                item.setTextAlignment(Qt.AlignCenter)
                self.month_list.addItem(item)

            self.update_status()
            print(f"[INFO] Loaded {len(months_with_shows)} months for {year}")

        except Exception as e:
            print(f"[ERROR] Failed to load month data: {e}")
            import traceback
            traceback.print_exc()

    def load_day_data(self, year, month):
        """Load days for the selected month"""
        self.day_list.clear()
        self.selected_day = None

        try:
            # Get shows for this month from cache
            shows = self.month_data.get((year, month), [])

            # Extract unique days with shows
            days_with_shows = set()
            for show in shows:
                day = int(show['date'].split('-')[2])
                days_with_shows.add(day)

            # Populate day list
            for day in sorted(days_with_shows):
                item = QListWidgetItem(f"{day:02d}")
                item.setData(Qt.UserRole, day)
                item.setTextAlignment(Qt.AlignCenter)
                self.day_list.addItem(item)

            self.update_status()
            print(f"[INFO] Loaded {len(days_with_shows)} days for {year}-{month:02d}")

        except Exception as e:
            print(f"[ERROR] Failed to load day data: {e}")
            import traceback
            traceback.print_exc()

    def on_year_selected(self, item):
        """Handle year selection"""
        self.selected_year = item.data(Qt.UserRole)
        self.load_month_data(self.selected_year)
        print(f"[INFO] Year selected: {self.selected_year}")

    def on_month_selected(self, item):
        """Handle month selection"""
        self.selected_month = item.data(Qt.UserRole)
        if self.selected_year:
            self.load_day_data(self.selected_year, self.selected_month)
        print(f"[INFO] Month selected: {self.selected_month}")

    def on_day_selected(self, item):
        """Handle day selection"""
        self.selected_day = item.data(Qt.UserRole)
        self.update_status()
        print(f"[INFO] Day selected: {self.selected_day}")

    def update_status(self):
        """Update the status label and enable/disable select button"""
        if self.selected_year and self.selected_month and self.selected_day:
            # Full date selected - enable button
            self.select_button.setEnabled(True)
            # Change button color to green when ready
            self.select_button.setStyleSheet(Theme.get_button_style(Theme.ACCENT_YELLOW, Theme.TEXT_DARK))
        else:
            # Incomplete selection - disable button
            self.select_button.setEnabled(False)

    def on_select_clicked(self):
        """Handle select button click"""
        if self.selected_year and self.selected_month and self.selected_day:
            date_str = f"{self.selected_year}-{self.selected_month:02d}-{self.selected_day:02d}"
            print(f"[INFO] Date selection confirmed: {date_str}")
            self.date_selected.emit(date_str)

    def reset_selection(self):
        """Reset all selections"""
        self.selected_year = None
        self.selected_month = None
        self.selected_day = None

        self.year_list.clearSelection()
        self.month_list.clear()
        self.day_list.clear()

        self.update_status()


# Test code
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Apply global theme
    app.setStyleSheet(Theme.get_global_stylesheet())

    widget = DateSelectorWidget()
    widget.setWindowTitle("Date Selector Test")
    widget.setGeometry(100, 100, 1000, 600)
    widget.show()

    # Test signal
    widget.date_selected.connect(lambda date: print(f"[TEST] Date selected signal: {date}"))

    sys.exit(app.exec_())
