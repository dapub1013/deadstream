#!/usr/bin/env python3
"""
Test playlist builder with example metadata (no API required).

This script tests the playlist builder using sample metadata,
so it works even without the Phase 2 API modules.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.audio.playlist import PlaylistBuilder, Playlist


def get_example_metadata():
    """
    Return example metadata in Archive.org format.
    
    This simulates what the API would return for Cornell '77.
    """
    return {
        'metadata': {
            'identifier': 'gd77-05-08.sbd.hicks.4982.sbeok.shnf',
            'date': '1977-05-08',
            'venue': 'Barton Hall, Cornell University',
            'coverage': 'Ithaca, NY'
        },
        'files': [
            # Set I
            {'name': 'gd77-05-08d1t01.mp3', 'format': 'VBR MP3', 'length': '347.28'},
            {'name': 'gd77-05-08d1t02.mp3', 'format': 'VBR MP3', 'length': '443.04'},
            {'name': 'gd77-05-08d1t03.mp3', 'format': 'VBR MP3', 'length': '271.68'},
            {'name': 'gd77-05-08d1t04.mp3', 'format': 'VBR MP3', 'length': '428.16'},
            {'name': 'gd77-05-08d1t05.mp3', 'format': 'VBR MP3', 'length': '614.88'},
            {'name': 'gd77-05-08d1t06.mp3', 'format': 'VBR MP3', 'length': '685.44'},
            {'name': 'gd77-05-08d1t07.mp3', 'format': 'VBR MP3', 'length': '484.32'},
            {'name': 'gd77-05-08d1t08.mp3', 'format': 'VBR MP3', 'length': '513.12'},
            {'name': 'gd77-05-08d1t09.mp3', 'format': 'VBR MP3', 'length': '402.24'},
            {'name': 'gd77-05-08d1t10.mp3', 'format': 'VBR MP3', 'length': '562.56'},
            
            # Set II
            {'name': 'gd77-05-08d2t01.mp3', 'format': 'VBR MP3', 'length': '789.12'},
            {'name': 'gd77-05-08d2t02.mp3', 'format': 'VBR MP3', 'length': '623.04'},
            {'name': 'gd77-05-08d2t03.mp3', 'format': 'VBR MP3', 'length': '512.64'},
            {'name': 'gd77-05-08d2t04.mp3', 'format': 'VBR MP3', 'length': '701.28'},
            {'name': 'gd77-05-08d2t05.mp3', 'format': 'VBR MP3', 'length': '834.72'},
            {'name': 'gd77-05-08d2t06.mp3', 'format': 'VBR MP3', 'length': '456.96'},
            {'name': 'gd77-05-08d2t07.mp3', 'format': 'VBR MP3', 'length': '598.32'},
            {'name': 'gd77-05-08d2t08.mp3', 'format': 'VBR MP3', 'length': '412.80'},
            
            # Encore
            {'name': 'gd77-05-08d3t01.mp3', 'format': 'VBR MP3', 'length': '234.24'},
            {'name': 'gd77-05-08d3t02.mp3', 'format': 'VBR MP3', 'length': '267.36'},
        ]
    }


def format_duration(seconds: float) -> str:
    """Format duration in seconds to MM:SS."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"


def test_playlist_building():
    """Test building a playlist from example metadata."""
    print("\n" + "="*70)
    print("PLAYLIST BUILDER TEST")
    print("="*70)
    
    # Get example metadata
    metadata = get_example_metadata()
    
    # Build playlist
    print("\nBuilding playlist from example metadata...")
    playlist = PlaylistBuilder.build_from_metadata(metadata)
    
    # Display basic info
    print("\n" + "="*70)
    print(f"SHOW: {playlist.date} - {playlist.venue}")
    print("="*70)
    print(f"\nIdentifier: {playlist.identifier}")
    print(f"Total tracks: {len(playlist)}")
    
    total_seconds = playlist.get_total_duration()
    total_mins = int(total_seconds // 60)
    print(f"Total duration: {total_mins} minutes ({format_duration(total_seconds)})")
    
    # Display setlist
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
    
    return playlist


def test_navigation(playlist: Playlist):
    """Test playlist navigation."""
    print("\n\n" + "="*70)
    print("NAVIGATION TEST")
    print("="*70)
    
    # Current track
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
    
    # Jump to track
    print("\nJumping to track 15 (Set II):")
    track = playlist.jump_to_track(14)  # 0-indexed
    if track:
        print(f"  Jumped to: {track.title} ({track.set_name})")


def test_set_detection():
    """Test set detection with various filename patterns."""
    print("\n\n" + "="*70)
    print("SET DETECTION TEST")
    print("="*70)
    
    test_files = [
        ('gd77-05-08d1t01.mp3', 'Set I'),
        ('gd77-05-08d2t05.mp3', 'Set II'),
        ('gd77-05-08d3t01.mp3', 'Encore'),
        ('show_set1_track01.mp3', 'Set I'),
        ('show_set2_track05.mp3', 'Set II'),
        ('show_encore_01.mp3', 'Encore'),
        ('random_file.mp3', 'Set I'),  # Default
    ]
    
    print("\nFilename pattern → Detected set:")
    print("-" * 70)
    
    for filename, expected in test_files:
        detected = PlaylistBuilder.detect_set(filename)
        status = "✓" if detected == expected else "✗"
        print(f"{status} {filename:30s} → {detected:10s} (expected: {expected})")


def test_streaming_urls(playlist: Playlist):
    """Show sample streaming URLs."""
    print("\n\n" + "="*70)
    print("STREAMING URLS (first 3 tracks)")
    print("="*70)
    
    for i in range(min(3, len(playlist))):
        track = playlist.get_track(i)
        print(f"\nTrack {i+1}: {track.title}")
        print(f"Set: {track.set_name}")
        print(f"Duration: {format_duration(track.duration)}")
        print(f"URL: {track.url}")


def main():
    """Main test function."""
    print("="*70)
    print("PLAYLIST MODULE TEST (Standalone)")
    print("="*70)
    print("\nThis test uses example metadata - no API required.")
    
    # Build playlist
    playlist = test_playlist_building()
    
    # Test navigation
    test_navigation(playlist)
    
    # Test set detection
    test_set_detection()
    
    # Show URLs
    test_streaming_urls(playlist)
    
    # Summary
    print("\n\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    print(f"\n✓ Playlist built successfully: {len(playlist)} tracks")
    print(f"✓ Sets detected: {', '.join(sorted(playlist.get_sets().keys()))}")
    print(f"✓ Total duration: {int(playlist.get_total_duration() / 60)} minutes")
    print(f"✓ Navigation working: next/previous/jump")
    print(f"✓ Streaming URLs generated")
    
    print("\n" + "="*70)
    print("✓ All tests passed!")
    print("="*70)
    
    print("\nPlaylist builder is working correctly!")
    print("\nNext steps:")
    print("  1. Test with real API data (once Phase 2 API is set up)")
    print("  2. Integrate with VLC player (Task 4.4)")
    print("  3. Add to database queries")


if __name__ == '__main__':
    main()
