#!/usr/bin/env python3
"""
Practical Integration Example: Using RecordingScorer with Database

This script demonstrates how Task 5.3's RecordingScorer would integrate
with your existing Phase 3 database and Phase 2 API client to automatically
select the best recording when a user wants to play a show.

NOTE: This is a simulation/demonstration. In your actual implementation,
you would:
1. Import from src.database.queries (Phase 3)
2. Import from src.api.metadata (Phase 2)
3. Import from src.selection.scoring (Phase 5 - Tasks 5.1, 5.2)
"""


# Simulated database query results
def simulate_db_query_by_date(date):
    """
    Simulate Phase 3 database query returning shows for a date.
    In reality, you'd use: from src.database.queries import search_by_date
    """
    # Simulate multiple Cornell '77 recordings in database
    if date == "1977-05-08":
        return [
            {
                'identifier': 'gd1977-05-08.sbd.miller.97065.flac16',
                'date': '1977-05-08',
                'venue': 'Barton Hall, Cornell University',
                'city': 'Ithaca',
                'state': 'NY',
                'avg_rating': 4.90,
                'num_reviews': 142
            },
            {
                'identifier': 'gd77-05-08.sbd.hicks.4982.sbeok.shnf',
                'date': '1977-05-08',
                'venue': 'Barton Hall, Cornell University',
                'city': 'Ithaca',
                'state': 'NY',
                'avg_rating': 4.75,
                'num_reviews': 28
            },
            {
                'identifier': 'gd1977-05-08.aud.wise.24822.sbeok.shnf',
                'date': '1977-05-08',
                'venue': 'Barton Hall, Cornell University',
                'city': 'Ithaca',
                'state': 'NY',
                'avg_rating': 4.20,
                'num_reviews': 15
            }
        ]
    return []


def simulate_api_get_metadata(identifier):
    """
    Simulate Phase 2 API call to get full metadata.
    In reality, you'd use: from src.api.metadata import get_show_metadata
    """
    # Simulate API response with full metadata
    metadata_db = {
        'gd1977-05-08.sbd.miller.97065.flac16': {
            'identifier': 'gd1977-05-08.sbd.miller.97065.flac16',
            'source': 'soundboard',
            'format': 'Flac',
            'taper': 'Charlie Miller',
            'lineage': 'Master Reel > DAT > FLAC',
            'files': [
                {'name': 'track01.flac', 'format': 'Flac'},
                {'name': 'track02.flac', 'format': 'Flac'}
            ]
        },
        'gd77-05-08.sbd.hicks.4982.sbeok.shnf': {
            'identifier': 'gd77-05-08.sbd.hicks.4982.sbeok.shnf',
            'source': 'soundboard',
            'format': 'Shorten',
            'taper': '',
            'lineage': 'Master > Cassette > DAT > SHN',
            'files': [
                {'name': 'track01.shn', 'format': 'Shorten'},
                {'name': 'track02.shn', 'format': 'Shorten'}
            ]
        },
        'gd1977-05-08.aud.wise.24822.sbeok.shnf': {
            'identifier': 'gd1977-05-08.aud.wise.24822.sbeok.shnf',
            'source': 'audience',
            'format': 'Shorten',
            'taper': '',
            'lineage': 'Microphone > Cassette > DAT > SHN',
            'files': [
                {'name': 'track01.shn', 'format': 'Shorten'},
                {'name': 'track02.shn', 'format': 'Shorten'}
            ]
        }
    }
    return metadata_db.get(identifier, {})


