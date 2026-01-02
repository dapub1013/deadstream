#!/usr/bin/env python3
"""
Visual demo of the refined year browser integration.
Shows the year browser appearing inline on the right panel.
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from src.ui.screens.browse_screen import BrowseScreen


def demo_sequence(browse_screen):
    """Demonstrate the year browser functionality"""

    step = [0]  # Counter in list to allow modification in nested function

    def next_step():
        step[0] += 1

        if step[0] == 1:
            print("\n[DEMO] Step 1: Initial view - Top Rated Shows (page 0)")
            print("       Left panel has 'Browse by Year' button")
            print("       Right panel shows top-rated show list")

        elif step[0] == 2:
            print("\n[DEMO] Step 2: Clicking 'Browse by Year' button...")
            browse_screen.show_year_browser()
            print("       Right panel now shows year browser grid (page 3)")
            print("       User can navigate decades and select years")

        elif step[0] == 3:
            print("\n[DEMO] Step 3: Navigate to 1970s decade...")
            browse_screen.year_browser_widget.current_decade = 1970
            browse_screen.year_browser_widget.update_year_grid()
            print("       Year grid updated to show 1970-1979")
            print("       Legendary years (1972, 1973, 1974, 1977) highlighted in gold")

        elif step[0] == 4:
            print("\n[DEMO] Step 4: Clicking '1977' button (legendary year)...")
            # Find and click 1977 button (index 7: 1970+7=1977)
            year_button = browse_screen.year_browser_widget.year_buttons[7]
            year_button.click()
            print("       Switched back to show list view (page 0)")
            print("       Header shows: '[LEGENDARY] 1977 (421 shows)'")
            print("       Show list populated with all 1977 shows")

        elif step[0] == 5:
            print("\n[DEMO] Step 5: Clicking 'Browse by Year' again...")
            browse_screen.show_year_browser()
            print("       Year browser appears again (page 3)")
            print("       State preserved - still showing 1970s")

        elif step[0] == 6:
            print("\n[DEMO] Step 6: Navigate to 1990s decade...")
            browse_screen.year_browser_widget.next_decade()
            browse_screen.year_browser_widget.next_decade()
            print("       Year grid updated to show 1990-1999")
            print("       1989 and 1990 highlighted as legendary years")

        elif step[0] == 7:
            print("\n[DEMO] Step 7: Clicking '1989' button...")
            # Navigate back to 1980s to get 1989
            browse_screen.year_browser_widget.previous_decade()
            # Find and click 1989 button (index 9: 1980+9=1989)
            year_button = browse_screen.year_browser_widget.year_buttons[9]
            year_button.click()
            print("       Switched back to show list view (page 0)")
            print("       Header shows: '[LEGENDARY] 1989 (X shows)'")

        elif step[0] == 8:
            print("\n" + "="*70)
            print("[DEMO] Complete! Year browser now appears inline on right panel.")
            print("       Same pattern as 'Browse by Date' - consistent UX!")
            print("="*70)
            QTimer.singleShot(2000, app.quit)
            return

        # Schedule next step
        if step[0] < 8:
            QTimer.singleShot(2000, next_step)

    # Start demo sequence
    QTimer.singleShot(1000, next_step)


if __name__ == "__main__":
    print("="*70)
    print("Year Browser Integration Demo")
    print("="*70)
    print("\nThis demo shows the refined 'Browse by Year' functionality.")
    print("The year browser now appears inline on the right panel,")
    print("matching the pattern used by 'Browse by Date'.\n")

    app = QApplication(sys.argv)

    # Apply dark theme
    app.setStyleSheet("""
        QWidget {
            background-color: #000000;
            color: #f3f4f6;
        }
    """)

    # Create browse screen
    browse_screen = BrowseScreen()
    browse_screen.setWindowTitle("Browse Screen - Year Browser Demo")
    browse_screen.setGeometry(100, 100, 1280, 720)
    browse_screen.show()

    # Start demo sequence
    demo_sequence(browse_screen)

    sys.exit(app.exec_())
