#!/usr/bin/env python3
"""
Integration Example: Adding Position Tracking to Audio Player

This example shows how to integrate the PositionTracker with the VLC-based
audio player you've built in Tasks 4.1-4.4.

UPDATED: Incorporates lessons learned from troubleshooting:
- Uses verified working URLs from Internet Archive
- Correct VLC configuration with network buffering
- Proper buffering wait logic
- Real-time position display with progress bar

Author: DeadStream Project
Phase: 4.5 - Track Playback Position Integration
"""

import vlc
import time
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.audio.position_tracker import PositionTracker, PlaybackPosition


# VERIFIED WORKING URLS from Internet Archive
# Always verify URLs with: wget --spider <url>
TEST_URLS = {
    'queen_jane': {
        'url': 'https://archive.org/download/gd1991-05-11.175524.5-1.fix.tobin.flac1648/04%20Queen%20Jane%20Approximately.mp3',
        'name': 'Queen Jane Approximately',
        'show': '1991-05-11, Shoreline Amphitheatre',
        'duration': '~7 minutes'
    },
    'cornell_77': {
        'url': 'https://archive.org/download/gd1977-05-08.sbd.hicks.4982.sbeok.shnf/gd77-05-08d1t01.mp3',
        'name': 'New Minglewood Blues',
        'show': '1977-05-08, Cornell University',
        'duration': '~5 minutes',
        'note': 'Verify this URL - may need updating'
    }
}


