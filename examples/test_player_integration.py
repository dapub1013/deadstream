#!/usr/bin/env python3
"""
Test PlayerScreen integration with ResilientPlayer
Phase 9, Task 9.8

This test demonstrates:
1. PlayerScreen creates ResilientPlayer instance
2. Real-time UI updates from player state
3. User controls connected to audio engine
4. Actual audio playback with streaming
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from src.ui.screens.player_screen import PlayerScreen
from src.database.queries import get_show_by_date, get_top_rated_shows
from src.api.metadata import get_metadata, extract_audio_files


def main():
    """Run player integration test"""
    print("=" * 70)
    print("DEADSTREAM PLAYER INTEGRATION TEST")
    print("Phase 9, Task 9.8 - ResilientPlayer Integration")
    print("=" * 70)
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create player screen
    player_screen = PlayerScreen()
    
    # Create test window
    window = QMainWindow()
    window.setCentralWidget(player_screen)
    window.setWindowTitle("DeadStream - Player Integration Test")
    window.setGeometry(100, 100, 1280, 720)
    window.show()
    
    # Load test show function
    def load_test_show():
        """Load a real show from database and play it"""
        print("\n[TEST] Searching for test show...")
        
        # Try to get Cornell '77
        shows = get_show_by_date('1977-05-08')
        
        # Fallback to top-rated show
        if not shows:
            print("[TEST] Cornell '77 not found, trying top-rated shows...")
            shows = get_top_rated_shows(limit=1, min_reviews=5)
        
        if not shows:
            print("[FAIL] No shows available in database")
            return
        
        show = shows[0]
        identifier = show['identifier']
        date = show.get('date', 'Unknown Date')
        venue = show.get('venue', 'Unknown Venue')
        
        print(f"[TEST] Found show: {date} - {venue}")
        print(f"[TEST] Identifier: {identifier}")
        
        # Get show metadata
        try:
            print("[TEST] Fetching metadata from Internet Archive...")
            metadata = get_metadata(identifier)
            audio_files = extract_audio_files(metadata)
            
            if not audio_files:
                print("[FAIL] No audio files found in show")
                return
            
            print(f"[PASS] Found {len(audio_files)} audio tracks")
            
            # Get first track
            total_tracks = len(audio_files)
            first_track = audio_files[0]
            track_name = first_track.get('title', first_track.get('name', 'Unknown Track'))
            
            # Parse track length (might be in MM:SS format or seconds)
            track_length_str = first_track.get('length', '300')
            try:
                # Try parsing as float (seconds)
                track_length = int(float(track_length_str))
            except ValueError:
                # Parse MM:SS or HH:MM:SS format
                if ':' in track_length_str:
                    parts = track_length_str.split(':')
                    if len(parts) == 2:  # MM:SS
                        minutes = int(parts[0])
                        seconds = int(parts[1])
                        track_length = minutes * 60 + seconds
                    elif len(parts) == 3:  # HH:MM:SS
                        hours = int(parts[0])
                        minutes = int(parts[1])
                        seconds = int(parts[2])
                        track_length = hours * 3600 + minutes * 60 + seconds
                    else:
                        track_length = 300  # Default 5 minutes
                else:
                    track_length = 300  # Default 5 minutes
            
            track_url = f"https://archive.org/download/{identifier}/{first_track['name']}"
            
            print(f"[TEST] First track: {track_name}")
            print(f"[TEST] Duration: {track_length}s")
            print(f"[TEST] URL: {track_url}")
            
            # Load and play using load_track_url (handles everything internally)
            print("[TEST] Loading track into player...")
            player_screen.load_track_url(
                url=track_url,
                track_name=track_name,
                set_name="SET I",
                track_num=1,
                total_tracks=total_tracks,
                duration=track_length
            )
            
            print("[PASS] Track loaded and playing!")
            print("\n[TEST] You should now hear audio playing...")
            
        except Exception as e:
            print(f"[FAIL] Error loading show: {e}")
            import traceback
            traceback.print_exc()
    
    # Load test show after 1 second
    QTimer.singleShot(1000, load_test_show)
    
    # Print test instructions
    print("\n" + "=" * 70)
    print("MANUAL TESTING INSTRUCTIONS")
    print("=" * 70)
    print("\nAUTOMATIC TESTS:")
    print("  [WAIT] Window opens in 1 second")
    print("  [WAIT] Show loads from database")
    print("  [WAIT] First track starts playing")
    print("  [CHECK] Progress bar updates automatically")
    print("  [CHECK] Time labels update in real-time")
    print("\nMANUAL INTERACTIONS TO TEST:")
    print("  1. Play/Pause button")
    print("     - Click to pause audio")
    print("     - Click again to resume")
    print("     - Button text should toggle")
    print("\n  2. Progress slider")
    print("     - Drag to different position")
    print("     - Audio should jump to that position")
    print("     - Time labels should update")
    print("\n  3. Volume slider")
    print("     - Drag to change volume")
    print("     - Audio volume should change immediately")
    print("     - Percentage label should update")
    print("\n  4. Mute button")
    print("     - Click to mute audio")
    print("     - Click again to unmute")
    print("     - Button text should toggle")
    print("\n  5. Skip buttons")
    print("     - Click '30s' backward/forward buttons")
    print("     - Audio position should jump 30 seconds")
    print("     - Progress bar should update")
    print("\n  6. Next/Previous track buttons")
    print("     - UI state updates (track counter)")
    print("     - Signal emitted for external handling")
    print("     - Full integration in Phase 10")
    print("\nEXPECTED BEHAVIOR:")
    print("  - Real audio streaming from Internet Archive")
    print("  - Smooth progress bar updates (5 times per second)")
    print("  - Responsive controls (immediate feedback)")
    print("  - Network resilience (auto-recovery from interruptions)")
    print("\nPress Ctrl+C in terminal to exit")
    print("=" * 70 + "\n")
    
    # Run application
    exit_code = app.exec_()
    
    # Cleanup
    print("\n[INFO] Test complete - cleaning up...")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
