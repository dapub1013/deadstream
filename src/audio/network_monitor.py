#!/usr/bin/env python3
"""
Network Monitor for DeadStream Audio Player

This module provides network connectivity monitoring and intelligent
retry logic for handling network interruptions during audio streaming.

Features:
- Periodic connectivity checks
- Connection state tracking
- Automatic reconnection with exponential backoff
- Integration with VLC media player

Author: DeadStream Project
Phase: 4.6 - Network Interruption Handling
"""

import socket
import time
import threading
from enum import Enum
from typing import Optional, Callable
from datetime import datetime, timedelta


class ConnectionState(Enum):
    """Network connection states"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"
    UNKNOWN = "unknown"


class NetworkMonitor:
    """
    Monitors network connectivity and provides automatic recovery.
    
    Usage:
        monitor = NetworkMonitor()
        monitor.on_state_change = handle_state_change
        monitor.start()
        
        # Later...
        if monitor.is_connected():
            # Safe to stream
            pass
    """
    
    def __init__(self, check_interval=5.0):
        """
        Initialize network monitor.
        
        Args:
            check_interval: Seconds between connectivity checks (default: 5.0)
        """
        self.check_interval = check_interval
        self.state = ConnectionState.UNKNOWN
        self.last_check_time = None
        self.consecutive_failures = 0
        
        # Callback for state changes
        self.on_state_change: Optional[Callable[[ConnectionState], None]] = None
        
        # Monitoring thread
        self._monitor_thread = None
        self._stop_monitoring = threading.Event()
        self._running = False
    
    def is_connected(self) -> bool:
        """
        Check if we currently have network connectivity.
        
        Returns:
            True if connected, False otherwise
        """
        return self.state == ConnectionState.CONNECTED
    
    def check_connectivity(self, timeout=3.0) -> bool:
        """
        Perform a single connectivity check.
        
        We test connectivity by attempting to connect to Archive.org's server.
        This is more reliable than ping (which may be blocked) and tests the
        actual service we need.
        
        Args:
            timeout: Connection timeout in seconds
            
        Returns:
            True if we can reach Archive.org, False otherwise
        """
        self.last_check_time = datetime.now()
        
        try:
            # Try to connect to Archive.org's HTTPS port
            # Use socket instead of HTTP to avoid overhead
            sock = socket.create_connection(
                ("archive.org", 443),
                timeout=timeout
            )
            sock.close()
            return True
            
        except (socket.timeout, socket.error, OSError):
            return False
    
    def _update_state(self, new_state: ConnectionState):
        """
        Update connection state and notify listeners.
        
        Args:
            new_state: New connection state
        """
        if new_state != self.state:
            old_state = self.state
            self.state = new_state
            
            print(f"Network state change: {old_state.value} -> {new_state.value}")
            
            # Notify callback if registered
            if self.on_state_change:
                try:
                    self.on_state_change(new_state)
                except Exception as e:
                    print(f"Error in state change callback: {e}")
    
    def _monitor_loop(self):
        """Main monitoring loop (runs in background thread)"""
        print(f"Network monitoring started (check interval: {self.check_interval}s)")
        
        while not self._stop_monitoring.is_set():
            # Check connectivity
            is_connected = self.check_connectivity()
            
            if is_connected:
                # Connection successful
                self.consecutive_failures = 0
                
                if self.state != ConnectionState.CONNECTED:
                    self._update_state(ConnectionState.CONNECTED)
            else:
                # Connection failed
                self.consecutive_failures += 1
                
                if self.state == ConnectionState.CONNECTED:
                    # Just lost connection
                    print(f"Network connection lost (failure {self.consecutive_failures})")
                    self._update_state(ConnectionState.DISCONNECTED)
                elif self.state == ConnectionState.RECONNECTING:
                    # Still trying to reconnect
                    print(f"Reconnection attempt failed (failure {self.consecutive_failures})")
                else:
                    # Was already disconnected
                    pass
            
            # Wait before next check
            self._stop_monitoring.wait(self.check_interval)
        
        print("Network monitoring stopped")
    
    def start(self):
        """Start background network monitoring"""
        if self._running:
            print("Network monitoring already running")
            return
        
        self._stop_monitoring.clear()
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True,
            name="NetworkMonitor"
        )
        self._monitor_thread.start()
        self._running = True
    
    def stop(self):
        """Stop background network monitoring"""
        if not self._running:
            return
        
        print("Stopping network monitoring...")
        self._stop_monitoring.set()
        
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
        
        self._running = False
    
    def get_status_string(self) -> str:
        """
        Get human-readable status string.
        
        Returns:
            Status description for display to user
        """
        if self.state == ConnectionState.CONNECTED:
            return "Connected"
        elif self.state == ConnectionState.DISCONNECTED:
            return f"Disconnected (checking...)"
        elif self.state == ConnectionState.RECONNECTING:
            return f"Reconnecting (attempt {self.consecutive_failures})..."
        else:
            return "Unknown"


class RetryStrategy:
    """
    Implements exponential backoff retry strategy for failed operations.
    
    Usage:
        retry = RetryStrategy()
        
        while retry.should_retry():
            try:
                # Attempt operation
                success = do_something()
                if success:
                    retry.reset()
                    break
            except Exception as e:
                retry.record_failure()
                time.sleep(retry.get_wait_time())
    """
    
    def __init__(self, max_retries=5, base_delay=1.0, max_delay=30.0):
        """
        Initialize retry strategy.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Initial delay between retries (seconds)
            max_delay: Maximum delay between retries (seconds)
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        
        self.attempt = 0
        self.last_attempt_time = None
    
    def should_retry(self) -> bool:
        """Check if we should attempt another retry"""
        return self.attempt < self.max_retries
    
    def record_failure(self):
        """Record a failed attempt"""
        self.attempt += 1
        self.last_attempt_time = datetime.now()
    
    def get_wait_time(self) -> float:
        """
        Calculate wait time before next retry using exponential backoff.
        
        Returns:
            Seconds to wait before next attempt
        """
        # Exponential backoff: base_delay * 2^attempt
        delay = self.base_delay * (2 ** self.attempt)
        
        # Cap at max_delay
        return min(delay, self.max_delay)
    
    def reset(self):
        """Reset retry counter after successful operation"""
        self.attempt = 0
        self.last_attempt_time = None
    
    def get_status_string(self) -> str:
        """Get human-readable status"""
        if self.attempt == 0:
            return "Ready"
        elif self.should_retry():
            return f"Retry {self.attempt}/{self.max_retries} (next in {self.get_wait_time():.1f}s)"
        else:
            return f"Max retries exceeded ({self.max_retries})"


