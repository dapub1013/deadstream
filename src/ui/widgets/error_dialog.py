"""
Error Dialog Widget

Displays user-facing error messages with retry/dismiss options.

Phase 10E.7 Polish:
- Uses Theme Manager for all colors/spacing/typography
- Helpful error recovery suggestions
- Professional appearance
- Zero hardcoded values
"""

import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from src.ui.styles.theme import Theme


class ErrorDialog(QDialog):
    """
    Modal dialog for displaying error messages to users.

    Features:
    - Error type categorization (Network, Playback, Database, etc.)
    - User-friendly error messages
    - Retry button for transient errors
    - Dismiss/Cancel button

    Signals:
        retry_requested: Emitted when user clicks Retry button
    """

    retry_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Error")
        self.setup_ui()

    def setup_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE
        )
        layout.setSpacing(Theme.SPACING_MEDIUM)

        # Error icon and title container
        header_layout = QHBoxLayout()
        header_layout.setSpacing(Theme.SPACING_SMALL)

        # Error icon
        self.icon_label = QLabel("!")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setFixedSize(50, 50)
        self.icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.ACCENT_RED};
                color: {Theme.TEXT_PRIMARY};
                font-size: 32px;
                font-weight: bold;
                border-radius: 25px;
            }}
        """)
        header_layout.addWidget(self.icon_label)

        # Title label
        self.title_label = QLabel("Error")
        title_font = QFont()
        title_font.setFamily(Theme.FONT_FAMILY)
        title_font.setPointSize(Theme.HEADER_MEDIUM)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        header_layout.addWidget(self.title_label, 1)

        layout.addLayout(header_layout)

        # Message label
        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)
        message_font = QFont()
        message_font.setFamily(Theme.FONT_FAMILY)
        message_font.setPointSize(Theme.BODY_MEDIUM)
        self.message_label.setFont(message_font)
        self.message_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                line-height: 1.5;
            }}
        """)
        layout.addWidget(self.message_label)

        # Suggestion label (helpful recovery actions)
        self.suggestion_label = QLabel("")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setVisible(False)
        suggestion_font = QFont()
        suggestion_font.setFamily(Theme.FONT_FAMILY)
        suggestion_font.setPointSize(Theme.BODY_SMALL)
        self.suggestion_label.setFont(suggestion_font)
        self.suggestion_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.ACCENT_BLUE};
                background-color: {Theme.BG_CARD};
                padding: {Theme.SPACING_SMALL}px;
                border-radius: {Theme.BUTTON_RADIUS}px;
                border-left: 3px solid {Theme.ACCENT_BLUE};
            }}
        """)
        layout.addWidget(self.suggestion_label)

        # Details label (optional technical details, hidden by default)
        self.details_label = QLabel("")
        self.details_label.setWordWrap(True)
        self.details_label.setVisible(False)
        details_font = QFont()
        details_font.setFamily("monospace")
        details_font.setPointSize(Theme.BODY_SMALL)
        self.details_label.setFont(details_font)
        self.details_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                font-family: monospace;
                background-color: {Theme.BG_CARD};
                padding: {Theme.SPACING_SMALL}px;
                border-radius: {Theme.BUTTON_RADIUS}px;
            }}
        """)
        layout.addWidget(self.details_label)

        # Button container
        button_layout = QHBoxLayout()
        button_layout.setSpacing(Theme.SPACING_SMALL)
        button_layout.addStretch()

        # Retry button (hidden by default)
        self.retry_button = QPushButton("Retry")
        self.retry_button.setVisible(False)
        self.retry_button.setMinimumSize(120, Theme.BUTTON_HEIGHT)
        self.retry_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.ACCENT_BLUE};
                color: {Theme.TEXT_PRIMARY};
                font-size: {Theme.BODY_MEDIUM}px;
                font-family: {Theme.FONT_FAMILY};
                font-weight: 600;
                border: none;
                border-radius: {Theme.BUTTON_RADIUS}px;
                padding: {Theme.SPACING_SMALL}px {Theme.SPACING_MEDIUM}px;
            }}
            QPushButton:hover {{
                background-color: {Theme.ACCENT_BLUE};
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                background-color: {Theme.ACCENT_BLUE};
                opacity: 0.8;
            }}
        """)
        self.retry_button.clicked.connect(self.on_retry_clicked)
        button_layout.addWidget(self.retry_button)

        # Dismiss button
        self.dismiss_button = QPushButton("OK")
        self.dismiss_button.setMinimumSize(120, Theme.BUTTON_HEIGHT)
        self.dismiss_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                font-size: {Theme.BODY_MEDIUM}px;
                font-family: {Theme.FONT_FAMILY};
                font-weight: 600;
                border: none;
                border-radius: {Theme.BUTTON_RADIUS}px;
                padding: {Theme.SPACING_SMALL}px {Theme.SPACING_MEDIUM}px;
            }}
            QPushButton:hover {{
                background-color: {Theme.BG_CARD};
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                background-color: {Theme.BG_CARD};
                opacity: 0.8;
            }}
        """)
        self.dismiss_button.clicked.connect(self.accept)
        button_layout.addWidget(self.dismiss_button)

        layout.addLayout(button_layout)

        # Set dialog background
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Theme.BG_PANEL_DARK};
            }}
        """)

        self.setLayout(layout)
        self.setMinimumWidth(500)

    def show_error(self, title, message, error_type="error", details=None,
                   suggestion=None, allow_retry=False):
        """
        Display an error dialog.

        Args:
            title: Error title (e.g., "Network Error", "Playback Error")
            message: User-friendly error message
            error_type: Type of error ("error", "warning", "info")
            details: Optional technical details to show
            suggestion: Helpful recovery suggestion for the user
            allow_retry: Whether to show a Retry button
        """
        self.title_label.setText(title)
        self.message_label.setText(message)

        # Update icon based on error type
        if error_type == "error":
            icon_bg = Theme.ACCENT_RED
            icon_text = "!"
        elif error_type == "warning":
            icon_bg = Theme.ACCENT_YELLOW
            icon_text = "!"
        elif error_type == "info":
            icon_bg = Theme.ACCENT_BLUE
            icon_text = "i"
        else:
            icon_bg = Theme.ACCENT_RED
            icon_text = "!"

        self.icon_label.setText(icon_text)
        self.icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {icon_bg};
                color: {Theme.TEXT_PRIMARY};
                font-size: 32px;
                font-weight: bold;
                border-radius: 25px;
            }}
        """)

        # Show/hide suggestion
        if suggestion:
            self.suggestion_label.setText(f"Suggestion: {suggestion}")
            self.suggestion_label.setVisible(True)
        else:
            self.suggestion_label.setVisible(False)

        # Show/hide details
        if details:
            self.details_label.setText(f"Details: {details}")
            self.details_label.setVisible(True)
        else:
            self.details_label.setVisible(False)

        # Show/hide retry button
        self.retry_button.setVisible(allow_retry)

        # Update dismiss button text
        if allow_retry:
            self.dismiss_button.setText("Cancel")
        else:
            self.dismiss_button.setText("OK")

        return self.exec_()

    def on_retry_clicked(self):
        """Handle retry button click"""
        self.retry_requested.emit()
        self.accept()


