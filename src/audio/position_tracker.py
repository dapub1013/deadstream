#!/usr/bin/env python3
"""
Playback Position Tracker for DeadStream

This module handles tracking the current playback position, calculating
progress, and formatting time displays for the UI.

Author: DeadStream Project
Phase: 4.5 - Track Playback Position
"""

from typing import Optional, Dict
import time


class PlaybackPosition:
    """
    Container for playback position information.
    All times are in seconds (not milliseconds).
    """
    
    def __init__(self, current_time: float = 0.0, total_time: float = 0.0):
        """
        Initialize position data.
        
        Args:
            current_time: Current position in seconds
            total_time: Total track duration in seconds
        """
        self.current_time = current_time
        self.total_time = total_time
    
    @property
    def percentage(self) -> float:
        """
        Calculate position as percentage (0.0 to 100.0).
        
        Returns:
            Percentage complete, or 0.0 if total_time is 0
        """
        if self.total_time > 0:
            return (self.current_time / self.total_time) * 100.0
        return 0.0
    
    @property
    def remaining_time(self) -> float:
        """
        Calculate remaining time in seconds.
        
        Returns:
            Seconds remaining, or 0.0 if unknown
        """
        if self.total_time > 0:
            return max(0.0, self.total_time - self.current_time)
        return 0.0
    
    def format_time(self, seconds: float) -> str:
        """
        Format time in seconds to MM:SS or H:MM:SS.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted string like "3:45" or "1:23:45"
        """
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    @property
    def current_time_formatted(self) -> str:
        """Get current time as formatted string (e.g., "3:45")"""
        return self.format_time(self.current_time)
    
    @property
    def total_time_formatted(self) -> str:
        """Get total time as formatted string (e.g., "11:23")"""
        return self.format_time(self.total_time)
    
    @property
    def remaining_time_formatted(self) -> str:
        """Get remaining time as formatted string (e.g., "7:38")"""
        return self.format_time(self.remaining_time)
    
    def to_dict(self) -> Dict:
        """
        Convert position data to dictionary for easy serialization.
        
        Returns:
            Dictionary with all position information
        """
        return {
            'current_time': self.current_time,
            'total_time': self.total_time,
            'percentage': self.percentage,
            'remaining_time': self.remaining_time,
            'current_formatted': self.current_time_formatted,
            'total_formatted': self.total_time_formatted,
            'remaining_formatted': self.remaining_time_formatted
        }
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        return (f"PlaybackPosition(current={self.current_time_formatted}, "
                f"total={self.total_time_formatted}, "
                f"progress={self.percentage:.1f}%)")


class PositionTracker:
    """
    Tracks playback position from a VLC media player instance.
    Polls the player periodically to get current position.
    """
    
    def __init__(self, player=None):
        """
        Initialize position tracker.
        
        Args:
            player: VLC MediaPlayer instance (optional, can be set later)
        """
        self.player = player
        self._last_update_time = 0
        self._update_interval = 0.5  # Update every 500ms
    
    def set_player(self, player):
        """
        Set or update the VLC player instance.
        
        Args:
            player: VLC MediaPlayer instance
        """
        self.player = player
    
    def get_position(self) -> Optional[PlaybackPosition]:
        """
        Get current playback position from VLC player.
        
        Returns:
            PlaybackPosition object, or None if player not available or not playing
        """
        if not self.player:
            return None
        
        try:
            # Get time values from VLC (in milliseconds)
            current_ms = self.player.get_time()
            total_ms = self.player.get_length()
            
            # VLC returns -1 if not available yet
            if current_ms < 0 or total_ms < 0:
                return None
            
            # Convert milliseconds to seconds
            current_seconds = current_ms / 1000.0
            total_seconds = total_ms / 1000.0
            
            return PlaybackPosition(current_seconds, total_seconds)
            
        except Exception as e:
            # Player might not be initialized yet
            return None
    
    def should_update(self) -> bool:
        """
        Check if enough time has passed for an update.
        Prevents excessive polling.
        
        Returns:
            True if we should fetch new position data
        """
        current_time = time.time()
        if current_time - self._last_update_time >= self._update_interval:
            self._last_update_time = current_time
            return True
        return False
    
    def set_update_interval(self, interval: float):
        """
        Set how often to poll for position updates.
        
        Args:
            interval: Update interval in seconds (e.g., 0.5 for 500ms)
        """
        self._update_interval = max(0.1, interval)  # Minimum 100ms


# Convenience function for quick position checks
def get_player_position(player) -> Optional[PlaybackPosition]:
    """
    Quick function to get position from a VLC player.
    
    Args:
        player: VLC MediaPlayer instance
        
    Returns:
        PlaybackPosition object, or None if not available
    """
    tracker = PositionTracker(player)
    return tracker.get_position()


# Example usage and testing
if __name__ == '__main__':
    print("PlaybackPosition Testing")
    print("=" * 60)
    
    # Test position calculations
    print("\n1. Testing position calculations:")
    pos = PlaybackPosition(current_time=215.5, total_time=682.0)
    print(f"   Position: {pos}")
    print(f"   Current: {pos.current_time_formatted}")
    print(f"   Total: {pos.total_time_formatted}")
    print(f"   Remaining: {pos.remaining_time_formatted}")
    print(f"   Progress: {pos.percentage:.1f}%")
    
    # Test edge cases
    print("\n2. Testing edge cases:")
    
    # Start of track
    pos_start = PlaybackPosition(0.0, 600.0)
    print(f"   Start: {pos_start}")
    
    # End of track
    pos_end = PlaybackPosition(600.0, 600.0)
    print(f"   End: {pos_end}")
    
    # Unknown duration
    pos_unknown = PlaybackPosition(30.0, 0.0)
    print(f"   Unknown duration: {pos_unknown}")
    
    # Long track (>1 hour)
    pos_long = PlaybackPosition(3725.0, 7200.0)
    print(f"   Long track: {pos_long}")
    print(f"   Formatted: {pos_long.current_time_formatted} / {pos_long.total_time_formatted}")
    
    # Test dictionary export
    print("\n3. Testing dictionary export:")
    import json
    print(json.dumps(pos.to_dict(), indent=2))
    
    print("\n" + "=" * 60)
    print("Position tracker ready for integration!")
