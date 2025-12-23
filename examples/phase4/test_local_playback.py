#!/usr/bin/env python3
"""
Phase 4.1: Simple Local File Playback Test

This script demonstrates basic VLC playback:
1. Load a local audio file
2. Play it using VLC
3. Show progress during playback
4. Wait for completion
5. Clean up resources

Usage:
    python test_local_playback.py [audio_file.mp3]
"""

import vlc
import time
import sys
import os


def format_time(milliseconds):
    """
    Convert milliseconds to MM:SS format.
    
    Args:
        milliseconds: Time in milliseconds
        
    Returns:
        Formatted string like "3:42"
    """
    if milliseconds < 0:
        return "0:00"
        
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    
    return f"{minutes}:{seconds:02d}"


def create_progress_bar(position, width=30):
    """
    Create a text progress bar.
    
    Args:
        position: Current position (0.0 to 1.0)
        width: Width of the bar in characters
        
    Returns:
        String like "[==========          ]"
    """
    filled = int(position * width)
    empty = width - filled
    return f"[{'=' * filled}{' ' * empty}]"


def test_local_playback(filepath):
    """
    Test VLC playback with a local audio file.
    
    Args:
        filepath: Path to audio file (MP3, FLAC, OGG, etc.)
        
    Returns:
        True if playback succeeded, False otherwise
    """
    print("\nVLC Local Playback Test")
    print("=" * 50)
    print()
    
    # Step 1: Validate file exists
    print(f"Checking file: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return False
        
    # Get absolute path (VLC prefers this)
    filepath = os.path.abspath(filepath)
    print(f"Absolute path: {filepath}")
    print()
    
    # Step 2: Create VLC instance
    print("Creating VLC instance...")
    
    # Options explanation:
    # --no-xlib: Don't try to open X11 display (good for headless)
    # --quiet: Suppress verbose VLC output
    # --no-video: We're playing audio only
    instance = vlc.Instance('--no-xlib', '--quiet', '--no-video')
    
    if not instance:
        print("Error: Failed to create VLC instance")
        return False
        
    print("VLC instance created")
    
    # Step 3: Create media player
    print("Creating media player...")
    player = instance.media_player_new()
    
    if not player:
        print("Error: Failed to create media player")
        instance.release()
        return False
        
    print("Media player created")
    print()
    
    # Step 4: Load media
    print(f"Loading media: {os.path.basename(filepath)}")
    media = instance.media_new(filepath)
    
    if not media:
        print("Error: Failed to load media")
        player.release()
        instance.release()
        return False
    
    # Associate media with player
    player.set_media(media)
    print("Media loaded successfully")
    print()
    
    # Step 5: Start playback
    print("Starting playback...")
    player.play()
    
    # Give VLC a moment to start
    time.sleep(0.5)
    
    # Check if playback actually started
    state = player.get_state()
    if state == vlc.State.Error:
        print("Error: VLC encountered an error starting playback")
        player.release()
        instance.release()
        return False
    
    print("Playback started!")
    print()
    
    # Step 6: Monitor playback progress
    print("Playing... (Press Ctrl+C to stop)")
    print()
    
    try:
        last_position = -1
        
        while True:
            # Get current state
            state = player.get_state()
            
            # Check if playback finished
            if state == vlc.State.Ended:
                print("\n")
                print("Playback complete!")
                break
            elif state == vlc.State.Error:
                print("\n")
                print("Error during playback!")
                break
            elif state == vlc.State.Stopped:
                print("\n")
                print("Playback stopped")
                break
            
            # Get playback position
            current_time = player.get_time()
            total_time = player.get_length()
            position = player.get_position()
            
            # Only update display if position changed
            # (reduces flicker and CPU usage)
            if position != last_position and total_time > 0:
                # Create progress display
                progress_bar = create_progress_bar(position)
                current_str = format_time(current_time)
                total_str = format_time(total_time)
                percent = int(position * 100)
                
                # Print on same line (carriage return)
                print(f"\r{progress_bar} {current_str} / {total_str} ({percent}%)", 
                      end='', flush=True)
                
                last_position = position
            
            # Wait a bit before checking again
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n")
        print("Playback interrupted by user")
    
    # Step 7: Clean up resources
    print()
    print("Cleaning up...")
    
    # Stop playback (if still playing)
    player.stop()
    
    # Release media player
    player.release()
    
    # Release VLC instance
    instance.release()
    
    print("Resources released")
    print()
    print("Test complete!")
    
    return True


def main():
    """
    Main entry point for the script.
    """
    # Check command line arguments
    if len(sys.argv) > 1:
        # User provided a file path
        filepath = sys.argv[1]
    else:
        # Use default test file if it exists
        default_file = "test_audio.mp3"
        
        if os.path.exists(default_file):
            filepath = default_file
        else:
            print("Usage: python test_local_playback.py [audio_file.mp3]")
            print()
            print("No file specified and test_audio.mp3 not found.")
            print()
            print("To download a test file:")
            print('wget -O test_audio.mp3 \\')
            print('  "https://archive.org/download/Greatest_Speeches_of_the_20th_Century/AbdicationAddress.mp3"')
            return 1
    
    # Run the test
    success = test_local_playback(filepath)
    
    # Exit with appropriate code
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