class AudioPlayerWithPosition:
    """
    Enhanced audio player that tracks playback position.
    
    This builds on the basic player from Task 4.4, adding position tracking.
    Uses proven VLC configuration for streaming from Internet Archive.
    """
    
    def __init__(self):
        """Initialize player with VLC and position tracking"""
        print("Initializing audio player...")
        
        # VLC configuration for Internet Archive streaming
        # CRITICAL: --network-caching=5000 provides 5-second buffer
        # This is REQUIRED for smooth streaming over SSH/headless
        self.instance = vlc.Instance(
            '--network-caching=5000',  # 5-second buffer (ESSENTIAL!)
            '--no-xlib',               # No X11 display (headless operation)
            '--quiet',                 # Reduce console output
            '--no-video'               # Audio only (no video processing)
        )
        
        self.player = self.instance.media_player_new()
        
        # Position tracking (new in Task 4.5)
        self.position_tracker = PositionTracker(self.player)
        
        # Current track info
        self.current_track_url = None
        self.current_track_name = None
        
        print("✓ Audio player with position tracking initialized")
    
    def load_track(self, url: str, track_name: str = "Unknown Track"):
        """
        Load a track for playback.
        
        Args:
            url: URL to audio file (must be accessible via HTTP/HTTPS)
            track_name: Display name for the track
            
        Returns:
            True if loaded successfully, False otherwise
        """
        print(f"\nLoading: {track_name}")
        
        # Show truncated URL for readability
        url_display = url if len(url) < 80 else url[:77] + "..."
        print(f"URL: {url_display}")
        
        try:
            media = self.instance.media_new(url)
            self.player.set_media(media)
            
            self.current_track_url = url
            self.current_track_name = track_name
            
            print("✓ Track loaded successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error loading track: {e}")
            return False
    
    def play(self):
        """Start or resume playback"""
        self.player.play()
        print("▶  Playback started")
    
    def pause(self):
        """Pause playback"""
        self.player.pause()
        print("⏸  Playback paused")
    
    def stop(self):
        """Stop playback"""
        self.player.stop()
        print("⏹  Playback stopped")
    
    def is_playing(self) -> bool:
        """Check if currently playing"""
        state = self.player.get_state()
        return state == vlc.State.Playing
    
    def get_state(self):
        """Get current VLC player state"""
        return self.player.get_state()
    
    def get_position(self) -> PlaybackPosition:
        """
        Get current playback position.
        
        Returns:
            PlaybackPosition object with current time/duration/percentage
        """
        return self.position_tracker.get_position()
    
    def wait_for_buffering(self, timeout=30):
        """
        Wait for stream to buffer and start playing.
        
        This is CRITICAL for streaming - don't skip this step!
        
        Args:
            timeout: Maximum seconds to wait for buffering
            
        Returns:
            True if playback started, False if timeout/error
        """
        print("\nBuffering stream...")
        print("(This may take a few seconds depending on your connection)")
        
        start_time = time.time()
        dots = 0
        
        while True:
            elapsed = time.time() - start_time
            state = self.get_state()
            
            if state == vlc.State.Playing:
                print(f"\n✓ Buffering complete ({elapsed:.1f}s)")
                return True
            elif state == vlc.State.Error:
                print(f"\n✗ VLC error during buffering")
                return False
            elif elapsed > timeout:
                print(f"\n✗ Buffering timeout after {timeout}s")
                print("  Check your internet connection or try again later")
                return False
            
            # Show buffering progress
            if state == vlc.State.Buffering or state == vlc.State.Opening:
                dots = (dots + 1) % 4
                print(f"\rBuffering{'.' * dots}   ", end='', flush=True)
            
            time.sleep(0.5)
    
    def create_progress_bar(self, percentage, width=30):
        """
        Create a text-based progress bar.
        
        Args:
            percentage: Progress percentage (0-100)
            width: Width of bar in characters
            
        Returns:
            String like "[==========          ]"
        """
        filled = int(percentage / 100 * width)
        empty = width - filled
        return f"[{'=' * filled}{' ' * empty}]"
    
    def print_position_status(self):
        """Print current position to console (for demo/debugging)"""
        pos = self.get_position()
        
        if pos and pos.total_time > 0:
            # Create progress bar
            progress_bar = self.create_progress_bar(pos.percentage)
            
            # Format: [========>     ] 2:15 / 7:23 (31%)
            print(f"\r{progress_bar} {pos.current_time_formatted} / "
                  f"{pos.total_time_formatted} ({pos.percentage:.0f}%)",
                  end='', flush=True)
        else:
            print("\rWaiting for position data...", end='', flush=True)
    
    def monitor_playback(self, duration: float = 30.0):
        """
        Monitor playback for a specified duration, printing position updates.
        
        Args:
            duration: How long to monitor (seconds)
        """
        print(f"\nMonitoring playback for {duration:.0f} seconds...")
        print("(Press Ctrl+C to stop early)")
        print()
        
        start_time = time.time()
        rebuffer_count = 0
        last_state = None
        
        try:
            while True:
                # Check if monitoring time is up
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break
                
                state = self.get_state()
                
                # Detect rebuffering events
                if state == vlc.State.Buffering and last_state == vlc.State.Playing:
                    rebuffer_count += 1
                    print(f"\n⚠  Rebuffering... (event #{rebuffer_count})")
                elif state == vlc.State.Playing and last_state == vlc.State.Buffering:
                    print("✓  Resumed")
                
                last_state = state
                
                # Check for error or end conditions
                if state == vlc.State.Error:
                    print("\n\n✗ Playback error occurred")
                    break
                elif state == vlc.State.Ended:
                    print("\n\n✓ Track finished playing")
                    break
                elif state == vlc.State.Stopped:
                    print("\n\n✓ Playback stopped")
                    break
                
                # Update position display (throttled to avoid excessive updates)
                if self.position_tracker.should_update():
                    self.print_position_status()
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n✓ Monitoring stopped by user")
        
        # Summary
        print(f"\n\nMonitoring complete:")
        print(f"  Duration: {elapsed:.1f}s")
        print(f"  Rebuffer events: {rebuffer_count}")
        if rebuffer_count == 0:
            print(f"  Connection quality: Excellent")
        elif rebuffer_count < 3:
            print(f"  Connection quality: Good")
        else:
            print(f"  Connection quality: Fair (consider checking connection)")
    
    def cleanup(self):
        """Clean up resources"""
        self.player.stop()
        self.player.release()
        self.instance.release()
        print("\n✓ Player resources released")


