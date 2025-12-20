#!/usr/bin/env python3
"""
API Helper Functions with Robust Error Handling

This module provides reusable functions for interacting with the
Internet Archive API with retry logic, exponential backoff, and
comprehensive error handling.

Usage:
    from src.api.helpers import fetch_with_retry, check_network
    
    data = fetch_with_retry('https://archive.org/metadata/...')
    if data:
        # Process data
"""

import requests
import time
import sys
from typing import Optional, Dict, Any


class NetworkError(Exception):
    """Raised when network connectivity is unavailable."""
    pass


class APIError(Exception):
    """Raised when API returns an error."""
    pass


def check_network(test_url='https://archive.org', timeout=5):
    """
    Check if network connectivity is available.
    
    Args:
        test_url (str): URL to test connectivity
        timeout (int): Timeout in seconds
        
    Returns:
        bool: True if network is available, False otherwise
    """
    try:
        response = requests.head(test_url, timeout=timeout)
        return True
    except requests.exceptions.RequestException:
        return False


def fetch_with_retry(url, params=None, max_retries=3, initial_delay=1, 
                     timeout=15, verbose=True):
    """
    Fetch data from URL with retry logic and exponential backoff.
    
    Args:
        url (str): URL to fetch
        params (dict): Query parameters
        max_retries (int): Maximum number of retry attempts
        initial_delay (int): Initial delay in seconds (doubles each retry)
        timeout (int): Request timeout in seconds
        verbose (bool): Print status messages
        
    Returns:
        dict: JSON response data, or None if all retries failed
        
    Raises:
        NetworkError: If network is unavailable
        APIError: If API returns an error after all retries
    """
    delay = initial_delay
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            if verbose and attempt > 0:
                print(f"  Retry attempt {attempt + 1}/{max_retries}...")
            
            response = requests.get(url, params=params, timeout=timeout)
            
            # Check for HTTP errors
            if response.status_code == 429:
                # Rate limited
                if verbose:
                    print(f"  Rate limited (429). Waiting {delay * 2} seconds...")
                time.sleep(delay * 2)
                delay *= 2
                continue
            
            elif response.status_code == 503:
                # Service unavailable
                if verbose:
                    print(f"  Service unavailable (503). Waiting {delay} seconds...")
                time.sleep(delay)
                delay *= 2
                continue
            
            elif response.status_code >= 400:
                # Other HTTP error
                response.raise_for_status()
            
            # Try to parse JSON
            try:
                data = response.json()
                return data
            except ValueError as e:
                if verbose:
                    print(f"  Invalid JSON response")
                last_exception = e
                time.sleep(delay)
                delay *= 2
                continue
        
        except requests.exceptions.Timeout:
            last_exception = TimeoutError(f"Request timed out after {timeout}s")
            if verbose:
                print(f"  Timeout. Waiting {delay} seconds...")
            time.sleep(delay)
            delay *= 2
            continue
        
        except requests.exceptions.ConnectionError as e:
            last_exception = NetworkError("Network connection failed")
            if verbose:
                print(f"  Connection error. Checking network...")
            
            # Check if network is available
            if not check_network():
                raise NetworkError("No network connectivity")
            
            time.sleep(delay)
            delay *= 2
            continue
        
        except requests.exceptions.RequestException as e:
            last_exception = e
            if verbose:
                print(f"  Request failed: {e}")
            time.sleep(delay)
            delay *= 2
            continue
    
    # All retries exhausted
    if verbose:
        print(f"  All {max_retries} attempts failed")
    
    if isinstance(last_exception, NetworkError):
        raise last_exception
    elif last_exception:
        raise APIError(f"API request failed: {last_exception}")
    else:
        raise APIError("API request failed for unknown reason")


def safe_get(data, *keys, default=None):
    """
    Safely navigate nested dictionary with multiple fallback keys.
    
    Args:
        data (dict): Dictionary to navigate
        *keys: Sequence of keys to try
        default: Default value if all keys fail
        
    Returns:
        Value at keys, or default
        
    Examples:
        # Try multiple keys in order
        title = safe_get(show, 'title', 'name', default='Unknown')
        
        # Navigate nested structure
        venue = safe_get(metadata, 'metadata', 'venue', default='Unknown')
    """
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
            if current is None:
                return default
        else:
            return default
    return current if current is not None else default


