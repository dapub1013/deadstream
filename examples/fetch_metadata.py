#!/usr/bin/env python3
"""
Phase 2.3: Fetch and parse show metadata from Internet Archive

This script demonstrates:
1. How to fetch complete metadata for a show
2. How to parse the JSON response
3. How to extract useful information
4. How to display it in a readable format

Usage:
    python3 fetch_metadata.py <identifier>
    python3 fetch_metadata.py gd77-05-08.sbd.hicks.4982.sbeok.shnf
"""

import requests
import sys
import json
from datetime import datetime


def fetch_metadata(identifier):
    """
    Fetch complete metadata for a show from Internet Archive.
    
    Args:
        identifier (str): The Archive.org identifier for the show
        
    Returns:
        dict: Complete metadata, or None if error
    """
    url = f"https://archive.org/metadata/{identifier}"
    
    try:
        print(f"Fetching metadata for: {identifier}")
        print(f"URL: {url}\n")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        metadata = response.json()
        return metadata
        
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
        return None


def parse_show_info(metadata):
    """
    Extract show information from metadata.
    
    Args:
        metadata (dict): Complete metadata from API
        
    Returns:
        dict: Parsed show information
    """
    # The metadata structure has a 'metadata' key with show info
    show_meta = metadata.get('metadata', {})
    
    info = {
        'identifier': show_meta.get('identifier', 'Unknown'),
        'title': show_meta.get('title', 'Unknown'),
        'date': show_meta.get('date', 'Unknown'),
        'venue': show_meta.get('venue', 'Unknown'),
        'coverage': show_meta.get('coverage', 'Unknown'),  # Often has city, state
        'description': show_meta.get('description', 'No description'),
        'source': show_meta.get('source', 'Unknown'),
        'taper': show_meta.get('taper', 'Unknown'),
        'transferer': show_meta.get('transferer', 'Unknown'),
        'lineage': show_meta.get('lineage', 'Unknown'),
        'avg_rating': show_meta.get('avg_rating', 'Not rated'),
        'num_reviews': show_meta.get('num_reviews', 0),
    }
    
    return info


def parse_audio_files(metadata):
    """
    Extract audio file information from metadata.
    
    Args:
        metadata (dict): Complete metadata from API
        
    Returns:
        list: List of audio files with relevant info
    """
    files = metadata.get('files', [])
    
    # Filter for audio files
    audio_files = []
    for file in files:
        # Look for MP3, FLAC, OGG files
        format_name = file.get('format', '').upper()
        if any(fmt in format_name for fmt in ['MP3', 'FLAC', 'OGG', 'VBR']):
            audio_files.append({
                'name': file.get('name', 'Unknown'),
                'format': format_name,
                'size': file.get('size', 'Unknown'),
                'length': file.get('length', 'Unknown'),  # Duration in seconds
                'track': file.get('track', 'Unknown'),
                'title': file.get('title', 'Unknown'),
            })
    
    return audio_files


def format_duration(seconds):
    """Convert seconds to MM:SS format."""
    if not seconds or seconds == 'Unknown':
        return 'Unknown'
    
    try:
        seconds = float(seconds)
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    except (ValueError, TypeError):
        return 'Unknown'


def format_size(bytes_size):
    """Convert bytes to human-readable format."""
    if not bytes_size or bytes_size == 'Unknown':
        return 'Unknown'
    
    try:
        bytes_size = int(bytes_size)
        if bytes_size < 1024:
            return f"{bytes_size} B"
        elif bytes_size < 1024 * 1024:
            return f"{bytes_size / 1024:.1f} KB"
        elif bytes_size < 1024 * 1024 * 1024:
            return f"{bytes_size / (1024 * 1024):.1f} MB"
        else:
            return f"{bytes_size / (1024 * 1024 * 1024):.2f} GB"
    except (ValueError, TypeError):
        return 'Unknown'


def print_show_info(info):
    """Print show information in a readable format."""
    print("=" * 70)
    print("SHOW INFORMATION")
    print("=" * 70)
    print(f"Title:       {info['title']}")
    print(f"Date:        {info['date']}")
    print(f"Venue:       {info['venue']}")
    print(f"Location:    {info['coverage']}")
    print(f"Identifier:  {info['identifier']}")
    print(f"\nRating:      {info['avg_rating']} ({info['num_reviews']} reviews)")
    print(f"\nSource:      {info['source']}")
    print(f"Taper:       {info['taper']}")
    print(f"Transfer:    {info['transferer']}")
    print(f"Lineage:     {info['lineage']}")
    print(f"\nDescription: {info['description'][:200]}")
    if len(info['description']) > 200:
        print("             ... (truncated)")
    print()


def print_audio_files(audio_files):
    """Print audio file information in a readable format."""
    print("=" * 70)
    print("AUDIO FILES")
    print("=" * 70)
    print(f"Found {len(audio_files)} audio files\n")
    
    # Group by format
    formats = {}
    for file in audio_files:
        format_name = file['format']
        if format_name not in formats:
            formats[format_name] = []
        formats[format_name].append(file)
    
    # Print by format
    for format_name, files in formats.items():
        print(f"\n{format_name} Files ({len(files)} files):")
        print("-" * 70)
        
        for idx, file in enumerate(files[:10], 1):  # Limit to first 10 per format
            print(f"\n{idx}. {file['name']}")
            if file['title'] != 'Unknown':
                print(f"   Title:    {file['title']}")
            print(f"   Duration: {format_duration(file['length'])}")
            print(f"   Size:     {format_size(file['size'])}")
        
        if len(files) > 10:
            print(f"\n... and {len(files) - 10} more {format_name} files")
    
    print()


def main():
    """Main function."""
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_metadata.py <identifier>")
        print("\nExample identifiers:")
        print("  gd77-05-08.sbd.hicks.4982.sbeok.shnf  (Cornell '77)")
        print("  gd1970-02-13.sbd.miller.97187.flac16  (Fillmore '70)")
        print("  gd1972-05-26.sbd.hollister.4844.sbeok.shnf  (Europe '72)")
        sys.exit(1)
    
    identifier = sys.argv[1]
    
    # Fetch metadata
    metadata = fetch_metadata(identifier)
    if not metadata:
        print("Failed to fetch metadata")
        sys.exit(1)
    
    # Parse show info
    show_info = parse_show_info(metadata)
    print_show_info(show_info)
    
    # Parse audio files
    audio_files = parse_audio_files(metadata)
    print_audio_files(audio_files)
    
    # Save raw metadata for inspection (optional)
    print("=" * 70)
    save = input("Save raw metadata to file? (y/n): ").lower()
    if save == 'y':
        filename = f"{identifier}_metadata.json"
        with open(filename, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Raw metadata saved to: {filename}")
        print(f"You can inspect it with: cat {filename} | less")
    
    print("\nPhase 2.3 complete!")


if __name__ == "__main__":
    main()
