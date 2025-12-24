#!/usr/bin/env python3
"""
Test User Preferences System

Tests loading, saving, and using preferences with the RecordingScorer.
"""

import sys
import os
sys.path.insert(0, '/home/david/deadstream')

from src.selection.preferences import PreferenceManager, create_default_preferences_file
from src.selection.scoring import RecordingScorer
from src.database.queries import get_show_by_date
from src.api.metadata import get_metadata

def test_preference_manager():
    """Test basic PreferenceManager functionality."""
    print("\n" + "="*60)
    print("TEST 1: PreferenceManager Basic Functions")
    print("="*60)
    
    # Create manager
    pm = PreferenceManager()
    
    # Display current preferences
    pm.display_current_preferences()
    
    # Test getting weights
    weights = pm.get_weights()
    print(f"\n[INFO] Retrieved weights: {weights}")
    
    # Verify sum
    total = sum(weights.values())
    if 0.99 <= total <= 1.01:
        print(f"[PASS] Weights sum to {total:.2f}")
    else:
        print(f"[FAIL] Weights sum to {total:.2f} (should be 1.0)")
        return False
    
    return True


def test_presets():
    """Test preset profiles."""
    print("\n" + "="*60)
    print("TEST 2: Preset Profiles")
    print("="*60)
    
    pm = PreferenceManager()
    
    # Test each preset
    for preset_name in pm.get_preset_names():
        print(f"\n[INFO] Testing preset: {preset_name}")
        
        pm.use_preset(preset_name)
        weights = pm.get_weights()
        
        print(f"  Weights: {weights}")
        
        # Verify sum
        total = sum(weights.values())
        if 0.99 <= total <= 1.01:
            print(f"  [PASS] {preset_name} weights sum to {total:.2f}")
        else:
            print(f"  [FAIL] {preset_name} weights sum to {total:.2f}")
            return False
    
    return True


def test_custom_weights():
    """Test setting custom weights."""
    print("\n" + "="*60)
    print("TEST 3: Custom Weights")
    print("="*60)
    
    pm = PreferenceManager()
    
    # Try valid custom weights
    custom_weights = {
        'source_type': 0.50,
        'format_quality': 0.30,
        'community_rating': 0.10,
        'lineage': 0.05,
        'taper': 0.05
    }
    
    print(f"\n[INFO] Setting custom weights: {custom_weights}")
    
    try:
        pm.set_weights(custom_weights)
        print("[PASS] Custom weights accepted")
        
        # Verify they were set
        retrieved = pm.get_weights()
        if retrieved == custom_weights:
            print("[PASS] Custom weights retrieved correctly")
        else:
            print("[FAIL] Retrieved weights don't match")
            return False
            
    except Exception as e:
        print(f"[FAIL] Error setting custom weights: {e}")
        return False
    
    # Try invalid weights (don't sum to 1.0)
    print("\n[INFO] Testing invalid weights (should fail)...")
    invalid_weights = {
        'source_type': 0.50,
        'format_quality': 0.30,
        'community_rating': 0.10,
        'lineage': 0.05,
        'taper': 0.15  # This makes total 1.10
    }
    
    try:
        pm.set_weights(invalid_weights)
        print("[FAIL] Invalid weights were accepted (should have been rejected)")
        return False
    except ValueError as e:
        print(f"[PASS] Invalid weights rejected as expected: {e}")
    
    return True


