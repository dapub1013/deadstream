#!/usr/bin/env python3
"""
Test script for VLC player with playlist integration.

This script demonstrates:
1. Building a playlist from a show
2. Loading the playlist into VLC player
3. Playing through multiple tracks
4. Using playback controls
5. Handling automatic track transitions
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.audio.playlist import PlaylistBuilder
from src.audio.vlc_player import VLCPlayer, PlayerState
from src.api.metadata import get_metadata


def format_time(seconds):
    """Format seconds as MM:SS."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def print_player_status(player):
    """Print current player status."""
    track = player.get_current_track()
    if not track:
        print("No track loaded")
        return
    
    position = player.get_position()
    duration = player.get_duration()
    
    print(f"\n--- Player Status ---")
    print(f"State: {player.get_state().value}")
    print(f"Track: {track.title}")
    print(f"Set: {track.set_name}")
    print(f"Progress: {format_time(position)} / {format_time(duration)}")
    print(f"Volume: {player.get_volume()}%")
    print(f"---")


def test_basic_playback():
    """Test 1: Basic playback with one track."""
    print("\n" + "="*60)
    print("TEST 1: Basic Playback")
    print("="*60)
    
    # Build playlist
    print("\nBuilding playlist for Cornell '77...")
    identifier = "gd77-05-08.sbd.hicks.4982.sbeok.shnf"
    metadata = get_metadata(identifier)
    
    builder = PlaylistBuilder()
    playlist = builder.build_from_metadata(metadata)
    
    # Format duration nicely
    total_secs = playlist.get_total_duration()
    total_hours = int(total_secs // 3600)
    total_mins = int((total_secs % 3600) // 60)
    total_duration_str = f"{total_hours}:{total_mins:02d}:{int(total_secs % 60):02d}"
    
    print(f"Playlist: {playlist.date} - {playlist.venue}")
    print(f"Tracks: {len(playlist.tracks)}")
    print(f"Duration: {total_duration_str}")
    
    # Create player
    print("\nCreating player...")
    player = VLCPlayer()
    
    # Load playlist
    print("Loading playlist...")
    success = player.load_playlist(playlist)
    print(f"Load {'succeeded' if success else 'failed'}")
    
    # Start playback
    print("\nStarting playback...")
    player.play()
    
    # Let it play for 15 seconds
    print("Playing for 15 seconds...")
    time.sleep(15)
    
    # Check status
    print_player_status(player)
    
    # Stop
    print("\nStopping...")
    player.stop()
    
    # Cleanup
    player.cleanup()
    
    print("\nTest 1 Complete!")


def test_playback_controls():
    """Test 2: All playback controls."""
    print("\n" + "="*60)
    print("TEST 2: Playback Controls")
    print("="*60)
    
    # Build playlist
    identifier = "gd77-05-08.sbd.hicks.4982.sbeok.shnf"
    metadata = get_metadata(identifier)
    
    builder = PlaylistBuilder()
    playlist = builder.build_from_metadata(metadata)
    
    # Create and load player
    player = VLCPlayer()
    player.load_playlist(playlist)
    
    # Test 1: Play
    print("\n1. Testing PLAY...")
    player.play()
    time.sleep(5)
    print_player_status(player)
    
    # Test 2: Pause
    print("\n2. Testing PAUSE...")
    player.pause()
    print(f"State after pause: {player.get_state().value}")
    time.sleep(2)
    
    # Test 3: Resume
    print("\n3. Testing RESUME...")
    player.play()
    time.sleep(5)
    print_player_status(player)
    
    # Test 4: Seek forward
    print("\n4. Testing SEEK FORWARD (30s)...")
    before = player.get_position()
    player.seek(30)
    time.sleep(1)
    after = player.get_position()
    print(f"Position: {format_time(before)} -> {format_time(after)}")
    
    # Test 5: Seek backward
    print("\n5. Testing SEEK BACKWARD (-15s)...")
    before = player.get_position()
    player.seek(-15)
    time.sleep(1)
    after = player.get_position()
    print(f"Position: {format_time(before)} -> {format_time(after)}")
    
    # Test 6: Volume
    print("\n6. Testing VOLUME...")
    print(f"Current volume: {player.get_volume()}%")
    player.set_volume(50)
    print(f"Set to 50%: {player.get_volume()}%")
    player.set_volume(75)
    print(f"Set to 75%: {player.get_volume()}%")
    
    # Test 7: Mute
    print("\n7. Testing MUTE...")
    player.mute()
    print("Muted for 2 seconds...")
    time.sleep(2)
    player.mute()
    print("Unmuted")
    
    time.sleep(3)
    
    # Cleanup
    player.stop()
    player.cleanup()
    
    print("\nTest 2 Complete!")


def test_track_navigation():
    """Test 3: Track navigation."""
    print("\n" + "="*60)
    print("TEST 3: Track Navigation")
    print("="*60)
    
    # Build playlist
    identifier = "gd77-05-08.sbd.hicks.4982.sbeok.shnf"
    metadata = get_metadata(identifier)
    
    builder = PlaylistBuilder()
    playlist = builder.build_from_metadata(metadata)
    
    # Create and load player
    player = VLCPlayer()
    player.load_playlist(playlist)
    
    # Start playing first track
    print("\n1. Playing first track...")
    player.play()
    time.sleep(10)
    print_player_status(player)
    
    # Skip to next track
    print("\n2. Skipping to NEXT track...")
    player.next_track()
    time.sleep(10)
    print_player_status(player)
    
    # Skip to next again
    print("\n3. Skipping to NEXT track again...")
    player.next_track()
    time.sleep(10)
    print_player_status(player)
    
    # Go back to previous
    print("\n4. Going to PREVIOUS track...")
    player.previous_track()
    time.sleep(10)
    print_player_status(player)
    
    # Jump to specific track
    print("\n5. Jumping to track 5...")
    player.jump_to_track(4)  # 0-based index
    time.sleep(10)
    print_player_status(player)
    
    # Cleanup
    player.stop()
    player.cleanup()
    
    print("\nTest 3 Complete!")


def test_automatic_transitions():
    """Test 4: Automatic track transitions."""
    print("\n" + "="*60)
    print("TEST 4: Automatic Track Transitions")
    print("="*60)
    print("\nThis test plays the first few seconds of multiple tracks")
    print("to verify automatic transitions work.\n")
    
    # Build playlist
    identifier = "gd77-05-08.sbd.hicks.4982.sbeok.shnf"
    metadata = get_metadata(identifier)
    
    builder = PlaylistBuilder()
    playlist = builder.build_from_metadata(metadata)
    
    # Create player with callback
    player = VLCPlayer()
    
    # Track changes for testing
    track_changes = []
    
    def on_track_changed(track):
        """Callback when track changes."""
        track_changes.append(track.title)
        print(f"\n>> Track changed to: {track.title}")
    
    player.on_track_changed = on_track_changed
    
    # Load and play
    player.load_playlist(playlist)
    player.play()
    
    # Let first track play for 10 seconds
    print("\nPlaying track 1 for 10 seconds...")
    time.sleep(10)
    
    # Skip to near end of track 1
    print("\nSeeking to near end of track 1...")
    duration = player.get_duration()
    player.seek_to(duration - 5)  # 5 seconds before end
    
    # Wait for automatic transition to track 2
    print("Waiting for automatic transition to track 2...")
    time.sleep(10)
    
    # Verify we're on track 2
    current = player.get_current_track()
    print(f"\nCurrent track: {current.title}")
    print(f"Expected: Track 2")
    
    # Summary
    print(f"\nTracks played: {len(track_changes)}")
    for i, title in enumerate(track_changes, 1):
        print(f"  {i}. {title}")
    
    # Cleanup
    player.stop()
    player.cleanup()
    
    print("\nTest 4 Complete!")


def interactive_test():
    """Test 5: Interactive player."""
    print("\n" + "="*60)
    print("TEST 5: Interactive Player")
    print("="*60)
    print("\nCommands:")
    print("  p  = play/pause")
    print("  n  = next track")
    print("  b  = previous track")
    print("  f  = seek forward 30s")
    print("  r  = seek backward 30s")
    print("  s  = status")
    print("  q  = quit")
    print("\n")
    
    # Build playlist
    identifier = "gd77-05-08.sbd.hicks.4982.sbeok.shnf"
    metadata = get_metadata(identifier)
    
    builder = PlaylistBuilder()
    playlist = builder.build_from_metadata(metadata)
    
    # Create and load player
    player = VLCPlayer()
    player.load_playlist(playlist)
    
    # Start playing
    player.play()
    print("Playing... Enter commands:")
    
    # Command loop
    while True:
        try:
            cmd = input("> ").strip().lower()
            
            if cmd == 'p':
                if player.is_playing():
                    player.pause()
                    print("Paused")
                else:
                    player.play()
                    print("Playing")
            
            elif cmd == 'n':
                player.next_track()
            
            elif cmd == 'b':
                player.previous_track()
            
            elif cmd == 'f':
                player.seek(30)
                print(f"Position: {format_time(player.get_position())}")
            
            elif cmd == 'r':
                player.seek(-30)
                print(f"Position: {format_time(player.get_position())}")
            
            elif cmd == 's':
                print_player_status(player)
            
            elif cmd == 'q':
                print("Quitting...")
                break
            
            else:
                print(f"Unknown command: {cmd}")
        
        except KeyboardInterrupt:
            print("\n\nQuitting...")
            break
        except EOFError:
            print("\n\nQuitting...")
            break
    
    # Cleanup
    player.stop()
    player.cleanup()
    
    print("\nTest 5 Complete!")


def main():
    """Run all tests or specific test."""
    if len(sys.argv) > 1:
        test_num = sys.argv[1]
        
        if test_num == '1':
            test_basic_playback()
        elif test_num == '2':
            test_playback_controls()
        elif test_num == '3':
            test_track_navigation()
        elif test_num == '4':
            test_automatic_transitions()
        elif test_num == '5':
            interactive_test()
        else:
            print(f"Unknown test: {test_num}")
            print("Valid tests: 1, 2, 3, 4, 5")
    else:
        print("\nVLC Player Test Suite")
        print("=" * 60)
        print("\nAvailable tests:")
        print("  1 - Basic playback")
        print("  2 - Playback controls")
        print("  3 - Track navigation")
        print("  4 - Automatic transitions")
        print("  5 - Interactive player")
        print("\nUsage: python test_vlc_player.py [test_number]")
        print("Example: python test_vlc_player.py 2")
        print("\nOr run interactively:")
        
        try:
            choice = input("\nRun interactive test? (y/n): ").strip().lower()
            if choice == 'y':
                interactive_test()
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting...")


if __name__ == "__main__":
    main()
