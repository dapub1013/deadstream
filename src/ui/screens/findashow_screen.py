#!/usr/bin/env python3
"""
FindAShow Screen - DeadStream Application

This screen provides a dedicated interface for finding shows by date.
Features:
- DateSelectorWidget (3-column date picker)
- Settings button (top-right corner, matching welcome_screen.py)
- Back button (returns to welcome screen)

Design: Gradient purple background, centered date selector
"""
import sys
import os

# Add project root to path
# __file__ is: .../deadstream/src/ui/screens/findashow_screen.py
# dirname(__file__) = .../deadstream/src/ui/screens
# dirname(dirname(__file__)) = .../deadstream/src/ui
# dirname(dirname(dirname(__file__))) = .../deadstream/src
# dirname(dirname(dirname(dirname(__file__)))) = .../deadstream (PROJECT ROOT)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem,
    QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPainter, QLinearGradient, QColor

from src.ui.styles.theme import Theme
from src.ui.components.icon_button import IconButton
from src.ui.widgets.date_selector import DateSelectorWidget


class FindAShowScreen(QWidget):
    """
    Find A Show screen with date selector and navigation.

    Features:
    - Centered DateSelectorWidget (3-column date picker)
    - Settings button (top-right corner)
    - Back button (returns to welcome screen)
    - Gradient purple background

    Signals:
    - date_selected: User selected a complete date (YYYY-MM-DD)
    - settings_requested: User wants to open settings
    - back_requested: User wants to go back to welcome screen
    """

    # Signals
    date_selected = pyqtSignal(str)  # Emits date string (YYYY-MM-DD)
    settings_requested = pyqtSignal()
    back_requested = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the find a show screen"""
        super().__init__(parent)

        # Set object name for identification
        self.setObjectName("findAShowScreen")

        # Enable auto-fill background so paintEvent is called
        self.setAutoFillBackground(True)

        # Create UI
        self._create_ui()

        print("[INFO] Find A Show screen initialized")

    def paintEvent(self, event):
        """
        Paint the gradient background manually.
        This is more reliable than stylesheets for gradients.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create linear gradient from top to bottom
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(Theme.BG_PRIMARY))  # #2E2870 deep purple
        gradient.setColorAt(1, QColor("#1a1a4a"))  # darker purple

        # Fill the entire widget with gradient
        painter.fillRect(self.rect(), gradient)

        # Call parent paintEvent to ensure child widgets are drawn
        super().paintEvent(event)

    def _create_ui(self):
        """Create the find a show screen UI"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE
        )
        main_layout.setSpacing(0)  # No spacing, we'll control it manually

        # Header with settings button (top-right) and back button (top-left)
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)

        # Add minimal vertical spacer above date selector
        main_layout.addSpacing(Theme.SPACING_MEDIUM)

        # Date selector container - takes up most of the screen height
        date_selector_container = QWidget()
        date_selector_container.setStyleSheet("background-color: transparent;")
        date_container_layout = QVBoxLayout(date_selector_container)

        # No padding to maximize available space
        date_container_layout.setContentsMargins(0, 0, 0, 0)
        date_container_layout.setSpacing(0)

        # Create horizontal layout to center the date selector
        date_selector_layout = self._create_date_selector()
        date_container_layout.addLayout(date_selector_layout)

        # Add the date selector with a large stretch factor to take up most vertical space
        main_layout.addWidget(date_selector_container, stretch=10)

        # Add minimal vertical spacer below date selector
        main_layout.addSpacing(Theme.SPACING_MEDIUM)

        self.setLayout(main_layout)

    def _create_header(self):
        """
        Create header with back button (left) and settings button (right).
        Matches the settings button position from welcome_screen.py.

        Returns:
            QHBoxLayout with back and settings buttons
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Back button (left side)
        back_btn = IconButton('back', variant='transparent')
        back_btn.setToolTip("Back to Welcome")
        back_btn.clicked.connect(self._on_back_clicked)
        layout.addWidget(back_btn)

        # Spacer to push settings button to right
        layout.addStretch()

        # Settings button (right side, exactly matching welcome_screen.py position)
        settings_btn = IconButton('settings', variant='transparent')
        settings_btn.setToolTip("Settings")
        settings_btn.clicked.connect(self._on_settings_clicked)
        layout.addWidget(settings_btn)

        return layout

    def _create_date_selector(self):
        """
        Create centered date selector widget.

        Returns:
            QHBoxLayout with centered DateSelectorWidget
        """
        layout = QHBoxLayout()
        layout.setSpacing(0)

        # Add left spacer
        layout.addStretch(1)

        # Date selector widget
        self.date_selector = DateSelectorWidget()
        self.date_selector.date_selected.connect(self._on_date_selected)

        # Set maximum width for better appearance on large screens
        self.date_selector.setMaximumWidth(1000)

        layout.addWidget(self.date_selector)

        # Add right spacer
        layout.addStretch(1)

        return layout

    # Signal handlers

    def _on_date_selected(self, date_str):
        """Handle date selection from DateSelectorWidget"""
        print(f"[INFO] FindAShow: Date selected: {date_str}")
        self.date_selected.emit(date_str)

    def _on_settings_clicked(self):
        """Handle Settings button click"""
        print("[INFO] FindAShow: Settings requested")
        self.settings_requested.emit()

    def _on_back_clicked(self):
        """Handle Back button click"""
        print("[INFO] FindAShow: Back to welcome requested")
        self.back_requested.emit()

    # Public methods

    def reset_selection(self):
        """Reset the date selector to initial state"""
        if hasattr(self, 'date_selector'):
            self.date_selector.reset_selection()


def main():
    """Test the find a show screen"""
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Create window
    window = FindAShowScreen()
    window.setWindowTitle("DeadStream - Find A Show")
    window.resize(1024, 600)

    # Connect signals for testing
    window.date_selected.connect(lambda date: print(f"[TEST] Date selected: {date}"))
    window.settings_requested.connect(lambda: print("[TEST] Settings requested!"))
    window.back_requested.connect(lambda: print("[TEST] Back requested!"))

    window.show()

    print("[INFO] Find A Show screen test running")
    print("[INFO] Select a date to test date_selected signal")
    print("[INFO] Click settings button to test settings_requested signal")
    print("[INFO] Click back button to test back_requested signal")
    print("[INFO] Close window to exit")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
