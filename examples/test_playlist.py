#!/usr/bin/env python3
"""
Test playlist builder with real Archive.org data.

This script demonstrates:
1. Fetching metadata from Archive.org
2. Building a structured playlist
3. Displaying setlist information
4. Navigating through tracks
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.metadata import get_metadata
from src.audio.playlist import PlaylistBuilder, Playlist


def format_duration(seconds: float) -> str:
    """Format duration in seconds to MM:SS."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"


def display_playlist_info(playlist: Playlist):
    """Display comprehensive playlist information."""
    print("\n" + "="*70)
    print(f"SHOW: {playlist.date} - {playlist.venue}")
    print("="*70)
    
    print(f"\nIdentifier: {playlist.identifier}")
    print(f"Total tracks: {len(playlist)}")
    
    total_seconds = playlist.get_total_duration()
    total_mins = int(total_seconds // 60)
    print(f"Total duration: {total_mins} minutes ({format_duration(total_seconds)})")
    
    # Display tracks grouped by set
    print("\n" + "-"*70)
    print("SETLIST")
    print("-"*70)
    
    sets = playlist.get_sets()
    for set_name in sorted(sets.keys()):
        tracks = sets[set_name]
        set_duration = sum(t.duration for t in tracks)
        
        print(f"\n{set_name} ({len(tracks)} tracks, {format_duration(set_duration)}):")
        print("-" * 70)
        
        for i, track in enumerate(tracks, 1):
            print(f"  {i:2d}. {track.title:40s} {format_duration(track.duration)}")
    
    print("\n" + "="*70)


def test_navigation(playlist: Playlist):
    """Test playlist navigation features."""
    print("\n" + "="*70)
    print("PLAYLIST NAVIGATION TEST")
    print("="*70)
    
    # Get current track
    current = playlist.get_current_track()
    print(f"\nCurrent track: {current.title} ({current.set_name})")
    
    # Move forward
    print("\nMoving forward 3 tracks:")
    for _ in range(3):
        next_track = playlist.next_track()
        if next_track:
            print(f"  → {next_track.title} ({next_track.set_name})")
    
    # Move backward
    print("\nMoving backward 2 tracks:")
    for _ in range(2):
        prev_track = playlist.previous_track()
        if prev_track:
            print(f"  ← {prev_track.title} ({prev_track.set_name})")
    
    # Jump to specific track
    print("\nJumping to track 10:")
    track = playlist.jump_to_track(9)  # 0-indexed
    if track:
        print(f"  Jumped to: {track.title} ({track.set_name})")


def test_with_cornell_77():
    """Test with the famous Cornell '77 show."""
    print("\nFetching Cornell '77 metadata from Archive.org...")
    print("(This may take a few seconds...)")
    
    identifier = 'gd77-05-08.sbd.hicks.4982.sbeok.shnf'
    
    try:
        # Fetch metadata
        metadata = get_metadata(identifier)
        
        # Build playlist
        playlist = PlaylistBuilder.build_from_metadata(metadata)
        
        # Display information
        display_playlist_info(playlist)
        
        # Test navigation
        test_navigation(playlist)
        
        # Show first 3 streaming URLs
        print("\n" + "="*70)
        print("SAMPLE STREAMING URLS (first 3 tracks)")
        print("="*70)
        for i in range(min(3, len(playlist))):
            track = playlist.get_track(i)
            print(f"\nTrack {i+1}: {track.title}")
            print(f"URL: {track.url}")
        
        return playlist
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nThis could be due to:")
        print("  - Network connection issues")
        print("  - Archive.org temporary unavailability")
        print("  - Invalid identifier")
        return None


def test_different_show():
    """Test with another show (different naming convention)."""
    print("\n\n" + "="*70)
    print("TESTING WITH DIFFERENT SHOW")
    print("="*70)
    
    # Try a 1969 show (different era, different naming)
    identifier = 'gd1969-08-16.sbd.miller.29539.flac16'
    
    print(f"\nFetching metadata for {identifier}...")
    
    try:
        metadata = get_metadata(identifier)
        playlist = PlaylistBuilder.build_from_metadata(metadata)
        
        # Show just the basic info
        print(f"\nShow: {playlist.date} - {playlist.venue}")
        print(f"Tracks: {len(playlist)}")
        
        # Show sets
        sets = playlist.get_sets()
        print(f"Sets detected: {', '.join(sorted(sets.keys()))}")
        
        return playlist
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def main():
    """Main test function."""
    print("="*70)
    print("PLAYLIST BUILDER TEST")
    print("="*70)
    
    # Test with Cornell '77
    playlist1 = test_with_cornell_77()
    
    # Test with another show
    playlist2 = test_different_show()
    
    # Summary
    print("\n\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    if playlist1:
        print(f"\n✓ Cornell '77: {len(playlist1)} tracks, "
              f"{int(playlist1.get_total_duration() / 60)} minutes")
    else:
        print("\n✗ Cornell '77: Failed to build playlist")
    
    if playlist2:
        print(f"✓ Test show 2: {len(playlist2)} tracks, "
              f"{int(playlist2.get_total_duration() / 60)} minutes")
    else:
        print("✗ Test show 2: Failed to build playlist")
    
    print("\n" + "="*70)
    
    if playlist1:
        print("\n✓ Playlist builder working correctly!")
        print("\nNext steps:")
        print("  1. Add playlist.py to src/audio/")
        print("  2. Test with VLC player (Task 4.4)")
        print("  3. Integrate with database queries (Phase 3)")
    else:
        print("\n⚠ Check network connection and try again")


if __name__ == '__main__':
    main()
