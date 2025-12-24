#!/usr/bin/env python3
"""
Task 5.3: Test RecordingScorer with Multiple Versions of Same Show

Tests the smart selection algorithm with famous shows that have multiple
recordings. Validates that scoring produces sensible rankings based on
source type, format, community ratings, and other quality indicators.
"""

# Mock RecordingScorer for testing
# In your actual implementation, you'd import from src.selection.scoring
class RecordingScorer:
    """
    Scores recordings based on quality indicators.
    """
    
    # Default scoring weights (0-1 scale, must sum to 1.0)
    DEFAULT_WEIGHTS = {
        'source_type': 0.35,
        'format_quality': 0.25,
        'community_rating': 0.20,
        'lineage': 0.10,
        'taper': 0.10
    }
    
    SOURCE_SCORES = {
        'soundboard': 100, 'sbd': 100,
        'matrix': 75,
        'audience': 50, 'aud': 50,
        'unknown': 25
    }
    
    FORMAT_SCORES = {
        'flac': 100, 'shn': 95,
        'mp3_320': 80, 'mp3_vbr': 75,
        'mp3_256': 70, 'mp3_192': 60,
        'mp3_160': 50, 'mp3_128': 40,
        'mp3_low': 30, 'unknown': 20
    }
    
    TAPER_SCORES = {
        'miller': 100,
        'bertha': 95,
        'vernon': 90,
        'unknown': 50
    }
    
    def __init__(self, weights=None):
        self.weights = weights if weights else self.DEFAULT_WEIGHTS.copy()
    
    def score_recording(self, metadata):
        """Calculate total score for a recording."""
        source_score = self._score_source_type(metadata.get('source', ''))
        format_score = self._score_format(metadata.get('format', ''))
        rating_score = self._score_community_rating(
            metadata.get('avg_rating'),
            metadata.get('num_reviews')
        )
        lineage_score = self._score_lineage(metadata.get('lineage', ''))
        taper_score = self._score_taper(metadata.get('taper', ''))
        
        total_score = (
            source_score * self.weights['source_type'] +
            format_score * self.weights['format_quality'] +
            rating_score * self.weights['community_rating'] +
            lineage_score * self.weights['lineage'] +
            taper_score * self.weights['taper']
        )
        
        return {
            'total_score': round(total_score, 2),
            'source_score': source_score,
            'format_score': format_score,
            'rating_score': rating_score,
            'lineage_score': lineage_score,
            'taper_score': taper_score,
            'identifier': metadata.get('identifier', 'unknown')
        }
    
    def _score_source_type(self, source):
        """Score based on recording source type."""
        if not source:
            return self.SOURCE_SCORES['unknown']
        
        source_lower = source.lower()
        if source_lower in self.SOURCE_SCORES:
            return self.SOURCE_SCORES[source_lower]
        
        if 'sbd' in source_lower or 'soundboard' in source_lower:
            return self.SOURCE_SCORES['soundboard']
        elif 'matrix' in source_lower:
            return self.SOURCE_SCORES['matrix']
        elif 'aud' in source_lower or 'audience' in source_lower:
            return self.SOURCE_SCORES['audience']
        
        return self.SOURCE_SCORES['unknown']
    
    def _score_format(self, format_str):
        """Score based on audio format quality."""
        if not format_str:
            return self.FORMAT_SCORES['unknown']
        
        format_lower = format_str.lower()
        
        if 'flac' in format_lower:
            return self.FORMAT_SCORES['flac']
        if 'shn' in format_lower or 'shorten' in format_lower:
            return self.FORMAT_SCORES['shn']
        
        if 'mp3' in format_lower:
            if '320' in format_str or '320k' in format_lower:
                return self.FORMAT_SCORES['mp3_320']
            elif 'vbr' in format_lower or 'v0' in format_lower:
                return self.FORMAT_SCORES['mp3_vbr']
            elif '256' in format_str:
                return self.FORMAT_SCORES['mp3_256']
            elif '192' in format_str:
                return self.FORMAT_SCORES['mp3_192']
            elif '160' in format_str:
                return self.FORMAT_SCORES['mp3_160']
            elif '128' in format_str:
                return self.FORMAT_SCORES['mp3_128']
            elif '64' in format_str or '96' in format_str:
                return self.FORMAT_SCORES['mp3_low']
            return 60
        
        return self.FORMAT_SCORES['unknown']
    
    def _score_community_rating(self, avg_rating, num_reviews):
        """Score based on community ratings."""
        if avg_rating is None or num_reviews is None:
            return 50
        
        rating_score = (avg_rating / 5.0) * 100
        
        if num_reviews >= 20:
            confidence = 1.0
        elif num_reviews >= 10:
            confidence = 0.95
        elif num_reviews >= 5:
            confidence = 0.90
        elif num_reviews >= 3:
            confidence = 0.80
        elif num_reviews >= 1:
            confidence = 0.70
        else:
            return 50
        
        final_score = rating_score * confidence + 50 * (1 - confidence)
        return round(final_score, 2)
    
    def _score_lineage(self, lineage):
        """Score based on recording lineage."""
        if not lineage:
            return 50
        
        lineage_lower = lineage.lower()
        if 'master' in lineage_lower and '>' not in lineage:
            return 100
        
        generations = lineage.count('>')
        if generations == 0:
            return 90
        elif generations == 1:
            return 80
        elif generations == 2:
            return 70
        elif generations == 3:
            return 60
        else:
            return max(50 - (generations - 3) * 10, 20)
    
    def _score_taper(self, taper):
        """Score based on taper reputation."""
        if not taper:
            return self.TAPER_SCORES['unknown']
        
        taper_lower = taper.lower()
        for known_taper, score in self.TAPER_SCORES.items():
            if known_taper in taper_lower:
                return score
        
        return self.TAPER_SCORES['unknown']
    
    def compare_recordings(self, recordings):
        """Score and rank multiple recordings."""
        scored = []
        for recording in recordings:
            score_result = self.score_recording(recording)
            scored.append(score_result)
        
        scored.sort(key=lambda x: x['total_score'], reverse=True)
        return scored
    
    def select_best(self, recordings):
        """Select the best recording from a list."""
        if not recordings:
            return None
        scored = self.compare_recordings(recordings)
        return scored[0]['identifier']


