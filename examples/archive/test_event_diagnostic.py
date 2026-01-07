#!/usr/bin/env python3
"""
Diagnostic: Test VLC event firing in different scenarios

This helps us understand when/how MediaPlayerEndReached fires.
"""

import sys
import os
import time
import threading

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.audio.resilient_player import ResilientPlayer
from src.database.queries import get_show_by_date, get_top_rated_shows
from src.api.metadata import get_metadata, extract_audio_files


def get_test_url():
    """Get a test URL from database"""
    shows = get_show_by_date('1977-05-08')
    if not shows:
        shows = get_top_rated_shows(limit=1, min_reviews=5)
    
    if not shows:
        return None
    
    show = shows[0]
    metadata = get_metadata(show['identifier'])
    audio_files = extract_audio_files(metadata)
    
    if not audio_files:
        return None
    
    return f"https://archive.org/download/{show['identifier']}/{audio_files[0]['name']}"


def test_scenario_1():
    """Scenario 1: Let track play to natural end"""
    print("\n" + "="*70)
    print("SCENARIO 1: Natural playback to end (will take several minutes)")
    print("="*70)
    
    event_fired = [False]
    
    def callback():
        print("\n[CALLBACK] Track ended callback was called!")
        event_fired[0] = True
    
    player = ResilientPlayer()
    player.on_track_ended = callback
    
    url = get_test_url()
    if not url:
        print("[ERROR] Could not get test URL")
        return False
    
    print(f"[INFO] URL: {url}")
    player.load_url(url)
    player.play()
    
    print("[INFO] Playing track naturally to completion...")
    print("[INFO] This will take the full track duration")
    print("[INFO] Press Ctrl+C to skip to Scenario 2")
    
    try:
        # Monitor playback
        while True:
            pos = player.get_position() / 1000.0
            dur = player.get_duration() / 1000.0
            state = player.get_state()
            
            print(f"\r[INFO] {pos:.1f}s / {dur:.1f}s | State: {state} | Event: {event_fired[0]}", end='', flush=True)
            
            if event_fired[0]:
                print("\n[PASS] Event fired!")
                break
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Skipped")
    
    player.cleanup()
    return event_fired[0]


def test_scenario_2():
    """Scenario 2: Seek near end and wait"""
    print("\n" + "="*70)
    print("SCENARIO 2: Seek to near end, then wait for natural completion")
    print("="*70)
    
    event_fired = [False]
    
    def callback():
        print("\n[CALLBACK] Track ended callback was called!")
        event_fired[0] = True
    
    player = ResilientPlayer()
    player.on_track_ended = callback
    
    url = get_test_url()
    if not url:
        print("[ERROR] Could not get test URL")
        return False
    
    print(f"[INFO] URL: {url}")
    player.load_url(url)
    player.play()
    
    # Wait for playback to start
    print("[INFO] Waiting for playback to start...")
    time.sleep(3)
    
    # Get duration and seek near end
    duration = player.get_duration()
    if duration > 10000:  # More than 10 seconds
        seek_pos = duration - 5000  # 5 seconds before end
        print(f"[INFO] Duration: {duration/1000.0:.1f}s")
        print(f"[INFO] Seeking to {seek_pos/1000.0:.1f}s (5s before end)...")
        player.seek(seek_pos)
        time.sleep(1)
    
    # Monitor until end
    print("[INFO] Waiting for track to end naturally...")
    timeout = 30
    start = time.time()
    
    while time.time() - start < timeout:
        pos = player.get_position() / 1000.0
        dur = player.get_duration() / 1000.0
        state = player.get_state()
        
        print(f"\r[INFO] {pos:.1f}s / {dur:.1f}s | State: {state} | Event: {event_fired[0]}", end='', flush=True)
        
        if event_fired[0]:
            print("\n[PASS] Event fired!")
            break
        
        time.sleep(0.5)
    
    if not event_fired[0]:
        print("\n[FAIL] Event did not fire")
    
    player.cleanup()
    return event_fired[0]


def test_scenario_3():
    """Scenario 3: Check if event fires with player.stop()"""
    print("\n" + "="*70)
    print("SCENARIO 3: Call player.stop() manually (should NOT fire event)")
    print("="*70)
    
    event_fired = [False]
    
    def callback():
        print("\n[CALLBACK] Track ended callback was called!")
        event_fired[0] = True
    
    player = ResilientPlayer()
    player.on_track_ended = callback
    
    url = get_test_url()
    if not url:
        print("[ERROR] Could not get test URL")
        return False
    
    print(f"[INFO] URL: {url}")
    player.load_url(url)
    player.play()
    
    print("[INFO] Playing for 3 seconds, then stopping...")
    time.sleep(3)
    
    player.stop()
    
    time.sleep(1)
    
    if event_fired[0]:
        print("[WARN] Event fired on manual stop - unexpected!")
    else:
        print("[PASS] Event did not fire on manual stop - correct!")
    
    player.cleanup()
    return not event_fired[0]  # Success = event did NOT fire


if __name__ == '__main__':
    print("\n" + "="*70)
    print("VLC MediaPlayerEndReached EVENT DIAGNOSTIC")
    print("="*70)
    print("\nThis will test 3 scenarios to understand event behavior:")
    print("1. Natural playback to end (long)")
    print("2. Seek near end, then wait")
    print("3. Manual stop (should not trigger)")
    print("\n" + "="*70)
    
    # Test scenario 2 (quickest to test)
    result2 = test_scenario_2()
    
    if result2:
        print("\n" + "="*70)
        print("DIAGNOSIS: Event system is working!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("DIAGNOSIS: Event is NOT firing")
        print("Possible issues:")
        print("1. VLC event manager not properly initialized")
        print("2. Python VLC bindings version issue")
        print("3. Event callback signature incorrect")
        print("="*70)
        
        # Try scenario 3 as well
        test_scenario_3()
