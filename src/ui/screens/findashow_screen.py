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
    QSizePolicy, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QPixmap, QIcon

from src.ui.styles.theme import Theme
from src.ui.widgets.date_selector import DateSelectorWidget


class FindAShowScreen(QWidget):
    """
    Find A Show screen with date selector and navigation.

    Features:
    - Centered DateSelectorWidget (3-column date picker)
    - Home button (absolutely positioned in upper left corner)
    - Settings button (absolutely positioned in upper right corner)
    - Gradient purple background

    Signals:
    - date_selected: User selected a complete date (YYYY-MM-DD)
    - home_requested: User wants to go home
    - settings_requested: User wants to open settings
    """

    # Signals
    date_selected = pyqtSignal(str)  # Emits date string (YYYY-MM-DD)
    settings_requested = pyqtSignal()
    home_requested = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize the find a show screen"""
        super().__init__(parent)

        # Set object name for identification
        self.setObjectName("findAShowScreen")

        # Enable auto-fill background so paintEvent is called
        self.setAutoFillBackground(True)

        # Create UI
        self._create_ui()

        # Create corner buttons (positioned absolutely)
        self._create_home_button()
        self._create_settings_button()

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

    def _create_home_button(self):
        """
        Create home button positioned absolutely in the upper left corner.

        Specifications:
        - Position: 25px from top, 25px from left edge
        - Size: 80x80px
        - Icon: assets/home-round.png scaled to 60x60px
        - Style: Transparent background with semi-transparent hover/press states
        """
        # Create button with this widget as parent
        self.home_btn = QPushButton(self)
        self.home_btn.setFixedSize(80, 80)

        # Load and scale icon
        icon_path = os.path.join(PROJECT_ROOT, 'assets', 'home-round.png')
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon = QIcon(scaled_pixmap)
            self.home_btn.setIcon(icon)
            self.home_btn.setIconSize(QSize(60, 60))
        else:
            print(f"[WARNING] Home icon not found at {icon_path}")

        # Style with transparent background and hover states
        self.home_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)

        # Connect click handler
        self.home_btn.clicked.connect(self._on_home_clicked)

        # Position button at fixed location (doesn't change with resize)
        self.home_btn.move(25, 25)

        # Make sure button is on top
        self.home_btn.raise_()

    def _create_settings_button(self):
        """
        Create settings button positioned absolutely in the upper right corner.

        Specifications:
        - Position: 25px from top, 25px from right edge
        - Size: 80x80px
        - Icon: assets/settings.png scaled to 60x60px
        - Style: Transparent background with semi-transparent hover/press states
        """
        # Create button with this widget as parent
        self.settings_btn = QPushButton(self)
        self.settings_btn.setFixedSize(80, 80)

        # Load and scale icon
        icon_path = os.path.join(PROJECT_ROOT, 'assets', 'settings.png')
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon = QIcon(scaled_pixmap)
            self.settings_btn.setIcon(icon)
            self.settings_btn.setIconSize(QSize(60, 60))
        else:
            print(f"[WARNING] Settings icon not found at {icon_path}")

        # Style with transparent background and hover states
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)

        # Connect click handler
        self.settings_btn.clicked.connect(self._on_settings_clicked)

        # Position button (will be repositioned in resizeEvent)
        self._position_settings_button()

        # Make sure button is on top
        self.settings_btn.raise_()

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

    def _position_settings_button(self):
        """Position the settings button in the upper right corner"""
        if hasattr(self, 'settings_btn'):
            x = self.width() - 80 - 25  # 25px margin from right
            y = 25  # 25px margin from top
            self.settings_btn.move(x, y)

    def resizeEvent(self, event):
        """Handle window resize to reposition settings button"""
        super().resizeEvent(event)
        self._position_settings_button()

    # Signal handlers

    def _on_date_selected(self, date_str):
        """Handle date selection from DateSelectorWidget"""
        print(f"[INFO] FindAShow: Date selected: {date_str}")
        self.date_selected.emit(date_str)

    def _on_settings_clicked(self):
        """Handle Settings button click"""
        print("[INFO] FindAShow: Settings requested")
        self.settings_requested.emit()

    def _on_home_clicked(self):
        """Handle Home button click"""
        print("[INFO] FindAShow: Home requested")
        self.home_requested.emit()

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
    window.home_requested.connect(lambda: print("[TEST] Home requested!"))

    window.show()

    print("[INFO] Find A Show screen test running")
    print("[INFO] Select a date to test date_selected signal")
    print("[INFO] Click home button (upper left) to test home_requested signal")
    print("[INFO] Click settings button (upper right) to test settings_requested signal")
    print("[INFO] Close window to exit")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