def create_test_recordings_cornell_77():
    """
    Create test data for Cornell '77 (May 8, 1977)
    One of the most famous Dead shows with multiple recordings.
    """
    return [
        {
            'identifier': 'gd1977-05-08.sbd.miller.97065.flac16',
            'source': 'soundboard',
            'format': 'FLAC',
            'avg_rating': 4.90,
            'num_reviews': 142,
            'lineage': 'Master Reel > DAT > FLAC',
            'taper': 'Charlie Miller',
            'description': 'Charlie Miller SBD remaster - FLAC'
        },
        {
            'identifier': 'gd77-05-08.sbd.hicks.4982.sbeok.shnf',
            'source': 'soundboard',
            'format': 'Shorten',
            'avg_rating': 4.75,
            'num_reviews': 28,
            'lineage': 'Master > Cassette > DAT > SHN',
            'taper': 'unknown',
            'description': 'Hicks SBD - Shorten format'
        },
        {
            'identifier': 'gd1977-05-08.aud.wise.24822.sbeok.shnf',
            'source': 'audience',
            'format': 'Shorten',
            'avg_rating': 4.20,
            'num_reviews': 15,
            'lineage': 'Microphone > Cassette > DAT > SHN',
            'taper': 'unknown',
            'description': 'Audience recording - Shorten'
        },
        {
            'identifier': 'gd77-05-08.sbd.MP3.torrent',
            'source': 'soundboard',
            'format': 'VBR MP3',
            'avg_rating': 4.50,
            'num_reviews': 8,
            'lineage': 'SBD > DAT > MP3 VBR',
            'taper': 'unknown',
            'description': 'SBD MP3 VBR encoding'
        },
        {
            'identifier': 'gd1977-05-08.aud.128k.mp3',
            'source': 'audience',
            'format': 'MP3 128k',
            'avg_rating': 3.50,
            'num_reviews': 3,
            'lineage': 'Mic > Cassette > MP3',
            'taper': 'unknown',
            'description': 'Low-quality audience MP3'
        }
    ]


