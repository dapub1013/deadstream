#!/usr/bin/env python3
"""
Test headphone output with dynamic URL from database
"""

import sys
import time

sys.path.insert(0, '/home/david/deadstream')

from examples.get_test_url import get_test_url
import vlc

print("Testing VLC with headphone jack output...")
print("="*70)

# Get a valid URL from database
print("\n[INFO] Getting test URL from database...")
test_url = get_test_url(verbose=False)

if not test_url:
    print("[ERROR] Could not get test URL from database")
    print("Make sure Phase 3 database is populated")
    sys.exit(1)

print(f"[INFO] Using URL: {test_url[:60]}...")

# Create VLC instance with EXPLICIT headphone device
print("\n[INFO] Creating VLC instance with headphone routing...")
instance = vlc.Instance(
    '--aout=alsa',                    # ALSA audio output
    '--alsa-audio-device=headphones', # EXPLICIT: Use headphone jack
    '--no-video',                     # Audio only
    '--quiet',                        # Suppress output
    '--verbose=0',                    # No error messages
    '--network-caching=8000'          # 8 second buffer
)

player = instance.media_player_new()

# Load and play
print("[INFO] Loading audio...")
media = instance.media_new(test_url)
player.set_media(media)

print("[INFO] Starting playback through HEADPHONES...")
print("[INFO] Buffering... (this takes a few seconds)")
player.play()

# Wait for buffering and initial playback
time.sleep(5)

# Check state
state = player.get_state()
position = player.get_time()
duration = player.get_length()

print(f"\n[INFO] VLC State: {state}")
print(f"[INFO] Position: {position}ms")
print(f"[INFO] Duration: {duration}ms")

if state == vlc.State.Playing or state == vlc.State.Buffering:
    print("\n" + "="*70)
    print("[SUCCESS] Audio is playing!")
    print("="*70)
    print("\nCHECK YOUR HEADPHONES - You should hear music!")
    print("If you hear Grateful Dead playing, the fix works!")
    print("\nPlaying for 15 seconds so you can verify...")
    print("="*70)
    
    # Play for 15 seconds with status updates
    for i in range(15):
        time.sleep(1)
        pos = player.get_time()
        print(f"Playing... {i+1}s (position: {pos}ms)", end='\r')
    
    print("\n\n[INFO] Stopping playback...")
    player.stop()
    
    print("\n" + "="*70)
    print("Did you hear audio in your headphones?")
    print("="*70)
    print("\nIf YES:")
    print("  Update src/audio/resilient_player.py")
    print("  Add: '--alsa-audio-device=headphones',")
    print("  Then all your tests will play through headphones!")
    print("\nIf NO:")
    print("  Your headphones might not be fully plugged in")
    print("  OR we need to try a different device name")
    print("="*70)
    
else:
    print(f"\n[WARN] Not playing. State: {state}")
    print("\nPossible issues:")
    print("1. Network connection problem")
    print("2. Archive.org temporarily unavailable")
    print("3. VLC audio configuration issue")
    print("\nTry running again in a moment...")

player.release()
instance.release()
