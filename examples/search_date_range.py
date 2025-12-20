#!/usr/bin/env python3
"""
Phase 2.4: Search for shows by date range with pagination support

This script demonstrates:
1. How to search by year, month, or custom date range
2. How to handle pagination (results > 100)
3. How to sort and display results
4. How to export results to JSON

Usage:
    # Search by year
    python3 search_date_range.py --year 1977
    
    # Search by year and month
    python3 search_date_range.py --year 1977 --month 5
    
    # Search by custom date range
    python3 search_date_range.py --start 1977-05-01 --end 1977-05-31
    
    # Limit results
    python3 search_date_range.py --year 1977 --limit 50
    
    # Export to JSON
    python3 search_date_range.py --year 1977 --export shows_1977.json
"""

import requests
import sys
import json
import argparse
from datetime import datetime


def search_date_range(year=None, month=None, start_date=None, end_date=None, 
                      rows=100, page=0, sort='date asc'):
    """
    Search for shows by date range.
    
    Args:
        year (int): Year to search (e.g., 1977)
        month (int): Month to search (1-12), requires year
        start_date (str): Start date (YYYY-MM-DD)
        end_date (str): End date (YYYY-MM-DD)
        rows (int): Number of results per page (max 100)
        page (int): Page number (0-indexed)
        sort (str): Sort order (e.g., 'date asc', 'avg_rating desc')
        
    Returns:
        dict: Search results with 'response' and 'responseHeader'
    """
    base_url = "https://archive.org/advancedsearch.php"
    
    # Build the query
    query_parts = ["collection:GratefulDead"]
    
    if start_date and end_date:
        # Custom date range
        query_parts.append(f"date:[{start_date} TO {end_date}]")
    elif year and month:
        # Specific year and month (e.g., 1977-05)
        query_parts.append(f"date:{year}-{month:02d}*")
    elif year:
        # Entire year
        query_parts.append(f"year:{year}")
    else:
        # No date filter - all shows
        pass
    
    query = " AND ".join(query_parts)
    
    # Fields to return
    fields = [
        'identifier',
        'title', 
        'date',
        'year',
        'venue',
        'coverage',  # Often has city, state
        'source',
        'avg_rating',
        'num_reviews',
    ]
    
    params = {
        'q': query,
        'fl': ','.join(fields),
        'rows': min(rows, 100),  # API max is 100
        'page': page,
        'sort': sort,
        'output': 'json',
    }
    
    try:
        print(f"Searching: {query}")
        print(f"Page: {page + 1}, Rows: {params['rows']}")
        
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        return data
        
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
        return None


def get_all_results(year=None, month=None, start_date=None, end_date=None, 
                    limit=None, sort='date asc'):
    """
    Get all results for a date range, handling pagination automatically.
    
    Args:
        year, month, start_date, end_date: Date filters
        limit (int): Maximum total results to fetch (None = all)
        sort (str): Sort order
        
    Returns:
        list: All matching shows
    """
    all_shows = []
    page = 0
    
    while True:
        # Determine how many rows to fetch this page
        if limit:
            remaining = limit - len(all_shows)
            if remaining <= 0:
                break
            rows = min(100, remaining)
        else:
            rows = 100
        
        # Fetch this page
        data = search_date_range(
            year=year,
            month=month,
            start_date=start_date,
            end_date=end_date,
            rows=rows,
            page=page,
            sort=sort
        )
        
        if not data:
            print("Failed to fetch results")
            break
        
        # Extract shows from response
        response = data.get('response', {})
        shows = response.get('docs', [])
        total_found = response.get('numFound', 0)
        
        if not shows:
            # No more results
            break
        
        all_shows.extend(shows)
        
        print(f"Fetched {len(shows)} shows (Total so far: {len(all_shows)}/{total_found})")
        
        # Check if we've got all results
        if len(all_shows) >= total_found:
            break
        
        # Check if we've hit our limit
        if limit and len(all_shows) >= limit:
            break
        
        # Move to next page
        page += 1
    
    return all_shows


def format_show(show, index=None):
    """
    Format a show for display.
    
    Args:
        show (dict): Show data from API
        index (int): Optional index number
        
    Returns:
        str: Formatted show info
    """
    # Extract fields with defaults
    date = show.get('date', 'Unknown date')
    venue = show.get('venue', 'Unknown venue')
    coverage = show.get('coverage', '')
    source = show.get('source', 'Unknown source')
    rating = show.get('avg_rating', 'Not rated')
    reviews = show.get('num_reviews', 0)
    identifier = show.get('identifier', 'Unknown')
    
    # Format rating
    if rating != 'Not rated':
        rating_str = f"{rating}/5.0 ({reviews} reviews)"
    else:
        rating_str = "Not rated"
    
    # Build output
    lines = []
    if index is not None:
        lines.append(f"\n{index}. {date}")
    else:
        lines.append(f"\n{date}")
    
    lines.append(f"   Venue:      {venue}")
    if coverage:
        lines.append(f"   Location:   {coverage}")
    lines.append(f"   Source:     {source}")
    lines.append(f"   Rating:     {rating_str}")
    lines.append(f"   Identifier: {identifier}")
    
    return "\n".join(lines)


