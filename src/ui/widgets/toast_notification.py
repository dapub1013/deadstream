"""
Toast Notification Widget

Displays temporary non-blocking notifications at the top of the screen.
"""

from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont


class ToastNotification(QLabel):
    """
    Non-blocking toast notification that appears at top of screen.

    Features:
    - Auto-dismiss after configurable timeout
    - Fade in/out animations
    - Different styles for info, warning, error, success
    - Click to dismiss
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
        self.setMinimumWidth(400)
        self.setMaximumWidth(600)

        # Set up opacity effect for fade animations
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

        # Auto-dismiss timer
        self.dismiss_timer = QTimer()
        self.dismiss_timer.setSingleShot(True)
        self.dismiss_timer.timeout.connect(self.fade_out)

        # Animation for fade in/out
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.finished.connect(self.on_animation_finished)

        self._is_fading_out = False

        # Make clickable to dismiss
        self.mousePressEvent = lambda event: self.fade_out()

    def show_toast(self, message, toast_type="info", duration=5000):
        """
        Show a toast notification.

        Args:
            message: Text to display
            toast_type: "info", "success", "warning", or "error"
            duration: How long to show in milliseconds (0 = manual dismiss only)
        """
        self.setText(message)

        # Set styling based on type
        if toast_type == "info":
            bg_color = "#3B82F6"  # Blue
            text_color = "white"
            icon = "ℹ"
        elif toast_type == "success":
            bg_color = "#10B981"  # Green
            text_color = "white"
            icon = "✓"
        elif toast_type == "warning":
            bg_color = "#F59E0B"  # Orange
            text_color = "white"
            icon = "⚠"
        elif toast_type == "error":
            bg_color = "#EF4444"  # Red
            text_color = "white"
            icon = "✕"
        else:
            bg_color = "#374151"  # Gray
            text_color = "white"
            icon = ""

        # Add icon to message
        if icon:
            display_text = f"{icon}  {message}"
        else:
            display_text = message

        self.setText(display_text)

        # Apply stylesheet
        font = QFont()
        font.setPointSize(14)
        font.setWeight(QFont.Medium)
        self.setFont(font)

        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                padding: 15px 25px;
                border-radius: 8px;
                border: none;
            }}
        """)

        # Adjust size to content
        self.adjustSize()

        # Position at top center of parent
        if self.parent():
            parent_rect = self.parent().rect()
            x = (parent_rect.width() - self.width()) // 2
            y = 20  # 20px from top
            self.move(x, y)

        # Show and fade in
        self._is_fading_out = False
        self.show()
        self.fade_in()

        # Set auto-dismiss timer
        if duration > 0:
            self.dismiss_timer.start(duration)

    def fade_in(self):
        """Fade in animation"""
        self.fade_animation.stop()
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def fade_out(self):
        """Fade out animation"""
        if self._is_fading_out:
            return  # Already fading out

        self._is_fading_out = True
        self.dismiss_timer.stop()
        self.fade_animation.stop()
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.start()

    def on_animation_finished(self):
        """Handle animation completion"""
        if self._is_fading_out:
            self.hide()
            self._is_fading_out = False


class ToastManager:
    """
    Manages multiple toast notifications for a parent widget.

    Ensures only one toast is shown at a time and queues additional toasts.
    """

    def __init__(self, parent):
        self.parent = parent
        self.current_toast = None
        self.toast_queue = []

    def show_info(self, message, duration=5000):
        """Show info toast"""
        self._show_toast(message, "info", duration)

    def show_success(self, message, duration=5000):
        """Show success toast"""
        self._show_toast(message, "success", duration)

    def show_warning(self, message, duration=5000):
        """Show warning toast"""
        self._show_toast(message, "warning", duration)

    def show_error(self, message, duration=5000):
        """Show error toast"""
        self._show_toast(message, "error", duration)

    def _show_toast(self, message, toast_type, duration):
        """Internal method to show or queue a toast"""
        if self.current_toast and self.current_toast.isVisible():
            # Queue this toast
            self.toast_queue.append((message, toast_type, duration))
        else:
            # Show immediately
            self._display_toast(message, toast_type, duration)

    def _display_toast(self, message, toast_type, duration):
        """Display a toast notification"""
        if self.current_toast is None:
            self.current_toast = ToastNotification(self.parent)

        self.current_toast.show_toast(message, toast_type, duration)

        # Set up callback to show next queued toast
        if duration > 0:
            QTimer.singleShot(duration + 300, self._show_next_queued)  # +300ms for fade out

    def _show_next_queued(self):
        """Show next toast in queue"""
        if self.toast_queue:
            message, toast_type, duration = self.toast_queue.pop(0)
            self._display_toast(message, toast_type, duration)

    def clear_queue(self):
        """Clear all queued toasts"""
        self.toast_queue.clear()

    def dismiss_current(self):
        """Dismiss currently showing toast"""
        if self.current_toast:
            self.current_toast.fade_out()
