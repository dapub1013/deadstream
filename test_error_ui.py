#!/usr/bin/env python3
"""
Test Error Handling UI - Task 10.3

Tests the new error dialog, toast notifications, and loading indicators.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from src.ui.widgets.error_dialog import ErrorDialog, show_playback_error, show_network_error, show_database_error
from src.ui.widgets.toast_notification import ToastManager
from src.ui.widgets.loading_spinner import LoadingOverlay, LoadingIndicator


class ErrorUITestWindow(QMainWindow):
    """Test window for error handling UI components"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error UI Test - DeadStream Phase 10.3")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Create layout
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Error Handling UI Test Suite")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #F3F4F6; margin-bottom: 20px;")
        layout.addWidget(title)

        # Error Dialog Tests
        dialog_label = QLabel("Error Dialogs:")
        dialog_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #D1D5DB; margin-top: 10px;")
        layout.addWidget(dialog_label)

        btn_network_error = QPushButton("Test Network Error Dialog")
        btn_network_error.clicked.connect(self.test_network_error)
        layout.addWidget(btn_network_error)

        btn_playback_error = QPushButton("Test Playback Error Dialog")
        btn_playback_error.clicked.connect(self.test_playback_error)
        layout.addWidget(btn_playback_error)

        btn_database_error = QPushButton("Test Database Error Dialog")
        btn_database_error.clicked.connect(self.test_database_error)
        layout.addWidget(btn_database_error)

        # Toast Notification Tests
        toast_label = QLabel("Toast Notifications:")
        toast_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #D1D5DB; margin-top: 20px;")
        layout.addWidget(toast_label)

        btn_toast_info = QPushButton("Test Info Toast")
        btn_toast_info.clicked.connect(self.test_toast_info)
        layout.addWidget(btn_toast_info)

        btn_toast_success = QPushButton("Test Success Toast")
        btn_toast_success.clicked.connect(self.test_toast_success)
        layout.addWidget(btn_toast_success)

        btn_toast_warning = QPushButton("Test Warning Toast")
        btn_toast_warning.clicked.connect(self.test_toast_warning)
        layout.addWidget(btn_toast_warning)

        btn_toast_error = QPushButton("Test Error Toast")
        btn_toast_error.clicked.connect(self.test_toast_error)
        layout.addWidget(btn_toast_error)

        btn_toast_queue = QPushButton("Test Toast Queue (3 toasts)")
        btn_toast_queue.clicked.connect(self.test_toast_queue)
        layout.addWidget(btn_toast_queue)

        # Loading Spinner Tests
        spinner_label = QLabel("Loading Indicators:")
        spinner_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #D1D5DB; margin-top: 20px;")
        layout.addWidget(spinner_label)

        btn_loading_overlay = QPushButton("Test Loading Overlay (3 seconds)")
        btn_loading_overlay.clicked.connect(self.test_loading_overlay)
        layout.addWidget(btn_loading_overlay)

        btn_loading_cancel = QPushButton("Test Loading with Cancel")
        btn_loading_cancel.clicked.connect(self.test_loading_with_cancel)
        layout.addWidget(btn_loading_cancel)

        # Create toast manager
        self.toast_manager = ToastManager(self)

        # Create loading overlay
        self.loading_overlay = LoadingOverlay(self)

        # Dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #111827;
            }
            QPushButton {
                background-color: #374151;
                color: white;
                font-size: 14px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
            QPushButton:pressed {
                background-color: #1F2937;
            }
        """)

    # ========================================================================
    # ERROR DIALOG TESTS
    # ========================================================================

    def test_network_error(self):
        """Test network error dialog"""
        print("[TEST] Showing network error dialog...")
        dialog = ErrorDialog(self)
        result = dialog.show_error(
            "Network Error",
            "Unable to connect to the Internet Archive. Please check your network connection and try again.",
            error_type="error",
            details="Connection timeout after 30 seconds",
            allow_retry=True
        )
        print(f"[TEST] Dialog result: {result}")

    def test_playback_error(self):
        """Test playback error dialog"""
        print("[TEST] Showing playback error dialog...")
        show_playback_error(
            self,
            "Unable to play 'Dark Star'. The audio stream may be unavailable or in an unsupported format.",
            details="VLC error code: 404 - Stream not found",
            allow_retry=True
        )

    def test_database_error(self):
        """Test database error dialog"""
        print("[TEST] Showing database error dialog...")
        show_database_error(
            self,
            "Database file not found or corrupted. Please verify the database is installed correctly.",
            details="/path/to/deadstream.db missing",
            allow_retry=False
        )

    # ========================================================================
    # TOAST NOTIFICATION TESTS
    # ========================================================================

    def test_toast_info(self):
        """Test info toast"""
        print("[TEST] Showing info toast...")
        self.toast_manager.show_info("Loading Dark Star from 5/8/1977...")

    def test_toast_success(self):
        """Test success toast"""
        print("[TEST] Showing success toast...")
        self.toast_manager.show_success("Show added to favorites!")

    def test_toast_warning(self):
        """Test warning toast"""
        print("[TEST] Showing warning toast...")
        self.toast_manager.show_warning("Network connection is slow. Audio may buffer.")

    def test_toast_error(self):
        """Test error toast"""
        print("[TEST] Showing error toast...")
        self.toast_manager.show_error("Failed to load track. Check your connection.")

    def test_toast_queue(self):
        """Test toast queueing"""
        print("[TEST] Showing 3 queued toasts...")
        self.toast_manager.show_info("First toast - info")
        self.toast_manager.show_success("Second toast - success")
        self.toast_manager.show_warning("Third toast - warning")

    # ========================================================================
    # LOADING SPINNER TESTS
    # ========================================================================

    def test_loading_overlay(self):
        """Test loading overlay"""
        print("[TEST] Showing loading overlay for 3 seconds...")
        self.loading_overlay.show_loading("Loading shows from database...")
        # Hide after 3 seconds
        QTimer.singleShot(3000, self.loading_overlay.hide_loading)

    def test_loading_with_cancel(self):
        """Test loading overlay with cancel button"""
        print("[TEST] Showing loading overlay with cancel...")
        self.loading_overlay.cancel_requested.connect(self.on_loading_cancelled)
        self.loading_overlay.show_loading("Loading large dataset...", allow_cancel=True)
        # Auto-hide after 10 seconds if not cancelled
        QTimer.singleShot(10000, self.loading_overlay.hide_loading)

    def on_loading_cancelled(self):
        """Handle loading cancellation"""
        print("[TEST] Loading cancelled by user")
        self.toast_manager.show_info("Loading cancelled")


def main():
    """Run the test application"""
    app = QApplication(sys.argv)

    window = ErrorUITestWindow()
    window.show()

    print("\n" + "="*60)
    print("DeadStream Error UI Test Suite - Phase 10.3")
    print("="*60)
    print("\nTest each button to verify error handling UI components:")
    print("  - Error dialogs (modal, with retry option)")
    print("  - Toast notifications (non-blocking, auto-dismiss)")
    print("  - Loading indicators (overlay, with cancel)")
    print("\nAll UI elements should match the DeadStream dark theme.")
    print("="*60 + "\n")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
