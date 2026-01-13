#!/usr/bin/env python3
"""
DeadStream Date & Time Settings Widget
Phase 8, Task 8.7: Date and time configuration

Provides controls for:
- Timezone selection
- Time format (12h/24h)
- Date format (US/International)
- Real-time clock display with format preview
"""

import sys
import os
from datetime import datetime

# Path manipulation for imports (4 levels up from src/ui/widgets/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QComboBox, QRadioButton, QButtonGroup, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from src.settings import get_settings
from src.ui.styles.theme import Theme

try:
    import pytz
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False
    print("[WARN] pytz not available, timezone support limited")


class DateTimeSettingsWidget(QWidget):
    """Widget for date and time configuration"""
    
    # Signals emitted when settings change
    timezone_changed = pyqtSignal(str)  # Timezone string
    time_format_changed = pyqtSignal(bool)  # True = 24h, False = 12h
    date_format_changed = pyqtSignal(str)  # 'US' or 'International'
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # Load settings from SettingsManager
        settings = get_settings()
        self.current_timezone = settings.get('datetime', 'timezone', 'America/New_York')
        self.use_24h = settings.get('datetime', 'time_format_24h', False)
        self.date_format = settings.get('datetime', 'date_format', 'US')

        # Clock update timer
        self.clock_timer = None

        self.init_ui()
        self.start_clock_updates()
    
    def init_ui(self):
        """Initialize the date/time settings UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(30)
        
        # Header
        header = self._create_header()
        main_layout.addLayout(header)
        
        # Current time display card
        time_card = self._create_current_time_card()
        main_layout.addWidget(time_card)
        
        # Timezone selection card
        timezone_card = self._create_timezone_card()
        main_layout.addWidget(timezone_card)
        
        # Format preferences card
        format_card = self._create_format_card()
        main_layout.addWidget(format_card)
        
        # Stretch at bottom
        main_layout.addStretch()
    
    def _create_header(self):
        """Create the header with title and subtitle"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Title
        title = QLabel("Date & Time Settings")
        title.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 28px;
            font-weight: bold;
            background-color: transparent;
        """)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Configure timezone and display format preferences")
        subtitle.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: 14px;
            background-color: transparent;
        """)
        layout.addWidget(subtitle)

        return layout
    
    def _create_current_time_card(self):
        """Create the current time display card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_CARD};
                border: none;
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Card title
        title = QLabel("Current Time")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        layout.addWidget(title)

        # Current time display (large)
        self.current_time_label = QLabel("--:--:--")
        time_font = QFont()
        time_font.setPointSize(36)
        time_font.setBold(True)
        self.current_time_label.setFont(time_font)
        self.current_time_label.setStyleSheet(f"""
            color: {Theme.ACCENT_YELLOW};
            background-color: {Theme._darken_color(Theme.BG_CARD, 10)};
            border-radius: 8px;
            padding: 20px;
        """)
        self.current_time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_time_label)

        # Current date display
        self.current_date_label = QLabel("--/--/----")
        date_font = QFont()
        date_font.setPointSize(18)
        self.current_date_label.setFont(date_font)
        self.current_date_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; background-color: transparent;")
        self.current_date_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_date_label)

        # Timezone info
        self.timezone_info_label = QLabel("Timezone: America/New_York (EST)")
        self.timezone_info_label.setStyleSheet(f"""
            color: {Theme._darken_color(Theme.TEXT_SECONDARY, 20)};
            font-size: 13px;
            background-color: transparent;
        """)
        self.timezone_info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.timezone_info_label)
        
        return card
    
    def _create_timezone_card(self):
        """Create the timezone selection card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_CARD};
                border: none;
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Card title
        title = QLabel("Timezone")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        layout.addWidget(title)

        # Description
        desc = QLabel("Select your timezone for accurate show dates and times")
        desc.setWordWrap(True)
        desc.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: 13px;
            background-color: transparent;
        """)
        layout.addWidget(desc)

        # Timezone selector
        tz_layout = QHBoxLayout()
        tz_layout.setSpacing(15)

        tz_label = QLabel("Timezone:")
        tz_label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 500;
            background-color: transparent;
        """)
        tz_layout.addWidget(tz_label)
        
        self.timezone_combo = QComboBox()
        
        # Add common US timezones
        timezones = [
            ('America/New_York', 'Eastern Time (New York)'),
            ('America/Chicago', 'Central Time (Chicago)'),
            ('America/Denver', 'Mountain Time (Denver)'),
            ('America/Phoenix', 'Mountain Time - No DST (Phoenix)'),
            ('America/Los_Angeles', 'Pacific Time (Los Angeles)'),
            ('America/Anchorage', 'Alaska Time (Anchorage)'),
            ('Pacific/Honolulu', 'Hawaii Time (Honolulu)'),
        ]
        
        # Add international timezones if pytz available
        if PYTZ_AVAILABLE:
            timezones.extend([
                ('Europe/London', 'UK Time (London)'),
                ('Europe/Paris', 'Central European Time (Paris)'),
                ('Asia/Tokyo', 'Japan Time (Tokyo)'),
                ('Australia/Sydney', 'Australian Eastern Time (Sydney)'),
            ])
        
        for tz_id, tz_name in timezones:
            self.timezone_combo.addItem(tz_name, tz_id)
        
        self.timezone_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Theme._darken_color(Theme.BG_CARD, 15)};
                color: {Theme.TEXT_PRIMARY};
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                min-width: 300px;
            }}
            QComboBox:hover {{
                background-color: {Theme._darken_color(Theme.BG_CARD, 10)};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 7px solid {Theme.TEXT_PRIMARY};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Theme._darken_color(Theme.BG_CARD, 15)};
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme._lighten_color(Theme.BG_CARD, 10)};
                selection-background-color: {Theme.ACCENT_GREEN};
                outline: none;
            }}
        """)
        self.timezone_combo.currentIndexChanged.connect(self._on_timezone_changed)
        tz_layout.addWidget(self.timezone_combo, stretch=1)

        layout.addLayout(tz_layout)

        # Info note
        note = QLabel("[INFO] Changing timezone affects how show dates are displayed. "
                     "Recordings are always stored with their original venue timezone.")
        note.setWordWrap(True)
        note.setStyleSheet(f"""
            color: {Theme._darken_color(Theme.TEXT_SECONDARY, 20)};
            font-size: 12px;
            font-style: italic;
            background-color: transparent;
        """)
        layout.addWidget(note)
        
        return card
    
    def _create_format_card(self):
        """Create the format preferences card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_CARD};
                border: none;
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(25)
        
        # Card title
        title = QLabel("Display Format Preferences")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        # Time format section
        time_format_section = self._create_time_format_section()
        layout.addWidget(time_format_section)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: #333333; max-height: 1px;")
        layout.addWidget(divider)
        
        # Date format section
        date_format_section = self._create_date_format_section()
        layout.addWidget(date_format_section)
        
        return card
    
    def _create_time_format_section(self):
        """Create the time format preference section"""
        section = QWidget()
        section.setStyleSheet("background-color: transparent;")
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)

        # Section label
        label = QLabel("Time Format:")
        label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 15px;
            font-weight: 600;
            background-color: transparent;
        """)
        section_layout.addWidget(label)
        
        # Radio button group for time format
        self.time_format_group = QButtonGroup(self)
        
        # 12-hour option
        radio_12h = QRadioButton("12-hour (3:45 PM)")
        radio_12h.setStyleSheet(f"""
            QRadioButton {{
                color: {Theme.TEXT_PRIMARY};
                font-size: 14px;
                spacing: 10px;
                background-color: transparent;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
            }}
            QRadioButton::indicator:unchecked {{
                background: {Theme._darken_color(Theme.BG_CARD, 15)};
                border: none;
                border-radius: 10px;
            }}
            QRadioButton::indicator:checked {{
                background: {Theme.ACCENT_GREEN};
                border: none;
                border-radius: 10px;
            }}
        """)
        radio_12h.setChecked(True)  # Default
        self.time_format_group.addButton(radio_12h, 0)
        section_layout.addWidget(radio_12h)
        
        # 24-hour option
        radio_24h = QRadioButton("24-hour (15:45)")
        radio_24h.setStyleSheet(f"""
            QRadioButton {{
                color: {Theme.TEXT_PRIMARY};
                font-size: 14px;
                spacing: 10px;
                background-color: transparent;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
            }}
            QRadioButton::indicator:unchecked {{
                background: {Theme._darken_color(Theme.BG_CARD, 15)};
                border: none;
                border-radius: 10px;
            }}
            QRadioButton::indicator:checked {{
                background: {Theme.ACCENT_GREEN};
                border: none;
                border-radius: 10px;
            }}
        """)
        self.time_format_group.addButton(radio_24h, 1)
        section_layout.addWidget(radio_24h)
        
        # Connect signal
        self.time_format_group.buttonClicked.connect(self._on_time_format_changed)
        
        return section
    
    def _create_date_format_section(self):
        """Create the date format preference section"""
        section = QWidget()
        section.setStyleSheet("background-color: transparent;")
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)

        # Section label
        label = QLabel("Date Format:")
        label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 15px;
            font-weight: 600;
            background-color: transparent;
        """)
        section_layout.addWidget(label)
        
        # Radio button group for date format
        self.date_format_group = QButtonGroup(self)
        
        # US format option
        radio_us = QRadioButton("US Format (MM/DD/YYYY)")
        radio_us.setStyleSheet(f"""
            QRadioButton {{
                color: {Theme.TEXT_PRIMARY};
                font-size: 14px;
                spacing: 10px;
                background-color: transparent;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
            }}
            QRadioButton::indicator:unchecked {{
                background: {Theme._darken_color(Theme.BG_CARD, 15)};
                border: none;
                border-radius: 10px;
            }}
            QRadioButton::indicator:checked {{
                background: {Theme.ACCENT_GREEN};
                border: none;
                border-radius: 10px;
            }}
        """)
        radio_us.setChecked(True)  # Default
        self.date_format_group.addButton(radio_us, 0)
        section_layout.addWidget(radio_us)
        
        # International format option
        radio_intl = QRadioButton("International Format (DD/MM/YYYY)")
        radio_intl.setStyleSheet(f"""
            QRadioButton {{
                color: {Theme.TEXT_PRIMARY};
                font-size: 14px;
                spacing: 10px;
                background-color: transparent;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
            }}
            QRadioButton::indicator:unchecked {{
                background: {Theme._darken_color(Theme.BG_CARD, 15)};
                border: none;
                border-radius: 10px;
            }}
            QRadioButton::indicator:checked {{
                background: {Theme.ACCENT_GREEN};
                border: none;
                border-radius: 10px;
            }}
        """)
        self.date_format_group.addButton(radio_intl, 1)
        section_layout.addWidget(radio_intl)
        
        # Connect signal
        self.date_format_group.buttonClicked.connect(self._on_date_format_changed)
        
        return section
    
    def start_clock_updates(self):
        """Start the clock update timer"""
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)  # Update every second
        
        # Initial update
        self._update_clock()
    
    def _update_clock(self):
        """Update the current time/date display"""
        if PYTZ_AVAILABLE:
            try:
                tz = pytz.timezone(self.current_timezone)
                now = datetime.now(tz)
            except:
                now = datetime.now()
        else:
            now = datetime.now()
        
        # Format time
        if self.use_24h:
            time_str = now.strftime("%H:%M:%S")
        else:
            time_str = now.strftime("%I:%M:%S %p")
        
        # Format date
        if self.date_format == 'US':
            date_str = now.strftime("%m/%d/%Y")
        else:
            date_str = now.strftime("%d/%m/%Y")
        
        # Update labels
        self.current_time_label.setText(time_str)
        self.current_date_label.setText(date_str)
        
        # Update timezone info
        if PYTZ_AVAILABLE:
            try:
                tz_abbrev = now.strftime("%Z")
                self.timezone_info_label.setText(f"Timezone: {self.current_timezone} ({tz_abbrev})")
            except:
                self.timezone_info_label.setText(f"Timezone: {self.current_timezone}")
        else:
            self.timezone_info_label.setText(f"Timezone: {self.current_timezone}")
    
    def _on_timezone_changed(self, index):
        """Handle timezone selection changes"""
        self.current_timezone = self.timezone_combo.itemData(index)

        # Persist to SettingsManager
        settings = get_settings()
        settings.set('datetime', 'timezone', self.current_timezone)
        print(f"[INFO] DateTime: Timezone saved to settings: {self.current_timezone}")

        self._update_clock()
        self.timezone_changed.emit(self.current_timezone)
    
    def _on_time_format_changed(self, button):
        """Handle time format preference changes"""
        button_id = self.time_format_group.id(button)
        self.use_24h = (button_id == 1)

        # Persist to SettingsManager
        settings = get_settings()
        settings.set('datetime', 'time_format_24h', self.use_24h)
        print(f"[INFO] DateTime: Time format saved to settings: {'24h' if self.use_24h else '12h'}")

        self._update_clock()
        self.time_format_changed.emit(self.use_24h)
    
    def _on_date_format_changed(self, button):
        """Handle date format preference changes"""
        button_id = self.date_format_group.id(button)
        self.date_format = 'International' if button_id == 1 else 'US'

        # Persist to SettingsManager
        settings = get_settings()
        settings.set('datetime', 'date_format', self.date_format)
        print(f"[INFO] DateTime: Date format saved to settings: {self.date_format}")

        self._update_clock()
        self.date_format_changed.emit(self.date_format)
    
    def get_timezone(self):
        """Get the current timezone setting"""
        return self.current_timezone
    
    def set_timezone(self, timezone):
        """Set the timezone"""
        # Find and select the timezone in the combo box
        for i in range(self.timezone_combo.count()):
            if self.timezone_combo.itemData(i) == timezone:
                self.timezone_combo.setCurrentIndex(i)
                break
    
    def get_time_format_24h(self):
        """Get whether 24-hour format is enabled"""
        return self.use_24h
    
    def set_time_format_24h(self, use_24h):
        """Set the time format"""
        button_id = 1 if use_24h else 0
        self.time_format_group.button(button_id).setChecked(True)
        self.use_24h = use_24h
        self._update_clock()
    
    def get_date_format(self):
        """Get the date format setting"""
        return self.date_format
    
    def set_date_format(self, format_type):
        """Set the date format ('US' or 'International')"""
        button_id = 1 if format_type == 'International' else 0
        self.date_format_group.button(button_id).setChecked(True)
        self.date_format = format_type
        self._update_clock()


# Test function for standalone testing
def test_datetime_settings():
    """Test the date/time settings widget"""
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Create and show widget
    widget = DateTimeSettingsWidget()
    widget.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
    widget.resize(700, 700)
    widget.show()
    
    # Connect signals for testing
    widget.timezone_changed.connect(
        lambda tz: print(f"[TEST] Timezone changed to: {tz}")
    )
    widget.time_format_changed.connect(
        lambda is_24h: print(f"[TEST] Time format changed to: {'24h' if is_24h else '12h'}")
    )
    widget.date_format_changed.connect(
        lambda fmt: print(f"[TEST] Date format changed to: {fmt}")
    )
    
    print("[INFO] DateTime settings widget loaded")
    print("[INFO] Clock updates every second")
    print("[INFO] Try changing timezone and formats")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    test_datetime_settings()
