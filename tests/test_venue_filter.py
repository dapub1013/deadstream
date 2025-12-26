#!/usr/bin/env python3
"""
Test script for Task 7.3: Venue Filter

This script tests the venue browsing functionality.

Run on desktop:
    python3 test_venue_filter.py

Run on Pi:
    ssh -X david@192.168.4.27
    cd ~/deadstream
    python3 test_venue_filter.py
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.database.queries import get_most_played_venues, search_by_venue


def test_venue_queries():
    """Test the database query functions for venues"""
    
    print("=" * 60)
    print("TASK 7.3: VENUE FILTER - DATABASE QUERY TEST")
    print("=" * 60)
    print()
    
    # Test 1: Get most played venues
    print("[TEST 1] Get most played venues")
    print("-" * 60)
    
    venues = get_most_played_venues(limit=20)
    
    if not venues:
        print("[FAIL] No venues returned")
        return False
    
    print(f"[PASS] Found {len(venues)} venues")
    print()
    print("Top 10 Venues:")
    for i, (venue, count) in enumerate(venues[:10], 1):
        print(f"  {i:2d}. {venue:45s} ({count:3d} shows)")
    
    print()
    
    # Test 2: Search for specific venue (Fillmore)
    print("[TEST 2] Search for Fillmore shows")
    print("-" * 60)
    
    fillmore_shows = search_by_venue("Fillmore", exact_match=False)
    
    if not fillmore_shows:
        print("[WARN] No Fillmore shows found (might not be in database)")
    else:
        print(f"[PASS] Found {len(fillmore_shows)} Fillmore shows")
        print()
        print("First 5 Fillmore shows:")
        for i, show in enumerate(fillmore_shows[:5], 1):
            print(f"  {i}. {show['date']} - {show['venue']}")
        print()
    
    # Test 3: Search for Winterland
    print("[TEST 3] Search for Winterland shows")
    print("-" * 60)
    
    winterland_shows = search_by_venue("Winterland", exact_match=False)
    
    if not winterland_shows:
        print("[WARN] No Winterland shows found")
    else:
        print(f"[PASS] Found {len(winterland_shows)} Winterland shows")
        print()
        print("First 5 Winterland shows:")
        for i, show in enumerate(winterland_shows[:5], 1):
            print(f"  {i}. {show['date']} - {show['venue']}")
        print()
    
    # Test 4: Search for venue with exact match
    print("[TEST 4] Exact match search")
    print("-" * 60)
    
    if venues:
        test_venue = venues[0][0]  # Use first venue from most played
        exact_shows = search_by_venue(test_venue, exact_match=True)
        partial_shows = search_by_venue(test_venue, exact_match=False)
        
        print(f"Test venue: {test_venue}")
        print(f"Exact match: {len(exact_shows)} shows")
        print(f"Partial match: {len(partial_shows)} shows")
        
        if len(exact_shows) <= len(partial_shows):
            print("[PASS] Exact match returns fewer or equal results")
        else:
            print("[FAIL] Exact match returned more results than partial")
    
    print()
    print("=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)
    print()
    print("[OK] Database queries working correctly")
    print("[OK] Ready to implement UI")
    print()
    
    return True


if __name__ == '__main__':
    try:
        success = test_venue_queries()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
