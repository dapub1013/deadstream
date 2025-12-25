#!/usr/bin/env python3
"""
Manual Recording Selection and Override

Provides interface for both automatic and manual recording selection.
Allows users to explicitly choose a specific recording instead of 
relying on automatic smart selection.

Usage:
    from src.selection.override import RecordingSelector
    
    selector = RecordingSelector()
    
    # Automatic selection
    best = selector.select_automatically('1977-05-08')
    
    # Manual selection
    chosen = selector.select_manually('gd1977-05-08.sbd.miller.86248.flac16')
    
    # With optional override
    result = selector.select_with_override('1977-05-08', 
                                           manual_identifier='specific.id')
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.database.queries import get_shows_by_date
from src.api.metadata import get_metadata, extract_audio_files
from src.selection.scoring import RecordingScorer
from typing import List, Dict, Optional


class RecordingSelector:
    """
    Handles both automatic and manual recording selection.
    
    Provides interface for:
    - Automatic selection (using RecordingScorer)
    - Manual selection (user chooses specific identifier)
    - Listing all available recordings for a show
    """
    
    def __init__(self, scorer=None):
        """
        Initialize selector.
        
        Args:
            scorer: Optional RecordingScorer instance. If None, creates default.
        """
        self.scorer = scorer if scorer else RecordingScorer()
    
    def list_recordings_for_show(self, date: str) -> List[Dict]:
        """
        Get all available recordings for a specific show date.
        
        Args:
            date: Show date in YYYY-MM-DD format
        
        Returns:
            List of recording metadata dicts, each containing:
            - identifier
            - date
            - venue
            - avg_rating
            - num_reviews
            - (plus score information if automatic scoring applied)
        """
        # Get all recordings for this date from database
        recordings = get_shows_by_date(date)
        
        if not recordings:
            print(f"[INFO] No recordings found for {date}")
            return []
        
        print(f"[INFO] Found {len(recordings)} recording(s) for {date}")
        return recordings
    
    def select_automatically(self, date: str) -> Optional[str]:
        """
        Use smart selection to choose best recording for a show.
        
        Args:
            date: Show date in YYYY-MM-DD format
        
        Returns:
            Identifier of best recording, or None if no recordings found
        """
        recordings = self.list_recordings_for_show(date)
        
        if not recordings:
            return None
        
        # If only one recording, return it
        if len(recordings) == 1:
            identifier = recordings[0]['identifier']
            print(f"[INFO] Only one recording available: {identifier}")
            return identifier
        
        # Use scorer to select best
        print(f"[INFO] Analyzing {len(recordings)} recordings...")
        best_identifier = self.scorer.select_best(recordings)
        
        if best_identifier:
            print(f"[INFO] Automatic selection: {best_identifier}")
        
        return best_identifier
    
    def select_manually(self, identifier: str) -> Optional[str]:
        """
        Manually select a specific recording by identifier.
        
        Validates that the recording exists and has playable audio.
        
        Args:
            identifier: Archive.org identifier (e.g., 'gd1977-05-08.sbd.miller.86248.flac16')
        
        Returns:
            The identifier if valid and playable, None otherwise
        """
        print(f"[INFO] Manual selection: {identifier}")
        
        # Validate recording exists and has audio
        try:
            metadata = get_metadata(identifier)
            audio_files = extract_audio_files(metadata)
            
            if not audio_files:
                print(f"[ERROR] Recording {identifier} has no playable audio files")
                return None
            
            print(f"[PASS] Recording validated: {len(audio_files)} audio file(s)")
            return identifier
            
        except Exception as e:
            print(f"[ERROR] Failed to validate recording {identifier}: {e}")
            return None
    
    def select_with_override(self, date: str, manual_identifier: Optional[str] = None) -> Optional[str]:
        """
        Select recording with optional manual override.
        
        If manual_identifier provided, use it (after validation).
        Otherwise, use automatic selection.
        
        This is the primary method to use in application code.
        
        Args:
            date: Show date in YYYY-MM-DD format
            manual_identifier: Optional specific identifier to use
        
        Returns:
            Selected identifier, or None if selection failed
        """
        if manual_identifier:
            # Manual override requested
            return self.select_manually(manual_identifier)
        else:
            # Automatic selection
            return self.select_automatically(date)
    
    def display_recordings(self, date: str, show_scores: bool = False) -> None:
        """
        Display all available recordings for a show in readable format.
        
        Args:
            date: Show date in YYYY-MM-DD format
            show_scores: If True, display automatic scores for each recording
        """
        recordings = self.list_recordings_for_show(date)
        
        if not recordings:
            print(f"\n[INFO] No recordings found for {date}")
            return
        
        print(f"\n{'='*70}")
        print(f"Available Recordings for {date}")
        print(f"{'='*70}")
        
        if show_scores and len(recordings) > 1:
            # Score all recordings
            scored = self.scorer.compare_recordings(recordings)
            
            for i, rec in enumerate(scored, 1):
                print(f"\n{i}. {rec['identifier']}")
                print(f"   Score: {rec['total_score']:.1f}/100")
                
                # Show breakdown
                print(f"   Source:    {rec['scores']['source']:.1f} "
                      f"(weight: {self.scorer.weights['source_type']:.0%})")
                print(f"   Format:    {rec['scores']['format']:.1f} "
                      f"(weight: {self.scorer.weights['format_quality']:.0%})")
                print(f"   Rating:    {rec['scores']['rating']:.1f} "
                      f"(weight: {self.scorer.weights['community_rating']:.0%})")
                print(f"   Lineage:   {rec['scores']['lineage']:.1f} "
                      f"(weight: {self.scorer.weights['lineage']:.0%})")
                print(f"   Taper:     {rec['scores']['taper']:.1f} "
                      f"(weight: {self.scorer.weights['taper']:.0%})")
                
                # Show metadata
                if 'venue' in rec and rec['venue']:
                    print(f"   Venue: {rec['venue']}")
                if 'avg_rating' in rec and rec['avg_rating']:
                    print(f"   Rating: {rec['avg_rating']:.1f} "
                          f"({rec.get('num_reviews', 0)} reviews)")
        else:
            # Simple list without scores
            for i, rec in enumerate(recordings, 1):
                print(f"\n{i}. {rec['identifier']}")
                if 'venue' in rec and rec['venue']:
                    print(f"   Venue: {rec['venue']}")
                if 'avg_rating' in rec and rec['avg_rating']:
                    print(f"   Rating: {rec['avg_rating']:.1f} "
                          f"({rec.get('num_reviews', 0)} reviews)")
        
        print(f"\n{'='*70}")