# Simplified RecordingScorer (from Tasks 5.1, 5.2)
class RecordingScorer:
    """Simplified version for demonstration."""
    
    DEFAULT_WEIGHTS = {
        'source_type': 0.35,
        'format_quality': 0.25,
        'community_rating': 0.20,
        'lineage': 0.10,
        'taper': 0.10
    }
    
    SOURCE_SCORES = {
        'soundboard': 100, 'sbd': 100,
        'audience': 50, 'aud': 50,
        'unknown': 25
    }
    
    FORMAT_SCORES = {
        'flac': 100, 'shorten': 95,
        'mp3_320': 80, 'mp3_vbr': 75,
        'unknown': 20
    }
    
    TAPER_SCORES = {
        'miller': 100, 'charlie miller': 100,
        'unknown': 50
    }
    
    def __init__(self, weights=None):
        self.weights = weights if weights else self.DEFAULT_WEIGHTS.copy()
    
    def score_recording(self, metadata):
        """Score a single recording."""
        source_score = self._score_source(metadata.get('source', ''))
        format_score = self._score_format(metadata.get('format', ''))
        rating_score = self._score_rating(
            metadata.get('avg_rating'),
            metadata.get('num_reviews')
        )
        lineage_score = 50  # Simplified
        taper_score = self._score_taper(metadata.get('taper', ''))
        
        total = (
            source_score * self.weights['source_type'] +
            format_score * self.weights['format_quality'] +
            rating_score * self.weights['community_rating'] +
            lineage_score * self.weights['lineage'] +
            taper_score * self.weights['taper']
        )
        
        return {
            'total_score': round(total, 2),
            'identifier': metadata.get('identifier', 'unknown')
        }
    
    def _score_source(self, source):
        if not source:
            return self.SOURCE_SCORES['unknown']
        s = source.lower()
        if 'sbd' in s or 'soundboard' in s:
            return self.SOURCE_SCORES['soundboard']
        if 'aud' in s or 'audience' in s:
            return self.SOURCE_SCORES['audience']
        return self.SOURCE_SCORES['unknown']
    
    def _score_format(self, fmt):
        if not fmt:
            return self.FORMAT_SCORES['unknown']
        f = fmt.lower()
        if 'flac' in f:
            return self.FORMAT_SCORES['flac']
        if 'shn' in f or 'shorten' in f:
            return self.FORMAT_SCORES['shorten']
        return self.FORMAT_SCORES['unknown']
    
    def _score_rating(self, avg_rating, num_reviews):
        if avg_rating is None or num_reviews is None:
            return 50
        rating_score = (avg_rating / 5.0) * 100
        confidence = 1.0 if num_reviews >= 20 else 0.9
        return rating_score * confidence + 50 * (1 - confidence)
    
    def _score_taper(self, taper):
        if not taper:
            return self.TAPER_SCORES['unknown']
        t = taper.lower()
        if 'miller' in t:
            return self.TAPER_SCORES['miller']
        return self.TAPER_SCORES['unknown']
    
    def select_best(self, recordings):
        """Select the best recording from a list."""
        if not recordings:
            return None
        
        scored = []
        for rec in recordings:
            score = self.score_recording(rec)
            scored.append(score)
        
        scored.sort(key=lambda x: x['total_score'], reverse=True)
        return scored[0]['identifier']


def demonstrate_smart_selection():
    """
    Demonstrate complete workflow: User wants to play Cornell '77
    """
    print("\n" + "=" * 80)
    print("SMART SHOW SELECTION - COMPLETE WORKFLOW DEMONSTRATION")
    print("=" * 80)
    
    # STEP 1: User wants to play Cornell '77
    print("\n[USER REQUEST] Play Cornell '77 (1977-05-08)")
    print("-" * 80)
    
    # STEP 2: Query database (Phase 3)
    print("\n[STEP 1] Query database for show date...")
    shows = simulate_db_query_by_date("1977-05-08")
    print(f"Found {len(shows)} recordings in database:")
    for show in shows:
        print(f"  - {show['identifier']}")
        print(f"    Rating: {show['avg_rating']} stars ({show['num_reviews']} reviews)")
    
    # STEP 3: Get full metadata for each recording (Phase 2)
    print("\n[STEP 2] Fetch full metadata from Archive.org API...")
    enriched_recordings = []
    for show in shows:
        metadata = simulate_api_get_metadata(show['identifier'])
        # Merge database data with API metadata
        full_metadata = {**show, **metadata}
        enriched_recordings.append(full_metadata)
        print(f"  - {metadata['identifier']}")
        print(f"    Source: {metadata['source']}, Format: {metadata['format']}")
        if metadata.get('taper'):
            print(f"    Taper: {metadata['taper']}")
    
    # STEP 4: Score all recordings (Phase 5 - NEW)
    print("\n[STEP 3] Score all recordings using RecordingScorer...")
    scorer = RecordingScorer()
    
    scored_recordings = []
    for recording in enriched_recordings:
        score_result = scorer.score_recording(recording)
        scored_recordings.append(score_result)
        print(f"  - {score_result['identifier'][:50]}")
        print(f"    Score: {score_result['total_score']}/100")
    
    # STEP 5: Select best recording
    print("\n[STEP 4] Select best recording...")
    best_identifier = scorer.select_best(enriched_recordings)
    print(f"âœ… SELECTED: {best_identifier}")
    
    # STEP 6: Get playback URLs (Phase 2 + Phase 4)
    print("\n[STEP 5] Prepare for playback...")
    best_metadata = simulate_api_get_metadata(best_identifier)
    print(f"Track list:")
    for idx, file in enumerate(best_metadata.get('files', []), 1):
        print(f"  {idx}. {file['name']} ({file['format']})")
    
    print("\n[STEP 6] Ready to play with ResilientAudioPlayer (Phase 4)")
    print("  player.load_url(track_url)")
    print("  player.play()")
    
    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETE - Best recording automatically selected!")
    print("=" * 80)


