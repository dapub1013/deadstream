#!/usr/bin/env python3
"""
Phase 2.1 - Internet Archive API Basics
Working examples of the three main API endpoints

Run this to understand how the API works!
"""

import requests
import json
from datetime import datetime

# Suppress SSL warnings for now (we'll fix this later)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_section(title):
    """Pretty print section headers"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

# ============================================================================
# EXAMPLE 1: Advanced Search API - Find Shows
# ============================================================================

def search_shows(query, fields='identifier,title,date,venue', max_results=5):
    """
    Search the Grateful Dead collection
    
    Args:
        query: Search query (e.g., "date:1977-05-08" or "year:1977")
        fields: Comma-separated list of fields to return
        max_results: Number of results to return (max 10000)
    
    Returns:
        List of show dictionaries
    """
    print_section(f"EXAMPLE 1: Searching for shows - {query}")
    
    url = "https://archive.org/advancedsearch.php"
    params = {
        'q': f'collection:GratefulDead AND {query}',
        'fl': fields,
        'rows': max_results,
        'output': 'json',
        'sort': 'date asc'
    }
    
    print(f"\nAPI URL: {url}")
    print(f"Query: {params['q']}")
    print(f"Fields: {params['fl']}")
    print(f"\nSending request...")
    
    try:
        response = requests.get(url, params=params, timeout=10, verify=False)
        response.raise_for_status()  # Raise error for bad status codes
        
        data = response.json()
        shows = data['response']['docs']
        total = data['response']['numFound']
        
        print(f"\nSUCCESS! Found {total} shows total")
        print(f"Returning first {len(shows)} results:\n")
        
        for i, show in enumerate(shows, 1):
            print(f"{i}. {show.get('date', 'Unknown date')}")
            print(f"   Identifier: {show.get('identifier', 'N/A')}")
            print(f"   Title: {show.get('title', 'N/A')}")
            print(f"   Venue: {show.get('venue', 'N/A')}")
            print()
        
        return shows
        
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out")
        return []
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON - {e}")
        return []

# ============================================================================
# EXAMPLE 2: Metadata API - Get Show Details
# ============================================================================

def get_show_metadata(identifier):
    """
    Get complete metadata for a specific show
    
    Args:
        identifier: Archive.org identifier (e.g., "gd77-05-08.sbd.hicks.4982.sbeok.shnf")
    
    Returns:
        Dictionary with full metadata
    """
    print_section(f"EXAMPLE 2: Getting metadata for {identifier}")
    
    url = f"https://archive.org/metadata/{identifier}"
    
    print(f"\nAPI URL: {url}")
    print(f"\nSending request...")
    
    try:
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        
        metadata = response.json()
        
        print(f"\nSUCCESS! Retrieved metadata")
        print(f"\n--- Basic Info ---")
        print(f"Title: {metadata.get('metadata', {}).get('title', 'N/A')}")
        print(f"Date: {metadata.get('metadata', {}).get('date', 'N/A')}")
        print(f"Venue: {metadata.get('metadata', {}).get('venue', 'N/A')}")
        print(f"Source: {metadata.get('metadata', {}).get('source', 'N/A')}")
        print(f"Taper: {metadata.get('metadata', {}).get('taper', 'N/A')}")
        
        # Show available audio files
        files = metadata.get('files', [])
        audio_files = [f for f in files if f.get('format') in ['VBR MP3', 'Ogg Vorbis', 'Flac']]
        
        print(f"\n--- Available Audio Files ({len(audio_files)} total) ---")
        for i, f in enumerate(audio_files[:5], 1):  # Show first 5
            print(f"{i}. {f.get('name', 'Unknown')}")
            print(f"   Format: {f.get('format', 'N/A')}")
            print(f"   Size: {f.get('size', 'N/A')} bytes")
        
        if len(audio_files) > 5:
            print(f"   ... and {len(audio_files) - 5} more files")
        
        return metadata
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON - {e}")
        return {}

# ============================================================================
# EXAMPLE 3: Direct Streaming URL
# ============================================================================

def get_streaming_url(identifier, filename):
    """
    Construct the direct streaming URL for an audio file
    
    Args:
        identifier: Archive.org identifier
        filename: Name of the audio file (from metadata)
    
    Returns:
        Streaming URL string
    """
    print_section("EXAMPLE 3: Building streaming URL")
    
    url = f"https://archive.org/download/{identifier}/{filename}"
    
    print(f"\nStreaming URL:")
    print(url)
    print("\nThis URL can be:")
    print("  - Streamed directly with VLC")
    print("  - Downloaded with wget/curl")
    print("  - Played in a web browser")
    
    return url

# ============================================================================
# EXAMPLE 4: Practical Search Queries
# ============================================================================

def demo_search_queries():
    """Demonstrate various useful search queries"""
    print_section("EXAMPLE 4: Common Search Patterns")
    
    print("\n1. Search by specific date:")
    print("   Query: date:1977-05-08")
    search_shows("date:1977-05-08", max_results=3)
    
    print("\n2. Search by year:")
    print("   Query: year:1977")
    shows = search_shows("year:1977", max_results=3)
    
    print("\n3. Search by venue (partial match):")
    print("   Query: venue:*Fillmore*")
    search_shows("venue:*Fillmore*", max_results=3)
    
    print("\nOther useful queries you can try:")
    print("  - date:[1977-01-01 TO 1977-12-31]  (date range)")
    print("  - source:*soundboard*               (only soundboards)")
    print("  - identifier:*sbd*                  (identifiers with 'sbd')")
    print("  - venue:*Winterland*                (specific venue)")

# ============================================================================
# MAIN DEMO
# ============================================================================

def main():
    """Run all examples"""
    print("\n" + "="*70)
    print(" Internet Archive API - Live Demo")
    print(" DeadStream Project - Phase 2.1")
    print("="*70)
    print("\nThis script demonstrates the three main API endpoints:")
    print("  1. Advanced Search - Find shows")
    print("  2. Metadata API - Get show details")
    print("  3. Streaming URLs - Play audio")
    print("\nPress Enter to continue...")
    input()
    
    # Example 1: Search for Cornell '77
    shows = search_shows("date:1977-05-08", max_results=3)
    
    if shows:
        print("\nPress Enter to get metadata for the first show...")
        input()
        
        # Example 2: Get metadata for first show found
        identifier = shows[0]['identifier']
        metadata = get_show_metadata(identifier)
        
        if metadata:
            print("\nPress Enter to see streaming URL example...")
            input()
            
            # Example 3: Build streaming URL
            files = metadata.get('files', [])
            audio_files = [f for f in files if f.get('format') == 'VBR MP3']
            
            if audio_files:
                filename = audio_files[0]['name']
                url = get_streaming_url(identifier, filename)
            else:
                print("No MP3 files found for this show")
    
    print("\nPress Enter to see common search patterns...")
    input()
    
    # Example 4: Show various search queries
    demo_search_queries()
    
    print_section("Demo Complete!")
    print("\nKey Takeaways:")
    print("  1. Search API finds shows by date, venue, year, etc.")
    print("  2. Metadata API gives full details for a specific show")
    print("  3. Streaming URLs follow a simple pattern")
    print("  4. No authentication required for read-only access")
    print("\nNext steps:")
    print("  - Try modifying the search queries above")
    print("  - Experiment with different date ranges")
    print("  - Look at the JSON structure in detail")
    print("="*70)

if __name__ == "__main__":
    main()
