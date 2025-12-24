#!/usr/bin/env python3
"""
Resilient Audio Player with Volume Control - Phase 4.7

This module provides a robust audio streaming player with comprehensive
error handling, automatic recovery, and volume control capabilities.

Features:
- Stream audio from URLs
- Automatic retry on network failures
- Health monitoring and recovery
- Playback controls (play, pause, stop, skip)
- Volume control (0-100%, mute/unmute)
- Position tracking and seeking

Author: DeadStream Project
Phase: 4.7 - Volume Control Complete
"""

import vlc
import time
import threading
from enum import Enum


class PlayerState(Enum):
    """Player state enumeration"""
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2
    BUFFERING = 3
    ERROR = 4


class ResilientPlayer:
    """
    Resilient audio streaming player with automatic recovery
    """
    
    def __init__(self):
        """Initialize the player"""
        # Create VLC instance with verified settings
        self.instance = vlc.Instance(
            '--aout=alsa',           # ALSA audio output
            '--no-video',            # Audio only
            '--quiet',               # Suppress output
            '--verbose=0',           # No error messages
            '--network-caching=8000' # 8 second buffer for streaming
        )
        
        # Create media player
        self.player = self.instance.media_player_new()
        
        # Playlist management
        self.playlist = []
        self.current_index = 0
        
        # State tracking
        self.state = PlayerState.STOPPED
        self.current_url = None
        
        # Health monitoring
        self.health_thread = None
        self.health_running = False
        self.last_position = 0
        self.stuck_count = 0
        
        # Volume state
        self._volume = 50  # Default 50%
        self._muted = False
        self._volume_before_mute = 50
        
        # Apply default volume
        self.player.audio_set_volume(self._volume)
    
    # ========================================================================
    # VOLUME CONTROL METHODS
    # ========================================================================
    
    def get_volume(self):
        """
        Get current volume level
        
        Returns:
            int: Volume level (0-100)
        """
        return self._volume
    
    def set_volume(self, volume):
        """
        Set volume level
        
        Args:
            volume: Volume level (0-100)
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate input
        if not isinstance(volume, (int, float)):
            print(f"[ERROR] Volume must be a number, got {type(volume)}")
            return False
        
        # Clamp to valid range
        volume = max(0, min(100, int(volume)))
        
        try:
            # Update VLC volume
            result = self.player.audio_set_volume(volume)
            
            if result == 0:  # Success
                self._volume = volume
                
                # If we were muted and volume is set, unmute
                if self._muted and volume > 0:
                    self._muted = False
                
                print(f"[INFO] Volume set to {volume}%")
                return True
            else:
                print(f"[WARN] VLC returned {result} when setting volume")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to set volume: {e}")
            return False
    
    def get_mute(self):
        """
        Check if audio is muted
        
        Returns:
            bool: True if muted, False otherwise
        """
        return self._muted
    
    def mute(self):
        """
        Mute audio output
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self._muted:
            print("[INFO] Already muted")
            return True
        
        try:
            # Save current volume
            self._volume_before_mute = self._volume
            
            # Set volume to 0
            result = self.player.audio_set_volume(0)
            
            if result == 0:  # Success
                self._muted = True
                print("[INFO] Audio muted")
                return True
            else:
                print(f"[WARN] VLC returned {result} when muting")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to mute: {e}")
            return False
    
    def unmute(self):
        """
        Unmute audio output (restore previous volume)
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._muted:
            print("[INFO] Already unmuted")
            return True
        
        try:
            # Restore previous volume
            restore_volume = self._volume_before_mute
            
            result = self.player.audio_set_volume(restore_volume)
            
            if result == 0:  # Success
                self._muted = False
                self._volume = restore_volume
                print(f"[INFO] Audio unmuted (volume: {restore_volume}%)")
                return True
            else:
                print(f"[WARN] VLC returned {result} when unmuting")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to unmute: {e}")
            return False
    
    def toggle_mute(self):
        """
        Toggle mute state
        
        Returns:
            bool: New mute state (True if now muted)
        """
        if self._muted:
            self.unmute()
        else:
            self.mute()
        
        return self._muted
    
    def volume_up(self, amount=5):
        """
        Increase volume by specified amount
        
        Args:
            amount: Amount to increase (default: 5)
            
        Returns:
            int: New volume level
        """
        new_volume = min(100, self._volume + amount)
        self.set_volume(new_volume)
        return self._volume
    
    def volume_down(self, amount=5):
        """
        Decrease volume by specified amount
        
        Args:
            amount: Amount to decrease (default: 5)
            
        Returns:
            int: New volume level
        """
        new_volume = max(0, self._volume - amount)
        self.set_volume(new_volume)
        return self._volume
    
    # ========================================================================
    # EXISTING PLAYBACK METHODS (unchanged)
    # ========================================================================
    
    def load_url(self, url):
        """Load a URL for playback"""
        try:
            print(f"[INFO] Loading: {url}")
            self.current_url = url
            
            # Create media from URL
            media = self.instance.media_new(url)
            
            # Set media to player
            self.player.set_media(media)
            
            print("[PASS] URL loaded successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to load URL: {e}")
            self.state = PlayerState.ERROR
            return False
    
    def play(self):
        """Start or resume playback"""
        try:
            if self.current_url is None:
                print("[WARN] No media loaded")
                return False
            
            # If unmuting on play, restore volume
            if self._muted:
                self.unmute()
            
            result = self.player.play()
            
            if result == 0:  # Success
                self.state = PlayerState.PLAYING
                
                # Start health monitoring if not already running
                if not self.health_running:
                    self._start_health_monitor()
                
                print("[PASS] Playback started")
                return True
            else:
                print(f"[FAIL] VLC play() returned {result}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Playback failed: {e}")
            self.state = PlayerState.ERROR
            return False
    
    def pause(self):
        """Pause playback"""
        try:
            self.player.pause()
            self.state = PlayerState.PAUSED
            print("[INFO] Playback paused")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to pause: {e}")
            return False
    
    def stop(self):
        """Stop playback and release resources"""
        try:
            # Stop health monitoring
            self._stop_health_monitor()
            
            # Stop playback
            self.player.stop()
            self.state = PlayerState.STOPPED
            self.current_url = None
            
            print("[INFO] Playback stopped")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to stop: {e}")
            return False
    
    def get_state(self):
        """Get current player state"""
        return self.state
    
    def get_position(self):
        """
        Get current playback position
        
        Returns:
            int: Position in milliseconds, or 0 if not playing
        """
        try:
            pos = self.player.get_time()
            return pos if pos >= 0 else 0
        except:
            return 0
    
    def get_duration(self):
        """
        Get total media duration
        
        Returns:
            int: Duration in milliseconds, or 0 if not available
        """
        try:
            dur = self.player.get_length()
            return dur if dur >= 0 else 0
        except:
            return 0
    
    def seek(self, position_ms):
        """
        Seek to specific position
        
        Args:
            position_ms: Position in milliseconds
            
        Returns:
            bool: True if successful
        """
        try:
            self.player.set_time(position_ms)
            print(f"[INFO] Seeked to {position_ms}ms")
            return True
        except Exception as e:
            print(f"[ERROR] Seek failed: {e}")
            return False
    
    def skip_forward(self, seconds=30):
        """Skip forward by specified seconds"""
        current_pos = self.get_position()
        new_pos = current_pos + (seconds * 1000)
        return self.seek(new_pos)
    
    def skip_backward(self, seconds=30):
        """Skip backward by specified seconds"""
        current_pos = self.get_position()
        new_pos = max(0, current_pos - (seconds * 1000))
        return self.seek(new_pos)
    
    def _start_health_monitor(self):
        """Start background health monitoring thread"""
        if self.health_running:
            return
        
        self.health_running = True
        self.health_thread = threading.Thread(target=self._health_monitor_loop, daemon=True)
        self.health_thread.start()
        print("[INFO] Health monitoring started")
    
    def _stop_health_monitor(self):
        """Stop health monitoring thread"""
        self.health_running = False
        if self.health_thread:
            self.health_thread.join(timeout=2)
        print("[INFO] Health monitoring stopped")
    
    def _health_monitor_loop(self):
        """Health monitoring background thread"""
        while self.health_running:
            try:
                # Check if we're supposed to be playing
                if self.state == PlayerState.PLAYING:
                    vlc_state = self.player.get_state()
                    
                    # If VLC says we're not playing but we should be
                    if vlc_state != vlc.State.Playing:
                        print(f"[WARN] VLC state mismatch: {vlc_state}")
                        
                        # Try to restart playback
                        print("[INFO] Attempting recovery...")
                        self.player.play()
                    
                    # Check if position is advancing
                    current_pos = self.get_position()
                    if current_pos == self.last_position:
                        self.stuck_count += 1
                        
                        if self.stuck_count > 5:  # Stuck for 5+ seconds
                            print("[WARN] Playback appears stuck, attempting recovery...")
                            self.player.stop()
                            time.sleep(0.5)
                            self.player.play()
                            self.stuck_count = 0
                    else:
                        self.stuck_count = 0
                        self.last_position = current_pos
                
            except Exception as e:
                print(f"[ERROR] Health monitor error: {e}")
            
            time.sleep(1)
    
    def cleanup(self):
        """Clean up resources"""
        print("[INFO] Cleaning up player resources...")
        self._stop_health_monitor()
        self.stop()
        self.player.release()
        print("[PASS] Cleanup complete")


# Convenience function for testing
def format_time(milliseconds):
    """Format milliseconds as MM:SS"""
    if milliseconds < 0:
        return "00:00"
    
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


if __name__ == '__main__':
    print("ResilientPlayer with Volume Control")
    print("This module should be imported, not run directly")
    print("See examples/test_volume_control.py for usage")
