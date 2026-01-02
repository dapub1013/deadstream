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
from src.ui.styles.button_styles import (
    PRIMARY_BUTTON_STYLE, BG_GRAY_800, BG_GRAY_700,
    BG_GRAY_900, TEXT_WHITE, TEXT_GRAY_400
)
from src.ui.styles.text_styles import TITLE_SECTION_STYLE, TEXT_SUPPORTING_STYLE


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
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # Header
        header = QLabel("Select Date")
        header.setStyleSheet(f"""
            QLabel {{
                {TITLE_SECTION_STYLE}
                padding-bottom: 8px;
                border-bottom: 2px solid {BG_GRAY_700};
            }}
        """)
        main_layout.addWidget(header)

        # Instructions
        instructions = QLabel("Choose Year, then Month, then Day")
        instructions.setStyleSheet(f"""
            QLabel {{
                {TEXT_SUPPORTING_STYLE}
            }}
        """)
        main_layout.addWidget(instructions)

        # Three-column layout
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(12)

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

        # Status/selection display
        self.status_label = QLabel("Select a year to begin")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                color: {TEXT_GRAY_400};
                padding: 16px;
                background-color: {BG_GRAY_900};
                border-radius: 8px;
                min-height: 60px;
            }}
        """)
        main_layout.addWidget(self.status_label)

        # Action button
        self.select_button = QPushButton("Load Shows for Selected Date")
        self.select_button.setStyleSheet(PRIMARY_BUTTON_STYLE)
        self.select_button.setMinimumHeight(60)
        self.select_button.setEnabled(False)
        self.select_button.clicked.connect(self.on_select_clicked)
        main_layout.addWidget(self.select_button)

    def create_column(self, title):
        """Create a column container with title. Returns (widget, layout) tuple."""
        column = QFrame()
        column.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_GRAY_900};
                border-radius: 8px;
                border: 2px solid {BG_GRAY_700};
            }}
        """)

        layout = QVBoxLayout(column)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Column title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {TEXT_WHITE};
                padding: 8px;
                background-color: {BG_GRAY_800};
                border-radius: 6px;
            }}
        """)
        layout.addWidget(title_label)

        return column, layout

    def style_list_widget(self, list_widget):
        """Apply consistent styling to list widgets"""
        list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {BG_GRAY_800};
                color: {TEXT_WHITE};
                border: none;
                border-radius: 6px;
                padding: 4px;
                font-size: 16px;
            }}
            QListWidget::item {{
                padding: 12px 8px;
                border-radius: 4px;
                margin: 2px 0px;
            }}
            QListWidget::item:hover {{
                background-color: #374151;
            }}
            QListWidget::item:selected {{
                background-color: #2563eb;
                color: white;
                font-weight: bold;
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
                count = self.year_data[year]
                item = QListWidgetItem(f"{year} ({count} shows)")
                item.setData(Qt.UserRole, int(year))
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
                item = QListWidgetItem(f"{month_names[month-1]} ({count} shows)")
                item.setData(Qt.UserRole, month)
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
                # Count shows on this day
                day_shows = [s for s in shows if int(s['date'].split('-')[2]) == day]
                count = len(day_shows)

                item = QListWidgetItem(f"{day} ({count} show{'s' if count > 1 else ''})")
                item.setData(Qt.UserRole, day)
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
            # Full date selected
            date_str = f"{self.selected_year}-{self.selected_month:02d}-{self.selected_day:02d}"
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted = date_obj.strftime("%B %d, %Y")

            self.status_label.setText(f"Selected: {formatted}")
            self.status_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 18px;
                    font-weight: bold;
                    color: {TEXT_WHITE};
                    padding: 16px;
                    background-color: #2563eb;
                    border-radius: 8px;
                    min-height: 60px;
                }}
            """)
            self.select_button.setEnabled(True)

        elif self.selected_year and self.selected_month:
            # Year and month selected
            month_names = [
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"
            ]
            self.status_label.setText(f"{month_names[self.selected_month-1]} {self.selected_year} - Select a day")
            self.status_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 16px;
                    color: {TEXT_GRAY_400};
                    padding: 16px;
                    background-color: {BG_GRAY_900};
                    border-radius: 8px;
                    min-height: 60px;
                }}
            """)
            self.select_button.setEnabled(False)

        elif self.selected_year:
            # Only year selected
            self.status_label.setText(f"{self.selected_year} - Select a month")
            self.status_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 16px;
                    color: {TEXT_GRAY_400};
                    padding: 16px;
                    background-color: {BG_GRAY_900};
                    border-radius: 8px;
                    min-height: 60px;
                }}
            """)
            self.select_button.setEnabled(False)
        else:
            # Nothing selected
            self.status_label.setText("Select a year to begin")
            self.status_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 16px;
                    color: {TEXT_GRAY_400};
                    padding: 16px;
                    background-color: {BG_GRAY_900};
                    border-radius: 8px;
                    min-height: 60px;
                }}
            """)
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

    # Apply dark theme
    app.setStyleSheet(f"""
        QWidget {{
            background-color: {BG_GRAY_800};
            color: {TEXT_WHITE};
        }}
    """)

    widget = DateSelectorWidget()
    widget.setWindowTitle("Date Selector Test")
    widget.setGeometry(100, 100, 1000, 600)
    widget.show()

    # Test signal
    widget.date_selected.connect(lambda date: print(f"[TEST] Date selected signal: {date}"))

    sys.exit(app.exec_())
