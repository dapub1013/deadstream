#!/usr/bin/env python3
"""
Internet Archive Metadata API

This module provides functions for fetching show metadata from Archive.org.
It wraps the ArchiveClient to provide a simple functional interface.
"""

import requests
from typing import Dict, Any, Optional
from .archive_client import ArchiveClient


# Create a shared client instance
_client = ArchiveClient()


def get_metadata(identifier: str) -> Dict[str, Any]:
    """
    Get complete metadata for a show from Archive.org.
    
    Args:
        identifier: Show identifier (e.g., 'gd77-05-08.sbd.hicks.4982.sbeok.shnf')
        
    Returns:
        Dictionary containing metadata and files
        
    Example:
        metadata = get_metadata('gd77-05-08.sbd.hicks.4982.sbeok.shnf')
        print(metadata['metadata']['date'])
        print(metadata['metadata']['venue'])
        for file in metadata['files']:
            print(file['name'])
    """
    url = f"{_client.BASE_METADATA_URL}/{identifier}"
    
    try:
        response = requests.get(url, timeout=_client.timeout)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        raise Exception(f"Timeout fetching metadata for {identifier}")
    except requests.exceptions.ConnectionError:
        raise Exception(f"Network error fetching metadata for {identifier}")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error fetching metadata for {identifier}: {e}")
    except Exception as e:
        raise Exception(f"Error fetching metadata for {identifier}: {e}")


def get_show_info(identifier: str) -> Dict[str, Any]:
    """
    Get basic show information (metadata section only).
    
    Args:
        identifier: Show identifier
        
    Returns:
        Dictionary with show metadata (date, venue, etc.)
    """
    metadata = get_metadata(identifier)
    return metadata.get('metadata', {})


def extract_audio_files(metadata: Dict[str, Any], 
                       format_preference: str = 'MP3') -> list:
    """
    Extract audio files from metadata.
    
    Args:
        metadata: Full metadata dictionary from get_metadata()
        format_preference: Preferred format ('MP3', 'FLAC', 'OGG')
        
    Returns:
        List of audio file dictionaries
    """
    files = metadata.get('files', [])
    audio_files = []
    
    for file_info in files:
        file_format = file_info.get('format', '').upper()
        
        # Check if this is an audio file
        if any(fmt in file_format for fmt in ['MP3', 'FLAC', 'OGG', 'VORBIS']):
            # Skip derivative files (like 64kb versions)
            filename = file_info.get('name', '')
            if '64kb' not in filename.lower() and '_vbr' not in filename.lower():
                audio_files.append(file_info)
    
    # If format preference specified, filter
    if format_preference and audio_files:
        preferred = [f for f in audio_files 
                    if format_preference.upper() in f.get('format', '').upper()]
        if preferred:
            return preferred
    
    return audio_files


def parse_setlist(files: list) -> Dict[str, list]:
    """
    Parse files into sets (Set I, Set II, Encore).
    
    This is a simple implementation - the playlist module does this better.
    
    Args:
        files: List of audio file dictionaries
        
    Returns:
        Dictionary mapping set names to file lists
    """
    setlist = {
        'Set I': [],
        'Set II': [],
        'Encore': []
    }
    
    for file_info in files:
        filename = file_info.get('name', '').lower()
        
        if 'd1t' in filename or '_set1_' in filename:
            setlist['Set I'].append(file_info)
        elif 'd2t' in filename or '_set2_' in filename:
            setlist['Set II'].append(file_info)
        elif 'd3t' in filename or '_encore' in filename or '_e_' in filename:
            setlist['Encore'].append(file_info)
        else:
            # Default to Set I
            setlist['Set I'].append(file_info)
    
    return setlist


# Example usage
if __name__ == '__main__':
    # Test with Cornell '77
    identifier = 'gd77-05-08.sbd.hicks.4982.sbeok.shnf'
    
    print(f"Fetching metadata for {identifier}...")
    
    try:
        # Get metadata
        metadata = get_metadata(identifier)
        
        # Show basic info
        info = get_show_info(identifier)
        print(f"\nShow: {info.get('date')} - {info.get('venue')}")
        
        # Get audio files
        audio_files = extract_audio_files(metadata)
        print(f"Audio files: {len(audio_files)}")
        
        # Show first 3 files
        print("\nFirst 3 files:")
        for file_info in audio_files[:3]:
            print(f"  - {file_info['name']} ({file_info.get('format')})")
        
    except Exception as e:
        print(f"Error: {e}")
