"""
VLC-based audio player with playlist support.

This module provides a VLCPlayer class that integrates with the Playlist
system to play Grateful Dead shows with automatic track transitions.

Classes:
    PlayerState: Enum for player states
    VLCPlayer: Main player class with playback controls
"""

import vlc
import time
from enum import Enum
from typing import Optional, Callable
from .playlist import Playlist


class PlayerState(Enum):
    """Player state enumeration."""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"
    LOADING = "loading"
    ERROR = "error"


class VLCPlayer:
    """
    VLC-based audio player with playlist support.
    
    Features:
    - Automatic track transitions
    - Play/pause/stop controls
    - Skip forward/backward
    - Seek within track
    - Volume control
    - Network error recovery
    - State tracking
    
    Usage:
        player = VLCPlayer()
        player.load_playlist(playlist)
        player.play()
        
        # Later...
        player.pause()
        player.next_track()
        player.seek(30)  # 30 seconds forward
    """
    
    def __init__(self):
        """Initialize the VLC player."""
        # Create VLC instance with appropriate options
        self.instance = vlc.Instance(
            '--no-xlib',           # No X11 display needed
            '--quiet',             # Suppress verbose output
            '--no-video',          # Audio only
            '--network-caching=5000',  # 5 second buffer for streaming
        )
        
        # Create media player
        self.player = self.instance.media_player_new()
        
        # Playlist
        self.playlist: Optional[Playlist] = None
        
        # State tracking
        self.state = PlayerState.STOPPED
        self.current_track_index = -1
        
        # Event callbacks (for future UI integration)
        self.on_track_changed: Optional[Callable] = None
        self.on_state_changed: Optional[Callable] = None
        self.on_position_changed: Optional[Callable] = None
        
        # Error recovery
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        
        # Set up event manager for automatic track transitions
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerEndReached,
            self._on_track_ended
        )
        
        print("VLCPlayer initialized")
    
    def load_playlist(self, playlist: Playlist) -> bool:
        """
        Load a playlist for playback.
        
        Args:
            playlist: Playlist object to load
            
        Returns:
            True if loaded successfully, False otherwise
        """
        if not playlist or not playlist.tracks:
            print("ERROR: Cannot load empty playlist")
            return False
        
        self.playlist = playlist
        self.current_track_index = -1  # Will be set to 0 on first play
        
        # Format total duration
        total_secs = playlist.get_total_duration()
        total_hours = int(total_secs // 3600)
        total_mins = int((total_secs % 3600) // 60)
        total_duration_str = f"{total_hours}:{total_mins:02d}:{int(total_secs % 60):02d}"
        
        print(f"Loaded playlist: {playlist.date} - {playlist.venue}")
        print(f"  {len(playlist.tracks)} tracks, {total_duration_str}")
        
        return True
    
    def play(self) -> bool:
        """
        Start or resume playback.
        
        Returns:
            True if playback started, False otherwise
        """
        if not self.playlist:
            print("ERROR: No playlist loaded")
            return False
        
        # If stopped or no track loaded, start from beginning
        if self.state == PlayerState.STOPPED or self.current_track_index < 0:
            return self._play_track(0)
        
        # If paused, resume
        if self.state == PlayerState.PAUSED:
            self.player.play()
            self.state = PlayerState.PLAYING
            self._notify_state_changed()
            print("Resumed playback")
            return True
        
        # Already playing
        return True
    
    def pause(self) -> bool:
        """
        Pause playback.
        
        Returns:
            True if paused, False if not playing
        """
        if self.state != PlayerState.PLAYING:
            return False
        
        self.player.pause()
        self.state = PlayerState.PAUSED
        self._notify_state_changed()
        print("Paused")
        
        return True
    
    def stop(self) -> bool:
        """
        Stop playback completely.
        
        Returns:
            True if stopped successfully
        """
        self.player.stop()
        self.state = PlayerState.STOPPED
        self.current_track_index = -1
        self._notify_state_changed()
        print("Stopped")
        
        return True
    
    def next_track(self) -> bool:
        """
        Skip to next track.
        
        Returns:
            True if skipped, False if at end of playlist
        """
        if not self.playlist:
            return False
        
        next_index = self.current_track_index + 1
        
        if next_index >= len(self.playlist.tracks):
            print("End of playlist reached")
            self.stop()
            return False
        
        return self._play_track(next_index)
    
    def previous_track(self) -> bool:
        """
        Go to previous track.
        
        Returns:
            True if went back, False if at beginning
        """
        if not self.playlist:
            return False
        
        # If more than 3 seconds into current track, restart it
        if self.get_position() > 3.0:
            self.seek_to(0)
            return True
        
        # Otherwise go to actual previous track
        prev_index = self.current_track_index - 1
        
        if prev_index < 0:
            print("Already at first track")
            return False
        
        return self._play_track(prev_index)
    
    def jump_to_track(self, index: int) -> bool:
        """
        Jump to specific track in playlist.
        
        Args:
            index: Track index (0-based)
            
        Returns:
            True if jumped successfully, False if invalid index
        """
        if not self.playlist:
            return False
        
        if index < 0 or index >= len(self.playlist.tracks):
            print(f"ERROR: Invalid track index {index}")
            return False
        
        return self._play_track(index)
    
    def seek(self, seconds: float) -> bool:
        """
        Seek relative to current position.
        
        Args:
            seconds: Seconds to seek (positive = forward, negative = back)
            
        Returns:
            True if seeked successfully
        """
        if self.state == PlayerState.STOPPED:
            return False
        
        current = self.get_position()
        new_position = max(0, current + seconds)
        
        return self.seek_to(new_position)
    
    def seek_to(self, position: float) -> bool:
        """
        Seek to absolute position in current track.
        
        Args:
            position: Position in seconds
            
        Returns:
            True if seeked successfully
        """
        if self.state == PlayerState.STOPPED:
            return False
        
        # VLC uses milliseconds
        self.player.set_time(int(position * 1000))
        
        print(f"Seeked to {position:.1f}s")
        return True
    
    def get_position(self) -> float:
        """
        Get current playback position in seconds.
        
        Returns:
            Position in seconds, or 0 if not playing
        """
        if self.state == PlayerState.STOPPED:
            return 0.0
        
        # VLC returns milliseconds
        return self.player.get_time() / 1000.0
    
    def get_duration(self) -> float:
        """
        Get duration of current track in seconds.
        
        Returns:
            Duration in seconds, or 0 if no track loaded
        """
        if self.current_track_index < 0 or not self.playlist:
            return 0.0
        
        # VLC returns milliseconds
        vlc_duration = self.player.get_length() / 1000.0
        
        # Use VLC's duration if available, otherwise use metadata
        if vlc_duration > 0:
            return vlc_duration
        
        return self.playlist.get_current_track().duration
    
    def set_volume(self, volume: int) -> bool:
        """
        Set playback volume.
        
        Args:
            volume: Volume level 0-100
            
        Returns:
            True if set successfully
        """
        volume = max(0, min(100, volume))  # Clamp to 0-100
        self.player.audio_set_volume(volume)
        print(f"Volume set to {volume}%")
        
        return True
    
    def get_volume(self) -> int:
        """
        Get current volume level.
        
        Returns:
            Volume level 0-100
        """
        return self.player.audio_get_volume()
    
    def mute(self) -> bool:
        """Toggle mute on/off."""
        current = self.player.audio_get_mute()
        self.player.audio_set_mute(not current)
        
        print("Muted" if not current else "Unmuted")
        return True
    
    def get_current_track(self):
        """
        Get currently playing track.
        
        Returns:
            Track object or None
        """
        if not self.playlist or self.current_track_index < 0:
            return None
        
        return self.playlist.get_current_track()
    
    def get_state(self) -> PlayerState:
        """Get current player state."""
        return self.state
    
    def is_playing(self) -> bool:
        """Check if currently playing."""
        return self.state == PlayerState.PLAYING
    
    def _play_track(self, index: int, retry_count: int = 0) -> bool:
        """
        Internal method to play a specific track.
        
        Args:
            index: Track index to play
            retry_count: Current retry attempt
            
        Returns:
            True if started playing, False otherwise
        """
        if not self.playlist or index < 0 or index >= len(self.playlist.tracks):
            return False
        
        track = self.playlist.tracks[index]
        
        # Format duration as MM:SS
        duration_mins = int(track.duration // 60)
        duration_secs = int(track.duration % 60)
        duration_str = f"{duration_mins:02d}:{duration_secs:02d}"
        
        print(f"\nPlaying track {index + 1}/{len(self.playlist.tracks)}")
        print(f"  {track.set_name}: {track.title}")
        print(f"  Duration: {duration_str}")
        
        try:
            # Set loading state
            self.state = PlayerState.LOADING
            self._notify_state_changed()
            
            # Create media from URL
            media = self.instance.media_new(track.url)
            
            if not media:
                raise Exception("Failed to create media object")
            
            # Set media in player
            self.player.set_media(media)
            
            # Start playback
            result = self.player.play()
            
            if result == -1:
                raise Exception("VLC play() returned error")
            
            # Wait a moment for playback to actually start
            time.sleep(0.5)
            
            # Check if it's actually playing
            vlc_state = self.player.get_state()
            if vlc_state == vlc.State.Error:
                raise Exception("VLC entered error state")
            
            # Update state
            self.current_track_index = index
            self.state = PlayerState.PLAYING
            
            # Notify callbacks
            self._notify_state_changed()
            self._notify_track_changed()
            
            print(f"Successfully started playback")
            return True
            
        except Exception as e:
            print(f"ERROR playing track: {e}")
            
            # Retry logic for network errors
            if retry_count < self.max_retries:
                print(f"Retrying in {self.retry_delay} seconds... (attempt {retry_count + 1}/{self.max_retries})")
                time.sleep(self.retry_delay)
                return self._play_track(index, retry_count + 1)
            else:
                print(f"Failed to play track after {self.max_retries} attempts")
                self.state = PlayerState.ERROR
                self._notify_state_changed()
                return False
    
    def _on_track_ended(self, event):
        """
        Callback when track ends - automatically play next track.
        
        This is called by VLC's event manager.
        """
        print("\nTrack ended, moving to next...")
        
        # Small delay to ensure clean transition
        time.sleep(0.1)
        
        # Play next track
        if not self.next_track():
            # No more tracks - stop
            print("Playlist complete")
            self.stop()
    
    def _notify_state_changed(self):
        """Notify state change callback if registered."""
        if self.on_state_changed:
            self.on_state_changed(self.state)
    
    def _notify_track_changed(self):
        """Notify track change callback if registered."""
        if self.on_track_changed:
            track = self.get_current_track()
            if track:
                self.on_track_changed(track)
    
    def cleanup(self):
        """Clean up VLC resources."""
        print("\nCleaning up VLC player...")
        
        if self.player:
            self.player.stop()
            self.player.release()
        
        if self.instance:
            self.instance.release()
        
        print("VLC resources released")


# Example usage
if __name__ == "__main__":
    from .playlist import PlaylistBuilder
    from ..api.metadata import get_metadata
    
    print("=== VLC Player Test ===\n")
    
    # Build a playlist
    print("Building playlist for Cornell '77...")
    identifier = "gd77-05-08.sbd.hicks.4982.sbeok.shnf"
    metadata = get_metadata(identifier)
    
    builder = PlaylistBuilder()
    playlist = builder.build_from_metadata(metadata)
    
    # Create player
    print("\nCreating player...")
    player = VLCPlayer()
    
    # Load playlist
    print("\nLoading playlist...")
    player.load_playlist(playlist)
    
    # Play
    print("\nStarting playback...")
    player.play()
    
    # Let it play for 30 seconds
    print("\nPlaying for 30 seconds...")
    time.sleep(30)
    
    # Test controls
    print("\nTesting controls...")
    print(f"Current position: {player.get_position():.1f}s / {player.get_duration():.1f}s")
    
    print("\nSeeking forward 30 seconds...")
    player.seek(30)
    time.sleep(2)
    print(f"New position: {player.get_position():.1f}s")
    
    print("\nPausing...")
    player.pause()
    time.sleep(2)
    
    print("\nResuming...")
    player.play()
    time.sleep(5)
    
    print("\nSkipping to next track...")
    player.next_track()
    time.sleep(10)
    
    print("\nGoing back to previous track...")
    player.previous_track()
    time.sleep(10)
    
    print("\nStopping...")
    player.stop()
    
    print("\nCleaning up...")
    player.cleanup()
    
    print("\n=== Test Complete ===")
