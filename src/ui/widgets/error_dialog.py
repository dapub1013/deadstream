"""
Error Dialog Widget

Displays user-facing error messages with retry/dismiss options.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


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
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Error icon and title container
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        # Error icon (using text for now, could use QIcon later)
        self.icon_label = QLabel("!")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setFixedSize(50, 50)
        self.icon_label.setStyleSheet("""
            QLabel {
                background-color: #EF4444;
                color: white;
                font-size: 32px;
                font-weight: bold;
                border-radius: 25px;
            }
        """)
        header_layout.addWidget(self.icon_label)

        # Title label
        self.title_label = QLabel("Error")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #F3F4F6;")
        header_layout.addWidget(self.title_label, 1)

        layout.addLayout(header_layout)

        # Message label
        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)
        message_font = QFont()
        message_font.setPointSize(14)
        self.message_label.setFont(message_font)
        self.message_label.setStyleSheet("""
            QLabel {
                color: #D1D5DB;
                line-height: 1.5;
            }
        """)
        layout.addWidget(self.message_label)

        # Details label (optional, hidden by default)
        self.details_label = QLabel("")
        self.details_label.setWordWrap(True)
        self.details_label.setVisible(False)
        details_font = QFont()
        details_font.setPointSize(12)
        self.details_label.setFont(details_font)
        self.details_label.setStyleSheet("""
            QLabel {
                color: #9CA3AF;
                font-family: monospace;
                background-color: #1F2937;
                padding: 10px;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.details_label)

        # Button container
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch()

        # Retry button (hidden by default)
        self.retry_button = QPushButton("Retry")
        self.retry_button.setVisible(False)
        self.retry_button.setMinimumSize(100, 50)
        self.retry_button.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                font-size: 16px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)
        self.retry_button.clicked.connect(self.on_retry_clicked)
        button_layout.addWidget(self.retry_button)

        # Dismiss button
        self.dismiss_button = QPushButton("OK")
        self.dismiss_button.setMinimumSize(100, 50)
        self.dismiss_button.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                font-size: 16px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
            QPushButton:pressed {
                background-color: #1F2937;
            }
        """)
        self.dismiss_button.clicked.connect(self.accept)
        button_layout.addWidget(self.dismiss_button)

        layout.addLayout(button_layout)

        # Set dialog background
        self.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
        """)

        self.setLayout(layout)
        self.setMinimumWidth(500)

    def show_error(self, title, message, error_type="error", details=None, allow_retry=False):
        """
        Display an error dialog.

        Args:
            title: Error title (e.g., "Network Error", "Playback Error")
            message: User-friendly error message
            error_type: Type of error ("error", "warning", "info")
            details: Optional technical details to show
            allow_retry: Whether to show a Retry button
        """
        self.title_label.setText(title)
        self.message_label.setText(message)

        # Update icon based on error type
        if error_type == "error":
            icon_bg = "#EF4444"  # Red
            icon_text = "!"
        elif error_type == "warning":
            icon_bg = "#F59E0B"  # Orange
            icon_text = "!"
        elif error_type == "info":
            icon_bg = "#3B82F6"  # Blue
            icon_text = "i"
        else:
            icon_bg = "#EF4444"
            icon_text = "!"

        self.icon_label.setText(icon_text)
        self.icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {icon_bg};
                color: white;
                font-size: 32px;
                font-weight: bold;
                border-radius: 25px;
            }}
        """)

        # Show/hide details
        if details:
            self.details_label.setText(details)
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


def show_network_error(parent, message, details=None, allow_retry=True):
    """Helper function to show network error dialog"""
    dialog = ErrorDialog(parent)
    return dialog.show_error(
        ErrorType.NETWORK,
        message,
        error_type="error",
        details=details,
        allow_retry=allow_retry
    )


def show_playback_error(parent, message, details=None, allow_retry=True):
    """Helper function to show playback error dialog"""
    dialog = ErrorDialog(parent)
    return dialog.show_error(
        ErrorType.PLAYBACK,
        message,
        error_type="error",
        details=details,
        allow_retry=allow_retry
    )


def show_database_error(parent, message, details=None, allow_retry=False):
    """Helper function to show database error dialog"""
    dialog = ErrorDialog(parent)
    return dialog.show_error(
        ErrorType.DATABASE,
        message,
        error_type="error",
        details=details,
        allow_retry=allow_retry
    )


def show_api_error(parent, message, details=None, allow_retry=True):
    """Helper function to show API error dialog"""
    dialog = ErrorDialog(parent)
    return dialog.show_error(
        ErrorType.API,
        message,
        error_type="error",
        details=details,
        allow_retry=allow_retry
    )
