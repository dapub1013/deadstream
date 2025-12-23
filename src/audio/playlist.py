"""
Playlist builder for Grateful Dead shows.

This module parses Internet Archive metadata to create structured playlists
with automatic set detection (Set I, Set II, Encore).
"""

import re
from typing import List, Dict, Optional, Tuple


class Track:
    """Represents a single track in a show."""
    
    def __init__(self, filename: str, title: str, duration: float, 
                 track_number: int, set_name: str, url: str):
        self.filename = filename
        self.title = title
        self.duration = duration  # in seconds
        self.track_number = track_number
        self.set_name = set_name  # "Set I", "Set II", "Encore", etc.
        self.url = url
    
    def __repr__(self):
        return f"Track({self.track_number}: {self.title} [{self.set_name}])"


class Playlist:
    """Represents a complete show playlist with sets."""
    
    def __init__(self, identifier: str, date: str, venue: str):
        self.identifier = identifier
        self.date = date
        self.venue = venue
        self.tracks: List[Track] = []
        self._current_index = 0
    
    def add_track(self, track: Track):
        """Add a track to the playlist."""
        self.tracks.append(track)
    
    def get_track(self, index: int) -> Optional[Track]:
        """Get a specific track by index."""
        if 0 <= index < len(self.tracks):
            return self.tracks[index]
        return None
    
    def get_current_track(self) -> Optional[Track]:
        """Get the currently selected track."""
        return self.get_track(self._current_index)
    
    def next_track(self) -> Optional[Track]:
        """Move to next track and return it."""
        if self._current_index < len(self.tracks) - 1:
            self._current_index += 1
            return self.get_current_track()
        return None
    
    def previous_track(self) -> Optional[Track]:
        """Move to previous track and return it."""
        if self._current_index > 0:
            self._current_index -= 1
            return self.get_current_track()
        return None
    
    def jump_to_track(self, index: int) -> Optional[Track]:
        """Jump to a specific track index."""
        if 0 <= index < len(self.tracks):
            self._current_index = index
            return self.get_current_track()
        return None
    
    def get_sets(self) -> Dict[str, List[Track]]:
        """Group tracks by set name."""
        sets = {}
        for track in self.tracks:
            if track.set_name not in sets:
                sets[track.set_name] = []
            sets[track.set_name].append(track)
        return sets
    
    def get_total_duration(self) -> float:
        """Get total duration of all tracks in seconds."""
        return sum(track.duration for track in self.tracks)
    
    def __len__(self):
        return len(self.tracks)
    
    def __repr__(self):
        return f"Playlist({self.identifier}: {len(self.tracks)} tracks)"


