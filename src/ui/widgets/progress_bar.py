#!/usr/bin/env python3
"""
Progress bar widget for DeadStream player screen.
Provides seek functionality with time display.

Phase 9, Task 9.5 - Progress bar with seek implementation
"""

# Path manipulation for imports (file will be in src/ui/widgets/)
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class ProgressBarWidget(QWidget):
    """
    Progress bar widget with seek functionality.
    
    Features:
    - Horizontal slider for progress/seeking
    - Current time / total duration display
    - Draggable seek
    - Blue gradient fill
    - Time formatting (MM:SS)
    
    Signals:
        seek_requested: Emitted when user seeks (int: position in seconds)
    """
    
    # Signals
    seek_requested = pyqtSignal(int)  # Position in seconds
    
    def __init__(self):
        """Initialize progress bar widget"""
        super().__init__()
        
        # State
        self.current_time = 0  # Current position in seconds
        self.total_duration = 0  # Total duration in seconds
        self.is_seeking = False  # User is dragging slider
        
        # Widgets
        self.current_label = None
        self.duration_label = None
        self.slider = None
        
        self.init_ui()
    
    def init_ui(self):
        """Set up the progress bar UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Progress slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setMinimumHeight(44)  # Touch-friendly
        
        # Slider styling
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #374151;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #FFFFFF;
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -4px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #E5E7EB;
            }
            QSlider::handle:horizontal:pressed {
                background: #D1D5DB;
            }
        """)
        
        # Connect slider events
        self.slider.sliderPressed.connect(self.on_slider_pressed)
        self.slider.sliderMoved.connect(self.on_slider_moved)
        self.slider.sliderReleased.connect(self.on_slider_released)
        
        main_layout.addWidget(self.slider)
        
        # Time labels row
        time_layout = QHBoxLayout()
        time_layout.setSpacing(0)
        time_layout.setContentsMargins(0, 0, 0, 0)
        
        # Current time label (left)
        self.current_label = QLabel("0:00")
        self.current_label.setAlignment(Qt.AlignLeft)
        self.current_label.setStyleSheet("""
            QLabel {
                color: #9CA3AF;
                font-size: 14px;
            }
        """)
        time_layout.addWidget(self.current_label)
        
        # Spacer
        time_layout.addStretch()
        
        # Total duration label (right)
        self.duration_label = QLabel("0:00")
        self.duration_label.setAlignment(Qt.AlignRight)
        self.duration_label.setStyleSheet("""
            QLabel {
                color: #9CA3AF;
                font-size: 14px;
            }
        """)
        time_layout.addWidget(self.duration_label)
        
        main_layout.addLayout(time_layout)
        
        self.setLayout(main_layout)
    
    def on_slider_pressed(self):
        """Handle slider press (start seeking)"""
        self.is_seeking = True
        print("[INFO] Seeking started")
    
    def on_slider_moved(self, value):
        """
        Handle slider movement during seek.
        
        Args:
            value (int): Slider position (0-100)
        """
        if self.is_seeking and self.total_duration > 0:
            # Calculate time from slider position
            position = int((value / 100.0) * self.total_duration)
            # Update current time label
            self.current_label.setText(self.format_time(position))
            print(f"[INFO] Seeking to {self.format_time(position)}")
    
    def on_slider_released(self):
        """Handle slider release (complete seek)"""
        if self.is_seeking and self.total_duration > 0:
            # Calculate final position
            value = self.slider.value()
            position = int((value / 100.0) * self.total_duration)
            
            # Update state
            self.current_time = position
            self.is_seeking = False
            
            # Emit seek signal
            self.seek_requested.emit(position)
            print(f"[INFO] Seek completed to {position}s ({self.format_time(position)})")
    
    def update_position(self, current_seconds, total_seconds):
        """
        Update progress bar position.

        Args:
            current_seconds (int): Current playback position in seconds
            total_seconds (int): Total track duration in seconds
        """
        self.current_time = current_seconds
        self.total_duration = total_seconds

        # Update labels - current time on left, time remaining on right
        self.current_label.setText(self.format_time(current_seconds))
        remaining_seconds = max(0, total_seconds - current_seconds)
        self.duration_label.setText(f"-{self.format_time(remaining_seconds)}")

        # Update slider (only if user isn't seeking)
        if not self.is_seeking and total_seconds > 0:
            percentage = (current_seconds / total_seconds) * 100
            self.slider.setValue(int(percentage))
    
    def set_duration(self, total_seconds):
        """
        Set total duration (when track loads).

        Args:
            total_seconds (int): Total track duration in seconds
        """
        self.total_duration = total_seconds
        # Show full duration as time remaining initially (with minus sign)
        self.duration_label.setText(f"-{self.format_time(total_seconds)}")
        self.slider.setMaximum(100)  # Always use percentage
        print(f"[INFO] Duration set to {self.format_time(total_seconds)}")
    
    def reset(self):
        """Reset progress bar to initial state"""
        self.current_time = 0
        self.total_duration = 0
        self.is_seeking = False
        self.slider.setValue(0)
        self.current_label.setText("0:00")
        self.duration_label.setText("0:00")
    
    @staticmethod
    def format_time(seconds):
        """
        Format seconds as MM:SS.
        
        Args:
            seconds (int): Time in seconds
            
        Returns:
            str: Formatted time string (e.g., "3:42", "12:05")
        """
        if seconds < 0:
            seconds = 0
        
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"


