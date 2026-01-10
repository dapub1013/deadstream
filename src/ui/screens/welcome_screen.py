#!/usr/bin/env python3
"""
Welcome Screen - DeadStream Application
Restyled with Phase 10A component library.

This is the first screen users see when launching DeadStream.
Features two primary actions:
- Find a Show (browse interface)
- Random Show (play random concert)

Design: Gradient purple background, centered logo, large touch-friendly buttons
"""
import sys
import os

# Add project root to path
# __file__ is: .../deadstream/src/ui/screens/welcome_screen.py
# dirname(__file__) = .../deadstream/src/ui/screens
# dirname(dirname(__file__)) = .../deadstream/src/ui
# dirname(dirname(dirname(__file__))) = .../deadstream/src
# dirname(dirname(dirname(dirname(__file__)))) = .../deadstream (PROJECT ROOT)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSpacerItem, 
    QSizePolicy, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QLinearGradient, QColor

from src.ui.styles.theme import Theme
from src.ui.components.pill_button import PillButton
from src.ui.components.icon_button import IconButton


class WelcomeScreen(QWidget):
    """
    Welcome screen with app branding and primary navigation.
    
    Features:
    - Centered logo/title
    - "Find a Show" button (yellow CTA)
    - "Random Show" button (red/exciting)
    - Optional settings button in top-right corner
    
    Signals:
    - browse_requested: User wants to browse shows
    - random_show_requested: User wants to play random show
    - settings_requested: User wants to open settings
    """
    
    # Signals
    browse_requested = pyqtSignal()
    random_show_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize the welcome screen"""
        super().__init__(parent)
        
        # Set object name for identification
        self.setObjectName("welcomeScreen")
        
        # Enable auto-fill background so paintEvent is called
        self.setAutoFillBackground(True)
        
        # Create UI
        self._create_ui()
        
        print("[INFO] Welcome screen initialized with component library")
    
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
        """Create the welcome screen UI"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE
        )
        main_layout.setSpacing(Theme.SPACING_LARGE)
        
        # Header with optional settings button
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)
        
        # Add vertical spacer to push content to center
        main_layout.addStretch(1)
        
        # Logo/Title section
        logo_layout = self._create_logo_section()
        main_layout.addLayout(logo_layout)
        
        # Spacing between logo and buttons (larger gap for visual balance)
        main_layout.addSpacing(48)  # Extra spacing between logo and buttons
        
        # Action buttons
        buttons_layout = self._create_action_buttons()
        main_layout.addLayout(buttons_layout)
        
        # Add vertical spacer below buttons
        main_layout.addStretch(2)
        
        self.setLayout(main_layout)
    
    def _create_header(self):
        """
        Create header with optional settings button.
        
        Returns:
            QHBoxLayout with settings button in top-right
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Spacer to push settings button to right
        layout.addStretch()
        
        # Settings button (transparent variant, floats in corner)
        settings_btn = IconButton('settings', variant='transparent')
        settings_btn.setToolTip("Settings")
        settings_btn.clicked.connect(self._on_settings_clicked)
        layout.addWidget(settings_btn)
        
        return layout
    
    def _create_logo_section(self):
        """
        Create centered logo/title section.
        
        Returns:
            QVBoxLayout with centered logo and subtitle
        """
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_MEDIUM)
        layout.setAlignment(Qt.AlignCenter)
        
        # Main title - "DeadStream"
        title = QLabel("DeadStream")
        title.setAlignment(Qt.AlignCenter)
        
        # Use Theme typography (64px for large welcome title)
        title_font = QFont(Theme.FONT_FAMILY)
        title_font.setPixelSize(64)  # Larger than HEADER_LARGE for welcome screen
        title_font.setBold(True)
        title.setFont(title_font)
        
        # Use Theme colors with transparent background
        title.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            background: transparent;
        """)
        
        layout.addWidget(title)
        
        # Subtitle - "Grateful Dead Concert Player"
        subtitle = QLabel("Grateful Dead Concert Player")
        subtitle.setAlignment(Qt.AlignCenter)
        
        subtitle_font = QFont(Theme.FONT_FAMILY)
        subtitle_font.setPixelSize(Theme.BODY_LARGE)  # 20px
        subtitle.setFont(subtitle_font)
        
        subtitle.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            background: transparent;
        """)
        
        layout.addWidget(subtitle)
        
        # Optional: Add lightning bolt or skull icon here in future
        # For now, keep it text-only
        
        return layout
    
    def _create_action_buttons(self):
        """
        Create centered action buttons.
        
        Returns:
            QVBoxLayout with primary action buttons
        """
        layout = QVBoxLayout()
        layout.setSpacing(Theme.BUTTON_SPACING)
        layout.setAlignment(Qt.AlignCenter)
        
        # Primary CTA: "Find a Show"
        find_btn = PillButton("Find a Show", variant='blue')
        find_btn.setMinimumWidth(300)  # Wider buttons look better on welcome screen
        find_btn.setToolTip("Browse Grateful Dead concerts")
        find_btn.clicked.connect(self._on_browse_clicked)
        layout.addWidget(find_btn)
        
        # Secondary action: "Random Show"
        random_btn = PillButton("Random Show", variant='gradient')
        random_btn.setMinimumWidth(300)
        random_btn.setToolTip("Play a random Grateful Dead concert")
        random_btn.clicked.connect(self._on_random_clicked)
        layout.addWidget(random_btn)
        
        return layout
    
    # Signal handlers
    
    def _on_browse_clicked(self):
        """Handle Find a Show button click"""
        print("[INFO] Welcome: Browse requested")
        self.browse_requested.emit()
    
    def _on_random_clicked(self):
        """Handle Random Show button click"""
        print("[INFO] Welcome: Random show requested")
        self.random_show_requested.emit()
    
    def _on_settings_clicked(self):
        """Handle Settings button click"""
        print("[INFO] Welcome: Settings requested")
        self.settings_requested.emit()


def main():
    """Test the welcome screen"""
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create window
    window = WelcomeScreen()
    window.setWindowTitle("DeadStream - Welcome")
    window.resize(1024, 600)
    
    # Connect signals for testing
    window.browse_requested.connect(lambda: print("[TEST] Browse requested!"))
    window.random_show_requested.connect(lambda: print("[TEST] Random show requested!"))
    window.settings_requested.connect(lambda: print("[TEST] Settings requested!"))
    
    window.show()
    
    print("[INFO] Welcome screen test running")
    print("[INFO] Click buttons to test signals")
    print("[INFO] Close window to exit")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
