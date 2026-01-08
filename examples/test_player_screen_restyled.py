#!/usr/bin/env python3
"""
Test script for Phase 10C restyled player screen.
Tests gradient background, IconButton controls, PillButton browse, and Theme styling.

Usage:
    python3 examples/test_player_screen_restyled.py
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from src.ui.screens.player_screen_restyled import PlayerScreen
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
    screen.setWindowTitle("DeadStream Player - Phase 10C Restyle Test")
    
    # Connect browse signal
    screen.browse_requested.connect(lambda: print("[TEST] Browse Shows button clicked - signal received"))
    
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
    print("PHASE 10C PLAYER SCREEN RESTYLE TEST")
    print("=" * 70)
    print("\nVisual Features to Verify:")
    print("  [GRADIENT] Purple gradient background (deep to darker purple)")
    print("  [LAYOUT] Split-screen: Concert info (left) + Controls (right)")
    print("  [BUTTONS] IconButton media controls (circular, 60px)")
    print("  [BUTTONS] Larger play/pause button (80px, yellow accent)")
    print("  [BUTTONS] PillButton 'Browse Shows' (blue, 300px wide)")
    print("  [THEME] All colors from Theme Manager (purple, white, gray)")
    print("  [TOUCH] All buttons 60px+ for touch friendliness")
    print("\nInteractive Features:")
    print("  [PLAY] Click play/pause button (large center button)")
    print("  [SKIP] Click +/- buttons to skip 30s forward/backward")
    print("  [SEEK] Drag progress slider to seek")
    print("  [VOLUME] Adjust volume slider")
    print("  [MUTE] Click mute button")
    print("  [BROWSE] Click 'Browse Shows' button (emits signal)")
    print("\nExpected Behavior:")
    print("  - Audio should start playing Cornell '77 (or top-rated show)")
    print("  - Play/pause icon should toggle between play and pause symbols")
    print("  - Progress bar should update in real-time (every 200ms)")
    print("  - Volume control should affect audio level")
    print("  - All buttons should have hover effects (lighter on hover)")
    print("  - Skip buttons should jump forward/backward 30 seconds")
    print("\nVisual Hierarchy Check:")
    print("  1. Gradient background fills entire screen")
    print("  2. Left panel shows concert info (placeholder)")
    print("  3. Right panel shows track info and controls")
    print("  4. Play/pause button is largest (80px, yellow)")
    print("  5. Other controls are 60px (prev/next/skip)")
    print("  6. 'Browse Shows' button at bottom (blue pill)")
    print("\nPress Ctrl+C to exit")
    print("=" * 70 + "\n")
    
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
