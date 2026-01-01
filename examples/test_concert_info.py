#!/usr/bin/env python3
"""
Test Concert Info Widget Integration with Player Screen

This script validates:
- Concert info widget displays correctly
- Show data loads and populates widget
- Track count updates when setlist loads
- Favorite button is present (disabled for Phase 10)
- Visual appearance matches UI spec
- Integration with existing player screen components

Usage:
    python examples/test_concert_info.py

Expected behavior:
- Window opens with player screen
- Concert info displays at top of left panel
- Title: "1977/05/08 Barton Hall, Cornell University"
- Location: "Ithaca, NY"
- Badges: Soundboard, rating, track count
- Setlist displays below concert info
- Favorite button visible but disabled
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from src.ui.screens.player_screen import PlayerScreen


class TestConcertInfo:
    """Test runner for concert info widget"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.screen = None
    
    def run_test(self):
        """Run concert info integration test"""
        print("\n" + "="*70)
        print("DeadStream - Concert Info Widget Integration Test")
        print("="*70)
        
        # Create player screen
        self.screen = PlayerScreen()
        self.screen.setWindowTitle("DeadStream - Concert Info Test (Phase 10.1)")
        self.screen.setGeometry(100, 100, 1280, 720)
        
        # Test show data (Cornell '77)
        test_show = {
            'date': '1977-05-08',
            'venue': 'Barton Hall, Cornell University',
            'city': 'Ithaca',
            'state': 'NY',
            'source': 'Soundboard',
            'avg_rating': 4.8,
            'num_reviews': 234,
            'identifier': 'gd1977-05-08.sbd.hicks.4982.sbeok.shnf'
        }
        
        print("\nTest show data:")
        print(f"  Date:       {test_show['date']}")
        print(f"  Venue:      {test_show['venue']}")
        print(f"  Location:   {test_show['city']}, {test_show['state']}")
        print(f"  Source:     {test_show['source']}")
        print(f"  Rating:     {test_show['avg_rating']}/5.0")
        print(f"  Reviews:    {test_show['num_reviews']}")
        
        print("\n" + "-"*70)
        print("Expected Visual Layout:")
        print("-"*70)
        print("Left Panel (top):")
        print("  +--------------------------------------------------------+")
        print("  | 1977/05/08 Barton Hall, Cornell University   [Heart] |")
        print("  | Ithaca, NY                                            |")
        print("  | [Soundboard] [Star 4.8/5.0] [XX tracks]               |")
        print("  +--------------------------------------------------------+")
        print("  | (Setlist below - scrollable)                          |")
        print("-"*70)
        
        print("\nValidation checklist:")
        print("  [ ] Concert title displays correctly")
        print("  [ ] Location displays correctly")
        print("  [ ] Source badge visible and correct")
        print("  [ ] Rating badge visible with star icon")
        print("  [ ] Track count badge updates when setlist loads")
        print("  [ ] Favorite button visible (gray heart)")
        print("  [ ] Favorite button disabled (Phase 10 limitation)")
        print("  [ ] Visual styling matches Phase 9 widgets")
        print("  [ ] Border between concert info and setlist visible")
        
        print("\n" + "-"*70)
        print("Instructions:")
        print("-"*70)
        print("  1. Window will open showing player screen")
        print("  2. Concert info should appear at top of left panel")
        print("  3. Verify all metadata displays correctly")
        print("  4. Check that visual styling matches specification")
        print("  5. Try clicking favorite button (should be disabled)")
        print("  6. Verify setlist appears below concert info")
        print("  7. Close window when testing complete")
        print("="*70 + "\n")
        
        # Load show (delayed to ensure UI is ready)
        QTimer.singleShot(500, lambda: self.load_and_verify(test_show))
        
        # Show window
        self.screen.show()
        
        # Run application
        return self.app.exec_()
    
    def load_and_verify(self, show_data):
        """Load show and verify concert info widget"""
        print("[INFO] Loading show data into player...")
        
        try:
            # Load show
            self.screen.load_show(show_data)
            
            # Verify concert info widget exists
            if hasattr(self.screen, 'concert_info'):
                print("[OK] Concert info widget found")
                
                # Verify data loaded
                if self.screen.concert_info.concert_title:
                    print(f"[OK] Concert title: {self.screen.concert_info.concert_title}")
                else:
                    print("[WARN] Concert title not set")
                
                if self.screen.concert_info.location:
                    print(f"[OK] Location: {self.screen.concert_info.location}")
                else:
                    print("[WARN] Location not set")
                
                if self.screen.concert_info.source_type:
                    print(f"[OK] Source type: {self.screen.concert_info.source_type}")
                else:
                    print("[WARN] Source type not set")
                
                if self.screen.concert_info.rating > 0:
                    print(f"[OK] Rating: {self.screen.concert_info.rating:.1f}/5.0")
                else:
                    print("[WARN] Rating not set")
                
                if self.screen.concert_info.track_count > 0:
                    print(f"[OK] Track count: {self.screen.concert_info.track_count}")
                else:
                    print("[INFO] Track count will update when setlist loads")
                
                print("\n[OK] Concert info widget integration successful!")
                print("[INFO] Visual verification required - check window display")
            else:
                print("[ERROR] Concert info widget not found on player screen!")
                print("[ERROR] Integration may be incomplete")
        
        except Exception as e:
            print(f"[ERROR] Failed to load show: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Run test"""
    tester = TestConcertInfo()
    return tester.run_test()


if __name__ == "__main__":
    sys.exit(main())