def demonstrate_user_preferences():
    """
    Demonstrate how user preferences affect selection.
    """
    print("\n" + "=" * 80)
    print("USER PREFERENCES DEMONSTRATION")
    print("=" * 80)
    
    shows = simulate_db_query_by_date("1977-05-08")
    enriched_recordings = []
    for show in shows:
        metadata = simulate_api_get_metadata(show['identifier'])
        enriched_recordings.append({**show, **metadata})
    
    # Default preferences (balanced)
    print("\n[SCENARIO 1] Default balanced preferences:")
    print("  Source: 35%, Format: 25%, Rating: 20%, Lineage: 10%, Taper: 10%")
    default_scorer = RecordingScorer()
    default_best = default_scorer.select_best(enriched_recordings)
    print(f"  Selected: {default_best[:50]}")
    
    # Audiophile preferences (format-focused)
    print("\n[SCENARIO 2] Audiophile preferences (format-focused):")
    print("  Source: 20%, Format: 45%, Rating: 15%, Lineage: 15%, Taper: 5%")
    audiophile_weights = {
        'source_type': 0.20,
        'format_quality': 0.45,
        'community_rating': 0.15,
        'lineage': 0.15,
        'taper': 0.05
    }
    audiophile_scorer = RecordingScorer(weights=audiophile_weights)
    audiophile_best = audiophile_scorer.select_best(enriched_recordings)
    print(f"  Selected: {audiophile_best[:50]}")
    
    # Community-focused preferences
    print("\n[SCENARIO 3] Community-focused preferences:")
    print("  Source: 25%, Format: 15%, Rating: 40%, Lineage: 10%, Taper: 10%")
    community_weights = {
        'source_type': 0.25,
        'format_quality': 0.15,
        'community_rating': 0.40,
        'lineage': 0.10,
        'taper': 0.10
    }
    community_scorer = RecordingScorer(weights=community_weights)
    community_best = community_scorer.select_best(enriched_recordings)
    print(f"  Selected: {community_best[:50]}")
    
    print("\n" + "=" * 80)
    print("All three preferences selected the same recording!")
    print("(Miller SBD FLAC is universally superior for Cornell '77)")
    print("=" * 80)


def main():
    """Run demonstrations."""
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + "  TASK 5.3: PRACTICAL INTEGRATION DEMONSTRATION".center(78) + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    
    print("\nThis demonstrates how the RecordingScorer integrates with:")
    print("  - Phase 3: Database queries")
    print("  - Phase 2: Archive.org API metadata")
    print("  - Phase 5: Smart selection scoring")
    print("  - Phase 4: Playback (next step)")
    
    demonstrate_smart_selection()
    demonstrate_user_preferences()
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("\n1. Task 5.4: Implement user preferences system")
    print("   - Create preference configuration file")
    print("   - Save/load user custom weights")
    print("   - Provide preset profiles")
    print("\n2. Task 5.5: Add manual override option")
    print("   - Allow user to see all versions")
    print("   - Let user pick manually if desired")
    print("\n3. Task 5.6: Create comparison tool")
    print("   - Show side-by-side comparison")
    print("   - Display scores for each recording")
    print("   - Help users understand selection logic")


if __name__ == '__main__':
    main()
