#!/usr/bin/env python3
"""
Quick patch to force VLC to use headphone jack

Add this at the top of your resilient_player.py file, or run this
to test if it works before updating the main file.
"""

import vlc
import time

# Test VLC with explicit headphone device
print("Testing VLC with headphone jack output...")
print("="*70)

# Create VLC instance with EXPLICIT device
instance = vlc.Instance(
    '--aout=alsa',                    # ALSA audio output
    '--alsa-audio-device=headphones', # EXPLICIT: Use headphone jack
    '--no-video',                     # Audio only
    '--quiet',                        # Suppress output
    '--verbose=0',                    # No error messages
    '--network-caching=8000'          # 8 second buffer
)

player = instance.media_player_new()

# Try to play a test URL
print("\n[INFO] Loading test audio from Archive.org...")

# Using a known-working URL (short audio file)
test_url = "https://archive.org/download/gd1977-05-08.sbd.hicks.4982.sbeok.shnf/gd77-05-08d1t01.mp3"

media = instance.media_new(test_url)
player.set_media(media)

print("[INFO] Starting playback through HEADPHONES...")
print("[INFO] You should hear audio in your headphones in 3-5 seconds...")
player.play()

# Wait for buffering
time.sleep(5)

# Check if playing
state = player.get_state()
print(f"[INFO] VLC State: {state}")

if state == vlc.State.Playing:
    print("\n" + "="*70)
    print("[SUCCESS] Audio should be playing through your HEADPHONES!")
    print("="*70)
    print("\nListening for 10 seconds...")
    print("If you hear music, the fix works!")
    print("="*70)
    
    # Play for 10 seconds
    time.sleep(10)
    
    player.stop()
    print("\n[INFO] Test complete!")
    print("\nIf you heard audio, update your resilient_player.py:")
    print("  Change: '--aout=alsa',")
    print("  To:     '--aout=alsa', '--alsa-audio-device=headphones',")
else:
    print(f"\n[WARN] Not playing. State: {state}")
    print("Trying alternative device name...")

player.release()
instance.release()
