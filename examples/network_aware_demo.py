#!/usr/bin/env python3
"""
Complete Network-Resilient Playback System

This example demonstrates how to integrate NetworkMonitor and
ResilientAudioPlayer for a production-ready streaming music player
that gracefully handles all types of network interruptions.

Features demonstrated:
- Network connection monitoring
- Automatic playback pause on disconnect
- Automatic resume on reconnect
- Coordinated state management
- User-friendly status messages

Author: DeadStream Project
Phase: 4.6 - Network Interruption Handling
"""

import time
from network_monitor import NetworkMonitor, ConnectionState
from resilient_audio_player import ResilientAudioPlayer, PlaybackState


class NetworkAwarePlayer:
    """
    Complete playback system with network awareness.
    
    Coordinates between:
    - Network connectivity monitoring
    - Audio playback with automatic recovery
    - User-facing state management
    
    Usage:
        player = NetworkAwarePlayer()
        player.load_and_play("https://...")
        
        # Player automatically handles:
        # - Network disconnections (pauses, shows message)
        # - Network reconnections (resumes playback)
        # - Temporary Archive.org issues (retries)
        # - VLC buffering (displays progress)
    """
    
    def __init__(self):
        """Initialize network-aware player"""
        # Create audio player with generous network cache
        self.audio_player = ResilientAudioPlayer(
            network_cache_ms=10000,  # 10 seconds of buffering
            max_retries=5
        )
        
        # Create network monitor
        self.network_monitor = NetworkMonitor(
            check_interval=5.0  # Check every 5 seconds
        )
        
        # Wire up callbacks
        self.audio_player.on_state_change = self._on_playback_state_change
        self.audio_player.on_error = self._on_playback_error
        self.audio_player.on_buffering = self._on_buffering
        self.network_monitor.on_state_change = self._on_network_state_change
        
        # State tracking
        self.was_playing_before_disconnect = False
        
        # Start network monitoring
        self.network_monitor.start()
        
        print("NetworkAwarePlayer initialized")
        print(f"Network monitoring: {self.network_monitor.check_interval}s interval")
        print(f"Audio buffering: {self.audio_player.network_cache_ms}ms")
        print(f"Max retries: {self.audio_player.max_retries}")
    
    def _on_playback_state_change(self, new_state: PlaybackState):
        """Handle playback state changes"""
        print(f"[PLAYBACK] State: {new_state.value}")
        
        # You would update your UI here
        # For now, just print status
        if new_state == PlaybackState.PLAYING:
            print("  â™ª Now playing")
        elif new_state == PlaybackState.PAUSED:
            print("  â—â— Paused")
        elif new_state == PlaybackState.BUFFERING:
            print("  â‹¯ Buffering...")
        elif new_state == PlaybackState.RECOVERING:
            print("  ↻ Attempting to recover...")
        elif new_state == PlaybackState.ERROR:
            print("  âœ— Error - please check connection")
    
    def _on_playback_error(self, message: str):
        """Handle playback errors"""
        print(f"[PLAYBACK ERROR] {message}")
        
        # You would show an error dialog here
        # For now, just log it
        print("  User should be notified via UI")
    
    def _on_buffering(self, percent: int):
        """Handle buffering progress"""
        # Only print every 10% to avoid spam
        if percent % 10 == 0:
            print(f"[BUFFERING] {percent}% loaded")
    
    def _on_network_state_change(self, new_state: ConnectionState):
        """Handle network state changes"""
        print(f"[NETWORK] State: {new_state.value}")
        
        if new_state == ConnectionState.DISCONNECTED:
            # Network just went down
            print("  ⚠ Network disconnected")
            
            # Save playback state
            if self.audio_player.is_playing():
                self.was_playing_before_disconnect = True
                print("  Pausing playback until connection restored...")
                self.audio_player.pause()
            
            # You would show a "Network disconnected" message in UI
            
        elif new_state == ConnectionState.CONNECTED:
            # Network is back
            print("  âœ" Network connected")
            
            # Resume playback if it was playing before
            if self.was_playing_before_disconnect:
                print("  Resuming playback...")
                self.audio_player.play()
                self.was_playing_before_disconnect = False
            
            # You would hide the "Network disconnected" message in UI
    
    def load_and_play(self, url: str):
        """
        Load a track and start playing.
        
        Args:
            url: URL to audio file
        """
        print(f"\nLoading: {url}")
        
        # Check network first
        if not self.network_monitor.is_connected():
            print("Warning: No network connection detected")
            print("Will attempt to play anyway (may fail)")
        
        # Load and play
        self.audio_player.load_track(url, auto_play=True)
    
    def play(self):
        """Resume playback"""
        self.audio_player.play()
    
    def pause(self):
        """Pause playback"""
        self.audio_player.pause()
    
    def stop(self):
        """Stop playback"""
        self.audio_player.stop()
    
    def seek_to_ms(self, position_ms: int):
        """Seek to position"""
        self.audio_player.seek_to_ms(position_ms)
    
    def get_status_summary(self) -> dict:
        """
        Get complete status for UI display.
        
        Returns:
            Dictionary with all status information
        """
        return {
            'network_connected': self.network_monitor.is_connected(),
            'network_status': self.network_monitor.get_status_string(),
            'playback_state': self.audio_player.state.value,
            'playback_status': self.audio_player.get_state_string(),
            'position_ms': self.audio_player.get_position_ms(),
            'duration_ms': self.audio_player.get_duration_ms(),
            'volume': self.audio_player.get_volume(),
        }
    
    def cleanup(self):
        """Cleanup resources"""
        print("\nCleaning up NetworkAwarePlayer...")
        self.network_monitor.stop()
        self.audio_player.cleanup()
        print("Cleanup complete")


# Example usage and testing
if __name__ == '__main__':
    import sys
    
    print("=" * 70)
    print("Network-Aware Player Integration Test")
    print("=" * 70)
    print()
    print("This test demonstrates:")
    print("  1. Automatic network monitoring")
    print("  2. Graceful handling of disconnections")
    print("  3. Automatic recovery when network returns")
    print("  4. Resilient streaming with retries")
    print()
    print("Try disconnecting/reconnecting your network during playback!")
    print("=" * 70)
    
    # Test URL - Cornell '77 first track
    test_url = "https://archive.org/download/gd77-05-08.sbd.hicks.4982.sbeok.shnf/gd77-05-08d1t01.mp3"
    
    # Create player
    player = NetworkAwarePlayer()
    
    try:
        # Load and play
        print("\nStarting playback...")
        player.load_and_play(test_url)
        
        # Monitor for 60 seconds
        print("\nMonitoring for 60 seconds...")
        print("Press Ctrl+C to stop\n")
        
        for i in range(60):
            # Get status
            status = player.get_status_summary()
            
            # Format display
            network_icon = "âœ"" if status['network_connected'] else "âœ—"
            
            pos_s = status['position_ms'] / 1000 if status['position_ms'] else 0
            dur_s = status['duration_ms'] / 1000 if status['duration_ms'] else 0
            
            if dur_s > 0:
                progress = (pos_s / dur_s) * 100
                time_str = f"{pos_s:.1f}s / {dur_s:.1f}s ({progress:.0f}%)"
            else:
                time_str = f"{pos_s:.1f}s / ???"
            
            print(f"[{i+1:2d}s] {network_icon} Net: {status['network_status']:20s} | "
                  f"Play: {status['playback_status']:25s} | {time_str}")
            
            time.sleep(1)
        
        print("\nTest completed successfully!")
    
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    
    except Exception as e:
        print(f"\nError during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        player.cleanup()
        print("\nTest finished")