class PlaylistBuilder:
    """Builds playlists from Archive.org metadata."""
    
    # Common set patterns in filenames
    SET_PATTERNS = [
        (r'd1t', 'Set I'),      # d1t01 = disc 1, track 01
        (r'd2t', 'Set II'),     # d2t01 = disc 2, track 01
        (r'd3t', 'Encore'),     # d3t01 = disc 3, track 01 (usually encore)
        (r'_set1_', 'Set I'),
        (r'_set2_', 'Set II'),
        (r'_encore', 'Encore'),
        (r'_e_', 'Encore'),
    ]
    
    # Patterns to extract track numbers
    TRACK_NUMBER_PATTERNS = [
        r't(\d+)',           # t01, t02, etc.
        r'track(\d+)',       # track01
        r'_(\d+)_',          # _01_, _02_
        r'-(\d+)\.',         # -01.mp3
    ]
    
    @staticmethod
    def detect_set(filename: str) -> str:
        """
        Detect which set a track belongs to based on filename.
        
        Args:
            filename: Audio file name (e.g., "gd77-05-08d1t01.mp3")
            
        Returns:
            Set name (e.g., "Set I", "Set II", "Encore")
        """
        filename_lower = filename.lower()
        
        for pattern, set_name in PlaylistBuilder.SET_PATTERNS:
            if re.search(pattern, filename_lower):
                return set_name
        
        # Default to Set I if no pattern matches
        return 'Set I'
    
    @staticmethod
    def extract_track_number(filename: str) -> int:
        """
        Extract track number from filename.
        
        Args:
            filename: Audio file name
            
        Returns:
            Track number (1-based), or 0 if not found
        """
        for pattern in PlaylistBuilder.TRACK_NUMBER_PATTERNS:
            match = re.search(pattern, filename.lower())
            if match:
                try:
                    return int(match.group(1))
                except (ValueError, IndexError):
                    continue
        
        return 0
    
    @staticmethod
    def clean_title(filename: str) -> str:
        """
        Clean up filename to create readable track title.
        
        Args:
            filename: Audio file name
            
        Returns:
            Cleaned title string
        """
        # Remove file extension
        title = re.sub(r'\.(mp3|flac|ogg)$', '', filename, flags=re.IGNORECASE)
        
        # Remove common prefixes (identifier patterns)
        title = re.sub(r'^gd\d{2}-\d{2}-\d{2}', '', title)
        
        # Remove disc/track notation
        title = re.sub(r'd\d+t\d+', '', title)
        
        # Remove underscores and hyphens at start/end
        title = title.strip('_-')
        
        # Replace underscores with spaces
        title = title.replace('_', ' ')
        
        # Capitalize words
        title = ' '.join(word.capitalize() for word in title.split())
        
        return title if title else filename
    
    @staticmethod
    def build_from_metadata(metadata: dict) -> Playlist:
        """
        Build a playlist from Archive.org metadata.
        
        Args:
            metadata: Dictionary from API metadata call
            
        Returns:
            Playlist object with all tracks
            
        Example metadata structure:
        {
            'metadata': {
                'identifier': 'gd77-05-08.sbd...',
                'date': '1977-05-08',
                'venue': 'Barton Hall, Cornell University'
            },
            'files': [
                {
                    'name': 'gd77-05-08d1t01.mp3',
                    'format': 'VBR MP3',
                    'length': '685.12'  # seconds
                },
                ...
            ]
        }
        """
        # Extract show information
        metadata_dict = metadata.get('metadata', {})
        identifier = metadata_dict.get('identifier', 'unknown')
        date = metadata_dict.get('date', 'unknown')
        venue = metadata_dict.get('venue', 'Unknown Venue')
        
        # Create playlist
        playlist = Playlist(identifier, date, venue)
        
        # Get audio files
        files = metadata.get('files', [])
        audio_files = []
        
        # Filter for audio files (MP3, FLAC, OGG)
        for file_info in files:
            file_format = file_info.get('format', '').upper()
            if any(fmt in file_format for fmt in ['MP3', 'FLAC', 'OGG', 'VORBIS']):
                # Skip derivative files (like 64kb MP3 versions)
                filename = file_info.get('name', '')
                if '64kb' not in filename.lower() and '_vbr' not in filename.lower():
                    audio_files.append(file_info)
        
        # Sort files by name (usually gives correct track order)
        audio_files.sort(key=lambda x: x.get('name', ''))
        
        # Build tracks
        for file_info in audio_files:
            filename = file_info.get('name', '')
            
            # Skip non-audio or derivative files
            if not filename:
                continue
            
            # Build streaming URL
            url = f"https://archive.org/download/{identifier}/{filename}"
            
            # Extract track information
            track_number = PlaylistBuilder.extract_track_number(filename)
            set_name = PlaylistBuilder.detect_set(filename)
            title = PlaylistBuilder.clean_title(filename)
            
            # Parse duration (may be string or float)
            duration_str = file_info.get('length', '0')
            try:
                duration = float(duration_str)
            except (ValueError, TypeError):
                duration = 0.0
            
            # Create track
            track = Track(
                filename=filename,
                title=title,
                duration=duration,
                track_number=track_number,
                set_name=set_name,
                url=url
            )
            
            playlist.add_track(track)
        
        return playlist
    
    @staticmethod
    def build_from_identifier(identifier: str, api_client) -> Playlist:
        """
        Build playlist by fetching metadata from Archive.org.
        
        Args:
            identifier: Show identifier
            api_client: ArchiveAPIClient instance (from Phase 2)
            
        Returns:
            Playlist object
        """
        from src.api.metadata import get_metadata
        
        # Fetch metadata
        metadata = get_metadata(identifier)
        
        # Build playlist
        return PlaylistBuilder.build_from_metadata(metadata)


# Example usage and testing functions
def example_usage():
    """
    Example of how to use the playlist builder.
    
    This would typically be called with real metadata from the API.
    """
    # Example metadata (simplified)
    metadata = {
        'metadata': {
            'identifier': 'gd77-05-08.sbd.hicks.4982.sbeok.shnf',
            'date': '1977-05-08',
            'venue': 'Barton Hall, Cornell University'
        },
        'files': [
            {
                'name': 'gd77-05-08d1t01.mp3',
                'format': 'VBR MP3',
                'length': '685.12'
            },
            {
                'name': 'gd77-05-08d1t02.mp3',
                'format': 'VBR MP3',
                'length': '512.34'
            },
            {
                'name': 'gd77-05-08d2t01.mp3',
                'format': 'VBR MP3',
                'length': '789.56'
            }
        ]
    }
    
    # Build playlist
    playlist = PlaylistBuilder.build_from_metadata(metadata)
    
    # Display playlist information
    print(f"\n{playlist}")
    print(f"Show: {playlist.date} - {playlist.venue}")
    print(f"Total tracks: {len(playlist)}")
    print(f"Total duration: {playlist.get_total_duration():.0f} seconds")
    
    # Show tracks by set
    print("\nTracks by set:")
    sets = playlist.get_sets()
    for set_name in sorted(sets.keys()):
        print(f"\n{set_name}:")
        for track in sets[set_name]:
            mins = int(track.duration // 60)
            secs = int(track.duration % 60)
            print(f"  {track.track_number:2d}. {track.title} ({mins}:{secs:02d})")
            print(f"      URL: {track.url}")


if __name__ == '__main__':
    # Run example
    example_usage()
    
    # Test set detection
    print("\n" + "="*60)
    print("Set Detection Tests:")
    print("="*60)
    
    test_files = [
        'gd77-05-08d1t01.mp3',
        'gd77-05-08d2t03.mp3',
        'gd77-05-08d3t01.mp3',
        'show_set1_track01.mp3',
        'show_set2_track05.mp3',
        'show_encore_01.mp3',
    ]
    
    for filename in test_files:
        set_name = PlaylistBuilder.detect_set(filename)
        track_num = PlaylistBuilder.extract_track_number(filename)
        title = PlaylistBuilder.clean_title(filename)
        print(f"{filename:30s} → {set_name:10s} Track {track_num:2d}: {title}")
