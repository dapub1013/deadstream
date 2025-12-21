#!/usr/bin/env python3
"""
Phase 2.1 - Quick Start Guide to Archive.org API

This script shows you the essential API patterns you need for DeadStream.
Run this to understand the structure, then use it as a template.
"""

import json

# ============================================================================
# PART 1: Understanding the Response Structure
# ============================================================================

print("="*70)
print(" PART 1: Understanding API Response Structure")
print("="*70)

# This is what the Search API actually returns
example_search_response = {
    "response": {
        "numFound": 12,  # Total matching shows
        "docs": [        # Array of show objects
            {
                "identifier": "gd77-05-08.sbd.hicks.4982.sbeok.shnf",
                "title": "Grateful Dead Live at Barton Hall, Cornell University on 1977-05-08",
                "date": "1977-05-08T00:00:00Z",
                "venue": "Barton Hall, Cornell University",
                "coverage": "Ithaca, NY",
                "avg_rating": 4.8,
                "source": "Soundboard"
            },
            {
                "identifier": "gd1977-05-08.sbd.miller.97065.sbeok.flac16",
                "title": "Grateful Dead Live at Barton Hall, Cornell University on 1977-05-08",
                "date": "1977-05-08T00:00:00Z",
                "venue": "Barton Hall, Cornell University",
                "coverage": "Ithaca, NY",
                "avg_rating": 4.7,
                "source": "Soundboard > Reel"
            }
        ]
    }
}

print("\n1. Search API Response Structure:")
print(f"   Total shows found: {example_search_response['response']['numFound']}")
print(f"   Number returned: {len(example_search_response['response']['docs'])}")
print("\n   First show:")
first_show = example_search_response['response']['docs'][0]
print(f"   - Identifier: {first_show['identifier']}")
print(f"   - Date: {first_show['date'][:10]}")  # Just the date part
print(f"   - Venue: {first_show['venue']}")
print(f"   - Rating: {first_show['avg_rating']}")

# This is what the Metadata API returns (simplified)
example_metadata_response = {
    "metadata": {
        "identifier": "gd77-05-08.sbd.hicks.4982.sbeok.shnf",
        "title": "Grateful Dead Live at Barton Hall, Cornell University on 1977-05-08",
        "date": "1977-05-08",
        "venue": "Barton Hall, Cornell University",
        "coverage": "Ithaca, NY",
        "source": "Soundboard",
        "taper": "Betty Cantor-Jackson",
        "avg_rating": "4.80",
        "description": "One of the most celebrated Grateful Dead concerts..."
    },
    "files": [
        {
            "name": "gd77-05-08d1t01.mp3",
            "format": "VBR MP3",
            "title": "New Minglewood Blues",
            "track": "01",
            "length": "221.45",
            "size": "5242880"
        },
        {
            "name": "gd77-05-08d1t02.mp3",
            "format": "VBR MP3",
            "title": "Loser",
            "track": "02",
            "length": "196.89",
            "size": "4718592"
        },
        {
            "name": "gd77-05-08d1t03.mp3",
            "format": "VBR MP3",
            "title": "El Paso",
            "track": "03",
            "length": "275.12",
            "size": "6553600"
        }
    ]
}

print("\n2. Metadata API Response Structure:")
print(f"   Show: {example_metadata_response['metadata']['title'][:50]}...")
print(f"   Source: {example_metadata_response['metadata']['source']}")
print(f"   Taper: {example_metadata_response['metadata']['taper']}")
print(f"   Number of files: {len(example_metadata_response['files'])}")
print("\n   First three tracks:")
for i, track in enumerate(example_metadata_response['files'][:3], 1):
    print(f"   {i}. {track['title']} ({track['length']} seconds)")

# ============================================================================
# PART 2: Essential Code Patterns
# ============================================================================

print("\n" + "="*70)
print(" PART 2: Essential Code Patterns for Your Project")
print("="*70)

print("""
# Pattern 1: Search for shows
# ---------------------------
import requests

def search_shows(query):
    url = "https://archive.org/advancedsearch.php"
    params = {
        'q': f'collection:GratefulDead AND {query}',
        'fl': 'identifier,title,date,venue,avg_rating',
        'rows': 100,
        'output': 'json',
        'sort': 'date asc'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return data['response']['docs']

# Examples:
# shows = search_shows('date:1977-05-08')
# shows = search_shows('year:1977')
# shows = search_shows('venue:*Cornell*')


# Pattern 2: Get show metadata
# ---------------------------
def get_metadata(identifier):
    url = f"https://archive.org/metadata/{identifier}"
    response = requests.get(url)
    return response.json()

# Example:
# metadata = get_metadata('gd77-05-08.sbd.hicks.4982.sbeok.shnf')


# Pattern 3: Extract playable tracks
# ----------------------------------
def get_tracks(metadata):
    identifier = metadata['metadata']['identifier']
    files = metadata['files']
    
    # Get MP3 files only
    mp3s = [f for f in files if f.get('format') == 'VBR MP3']
    mp3s.sort(key=lambda x: x.get('name', ''))
    
    tracks = []
    for f in mp3s:
        url = f"https://archive.org/download/{identifier}/{f['name']}"
        tracks.append({
            'url': url,
            'title': f.get('title', 'Unknown'),
            'duration': float(f.get('length', 0))
        })
    
    return tracks

# Example:
# tracks = get_tracks(metadata)
# for track in tracks:
#     print(track['title'], track['url'])


# Pattern 4: Pick best recording
# ------------------------------
def pick_best(shows):
    # Prefer soundboards
    sbd = [s for s in shows if 'sbd' in s['identifier'].lower()]
    if sbd:
        # Return highest rated soundboard
        return max(sbd, key=lambda x: x.get('avg_rating', 0))
    
    # Otherwise return highest rated
    return max(shows, key=lambda x: x.get('avg_rating', 0))

# Example:
# shows = search_shows('date:1977-05-08')
# best = pick_best(shows)
""")

