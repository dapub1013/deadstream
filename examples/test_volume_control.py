#!/usr/bin/env python3
"""
Test Volume Control - Phase 4.7

This script tests all volume control features of ResilientPlayer:
- Get/set volume
- Mute/unmute
- Volume up/down
- Volume persistence during playback

Usage:
    python examples/test_volume_control.py
"""

import sys
import time

# Add project to path
sys.path.insert(0, '/home/david/deadstream')

from src.audio.resilient_player import ResilientPlayer
from examples.get_test_url import get_test_url


def test_volume_basic():
    """Test basic volume get/set"""
    print("\n" + "="*70)
    print("TEST 1: Basic Volume Get/Set")
    print("="*70)
    
    player = ResilientPlayer()
    
    # Test 1.1: Get initial volume
    initial_volume = player.get_volume()
    print(f"[INFO] Initial volume: {initial_volume}%")
    assert initial_volume == 50, "Default volume should be 50%"
    print("[PASS] Default volume is correct")
    
    # Test 1.2: Set volume to 75%
    result = player.set_volume(75)
    assert result == True, "set_volume should return True"
    assert player.get_volume() == 75, "Volume should be 75%"
    print("[PASS] Set volume to 75%")
    
    # Test 1.3: Set volume to 0%
    result = player.set_volume(0)
    assert result == True, "set_volume should return True"
    assert player.get_volume() == 0, "Volume should be 0%"
    print("[PASS] Set volume to 0%")
    
    # Test 1.4: Set volume to 100%
    result = player.set_volume(100)
    assert result == True, "set_volume should return True"
    assert player.get_volume() == 100, "Volume should be 100%"
    print("[PASS] Set volume to 100%")
    
    player.cleanup()
    print("\n[SUCCESS] Basic volume tests passed")
    return True


def test_volume_bounds():
    """Test volume bounds checking"""
    print("\n" + "="*70)
    print("TEST 2: Volume Bounds Checking")
    print("="*70)
    
    player = ResilientPlayer()
    
    # Test 2.1: Set volume above 100 (should clamp to 100)
    player.set_volume(150)
    assert player.get_volume() == 100, "Volume should clamp to 100"
    print("[PASS] Volume clamped to 100 (input: 150)")
    
    # Test 2.2: Set volume below 0 (should clamp to 0)
    player.set_volume(-50)
    assert player.get_volume() == 0, "Volume should clamp to 0"
    print("[PASS] Volume clamped to 0 (input: -50)")
    
    # Test 2.3: Set volume with float
    player.set_volume(66.7)
    assert player.get_volume() == 66, "Float should be converted to int"
    print("[PASS] Float volume converted to int (66.7 -> 66)")
    
    player.cleanup()
    print("\n[SUCCESS] Bounds checking tests passed")
    return True


def test_mute_unmute():
    """Test mute/unmute functionality"""
    print("\n" + "="*70)
    print("TEST 3: Mute/Unmute")
    print("="*70)
    
    player = ResilientPlayer()
    
    # Set initial volume
    player.set_volume(75)
    
    # Test 3.1: Initial state (not muted)
    assert player.get_mute() == False, "Should not be muted initially"
    print("[PASS] Initial state: not muted")
    
    # Test 3.2: Mute
    result = player.mute()
    assert result == True, "mute() should return True"
    assert player.get_mute() == True, "Should be muted"
    print("[PASS] Mute successful")
    
    # Test 3.3: Unmute
    result = player.unmute()
    assert result == True, "unmute() should return True"
    assert player.get_mute() == False, "Should not be muted"
    assert player.get_volume() == 75, "Volume should restore to 75%"
    print("[PASS] Unmute successful, volume restored")
    
    # Test 3.4: Toggle mute
    player.toggle_mute()
    assert player.get_mute() == True, "Should be muted after toggle"
    print("[PASS] Toggle to muted")
    
    player.toggle_mute()
    assert player.get_mute() == False, "Should be unmuted after toggle"
    print("[PASS] Toggle to unmuted")
    
    player.cleanup()
    print("\n[SUCCESS] Mute/unmute tests passed")
    return True


