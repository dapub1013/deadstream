#!/usr/bin/env python3
"""
Network-Resilient Audio Player for DeadStream

This module extends the basic AudioPlayer with robust network interruption
handling, automatic recovery, and playback position preservation.

Features:
- Automatic retry on network failures
- Playback position preservation during reconnects
- VLC buffer configuration for network streaming
- Connection state monitoring integration
- Graceful degradation during network issues

Author: DeadStream Project
Phase: 4.6 - Network Interruption Handling
"""

import vlc
import time
from enum import Enum
from typing import Optional, Callable
from datetime import datetime


class PlaybackState(Enum):
    """Audio player states"""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"
    BUFFERING = "buffering"
    ERROR = "error"
    RECOVERING = "recovering"


class ResilientAudioPlayer:
    """
    VLC-based audio player with network interruption handling.
    
    This player automatically handles:
    - Network disconnections during streaming
    - Archive.org temporary unavailability
    - VLC buffer underruns
    - Playback position recovery after interruptions
    
    Usage:
        player = ResilientAudioPlayer()
        
        # Configure callbacks
        player.on_state_change = handle_state_change
        player.on_error = handle_error
        
        # Load and play
        player.load_track("https://archive.org/download/...")
        player.play()
        
        # Network interruption happens...
        # Player automatically attempts recovery
    """
    
    def __init__(self, network_cache_ms=5000, max_retries=3):
        """
        Initialize resilient audio player.
        
        Args:
            network_cache_ms: VLC network cache size in milliseconds
                             (higher = more buffering, more resilience)
            max_retries: Maximum automatic retry attempts
        """
        # VLC instance with network optimization and ALSA audio
        instance_args = [
            '--aout=alsa',  # Use ALSA audio output (works with Pi headphones)
            '--no-video',  # Audio only
            '--quiet',  # Suppress VLC output
            '--verbose=0',  # Suppress error messages
            f'--network-caching={network_cache_ms}',  # Buffer for network streams
            '--file-caching=1000',  # Lower cache for local files
        ]
        
        self.instance = vlc.Instance(' '.join(instance_args))
        self.player = self.instance.media_player_new()
        
        # Network resilience settings
        self.network_cache_ms = network_cache_ms
        self.max_retries = max_retries
        
        # Current state
        self.state = PlaybackState.STOPPED
        self.current_url = None
        self.current_media = None
        
        # Recovery state
        self.retry_count = 0
        self.saved_position_ms = 0
        self.last_known_position_ms = 0
        self.is_recovering = False
        
        # Callbacks (set by external code)
        self.on_state_change: Optional[Callable[[PlaybackState], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None
        self.on_buffering: Optional[Callable[[int], None]] = None
        
        # Event manager for VLC callbacks
        self.event_manager = self.player.event_manager()
        self._setup_vlc_callbacks()
        
        print(f"ResilientAudioPlayer initialized (cache: {network_cache_ms}ms, retries: {max_retries})")
    
    def _setup_vlc_callbacks(self):
        """Setup VLC event handlers"""
        # Playing state
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerPlaying,
            self._on_vlc_playing
        )
        
        # Paused state
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerPaused,
            self._on_vlc_paused
        )
        
        # Stopped state
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerStopped,
            self._on_vlc_stopped
        )
        
        # Error/EndReached
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerEndReached,
            self._on_vlc_end_reached
        )
        
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerEncounteredError,
            self._on_vlc_error
        )
        
        # Buffering progress
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerBuffering,
            self._on_vlc_buffering
        )
    
    def _on_vlc_playing(self, event):
        """VLC callback: Media started playing"""
        if self.is_recovering:
            print(f"Recovery successful! Resumed playback")
            self.retry_count = 0
            self.is_recovering = False
        
        self._update_state(PlaybackState.PLAYING)
    
    def _on_vlc_paused(self, event):
        """VLC callback: Media paused"""
        if not self.is_recovering:  # Don't update state during recovery
            self._update_state(PlaybackState.PAUSED)
    
    def _on_vlc_stopped(self, event):
        """VLC callback: Media stopped"""
        if not self.is_recovering:  # Don't update state during recovery
            self._update_state(PlaybackState.STOPPED)
    
    def _on_vlc_end_reached(self, event):
        """VLC callback: End of media reached"""
        # Could be normal end or network error
        current_pos = self.get_position_ms()
        duration = self.get_duration_ms()
        
        if duration and current_pos < duration - 1000:  # Not at end
            # Unexpected end - likely network issue
            print(f"Unexpected end reached at {current_pos}ms / {duration}ms")
            self._attempt_recovery("Media ended unexpectedly (possible network issue)")
        else:
            # Normal end of track
            self._update_state(PlaybackState.STOPPED)
    
    def _on_vlc_error(self, event):
        """VLC callback: Error encountered"""
        print("VLC error encountered")
        self._attempt_recovery("VLC playback error")
    
    def _on_vlc_buffering(self, event):
        """VLC callback: Buffering in progress"""
        # event.u.new_cache contains buffer percentage (0-100)
        # This is undocumented but works in practice
        if self.on_buffering:
            try:
                # Try to extract buffering percentage
                buffer_pct = getattr(event, 'u', None)
                if buffer_pct:
                    self.on_buffering(int(buffer_pct))
            except:
                pass  # If we can't get the value, that's okay
    
    def _update_state(self, new_state: PlaybackState):
        """Update playback state and notify listeners"""
        if new_state != self.state:
            old_state = self.state
            self.state = new_state
            
            print(f"Player state: {old_state.value} -> {new_state.value}")
            
            if self.on_state_change:
                try:
                    self.on_state_change(new_state)
                except Exception as e:
                    print(f"Error in state change callback: {e}")
    
    def _attempt_recovery(self, reason: str):
        """
        Attempt to recover from playback error.
        
        Args:
            reason: Description of why recovery is needed
        """
        if self.is_recovering:
            print("Already attempting recovery, skipping duplicate attempt")
            return
        
        if self.retry_count >= self.max_retries:
            print(f"Max retries ({self.max_retries}) exceeded, giving up")
            self._update_state(PlaybackState.ERROR)
            
            if self.on_error:
                self.on_error(f"Playback failed after {self.max_retries} retries: {reason}")
            return
        
        self.retry_count += 1
        self.is_recovering = True
        
        print(f"Attempting recovery (retry {self.retry_count}/{self.max_retries}): {reason}")
        self._update_state(PlaybackState.RECOVERING)
        
        # Save current position
        self.saved_position_ms = self.get_position_ms()
        print(f"Saved position: {self.saved_position_ms}ms")
        
        # Wait a moment for network to stabilize
        wait_time = min(2.0 * self.retry_count, 10.0)  # Exponential backoff
        print(f"Waiting {wait_time}s before retry...")
        time.sleep(wait_time)
        
        # Attempt to reload and resume
        if self.current_url:
            print(f"Reloading: {self.current_url}")
            self.load_track(self.current_url, auto_play=False)
            
            # Seek to saved position
            if self.saved_position_ms > 0:
                print(f"Seeking to {self.saved_position_ms}ms")
                self.seek_to_ms(self.saved_position_ms)
            
            # Resume playback
            self.play()
        else:
            print("No URL to reload")
            self.is_recovering = False
            self._update_state(PlaybackState.ERROR)
    
    def load_track(self, url: str, auto_play: bool = False):
        """
        Load an audio track from URL.
        
        Args:
            url: URL to audio file (local or remote)
            auto_play: If True, start playing immediately
        """
        print(f"Loading track: {url}")
        
        try:
            # Stop current playback
            if self.player.is_playing():
                self.player.stop()
            
            # Save URL for potential recovery
            self.current_url = url
            
            # Create new media
            self.current_media = self.instance.media_new(url)
            if not self.current_media:
                print("ERROR: Failed to create media object")
                if self.on_error:
                    self.on_error(f"Failed to load URL: {url}")
                return
            
            self.player.set_media(self.current_media)
            
            # Reset recovery state
            self.retry_count = 0
            self.is_recovering = False
            self.saved_position_ms = 0
            
            if auto_play:
                self.play()
        
        except Exception as e:
            print(f"ERROR loading track: {e}")
            if self.on_error:
                self.on_error(f"Failed to load track: {e}")
    
    def play(self):
        """Start or resume playback"""
        if self.player.play() == 0:
            print("Playback started")
        else:
            print("Failed to start playback")
            if self.on_error:
                self.on_error("Failed to start playback")
    
    def pause(self):
        """Pause playback"""
        self.player.pause()
        print("Playback paused")
    
    def stop(self):
        """Stop playback"""
        if self.player.is_playing() or self.player.get_state() != vlc.State.Stopped:
            self.player.stop()
        
        if not self.is_recovering:
            self._update_state(PlaybackState.STOPPED)
        print("Playback stopped")
    
    def seek_to_ms(self, position_ms: int):
        """
        Seek to specific position.
        
        Args:
            position_ms: Position in milliseconds
        """
        if self.player.is_seekable():
            self.player.set_time(position_ms)
            print(f"Seeked to {position_ms}ms")
        else:
            print("Media is not seekable")
    
    def get_position_ms(self) -> int:
        """Get current playback position in milliseconds"""
        pos = self.player.get_time()
        if pos >= 0:
            self.last_known_position_ms = pos
            return pos
        return self.last_known_position_ms
    
    def get_duration_ms(self) -> Optional[int]:
        """Get total duration in milliseconds"""
        duration = self.player.get_length()
        return duration if duration > 0 else None
    
    def get_volume(self) -> int:
        """Get current volume (0-100)"""
        return self.player.audio_get_volume()
    
    def set_volume(self, volume: int):
        """
        Set volume.
        
        Args:
            volume: Volume level (0-100)
        """
        volume = max(0, min(100, volume))
        self.player.audio_set_volume(volume)
    
    def is_playing(self) -> bool:
        """Check if currently playing"""
        return self.player.is_playing()
    
    def get_state_string(self) -> str:
        """Get human-readable state string"""
        if self.state == PlaybackState.PLAYING:
            return "Playing"
        elif self.state == PlaybackState.PAUSED:
            return "Paused"
        elif self.state == PlaybackState.STOPPED:
            return "Stopped"
        elif self.state == PlaybackState.BUFFERING:
            return "Buffering..."
        elif self.state == PlaybackState.RECOVERING:
            return f"Recovering (attempt {self.retry_count}/{self.max_retries})..."
        elif self.state == PlaybackState.ERROR:
            return "Error"
        else:
            return "Unknown"
    
    def cleanup(self):
        """Cleanup VLC resources"""
        print("Cleaning up audio player...")
        self.stop()
        self.player.release()
        self.instance.release()


