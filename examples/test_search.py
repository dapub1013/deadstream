#!/usr/bin/env python3
"""
Task 2.2: Test Script - Search for Cornell '77
Simple script to test the Archive.org search functionality
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.archive_client import ArchiveClient


def print_separator(char='=', length=70):
    """Print a separator line"""
    print(char * length)


def format_show(show: dict, index: int) -> str:
    """
    Format a show for display
    
    Args:
        show: Show dictionary from API
        index: Show number (for display)
    
    Returns:
        Formatted string
    """
    # Extract fields with defaults for missing data
    identifier = show.get('identifier', 'N/A')
    title = show.get('title', 'Unknown Show')
    date = show.get('date', 'Unknown Date')
    venue = show.get('venue', 'Unknown Venue')
    location = show.get('coverage', 'Unknown Location')
    rating = show.get('avg_rating', 'N/A')
    
    # Format the date (remove time portion if present)
    if 'T' in date:
        date = date.split('T')[0]
    
    # Build the formatted output
    output = f"\n{index}. {date} - {venue}\n"
    output += f"   Location: {location}\n"
    output += f"   Identifier: {identifier}\n"
    output += f"   Rating: {rating}/5.0\n"
    
    return output


def main():
    """Main test function"""
    print_separator()
    print(" Task 2.2: Search for Cornell '77")
    print(" Testing Archive.org API Search")
    print_separator()
    
    # Create the client
    print("\nInitializing Archive.org client...")
    client = ArchiveClient()
    
    # Search for Cornell '77
    search_query = "date:1977-05-08"
    print(f"\nSearching for: {search_query}")
    print("Please wait...\n")
    
    try:
        # Perform the search
        shows = client.search_shows(search_query)
        
        # Display results
        print(f"SUCCESS! Found {len(shows)} recordings:\n")
        print_separator('-')
        
        for i, show in enumerate(shows, 1):
            print(format_show(show, i))
        
        print_separator('-')
        print(f"\nTotal recordings found: {len(shows)}")
        
        # Show which is likely the best
        if shows:
            best = max(shows, key=lambda x: x.get('avg_rating', 0))
            print(f"\nHighest rated: {best.get('identifier')}")
            print(f"Rating: {best.get('avg_rating')}/5.0")
        
        print_separator()
        print("✓ Task 2.2 Complete: Search functionality working!")
        print_separator()
        
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out")
        print("The Archive.org server took too long to respond")
        sys.exit(1)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Connection failed")
        print("Could not connect to Archive.org")
        print("Check your network connection")
        sys.exit(1)
        
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error occurred: {e}")
        print("The Archive.org server returned an error")
        sys.exit(1)
        
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Import requests here so error shows if not installed
    import requests
    main()