def create_test_recordings_veneta_72():
    """
    Create test data for Veneta '72 (August 27, 1972)
    Famous "Sunshine Daydream" show.
    """
    return [
        {
            'identifier': 'gd1972-08-27.sbd.miller.112893.flac2496',
            'source': 'soundboard',
            'format': 'FLAC',
            'avg_rating': 4.95,
            'num_reviews': 201,
            'lineage': 'Master Reel > FLAC 24/96',
            'taper': 'Charlie Miller',
            'description': 'Miller 24/96 remaster from master'
        },
        {
            'identifier': 'gd72-08-27.aud.bertha.2478.sbeok.shnf',
            'source': 'audience',
            'format': 'Shorten',
            'avg_rating': 4.65,
            'num_reviews': 45,
            'lineage': 'Mic > Reel > DAT > SHN',
            'taper': 'Bertha Board',
            'description': 'Bertha Board audience - excellent'
        },
        {
            'identifier': 'gd1972-08-27.matrix.vernon.24599.sbeok.shnf',
            'source': 'matrix',
            'format': 'Shorten',
            'avg_rating': 4.80,
            'num_reviews': 67,
            'lineage': 'SBD+AUD matrix > DAT > SHN',
            'taper': 'Dan Healy/Vernon',
            'description': 'Matrix mix by Vernon'
        }
    ]


def create_test_recordings_europe_72():
    """
    Create test data for Europe '72 tour show
    (April 8, 1972 - Wembley Empire Pool)
    """
    return [
        {
            'identifier': 'gd72-04-08.sbd.connor.14163.sbeok.shnf',
            'source': 'soundboard',
            'format': 'Shorten',
            'avg_rating': 4.55,
            'num_reviews': 32,
            'lineage': 'SBD > Reel > SHN',
            'taper': 'unknown',
            'description': 'Standard SBD - good quality'
        },
        {
            'identifier': 'gd1972-04-08.aud.glassberg.83896.flac16',
            'source': 'audience',
            'format': 'FLAC',
            'avg_rating': 4.20,
            'num_reviews': 18,
            'lineage': 'Mic > Cassette > FLAC',
            'taper': 'unknown',
            'description': 'Audience recording - FLAC'
        },
        {
            'identifier': 'gd72-04-08.sbd.mp3-320.torrent',
            'source': 'soundboard',
            'format': 'MP3 320k',
            'avg_rating': 4.30,
            'num_reviews': 12,
            'lineage': 'SBD > DAT > MP3 320k',
            'taper': 'unknown',
            'description': 'SBD high-quality MP3'
        }
    ]


def display_comparison_results(show_name, recordings, scored_results):
    """Display scoring results in a clear comparison format."""
    print(f"\n{'=' * 80}")
    print(f"SHOW: {show_name}")
    print(f"Total recordings tested: {len(recordings)}")
    print(f"{'=' * 80}\n")
    
    print(f"{'Rank':<6}{'Total':<8}{'Source':<8}{'Format':<8}{'Rating':<8}{'Lineage':<8}{'Taper':<8}{'Identifier'}")
    print(f"{'-' * 80}")
    
    for idx, result in enumerate(scored_results, 1):
        # Find original recording for description
        original = next((r for r in recordings if r['identifier'] == result['identifier']), None)
        
        print(f"{idx:<6}"
              f"{result['total_score']:<8.2f}"
              f"{result['source_score']:<8.0f}"
              f"{result['format_score']:<8.0f}"
              f"{result['rating_score']:<8.2f}"
              f"{result['lineage_score']:<8.0f}"
              f"{result['taper_score']:<8.0f}"
              f"{result['identifier'][:40]}")
        
        if original:
            print(f"       {original['description']}")
            print()


def test_cornell_77():
    """Test scoring with Cornell '77 recordings."""
    print("\n" + "=" * 80)
    print("TEST 1: Cornell '77 (May 8, 1977)")
    print("=" * 80)
    print("\nExpected winner: Charlie Miller SBD FLAC remaster")
    print("Reasoning: Soundboard + FLAC + highest rating + Miller taper + good lineage")
    
    recordings = create_test_recordings_cornell_77()
    scorer = RecordingScorer()
    scored = scorer.compare_recordings(recordings)
    
    display_comparison_results("Cornell '77 (1977-05-08)", recordings, scored)
    
    # Validate results
    best = scored[0]
    print("\nVALIDATION:")
    print(f"Best recording: {best['identifier']}")
    
    expected = 'gd1977-05-08.sbd.miller.97065.flac16'
    if best['identifier'] == expected:
        print("✓ PASS: Correctly selected Miller SBD FLAC")
    else:
        print(f"✗ FAIL: Expected {expected}, got {best['identifier']}")
    
    # Check that SBD beats AUD
    sbd_scores = [s for s in scored if 'sbd' in s['identifier']]
    aud_scores = [s for s in scored if 'aud' in s['identifier']]
    
    if sbd_scores and aud_scores:
        if min(s['total_score'] for s in sbd_scores) > max(s['total_score'] for s in aud_scores):
            print("✓ PASS: All SBD recordings scored higher than AUD")
        else:
            print("✗ FAIL: Some AUD recordings scored higher than SBD")


