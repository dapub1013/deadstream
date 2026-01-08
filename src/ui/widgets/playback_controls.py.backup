#!/usr/bin/env python3
"""
Playback controls widget for DeadStream player screen.
Provides main playback controls and 30-second skip functionality.

Phase 9, Task 9.4 - Playback controls implementation
"""

# Path manipulation for imports (file will be in src/ui/widgets/)
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import centralized styles
from src.ui.styles.button_styles import (
    PLAYBACK_BUTTON_STYLE, PLAY_PAUSE_BUTTON_STYLE,
    SMALL_CONTROL_BUTTON_STYLE
)
from src.ui.styles.text_styles import (
    TEXT_SUPPORTING_STYLE
)


class PlaybackControlsWidget(QWidget):
    """
    Playback controls widget with main controls and 30-second skip buttons.
    
    Features:
    - Main controls: Previous, Play/Pause, Next
    - 30-second skip: Rewind 30s, Skip 30s
    - Track counter display
    
    Signals:
        play_pause_clicked: Play/pause button pressed
        previous_clicked: Previous track button pressed
        next_clicked: Next track button pressed
        skip_backward_30s: Skip backward 30 seconds
        skip_forward_30s: Skip forward 30 seconds
    """
    
    # Signals
    play_pause_clicked = pyqtSignal()
    previous_clicked = pyqtSignal()
    next_clicked = pyqtSignal()
    skip_backward_30s = pyqtSignal()
    skip_forward_30s = pyqtSignal()
    
    def __init__(self):
        """Initialize playback controls widget"""
        super().__init__()
        
        # State
        self.is_playing = False
        self.current_track = 0
        self.total_tracks = 0
        
        # Widgets
        self.play_pause_btn = None
        self.previous_btn = None
        self.next_btn = None
        self.track_counter = None
        
        self.init_ui()
    
    def init_ui(self):
        """Set up the playback controls UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Main controls row
        main_controls = self.create_main_controls()
        main_layout.addWidget(main_controls)
        
        # 30-second skip row
        skip_controls = self.create_skip_controls()
        main_layout.addWidget(skip_controls)
        
        # Track counter
        self.track_counter = QLabel("Track 0 of 0")
        self.track_counter.setAlignment(Qt.AlignCenter)
        self.track_counter.setStyleSheet(f"""
            QLabel {{
                {TEXT_SUPPORTING_STYLE}
                padding: 5px;
            }}
        """)
        main_layout.addWidget(self.track_counter)
        
        self.setLayout(main_layout)
    
    def create_main_controls(self):
        """Create main playback control buttons"""
        container = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Previous button
        self.previous_btn = self.create_control_button(
            "Previous",
            "<<",
            enabled=False
        )
        self.previous_btn.clicked.connect(self.on_previous_clicked)
        layout.addWidget(self.previous_btn)
        
        # Play/Pause button (larger, primary)
        self.play_pause_btn = self.create_control_button(
            "Play",
            "PLAY",
            is_primary=True
        )
        self.play_pause_btn.clicked.connect(self.on_play_pause_clicked)
        layout.addWidget(self.play_pause_btn)
        
        # Next button
        self.next_btn = self.create_control_button(
            "Next",
            ">>",
            enabled=False
        )
        self.next_btn.clicked.connect(self.on_next_clicked)
        layout.addWidget(self.next_btn)
        
        container.setLayout(layout)
        return container
    
    def create_skip_controls(self):
        """Create 30-second skip buttons"""
        container = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        # Center the controls
        layout.addStretch()

        # Rewind 30s button
        rewind_btn = QPushButton("< 30s")
        rewind_btn.setMinimumSize(100, 44)
        rewind_btn.setStyleSheet(SMALL_CONTROL_BUTTON_STYLE)
        rewind_btn.clicked.connect(self.on_skip_backward_clicked)
        layout.addWidget(rewind_btn)

        # Skip 30s button
        skip_btn = QPushButton("30s >")
        skip_btn.setMinimumSize(100, 44)
        skip_btn.setStyleSheet(SMALL_CONTROL_BUTTON_STYLE)
        skip_btn.clicked.connect(self.on_skip_forward_clicked)
        layout.addWidget(skip_btn)

        layout.addStretch()

        container.setLayout(layout)
        return container
    
    def create_control_button(self, tooltip, text, is_primary=False, enabled=True):
        """
        Create a control button with consistent styling.

        Args:
            tooltip (str): Button tooltip
            text (str): Button text
            is_primary (bool): Whether this is the primary button (larger)
            enabled (bool): Initial enabled state

        Returns:
            QPushButton: Configured button
        """
        btn = QPushButton(text)
        btn.setToolTip(tooltip)

        if is_primary:
            # Larger play/pause button - use centralized style
            btn.setMinimumSize(80, 80)
            btn.setStyleSheet(PLAY_PAUSE_BUTTON_STYLE)
        else:
            # Standard control buttons - use centralized style
            btn.setMinimumSize(60, 60)
            btn.setStyleSheet(PLAYBACK_BUTTON_STYLE)
            btn.setEnabled(enabled)

        return btn
    
    def on_play_pause_clicked(self):
        """Handle play/pause button click"""
        self.is_playing = not self.is_playing
        self.update_play_pause_button()
        self.play_pause_clicked.emit()
        print(f"[INFO] Play/pause clicked - Playing: {self.is_playing}")
    
    def on_previous_clicked(self):
        """Handle previous button click"""
        if self.current_track > 1:
            print("[INFO] Previous track clicked")
            self.previous_clicked.emit()
    
    def on_next_clicked(self):
        """Handle next button click"""
        if self.current_track < self.total_tracks:
            print("[INFO] Next track clicked")
            self.next_clicked.emit()
    
    def on_skip_backward_clicked(self):
        """Handle skip backward 30s button click"""
        print("[INFO] Skip backward 30s clicked")
        self.skip_backward_30s.emit()
    
    def on_skip_forward_clicked(self):
        """Handle skip forward 30s button click"""
        print("[INFO] Skip forward 30s clicked")
        self.skip_forward_30s.emit()
    
    def update_play_pause_button(self):
        """Update play/pause button text and appearance"""
        if self.is_playing:
            self.play_pause_btn.setText("PAUSE")
            self.play_pause_btn.setToolTip("Pause")
        else:
            self.play_pause_btn.setText("PLAY")
            self.play_pause_btn.setToolTip("Play")
    
    def set_playing(self, is_playing):
        """
        Set playing state.
        
        Args:
            is_playing (bool): Whether audio is currently playing
        """
        if self.is_playing != is_playing:
            self.is_playing = is_playing
            self.update_play_pause_button()
    
    def update_track_position(self, track_num, total_tracks):
        """
        Update track counter and button states.
        
        Args:
            track_num (int): Current track number (1-indexed)
            total_tracks (int): Total number of tracks
        """
        self.current_track = track_num
        self.total_tracks = total_tracks
        
        # Update track counter
        self.track_counter.setText(f"Track {track_num} of {total_tracks}")
        
        # Update previous button state
        if self.current_track > 1:
            self.previous_btn.setEnabled(True)
        else:
            self.previous_btn.setEnabled(False)

        # Update next button state
        if self.current_track < self.total_tracks:
            self.next_btn.setEnabled(True)
        else:
            self.next_btn.setEnabled(False)

        # Styles are already set via PLAYBACK_BUTTON_STYLE which handles disabled state
    
    def reset(self):
        """Reset controls to initial state"""
        self.is_playing = False
        self.current_track = 0
        self.total_tracks = 0
        self.update_play_pause_button()
        self.track_counter.setText("Track 0 of 0")
        self.previous_btn.setEnabled(False)
        self.next_btn.setEnabled(False)


if __name__ == "__main__":
    """Test the playback controls widget"""
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
    from PyQt5.QtCore import QTimer
    
    app = QApplication(sys.argv)
    
    # Create test window
    window = QMainWindow()
    window.setWindowTitle("Playback Controls Test")
    window.setGeometry(100, 100, 600, 400)
    
    # Create central widget
    central = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(40, 40, 40, 40)
    
    # Add title
    title = QLabel("Playback Controls Widget Test")
    title.setFont(QFont("Arial", 18, QFont.Bold))
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("color: #FFFFFF; padding: 20px;")
    layout.addWidget(title)
    
    # Add playback controls
    controls = PlaybackControlsWidget()
    layout.addWidget(controls)
    
    # Connect signals
    controls.play_pause_clicked.connect(lambda: print("[TEST] Play/pause signal received"))
    controls.previous_clicked.connect(lambda: print("[TEST] Previous signal received"))
    controls.next_clicked.connect(lambda: print("[TEST] Next signal received"))
    controls.skip_backward_30s.connect(lambda: print("[TEST] Skip backward signal received"))
    controls.skip_forward_30s.connect(lambda: print("[TEST] Skip forward signal received"))
    
    # Test instructions
    instructions = QLabel(
        "Test Instructions:\n"
        "- Click PLAY to toggle play/pause state\n"
        "- Previous/Next disabled (track 0 of 0)\n"
        "- Use buttons to test signals\n"
        "- Watch console for signal output"
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
    
    layout.addStretch()
    
    central.setLayout(layout)
    window.setCentralWidget(central)
    
    # Set dark background
    window.setStyleSheet("QMainWindow { background-color: #000000; }")
    
    window.show()
    
    # Simulate track updates after 2 seconds
    def update_track():
        print("[TEST] Updating to track 3 of 8")
        controls.update_track_position(3, 8)
    
    QTimer.singleShot(2000, update_track)
    
    sys.exit(app.exec_())
