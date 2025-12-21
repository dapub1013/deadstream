#!/usr/bin/env python3
"""
Rate-limited request wrapper for Internet Archive API.
Implements polite request patterns and automatic retry logic.
"""

import requests
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple rate limiter using token bucket algorithm.
    Ensures we don't exceed specified requests per second.
    """
    
    def __init__(self, requests_per_second=2):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_second: Maximum requests per second (default: 2)
        """
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
    
    def wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            logger.debug(f"Rate limiting: waiting {sleep_time:.3f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()


class ArchiveAPIClient:
    """
    Internet Archive API client with built-in rate limiting and retry logic.
    """
    
    def __init__(self, requests_per_second=2, max_retries=3):
        """
        Initialize API client.
        
        Args:
            requests_per_second: Rate limit (default: 2 req/s)
            max_retries: Maximum retry attempts (default: 3)
        """
        self.rate_limiter = RateLimiter(requests_per_second)
        self.max_retries = max_retries
        self.session = requests.Session()
        
        # Set a user-agent to identify our application
        self.session.headers.update({
            'User-Agent': 'DeadStream/1.0 (Grateful Dead Concert Player; Educational Project)'
        })
    
    def request(self, url, params=None, timeout=10):
        """
        Make a rate-limited request with retry logic.
        
        Args:
            url: API endpoint URL
            params: Query parameters
            timeout: Request timeout in seconds
            
        Returns:
            requests.Response object
            
        Raises:
            requests.exceptions.RequestException: If all retries fail
        """
        
        for attempt in range(self.max_retries):
            try:
                # Wait to respect rate limit
                self.rate_limiter.wait_if_needed()
                
                # Make the request
                logger.info(f"Making request to {url} (attempt {attempt + 1}/{self.max_retries})")
                response = self.session.get(url, params=params, timeout=timeout)
                
                # Check for rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited! Waiting {retry_after}s before retry")
                    time.sleep(retry_after)
                    continue
                
                # Check for service unavailable
                if response.status_code == 503:
                    wait_time = 5 * (attempt + 1)  # Exponential backoff
                    logger.warning(f"Service unavailable. Waiting {wait_time}s before retry")
                    time.sleep(wait_time)
                    continue
                
                # Success or other error
                response.raise_for_status()  # Raise exception for 4xx/5xx
                return response
                
            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{self.max_retries})")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2)  # Wait before retry
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2)
        
        raise requests.exceptions.RequestException("Max retries exceeded")
    
    def search(self, query, fields='identifier,title,date,venue', rows=50):
        """
        Search Archive.org with rate limiting.
        
        Args:
            query: Search query string
            fields: Fields to return
            rows: Number of results
            
        Returns:
            dict: JSON response
        """
        url = "https://archive.org/advancedsearch.php"
        params = {
            'q': query,
            'fl': fields,
            'rows': rows,
            'output': 'json'
        }
        
        response = self.request(url, params=params)
        return response.json()
    
    def get_metadata(self, identifier):
        """
        Get metadata for a specific show with rate limiting.
        
        Args:
            identifier: Archive.org identifier
            
        Returns:
            dict: JSON metadata
        """
        url = f"https://archive.org/metadata/{identifier}"
        response = self.request(url)
        return response.json()