def demo_position_tracking():
    """
    Demonstration of position tracking with a real audio stream.
    """
    
    print("=" * 70)
    print("DeadStream - Position Tracking Demo (Task 4.5)")
    print("=" * 70)
    
    # Create player
    player = AudioPlayerWithPosition()
    
    # Use verified working URL
    track = TEST_URLS['queen_jane']
    
    print(f"\nTest Track:")
    print(f"  Title: {track['name']}")
    print(f"  Show: {track['show']}")
    print(f"  Duration: {track['duration']}")
    
    # Load track
    if not player.load_track(track['url'], track['name']):
        print("\n✗ Failed to load track")
        return False
    
    # Start playback
    player.play()
    
    # CRITICAL: Wait for buffering before monitoring
    if not player.wait_for_buffering(timeout=30):
        print("\n✗ Failed to start playback")
        player.cleanup()
        return False
    
    print()
    print("🎵 Audio should be playing through your headphones now!")
    print()
    
    # Monitor for 30 seconds to demonstrate position tracking
    player.monitor_playback(duration=30.0)
    
    # Show final position statistics
    print("\nFinal Position Statistics:")
    final_pos = player.get_position()
    if final_pos:
        print(f"  Current time: {final_pos.current_time_formatted}")
        print(f"  Total time: {final_pos.total_time_formatted}")
        print(f"  Completed: {final_pos.percentage:.1f}%")
        print(f"  Remaining: {final_pos.remaining_time_formatted}")
        
        # Show dictionary representation (useful for UI integration)
        print(f"\n  Position as dictionary:")
        for key, value in final_pos.to_dict().items():
            print(f"    {key}: {value}")
    
    # Clean up
    player.cleanup()
    
    print()
    print("=" * 70)
    print("✓ Position tracking demo complete!")
    print("=" * 70)
    
    return True


def demo_position_calculations():
    """
    Demonstrate position calculations without actual playback.
    Useful for understanding the math and formatting.
    """
    
    print("\n" + "=" * 70)
    print("Position Calculation Examples (No Audio Required)")
    print("=" * 70)
    
    examples = [
        (0.0, 420.0, "Start of 7-minute track"),
        (210.0, 420.0, "Halfway through track"),
        (350.0, 420.0, "Near the end (50 seconds left)"),
        (420.0, 420.0, "Track complete"),
        (0.0, 682.0, "Start of 11-minute jam"),
        (341.0, 682.0, "Middle of long jam"),
        (3725.0, 7200.0, "Over 1 hour into 2-hour show"),
    ]
    
    for current, total, description in examples:
        pos = PlaybackPosition(current, total)
        print(f"\n{description}:")
        print(f"  Time: {pos.current_time_formatted} / {pos.total_time_formatted}")
        print(f"  Progress: {pos.percentage:.1f}%")
        print(f"  Remaining: {pos.remaining_time_formatted}")
        
        # Show calculation details
        print(f"  (Raw values: {current}s / {total}s)")


def list_test_urls():
    """Display available test URLs"""
    print("\n" + "=" * 70)
    print("Available Test URLs")
    print("=" * 70)
    
    for key, track in TEST_URLS.items():
        print(f"\n{key}:")
        print(f"  Title: {track['name']}")
        print(f"  Show: {track['show']}")
        print(f"  Duration: {track['duration']}")
        if 'note' in track:
            print(f"  Note: {track['note']}")
        print(f"  URL: {track['url'][:60]}...")


if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--calc-only':
            # Just show calculations (no internet/audio required)
            demo_position_calculations()
            sys.exit(0)
        elif sys.argv[1] == '--urls':
            # List available test URLs
            list_test_urls()
            sys.exit(0)
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("\nUsage: python integration_example.py [options]")
            print("\nOptions:")
            print("  --calc-only   Show position calculations without audio")
            print("  --urls        List available test URLs")
            print("  --help        Show this help message")
            print("\nNo options: Run full demo with audio streaming")
            sys.exit(0)
    
    # Full demo with actual streaming
    print("\n🎵 DeadStream Position Tracking Demo")
    print()
    print("This demo will:")
    print("  1. Stream a Grateful Dead track from Internet Archive")
    print("  2. Display real-time position updates")
    print("  3. Show progress bar with time elapsed/remaining")
    print("  4. Run for 30 seconds (or until you press Ctrl+C)")
    print()
    print("Requirements:")
    print("  ✓ Internet connection")
    print("  ✓ Headphones plugged into 3.5mm jack (card 2)")
    print("  ✓ VLC and python-vlc installed")
    print()
    print("Troubleshooting:")
    print("  • No audio? Check volume: amixer get PCM")
    print("  • Buffering timeout? Check network: ping archive.org")
    print("  • VLC error? Try: python test_url_streaming.py")
    print()
    
    response = input("Continue with demo? (y/n): ")
    if response.lower() == 'y':
        success = demo_position_tracking()
        sys.exit(0 if success else 1)
    else:
        print("\nDemo cancelled.")
        print("Run with --calc-only to see calculations without audio.")
        print("Run with --urls to see available test URLs.")
