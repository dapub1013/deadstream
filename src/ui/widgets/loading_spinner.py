"""
Loading Spinner Widget

Animated loading indicator to replace text-only loading states.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont


class LoadingSpinner(QWidget):
    """
    Animated circular loading spinner.

    Features:
    - Smooth rotation animation
    - Customizable color and size
    - Optional cancel button
    - Optional loading message
    """

    cancel_requested = pyqtSignal()

    def __init__(self, parent=None, size=60, color="#3B82F6"):
        super().__init__(parent)
        self.size = size
        self.color = QColor(color)
        self.angle = 0
        self.setFixedSize(size, size)

        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)

    def start(self):
        """Start the spinning animation"""
        self.timer.start(50)  # Update every 50ms (20fps)
        self.show()

    def stop(self):
        """Stop the spinning animation"""
        self.timer.stop()
        self.hide()

    def rotate(self):
        """Rotate the spinner"""
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        """Paint the spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Center point
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = min(center_x, center_y) - 5

        # Draw circular arc
        pen = QPen(self.color)
        pen.setWidth(4)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        # Rotate painter
        painter.translate(center_x, center_y)
        painter.rotate(self.angle)
        painter.translate(-center_x, -center_y)

        # Draw arc (270 degrees)
        painter.drawArc(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2,
            0,  # Start angle
            270 * 16  # Span angle (Qt uses 1/16th degree units)
        )


class LoadingOverlay(QWidget):
    """
    Full loading overlay with spinner, message, and optional cancel button.

    Shows centered spinner with loading message and optional cancel action.
    """

    cancel_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Initialize the overlay UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Spinner
        self.spinner = LoadingSpinner(self, size=80, color="#3B82F6")
        spinner_container = QWidget()
        spinner_layout = QVBoxLayout(spinner_container)
        spinner_layout.setAlignment(Qt.AlignCenter)
        spinner_layout.addWidget(self.spinner)
        layout.addWidget(spinner_container)

        # Message label
        self.message_label = QLabel("Loading...")
        self.message_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setWeight(QFont.Medium)
        self.message_label.setFont(font)
        self.message_label.setStyleSheet("color: #D1D5DB;")
        layout.addWidget(self.message_label)

        # Cancel button (hidden by default)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setVisible(False)
        self.cancel_button.setMinimumSize(120, 50)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                font-size: 14px;
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
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        cancel_container = QWidget()
        cancel_layout = QVBoxLayout(cancel_container)
        cancel_layout.setAlignment(Qt.AlignCenter)
        cancel_layout.addWidget(self.cancel_button)
        layout.addWidget(cancel_container)

        self.setLayout(layout)

        # Semi-transparent background
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(17, 24, 39, 0.9);
            }
        """)

        # Initially hidden
        self.hide()

    def show_loading(self, message="Loading...", allow_cancel=False):
        """
        Show the loading overlay.

        Args:
            message: Loading message to display
            allow_cancel: Whether to show cancel button
        """
        self.message_label.setText(message)
        self.cancel_button.setVisible(allow_cancel)

        # Resize to fill parent
        if self.parent():
            self.setGeometry(self.parent().rect())

        self.show()
        self.raise_()  # Bring to front
        self.spinner.start()

    def hide_loading(self):
        """Hide the loading overlay"""
        self.spinner.stop()
        self.hide()

    def on_cancel_clicked(self):
        """Handle cancel button click"""
        self.cancel_requested.emit()
        self.hide_loading()

    def resizeEvent(self, event):
        """Handle parent resize"""
        if self.parent():
            self.setGeometry(self.parent().rect())
        super().resizeEvent(event)


class LoadingIndicator(QWidget):
    """
    Inline loading indicator (non-overlay).

    Smaller loading indicator suitable for embedding in layouts.
    """

    def __init__(self, parent=None, message="Loading..."):
        super().__init__(parent)
        self.setup_ui(message)

    def setup_ui(self, message):
        """Initialize the indicator UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Spinner
        self.spinner = LoadingSpinner(self, size=40, color="#3B82F6")
        spinner_container = QWidget()
        spinner_layout = QVBoxLayout(spinner_container)
        spinner_layout.setAlignment(Qt.AlignCenter)
        spinner_layout.addWidget(self.spinner)
        layout.addWidget(spinner_container)

        # Message
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        self.message_label.setFont(font)
        self.message_label.setStyleSheet("color: #9CA3AF;")
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def start(self, message=None):
        """Start the spinner"""
        if message:
            self.message_label.setText(message)
        self.spinner.start()
        self.show()

    def stop(self):
        """Stop the spinner"""
        self.spinner.stop()
        self.hide()

    def set_message(self, message):
        """Update the loading message"""
        self.message_label.setText(message)
