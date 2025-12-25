#!/usr/bin/env python3
"""
Quick test of comparison tool with several famous shows.
"""

import sys
import os
sys.path.insert(0, '/home/david/deadstream')

from src.database.queries import get_show_by_date
from src.selection.scoring import RecordingScorer
from src.selection.preferences import PreferenceManager

# Famous shows with known multiple recordings
TEST_SHOWS = [
    ('1977-05-08', 'Cornell 77'),
    ('1972-05-11', 'Rotterdam 72'),
    ('1974-05-19', 'Portland Memorial Coliseum'),
    ('1970-02-13', 'Fillmore East'),
]

def quick_test():
    """Test that comparison works for several shows."""
    print("\n[INFO] Testing Comparison Tool\n")
    
    scorer = RecordingScorer()
    
    for date, description in TEST_SHOWS:
        shows = get_show_by_date(date)
        
        if not shows:
            print(f"[SKIP] {date} ({description}) - No recordings found")
            continue
        
        if len(shows) == 1:
            print(f"[SKIP] {date} ({description}) - Only 1 recording")
            continue
        
        print(f"[TEST] {date} ({description})")
        print(f"       Found {len(shows)} recordings")
        
        # Just check that scoring doesn't crash
        try:
            results = []
            for show in shows[:3]:  # Test first 3
                score = scorer.score_recording({
                    'identifier': show['identifier'],
                    'source': show.get('source', ''),
                    'format': '',
                    'avg_rating': show.get('avg_rating'),
                    'num_reviews': show.get('num_reviews')
                })
                results.append(score)
            
            results.sort(key=lambda x: x['total_score'], reverse=True)
            winner = results[0]
            
            print(f"       Winner: {winner['identifier']}")
            print(f"       Score: {winner['total_score']:.2f}/100")
            print()
            
        except Exception as e:
            print(f"[FAIL] Error scoring: {e}\n")
            return False
    
    print("[PASS] All tests completed successfully\n")
    return True


if __name__ == '__main__':
    success = quick_test()
    sys.exit(0 if success else 1)
