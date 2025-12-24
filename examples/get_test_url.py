#!/usr/bin/env python3
"""
Get Valid Test URL from DeadStream Database

This script queries your local database to find a good show
for testing, then fetches the actual streaming URLs from Archive.org.
"""

import sys
import os

# Add project to path
sys.path.insert(0, '/home/david/deadstream')

from src.database.queries import get_top_rated_shows, get_show_by_date
from src.api.metadata import get_metadata, extract_audio_files

def get_test_url():
    """Get a valid, working test URL for audio streaming"""
    
    print("Finding test show...")
    
    # Try Cornell '77 first (known to exist)
    print("\n1. Checking Cornell '77 (1977-05-08)...")
    cornell_shows = get_show_by_date('1977-05-08')
    
    if cornell_shows:
        # Get first Cornell recording
        show = cornell_shows[0]
        print(f"   Found: {show['identifier']}")
        
        # Get metadata to find audio files
        print("   Fetching metadata from Archive.org...")
        try:
            metadata = get_metadata(show['identifier'])
            audio_files = extract_audio_files(metadata)
            
            if audio_files:
                # Get first MP3 track
                first_track = audio_files[0]
                url = f"https://archive.org/download/{show['identifier']}/{first_track['name']}"
                
                print(f"\n[SUCCESS] Found valid test URL:")
                print(f"Show: {show['date']} - {show['venue']}")
                print(f"Identifier: {show['identifier']}")
                print(f"Track: {first_track['name']}")
                print(f"Format: {first_track['format']}")
                print(f"\nURL: {url}")
                return url
                
        except Exception as e:
            print(f"   Error getting metadata: {e}")
    
    # Fallback: Try a top-rated show
    print("\n2. Trying top-rated shows as fallback...")
    top_shows = get_top_rated_shows(limit=5, min_reviews=10)
    
    for show in top_shows:
        print(f"\n   Trying: {show['date']} - {show['venue']} (rating: {show['avg_rating']})")
        
        try:
            metadata = get_metadata(show['identifier'])
            audio_files = extract_audio_files(metadata)
            
            if audio_files:
                first_track = audio_files[0]
                url = f"https://archive.org/download/{show['identifier']}/{first_track['name']}"
                
                print(f"\n[SUCCESS] Found valid test URL:")
                print(f"Show: {show['date']} - {show['venue']}")
                print(f"Identifier: {show['identifier']}")
                print(f"Track: {first_track['name']}")
                print(f"\nURL: {url}")
                return url
                
        except Exception as e:
            print(f"   Error: {e}")
            continue
    
    print("\n[FAIL] Could not find a valid test URL")
    return None

if __name__ == '__main__':
    print("="*70)
    print("DeadStream - Get Valid Test URL")
    print("="*70)
    
    url = get_test_url()
    
    if url:
        print("\n" + "="*70)
        print("COPY THIS URL FOR TESTING:")
        print("="*70)
        print(url)
        print("\nUse this in your test scripts instead of hardcoded URLs")
    else:
        print("\nCould not find a working test URL.")
        print("Check your database and network connection.")
