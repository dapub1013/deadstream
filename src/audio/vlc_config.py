#!/usr/bin/env python3
"""
Platform-Aware VLC Configuration - Phase 9.8

This module provides VLC instance creation that automatically adapts
to the host platform (macOS for development, Linux for production).

Features:
- Automatic platform detection
- macOS: Auto-detect audio output
- Linux (RPi): Force ALSA audio output
- Consistent streaming settings across platforms
- Debug mode for troubleshooting

Usage:
    from src.audio.vlc_config import create_vlc_instance
    
    instance = create_vlc_instance()
    player = instance.media_player_new()

Author: DeadStream Project
Phase: 9.8 - Cross-Platform Development
"""

import vlc
import platform


def get_platform_type():
    """
    Detect the current platform
    
    Returns:
        str: 'macos', 'linux', or 'other'
    """
    system = platform.system()
    
    if system == 'Darwin':
        return 'macos'
    elif system == 'Linux':
        return 'linux'
    else:
        return 'other'


def create_vlc_instance(debug=False):
    """
    Create a VLC instance with platform-appropriate configuration
    
    Args:
        debug: If True, enable verbose output for troubleshooting
        
    Returns:
        vlc.Instance: Configured VLC instance
        
    Platform-Specific Behavior:
        macOS (Development):
            - No explicit audio output (VLC auto-detects)
            - Uses default CoreAudio output
            - Works with Mac speakers/headphones
            
        Linux (Raspberry Pi Production):
            - Forces ALSA audio output (--aout=alsa)
            - Required for headphone jack on Pi
            - Verified working configuration
            
        Common Settings:
            - No video output (--no-video)
            - 8-second network buffer for streaming
            - Quiet mode (unless debug=True)
    """
    platform_type = get_platform_type()
    
    # Base arguments common to all platforms
    args = [
        '--no-video',            # Audio only
        '--network-caching=8000' # 8 second buffer for streaming
    ]
    
    # Platform-specific audio configuration
    if platform_type == 'linux':
        # Raspberry Pi / Linux
        # MUST use ALSA for headphone jack to work
        args.insert(0, '--aout=alsa')
        if debug:
            print("[INFO] Platform: Linux (Raspberry Pi)")
            print("[INFO] Audio output: ALSA")
    
    elif platform_type == 'macos':
        # macOS Development
        # VLC auto-detects CoreAudio
        if debug:
            print("[INFO] Platform: macOS")
            print("[INFO] Audio output: Auto-detect (CoreAudio)")
    
    else:
        # Unknown platform
        if debug:
            print(f"[WARN] Platform: Unknown ({platform.system()})")
            print("[INFO] Audio output: Auto-detect")
    
    # Debug/quiet mode
    if debug:
        args.append('--verbose=2')
    else:
        args.extend(['--quiet', '--verbose=0'])
    
    # Create and return instance
    instance = vlc.Instance(*args)
    
    if debug:
        print(f"[INFO] VLC instance created with args: {args}")
    
    return instance


def get_platform_info():
    """
    Get detailed platform information
    
    Returns:
        dict: Platform details for debugging
    """
    return {
        'system': platform.system(),
        'release': platform.release(),
        'machine': platform.machine(),
        'platform_type': get_platform_type()
    }


if __name__ == '__main__':
    # Show platform detection when run directly
    print("=" * 60)
    print("VLC Platform Configuration Test")
    print("=" * 60)
    
    info = get_platform_info()
    print(f"\nPlatform Detection:")
    print(f"  System: {info['system']}")
    print(f"  Release: {info['release']}")
    print(f"  Machine: {info['machine']}")
    print(f"  Type: {info['platform_type']}")
    
    print("\nCreating VLC instance (debug mode)...")
    instance = create_vlc_instance(debug=True)
    
    print("\n[PASS] VLC instance created successfully")
    print("\nThis instance is ready to use for audio playback.")
    print("On macOS: Will use your Mac's speakers/headphones")
    print("On Linux: Will use ALSA (Raspberry Pi headphone jack)")
