#!/usr/bin/env python3
"""
Interactive Volume Control Demo - Phase 4.7

This interactive script lets you test volume control manually
while playing a live stream from Archive.org.

Controls:
    +/=  : Volume up 5%
    -    : Volume down 5%
    m    : Toggle mute
    0-9  : Set volume to 0%, 10%, 20%, ... 90%
    q    : Quit

Usage:
    python examples/demo_volume_interactive.py
"""

import sys
import time
import threading

# Add project to path
sys.path.insert(0, '/home/david/deadstream')

from src.audio.resilient_player import ResilientPlayer, format_time
from examples.get_test_url import get_test_url


class VolumeDemo:
    """Interactive volume control demo"""
    
    def __init__(self):
        self.player = ResilientPlayer()
        self.running = False
        
    def display_help(self):
        """Show keyboard controls"""
        print("\n" + "="*70)
        print("VOLUME CONTROL DEMO - Keyboard Controls")
        print("="*70)
        print("  +/=  : Volume up 5%")
        print("  -    : Volume down 5%")
        print("  m    : Toggle mute")
        print("  0-9  : Set volume to 0%, 10%, 20%, ... 90%")
        print("  s    : Show status")
        print("  h    : Show this help")
        print("  q    : Quit")
        print("="*70)
    
    def display_status(self):
        """Display current playback and volume status"""
        volume = self.player.get_volume()
        muted = self.player.get_mute()
        position = self.player.get_position()
        duration = self.player.get_duration()
        state = self.player.get_state()
        
        mute_indicator = "[MUTED]" if muted else ""
        
        print(f"\n--- Status {mute_indicator} ---")
        print(f"Volume: {volume}%")
        print(f"Position: {format_time(position)} / {format_time(duration)}")
        print(f"State: {state.name}")
        print("-" * 30)
    
    def status_monitor(self):
        """Background thread to show periodic status"""
        while self.running:
            time.sleep(10)
            if self.running:
                self.display_status()
    
    def run(self):
        """Run the interactive demo"""
        print("\n" + "="*70)
        print("DEADSTREAM - INTERACTIVE VOLUME CONTROL DEMO")
        print("="*70)
        
        # Get test URL
        print("\n[INFO] Getting test URL from database...")
        test_url = get_test_url(verbose=False)
        
        if not test_url:
            print("[ERROR] Could not get test URL")
            print("Make sure your database is populated (Phase 3)")
            return 1
        
        print(f"[INFO] Test URL: {test_url[:60]}...")
        
        # Load and play
        print("\n[INFO] Loading audio...")
        if not self.player.load_url(test_url):
            print("[ERROR] Failed to load URL")
            return 1
        
        print("[INFO] Starting playback...")
        if not self.player.play():
            print("[ERROR] Failed to start playback")
            return 1
        
        # Wait for buffering
        print("[INFO] Buffering (3 seconds)...")
        time.sleep(3)
        
        # Show initial status
        self.display_help()
        self.display_status()
        
        # Start status monitor
        self.running = True
        monitor_thread = threading.Thread(target=self.status_monitor, daemon=True)
        monitor_thread.start()
        
        # Main command loop
        print("\nEnter commands (h for help):")
        
        try:
            while True:
                # Get command
                command = input("> ").strip().lower()
                
                if not command:
                    continue
                
                # Process command
                if command == 'q':
                    print("[INFO] Quitting...")
                    break
                
                elif command == 'h':
                    self.display_help()
                
                elif command == 's':
                    self.display_status()
                
                elif command in ('+', '='):
                    new_vol = self.player.volume_up(5)
                    print(f"[INFO] Volume: {new_vol}%")
                
                elif command == '-':
                    new_vol = self.player.volume_down(5)
                    print(f"[INFO] Volume: {new_vol}%")
                
                elif command == 'm':
                    muted = self.player.toggle_mute()
                    status = "MUTED" if muted else "UNMUTED"
                    print(f"[INFO] Audio {status}")
                
                elif command.isdigit():
                    # Set volume to 0%, 10%, 20%, etc.
                    digit = int(command)
                    volume = digit * 10
                    self.player.set_volume(volume)
                    print(f"[INFO] Volume: {volume}%")
                
                else:
                    print(f"[WARN] Unknown command: {command}")
                    print("Type 'h' for help")
        
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user")
        
        except EOFError:
            print("\n[INFO] EOF received")
        
        finally:
            # Clean up
            self.running = False
            print("\n[INFO] Stopping playback...")
            self.player.stop()
            self.player.cleanup()
            print("[INFO] Done!")
        
        return 0


def main():
    """Main entry point"""
    demo = VolumeDemo()
    return demo.run()


if __name__ == '__main__':
    sys.exit(main())
