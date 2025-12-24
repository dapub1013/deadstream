#!/usr/bin/env python3
"""
Test the recording scoring system.

Tests scoring logic with various recording scenarios.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.selection.scoring import RecordingScorer


def test_source_type_scoring():
    """Test that source type scores correctly."""
    print("=== Testing Source Type Scoring ===\n")
    
    scorer = RecordingScorer()
    
    test_cases = [
        {'identifier': 'test1', 'source': 'soundboard', 'expected': 100},
        {'identifier': 'test2', 'source': 'SBD', 'expected': 100},
        {'identifier': 'test3', 'source': 'audience', 'expected': 50},
        {'identifier': 'test4', 'source': 'AUD', 'expected': 50},
        {'identifier': 'test5', 'source': 'matrix', 'expected': 75},
        {'identifier': 'test6', 'source': '', 'expected': 25},
    ]
    
    for case in test_cases:
        result = scorer._score_source_type(case['source'])
        status = "âœ"" if result == case['expected'] else "âœ—"
        print(f"{status} Source '{case['source']}': {result} (expected {case['expected']})")
    
    print()


def test_format_scoring():
    """Test that format scores correctly."""
    print("=== Testing Format Scoring ===\n")
    
    scorer = RecordingScorer()
    
    test_cases = [
        {'format': 'Flac', 'expected': 100},
        {'format': 'VBR MP3', 'expected': 75},
        {'format': 'MP3 320kbps', 'expected': 80},
        {'format': 'MP3 128kbps', 'expected': 40},
        {'format': 'Shorten', 'expected': 95},
        {'format': '', 'expected': 20},
    ]
    
    for case in test_cases:
        result = scorer._score_format(case['format'])
        status = "âœ"" if result == case['expected'] else "âœ—"
        print(f"{status} Format '{case['format']}': {result} (expected {case['expected']})")
    
    print()


def test_community_rating():
    """Test community rating scoring."""
    print("=== Testing Community Rating ===\n")
    
    scorer = RecordingScorer()
    
    test_cases = [
        # (avg_rating, num_reviews, description)
        (5.0, 50, "Perfect rating, many reviews"),
        (4.5, 20, "Great rating, good reviews"),
        (3.0, 5, "Average rating, few reviews"),
        (5.0, 1, "Perfect rating, only 1 review"),
        (None, None, "No rating data"),
    ]
    
    for avg_rating, num_reviews, desc in test_cases:
        result = scorer._score_community_rating(avg_rating, num_reviews)
        print(f"{desc}: {result:.2f}")
    
    print()


def test_complete_scoring():
    """Test complete recording scores."""
    print("=== Testing Complete Recording Scoring ===\n")
    
    scorer = RecordingScorer()
    
    # Cornell '77 example - multiple recordings
    recordings = [
        {
            'identifier': 'gd1977-05-08.sbd.miller.97065.flac16',
            'source': 'soundboard',
            'format': 'Flac',
            'avg_rating': 4.9,
            'num_reviews': 85,
            'lineage': 'Master Reel > DAT > FLAC',
            'taper': 'Charlie Miller'
        },
        {
            'identifier': 'gd1977-05-08.aud.unknown.flac',
            'source': 'audience',
            'format': 'Flac',
            'avg_rating': 3.5,
            'num_reviews': 12,
            'lineage': 'Unknown',
            'taper': 'Unknown'
        },
        {
            'identifier': 'gd1977-05-08.sbd.mp3',
            'source': 'soundboard',
            'format': 'MP3 128kbps',
            'avg_rating': 4.0,
            'num_reviews': 5,
            'lineage': 'Unknown',
            'taper': 'Unknown'
        }
    ]
    
    for recording in recordings:
        result = scorer.score_recording(recording)
        print(f"Recording: {recording['identifier']}")
        print(f"  Total Score: {result['total_score']}")
        print(f"  Breakdown:")
        print(f"    Source:  {result['source_score']}")
        print(f"    Format:  {result['format_score']}")
        print(f"    Rating:  {result['rating_score']}")
        print(f"    Lineage: {result['lineage_score']}")
        print(f"    Taper:   {result['taper_score']}")
        print()


def test_best_selection():
    """Test selecting the best recording."""
    print("=== Testing Best Recording Selection ===\n")
    
    scorer = RecordingScorer()
    
    recordings = [
        {
            'identifier': 'aud-flac',
            'source': 'audience',
            'format': 'Flac',
            'avg_rating': 4.5,
            'num_reviews': 20
        },
        {
            'identifier': 'sbd-mp3-128',
            'source': 'soundboard',
            'format': 'MP3 128kbps',
            'avg_rating': 4.0,
            'num_reviews': 10
        },
        {
            'identifier': 'sbd-flac-miller',
            'source': 'soundboard',
            'format': 'Flac',
            'avg_rating': 5.0,
            'num_reviews': 50,
            'taper': 'miller'
        }
    ]
    
    ranked = scorer.compare_recordings(recordings)
    
    print("Rankings:")
    for i, result in enumerate(ranked, 1):
        print(f"{i}. {result['identifier']}: {result['total_score']}")
    
    best = scorer.select_best(recordings)
    print(f"\nBest recording: {best}")
    print()


def test_custom_weights():
    """Test custom weighting preferences."""
    print("=== Testing Custom Weights ===\n")
    
    # User who cares only about source type
    audiophile_weights = {
        'source_type': 0.50,
        'format_quality': 0.30,
        'community_rating': 0.10,
        'lineage': 0.05,
        'taper': 0.05
    }
    
    # User who trusts community ratings most
    community_weights = {
        'source_type': 0.20,
        'format_quality': 0.20,
        'community_rating': 0.40,
        'lineage': 0.10,
        'taper': 0.10
    }
    
    test_recording = {
        'identifier': 'test',
        'source': 'audience',
        'format': 'Flac',
        'avg_rating': 5.0,
        'num_reviews': 100
    }
    
    default_scorer = RecordingScorer()
    audiophile_scorer = RecordingScorer(weights=audiophile_weights)
    community_scorer = RecordingScorer(weights=community_weights)
    
    print(f"Same recording, different preferences:")
    print(f"  Default:   {default_scorer.score_recording(test_recording)['total_score']}")
    print(f"  Audiophile: {audiophile_scorer.score_recording(test_recording)['total_score']}")
    print(f"  Community: {community_scorer.score_recording(test_recording)['total_score']}")
    print()


if __name__ == '__main__':
    print("Testing Recording Scoring System\n")
    print("=" * 50)
    print()
    
    test_source_type_scoring()
    test_format_scoring()
    test_community_rating()
    test_complete_scoring()
    test_best_selection()
    test_custom_weights()
    
    print("=" * 50)
    print("\nAll tests complete!")