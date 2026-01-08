#!/usr/bin/env python3
"""
Test script for hybrid player screen.
Original left panel + Mockup right panel.

Usage:
    python3 examples/test_player_hybrid.py
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from src.ui.screens.player_screen import PlayerScreen
from src.database.queries import get_show_by_date, get_top_rated_shows
from src.api.metadata import get_metadata, extract_audio_files


def get_test_url():
    """Get a valid test URL from database"""
    # Try Cornell '77
    shows = get_show_by_date('1977-05-08')
    
    # Fallback to top-rated shows
    if not shows:
        print("[INFO] Cornell '77 not found, trying top-rated shows...")
        shows = get_top_rated_shows(limit=3, min_reviews=5)
    
    # Try each show until we get valid audio
    for show in shows[:3]:
        try:
            print(f"[INFO] Trying show: {show.get('date', 'Unknown')} - {show.get('venue', 'Unknown')}")
            metadata = get_metadata(show['identifier'])
            audio_files = extract_audio_files(metadata)
            
            if audio_files:
                first_track = audio_files[0]
                url = f"https://archive.org/download/{show['identifier']}/{first_track['name']}"
                
                return {
                    'url': url,
                    'track_name': first_track.get('title', 'Unknown'),
                    'show_date': show.get('date', 'Unknown'),
                    'venue': show.get('venue', 'Unknown'),
                    'total_tracks': len(audio_files)
                }
        except Exception as e:
            print(f"[ERROR] Failed to get audio from show: {e}")
            continue
    
    return None


def main():
    """Run the test"""
    app = QApplication(sys.argv)
    
    # Create player screen
    screen = PlayerScreen()
    screen.setGeometry(100, 100, 1024, 600)
    screen.setWindowTitle("DeadStream Player - Hybrid Design Test")
    
    # Connect signals
    screen.home_requested.connect(lambda: print("[TEST] Home button clicked - signal received"))
    screen.settings_requested.connect(lambda: print("[TEST] Settings button clicked - signal received"))
    
    # Load test show after 1 second
    def load_test_show():
        print("\n" + "=" * 70)
        print("Loading test show from database...")
        print("=" * 70)
        
        test_data = get_test_url()
        
        if test_data:
            print(f"[PASS] Test show found:")
            print(f"  Date: {test_data['show_date']}")
            print(f"  Venue: {test_data['venue']}")
            print(f"  Track: {test_data['track_name']}")
            print(f"  Total tracks: {test_data['total_tracks']}")
            
            # Load track
            screen.load_track_url(
                url=test_data['url'],
                track_name=test_data['track_name'],
                set_name="SET I",
                track_num=1,
                total_tracks=test_data['total_tracks'],
                duration=0
            )
            print("[PASS] Track loaded and playing")
            print("=" * 70 + "\n")
        else:
            print("[FAIL] Could not find valid test show in database")
            print("=" * 70 + "\n")
    
    screen.show()
    
    # Load test show after 1 second
    QTimer.singleShot(1000, load_test_show)
    
    # Print test instructions
    print("\n" + "=" * 70)
    print("HYBRID PLAYER SCREEN TEST")
    print("=" * 70)
    print("\nLEFT PANEL (Original Design):")
    print("  [CHECK] Purple gradient background")
    print("  [CHECK] 'Concert Information' header")
    print("  [CHECK] 'No show loaded' placeholder")
    print("  [CHECK] 'Setlist' section header")
    print("  [CHECK] 'Track list will appear here...' placeholder")
    print("\nRIGHT PANEL (Mockup Design):")
    print("  [CHECK] Pure black background (#000000)")
    print("  [CHECK] Yellow home icon (top right corner)")
    print("  [CHECK] 'NOW PLAYING' label (gray, centered)")
    print("  [CHECK] '1 of 25' track counter (gray, centered)")
    print("  [CHECK] Large song title (white, 48px, bold, centered)")
    print("  [CHECK] Progress bar with timestamps")
    print("  [CHECK] 5 circular media control buttons:")
    print("          - Skip back 30s (outline, 60px)")
    print("          - Previous track (solid, 60px)")
    print("          - Play/Pause (solid, 90px, center)")
    print("          - Next track (solid, 60px)")
    print("          - Skip forward 30s (outline, 60px)")
    print("  [CHECK] Volume slider at bottom")
    print("  [CHECK] Settings icon (bottom right corner)")
    print("\nInteractive Features:")
    print("  - Click play/pause (center button)")
    print("  - Click prev/next (placeholder - no playlist yet)")
    print("  - Click skip buttons for 30s jumps")
    print("  - Drag progress slider to seek")
    print("  - Adjust volume slider")
    print("  - Click home icon (top right)")
    print("  - Click settings icon (bottom right)")
    print("\nExpected Behavior:")
    print("  - Audio plays automatically")
    print("  - Play/pause icon toggles (play <-> pause)")
    print("  - Track counter shows '1 of [total]'")
    print("  - Progress bar updates in real-time")
    print("  - All buttons have hover effects")
    print("\nPress Ctrl+C to exit")
    print("=" * 70 + "\n")
    
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
