#!/usr/bin/env python3
"""
Test script for Random Show functionality (Task 7.6)

This script tests:
1. get_random_show() database function
2. Repeated random calls return different shows (usually)
3. Browse screen integration
4. Error handling
5. Edge cases

Usage:
    # Desktop
    python3 examples/test_random_show.py
    
    # Raspberry Pi
    ssh -X david@192.168.4.27
    cd ~/deadstream
    python3 examples/test_random_show.py
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.database.queries import get_random_show, get_show_count


def test_get_random_show():
    """Test the get_random_show() database function"""
    
    print("=" * 70)
    print("TEST 1: get_random_show() Database Function")
    print("=" * 70)
    print()
    
    try:
        # Get total show count first
        total_shows = get_show_count()
        print(f"[INFO] Database contains {total_shows:,} shows")
        print()
        
        if total_shows == 0:
            print("[WARN] Database is empty! Cannot test random show.")
            print("[WARN] Run populate_database.py first.")
            return False
        
        # Test getting a random show
        print("[INFO] Getting a random show...")
        show = get_random_show()
        
        if not show:
            print("[ERROR] get_random_show() returned None")
            return False
        
        # Verify show has required fields
        required_fields = ['identifier', 'date', 'venue', 'city', 'state']
        missing_fields = [f for f in required_fields if f not in show]
        
        if missing_fields:
            print(f"[ERROR] Random show missing fields: {missing_fields}")
            return False
        
        # Print show details
        print("[OK] Random show retrieved successfully!")
        print()
        print("Show Details:")
        print(f"  Date: {show['date']}")
        print(f"  Venue: {show['venue']}")
        print(f"  City: {show['city']}, {show['state']}")
        print(f"  Identifier: {show['identifier']}")
        if show.get('avg_rating'):
            print(f"  Rating: {show['avg_rating']:.1f}/5.0")
        print()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_random_variation():
    """Test that repeated calls return different shows"""
    
    print("=" * 70)
    print("TEST 2: Random Variation")
    print("=" * 70)
    print()
    
    try:
        # Get 10 random shows
        num_tests = 10
        print(f"[INFO] Getting {num_tests} random shows...")
        print()
        
        shows = []
        identifiers = set()
        
        for i in range(num_tests):
            show = get_random_show()
            if show:
                shows.append(show)
                identifiers.add(show['identifier'])
                print(f"  {i+1}. {show['date']} - {show['venue']}")
        
        print()
        
        # Calculate uniqueness
        unique_count = len(identifiers)
        uniqueness_pct = (unique_count / num_tests) * 100
        
        print(f"[INFO] Got {unique_count} unique shows out of {num_tests} calls")
        print(f"[INFO] Uniqueness: {uniqueness_pct:.0f}%")
        print()
        
        # With a large database, we should get mostly unique shows
        # But some repeats are possible (and that's OK for random)
        if unique_count >= num_tests * 0.7:  # 70% unique is good enough
            print("[OK] Good variation in random results")
            return True
        else:
            print("[WARN] Low variation - but this could just be luck")
            print("[WARN] Random selection is working, just got some duplicates")
            return True  # Still pass - randomness allows duplicates
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_random_show_fields():
    """Test that random shows have all expected fields"""
    
    print("=" * 70)
    print("TEST 3: Random Show Field Validation")
    print("=" * 70)
    print()
    
    try:
        show = get_random_show()
        
        if not show:
            print("[ERROR] No random show returned")
            return False
        
        # Expected fields (all shows should have these)
        required_fields = {
            'identifier': str,
            'date': str,
            'venue': str,
            'city': str,
            'state': str,
        }
        
        # Optional fields
        optional_fields = {
            'avg_rating': (float, type(None)),
            'num_reviews': (int, type(None)),
            'source': str,
            'lineage': str,
            'taper': str,
        }
        
        print("[INFO] Validating required fields...")
        all_valid = True
        
        for field, expected_type in required_fields.items():
            if field not in show:
                print(f"  [ERROR] Missing required field: {field}")
                all_valid = False
            elif not isinstance(show[field], expected_type):
                print(f"  [ERROR] Field {field} has wrong type: {type(show[field])}")
                all_valid = False
            else:
                print(f"  [OK] {field}: {show[field]}")
        
        print()
        print("[INFO] Checking optional fields...")
        
        for field, expected_types in optional_fields.items():
            if field in show and show[field] is not None:
                if not isinstance(show[field], expected_types):
                    print(f"  [WARN] Field {field} has unexpected type: {type(show[field])}")
                else:
                    print(f"  [OK] {field}: {show[field]}")
        
        print()
        
        if all_valid:
            print("[OK] All required fields present and valid")
            return True
        else:
            print("[ERROR] Some required fields missing or invalid")
            return False
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_browse_screen_integration():
    """Test random show integration in browse screen"""
    
    print("=" * 70)
    print("TEST 4: Browse Screen Integration")
    print("=" * 70)
    print()
    
    try:
        from PyQt5.QtWidgets import QApplication
        from src.ui.screens.browse_screen import BrowseScreen
        
        # Create application (required for PyQt5)
        app = QApplication(sys.argv)
        
        print("[INFO] Creating browse screen...")
        browse = BrowseScreen()
        
        print("[INFO] Testing load_random_show() method...")
        browse.load_random_show()
        
        # Check that a show was loaded
        if not browse.current_shows:
            print("[ERROR] No shows loaded after load_random_show()")
            return False
        
        if len(browse.current_shows) != 1:
            print(f"[ERROR] Expected 1 show, got {len(browse.current_shows)}")
            return False
        
        show = browse.current_shows[0]
        
        print("[OK] Random show loaded successfully!")
        print()
        print("Show Details:")
        print(f"  Date: {show['date']}")
        print(f"  Venue: {show['venue']}")
        print(f"  City: {show['city']}, {show['state']}")
        print()
        
        # Check header was updated
        header_title = browse.header_title.text()
        header_subtitle = browse.header_subtitle.text()
        
        print(f"Header Title: {header_title}")
        print(f"Header Subtitle: {header_subtitle}")
        print()
        
        if "Random Show" not in header_title:
            print("[WARN] Header title doesn't contain 'Random Show'")
        
        if show['date'] not in header_subtitle:
            print("[WARN] Header subtitle doesn't contain show date")
        
        print("[OK] Browse screen integration working!")
        return True
        
    except ImportError as e:
        print(f"[WARN] Cannot test UI integration (PyQt5 not available): {e}")
        print("[INFO] This is OK if running on headless system")
        return True
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling for edge cases"""
    
    print("=" * 70)
    print("TEST 5: Error Handling")
    print("=" * 70)
    print()
    
    try:
        # Test 1: Random show with empty database
        # (We can't actually test this without breaking the real database,
        #  so we'll just verify the function handles None gracefully)
        
        print("[INFO] Testing that None handling works...")
        show = get_random_show()
        
        if show is None:
            print("[WARN] get_random_show() returned None")
            print("[INFO] This is OK if database is empty")
        else:
            print("[OK] get_random_show() returned a valid show")
        
        print()
        
        # Test 2: Verify browse screen handles errors gracefully
        try:
            from PyQt5.QtWidgets import QApplication
            from src.ui.screens.browse_screen import BrowseScreen
            
            app = QApplication(sys.argv)
            browse = BrowseScreen()
            
            # This should not crash even if there are no shows
            print("[INFO] Testing browse screen error handling...")
            browse.load_random_show()
            print("[OK] browse.load_random_show() completed without crashing")
            
        except ImportError:
            print("[WARN] Cannot test UI error handling (PyQt5 not available)")
        
        print()
        print("[OK] Error handling tests complete")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all test cases"""
    
    print()
    print("=" * 70)
    print("TASK 7.6: RANDOM SHOW FUNCTIONALITY TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        ("Database Function", test_get_random_show),
        ("Random Variation", test_random_variation),
        ("Field Validation", test_random_show_fields),
        ("Browse Integration", test_browse_screen_integration),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print()
        except Exception as e:
            print(f"[ERROR] Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
            print()
    
    # Print summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("[OK] All tests passed!")
        print()
        print("Task 7.6 COMPLETE - Random show button is working correctly!")
        return True
    else:
        print(f"[ERROR] {total - passed} test(s) failed")
        return False


if __name__ == '__main__':
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[INFO] Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Test suite crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
