#!/usr/bin/env python3
"""
Test script for DateTimeSettingsWidget
Verifies the widget loads and functions correctly
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from src.ui.widgets.datetime_settings_widget import DateTimeSettingsWidget


def main():
    """Test the datetime settings widget"""
    print("=" * 60)
    print("DATETIME SETTINGS WIDGET TEST")
    print("=" * 60)
    print()
    
    app = QApplication(sys.argv)
    
    # Create widget
    widget = DateTimeSettingsWidget()
    widget.setStyleSheet("background-color: #121212;")
    widget.setWindowTitle("DeadStream - Date & Time Settings")
    widget.setGeometry(100, 100, 800, 700)
    
    # Connect signals for testing
    widget.timezone_changed.connect(
        lambda tz: print(f"[SIGNAL] Timezone changed to: {tz}")
    )
    widget.time_format_changed.connect(
        lambda is_24h: print(f"[SIGNAL] Time format changed to: {'24-hour' if is_24h else '12-hour'}")
    )
    widget.date_format_changed.connect(
        lambda fmt: print(f"[SIGNAL] Date format changed to: {fmt}")
    )
    
    # Show widget
    widget.show()
    
    print("[OK] DateTimeSettingsWidget created successfully")
    print("[INFO] Current settings:")
    print(f"  Timezone: {widget.get_timezone()}")
    print(f"  Time format: {'24-hour' if widget.get_time_format_24h() else '12-hour'}")
    print(f"  Date format: {widget.get_date_format()}")
    print()
    print("[INFO] Clock updates every second")
    print("[INFO] Try changing:")
    print("  - Timezone dropdown")
    print("  - Time format (12h/24h)")
    print("  - Date format (US/International)")
    print()
    print("Press Ctrl+C to quit")
    print("=" * 60)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
