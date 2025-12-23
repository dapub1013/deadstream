#!/usr/bin/env python3
"""
Test Script for Position Tracking (Task 4.5)

This script tests all aspects of the position tracking functionality
without requiring actual audio playback.

Run this to verify your implementation is correct before integrating
with your actual audio player.

Author: DeadStream Project
Phase: 4.5 - Track Playback Position Tests
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.audio.position_tracker import PlaybackPosition, PositionTracker


def test_playback_position():
    """Test PlaybackPosition class calculations"""
    
    print("=" * 70)
    print("TEST 1: PlaybackPosition Class")
    print("=" * 70)
    
    # Test 1: Normal playback position
    print("\n1.1 Normal Position (3:35 / 11:22)")
    pos = PlaybackPosition(215.0, 682.0)
    assert pos.current_time == 215.0, "Current time incorrect"
    assert pos.total_time == 682.0, "Total time incorrect"
    assert 31.5 < pos.percentage < 31.6, f"Percentage incorrect: {pos.percentage}"
    assert pos.current_time_formatted == "3:35", f"Format incorrect: {pos.current_time_formatted}"
    assert pos.total_time_formatted == "11:22", f"Format incorrect: {pos.total_time_formatted}"
    print("   ✓ All calculations correct")
    print(f"   Position: {pos}")
    
    # Test 2: Start of track
    print("\n1.2 Start of Track (0:00 / 5:00)")
    pos_start = PlaybackPosition(0.0, 300.0)
    assert pos_start.percentage == 0.0, "Start percentage should be 0"
    assert pos_start.remaining_time == 300.0, "Remaining time incorrect"
    print("   ✓ Start position correct")
    print(f"   Position: {pos_start}")
    
    # Test 3: End of track
    print("\n1.3 End of Track (5:00 / 5:00)")
    pos_end = PlaybackPosition(300.0, 300.0)
    assert pos_end.percentage == 100.0, "End percentage should be 100"
    assert pos_end.remaining_time == 0.0, "Remaining time should be 0"
    print("   ✓ End position correct")
    print(f"   Position: {pos_end}")
    
    # Test 4: Long track (over 1 hour)
    print("\n1.4 Long Track (1:02:05 / 2:00:00)")
    pos_long = PlaybackPosition(3725.0, 7200.0)
    assert pos_long.current_time_formatted == "1:02:05", f"Long format incorrect: {pos_long.current_time_formatted}"
    assert pos_long.total_time_formatted == "2:00:00", f"Long format incorrect: {pos_long.total_time_formatted}"
    print("   ✓ Long track formatting correct")
    print(f"   Position: {pos_long}")
    
    # Test 5: Unknown duration
    print("\n1.5 Unknown Duration (0:30 / unknown)")
    pos_unknown = PlaybackPosition(30.0, 0.0)
    assert pos_unknown.percentage == 0.0, "Unknown duration should give 0% (not infinity)"
    assert pos_unknown.remaining_time == 0.0, "Unknown remaining should be 0"
    print("   ✓ Unknown duration handled correctly")
    print(f"   Position: {pos_unknown}")
    
    # Test 6: Dictionary export
    print("\n1.6 Dictionary Export")
    pos_dict = pos.to_dict()
    required_keys = ['current_time', 'total_time', 'percentage', 'remaining_time',
                     'current_formatted', 'total_formatted', 'remaining_formatted']
    for key in required_keys:
        assert key in pos_dict, f"Missing key in dictionary: {key}"
    print("   ✓ Dictionary export contains all required keys")
    print(f"   Keys: {list(pos_dict.keys())}")
    
    print("\n✓ All PlaybackPosition tests passed!")
    return True


def test_time_formatting():
    """Test time formatting with various durations"""
    
    print("\n" + "=" * 70)
    print("TEST 2: Time Formatting")
    print("=" * 70)
    
    test_cases = [
        (0, "0:00", "Zero seconds"),
        (30, "0:30", "30 seconds"),
        (60, "1:00", "One minute"),
        (90, "1:30", "One and a half minutes"),
        (215, "3:35", "Three minutes, 35 seconds"),
        (600, "10:00", "Ten minutes"),
        (3599, "59:59", "Just under one hour"),
        (3600, "1:00:00", "Exactly one hour"),
        (3665, "1:01:05", "One hour, one minute, five seconds"),
        (7200, "2:00:00", "Two hours"),
    ]
    
    pos = PlaybackPosition(0, 0)  # Dummy position for formatting tests
    
    for seconds, expected, description in test_cases:
        formatted = pos.format_time(seconds)
        status = "✓" if formatted == expected else "✗"
        print(f"   {status} {description:30} {seconds:5}s -> {formatted:8} (expected: {expected})")
        assert formatted == expected, f"Format mismatch for {seconds}s: got {formatted}, expected {expected}"
    
    print("\n✓ All time formatting tests passed!")
    return True


def test_position_tracker():
    """Test PositionTracker class (without actual VLC player)"""
    
    print("\n" + "=" * 70)
    print("TEST 3: PositionTracker Class")
    print("=" * 70)
    
    # Test 1: Initialization without player
    print("\n3.1 Initialization")
    tracker = PositionTracker()
    assert tracker.player is None, "Player should be None initially"
    print("   ✓ Tracker initialized without player")
    
    # Test 2: Set player
    print("\n3.2 Setting Player")
    mock_player = "mock_player_object"  # In real use, this would be vlc.MediaPlayer
    tracker.set_player(mock_player)
    assert tracker.player == mock_player, "Player not set correctly"
    print("   ✓ Player set successfully")
    
    # Test 3: Update interval
    print("\n3.3 Update Interval")
    tracker.set_update_interval(1.0)
    assert tracker._update_interval == 1.0, "Update interval not set"
    
    # Test minimum interval enforcement
    tracker.set_update_interval(0.05)  # Try to set too low
    assert tracker._update_interval >= 0.1, "Minimum interval not enforced"
    print("   ✓ Update interval works correctly")
    
    # Test 4: Should update logic
    print("\n3.4 Update Throttling")
    tracker.set_update_interval(0.5)
    
    # First call should always return True
    assert tracker.should_update() == True, "First update check should return True"
    
    # Immediate second call should return False (not enough time passed)
    assert tracker.should_update() == False, "Second immediate check should return False"
    
    print("   ✓ Update throttling works correctly")
    
    # Test 5: Get position without player
    print("\n3.5 Get Position (No Player)")
    pos = tracker.get_position()
    assert pos is None, "Position should be None when no player available"
    print("   ✓ Handles missing player gracefully")
    
    print("\n✓ All PositionTracker tests passed!")
    return True


def test_edge_cases():
    """Test edge cases and error conditions"""
    
    print("\n" + "=" * 70)
    print("TEST 4: Edge Cases")
    print("=" * 70)
    
    # Test 1: Negative times (shouldn't happen, but handle gracefully)
    print("\n4.1 Negative Times")
    pos = PlaybackPosition(-10.0, 300.0)
    # Should still work, even if nonsensical
    formatted = pos.current_time_formatted
    print(f"   Negative time formatted as: {formatted}")
    print("   ✓ Handles negative times without crashing")
    
    # Test 2: Current > Total (shouldn't happen, but handle it)
    print("\n4.2 Current Exceeds Total")
    pos = PlaybackPosition(400.0, 300.0)
    percentage = pos.percentage
    remaining = pos.remaining_time
    print(f"   Percentage: {percentage:.1f}% (over 100% is acceptable)")
    print(f"   Remaining: {remaining:.1f}s (negative is clamped to 0)")
    assert remaining >= 0, "Remaining time should not be negative"
    print("   ✓ Handles current > total gracefully")
    
    # Test 3: Very large numbers
    print("\n4.3 Very Large Numbers (24 hour marathon jam)")
    pos = PlaybackPosition(43200.0, 86400.0)  # 12 hours into 24 hour track
    assert pos.percentage == 50.0, "Large number percentage incorrect"
    formatted = pos.current_time_formatted
    print(f"   12 hours formatted as: {formatted}")
    print("   ✓ Handles very large durations")
    
    # Test 4: Float precision
    print("\n4.4 Float Precision")
    pos = PlaybackPosition(123.456789, 456.789123)
    percentage = pos.percentage
    print(f"   Precise percentage: {percentage}")
    # Should not crash or produce NaN
    assert not (percentage != percentage), "Percentage is NaN"  # NaN check
    print("   ✓ Handles float precision correctly")
    
    print("\n✓ All edge case tests passed!")
    return True


def run_all_tests():
    """Run all test suites"""
    
    print("\n" + "=" * 70)
    print("DeadStream Position Tracker - Test Suite")
    print("Task 4.5 - Track Playback Position")
    print("=" * 70)
    
    results = []
    
    try:
        results.append(("PlaybackPosition Class", test_playback_position()))
    except AssertionError as e:
        print(f"\n✗ PlaybackPosition tests FAILED: {e}")
        results.append(("PlaybackPosition Class", False))
    
    try:
        results.append(("Time Formatting", test_time_formatting()))
    except AssertionError as e:
        print(f"\n✗ Time Formatting tests FAILED: {e}")
        results.append(("Time Formatting", False))
    
    try:
        results.append(("PositionTracker Class", test_position_tracker()))
    except AssertionError as e:
        print(f"\n✗ PositionTracker tests FAILED: {e}")
        results.append(("PositionTracker Class", False))
    
    try:
        results.append(("Edge Cases", test_edge_cases()))
    except AssertionError as e:
        print(f"\n✗ Edge Case tests FAILED: {e}")
        results.append(("Edge Cases", False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8} {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED - Task 4.5 implementation is correct!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Copy position_tracker.py to your project's src/audio/ directory")
        print("2. Integrate with your existing audio player")
        print("3. Test with real audio playback")
        print("4. Move on to Task 4.6 (Seek functionality)")
    else:
        print("✗ SOME TESTS FAILED - Please review implementation")
        print("=" * 70)
    
    return all_passed


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