# Example usage and testing
if __name__ == '__main__':
    import sys
    
    print("Network Monitor Test")
    print("=" * 60)
    
    def on_state_change(new_state):
        """Callback for state changes"""
        print(f">>> State changed to: {new_state.value}")
    
    # Create monitor
    monitor = NetworkMonitor(check_interval=3.0)
    monitor.on_state_change = on_state_change
    
    # Start monitoring
    monitor.start()
    
    try:
        # Monitor for 30 seconds
        print("\nMonitoring network for 30 seconds...")
        print("Try disconnecting/reconnecting your network to test\n")
        
        for i in range(30):
            print(f"[{i+1:2d}s] Status: {monitor.get_status_string()}")
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    
    finally:
        print("\nStopping monitor...")
        monitor.stop()
        print("Test complete")
    
    # Test retry strategy
    print("\n" + "=" * 60)
    print("Retry Strategy Test")
    print("=" * 60)
    
    retry = RetryStrategy(max_retries=5, base_delay=1.0)
    
    print("\nSimulating failed retries:")
    while retry.should_retry():
        print(f"Attempt {retry.attempt + 1}: {retry.get_status_string()}")
        retry.record_failure()
        
        if retry.should_retry():
            wait = retry.get_wait_time()
            print(f"  Waiting {wait:.1f}s before next retry...")
            time.sleep(wait)
    
    print(f"\nFinal status: {retry.get_status_string()}")
