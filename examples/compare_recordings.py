#!/usr/bin/env python3
"""
Recording Comparison Tool

Compare all available recordings for a specific show date.
Shows scoring details and explains selection decisions.

Usage:
    python examples/compare_recordings.py --date 1977-05-08
    python examples/compare_recordings.py --date 1970-02-13 --preset audiophile
    python examples/compare_recordings.py --date 1972-05-11 --weights custom
"""

import sys
import os
import argparse

# Add project root to path
sys.path.insert(0, '/home/david/deadstream')

from src.database.queries import get_show_by_date
from src.api.metadata import get_metadata, extract_audio_files
from src.selection.scoring import RecordingScorer
from src.selection.preferences import PreferenceManager


def format_score_bar(score, width=40):
    """Create a visual bar graph for score (0-100)."""
    filled = int((score / 100) * width)
    empty = width - filled
    return '[' + '#' * filled + '-' * empty + ']'


def print_separator(char='=', width=80):
    """Print a separator line."""
    print(char * width)


def print_recording_details(result, rank=None):
    """
    Print detailed scoring breakdown for one recording.
    
    Args:
        result: Scoring result dict
        rank: Optional rank number (1, 2, 3, etc.)
    """
    if rank:
        print(f"\n[RANK #{rank}] {result['identifier']}")
    else:
        print(f"\n{result['identifier']}")
    
    print_separator('-')
    
    # Total score with visual bar
    total = result['total_score']
    bar = format_score_bar(total)
    print(f"TOTAL SCORE: {total:6.2f}/100 {bar}")
    
    # Component scores
    print("\nComponent Scores:")
    print(f"  Source Type:       {result['source_score']:6.2f}/100")
    print(f"  Format Quality:    {result['format_score']:6.2f}/100")
    print(f"  Community Rating:  {result['rating_score']:6.2f}/100")
    print(f"  Lineage:           {result['lineage_score']:6.2f}/100")
    print(f"  Taper:             {result['taper_score']:6.2f}/100")


def compare_show_recordings(date, preference_manager=None):
    """
    Compare all recordings for a specific show date.
    
    Args:
        date: Show date in YYYY-MM-DD format
        preference_manager: Optional PreferenceManager for custom weights
        
    Returns:
        List of scored recordings (sorted best to worst)
    """
    # Get all recordings for this date
    shows = get_show_by_date(date)
    
    if not shows:
        print(f"[ERROR] No shows found for {date}")
        return []
    
    print(f"[INFO] Found {len(shows)} recording(s) for {date}")
    print_separator()
    
    # Initialize scorer
    scorer = RecordingScorer(preference_manager=preference_manager)
    
    # Collect metadata and score each recording
    recordings_with_scores = []
    
    for show in shows:
        identifier = show['identifier']
        
        try:
            # Get full metadata from API
            metadata = get_metadata(identifier)
            
            # Extract relevant scoring data
            recording_data = {
                'identifier': identifier,
                'source': show.get('source', metadata.get('source', '')),
                'format': metadata.get('format', ''),
                'avg_rating': show.get('avg_rating'),
                'num_reviews': show.get('num_reviews'),
                'lineage': metadata.get('lineage', ''),
                'taper': metadata.get('taper', '')
            }
            
            # Score the recording
            score_result = scorer.score_recording(recording_data)
            recordings_with_scores.append(score_result)
            
        except Exception as e:
            print(f"[WARN] Failed to score {identifier}: {e}")
            continue
    
    # Sort by score (best first)
    recordings_with_scores.sort(key=lambda x: x['total_score'], reverse=True)
    
    return recordings_with_scores


def main():
    """Main comparison tool."""
    parser = argparse.ArgumentParser(
        description='Compare all recordings for a specific show date',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Compare Cornell '77 with default weights:
    python examples/compare_recordings.py --date 1977-05-08
  
  Compare with audiophile preset:
    python examples/compare_recordings.py --date 1977-05-08 --preset audiophile
  
  Compare with custom weights from config file:
    python examples/compare_recordings.py --date 1972-05-11 --weights custom
        """
    )
    
    parser.add_argument(
        '--date',
        required=True,
        help='Show date in YYYY-MM-DD format (e.g., 1977-05-08)'
    )
    
    parser.add_argument(
        '--preset',
        choices=['balanced', 'audiophile', 'crowd_favorite'],
        help='Use a preset weighting profile'
    )
    
    parser.add_argument(
        '--weights',
        choices=['default', 'custom'],
        default='default',
        help='Use default weights or custom weights from config file'
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 80)
    print(" DEADSTREAM RECORDING COMPARISON TOOL")
    print("=" * 80)
    print(f"\nAnalyzing recordings for: {args.date}\n")
    
    # Set up preference manager based on arguments
    pm = None
    if args.weights == 'custom' or args.preset:
        pm = PreferenceManager()
        
        if args.preset:
            print(f"[INFO] Using preset: {args.preset}")
            pm.use_preset(args.preset)
        else:
            print("[INFO] Using custom weights from config/preferences.yaml")
        
        pm.display_current_preferences()
    else:
        print("[INFO] Using default scoring weights")
        print_separator()
    
    # Run comparison
    results = compare_show_recordings(args.date, pm)
    
    if not results:
        print("\n[ERROR] No recordings could be scored.")
        return 1
    
    # Display results
    print(f"\n{'=' * 80}")
    print(f" COMPARISON RESULTS ({len(results)} recording(s))")
    print('=' * 80)
    
    for i, result in enumerate(results, 1):
        print_recording_details(result, rank=i)
    
    # Show winner
    print("\n" + "=" * 80)
    winner = results[0]
    print(f"[WINNER] Best recording: {winner['identifier']}")
    print(f"         Score: {winner['total_score']:.2f}/100")
    
    if len(results) > 1:
        second = results[1]
        margin = winner['total_score'] - second['total_score']
        print(f"         Margin over #2: {margin:.2f} points")
    
    print("=" * 80 + "\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