class ErrorType:
    """Error type constants"""
    NETWORK = "Network Error"
    PLAYBACK = "Playback Error"
    DATABASE = "Database Error"
    API = "API Error"
    VALIDATION = "Invalid Input"
    UNKNOWN = "Error"


def show_network_error(parent, message, details=None, suggestion=None, allow_retry=True):
    """
    Helper function to show network error dialog.

    Args:
        parent: Parent widget
        message: Error message
        details: Optional technical details
        suggestion: Optional recovery suggestion (defaults to network-specific suggestion)
        allow_retry: Whether to show retry button
    """
    if suggestion is None:
        suggestion = "Check your internet connection and try again"

    dialog = ErrorDialog(parent)
    return dialog.show_error(
        ErrorType.NETWORK,
        message,
        error_type="error",
        details=details,
        suggestion=suggestion,
        allow_retry=allow_retry
    )


def show_playback_error(parent, message, details=None, suggestion=None, allow_retry=True):
    """
    Helper function to show playback error dialog.

    Args:
        parent: Parent widget
        message: Error message
        details: Optional technical details
        suggestion: Optional recovery suggestion (defaults to playback-specific suggestion)
        allow_retry: Whether to show retry button
    """
    if suggestion is None:
        suggestion = "Try selecting a different recording or check your audio settings"

    dialog = ErrorDialog(parent)
    return dialog.show_error(
        ErrorType.PLAYBACK,
        message,
        error_type="error",
        details=details,
        suggestion=suggestion,
        allow_retry=allow_retry
    )


def show_database_error(parent, message, details=None, suggestion=None, allow_retry=False):
    """
    Helper function to show database error dialog.

    Args:
        parent: Parent widget
        message: Error message
        details: Optional technical details
        suggestion: Optional recovery suggestion (defaults to database-specific suggestion)
        allow_retry: Whether to show retry button
    """
    if suggestion is None:
        suggestion = "Try restarting the application or re-initializing the database"

    dialog = ErrorDialog(parent)
    return dialog.show_error(
        ErrorType.DATABASE,
        message,
        error_type="error",
        details=details,
        suggestion=suggestion,
        allow_retry=allow_retry
    )


def show_api_error(parent, message, details=None, suggestion=None, allow_retry=True):
    """
    Helper function to show API error dialog.

    Args:
        parent: Parent widget
        message: Error message
        details: Optional technical details
        suggestion: Optional recovery suggestion (defaults to API-specific suggestion)
        allow_retry: Whether to show retry button
    """
    if suggestion is None:
        suggestion = "Wait a moment and try again, or check archive.org status"

    dialog = ErrorDialog(parent)
    return dialog.show_error(
        ErrorType.API,
        message,
        error_type="error",
        details=details,
        suggestion=suggestion,
        allow_retry=allow_retry
    )
