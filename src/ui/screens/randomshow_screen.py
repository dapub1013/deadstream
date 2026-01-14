#!/usr/bin/env python3
"""
Random Show Screen for DeadStream - Phase 10F

Displays a randomly selected show with full details and setlist.
Users can play the show or request a different random show.

Design:
- Concert header at top (date, venue, location, rating)
- Large panel with full setlist (scrollable)
- Two action buttons at bottom ("Play Show", "Try Again")
- Home and settings icons in corners

Follows Phase 10A-10E styling with Theme Manager integration.
"""

# Path manipulation for imports (file in src/ui/screens/)
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QLinearGradient, QColor

# Import Theme Manager and components
from src.ui.styles.theme import Theme
from src.ui.components.pill_button import PillButton
from src.ui.components.icon_button import IconButton

# Import widgets
from src.ui.widgets.random_show_widget import RandomShowWidget


class RandomShowScreen(QWidget):
    """
    Random Show Screen - Phase 10F

    Displays a randomly selected Grateful Dead show with:
    - Concert metadata (date, venue, location, rating)
    - Full setlist with tracks organized by set
    - "Play Show" button to start playback
    - "Try Again" button to load a different random show
    - Corner navigation (home, settings)

    Signals:
        show_selected: Emitted when user clicks "Play Show" (emits show dict)
        home_requested: Navigate to welcome screen
        settings_requested: Navigate to settings screen
    """

    # Navigation signals
    show_selected = pyqtSignal(dict)
    home_requested = pyqtSignal()
    settings_requested = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize random show screen"""
        super().__init__(parent)

        # Set object name for identification
        self.setObjectName("randomShowScreen")

        # Enable auto-fill background for gradient
        self.setAutoFillBackground(True)

        # Create UI
        self.init_ui()

        print("[INFO] Random Show screen initialized")

    def paintEvent(self, event):
        """
        Paint the gradient background manually.
        Gradient from purple to darker purple (consistent with welcome screen).
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

    def init_ui(self):
        """Set up the random show screen layout"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            Theme.SPACING_XLARGE,
            Theme.SPACING_XLARGE,
            Theme.SPACING_XLARGE,
            Theme.SPACING_XLARGE
        )
        main_layout.setSpacing(Theme.SPACING_LARGE)

        # Title header
        title_label = QLabel("Random Show")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
            }}
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Random show widget (does all the heavy lifting)
        self.random_show_widget = RandomShowWidget()
        self.random_show_widget.setStyleSheet(f"""
            RandomShowWidget {{
                background-color: transparent;
                border: none;
            }}
        """)

        # Connect signals from widget
        self.random_show_widget.show_selected.connect(self._on_show_selected)
        self.random_show_widget.reload_requested.connect(self._on_reload_requested)

        main_layout.addWidget(self.random_show_widget)

        # Corner navigation buttons
        self.create_corner_buttons()

        self.setLayout(main_layout)

    def create_corner_buttons(self):
        """Create ghost-style corner navigation buttons"""
        # Home button (top-right)
        self.home_button = IconButton('home', variant='transparent')
        self.home_button.setParent(self)
        self.home_button.move(self.width() - 72, 12)  # 12px from edges
        self.home_button.clicked.connect(self._on_home_clicked)
        self.home_button.raise_()  # Ensure it's on top

        # Settings button (bottom-right)
        self.settings_button = IconButton('settings', variant='transparent')
        self.settings_button.setParent(self)
        self.settings_button.move(self.width() - 72, self.height() - 72)
        self.settings_button.clicked.connect(self._on_settings_clicked)
        self.settings_button.raise_()  # Ensure it's on top

    def resizeEvent(self, event):
        """Reposition corner buttons on window resize"""
        super().resizeEvent(event)

        # Reposition home button (top-right)
        if hasattr(self, 'home_button'):
            self.home_button.move(self.width() - 72, 12)

        # Reposition settings button (bottom-right)
        if hasattr(self, 'settings_button'):
            self.settings_button.move(self.width() - 72, self.height() - 72)

    def showEvent(self, event):
        """Called when screen is shown - load a random show"""
        super().showEvent(event)

        # Load random show when screen becomes visible
        print("[INFO] Random Show screen shown - loading random show")
        self.random_show_widget.load_random_show()

    def _on_show_selected(self, show):
        """Handle show selection from widget"""
        print(f"[INFO] Random show selected: {show['date']} - {show['venue']}")
        self.show_selected.emit(show)

    def _on_reload_requested(self):
        """Handle reload request from widget"""
        print("[INFO] Random show reload requested")
        # Widget handles the reload internally, we just log it

    def _on_home_clicked(self):
        """Handle home button click"""
        print("[INFO] Home button clicked from Random Show screen")
        self.home_requested.emit()

    def _on_settings_clicked(self):
        """Handle settings button click"""
        print("[INFO] Settings button clicked from Random Show screen")
        self.settings_requested.emit()


if __name__ == "__main__":
    """Test the random show screen"""
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Apply theme
    app.setStyleSheet(f"""
        QWidget {{
            background-color: {Theme.BG_PRIMARY};
            color: {Theme.TEXT_PRIMARY};
        }}
    """)

    screen = RandomShowScreen()
    screen.setGeometry(100, 100, 1280, 720)
    screen.setWindowTitle("Random Show Screen Test")

    # Handle signals
    screen.show_selected.connect(lambda show: print(f"[TEST] Show selected: {show['date']}"))
    screen.home_requested.connect(lambda: print("[TEST] Home requested"))
    screen.settings_requested.connect(lambda: print("[TEST] Settings requested"))

    screen.show()
    sys.exit(app.exec_())
