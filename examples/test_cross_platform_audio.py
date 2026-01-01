#!/usr/bin/env python3
"""
Cross-Platform Audio Test - Phase 9.8

Tests audio playback on both macOS (development) and Linux (production).
Automatically adapts to the host platform.

This demonstrates:
- Platform detection
- Audio playback on macOS speakers/headphones
- Audio playback on Raspberry Pi
- Same code works on both platforms

Usage:
    # On macOS (development)
    python examples/test_cross_platform_audio.py
    
    # On Raspberry Pi (production)  
    python examples/test_cross_platform_audio.py

Author: DeadStream Project
Phase: 9.8 - Cross-Platform Development
"""

import sys
import os
import time

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.database.queries import get_show_by_date, get_top_rated_shows
from src.api.metadata import get_metadata, extract_audio_files
from src.audio.resilient_player import ResilientPlayer
from src.audio.vlc_config import get_platform_info


def get_test_url():
    """
    Get a valid test URL from database
    
    Returns:
        str: URL to audio file, or None if not found
    """
    print("[INFO] Getting test URL from database...")
    
    # Try Cornell '77 first
    shows = get_show_by_date('1977-05-08')
    
    # Fallback to top-rated shows
    if not shows:
        print("[INFO] Cornell '77 not found, using top-rated shows")
        shows = get_top_rated_shows(limit=3, min_reviews=5)
    
    # Try each show until we get valid audio
    for show in shows[:3]:
        try:
            print(f"[INFO] Trying show: {show['identifier']}")
            metadata = get_metadata(show['identifier'])
            audio_files = extract_audio_files(metadata)
            
            if audio_files:
                url = f"https://archive.org/download/{show['identifier']}/{audio_files[0]['name']}"
                print(f"[PASS] Got test URL: {audio_files[0]['name']}")
                return url
        except Exception as e:
            print(f"[WARN] Failed to get metadata: {e}")
            continue
    
    return None


def main():
    """Run cross-platform audio test"""
    print("=" * 70)
    print("DeadStream Cross-Platform Audio Test")
    print("=" * 70)
    
    # Show platform info
    info = get_platform_info()
    print(f"\n[INFO] Platform Detection:")
    print(f"  System: {info['system']}")
    print(f"  Platform Type: {info['platform_type']}")
    print(f"  Machine: {info['machine']}")
    
    if info['platform_type'] == 'macos':
        print("\n[INFO] Running on macOS - will use Mac speakers/headphones")
    elif info['platform_type'] == 'linux':
        print("\n[INFO] Running on Linux - will use ALSA (Pi headphone jack)")
    else:
        print(f"\n[WARN] Unknown platform: {info['system']}")
    
    # Get test URL
    print("\n" + "=" * 70)
    test_url = get_test_url()
    
    if not test_url:
        print("[FAIL] Could not get valid test URL")
        return 1
    
    # Create player (debug mode to see VLC config)
    print("\n" + "=" * 70)
    print("Creating audio player...")
    player = ResilientPlayer(debug=True)
    
    # Load and play
    print("\n" + "=" * 70)
    print("Loading audio...")
    if not player.load_url(test_url):
        print("[FAIL] Failed to load URL")
        return 1
    
    print("\n[INFO] Starting playback...")
    print("[INFO] You should hear audio from your:")
    if info['platform_type'] == 'macos':
        print("  - Mac speakers")
        print("  - or Mac headphones")
    elif info['platform_type'] == 'linux':
        print("  - Raspberry Pi headphone jack")
        print("  - or connected speakers")
    
    if not player.play():
        print("[FAIL] Failed to start playback")
        return 1
    
    # Let it play for 10 seconds
    print("\n[INFO] Playing for 10 seconds...")
    for i in range(10):
        time.sleep(1)
        
        # Show position
        position = player.get_position()
        duration = player.get_duration()
        
        if duration > 0:
            pos_str = format_time(position)
            dur_str = format_time(duration)
            pct = int((position / duration) * 100)
            print(f"  Position: {pos_str} / {dur_str} ({pct}%)")
        else:
            print(f"  Position: {format_time(position)}")
    
    # Test volume control
    print("\n" + "=" * 70)
    print("Testing volume control...")
    
    print("[INFO] Setting volume to 30%...")
    player.set_volume(30)
    time.sleep(2)
    
    print("[INFO] Setting volume to 70%...")
    player.set_volume(70)
    time.sleep(2)
    
    print("[INFO] Muting...")
    player.mute()
    time.sleep(2)
    
    print("[INFO] Unmuting...")
    player.unmute()
    time.sleep(2)
    
    # Cleanup
    print("\n" + "=" * 70)
    print("Stopping playback...")
    player.cleanup()
    
    print("\n" + "=" * 70)
    print("[PASS] Cross-platform audio test complete!")
    print("\nThis same code works on:")
    print("  - macOS (development)")
    print("  - Linux/Raspberry Pi (production)")
    print("=" * 70)
    
    return 0


def format_time(milliseconds):
    """Format milliseconds as MM:SS"""
    if milliseconds < 0:
        return "00:00"
    
    total_seconds = milliseconds // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


if __name__ == '__main__':
    sys.exit(main())
