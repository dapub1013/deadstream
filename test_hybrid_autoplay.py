#!/usr/bin/env python3
"""
Test auto-play next track with HYBRID event/polling approach

This test plays short segments of 3 tracks to verify auto-advance works.
Uses both VLC events AND polling for maximum reliability.
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from src.audio.resilient_player import ResilientPlayer
from src.database.queries import get_show_by_date, get_top_rated_shows
from src.api.metadata import get_metadata, extract_audio_files


class HybridAutoPlayTest(QMainWindow):
    """Test window for hybrid auto-play approach"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto-Play Test - Hybrid Event/Polling")
        self.setGeometry(100, 100, 700, 500)
        
        # State
        self.playlist = []
        self.current_index = 0
        self.test_duration = 10  # Play 10 seconds of each track
        self.track_start_pos = 0
        self._track_end_triggered = False
        
        # Create player with BOTH approaches
        self.player = ResilientPlayer()
        self.player.on_track_ended = self.on_vlc_event_fired  # VLC event callback
        
        # Build UI
        self._build_ui()
        
        # Start polling timer (simulates PlayerScreen's update_ui_from_player)
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self._poll_for_track_end)
        self.poll_timer.start(200)  # Same as PlayerScreen (200ms)
        
        # Load test playlist
        self._load_test_playlist()
    
    def _build_ui(self):
        """Build test UI"""
        central = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Auto-Play Test: Hybrid Approach")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 20px; color: #3B82F6;")
        layout.addWidget(title)
        
        # Status
        self.status_label = QLabel("Loading...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; padding: 10px; color: white;")
        layout.addWidget(self.status_label)
        
        # Track info
        self.track_label = QLabel("Track: --")
        self.track_label.setAlignment(Qt.AlignCenter)
        self.track_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px; color: white;")
        layout.addWidget(self.track_label)
        
        # Progress
        self.progress_label = QLabel("0:00 / 0:00")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("font-size: 18px; padding: 10px; color: #9CA3AF;")
        layout.addWidget(self.progress_label)
        
        # Event detection method
        self.method_label = QLabel("Detection: --")
        self.method_label.setAlignment(Qt.AlignCenter)
        self.method_label.setStyleSheet("font-size: 14px; padding: 10px; color: #10B981;")
        layout.addWidget(self.method_label)
        
        # Instructions
        info = QLabel(
            "This test plays 10 seconds of each track.\n"
            "Watch for auto-advance when each segment ends.\n"
            "Method will show 'VLC Event' or 'Polling'"
        )
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("font-size: 12px; padding: 20px; color: #6B7280;")
        layout.addWidget(info)
        
        # Skip button
        skip_btn = QPushButton("Skip to Next Track")
        skip_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        skip_btn.clicked.connect(self.manual_next)
        layout.addWidget(skip_btn)
        
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.setStyleSheet("background-color: #1F2937;")
    
    def _load_test_playlist(self):
        """Load test show"""
        print("\n" + "="*70)
        print("HYBRID AUTO-PLAY TEST")
        print("="*70)
        
        shows = get_show_by_date('1977-05-08')
        if not shows:
            shows = get_top_rated_shows(limit=1, min_reviews=5)
        
        if not shows:
            self.status_label.setText("ERROR: Could not load test show")
            return
        
        show = shows[0]
        print(f"[TEST] Show: {show['identifier']}")
        
        metadata = get_metadata(show['identifier'])
        audio_files = extract_audio_files(metadata)
        
        # Build playlist (3 tracks)
        for i, audio in enumerate(audio_files[:3]):
            self.playlist.append({
                'title': audio.get('title', f'Track {i+1}'),
                'url': f"https://archive.org/download/{show['identifier']}/{audio['name']}",
                'number': i + 1
            })
        
        print(f"[TEST] Loaded {len(self.playlist)} tracks")
        print(f"[TEST] Each will play for {self.test_duration} seconds")
        print("[TEST] Auto-advance uses BOTH VLC events AND polling")
        print("="*70 + "\n")
        
        self.status_label.setText(f"Ready - {len(self.playlist)} tracks loaded")
        self.play_track(0)
    
    def play_track(self, index):
        """Play a track"""
        if index < 0 or index >= len(self.playlist):
            return
        
        self.current_index = index
        self._track_end_triggered = False
        track = self.playlist[index]
        
        print(f"\n>>> Playing track {index + 1}/{len(self.playlist)}")
        print(f">>> {track['title']}")
        
        self.track_label.setText(f"Track {index + 1}/{len(self.playlist)}: {track['title']}")
        self.method_label.setText("Detection: Waiting...")
        
        self.player.load_url(track['url'])
        self.player.play()
        
        # Track when we started this segment
        self.track_start_pos = 0
    
    def _poll_for_track_end(self):
        """
        Polling-based track end detection (200ms timer)
        This simulates PlayerScreen.update_ui_from_player()
        """
        if not self.player.is_playing():
            return
        
        position_ms = self.player.get_position()
        duration_ms = self.player.get_duration()
        
        # Update progress display
        pos_sec = position_ms / 1000.0
        dur_sec = duration_ms / 1000.0
        self.progress_label.setText(f"{pos_sec:.1f}s / {dur_sec:.1f}s")
        
        # For testing: stop after test_duration seconds
        if pos_sec >= self.test_duration:
            if not self._track_end_triggered:
                print(f"\n[POLLING] Reached {self.test_duration}s test duration")
                print("[POLLING] Triggering auto-advance via polling")
                self._track_end_triggered = True
                self.method_label.setText("Detection: POLLING (timer-based)")
                self.method_label.setStyleSheet("font-size: 14px; padding: 10px; color: #F59E0B;")
                QTimer.singleShot(100, self.on_track_ended)
    
    def on_vlc_event_fired(self):
        """VLC event callback - track naturally ended"""
        if not self._track_end_triggered:
            print("\n[VLC EVENT] MediaPlayerEndReached fired!")
            print("[VLC EVENT] Triggering auto-advance via VLC event")
            self._track_end_triggered = True
            self.method_label.setText("Detection: VLC EVENT (ideal!)")
            self.method_label.setStyleSheet("font-size: 14px; padding: 10px; color: #10B981;")
            self.on_track_ended()
    
    def on_track_ended(self):
        """Auto-advance to next track"""
        print("="*70)
        print("AUTO-ADVANCE TRIGGERED")
        print("="*70)
        
        next_index = self.current_index + 1
        
        if next_index < len(self.playlist):
            print(f"[AUTO-PLAY] Advancing to track {next_index + 1}")
            self.play_track(next_index)
        else:
            print("[AUTO-PLAY] Test complete!")
            self.status_label.setText("Test Complete - All tracks played!")
            self.track_label.setText("SUCCESS! Auto-play working!")
            self.track_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px; color: #10B981;")
            print("\n[PASS] Auto-play test SUCCESSFUL!")
            print("="*70 + "\n")
    
    def manual_next(self):
        """Manual skip button"""
        print("\n[MANUAL] User clicked next")
        self.on_track_ended()
    
    def closeEvent(self, event):
        """Cleanup"""
        self.poll_timer.stop()
        self.player.stop()
        event.accept()


if __name__ == '__main__':
    print("\n[INFO] Starting hybrid auto-play test")
    print("[INFO] This uses BOTH VLC events AND polling")
    print("[INFO] Whichever fires first will trigger auto-advance\n")
    
    app = QApplication(sys.argv)
    window = HybridAutoPlayTest()
    window.show()
    sys.exit(app.exec_())