def test_save_and_load():
    """Test saving and loading preferences."""
    print("\n" + "="*60)
    print("TEST 4: Save and Load Preferences")
    print("="*60)
    
    # Create test config path
    test_config = '/tmp/test_preferences.yaml'
    
    # Remove existing test file
    if os.path.exists(test_config):
        os.remove(test_config)
    
    # Create manager with test path
    pm1 = PreferenceManager(config_path=test_config)
    
    # Set custom weights
    custom_weights = {
        'source_type': 0.40,
        'format_quality': 0.30,
        'community_rating': 0.15,
        'lineage': 0.10,
        'taper': 0.05
    }
    
    print(f"\n[INFO] Setting and saving custom weights...")
    pm1.set_weights(custom_weights)
    
    if not pm1.save_preferences():
        print("[FAIL] Failed to save preferences")
        return False
    
    print("[PASS] Preferences saved")
    
    # Create new manager and load
    print("\n[INFO] Loading preferences from file...")
    pm2 = PreferenceManager(config_path=test_config)
    
    loaded_weights = pm2.get_weights()
    
    if loaded_weights == custom_weights:
        print("[PASS] Loaded weights match saved weights")
    else:
        print(f"[FAIL] Loaded weights don't match")
        print(f"  Expected: {custom_weights}")
        print(f"  Got: {loaded_weights}")
        return False
    
    # Clean up
    os.remove(test_config)
    
    return True


def test_scorer_integration():
    """Test RecordingScorer with PreferenceManager."""
    print("\n" + "="*60)
    print("TEST 5: RecordingScorer Integration")
    print("="*60)
    
    # Create preference manager with audiophile preset
    pm = PreferenceManager()
    pm.use_preset('audiophile')
    
    print("\n[INFO] Using 'audiophile' preset")
    pm.display_current_preferences()
    
    # Create scorer with preference manager
    scorer = RecordingScorer(preference_manager=pm)
    
    print("\n[INFO] Created RecordingScorer with preferences")
    print(f"Scorer weights: {scorer.weights}")
    
    # Verify weights match
    if scorer.weights == pm.get_weights():
        print("[PASS] Scorer using preference manager weights")
    else:
        print("[FAIL] Scorer weights don't match preference manager")
        return False
    
    # Test with different preset
    pm.use_preset('crowd_favorite')
    scorer2 = RecordingScorer(preference_manager=pm)
    
    print("\n[INFO] Testing 'crowd_favorite' preset")
    print(f"Scorer weights: {scorer2.weights}")
    
    if scorer2.weights == pm.get_weights():
        print("[PASS] Scorer updated with new preset")
    else:
        print("[FAIL] Scorer not using new preset")
        return False
    
    return True


def test_real_scoring():
    """Test scoring with different preference profiles."""
    print("\n" + "="*60)
    print("TEST 6: Real Scoring with Different Profiles")
    print("="*60)
    
    # Get a show with multiple recordings
    print("\n[INFO] Getting Cornell '77 (multiple recordings)...")
    shows = get_show_by_date('1977-05-08')
    
    if not shows:
        print("[WARN] Could not get Cornell '77, skipping real scoring test")
        return True
    
    print(f"[INFO] Found {len(shows)} recording(s)")
    
    # Test with different profiles
    profiles = ['balanced', 'audiophile', 'crowd_favorite']
    
    for profile_name in profiles:
        print(f"\n[INFO] Scoring with '{profile_name}' profile...")
        
        pm = PreferenceManager()
        pm.use_preset(profile_name)
        scorer = RecordingScorer(preference_manager=pm)
        
        # Score first recording
        if len(shows) > 0:
            show = shows[0]
            try:
                metadata = get_metadata(show['identifier'])
                score_data = scorer.score_recording(metadata)
                
                print(f"  Total Score: {score_data['total_score']:.1f}")
                print(f"  Breakdown:")
                for component, score in score_data['component_scores'].items():
                    print(f"    {component:20s}: {score:.1f}")
                    
            except Exception as e:
                print(f"  [WARN] Could not score: {e}")
    
    print("\n[PASS] Scored with multiple profiles")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("DeadStream User Preferences Test Suite")
    print("="*60)
    
    tests = [
        ("PreferenceManager Basics", test_preference_manager),
        ("Preset Profiles", test_presets),
        ("Custom Weights", test_custom_weights),
        ("Save and Load", test_save_and_load),
        ("Scorer Integration", test_scorer_integration),
        ("Real Scoring", test_real_scoring),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print("\n[FAILURE] Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
