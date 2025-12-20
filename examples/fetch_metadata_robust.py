#!/usr/bin/env python3
"""
Phase 2.5: Robust metadata fetching with comprehensive error handling

This is an improved version of fetch_metadata.py that demonstrates:
1. Retry logic with exponential backoff
2. User-friendly error messages
3. Network connectivity checking
4. Graceful degradation (partial data is okay)
5. Input validation

Usage:
    python3 fetch_metadata_robust.py <identifier>
    python3 fetch_metadata_robust.py gd77-05-08.sbd.hicks.4982.sbeok.shnf
"""

import sys
import json
from pathlib import Path

# Add src to path so we can import our helpers
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.helpers import (
    fetch_with_retry,
    safe_get,
    validate_identifier,
    print_error,
    NetworkError,
    APIError,
    check_network
)


def fetch_metadata(identifier, verbose=True):
    """
    Fetch metadata with robust error handling.
    
    Args:
        identifier (str): Archive.org identifier
        verbose (bool): Print progress messages
        
    Returns:
        dict: Metadata, or None if failed
    """
    # Validate identifier first
    if not validate_identifier(identifier):
        raise ValueError(f"Invalid identifier format: {identifier}")
    
    url = f"https://archive.org/metadata/{identifier}"
    
    if verbose:
        print(f"Fetching metadata for: {identifier}")
        print(f"URL: {url}\n")
    
    try:
        metadata = fetch_with_retry(url, verbose=verbose)
        return metadata
    except (NetworkError, APIError) as e:
        raise


def parse_show_info(metadata):
    """
    Extract show information with safe navigation.
    
    Args:
        metadata (dict): Complete metadata from API
        
    Returns:
        dict: Parsed show information (always returns, never None)
    """
    # Use safe_get for all fields
    show_meta = metadata.get('metadata', {})
    
    info = {
        'identifier': safe_get(show_meta, 'identifier', default='Unknown'),
        'title': safe_get(show_meta, 'title', default='Unknown Show'),
        'date': safe_get(show_meta, 'date', default='Unknown Date'),
        'venue': safe_get(show_meta, 'venue', default='Unknown Venue'),
        'coverage': safe_get(show_meta, 'coverage', default=''),
        'description': safe_get(show_meta, 'description', default='No description available'),
        'source': safe_get(show_meta, 'source', default='Unknown'),
        'taper': safe_get(show_meta, 'taper', default='Unknown'),
        'transferer': safe_get(show_meta, 'transferer', default='Unknown'),
        'lineage': safe_get(show_meta, 'lineage', default='Unknown'),
        'avg_rating': safe_get(show_meta, 'avg_rating', default=None),
        'num_reviews': safe_get(show_meta, 'num_reviews', default=0),
    }
    
    return info


def parse_audio_files(metadata):
    """
    Extract audio files with error handling.
    
    Args:
        metadata (dict): Complete metadata from API
        
    Returns:
        list: Audio files (may be empty if none found)
    """
    files = metadata.get('files', [])
    
    if not files:
        return []
    
    audio_files = []
    for file in files:
        try:
            format_name = safe_get(file, 'format', default='').upper()
            if any(fmt in format_name for fmt in ['MP3', 'FLAC', 'OGG', 'VBR']):
                audio_files.append({
                    'name': safe_get(file, 'name', default='Unknown'),
                    'format': format_name,
                    'size': safe_get(file, 'size', default='Unknown'),
                    'length': safe_get(file, 'length', default='Unknown'),
                    'track': safe_get(file, 'track', default='Unknown'),
                    'title': safe_get(file, 'title', default=''),
                })
        except Exception as e:
            # Skip files that cause errors but continue processing
            continue
    
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
    """Print show information."""
    print("=" * 70)
    print("SHOW INFORMATION")
    print("=" * 70)
    print(f"Title:       {info['title']}")
    print(f"Date:        {info['date']}")
    print(f"Venue:       {info['venue']}")
    if info['coverage']:
        print(f"Location:    {info['coverage']}")
    print(f"Identifier:  {info['identifier']}")
    
    if info['avg_rating']:
        print(f"\nRating:      {info['avg_rating']}/5.0 ({info['num_reviews']} reviews)")
    else:
        print(f"\nRating:      Not rated")
    
    print(f"\nSource:      {info['source']}")
    print(f"Taper:       {info['taper']}")
    print(f"Transfer:    {info['transferer']}")
    
    if info['lineage'] != 'Unknown':
        print(f"Lineage:     {info['lineage']}")
    
    desc = info['description']
    if len(desc) > 200:
        print(f"\nDescription: {desc[:200]}...")
    else:
        print(f"\nDescription: {desc}")
    print()


def print_audio_files(audio_files):
    """Print audio file information."""
    print("=" * 70)
    print("AUDIO FILES")
    print("=" * 70)
    
    if not audio_files:
        print("No audio files found")
        print()
        return
    
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
        
        for idx, file in enumerate(files[:10], 1):
            print(f"\n{idx}. {file['name']}")
            if file['title']:
                print(f"   Title:    {file['title']}")
            print(f"   Duration: {format_duration(file['length'])}")
            print(f"   Size:     {format_size(file['size'])}")
        
        if len(files) > 10:
            print(f"\n... and {len(files) - 10} more {format_name} files")
    
    print()


def main():
    """Main function with comprehensive error handling."""
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_metadata_robust.py <identifier>")
        print("\nExample identifiers:")
        print("  gd77-05-08.sbd.hicks.4982.sbeok.shnf  (Cornell '77)")
        print("  gd1970-02-13.sbd.miller.97187.flac16  (Fillmore '70)")
        print("  gd1972-05-26.sbd.hollister.4844.sbeok.shnf  (Europe '72)")
        sys.exit(1)
    
    identifier = sys.argv[1]
    
    # Check network first
    print("Checking network connectivity...")
    if not check_network():
        print_error(
            NetworkError("No network connection available"),
            "checking connectivity",
            exit_code=1
        )
    print("Network OK\n")
    
    # Fetch metadata
    try:
        metadata = fetch_metadata(identifier, verbose=True)
        
        if not metadata:
            print("Warning: Empty metadata returned")
            sys.exit(1)
        
    except ValueError as e:
        print_error(e, "validating identifier", exit_code=1)
    except NetworkError as e:
        print_error(e, f"fetching metadata for {identifier}", exit_code=1)
    except APIError as e:
        print_error(e, f"fetching metadata for {identifier}", exit_code=1)
    except Exception as e:
        print_error(e, f"fetching metadata for {identifier}", exit_code=1)
    
    # Parse show info (should always work even with partial data)
    try:
        show_info = parse_show_info(metadata)
        print_show_info(show_info)
    except Exception as e:
        print("Warning: Could not parse show information")
        print(f"Error: {e}\n")
    
    # Parse audio files (may return empty list)
    try:
        audio_files = parse_audio_files(metadata)
        print_audio_files(audio_files)
    except Exception as e:
        print("Warning: Could not parse audio files")
        print(f"Error: {e}\n")
    
    # Offer to save raw metadata
    print("=" * 70)
    try:
        save = input("Save raw metadata to file? (y/n): ").lower()
        if save == 'y':
            filename = f"{identifier}_metadata.json"
            with open(filename, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"Raw metadata saved to: {filename}")
    except KeyboardInterrupt:
        print("\nSkipping save")
    except IOError as e:
        print(f"Error saving file: {e}")
    
    print("\nPhase 2.5: Robust error handling complete!")


if __name__ == "__main__":
    main()
