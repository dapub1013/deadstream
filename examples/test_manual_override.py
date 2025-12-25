#!/usr/bin/env python3
"""
Test Suite for Task 5.5: Manual Override Functionality

Tests the RecordingSelector class which provides both automatic
and manual recording selection capabilities.

Run from project root:
    python examples/test_manual_override.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, '/home/david/deadstream')

from src.selection.override import RecordingSelector
from src.selection.scoring import RecordingScorer


def test_list_recordings():
    """Test listing all recordings for a show."""
    print("\n" + "="*70)
    print("[TEST 1] List Recordings for Cornell '77")
    print("="*70)
    
    selector = RecordingSelector()
    recordings = selector.list_recordings_for_show('1977-05-08')
    
    if recordings:
        print(f"[PASS] Found {len(recordings)} recording(s)")
        for i, rec in enumerate(recordings[:3], 1):  # Show first 3
            print(f"  {i}. {rec['identifier']}")
        if len(recordings) > 3:
            print(f"  ... and {len(recordings) - 3} more")
        return True
    else:
        print("[FAIL] No recordings found")
        return False


def test_automatic_selection():
    """Test automatic smart selection."""
    print("\n" + "="*70)
    print("[TEST 2] Automatic Selection")
    print("="*70)
    
    selector = RecordingSelector()
    auto_id = selector.select_automatically('1977-05-08')
    
    if auto_id:
        print(f"[PASS] Automatically selected: {auto_id}")
        return True
    else:
        print("[FAIL] Automatic selection returned None")
        return False


def test_manual_selection_valid():
    """Test manual selection with a valid identifier."""
    print("\n" + "="*70)
    print("[TEST 3] Manual Selection (Valid Identifier)")
    print("="*70)
    
    selector = RecordingSelector()
    
    # Get a valid identifier first
    recordings = selector.list_recordings_for_show('1977-05-08')
    if not recordings:
        print("[SKIP] No recordings available for testing")
        return None
    
    # Try to manually select the second recording (if available)
    test_id = recordings[1]['identifier'] if len(recordings) > 1 else recordings[0]['identifier']
    print(f"\nAttempting manual selection: {test_id}")
    
    result = selector.select_manually(test_id)
    
    if result == test_id:
        print(f"[PASS] Manual selection successful")
        return True
    else:
        print("[FAIL] Manual selection failed")
        return False


def test_manual_selection_invalid():
    """Test manual selection with an invalid identifier."""
    print("\n" + "="*70)
    print("[TEST 4] Manual Selection (Invalid Identifier)")
    print("="*70)
    
    selector = RecordingSelector()
    
    # Try with a fake identifier
    fake_id = "gd1977-05-08.fake.recording.notreal"
    print(f"\nAttempting manual selection: {fake_id}")
    
    result = selector.select_manually(fake_id)
    
    if result is None:
        print("[PASS] Correctly rejected invalid identifier")
        return True
    else:
        print("[FAIL] Should have rejected invalid identifier")
        return False


def test_select_with_override_auto():
    """Test select_with_override using automatic selection."""
    print("\n" + "="*70)
    print("[TEST 5] Select with Override (Auto Mode)")
    print("="*70)
    
    selector = RecordingSelector()
    result = selector.select_with_override('1977-05-08')
    
    if result:
        print(f"[PASS] Auto mode selected: {result}")
        return True
    else:
        print("[FAIL] Auto mode returned None")
        return False


def test_select_with_override_manual():
    """Test select_with_override using manual override."""
    print("\n" + "="*70)
    print("[TEST 6] Select with Override (Manual Mode)")
    print("="*70)
    
    selector = RecordingSelector()
    
    # Get a valid identifier
    recordings = selector.list_recordings_for_show('1977-05-08')
    if not recordings:
        print("[SKIP] No recordings available")
        return None
    
    manual_choice = recordings[0]['identifier']
    print(f"\nManual override to: {manual_choice}")
    
    result = selector.select_with_override('1977-05-08', manual_identifier=manual_choice)
    
    if result == manual_choice:
        print(f"[PASS] Manual override honored")
        return True
    else:
        print("[FAIL] Manual override not honored")
        return False


def test_display_recordings():
    """Test the display functionality."""
    print("\n" + "="*70)
    print("[TEST 7] Display Recordings (with scores)")
    print("="*70)
    
    selector = RecordingSelector()
    selector.display_recordings('1977-05-08', show_scores=True)
    
    print("\n[PASS] Display test complete")
    return True


def test_single_recording():
    """Test handling of shows with only one recording."""
    print("\n" + "="*70)
    print("[TEST 8] Single Recording Show")
    print("="*70)
    
    selector = RecordingSelector()
    
    # Find a show with only one recording
    # We'll use a less-popular show from the 1960s
    test_date = '1967-01-14'  # Early show, likely one recording
    
    recordings = selector.list_recordings_for_show(test_date)
    
    if len(recordings) == 1:
        result = selector.select_automatically(test_date)
        if result == recordings[0]['identifier']:
            print("[PASS] Single recording correctly returned")
            return True
        else:
            print("[FAIL] Single recording not returned correctly")
            return False
    elif len(recordings) == 0:
        print("[SKIP] No recordings found for test date")
        return None
    else:
        print(f"[SKIP] Test date has {len(recordings)} recordings (need 1)")
        return None


def main():
    """Run all tests."""
    
    print("\n" + "="*70)
    print("Task 5.5: Manual Override Test Suite")
    print("="*70)
    
    tests = [
        ("List Recordings", test_list_recordings),
        ("Automatic Selection", test_automatic_selection),
        ("Manual Selection (Valid)", test_manual_selection_valid),
        ("Manual Selection (Invalid)", test_manual_selection_invalid),
        ("Override - Auto Mode", test_select_with_override_auto),
        ("Override - Manual Mode", test_select_with_override_manual),
        ("Display Recordings", test_display_recordings),
        ("Single Recording", test_single_recording),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] Test '{test_name}' raised exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r is None)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result is True else "[SKIP]" if result is None else "[FAIL]"
        print(f"{status} {test_name}")
    
    print("\n" + "-"*70)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped ({total} total)")
    
    if failed == 0:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[FAILURE] {failed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
