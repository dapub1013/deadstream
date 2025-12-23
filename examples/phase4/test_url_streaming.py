#!/usr/bin/env python3
"""
Phase 4.2: URL Streaming Test

This script demonstrates streaming audio from Internet Archive:
1. Stream from a remote URL (not local file)
2. Handle buffering states
3. Monitor network status
4. Display streaming progress
5. Handle network errors gracefully

Usage:
    python test_url_streaming.py [url]
    
    If no URL provided, uses a default Grateful Dead track.
"""

import vlc
import time
import sys
import requests


# Default test URL - Shoreline Amphitheatre on 1991-05-11, Queen Jane Approximately (~7 minutes)
DEFAULT_URL = "https://archive.org/download/gd1991-05-11.175524.5-1.fix.tobin.flac1648/04%20Queen%20Jane%20Approximately.mp3"


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


def check_url_accessible(url):
    """
    Verify URL is accessible before trying to stream.
    
    Args:
        url: URL to check
        
    Returns:
        (is_valid, status_message)
    """
    print(f"Checking URL accessibility...")
    
    try:
        # Send HEAD request (faster than GET)
        response = requests.head(url, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            # Get content type
            content_type = response.headers.get('content-type', 'unknown')
            
            # Get file size if available
            content_length = response.headers.get('content-length')
            if content_length:
                size_mb = int(content_length) / (1024 * 1024)
                size_str = f"{size_mb:.2f} MB"
            else:
                size_str = "unknown size"
            
            return True, f"URL OK - {content_type}, {size_str}"
        else:
            return False, f"HTTP {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "Connection timeout"
    except requests.exceptions.ConnectionError:
        return False, "Connection failed - check network"
    except Exception as e:
        return False, f"Error: {str(e)}"


def test_url_streaming(url):
    """
    Test VLC streaming from a URL.
    
    Args:
        url: HTTP(S) URL to stream
        
    Returns:
        True if streaming succeeded, False otherwise
    """
    print("\nVLC URL Streaming Test")
    print("=" * 60)
    print()
    print(f"URL: {url}")
    print()
    
    # Step 1: Check if URL is accessible
    url_valid, status_msg = check_url_accessible(url)
    print(f"Status: {status_msg}")
    
    if not url_valid:
        print("\nError: URL is not accessible")
        print("Check your internet connection and URL")
        return False
    
    print()
    
    # Step 2: Create VLC instance with streaming options
    print("Creating VLC instance...")
    
    # Streaming-specific options:
    # --network-caching=5000: Buffer 5 seconds (smoother playback)
    # --no-xlib: Headless operation
    # --quiet: Suppress verbose output
    # --no-video: Audio only
    instance = vlc.Instance(
        '--network-caching=5000',
        '--no-xlib',
        '--quiet',
        '--no-video'
    )
    
    if not instance:
        print("Error: Failed to create VLC instance")
        return False
    
    print("VLC instance created (5-second buffer)")
    
    # Step 3: Create media player
    print("Creating media player...")
    player = instance.media_player_new()
    
    if not player:
        print("Error: Failed to create media player")
        instance.release()
        return False
    
    print("Media player created")
    print()
    
    # Step 4: Load URL as media
    print("Loading URL...")
    media = instance.media_new(url)
    
    if not media:
        print("Error: Failed to load URL")
        player.release()
        instance.release()
        return False
    
    # Associate media with player
    player.set_media(media)
    print("URL loaded into player")
    print()
    
    # Step 5: Start streaming
    print("Starting stream...")
    player.play()
    
    # Step 6: Wait for buffering
    print("Buffering... (this may take a few seconds)")
    
    buffering_start = time.time()
    max_buffer_wait = 30  # seconds
    
    while True:
        state = player.get_state()
        elapsed = time.time() - buffering_start
        
        if state == vlc.State.Playing:
            buffer_time = elapsed
            print(f"Buffered in {buffer_time:.1f} seconds - now playing!")
            break
        elif state == vlc.State.Error:
            print("\nError: VLC encountered an error during buffering")
            player.release()
            instance.release()
            return False
        elif elapsed > max_buffer_wait:
            print(f"\nError: Buffering timeout after {max_buffer_wait} seconds")
            print("Check your internet connection speed")
            player.stop()
            player.release()
            instance.release()
            return False
        elif state == vlc.State.Buffering:
            # Show buffering dots
            dots = "." * (int(elapsed) % 4)
            print(f"\rBuffering{dots:4s}", end='', flush=True)
        
        time.sleep(0.5)
    
    print()
    
    # Step 7: Monitor streaming playback
    print("\nStreaming... (Press Ctrl+C to stop)")
    print()
    
    last_state = None
    last_position = -1
    rebuffer_count = 0
    
    try:
        while True:
            # Get current state
            state = player.get_state()
            
            # Detect state changes
            if state != last_state:
                if state == vlc.State.Buffering:
                    rebuffer_count += 1
                    print(f"\n[Rebuffering... #{rebuffer_count}]")
                elif state == vlc.State.Playing and last_state == vlc.State.Buffering:
                    print("[Resumed]")
                
                last_state = state
            
            # Check if playback finished or errored
            if state == vlc.State.Ended:
                print("\n")
                print("Stream complete!")
                break
            elif state == vlc.State.Error:
                print("\n")
                print("Error during streaming!")
                break
            elif state == vlc.State.Stopped:
                print("\n")
                print("Stream stopped")
                break
            
            # Show progress (only when playing)
            if state == vlc.State.Playing:
                current_time = player.get_time()
                total_time = player.get_length()
                position = player.get_position()
                
                # Only update if position changed
                if position != last_position and total_time > 0:
                    progress_bar = create_progress_bar(position)
                    current_str = format_time(current_time)
                    total_str = format_time(total_time)
                    percent = int(position * 100)
                    
                    # Print on same line
                    print(f"\r{progress_bar} {current_str} / {total_str} ({percent}%)", 
                          end='', flush=True)
                    
                    last_position = position
            
            # Wait before checking again
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n")
        print("Stream interrupted by user")
    
    # Step 8: Summary
    print()
    print("=" * 60)
    print("Streaming Summary:")
    print(f"  URL: {url}")
    print(f"  Rebuffering events: {rebuffer_count}")
    if rebuffer_count == 0:
        print("  Quality: Excellent (no buffering interruptions)")
    elif rebuffer_count < 3:
        print("  Quality: Good (minor buffering)")
    else:
        print("  Quality: Fair (frequent buffering - check connection)")
    print()
    
    # Step 9: Clean up
    print("Cleaning up...")
    player.stop()
    player.release()
    instance.release()
    print("Resources released")
    print()
    print("Test complete!")
    
    return True


def show_test_urls():
    """Display some good test URLs from Archive.org"""
    print("\nSuggested Test URLs (Grateful Dead - Cornell '77):")
    print()
    print("Short (~3 min) - Minglewood Blues:")
    print("  https://archive.org/download/gd1977-05-08.sbd.hicks.4982.sbeok.shnf/gd77-05-08d1t01.mp3")
    print()
    print("Medium (~8 min) - Loser:")
    print("  https://archive.org/download/gd1977-05-08.sbd.hicks.4982.sbeok.shnf/gd77-05-08d1t02.mp3")
    print()
    print("Long (~20 min) - Scarlet > Fire:")
    print("  https://archive.org/download/gd1977-05-08.sbd.hicks.4982.sbeok.shnf/gd77-05-08d2t01.mp3")
    print()


def main():
    """Main entry point for the script"""
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage: python test_url_streaming.py [url]")
            print()
            print("If no URL provided, uses default Cornell '77 track.")
            print()
            show_test_urls()
            return 0
        
        # User provided a URL
        url = sys.argv[1]
    else:
        # Use default
        print(f"No URL provided - using default Cornell '77 track")
        print("(Use --help to see other test URLs)")
        print()
        url = DEFAULT_URL
    
    # Run the test
    success = test_url_streaming(url)
    
    # Exit with appropriate code
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
