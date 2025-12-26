#!/usr/bin/env python3
"""
Test script for DateBrowser widget (Phase 7, Task 7.2)

This demonstrates the calendar-style date browser for finding shows.

Usage:
    python examples/phase7_date_browser_test.py
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.ui.widgets.date_browser import DateBrowser
from src.database.queries import get_shows_by_month


class DateBrowserDemo(QMainWindow):
    """Demo window to test the DateBrowser widget"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Set up the demo window"""
        self.setWindowTitle("DeadStream - Date Browser Test (Phase 7.2)")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Date Browser Widget Test")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Click on any blue date to see shows for that day.\n"
            "Use < and > buttons to navigate months.\n"
            "Click 'Today' to return to current month."
        )
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Date browser widget
        self.date_browser = DateBrowser()
        self.date_browser.date_selected.connect(self.on_date_selected)
        layout.addWidget(self.date_browser)
        
        # Selected date info
        self.info_label = QLabel("Select a date to see details")
        self.info_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)
        
        # Show details area
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(200)
        layout.addWidget(self.details_text)
        
        central.setLayout(layout)
        self.setCentralWidget(central)
        
        print("[INFO] DateBrowser demo window initialized")
    
    def on_date_selected(self, date_str):
        """Handle date selection from browser"""
        try:
            # Parse the date
            year, month, day = date_str.split('-')
            year, month, day = int(year), int(month), int(day)
            
            # Update label
            from datetime import datetime
            date_obj = datetime(year, month, day)
            formatted_date = date_obj.strftime("%A, %B %d, %Y")
            self.info_label.setText(f"Shows on {formatted_date}")
            
            # Get shows for this month and filter to exact date
            shows = get_shows_by_month(year, month)
            date_shows = [s for s in shows if s['date'] == date_str]
            
            # Display show details
            if date_shows:
                details = f"Found {len(date_shows)} recording(s) on {formatted_date}:\n\n"
                for i, show in enumerate(date_shows, 1):
                    details += f"{i}. {show['venue']}\n"
                    details += f"   {show['city']}, {show['state']}\n"
                    details += f"   Identifier: {show['identifier']}\n"
                    if show['avg_rating']:
                        details += f"   Rating: {show['avg_rating']:.2f}/5.0 ({show['num_reviews']} reviews)\n"
                    details += "\n"
                
                self.details_text.setPlainText(details)
            else:
                self.details_text.setPlainText(f"No shows found on {formatted_date}")
            
            print(f"[INFO] Displaying {len(date_shows)} show(s) for {date_str}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load show details: {e}")
            self.details_text.setPlainText(f"Error loading shows: {e}")


def main():
    """Run the date browser test"""
    print("=" * 60)
    print("DateBrowser Widget Test (Phase 7, Task 7.2)")
    print("=" * 60)
    
    app = QApplication(sys.argv)
    
    # Apply dark theme
    app.setStyle("Fusion")
    from PyQt5.QtGui import QPalette, QColor
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(45, 45, 45))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    # Create and show demo window
    demo = DateBrowserDemo()
    demo.show()
    
    print("\n[INFO] Date browser test window displayed")
    print("[INFO] Try clicking on different dates (blue = has shows)")
    print("[INFO] Use month navigation buttons to browse")
    print("\nPress Ctrl+Q to quit")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
