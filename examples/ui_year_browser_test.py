#!/usr/bin/env python3
"""
Test script for Year Browser Widget (Task 7.4)

Tests the year selector functionality including:
- Legendary years section display
- Decade expansion/collapse
- Year selection
- Database integration
- UI responsiveness
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

from src.ui.widgets.year_browser import YearBrowser


class TestWindow(QMainWindow):
    """Test window for year browser"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Year Browser Test - Task 7.4")
        self.setGeometry(100, 100, 900, 700)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Status label
        self.status_label = QLabel("Select a year to see the signal...")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #1f2937;
                color: white;
                padding: 10px;
                font-size: 14px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Year browser widget
        self.browser = YearBrowser()
        self.browser.year_selected.connect(self.on_year_selected)
        layout.addWidget(self.browser)
        
        print("[INFO] Year Browser Test Window initialized")
        print("[INFO] Test the following:")
        print("  1. Click legendary years (1977, 1972, etc.)")
        print("  2. Expand/collapse decades")
        print("  3. Verify only one decade expands at a time")
        print("  4. Click individual years within decades")
        print("  5. Check show counts are displayed")
    
    def on_year_selected(self, year):
        """Handle year selection signal"""
        self.status_label.setText(f"[SIGNAL RECEIVED] Year selected: {year}")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #7c3aed;
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        print(f"[SIGNAL] Year selected: {year}")


def main():
    """Run the test"""
    print("=" * 60)
    print("YEAR BROWSER TEST - TASK 7.4")
    print("=" * 60)
    
    app = QApplication(sys.argv)
    
    # Create and show test window
    window = TestWindow()
    window.show()
    
    print("\n[INFO] Test window displayed")
    print("[INFO] Interact with the year browser to test functionality\n")
    
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
