#!/usr/bin/env python3
"""
PyQt5 Learning Exercise 3: Mini Music Player (FIXED)
Demonstrates: UI integration with backend, timers, real-time updates
Connects PyQt5 to the actual VLC audio engine from Phase 4
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QSlider, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor

from src.audio.resilient_player import ResilientPlayer, PlayerState
from src.database.queries import get_show_by_date
from src.api.metadata import get_metadata, extract_audio_files

class MiniMusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.player = None
        self.current_url = None
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_playback_info)
        self.init_ui()
        self.load_test_track()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("DeadStream Mini Player - VLC Integration Test")
        self.setGeometry(100, 100, 600, 400)
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Mini Music Player")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; margin: 15px; font-weight: bold;")
        layout.addWidget(title)
        
        # Track info
        self.track_label = QLabel("Loading track...")
        self.track_label.setAlignment(Qt.AlignCenter)
        self.track_label.setStyleSheet("font-size: 14px; color: #90CAF9; margin: 10px;")
        self.track_label.setWordWrap(True)
        layout.addWidget(self.track_label)
        
        # Status label
        self.status_label = QLabel("Status: Initializing")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12px; color: #81C784; margin: 5px;")
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v / %m seconds")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #424242;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #1976D2;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Time labels
        time_layout = QHBoxLayout()
        self.current_time_label = QLabel("0:00")
        self.current_time_label.setStyleSheet("font-size: 11px; color: #BDBDBD;")
        time_layout.addWidget(self.current_time_label)
        
        time_layout.addStretch()
        
        self.total_time_label = QLabel("0:00")
        self.total_time_label.setStyleSheet("font-size: 11px; color: #BDBDBD;")
        time_layout.addWidget(self.total_time_label)
        
        layout.addLayout(time_layout)
        
        layout.addSpacing(20)
        
        # Playback controls
        controls_layout = QHBoxLayout()
        controls_layout.addStretch()
        
        # Play button
        self.play_button = QPushButton("Play")
        self.play_button.setFixedSize(80, 60)
        self.play_button.setStyleSheet(self.get_button_style("#43A047"))
        self.play_button.clicked.connect(self.play_pause)
        controls_layout.addWidget(self.play_button)
        
        # Stop button
        stop_button = QPushButton("Stop")
        stop_button.setFixedSize(80, 60)
        stop_button.setStyleSheet(self.get_button_style("#E53935"))
        stop_button.clicked.connect(self.stop)
        controls_layout.addWidget(stop_button)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        layout.addSpacing(20)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume:")
        volume_label.setStyleSheet("font-size: 12px;")
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(75)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #424242;
                height: 8px;
                background: #424242;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #1976D2;
                border: 1px solid #1565C0;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: #1976D2;
                border-radius: 4px;
            }
        """)
        self.volume_slider.valueChanged.connect(self.change_volume)
        volume_layout.addWidget(self.volume_slider)
        
        self.volume_label = QLabel("75%")
        self.volume_label.setStyleSheet("font-size: 12px; min-width: 40px;")
        volume_layout.addWidget(self.volume_label)
        
        layout.addLayout(volume_layout)
        
        layout.addSpacing(20)
        
        # Info label
        info_label = QLabel("This demonstrates PyQt5 integration with Phase 4 audio engine")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 10px; color: #757575; margin-top: 10px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Set layout
        self.setLayout(layout)
    
    def load_test_track(self):
        """Load a test track from the database"""
        print("[INFO] Loading test track from database...")
        
        try:
            # Get Cornell '77
            shows = get_show_by_date('1977-05-08')
            
            if not shows:
                self.track_label.setText("Error: Could not find test show")
                self.status_label.setText("Status: Failed to load")
                return
            
            show = shows[0]
            
            # Get metadata
            metadata = get_metadata(show['identifier'])
            audio_files = extract_audio_files(metadata)
            
            if not audio_files:
                self.track_label.setText("Error: No audio files found")
                self.status_label.setText("Status: Failed to load")
                return
            
            # Use first track
            audio_file = audio_files[0]
            self.current_url = f"https://archive.org/download/{show['identifier']}/{audio_file['name']}"
            
            # Update UI
            track_name = audio_file['name'].replace('.mp3', '').replace('_', ' ')
            self.track_label.setText(f"{show['date']}: {track_name}")
            
            # Initialize player
            self.player = ResilientPlayer()
            self.player.load_url(self.current_url)
            
            self.status_label.setText("Status: Ready to play")
            print(f"[PASS] Track loaded: {track_name}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load track: {e}")
            self.track_label.setText(f"Error loading track: {e}")
            self.status_label.setText("Status: Error")
    
    def play_pause(self):
        """Toggle play/pause"""
        if not self.player:
            print("[ERROR] No player initialized")
            return
        
        if self.player.get_state() == PlayerState.PLAYING:
            self.player.pause()
            self.play_button.setText("Play")
            self.status_label.setText("Status: Paused")
            self.update_timer.stop()
            print("[INFO] Playback paused")
        else:
            self.player.play()
            self.play_button.setText("Pause")
            self.status_label.setText("Status: Playing")
            self.update_timer.start(500)  # Update every 500ms
            print("[INFO] Playback started")
    
    def stop(self):
        """Stop playback"""
        if not self.player:
            return
        
        self.player.stop()
        self.play_button.setText("Play")
        self.status_label.setText("Status: Stopped")
        self.update_timer.stop()
        self.progress_bar.setValue(0)
        self.current_time_label.setText("0:00")
        print("[INFO] Playback stopped")
    
    def change_volume(self, value):
        """Change volume"""
        if self.player:
            self.player.set_volume(value)
        
        self.volume_label.setText(f"{value}%")
    
    def update_playback_info(self):
        """Update playback position and duration (called by timer)"""
        if not self.player:
            return
        
        # Get current position and duration (returns milliseconds)
        position_ms = self.player.get_position()
        duration_ms = self.player.get_duration()
        
        # Convert to seconds
        position = position_ms / 1000.0
        duration = duration_ms / 1000.0
        
        if duration > 0:
            # Update progress bar
            self.progress_bar.setMaximum(int(duration))
            self.progress_bar.setValue(int(position))
            
            # Update time labels
            self.current_time_label.setText(self.format_time(position))
            self.total_time_label.setText(self.format_time(duration))
    
    def format_time(self, seconds):
        """Format seconds as MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def get_button_style(self, color):
        """Generate button stylesheet"""
        return f"""
            QPushButton {{
                font-size: 14px;
                font-weight: bold;
                background-color: {color};
                border-radius: 5px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """
    
    def lighten_color(self, hex_color):
        """Lighten a hex color"""
        color_map = {
            '#43A047': '#66BB6A',
            '#E53935': '#EF5350',
        }
        return color_map.get(hex_color, hex_color)
    
    def darken_color(self, hex_color):
        """Darken a hex color"""
        color_map = {
            '#43A047': '#2E7D32',
            '#E53935': '#C62828',
        }
        return color_map.get(hex_color, hex_color)
    
    def apply_dark_theme(self):
        """Apply dark theme"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)
    
    def closeEvent(self, event):
        """Handle window close - cleanup VLC player"""
        print("[INFO] Closing player...")
        if self.player:
            self.player.cleanup()
        event.accept()

def main():
    print("[INFO] Starting Mini Music Player")
    print("[INFO] This integrates PyQt5 with the Phase 4 ResilientPlayer")
    print("[INFO] Loading Cornell '77 from database...")
    
    app = QApplication(sys.argv)
    window = MiniMusicPlayer()
    window.show()
    
    print("[INFO] Window displayed - Press Play to start streaming")
    
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
