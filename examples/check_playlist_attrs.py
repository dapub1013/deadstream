#!/usr/bin/env python3
"""Quick diagnostic to check Playlist attributes."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.audio.playlist import PlaylistBuilder
from src.api.metadata import get_metadata

# Build a playlist
identifier = "gd77-05-08.sbd.hicks.4982.sbeok.shnf"
metadata = get_metadata(identifier)

builder = PlaylistBuilder()
playlist = builder.build_from_metadata(metadata)

print("=== Playlist Attributes ===")
print(f"Type: {type(playlist)}")
print(f"\nAvailable attributes:")
for attr in dir(playlist):
    if not attr.startswith('_'):
        try:
            value = getattr(playlist, attr)
            if not callable(value):
                print(f"  {attr}: {value}")
        except:
            pass

print(f"\nAvailable methods:")
for attr in dir(playlist):
    if not attr.startswith('_'):
        value = getattr(playlist, attr)
        if callable(value):
            print(f"  {attr}()")

print(f"\nFirst track:")
if playlist.tracks:
    track = playlist.tracks[0]
    print(f"  Type: {type(track)}")
    for attr in dir(track):
        if not attr.startswith('_'):
            try:
                value = getattr(track, attr)
                if not callable(value):
                    print(f"  {attr}: {value}")
            except:
                pass