def print_summary(shows, search_params):
    """
    Print summary of search results.
    
    Args:
        shows (list): All shows found
        search_params (dict): Search parameters used
    """
    print("\n" + "=" * 70)
    print("SEARCH SUMMARY")
    print("=" * 70)
    
    if search_params.get('year') and search_params.get('month'):
        month_name = datetime(2000, search_params['month'], 1).strftime('%B')
        print(f"Search: {month_name} {search_params['year']}")
    elif search_params.get('year'):
        print(f"Search: {search_params['year']}")
    elif search_params.get('start_date') and search_params.get('end_date'):
        print(f"Search: {search_params['start_date']} to {search_params['end_date']}")
    else:
        print("Search: All shows")
    
    print(f"Total shows found: {len(shows)}")
    
    if shows:
        # Calculate statistics
        rated_shows = [s for s in shows if s.get('avg_rating')]
        if rated_shows:
            avg_rating = sum(float(s['avg_rating']) for s in rated_shows) / len(rated_shows)
            print(f"Average rating: {avg_rating:.2f}/5.0")
        
        # Date range
        dates = [s.get('date') for s in shows if s.get('date')]
        if dates:
            dates.sort()
            print(f"Date range: {dates[0]} to {dates[-1]}")
        
        # Unique venues
        venues = set(s.get('venue') for s in shows if s.get('venue'))
        print(f"Unique venues: {len(venues)}")
    
    print()


def export_to_json(shows, filename):
    """
    Export shows to JSON file.
    
    Args:
        shows (list): Shows to export
        filename (str): Output filename
    """
    try:
        with open(filename, 'w') as f:
            json.dump(shows, f, indent=2)
        print(f"Exported {len(shows)} shows to: {filename}")
    except IOError as e:
        print(f"Error writing file: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Search for Grateful Dead shows by date range',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # All shows from 1977
  %(prog)s --year 1977
  
  # May 1977 (the legendary month!)
  %(prog)s --year 1977 --month 5
  
  # Custom date range
  %(prog)s --start 1977-05-01 --end 1977-05-31
  
  # Limit to 50 results
  %(prog)s --year 1977 --limit 50
  
  # Sort by rating (highest first)
  %(prog)s --year 1977 --sort "avg_rating desc"
  
  # Export to JSON
  %(prog)s --year 1977 --export shows_1977.json
        """
    )
    
    # Date filters
    parser.add_argument('--year', type=int, help='Year to search (e.g., 1977)')
    parser.add_argument('--month', type=int, help='Month to search (1-12)')
    parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    
    # Options
    parser.add_argument('--limit', type=int, help='Maximum number of results')
    parser.add_argument('--sort', default='date asc', 
                       help='Sort order (default: "date asc")')
    parser.add_argument('--export', help='Export results to JSON file')
    parser.add_argument('--no-display', action='store_true',
                       help='Don\'t display results (use with --export)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.month and not args.year:
        print("Error: --month requires --year")
        sys.exit(1)
    
    if (args.start or args.end) and (args.year or args.month):
        print("Error: Use either --year/--month OR --start/--end, not both")
        sys.exit(1)
    
    if args.start and not args.end:
        print("Error: --start requires --end")
        sys.exit(1)
    
    if args.end and not args.start:
        print("Error: --end requires --start")
        sys.exit(1)
    
    # Build search parameters
    search_params = {}
    if args.year:
        search_params['year'] = args.year
    if args.month:
        search_params['month'] = args.month
    if args.start:
        search_params['start_date'] = args.start
    if args.end:
        search_params['end_date'] = args.end
    
    # Fetch all results
    print("Searching Internet Archive...")
    print()
    
    shows = get_all_results(
        year=search_params.get('year'),
        month=search_params.get('month'),
        start_date=search_params.get('start_date'),
        end_date=search_params.get('end_date'),
        limit=args.limit,
        sort=args.sort
    )
    
    # Print summary
    print_summary(shows, search_params)
    
    # Display results
    if not args.no_display and shows:
        print("=" * 70)
        print("RESULTS")
        print("=" * 70)
        for i, show in enumerate(shows, 1):
            print(format_show(show, i))
        print()
    
    # Export if requested
    if args.export:
        export_to_json(shows, args.export)
    
    print(f"Phase 2.4: Found {len(shows)} shows")


if __name__ == "__main__":
    main()
