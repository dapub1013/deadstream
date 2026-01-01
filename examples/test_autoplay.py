#!/usr/bin/env python3
"""
Test script for Task 10.2: Auto-Play Next Track

This script tests the automatic track advancement feature:
1. Loads a show with multiple tracks
2. Plays first track
3. Automatically advances to next track when current track ends
4. Continues until end of playlist

Run this to verify auto-play is working correctly!
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from src.audio.resilient_player import ResilientPlayer


class AutoPlayTestWindow(QMainWindow):
    """Simple test window to verify auto-play functionality"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto-Play Next Track Test")
        self.setGeometry(100, 100, 600, 400)
        
        # Track list for testing
        self.playlist = []
        self.current_index = 0
        
        # Create player
        self.player = ResilientPlayer()
        
        # CRITICAL: Connect track end callback
        self.player.on_track_ended = self.on_track_ended
        
        # Build UI
        self._build_ui()
        
        # Load test playlist
        self._load_test_playlist()
    
    def _build_ui(self):
        """Build simple test UI"""
        central = QWidget()
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Loading test playlist...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                padding: 20px;
                color: white;
            }
        """)
        layout.addWidget(self.status_label)
        
        self.track_label = QLabel("Track: --")
        self.track_label.setAlignment(Qt.AlignCenter)
        self.track_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                color: #3B82F6;
            }
        """)
        layout.addWidget(self.track_label)
        
        central.setLayout(layout)
        self.setCentralWidget(central)
        
        # Dark theme
        self.setStyleSheet("background-color: #1F2937;")
    
    def _load_test_playlist(self):
        """Load a test show from database"""
        from src.database.queries import get_show_by_date, get_top_rated_shows
        from src.api.metadata import get_metadata, extract_audio_files
        
        print("\n" + "="*60)
        print("AUTO-PLAY NEXT TRACK TEST")
        print("="*60)
        
        # Try Cornell '77
        shows = get_show_by_date('1977-05-08')
        
        if not shows:
            print("[INFO] Cornell not found, trying top-rated shows...")
            shows = get_top_rated_shows(limit=1, min_reviews=5)
        
        if not shows:
            self.status_label.setText("ERROR: Could not load test show!")
            return
        
        show = shows[0]
        print(f"\n[TEST] Loading show: {show['identifier']}")
        
        # Get metadata
        metadata = get_metadata(show['identifier'])
        audio_files = extract_audio_files(metadata)
        
        # Build playlist (first 3 tracks for quick testing)
        for i, audio in enumerate(audio_files[:3]):
            track = {
                'title': audio.get('title', f'Track {i+1}'),
                'url': f"https://archive.org/download/{show['identifier']}/{audio['name']}",
                'number': i + 1
            }
            self.playlist.append(track)
        
        print(f"[TEST] Loaded {len(self.playlist)} tracks")
        print("\n[TEST] Auto-play test starting...")
        print("[TEST] Each track will play for ~10 seconds, then auto-advance")
        print("[TEST] Watch the console and UI for auto-advance messages!")
        print("="*60 + "\n")
        
        # Update UI
        self.status_label.setText(f"Loaded {len(self.playlist)} tracks")
        
        # Start playing first track
        self.play_track(0)
        
        # For testing: seek to near end of track so we don't wait long
        # Remove this in production!
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self._seek_to_near_end())
    
    def _seek_to_near_end(self):
        """Test helper: seek to 10 seconds before end"""
        duration = self.player.get_duration()
        if duration > 15000:  # If track is longer than 15 seconds
            seek_position = duration - 10000  # 10 seconds before end
            self.player.seek(seek_position)
            print(f"[TEST] Seeked to near end (for testing auto-advance)")
    
    def play_track(self, index):
        """Play a specific track"""
        if index < 0 or index >= len(self.playlist):
            print(f"[ERROR] Invalid track index: {index}")
            return
        
        self.current_index = index
        track = self.playlist[index]
        
        print(f"\n>>> Playing track {index + 1}/{len(self.playlist)}")
        print(f">>> Title: {track['title']}")
        
        # Update UI
        self.track_label.setText(f"Track {index + 1}/{len(self.playlist)}: {track['title']}")
        
        # Load and play
        self.player.load_url(track['url'])
        self.player.play()
    
    def on_track_ended(self):
        """
        Callback when track ends - THIS IS THE AUTO-PLAY MAGIC!
        
        This method is automatically called by ResilientPlayer when
        the VLC MediaPlayerEndReached event fires.
        """
        print("\n" + "="*60)
        print("AUTO-PLAY EVENT TRIGGERED!")
        print("="*60)
        
        # Check if there's a next track
        next_index = self.current_index + 1
        
        if next_index < len(self.playlist):
            print(f"[AUTO-PLAY] Advancing to next track ({next_index + 1}/{len(self.playlist)})")
            self.play_track(next_index)
        else:
            print("[AUTO-PLAY] End of playlist reached")
            self.status_label.setText("Test complete - all tracks played!")
            self.track_label.setText("Auto-play test PASSED!")
            print("\n[PASS] Auto-play next track test SUCCESSFUL!")
            print("="*60 + "\n")
    
    def closeEvent(self, event):
        """Cleanup on close"""
        self.player.stop()
        event.accept()


if __name__ == '__main__':
    print("\n[INFO] Starting auto-play next track test...")
    print("[INFO] This will play 3 short tracks with auto-advance")
    print("[INFO] Watch for 'AUTO-PLAY EVENT TRIGGERED!' messages\n")
    
    app = QApplication(sys.argv)
    window = AutoPlayTestWindow()
    window.show()
    sys.exit(app.exec_())