# ============================================================================
# PART 3: Practical Example (Works Offline)
# ============================================================================

print("\n" + "="*70)
print(" PART 3: Practical Example - Processing Metadata")
print("="*70)

print("\nLet's process the example metadata from Cornell '77:\n")

def extract_setlist(metadata):
    """Extract setlist organized by set"""
    files = metadata['files']
    mp3s = [f for f in files if f.get('format') == 'VBR MP3']
    mp3s.sort(key=lambda x: x.get('name', ''))
    
    setlist = {'Set I': [], 'Set II': [], 'Encore': []}
    
    for f in mp3s:
        name = f['name']
        title = f.get('title', 'Unknown')
        
        # Determine set based on filename
        if 'd1t' in name:
            setlist['Set I'].append(title)
        elif 'd2t' in name:
            setlist['Set II'].append(title)
        elif 'd3t' in name:
            setlist['Encore'].append(title)
    
    return setlist

def format_duration(seconds):
    """Convert seconds to MM:SS format"""
    mins = int(float(seconds) // 60)
    secs = int(float(seconds) % 60)
    return f"{mins}:{secs:02d}"

# Process the example data
setlist = extract_setlist(example_metadata_response)

for set_name, songs in setlist.items():
    if songs:
        print(f"{set_name}:")
        for i, song in enumerate(songs, 1):
            print(f"  {i}. {song}")
        print()

print("Total runtime calculation:")
total_seconds = sum(float(f['length']) for f in example_metadata_response['files'])
print(f"Total show length: {format_duration(total_seconds)}")

# ============================================================================
# PART 4: Ready-to-Use Template
# ============================================================================

print("\n" + "="*70)
print(" PART 4: Template for Your Code")
print("="*70)

template = '''
# Save this as: src/api/archive_client.py

import requests
from typing import List, Dict, Optional

class ArchiveClient:
    """Client for Internet Archive Grateful Dead collection"""
    
    BASE_SEARCH_URL = "https://archive.org/advancedsearch.php"
    BASE_METADATA_URL = "https://archive.org/metadata"
    BASE_DOWNLOAD_URL = "https://archive.org/download"
    
    def search_shows(self, query: str, max_results: int = 100) -> List[Dict]:
        """Search for shows matching query"""
        params = {
            'q': f'collection:GratefulDead AND {query}',
            'fl': 'identifier,title,date,venue,coverage,avg_rating,source',
            'rows': max_results,
            'output': 'json',
            'sort': 'date asc'
        }
        
        response = requests.get(self.BASE_SEARCH_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return data['response']['docs']
    
    def get_metadata(self, identifier: str) -> Dict:
        """Get full metadata for a show"""
        url = f"{self.BASE_METADATA_URL}/{identifier}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        return response.json()
    
    def get_streaming_urls(self, identifier: str) -> List[Dict]:
        """Get streaming URLs for all tracks in a show"""
        metadata = self.get_metadata(identifier)
        files = metadata.get('files', [])
        
        # Get MP3 files only
        mp3_files = [f for f in files if f.get('format') == 'VBR MP3']
        mp3_files.sort(key=lambda x: x.get('name', ''))
        
        tracks = []
        for f in mp3_files:
            url = f"{self.BASE_DOWNLOAD_URL}/{identifier}/{f['name']}"
            tracks.append({
                'url': url,
                'title': f.get('title', 'Unknown'),
                'track': f.get('track', '?'),
                'duration': float(f.get('length', 0)),
                'set': self._determine_set(f['name'])
            })
        
        return tracks
    
    def _determine_set(self, filename: str) -> str:
        """Determine which set a track belongs to"""
        if 'd1t' in filename:
            return 'Set I'
        elif 'd2t' in filename:
            return 'Set II'
        elif 'd3t' in filename:
            return 'Encore'
        return 'Unknown'
    
    def find_best_recording(self, date: str) -> Optional[Dict]:
        """Find the best recording for a specific date"""
        shows = self.search_shows(f'date:{date}')
        
        if not shows:
            return None
        
        # Prefer soundboards
        soundboards = [s for s in shows 
                      if 'sbd' in s.get('identifier', '').lower()]
        
        if soundboards:
            return max(soundboards, key=lambda x: x.get('avg_rating', 0))
        
        return max(shows, key=lambda x: x.get('avg_rating', 0))

# Usage example:
# client = ArchiveClient()
# shows = client.search_shows('year:1977')
# best = client.find_best_recording('1977-05-08')
# tracks = client.get_streaming_urls(best['identifier'])
'''

print("\nTemplate saved above - copy this to start building your API module!")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print(" SUMMARY: What You Learned")
print("="*70)

print("""
1. THREE MAIN APIS:
   - Search: Find shows by date/venue/year
   - Metadata: Get full details for a specific show
   - Streaming: Direct URLs to audio files

2. ESSENTIAL PATTERNS:
   - Search → Get list of shows
   - Pick best → Choose highest rated/soundboard
   - Get metadata → Get full show details
   - Extract tracks → Build playlist

3. RESPONSE STRUCTURE:
   - Search: {response: {docs: [...]}}
   - Metadata: {metadata: {...}, files: [...]}
   - Tracks: Build URLs from identifier + filename

4. NEXT STEPS:
   - Copy the ArchiveClient template
   - Test it with real API calls (when network available)
   - Add error handling
   - Add caching

REFERENCE DOCUMENT:
   See archive_api_reference.md for complete API documentation

When you're ready to test with real API calls, run this:
   python3 api_basics.py

Happy coding!
""")
