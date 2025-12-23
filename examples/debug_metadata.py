#!/usr/bin/env python3
"""Debug script to examine Cornell '77 metadata structure"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.metadata import get_metadata
import json

identifier = 'gd77-05-08.sbd.hicks.4982.sbeok.shnf'

print("Fetching metadata...")
metadata = get_metadata(identifier)

print("\n" + "="*70)
print("METADATA STRUCTURE")
print("="*70)

# Show metadata section
print("\nMetadata section:")
print(json.dumps(metadata.get('metadata', {}), indent=2)[:500])

# Show first 3 audio files
print("\n\nFirst 3 audio files:")
mp3_files = [f for f in metadata.get('files', []) 
             if 'MP3' in f.get('format', '').upper() and '64kb' not in f.get('name', '')]

for i, f in enumerate(mp3_files[:3]):
    print(f"\nFile {i+1}:")
    print(f"  name: {f.get('name')}")
    print(f"  format: {f.get('format')}")
    print(f"  size: {f.get('size')}")
    print(f"  length: {f.get('length')} (type: {type(f.get('length'))})")
    print(f"  title: {f.get('title', 'N/A')}")
    print(f"  track: {f.get('track', 'N/A')}")
    print(f"  creator: {f.get('creator', 'N/A')}")

print("\n\nTotal MP3 files found:", len(mp3_files))