# Example usage and testing
if __name__ == '__main__':
    import sys
    
    print("Resilient Audio Player Test")
    print("=" * 60)
    
    # Test URL (Cornell '77)
    test_url = "https://archive.org/download/gd77-05-08.sbd.hicks.4982.sbeok.shnf/gd77-05-08d1t01.mp3"
    
    def on_state_change(state):
        print(f">>> State changed to: {state.value}")
    
    def on_error(message):
        print(f">>> ERROR: {message}")
    
    def on_buffering(percent):
        print(f">>> Buffering: {percent}%")
    
    # Create player
    player = ResilientAudioPlayer(network_cache_ms=8000, max_retries=3)
    player.on_state_change = on_state_change
    player.on_error = on_error
    player.on_buffering = on_buffering
    
    try:
        print(f"\nLoading test track...")
        print(f"URL: {test_url}\n")
        
        player.load_track(test_url, auto_play=True)
        
        print("Playing for 20 seconds...")
        print("Try disconnecting your network to test recovery\n")
        
        for i in range(20):
            pos = player.get_position_ms()
            dur = player.get_duration_ms()
            state = player.get_state_string()
            
            if dur:
                progress = (pos / dur) * 100
                print(f"[{i+1:2d}s] {state} | {pos/1000:.1f}s / {dur/1000:.1f}s ({progress:.1f}%)")
            else:
                print(f"[{i+1:2d}s] {state} | Position: {pos/1000:.1f}s")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    
    finally:
        print("\nCleaning up...")
        player.cleanup()
        print("Test complete")
