#!/usr/bin/env python3
"""
Diagnostic test for findashow -> player flow
Traces exactly what happens when a date is selected
"""

import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Test database query first
print("=" * 70)
print("STEP 1: Testing database query")
print("=" * 70)

from src.database.queries import get_show_by_date

date_str = '1977-05-08'
print(f"Querying shows for {date_str}...")
shows = get_show_by_date(date_str)

if shows:
    print(f"[PASS] Found {len(shows)} show(s)")
    for i, show in enumerate(shows):
        print(f"  Show {i+1}:")
        print(f"    identifier: {show.get('identifier')}")
        print(f"    venue: {show.get('venue')}")
        print(f"    date: {show.get('date')}")
else:
    print(f"[FAIL] No shows found for {date_str}")
    sys.exit(1)

# Test metadata fetch
print("\n" + "=" * 70)
print("STEP 2: Testing metadata fetch")
print("=" * 70)

from src.api.metadata import get_metadata, extract_audio_files

show = shows[0]
identifier = show.get('identifier')
print(f"Fetching metadata for: {identifier}")

try:
    metadata = get_metadata(identifier)
    print(f"[PASS] Metadata fetched successfully")
    print(f"  Has 'metadata' key: {'metadata' in metadata}")
    print(f"  Has 'files' key: {'files' in metadata}")

    if 'files' in metadata:
        print(f"  Number of files: {len(metadata['files'])}")
except Exception as e:
    print(f"[FAIL] Failed to fetch metadata: {e}")
    sys.exit(1)

# Test audio file extraction
print("\n" + "=" * 70)
print("STEP 3: Testing audio file extraction")
print("=" * 70)

try:
    audio_files = extract_audio_files(metadata)
    print(f"[PASS] Extracted {len(audio_files)} audio files")

    if audio_files:
        print(f"\nFirst 3 tracks:")
        for i, track in enumerate(audio_files[:3]):
            print(f"  Track {i+1}:")
            print(f"    name: {track.get('name')}")
            print(f"    title: {track.get('title', 'N/A')}")
            print(f"    format: {track.get('format')}")
            print(f"    length: {track.get('length', 'N/A')}")
    else:
        print(f"[FAIL] No audio files found in metadata")
        sys.exit(1)

except Exception as e:
    print(f"[FAIL] Failed to extract audio files: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test player screen load_show method
print("\n" + "=" * 70)
print("STEP 4: Testing PlayerScreen.load_show()")
print("=" * 70)

from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)

from src.ui.screens.player_screen import PlayerScreen

player_screen = PlayerScreen()
print("PlayerScreen created")

print(f"\nBefore load_show:")
print(f"  current_show: {player_screen.current_show}")
print(f"  playlist length: {len(player_screen.playlist) if hasattr(player_screen, 'playlist') else 'N/A'}")
print(f"  total_tracks: {player_screen.total_tracks}")

print(f"\nCalling load_show()...")
player_screen.load_show(show)

print(f"\nAfter load_show:")
print(f"  current_show: {player_screen.current_show}")
print(f"  playlist length: {len(player_screen.playlist) if hasattr(player_screen, 'playlist') else 'N/A'}")
print(f"  current_track_index: {player_screen.current_track_index}")
print(f"  total_tracks: {player_screen.total_tracks}")
print(f"  song_title: {player_screen.song_title_label.text()}")
print(f"  track_counter: {player_screen.track_counter_label.text()}")

# Verify success
print("\n" + "=" * 70)
print("RESULTS:")
print("=" * 70)

success = True

if player_screen.current_show is None:
    print("[FAIL] current_show is None")
    success = False
else:
    print("[PASS] current_show is set")

if not hasattr(player_screen, 'playlist') or len(player_screen.playlist) == 0:
    print("[FAIL] playlist is empty")
    success = False
else:
    print(f"[PASS] playlist has {len(player_screen.playlist)} tracks")

if player_screen.total_tracks == 0:
    print("[FAIL] total_tracks is 0")
    success = False
else:
    print(f"[PASS] total_tracks = {player_screen.total_tracks}")

if player_screen.song_title_label.text() == "Song Title":
    print("[FAIL] song title not updated from default")
    success = False
else:
    print(f"[PASS] song title updated: {player_screen.song_title_label.text()}")

if success:
    print("\n[SUCCESS] load_show() works correctly!")
    sys.exit(0)
else:
    print("\n[FAIL] load_show() has issues")
    sys.exit(1)
