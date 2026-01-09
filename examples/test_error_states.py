#!/usr/bin/env python3
"""
Test Error States - Phase 10E.7

Tests polished error dialogs and toast notifications with Theme Manager integration.

Usage:
    python3 examples/test_error_states.py
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from src.ui.styles.theme import Theme
from src.ui.widgets.error_dialog import (
    ErrorDialog, show_network_error, show_playback_error,
    show_database_error, show_api_error
)
from src.ui.widgets.toast_notification import ToastManager
from src.ui.widgets.error_messages import ErrorMessages, ErrorMessageFormatter


class ErrorTestWindow(QWidget):
    """Test window for error states"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error States Test - Phase 10E.7")
        self.resize(1024, 600)
        self.setup_ui()

        # Toast manager
        self.toast_manager = ToastManager(self)

    def setup_ui(self):
        """Set up the test UI"""
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_MEDIUM)
        layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE
        )

        # Title
        title = QLabel("Error States Test - Phase 10E.7")
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setFamily(Theme.FONT_FAMILY)
        font.setPointSize(Theme.HEADER_MEDIUM)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        layout.addWidget(title)

        # Description
        desc = QLabel("Test polished error dialogs and toast notifications with helpful suggestions")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc_font = QFont()
        desc_font.setFamily(Theme.FONT_FAMILY)
        desc_font.setPointSize(Theme.BODY_MEDIUM)
        desc.setFont(desc_font)
        desc.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        layout.addWidget(desc)

        layout.addSpacing(Theme.SPACING_LARGE)

        # Error Dialog Tests
        error_label = QLabel("Error Dialogs:")
        error_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-weight: bold;")
        layout.addWidget(error_label)

        # Network Error
        btn_network = self.create_test_button("Network Error (with retry)")
        btn_network.clicked.connect(self.test_network_error)
        layout.addWidget(btn_network)

        # Playback Error
        btn_playback = self.create_test_button("Playback Error (with suggestion)")
        btn_playback.clicked.connect(self.test_playback_error)
        layout.addWidget(btn_playback)

        # Database Error
        btn_database = self.create_test_button("Database Error (with details)")
        btn_database.clicked.connect(self.test_database_error)
        layout.addWidget(btn_database)

        # API Error
        btn_api = self.create_test_button("API Error (rate limit)")
        btn_api.clicked.connect(self.test_api_error)
        layout.addWidget(btn_api)

        layout.addSpacing(Theme.SPACING_MEDIUM)

        # Toast Notification Tests
        toast_label = QLabel("Toast Notifications:")
        toast_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-weight: bold;")
        layout.addWidget(toast_label)

        # Info Toast
        btn_toast_info = self.create_test_button("Info Toast")
        btn_toast_info.clicked.connect(self.test_toast_info)
        layout.addWidget(btn_toast_info)

        # Success Toast
        btn_toast_success = self.create_test_button("Success Toast")
        btn_toast_success.clicked.connect(self.test_toast_success)
        layout.addWidget(btn_toast_success)

        # Warning Toast
        btn_toast_warning = self.create_test_button("Warning Toast")
        btn_toast_warning.clicked.connect(self.test_toast_warning)
        layout.addWidget(btn_toast_warning)

        # Error Toast
        btn_toast_error = self.create_test_button("Error Toast")
        btn_toast_error.clicked.connect(self.test_toast_error)
        layout.addWidget(btn_toast_error)

        # Sequential Toast Test
        btn_toast_seq = self.create_test_button("Multiple Toasts (Sequential)")
        btn_toast_seq.clicked.connect(self.test_toast_sequential)
        layout.addWidget(btn_toast_seq)

        layout.addStretch()

        # Set background
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme.BG_PRIMARY};
            }}
        """)

        self.setLayout(layout)

    def create_test_button(self, text):
        """Create a styled test button"""
        button = QPushButton(text)
        button.setMinimumHeight(Theme.BUTTON_HEIGHT)
        button.setStyleSheet(f"""
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
        return button

    def test_network_error(self):
        """Test network error dialog"""
        print("[TEST] Showing network error dialog with retry button")
        show_network_error(
            self,
            message="Unable to connect to archive.org",
            details="Connection timeout after 30 seconds",
            allow_retry=True
        )

    def test_playback_error(self):
        """Test playback error dialog"""
        print("[TEST] Showing playback error dialog with suggestion")
        error = ErrorMessages.PLAYBACK_NO_AUDIO
        dialog = ErrorDialog(self)
        dialog.show_error(
            title=error["title"],
            message=error["message"],
            suggestion=error["suggestion"],
            error_type="error",
            allow_retry=True
        )

    def test_database_error(self):
        """Test database error dialog"""
        print("[TEST] Showing database error dialog with technical details")
        show_database_error(
            self,
            message="Failed to query shows from database",
            details="sqlite3.OperationalError: no such table: shows",
            allow_retry=False
        )

    def test_api_error(self):
        """Test API error dialog"""
        print("[TEST] Showing API rate limit error")
        error = ErrorMessages.API_RATE_LIMIT
        dialog = ErrorDialog(self)
        dialog.show_error(
            title=error["title"],
            message=error["message"],
            suggestion=error["suggestion"],
            error_type="warning",
            allow_retry=False
        )

    def test_toast_info(self):
        """Test info toast"""
        print("[TEST] Showing info toast")
        self.toast_manager.show_info("Show added to queue", duration=3000)

    def test_toast_success(self):
        """Test success toast"""
        print("[TEST] Showing success toast")
        self.toast_manager.show_success("Database updated successfully", duration=3000)

    def test_toast_warning(self):
        """Test warning toast"""
        print("[TEST] Showing warning toast")
        self.toast_manager.show_warning("Low disk space for audio cache", duration=3000)

    def test_toast_error(self):
        """Test error toast"""
        print("[TEST] Showing error toast")
        self.toast_manager.show_error("Failed to load audio stream", duration=3000)

    def test_toast_sequential(self):
        """Test multiple toasts shown sequentially"""
        print("[TEST] Showing multiple toasts in sequence")
        self.toast_manager.show_info("Loading show metadata...", duration=2000)
        self.toast_manager.show_success("Show loaded successfully", duration=2000)
        self.toast_manager.show_info("Starting playback...", duration=2000)


def main():
    """Main test function"""
    print("[INFO] Starting Error States Test - Phase 10E.7")
    print("[INFO] Testing error dialogs and toast notifications")
    print("[INFO] All errors should use Theme Manager colors")
    print("[INFO] All errors should have helpful suggestions")
    print()

    app = QApplication(sys.argv)

    # Create test window
    window = ErrorTestWindow()
    window.show()

    print("[INFO] Test window displayed")
    print("[INFO] Click buttons to test different error states")
    print()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
