#!/usr/bin/env python3
"""
Resilient Audio Player with Platform-Aware Audio - Phase 9.8

This module provides a robust audio streaming player with comprehensive
error handling, automatic recovery, and cross-platform audio support.

Features:
- Stream audio from URLs
- Automatic retry on network failures
- Health monitoring and recovery
- Playback controls (play, pause, stop, skip)
- Volume control (0-100%, mute/unmute)
- Position tracking and seeking
- Platform-aware audio (macOS dev, Linux production)

Author: DeadStream Project
Phase: 9.8 - Cross-Platform Audio Support
"""

import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import vlc
import time
import threading
from enum import Enum
from src.audio.vlc_config import create_vlc_instance
from src.settings import get_settings


class PlayerState(Enum):
    """Player state enumeration"""
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2
    BUFFERING = 3
    ERROR = 4


class ResilientPlayer:
    """
    Resilient audio streaming player with automatic recovery,
    platform-aware audio configuration, and gapless playback support.

    Gapless playback is achieved using VLC's MediaListPlayer which
    handles seamless transitions between tracks in a playlist.
    """

    def __init__(self, debug=False):
        """
        Initialize the player

        Args:
            debug: If True, enable verbose VLC output
        """
        # Create platform-aware VLC instance
        self.instance = create_vlc_instance(debug=debug)

        # Create media list player for gapless playback
        self.list_player = self.instance.media_list_player_new()
        self.media_list = self.instance.media_list_new()
        self.list_player.set_media_list(self.media_list)

        # Get the underlying media player for position/volume control
        self.player = self.list_player.get_media_player()

        # Playlist management
        self.playlist = []
        self.current_index = 0

        # State tracking
        self.state = PlayerState.STOPPED
        self.current_url = None

        # Gapless playback: track URLs for the media list
        self._playlist_urls = []
        self._next_media = None
        self._next_url = None

        # Health monitoring
        self.health_thread = None
        self.health_running = False
        self.last_position = 0
        self.stuck_count = 0

        # Volume state - load from settings
        settings = get_settings()
        self._volume = settings.get('audio', 'default_volume', 77)
        self._muted = False
        self._volume_before_mute = self._volume

        # Apply default volume
        self.player.audio_set_volume(self._volume)

        # Track end callback (for UI updates when track changes)
        self.on_track_ended = None  # Set by PlayerScreen

        # Set up VLC event manager for track end detection
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerEndReached,
            self._on_track_ended_internal
        )
    
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
            print("[INFO] Not currently muted")
            return True
        
        try:
            # Restore previous volume
            result = self.player.audio_set_volume(self._volume_before_mute)
            
            if result == 0:  # Success
                self._muted = False
                self._volume = self._volume_before_mute
                print(f"[INFO] Audio unmuted (volume: {self._volume}%)")
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
            bool: True if now muted, False if now unmuted
        """
        if self._muted:
            self.unmute()
            return False
        else:
            self.mute()
            return True
    
    def volume_up(self, increment=5):
        """
        Increase volume by specified amount
        
        Args:
            increment: Amount to increase (default 5%)
            
        Returns:
            bool: True if successful
        """
        new_volume = min(100, self._volume + increment)
        return self.set_volume(new_volume)
    
    def volume_down(self, increment=5):
        """
        Decrease volume by specified amount
        
        Args:
            increment: Amount to decrease (default 5%)
            
        Returns:
            bool: True if successful
        """
        new_volume = max(0, self._volume - increment)
        return self.set_volume(new_volume)
    
    # ========================================================================
    # PLAYBACK CONTROL METHODS
    # ========================================================================

    def load_playlist(self, urls):
        """
        Load an entire playlist of URLs for gapless playback.

        Loading the full playlist at once allows VLC's MediaListPlayer
        to handle seamless transitions between all tracks.

        Args:
            urls: List of URLs to load

        Returns:
            bool: True if loaded successfully
        """
        try:
            print(f"[INFO] Loading playlist with {len(urls)} tracks...")

            # Stop any existing playback
            if self.state != PlayerState.STOPPED:
                self.stop()

            # Clear the media list
            self.media_list.lock()
            while self.media_list.count() > 0:
                self.media_list.remove_index(0)
            self.media_list.unlock()
            self._playlist_urls = []

            # Add all tracks to the media list
            self.media_list.lock()
            for url in urls:
                media = self.instance.media_new(url)
                media.add_option(':network-caching=8000')
                self.media_list.add_media(media)
                self._playlist_urls.append(url)
            self.media_list.unlock()

            # Store first URL
            if urls:
                self.current_url = urls[0]

            print(f"[PASS] Playlist loaded with {self.media_list.count()} tracks")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to load playlist: {e}")
            self.state = PlayerState.ERROR
            return False

    def preload_next(self, url):
        """
        Add the next track URL to the media list for gapless playback.

        The MediaListPlayer will automatically transition to the next
        track when the current one ends, providing gapless playback.

        Args:
            url: URL to add to playlist for gapless transition

        Returns:
            bool: True if added successfully
        """
        try:
            # Check if this URL is already in the playlist
            if url in self._playlist_urls:
                print(f"[INFO] Track already in playlist, skipping")
                self._next_url = url
                return True

            print(f"[INFO] Adding next track to playlist: {url[:80]}...")

            # Create media object for next track
            media = self.instance.media_new(url)
            media.add_option(':network-caching=8000')

            # Add to the media list (locked operation)
            self.media_list.lock()
            self.media_list.add_media(media)
            self.media_list.unlock()

            # Store reference
            self._next_media = media
            self._next_url = url
            self._playlist_urls.append(url)

            print(f"[PASS] Next track added (playlist now has {self.media_list.count()} items)")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to add next track: {e}")
            self._next_media = None
            self._next_url = None
            return False

    def play_preloaded(self):
        """
        The MediaListPlayer handles gapless transitions automatically.
        This method is kept for API compatibility but the transition
        happens automatically via VLC's internal gapless handling.

        Returns:
            bool: True (transition handled by MediaListPlayer)
        """
        # MediaListPlayer handles this automatically
        # Just update our state tracking
        if self._next_url:
            self.current_url = self._next_url
            self._next_media = None
            self._next_url = None
            self.state = PlayerState.PLAYING
            print("[PASS] Gapless transition (handled by MediaListPlayer)")
            return True
        return False

    def has_preloaded(self):
        """
        Check if a next track is queued in the playlist.

        Returns:
            bool: True if next track is queued
        """
        return self._next_media is not None or self._next_url is not None

    def clear_preloaded(self):
        """Clear pre-loaded state."""
        self._next_media = None
        self._next_url = None

    def play_item_at_index(self, index):
        """
        Play a specific item in the media list by index.

        Args:
            index: Index of the item to play (0-based)

        Returns:
            bool: True if playback started
        """
        try:
            if index < 0 or index >= self.media_list.count():
                print(f"[ERROR] Invalid playlist index: {index}")
                return False

            result = self.list_player.play_item_at_index(index)

            if result == 0:
                self.state = PlayerState.PLAYING
                if index < len(self._playlist_urls):
                    self.current_url = self._playlist_urls[index]
                print(f"[PASS] Playing item at index {index}")
                return True
            else:
                print(f"[FAIL] play_item_at_index returned {result}")
                return False

        except Exception as e:
            print(f"[ERROR] Failed to play item at index: {e}")
            return False

    def load_url(self, url):
        """
        Load a URL for playback (clears existing playlist).

        Args:
            url: URL to audio stream

        Returns:
            bool: True if loaded successfully
        """
        try:
            print(f"[INFO] Loading URL: {url}")

            # Stop any existing playback
            if self.state != PlayerState.STOPPED:
                self.stop()

            # Clear the media list
            self.media_list.lock()
            while self.media_list.count() > 0:
                self.media_list.remove_index(0)
            self.media_list.unlock()
            self._playlist_urls = []

            # Clear pre-loaded state
            self.clear_preloaded()

            # Create new media
            media = self.instance.media_new(url)
            media.add_option(':network-caching=8000')  # 8 second buffer

            # Add to the media list
            self.media_list.lock()
            self.media_list.add_media(media)
            self.media_list.unlock()
            self._playlist_urls.append(url)

            # Store URL for recovery
            self.current_url = url

            print(f"[PASS] URL loaded successfully (playlist has {self.media_list.count()} items)")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to load URL: {e}")
            self.state = PlayerState.ERROR
            return False
    
    def play(self):
        """Start or resume playback using MediaListPlayer for gapless support"""
        try:
            if self.current_url is None and self.media_list.count() == 0:
                print("[WARN] No media loaded")
                return False

            # If unmuting on play, restore volume
            if self._muted:
                self.unmute()

            # Check current VLC state to determine action
            vlc_state = self.player.get_state()

            if vlc_state == vlc.State.Paused:
                # Resume from pause - use the underlying media player
                # MediaListPlayer.pause() toggles, so we use it to unpause
                self.list_player.pause()
                self.state = PlayerState.PLAYING
                print("[PASS] Playback resumed (from pause)")
                return True
            elif vlc_state == vlc.State.Playing:
                # Already playing
                self.state = PlayerState.PLAYING
                print("[INFO] Already playing")
                return True
            else:
                # Start fresh playback
                result = self.list_player.play()

                if result == 0:  # Success
                    self.state = PlayerState.PLAYING

                    # Start health monitoring if not already running
                    if not self.health_running:
                        self._start_health_monitor()

                    print("[PASS] Playback started (gapless mode)")
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
            # Check if actually playing before pausing
            vlc_state = self.player.get_state()

            if vlc_state == vlc.State.Playing:
                # MediaListPlayer.pause() toggles pause state
                self.list_player.pause()
                self.state = PlayerState.PAUSED
                print("[INFO] Playback paused")
                return True
            elif vlc_state == vlc.State.Paused:
                # Already paused
                self.state = PlayerState.PAUSED
                print("[INFO] Already paused")
                return True
            else:
                print(f"[INFO] Cannot pause - VLC state is {vlc_state}")
                return False

        except Exception as e:
            print(f"[ERROR] Failed to pause: {e}")
            return False

    def stop(self):
        """Stop playback and release resources"""
        try:
            # Stop health monitoring
            self._stop_health_monitor()

            # Stop playback
            self.list_player.stop()
            self.state = PlayerState.STOPPED
            self.current_url = None

            print("[INFO] Playback stopped")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to stop: {e}")
            return False
    
    def get_state(self):
        """Get current player state (synced with VLC)"""
        try:
            vlc_state = self.player.get_state()
            # Map VLC state to our PlayerState enum
            if vlc_state == vlc.State.Playing:
                self.state = PlayerState.PLAYING
            elif vlc_state == vlc.State.Paused:
                self.state = PlayerState.PAUSED
            elif vlc_state == vlc.State.Stopped:
                self.state = PlayerState.STOPPED
            elif vlc_state == vlc.State.Buffering:
                self.state = PlayerState.BUFFERING
            elif vlc_state == vlc.State.Error:
                self.state = PlayerState.ERROR
            # NothingSpecial and Ended states - keep current state
        except:
            pass
        return self.state
    
    def is_playing(self):
        """
        Check if currently playing

        Returns:
            bool: True if playing, False otherwise
        """
        # Check VLC's actual state to stay in sync
        try:
            vlc_state = self.player.get_state()
            is_playing = vlc_state == vlc.State.Playing
            # Update internal state to match VLC
            if is_playing:
                self.state = PlayerState.PLAYING
            elif vlc_state == vlc.State.Paused:
                self.state = PlayerState.PAUSED
            return is_playing
        except:
            return self.state == PlayerState.PLAYING
    
    def get_position(self):
        """
        Get current playback position in milliseconds
        
        Returns:
            int: Position in milliseconds, or 0 if not available
        """
        try:
            pos = self.player.get_time()
            return pos if pos >= 0 else 0
        except:
            return 0
    
    def get_duration(self):
        """
        Get total duration in milliseconds
        
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
            print(f"[INFO] Seeked to {format_time(position_ms)}")
            return True
        except Exception as e:
            print(f"[ERROR] Seek failed: {e}")
            return False
    
    def skip_forward(self, seconds=30):
        """
        Skip forward by specified seconds
        
        Args:
            seconds: Number of seconds to skip (default 30)
            
        Returns:
            bool: True if successful
        """
        current = self.get_position()
        new_pos = current + (seconds * 1000)
        return self.seek(new_pos)
    
    def skip_backward(self, seconds=30):
        """
        Skip backward by specified seconds
        
        Args:
            seconds: Number of seconds to skip back (default 30)
            
        Returns:
            bool: True if successful
        """
        current = self.get_position()
        new_pos = max(0, current - (seconds * 1000))
        return self.seek(new_pos)
    
    # ========================================================================
    # TRACK END EVENT HANDLING
    # ========================================================================
    
    def _on_track_ended_internal(self, event):
        """
        Internal VLC event handler - called when track ends
        
        This is called by VLC's event manager when MediaPlayerEndReached fires.
        It triggers the user-defined callback (if set) to auto-advance to next track.
        
        Args:
            event: VLC event object (not used, but required by VLC)
        """
        print("\n" + "="*60)
        print("[EVENT] MediaPlayerEndReached FIRED!")
        print("="*60)
        print(f"[INFO] Current state: {self.state}")
        print(f"[INFO] Current URL: {self.current_url}")
        
        # Call user-defined callback if set
        if self.on_track_ended:
            try:
                print("[INFO] Calling on_track_ended callback...")
                self.on_track_ended()
                print("[PASS] Callback completed successfully")
            except Exception as e:
                print(f"[ERROR] Track end callback failed: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("[WARN] No on_track_ended callback set - track will not auto-advance")
        
        print("="*60 + "\n")
    
    # ========================================================================
    # HEALTH MONITORING
    # ========================================================================
    
    def _start_health_monitor(self):
        """Start background health monitoring thread"""
        if self.health_running:
            return
        
        self.health_running = True
        self.health_thread = threading.Thread(target=self._health_monitor_loop, daemon=True)
        self.health_thread.start()
        print("[INFO] Health monitor started")
    
    def _stop_health_monitor(self):
        """Stop background health monitoring thread"""
        if not self.health_running:
            return
        
        self.health_running = False
        if self.health_thread:
            self.health_thread.join(timeout=2)
        print("[INFO] Health monitor stopped")
    
    def _health_monitor_loop(self):
        """
        Background thread that monitors playback health
        Detects stuck playback and attempts recovery
        """
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
        self.list_player.release()
        self.media_list.release()
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
    print("ResilientPlayer with Platform-Aware Audio")
    print("This module should be imported, not run directly")
    print("See examples/test_cross_platform_audio.py for usage")
