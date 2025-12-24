#!/usr/bin/env python3
"""
Phase 5.1: Analyze Recording Quality Indicators

This script examines shows with multiple recordings to identify
quality indicators we can use for smart selection.

Learning goals:
- Understand what metadata is available
- Identify patterns in high-quality recordings
- Build foundation for scoring algorithm
"""

import sys
sys.path.insert(0, '/home/david/deadstream')

from src.database.queries import get_show_by_date
from src.api.metadata import get_metadata
import time


def analyze_show_date(date):
    """
    Analyze all recordings available for a specific date.
    
    Returns dict with analysis results.
    """
    print(f"\n{'='*70}")
    print(f"Analyzing recordings for: {date}")
    print(f"{'='*70}\n")
    
    # Get all recordings for this date
    shows = get_show_by_date(date)
    
    if not shows:
        print("[INFO] No recordings found for this date")
        return None
    
    print(f"Found {len(shows)} recording(s) for this date:\n")
    
    recordings = []
    
    for i, show in enumerate(shows, 1):
        print(f"Recording #{i}: {show['identifier']}")
        print(f"  Venue: {show['venue']}")
        print(f"  Rating: {show['avg_rating']} ({show['num_reviews']} reviews)")
        
        # Get full metadata
        try:
            metadata = get_metadata(show['identifier'])
            time.sleep(0.5)  # Rate limiting
            
            # Extract quality indicators
            indicators = extract_quality_indicators(metadata)
            
            # Display indicators
            print(f"  Source: {indicators['source_type']}")
            print(f"  Taper: {indicators['taper']}")
            print(f"  Lineage: {indicators['lineage'][:80]}..." if len(indicators['lineage']) > 80 else f"  Lineage: {indicators['lineage']}")
            print(f"  Audio formats: {', '.join(indicators['formats'])}")
            print(f"  Has FLAC: {indicators['has_flac']}")
            print(f"  Description length: {indicators['desc_length']} chars")
            print("")
            
            recordings.append({
                'show': show,
                'indicators': indicators
            })
            
        except Exception as e:
            print(f"  [ERROR] Could not fetch metadata: {e}\n")
            continue
    
    return {
        'date': date,
        'count': len(recordings),
        'recordings': recordings
    }


def extract_quality_indicators(metadata):
    """
    Extract all possible quality indicators from metadata.
    
    This is the key function - identifies what data we have available
    to score recordings.
    """
    indicators = {
        'source_type': 'unknown',
        'taper': 'unknown',
        'lineage': '',
        'formats': [],
        'has_flac': False,
        'has_mp3': False,
        'desc_length': 0,
        'transferer': 'unknown'
    }
    
    # Source type (soundboard, audience, matrix)
    source = metadata.get('source', '').lower()
    identifier = metadata.get('identifier', '').lower()
    
    if 'sbd' in identifier or 'soundboard' in source:
        indicators['source_type'] = 'soundboard'
    elif 'matrix' in identifier or 'matrix' in source:
        indicators['source_type'] = 'matrix'
    elif 'aud' in identifier or 'audience' in source:
        indicators['source_type'] = 'audience'
    
    # Taper information
    taper = metadata.get('taper', '')
    if taper:
        indicators['taper'] = taper
    
    # Lineage (recording chain)
    lineage = metadata.get('lineage', '')
    if lineage:
        indicators['lineage'] = lineage
    
    # Transferer
    transferer = metadata.get('transferer', '')
    if transferer:
        indicators['transferer'] = transferer
    
    # Description length (detailed descriptions often indicate quality)
    description = metadata.get('description', '')
    if description:
        indicators['desc_length'] = len(description)
    
    # Available formats
    files = metadata.get('files', [])
    formats_found = set()
    
    for file_info in files:
        format_name = file_info.get('format', '').lower()
        
        if 'flac' in format_name:
            indicators['has_flac'] = True
            formats_found.add('FLAC')
        elif 'vbr mp3' in format_name or 'mp3' in format_name:
            indicators['has_mp3'] = True
            formats_found.add('MP3')
        elif 'ogg' in format_name:
            formats_found.add('OGG')
    
    indicators['formats'] = sorted(list(formats_found))
    
    return indicators


def analyze_multiple_dates(dates):
    """
    Analyze multiple dates to find patterns.
    """
    print("\n" + "="*70)
    print("RECORDING QUALITY INDICATOR ANALYSIS")
    print("="*70)
    
    all_results = []
    
    for date in dates:
        result = analyze_show_date(date)
        if result:
            all_results.append(result)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY OF FINDINGS")
    print("="*70 + "\n")
    
    total_dates = len(all_results)
    total_recordings = sum(r['count'] for r in all_results)
    
    print(f"Analyzed {total_dates} show dates")
    print(f"Found {total_recordings} total recordings")
    print(f"Average recordings per date: {total_recordings/total_dates:.1f}")
    
    # Count source types
    source_counts = {'soundboard': 0, 'matrix': 0, 'audience': 0, 'unknown': 0}
    flac_count = 0
    
    for result in all_results:
        for rec in result['recordings']:
            source = rec['indicators']['source_type']
            source_counts[source] += 1
            if rec['indicators']['has_flac']:
                flac_count += 1
    
    print(f"\nSource type distribution:")
    print(f"  Soundboard: {source_counts['soundboard']}")
    print(f"  Matrix: {source_counts['matrix']}")
    print(f"  Audience: {source_counts['audience']}")
    print(f"  Unknown: {source_counts['unknown']}")
    
    print(f"\nFormat availability:")
    print(f"  FLAC available: {flac_count}/{total_recordings} ({100*flac_count/total_recordings:.1f}%)")
    
    print("\n" + "="*70)
    print("KEY INDICATORS IDENTIFIED:")
    print("="*70)
    print("""
1. Source Type (identifier/source field)
   - Soundboard (highest quality)
   - Matrix (mixed sources)
   - Audience (variable quality)

2. Community Rating (avg_rating, num_reviews)
   - Already in database
   - Higher ratings = better recordings
   - More reviews = more reliable rating

3. Taper/Transferer Information
   - Known quality tapers (Charlie Miller, etc.)
   - Can use for additional scoring

4. Format Availability
   - FLAC preferred over MP3
   - Indicates quality of preservation

5. Lineage Information
   - Detailed lineage suggests quality preservation
   - Length of lineage description

6. Description Length
   - Detailed descriptions often indicate care taken
   - Can be secondary indicator
""")


def main():
    """
    Analyze famous shows with multiple recordings.
    
    These are well-known shows that likely have many versions.
    """
    
    # Cornell '77 - One of the most famous shows
    dates_to_analyze = [
        '1977-05-08',  # Cornell '77
        '1972-05-11',  # Rotterdam '72
        '1974-05-19',  # Portland '74
    ]
    
    analyze_multiple_dates(dates_to_analyze)
    
    print("\n[SUCCESS] Analysis complete!")
    print("\nNext step: Use these indicators to build scoring function (Task 5.2)")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())