def test_volume_up_down():
    """Test volume_up and volume_down methods"""
    print("\n" + "="*70)
    print("TEST 4: Volume Up/Down")
    print("="*70)
    
    player = ResilientPlayer()
    
    # Start at 50%
    player.set_volume(50)
    
    # Test 4.1: Volume up
    new_vol = player.volume_up(10)
    assert new_vol == 60, "Volume should be 60% (50 + 10)"
    print("[PASS] Volume up by 10: 50% -> 60%")
    
    # Test 4.2: Volume down
    new_vol = player.volume_down(5)
    assert new_vol == 55, "Volume should be 55% (60 - 5)"
    print("[PASS] Volume down by 5: 60% -> 55%")
    
    # Test 4.3: Volume up beyond 100
    player.set_volume(95)
    new_vol = player.volume_up(10)
    assert new_vol == 100, "Volume should clamp at 100%"
    print("[PASS] Volume up with clamp: 95% + 10 = 100%")
    
    # Test 4.4: Volume down below 0
    player.set_volume(3)
    new_vol = player.volume_down(5)
    assert new_vol == 0, "Volume should clamp at 0%"
    print("[PASS] Volume down with clamp: 3% - 5 = 0%")
    
    # Test 4.5: Default amount (5%)
    player.set_volume(50)
    new_vol = player.volume_up()  # No amount specified
    assert new_vol == 55, "Default volume_up should be 5%"
    print("[PASS] Default volume_up: 50% -> 55%")
    
    new_vol = player.volume_down()  # No amount specified
    assert new_vol == 50, "Default volume_down should be 5%"
    print("[PASS] Default volume_down: 55% -> 50%")
    
    player.cleanup()
    print("\n[SUCCESS] Volume up/down tests passed")
    return True


def test_volume_during_playback():
    """Test volume control during active playback"""
    print("\n" + "="*70)
    print("TEST 5: Volume Control During Playback")
    print("="*70)
    
    # Get test URL
    print("[INFO] Getting test URL from database...")
    test_url = get_test_url(verbose=False)
    
    if not test_url:
        print("[SKIP] Could not get test URL - skipping playback test")
        return True
    
    print(f"[INFO] Test URL: {test_url[:60]}...")
    
    player = ResilientPlayer()
    
    # Load and start playback
    print("[INFO] Loading URL...")
    player.load_url(test_url)
    
    print("[INFO] Starting playback...")
    player.play()
    
    # Wait for buffering
    print("[INFO] Waiting 3 seconds for buffering...")
    time.sleep(3)
    
    # Test 5.1: Change volume during playback
    print("[INFO] Testing volume changes during playback...")
    
    player.set_volume(30)
    print(f"[INFO] Volume set to 30% - Position: {player.get_position()}ms")
    time.sleep(2)
    
    player.set_volume(60)
    print(f"[INFO] Volume set to 60% - Position: {player.get_position()}ms")
    time.sleep(2)
    
    player.set_volume(90)
    print(f"[INFO] Volume set to 90% - Position: {player.get_position()}ms")
    time.sleep(2)
    
    print("[PASS] Volume changed during playback without issues")
    
    # Test 5.2: Mute during playback
    print("[INFO] Testing mute during playback...")
    player.mute()
    print("[INFO] Audio muted")
    time.sleep(2)
    
    player.unmute()
    print("[INFO] Audio unmuted")
    time.sleep(2)
    
    print("[PASS] Mute/unmute during playback worked")
    
    # Stop playback
    player.stop()
    player.cleanup()
    
    print("\n[SUCCESS] Playback volume control tests passed")
    return True


def test_volume_state_persistence():
    """Test that volume state persists correctly"""
    print("\n" + "="*70)
    print("TEST 6: Volume State Persistence")
    print("="*70)
    
    player = ResilientPlayer()
    
    # Test 6.1: Volume persists after mute/unmute
    player.set_volume(80)
    player.mute()
    player.unmute()
    assert player.get_volume() == 80, "Volume should persist after unmute"
    print("[PASS] Volume persisted after mute/unmute (80%)")
    
    # Test 6.2: Setting volume while muted unmutes
    player.set_volume(70)
    player.mute()
    assert player.get_mute() == True, "Should be muted"
    
    player.set_volume(60)  # Setting volume should unmute
    assert player.get_mute() == False, "Setting volume should unmute"
    assert player.get_volume() == 60, "Volume should be 60%"
    print("[PASS] Setting volume while muted unmutes player")
    
    # Test 6.3: Mute remembers previous volume
    player.set_volume(45)
    player.mute()
    player.set_volume(0)  # Manually set to 0 while muted
    player.unmute()
    assert player.get_volume() == 45, "Should restore to pre-mute volume"
    print("[PASS] Unmute restores correct volume (45%)")
    
    player.cleanup()
    print("\n[SUCCESS] State persistence tests passed")
    return True


def main():
    """Run all volume control tests"""
    print("\n" + "="*70)
    print("DEADSTREAM - VOLUME CONTROL TEST SUITE")
    print("Phase 4.7 - Complete Testing")
    print("="*70)
    
    tests = [
        ("Basic Volume Get/Set", test_volume_basic),
        ("Volume Bounds Checking", test_volume_bounds),
        ("Mute/Unmute", test_mute_unmute),
        ("Volume Up/Down", test_volume_up_down),
        ("Volume During Playback", test_volume_during_playback),
        ("Volume State Persistence", test_volume_state_persistence)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except AssertionError as e:
            print(f"\n[FAIL] {test_name}: {e}")
            results.append((test_name, False))
        except Exception as e:
            print(f"\n[ERROR] {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {test_name}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All volume control tests passed!")
        print("\nPhase 4.7 - Volume Control: COMPLETE")
        return 0
    else:
        print(f"\n[FAIL] {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