def validate_identifier(identifier):
    """
    Validate that an identifier looks reasonable.
    
    Args:
        identifier (str): Archive.org identifier
        
    Returns:
        bool: True if valid format, False otherwise
        
    Examples:
        valid: gd77-05-08.sbd.hicks.4982.sbeok.shnf
        invalid: 1977-05-08, gd77, ""
    """
    if not identifier or not isinstance(identifier, str):
        return False
    
    # Basic checks
    if len(identifier) < 10:
        return False
    
    # Should contain letters and numbers
    if not any(c.isalpha() for c in identifier):
        return False
    if not any(c.isdigit() for c in identifier):
        return False
    
    return True


def validate_date(date_string):
    """
    Validate date string format.
    
    Args:
        date_string (str): Date in YYYY-MM-DD format
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not date_string or not isinstance(date_string, str):
        return False
    
    try:
        from datetime import datetime
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def format_error_message(error, context=""):
    """
    Format error message for user display.
    
    Args:
        error (Exception): The error that occurred
        context (str): Additional context about what was being done
        
    Returns:
        str: User-friendly error message
    """
    if isinstance(error, NetworkError):
        msg = "Network Error: Unable to connect to Internet Archive"
        if context:
            msg += f"\n  While: {context}"
        msg += "\n  Please check your internet connection and try again."
        return msg
    
    elif isinstance(error, requests.exceptions.Timeout):
        msg = "Timeout Error: Request took too long"
        if context:
            msg += f"\n  While: {context}"
        msg += "\n  The server may be slow. Try again in a few moments."
        return msg
    
    elif isinstance(error, APIError):
        msg = f"API Error: {str(error)}"
        if context:
            msg += f"\n  While: {context}"
        msg += "\n  This may be a temporary issue. Try again later."
        return msg
    
    elif isinstance(error, ValueError):
        msg = "Data Error: Invalid response from server"
        if context:
            msg += f"\n  While: {context}"
        msg += "\n  The data format may have changed. Please report this issue."
        return msg
    
    else:
        msg = f"Unexpected Error: {type(error).__name__}"
        if context:
            msg += f"\n  While: {context}"
        msg += f"\n  Details: {str(error)}"
        return msg


def print_error(error, context="", exit_code=None):
    """
    Print formatted error message and optionally exit.
    
    Args:
        error (Exception): The error that occurred
        context (str): Additional context
        exit_code (int): If provided, exit with this code after printing
    """
    print("\n" + "=" * 70)
    print("ERROR")
    print("=" * 70)
    print(format_error_message(error, context))
    print("=" * 70 + "\n")
    
    if exit_code is not None:
        sys.exit(exit_code)


# Example usage
if __name__ == "__main__":
    # Test network check
    print("Testing network connectivity...")
    if check_network():
        print("  Network OK")
    else:
        print("  Network FAILED")
    
    # Test fetch with retry
    print("\nTesting fetch with retry...")
    try:
        data = fetch_with_retry(
            'https://archive.org/metadata/gd77-05-08.sbd.hicks.4982.sbeok.shnf',
            verbose=True
        )
        print(f"  Success! Got {len(data)} top-level keys")
    except (NetworkError, APIError) as e:
        print_error(e, "testing fetch_with_retry")
    
    # Test safe_get
    print("\nTesting safe_get...")
    test_data = {'metadata': {'title': 'Test Show', 'venue': None}}
    title = safe_get(test_data, 'metadata', 'title', default='Unknown')
    venue = safe_get(test_data, 'metadata', 'venue', default='Unknown Venue')
    missing = safe_get(test_data, 'metadata', 'nonexistent', default='Default')
    print(f"  Title: {title}")
    print(f"  Venue: {venue}")
    print(f"  Missing: {missing}")
    
    # Test validation
    print("\nTesting validation...")
    print(f"  Valid ID: {validate_identifier('gd77-05-08.sbd.hicks.4982.sbeok.shnf')}")
    print(f"  Invalid ID: {validate_identifier('gd77')}")
    print(f"  Valid date: {validate_date('1977-05-08')}")
    print(f"  Invalid date: {validate_date('05-08-1977')}")
    
    print("\nAll tests complete!")
