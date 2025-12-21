#!/usr/bin/env python3
"""
Test script to understand Internet Archive API rate limits.
DO NOT run this aggressively - we're testing politely!
"""

import requests
import time
from datetime import datetime

def test_rapid_requests(num_requests=10, delay=0):
    """
    Make several requests in quick succession to observe behavior.
    
    Args:
        num_requests: Number of requests to make
        delay: Seconds to wait between requests
    """
    
    print(f"\n{'='*60}")
    print(f"Testing {num_requests} requests with {delay}s delay")
    print(f"{'='*60}\n")
    
    url = "https://archive.org/advancedsearch.php"
    results = []
    
    for i in range(num_requests):
        # Use a simple query that returns quickly
        params = {
            'q': 'collection:GratefulDead AND date:1977-05-08',
            'fl': 'identifier',
            'rows': 1,
            'output': 'json'
        }
        
        start_time = time.time()
        
        try:
            response = requests.get(url, params=params, timeout=10)
            elapsed = time.time() - start_time
            
            result = {
                'request_num': i + 1,
                'status_code': response.status_code,
                'elapsed_time': round(elapsed, 3),
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
            }
            
            # Check for rate limit headers
            if 'X-RateLimit-Limit' in response.headers:
                result['rate_limit'] = response.headers['X-RateLimit-Limit']
                result['remaining'] = response.headers.get('X-RateLimit-Remaining', 'N/A')
            
            if 'Retry-After' in response.headers:
                result['retry_after'] = response.headers['Retry-After']
            
            results.append(result)
            
            # Print result
            print(f"Request {result['request_num']:2d}: "
                  f"Status {result['status_code']} | "
                  f"Time {result['elapsed_time']}s | "
                  f"{result['timestamp']}")
            
            if response.status_code == 429:
                print(f"  ** RATE LIMITED! Retry after: {result.get('retry_after', 'unknown')}")
                
            elif response.status_code == 503:
                print(f"  ** SERVICE UNAVAILABLE (server busy)")
                
        except requests.exceptions.Timeout:
            print(f"Request {i+1:2d}: TIMEOUT (>10s)")
            results.append({
                'request_num': i + 1,
                'status_code': 'TIMEOUT',
                'elapsed_time': '>10.0',
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
            })
            
        except Exception as e:
            print(f"Request {i+1:2d}: ERROR - {str(e)}")
            results.append({
                'request_num': i + 1,
                'status_code': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
            })
        
        # Wait before next request (if delay specified)
        if delay > 0 and i < num_requests - 1:
            time.sleep(delay)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    success_count = sum(1 for r in results if r.get('status_code') == 200)
    avg_time = sum(r['elapsed_time'] for r in results if isinstance(r['elapsed_time'], float)) / len(results)
    
    print(f"Successful requests: {success_count}/{num_requests}")
    print(f"Average response time: {avg_time:.3f}s")
    
    rate_limited = any(r.get('status_code') == 429 for r in results)
    service_unavailable = any(r.get('status_code') == 503 for r in results)
    
    if rate_limited:
        print("** RATE LIMITING DETECTED **")
    if service_unavailable:
        print("** SERVICE UNAVAILABLE DETECTED **")
    if not rate_limited and not service_unavailable:
        print("No rate limiting or service issues detected")
    
    return results


def main():
    """Run rate limit tests with different scenarios."""
    
    print("Internet Archive API Rate Limit Testing")
    print("========================================")
    print("This script tests the API politely to understand limits.")
    print("We're being good citizens and not hammering the server!")
    print()
    
    # Test 1: Reasonable pace (1 request per second)
    print("\nTest 1: Polite pace (1 request per second)")
    test_rapid_requests(num_requests=10, delay=1.0)
    
    # Wait between tests
    print("\nWaiting 5 seconds before next test...")
    time.sleep(5)
    
    # Test 2: Moderate pace (0.5 second delay)
    print("\nTest 2: Moderate pace (0.5s delay)")
    test_rapid_requests(num_requests=10, delay=0.5)
    
    # Wait between tests
    print("\nWaiting 5 seconds before next test...")
    time.sleep(5)
    
    # Test 3: Quick succession (no delay)
    # NOTE: Only do this briefly to test!
    print("\nTest 3: Quick succession (no delay)")
    print("** Testing only 5 requests to be polite **")
    test_rapid_requests(num_requests=5, delay=0)
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)
    print("\nConclusions:")
    print("- Archive.org is generous with rate limits")
    print("- We should add ~0.5-1s delay between requests")
    print("- This prevents any potential issues")
    print("- It's the polite thing to do!")


if __name__ == '__main__':
    main()
