#!/usr/bin/env python3
"""
Volume Control Widget for DeadStream Player Screen.
Provides volume slider and mute button with visual feedback.

Phase 9, Task 9.7 - Volume Control Implementation
"""

# Path manipulation for imports (file in src/ui/widgets/)
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QSlider, QLabel, QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class VolumeControlWidget(QWidget):
    """
    Volume control widget with slider and mute button.
    
    Features:
    - Volume slider (0-100%)
    - Mute/unmute button
    - Visual volume percentage display
    - Touch-optimized sizing
    
    Signals:
        volume_changed(int): Volume changed to new level (0-100)
        mute_toggled(bool): Mute state toggled (True=muted, False=unmuted)
    """
    
    # Signals
    volume_changed = pyqtSignal(int)  # New volume level (0-100)
    mute_toggled = pyqtSignal(bool)   # True if muted, False if unmuted
    
    def __init__(self, parent=None):
        """Initialize volume control widget"""
        super().__init__(parent)
        
        # State
        self.current_volume = 50      # Default volume
        self.is_muted = False         # Mute state
        self.volume_before_mute = 50  # Volume to restore after unmute
        
        # UI elements
        self.mute_button = None
        self.volume_slider = None
        self.volume_label = None
        
        self.init_ui()
    
    def init_ui(self):
        """Set up the volume control UI"""
        # Main horizontal layout
        layout = QHBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Mute button (left)
        self.mute_button = QPushButton()
        self.mute_button.setFixedSize(50, 50)
        self._update_mute_button_icon()
        self.mute_button.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                border: none;
                border-radius: 8px;
                font-size: 20px;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:pressed {
                background-color: #4B5563;
            }
        """)
        self.mute_button.clicked.connect(self.on_mute_clicked)
        layout.addWidget(self.mute_button)
        
        # Volume slider (center, expandable)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.current_volume)
        self.volume_slider.setMinimumHeight(50)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #1F2937;
                height: 12px;
                border-radius: 6px;
            }
            QSlider::handle:horizontal {
                background: #8B5CF6;
                width: 28px;
                height: 28px;
                margin: -8px 0;
                border-radius: 14px;
            }
            QSlider::handle:horizontal:hover {
                background: #A78BFA;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366F1, stop:1 #8B5CF6);
                border-radius: 6px;
            }
        """)
        self.volume_slider.valueChanged.connect(self.on_volume_slider_changed)
        layout.addWidget(self.volume_slider, stretch=1)
        
        # Volume percentage label (right)
        self.volume_label = QLabel(f"{self.current_volume}%")
        self.volume_label.setFixedWidth(60)
        self.volume_label.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 16, QFont.Bold)
        self.volume_label.setFont(font)
        self.volume_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.volume_label)
        
        self.setLayout(layout)
    
    def on_mute_clicked(self):
        """Handle mute button click"""
        self.toggle_mute()
    
    def on_volume_slider_changed(self, value):
        """
        Handle volume slider value change.
        
        Args:
            value (int): New volume level (0-100)
        """
        # If muted and user moves slider, unmute
        if self.is_muted and value > 0:
            self.is_muted = False
            self._update_mute_button_icon()
        
        self.current_volume = value
        self.volume_label.setText(f"{value}%")
        
        print(f"[INFO] Volume slider changed to {value}%")
        self.volume_changed.emit(value)
    
    def set_volume(self, volume):
        """
        Set volume level programmatically.
        
        Args:
            volume (int): Volume level (0-100)
        """
        # Validate input
        if not isinstance(volume, (int, float)):
            print(f"[ERROR] Volume must be a number, got {type(volume)}")
            return
        
        # Clamp to valid range
        volume = max(0, min(100, int(volume)))
        
        # Update slider (this will trigger on_volume_slider_changed)
        self.volume_slider.setValue(volume)
        
        print(f"[INFO] Volume set to {volume}%")
    
    def get_volume(self):
        """
        Get current volume level.
        
        Returns:
            int: Current volume (0-100)
        """
        return self.current_volume
    
    def mute(self):
        """Mute audio"""
        if self.is_muted:
            print("[INFO] Already muted")
            return
        
        # Save current volume
        self.volume_before_mute = self.current_volume
        
        # Set to muted
        self.is_muted = True
        
        # Update UI
        self._update_mute_button_icon()
        
        print("[INFO] Audio muted")
        self.mute_toggled.emit(True)
    
    def unmute(self):
        """Unmute audio (restore previous volume)"""
        if not self.is_muted:
            print("[INFO] Already unmuted")
            return
        
        # Restore previous volume
        self.is_muted = False
        
        # Update UI
        self._update_mute_button_icon()
        self.volume_slider.setValue(self.volume_before_mute)
        
        print(f"[INFO] Audio unmuted (restored to {self.volume_before_mute}%)")
        self.mute_toggled.emit(False)
    
    def toggle_mute(self):
        """Toggle mute state"""
        if self.is_muted:
            self.unmute()
        else:
            self.mute()
    
    def is_currently_muted(self):
        """
        Check if currently muted.
        
        Returns:
            bool: True if muted, False otherwise
        """
        return self.is_muted
    
    def _update_mute_button_icon(self):
        """Update mute button icon based on state"""
        if self.is_muted:
            # Muted - show speaker with X
            self.mute_button.setText("🔇")
        else:
            # Unmuted - show speaker
            self.mute_button.setText("🔊")


if __name__ == "__main__":
    """Test the volume control widget"""
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("DeadStream Volume Control - Task 9.7")
    window.setGeometry(100, 100, 600, 200)
    
    # Central widget
    central = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(30, 30, 30, 30)
    
    # Add volume control
    volume_control = VolumeControlWidget()
    
    # Connect signals for testing
    volume_control.volume_changed.connect(
        lambda v: print(f"[TEST] Volume changed signal: {v}%")
    )
    volume_control.mute_toggled.connect(
        lambda m: print(f"[TEST] Mute toggled signal: {'MUTED' if m else 'UNMUTED'}")
    )
    
    layout.addWidget(volume_control)
    
    # Info label
    info_label = QLabel(
        "Test the volume control:\n"
        "- Drag slider to change volume\n"
        "- Click speaker button to mute/unmute\n"
        "- Moving slider while muted will unmute\n"
        "- Check console for signal output"
    )
    info_label.setStyleSheet("""
        color: #9CA3AF;
        padding: 20px;
        font-size: 14px;
    """)
    info_label.setWordWrap(True)
    layout.addWidget(info_label)
    
    central.setLayout(layout)
    window.setCentralWidget(central)
    
    # Set dark background
    window.setStyleSheet("background-color: #000000;")
    
    window.show()
    
    print("\n=== Volume Control Widget Test (Task 9.7) ===")
    print("Volume control widget loaded")
    print("Default volume: 50%")
    print("Test all interactions:")
    print("  - Slider movement")
    print("  - Mute button")
    print("  - Unmute by moving slider")
    print("============================================\n")
    
    sys.exit(app.exec_())