if __name__ == "__main__":
    """Test the progress bar widget"""
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
    from PyQt5.QtCore import QTimer
    
    app = QApplication(sys.argv)
    
    # Create test window with timer cleanup
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.timer = None
        
        def closeEvent(self, event):
            if self.timer:
                self.timer.stop()
            event.accept()
    
    window = TestWindow()
    window.setWindowTitle("Progress Bar Test")
    window.setGeometry(100, 100, 600, 300)
    
    # Create central widget
    central = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(40, 40, 40, 40)
    
    # Add title
    title = QLabel("Progress Bar Widget Test")
    title.setFont(QFont("Arial", 18, QFont.Bold))
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("color: #FFFFFF; padding: 20px;")
    layout.addWidget(title)
    
    # Add progress bar
    progress = ProgressBarWidget()
    layout.addWidget(progress)
    
    # Connect seek signal
    progress.seek_requested.connect(
        lambda pos: print(f"[TEST] Seek requested to {pos}s ({progress.format_time(pos)})")
    )
    
    # Test instructions
    instructions = QLabel(
        "Test Instructions:\n"
        "- Drag slider to seek (watch time update)\n"
        "- Release to trigger seek signal\n"
        "- Watch auto-progress simulation below\n"
        "- Check console for seek output"
    )
    instructions.setStyleSheet("""
        QLabel {
            color: #9CA3AF;
            font-size: 12px;
            padding: 10px;
            background-color: #1F2937;
            border-radius: 8px;
        }
    """)
    layout.addWidget(instructions)
    
    # Status label
    status = QLabel("Status: Initializing...")
    status.setStyleSheet("""
        QLabel {
            color: #FFFFFF;
            font-size: 14px;
            padding: 10px;
        }
    """)
    layout.addWidget(status)
    
    layout.addStretch()
    
    central.setLayout(layout)
    window.setCentralWidget(central)
    
    # Set dark background
    window.setStyleSheet("QMainWindow { background-color: #000000; }")
    
    window.show()
    
    # Simulate playback
    current_pos = 0
    track_duration = 420  # 7 minutes
    
    def init_track():
        """Initialize with track duration"""
        progress.set_duration(track_duration)
        status.setText(f"Status: Track loaded ({progress.format_time(track_duration)} duration)")
    
    def update_progress():
        """Simulate progress updates"""
        global current_pos
        if current_pos < track_duration:
            current_pos += 1
            progress.update_position(current_pos, track_duration)
            status.setText(
                f"Status: Playing - {progress.format_time(current_pos)} / "
                f"{progress.format_time(track_duration)}"
            )
    
    # Set duration after 1 second
    QTimer.singleShot(1000, init_track)
    
    # Update progress every second
    window.timer = QTimer()
    window.timer.timeout.connect(update_progress)
    window.timer.start(1000)  # Update every 1 second
    
    sys.exit(app.exec_())