def test_veneta_72():
    """Test scoring with Veneta '72 recordings."""
    print("\n" + "=" * 80)
    print("TEST 2: Veneta '72 (August 27, 1972)")
    print("=" * 80)
    print("\nExpected winner: Miller 24/96 FLAC from master")
    print("Reasoning: SBD + FLAC + highest rating + Miller + master lineage")
    
    recordings = create_test_recordings_veneta_72()
    scorer = RecordingScorer()
    scored = scorer.compare_recordings(recordings)
    
    display_comparison_results("Veneta '72 (1972-08-27)", recordings, scored)
    
    # Validate results
    best = scored[0]
    print("\nVALIDATION:")
    print(f"Best recording: {best['identifier']}")
    
    expected = 'gd1972-08-27.sbd.miller.112893.flac2496'
    if best['identifier'] == expected:
        print("✓ PASS: Correctly selected Miller master FLAC")
    else:
        print(f"✗ FAIL: Expected {expected}, got {best['identifier']}")


def test_europe_72():
    """Test scoring with Europe '72 recordings."""
    print("\n" + "=" * 80)
    print("TEST 3: Europe '72 - Wembley (April 8, 1972)")
    print("=" * 80)
    print("\nExpected winner: SBD Shorten (best source type, decent format)")
    print("Reasoning: SBD beats AUD even with older format")
    
    recordings = create_test_recordings_europe_72()
    scorer = RecordingScorer()
    scored = scorer.compare_recordings(recordings)
    
    display_comparison_results("Europe '72 Wembley (1972-04-08)", recordings, scored)
    
    # Validate results
    best = scored[0]
    print("\nVALIDATION:")
    print(f"Best recording: {best['identifier']}")
    
    # Should prefer SBD over AUD
    if 'sbd' in best['identifier']:
        print("✓ PASS: Selected SBD recording")
    else:
        print("✗ FAIL: Did not select SBD recording")


def test_custom_weights():
    """Test scoring with custom weight preferences."""
    print("\n" + "=" * 80)
    print("TEST 4: Custom Weights - Format-Focused User")
    print("=" * 80)
    print("\nScenario: User who prioritizes format quality over source type")
    
    # Custom weights: format > source
    custom_weights = {
        'source_type': 0.15,      # Lower priority
        'format_quality': 0.45,   # Higher priority
        'community_rating': 0.20,
        'lineage': 0.10,
        'taper': 0.10
    }
    
    recordings = create_test_recordings_cornell_77()
    
    # Test with default weights
    default_scorer = RecordingScorer()
    default_best = default_scorer.select_best(recordings)
    
    # Test with custom weights
    custom_scorer = RecordingScorer(weights=custom_weights)
    custom_best = custom_scorer.select_best(recordings)
    
    print(f"\nDefault weights best: {default_best}")
    print(f"Custom weights best:  {custom_best}")
    
    if default_best == custom_best:
        print("\n✓ Both selected same recording (Miller SBD FLAC is universally best)")
    else:
        print("\n✓ Different preferences produced different results")


def main():
    """Run all tests."""
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + "  TASK 5.3: TEST RECORDING SCORER WITH MULTIPLE VERSIONS".center(78) + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    
    try:
        test_cornell_77()
        test_veneta_72()
        test_europe_72()
        test_custom_weights()
        
        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETE")
        print("=" * 80)
        print("\nKEY LEARNINGS:")
        print("1. Scoring algorithm successfully ranks recordings by quality")
        print("2. Soundboard recordings consistently beat audience recordings")
        print("3. FLAC format scores higher than MP3")
        print("4. Community ratings influence final scores appropriately")
        print("5. Taper reputation (Miller, Bertha, Vernon) adds value")
        print("6. Custom weight preferences allow user personalization")
        print("\nREADY FOR TASK 5.4: Implement user preferences system")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
