#!/usr/bin/env python3
"""
DeadStream - 7" Touchscreen Calibration Test
Phase 6 Task 6.4 (Extended)

Quick test for touch screen accuracy and calibration.
Useful when adding the physical 7" touchscreen in Phase 11.
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QFont

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


class TouchCalibrationWindow(QMainWindow):
    """
    Simple 9-point calibration test for touchscreen accuracy.
    Tests corners, edges, and center of screen.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeadStream Touch Calibration")
        
        # Test points (will be calculated based on screen size)
        self.test_points = []
        self.current_point = 0
        self.touches = []
        
        self.init_ui()
        self.setup_test_points()
        
    def init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Instructions
        self.instructions = QLabel(
            "Touch Calibration Test\n\n"
            "Tap each blue circle as accurately as possible.\n"
            "Tests will verify touch accuracy across the entire screen."
        )
        self.instructions.setAlignment(Qt.AlignCenter)
        self.instructions.setFont(QFont("Arial", 14))
        layout.addWidget(self.instructions)
        
        # Drawing area
        self.canvas = CalibrationCanvas()
        self.canvas.touch_recorded.connect(self.record_touch)
        layout.addWidget(self.canvas)
        
        # Progress
        self.progress = QLabel("Tap target 1 of 9")
        self.progress.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress)
        
        # Control button
        self.reset_btn = QPushButton("Reset Test")
        self.reset_btn.clicked.connect(self.reset_test)
        self.reset_btn.setMinimumHeight(60)
        layout.addWidget(self.reset_btn)
        
        # Theme
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                margin: 10px;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
            }
        """)
        
    def setup_test_points(self):
        """Setup 9 calibration points"""
        # Will be set when window is shown and we know size
        pass
        
    def showEvent(self, event):
        """Called when window is shown - setup test points"""
        super().showEvent(event)
        
        # Get canvas size
        width = self.canvas.width()
        height = self.canvas.height()
        
        margin = 80  # Keep targets away from edges
        
        # 9 points: 4 corners, 4 edges, 1 center
        self.test_points = [
            QPoint(margin, margin),  # Top-left
            QPoint(width // 2, margin),  # Top-center
            QPoint(width - margin, margin),  # Top-right
            QPoint(margin, height // 2),  # Middle-left
            QPoint(width // 2, height // 2),  # Center
            QPoint(width - margin, height // 2),  # Middle-right
            QPoint(margin, height - margin),  # Bottom-left
            QPoint(width // 2, height - margin),  # Bottom-center
            QPoint(width - margin, height - margin),  # Bottom-right
        ]
        
        self.canvas.set_test_points(self.test_points)
        self.canvas.set_current_target(0)
        
    def record_touch(self, touch_pos):
        """Record a touch and check accuracy"""
        if self.current_point >= len(self.test_points):
            return
            
        target = self.test_points[self.current_point]
        self.touches.append(touch_pos)
        
        # Calculate accuracy
        dx = touch_pos.x() - target.x()
        dy = touch_pos.y() - target.y()
        distance = (dx * dx + dy * dy) ** 0.5
        
        print(f"[INFO] Point {self.current_point + 1}/9:")
        print(f"       Target: ({target.x()}, {target.y()})")
        print(f"       Touch:  ({touch_pos.x()}, {touch_pos.y()})")
        print(f"       Error:  {distance:.1f} pixels")
        
        # Move to next point
        self.current_point += 1
        
        if self.current_point < len(self.test_points):
            self.canvas.set_current_target(self.current_point)
            self.progress.setText(f"Tap target {self.current_point + 1} of 9")
        else:
            self.show_results()
            
    def show_results(self):
        """Display calibration results"""
        if not self.touches:
            return
            
        # Calculate average error
        total_error = 0
        max_error = 0
        
        for i, touch in enumerate(self.touches):
            target = self.test_points[i]
            dx = touch.x() - target.x()
            dy = touch.y() - target.y()
            error = (dx * dx + dy * dy) ** 0.5
            total_error += error
            max_error = max(max_error, error)
            
        avg_error = total_error / len(self.touches)
        
        print()
        print("=" * 60)
        print("Calibration Results:")
        print("=" * 60)
        print(f"Average error: {avg_error:.1f} pixels")
        print(f"Maximum error: {max_error:.1f} pixels")
        
        # Evaluate
        if avg_error < 20:
            result = "EXCELLENT - Touch is very accurate"
            status = "[PASS]"
        elif avg_error < 40:
            result = "GOOD - Touch is acceptably accurate"
            status = "[PASS]"
        elif avg_error < 60:
            result = "FAIR - Consider recalibration"
            status = "[WARN]"
        else:
            result = "POOR - Touchscreen needs calibration"
            status = "[FAIL]"
            
        print(f"{status} {result}")
        print("=" * 60)
        
        self.instructions.setText(
            f"Calibration Complete!\n\n"
            f"Average Error: {avg_error:.1f} pixels\n"
            f"{result}"
        )
        self.progress.setText("Test complete - Press Reset to try again")
        
    def reset_test(self):
        """Reset the calibration test"""
        self.current_point = 0
        self.touches = []
        self.canvas.set_current_target(0)
        self.progress.setText("Tap target 1 of 9")
        self.instructions.setText(
            "Touch Calibration Test\n\n"
            "Tap each blue circle as accurately as possible.\n"
            "Tests will verify touch accuracy across the entire screen."
        )
        print("[INFO] Test reset")


class CalibrationCanvas(QWidget):
    """Canvas widget for drawing calibration targets"""
    
    from PyQt5.QtCore import pyqtSignal
    touch_recorded = pyqtSignal(QPoint)
    
    def __init__(self):
        super().__init__()
        self.test_points = []
        self.current_target = 0
        self.setMinimumSize(600, 400)
        
    def set_test_points(self, points):
        """Set the test points to draw"""
        self.test_points = points
        self.update()
        
    def set_current_target(self, index):
        """Set which target is currently active"""
        self.current_target = index
        self.update()
        
    def paintEvent(self, event):
        """Draw the calibration targets"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw all points
        for i, point in enumerate(self.test_points):
            if i < self.current_target:
                # Already touched - show green
                painter.setPen(QPen(QColor(34, 197, 94), 2))
                painter.setBrush(QColor(34, 197, 94, 100))
                painter.drawEllipse(point, 15, 15)
            elif i == self.current_target:
                # Current target - show blue
                painter.setPen(QPen(QColor(37, 99, 235), 3))
                painter.setBrush(QColor(37, 99, 235, 100))
                painter.drawEllipse(point, 30, 30)
                # Draw crosshair
                painter.drawLine(point.x() - 40, point.y(), point.x() + 40, point.y())
                painter.drawLine(point.x(), point.y() - 40, point.x(), point.y() + 40)
            else:
                # Future target - show gray
                painter.setPen(QPen(QColor(156, 163, 175), 1))
                painter.setBrush(QColor(156, 163, 175, 50))
                painter.drawEllipse(point, 10, 10)
                
    def mousePressEvent(self, event):
        """Handle mouse/touch press"""
        if self.current_target < len(self.test_points):
            self.touch_recorded.emit(event.pos())


def main():
    """Run the calibration test"""
    print("=" * 60)
    print("DeadStream Touch Calibration Test")
    print("=" * 60)
    print()
    print("[INFO] This test validates touchscreen accuracy")
    print("[INFO] Tap each blue circle as accurately as possible")
    print()
    
    app = QApplication(sys.argv)
    window = TouchCalibrationWindow()
    
    # Set to target screen size (can be windowed for testing)
    window.setGeometry(100, 100, 1024, 600)
    window.show()
    
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
