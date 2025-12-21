#!/usr/bin/env python3
"""
Demo script showing how to use the rate-limited API client.
"""

import sys
import os
import time

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.rate_limiter import ArchiveAPIClient


def demo_usage():
    """Demonstrate using the rate-limited API client."""
    
    print("Archive.org API Client Demo")
    print("="*60)
    
    # Create client with 2 requests per second
    client = ArchiveAPIClient(requests_per_second=2, max_retries=3)
    
    # Search for shows
    print("\n1. Searching for Cornell '77...")
    try:
        results = client.search(
            query='collection:GratefulDead AND date:1977-05-08',
            fields='identifier,title,venue,avg_rating',
            rows=5
        )
        
        print(f"Found {results['response']['numFound']} shows")
        for doc in results['response']['docs']:
            print(f"  - {doc.get('identifier')}")
            print(f"    {doc.get('title', 'N/A')}")
            print(f"    Rating: {doc.get('avg_rating', 'N/A')}")
            
    except Exception as e:
        print(f"Search failed: {str(e)}")
    
    # Get metadata for a show
    print("\n2. Getting metadata for a show...")
    try:
        identifier = "gd1977-05-08.sbd.hicks.4982.sbeok.shnf"
        metadata = client.get_metadata(identifier)
        
        print(f"Show: {metadata['metadata'].get('title', 'N/A')}")
        print(f"Date: {metadata['metadata'].get('date', 'N/A')}")
        print(f"Venue: {metadata['metadata'].get('venue', 'N/A')}")
        print(f"Source: {metadata['metadata'].get('source', 'N/A')}")
        
    except Exception as e:
        print(f"Metadata fetch failed: {str(e)}")
    
    # Make multiple requests to show rate limiting in action
    print("\n3. Making 5 rapid searches (rate limiting active)...")
    print("Notice the delay between requests...")
    start_time = time.time()
    
    for i in range(5):
        try:
            results = client.search(
                query=f'collection:GratefulDead AND year:197{i}',
                rows=1
            )
            print(f"  Request {i+1}: Success ({results['response']['numFound']} shows)")
        except Exception as e:
            print(f"  Request {i+1}: Failed - {str(e)}")
    
    elapsed = time.time() - start_time
    print(f"\n5 requests completed in {elapsed:.2f}s")
    print(f"Average: {elapsed/5:.2f}s per request (includes rate limiting delay)")
    print(f"Expected: ~2.5s with 2 req/s limit (0.5s per request)")
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("\nKey points:")
    print("- Requests are automatically spaced out")
    print("- Retries happen automatically on errors")
    print("- User-Agent header identifies our app")
    print("- This is production-ready code!")


if __name__ == '__main__':
    demo_usage()
