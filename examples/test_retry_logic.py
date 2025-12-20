#!/usr/bin/env python3
"""
Test script to demonstrate retry logic and error handling.

This simulates various failure scenarios to show how the retry
logic works.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.helpers import (
    fetch_with_retry,
    check_network,
    NetworkError,
    APIError,
    print_error
)


def test_successful_request():
    """Test a normal successful request."""
    print("\n" + "=" * 70)
    print("TEST 1: Successful Request")
    print("=" * 70)
    
    try:
        data = fetch_with_retry(
            'https://archive.org/metadata/gd77-05-08.sbd.hicks.4982.sbeok.shnf',
            max_retries=3,
            verbose=True
        )
        print("SUCCESS: Got metadata")
        print(f"  Title: {data.get('metadata', {}).get('title', 'Unknown')}")
    except Exception as e:
        print(f"FAILED: {e}")


def test_invalid_url():
    """Test with an invalid URL (should fail after retries)."""
    print("\n" + "=" * 70)
    print("TEST 2: Invalid URL (Will Retry Then Fail)")
    print("=" * 70)
    
    try:
        data = fetch_with_retry(
            'https://archive.org/metadata/this-does-not-exist-12345',
            max_retries=2,
            initial_delay=0.5,
            verbose=True
        )
        print("FAILED: Should have raised an error")
    except APIError as e:
        print(f"SUCCESS: Correctly raised APIError after retries")
    except Exception as e:
        print(f"UNEXPECTED: {type(e).__name__}: {e}")


def test_network_check():
    """Test network connectivity check."""
    print("\n" + "=" * 70)
    print("TEST 3: Network Connectivity Check")
    print("=" * 70)
    
    if check_network():
        print("SUCCESS: Network is available")
    else:
        print("WARNING: Network is not available")


def test_timeout():
    """Test timeout handling."""
    print("\n" + "=" * 70)
    print("TEST 4: Timeout Handling (Very Short Timeout)")
    print("=" * 70)
    
    try:
        # Use a very short timeout to trigger timeout error
        data = fetch_with_retry(
            'https://archive.org/metadata/gd77-05-08.sbd.hicks.4982.sbeok.shnf',
            timeout=0.001,  # 1 millisecond - will timeout
            max_retries=2,
            initial_delay=0.5,
            verbose=True
        )
        print("FAILED: Should have timed out")
    except (APIError, TimeoutError) as e:
        print(f"SUCCESS: Correctly handled timeout")
    except Exception as e:
        print(f"UNEXPECTED: {type(e).__name__}: {e}")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("RETRY LOGIC AND ERROR HANDLING TESTS")
    print("=" * 70)
    print("\nThese tests demonstrate how the error handling works.")
    print("Some tests are EXPECTED to fail - that's the point!")
    
    # Run tests
    test_successful_request()
    test_invalid_url()
    test_network_check()
    test_timeout()
    
    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETE")
    print("=" * 70)
    print("\nKey Learnings:")
    print("  - Successful requests work normally")
    print("  - Invalid requests retry then fail gracefully")
    print("  - Network connectivity is checked")
    print("  - Timeouts are handled with retries")
    print("  - Exponential backoff prevents hammering the server")


if __name__ == "__main__":
    main()

