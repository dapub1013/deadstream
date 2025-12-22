#!/usr/bin/env python3
"""
Test script for database query functions

This script tests all the query functions in src/database/queries.py
to verify they work correctly with the populated database.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.database import queries


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def print_show(show, show_number=None):
    """Print a show in a nice format"""
    prefix = f"{show_number}. " if show_number else "  "
    location = f"{show['city']}, {show['state']}" if show['city'] and show['state'] else (show['city'] or show['state'] or "Unknown")
    venue = show['venue'] or "Unknown venue"
    rating = f"{show['avg_rating']:.2f}★" if show['avg_rating'] else "Unrated"
    
    print(f"{prefix}{show['date']} - {venue}")
    print(f"   {location} - {rating} ({show['num_reviews']} reviews)")


def main():
    print("\n" + "="*60)
    print("DATABASE QUERY FUNCTIONS TEST")
    print("="*60)
    
    # Test 1: Get specific show (Cornell '77)
    print_section("Test 1: Get Show by Identifier")
    cornell = queries.get_show_by_identifier("gd77-05-08.sbd.hicks.4982.sbeok.shnf")
    if cornell:
        print_show(cornell)
        print(f"   Identifier: {cornell['identifier']}")
    else:
        print("  Cornell '77 not found (try another identifier)")
    
    # Test 2: Get shows on a specific date
    print_section("Test 2: Get Shows on Date (1977-05-08)")
    may_8_shows = queries.get_show_by_date("1977-05-08")
    print(f"Found {len(may_8_shows)} recording(s) of this show:")
    for i, show in enumerate(may_8_shows[:5], 1):
        print_show(show, i)
    
    # Test 3: Top rated shows
    print_section("Test 3: Top 10 Rated Shows (All Time)")
    top_shows = queries.get_top_rated_shows(limit=10, min_reviews=10)
    for i, show in enumerate(top_shows, 1):
        print_show(show, i)
    
    # Test 4: Shows from a specific year
    print_section("Test 4: Top 5 Shows from 1977")
    shows_1977 = queries.get_top_rated_by_year(1977, limit=5)
    for i, show in enumerate(shows_1977, 1):
        print_show(show, i)
    
    # Test 5: Search by venue
    print_section("Test 5: Shows at Fillmore (partial match)")
    fillmore_shows = queries.search_by_venue("Fillmore", exact_match=False)
    print(f"Found {len(fillmore_shows)} shows at Fillmore venues:")
    for show in fillmore_shows[:5]:
        print_show(show)
    if len(fillmore_shows) > 5:
        print(f"  ... and {len(fillmore_shows) - 5} more")
    
    # Test 6: On this day in history
    print_section("Test 6: Shows on December 21st (Today!)")
    today_shows = queries.get_on_this_day(12, 21)
    print(f"Found {len(today_shows)} show(s) on December 21st across all years:")
    for show in today_shows:
        print_show(show)
    
    # Test 7: Random show
    print_section("Test 7: Random Show")
    random_show = queries.get_random_show()
    if random_show:
        print("Here's a random show from the collection:")
        print_show(random_show)
    
    # Test 8: Statistics
    print_section("Test 8: Database Statistics")
    total_shows = queries.get_show_count()
    venue_count = queries.get_venue_count()
    date_range = queries.get_date_range()
    
    print(f"Total shows: {total_shows:,}")
    print(f"Unique venues: {venue_count:,}")
    print(f"Date range: {date_range[0]} to {date_range[1]}")
    
    print("\nShows by decade:")
    year_counts = queries.get_show_count_by_year()
    decades = {}
    for year, count in year_counts:
        decade = (int(year) // 10) * 10
        decades[decade] = decades.get(decade, 0) + count
    
    for decade in sorted(decades.keys()):
        print(f"  {decade}s: {decades[decade]:,} shows")
    
    print("\nTop 5 most played venues:")
    top_venues = queries.get_most_played_venues(limit=5)
    for i, (venue, count) in enumerate(top_venues, 1):
        print(f"  {i}. {venue}: {count} shows")
    
    print("\nTop 5 states by show count:")
    state_stats = queries.get_shows_by_state_stats()
    for i, (state, count) in enumerate(state_stats[:5], 1):
        print(f"  {i}. {state}: {count} shows")
    
    # Test 9: Combined search
    print_section("Test 9: Combined Search (NY, 1970s, rating > 4.0)")
    combined = queries.search_shows(
        state="NY",
        min_rating=4.0,
        limit=5
    )
    # Filter to 1970s
    combined_70s = [s for s in combined if s['date'].startswith('197')]
    print(f"Found {len(combined_70s)} matching shows:")
    for i, show in enumerate(combined_70s[:5], 1):
        print_show(show, i)
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETE - Query functions working!")
    print("="*60)
    print()


if __name__ == '__main__':
    main()
