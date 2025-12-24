#!/usr/bin/env python3
"""
Get Valid Test URL from DeadStream Database

This script queries your local database to find a good show
for testing, then fetches the actual streaming URLs from Archive.org.

Can be used as:
1. Standalone script: python examples/get_test_url.py
2. Imported module: from examples.get_test_url import get_test_url
"""

import sys
import os

# Add project to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.database.queries import get_top_rated_shows, get_show_by_date
from src.api.metadata import get_metadata, extract_audio_files


def get_test_url(verbose=True):
    """
    Get a valid, working test URL for audio streaming.
    
    Args:
        verbose: If True, print progress messages
        
    Returns:
        str: Valid streaming URL, or None if none found
    """
    
    if verbose:
        print("Finding test show...")
    
    # Try Cornell '77 first (known to exist)
    if verbose:
        print("\n1. Checking Cornell '77 (1977-05-08)...")
    
    cornell_shows = get_show_by_date('1977-05-08')
    
    if cornell_shows:
        # Get first Cornell recording
        show = cornell_shows[0]
        if verbose:
            print(f"   Found: {show['identifier']}")
        
        # Get metadata to find audio files
        if verbose:
            print("   Fetching metadata from Archive.org...")
        
        try:
            metadata = get_metadata(show['identifier'])
            audio_files = extract_audio_files(metadata)
            
            if audio_files:
                # Get first MP3 track
                first_track = audio_files[0]
                url = f"https://archive.org/download/{show['identifier']}/{first_track['name']}"
                
                if verbose:
                    print(f"\n[SUCCESS] Found valid test URL:")
                    print(f"Show: {show['date']} - {show.get('venue', 'Unknown')}")
                    print(f"Identifier: {show['identifier']}")
                    print(f"Track: {first_track['name']}")
                    print(f"Format: {first_track.get('format', 'Unknown')}")
                    print(f"\nURL: {url}")
                
                return url
                
        except Exception as e:
            if verbose:
                print(f"   Error getting metadata: {e}")
    
    # Fallback: Try a top-rated show
    if verbose:
        print("\n2. Trying top-rated shows as fallback...")
    
    top_shows = get_top_rated_shows(limit=5, min_reviews=10)
    
    for show in top_shows:
        if verbose:
            print(f"\n   Trying: {show['date']} - {show.get('venue', 'Unknown')} "
                  f"(rating: {show.get('avg_rating', 'N/A')})")
        
        try:
            metadata = get_metadata(show['identifier'])
            audio_files = extract_audio_files(metadata)
            
            if audio_files:
                first_track = audio_files[0]
                url = f"https://archive.org/download/{show['identifier']}/{first_track['name']}"
                
                if verbose:
                    print(f"\n[SUCCESS] Found valid test URL:")
                    print(f"Show: {show['date']} - {show.get('venue', 'Unknown')}")
                    print(f"Identifier: {show['identifier']}")
                    print(f"Track: {first_track['name']}")
                    print(f"\nURL: {url}")
                
                return url
                
        except Exception as e:
            if verbose:
                print(f"   Error: {e}")
            continue
    
    if verbose:
        print("\n[FAIL] Could not find a valid test URL")
    
    return None


def main():
    """Main function when run as script"""
    print("="*70)
    print("DeadStream - Get Valid Test URL")
    print("="*70)
    
    url = get_test_url(verbose=True)
    
    if url:
        print("\n" + "="*70)
        print("COPY THIS URL FOR TESTING:")
        print("="*70)
        print(url)
        print("\nUse this in your test scripts instead of hardcoded URLs")
        print("\nOr import this function:")
        print("  from examples.get_test_url import get_test_url")
        print("  test_url = get_test_url(verbose=False)")
        return 0
    else:
        print("\nCould not find a working test URL.")
        print("Check your database and network connection.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
