#!/usr/bin/env python3
"""
Test script for NowPlayingBar widget - Phase 10F Task 10F.5

Tests the complete NowPlayingBar widget with real ResilientPlayer integration:
- Visual appearance (80px height, black background, proper spacing)
- Track info display
- All button sizes (60x60px)
- Play/pause icon toggle
- Prev/next buttons functionality
- Clicking bar emits player_requested signal
- Real-time updates from player (200ms timer)

Usage:
    python3 examples/test_now_playing_bar.py

Reference files:
- examples/test_player_hybrid.py - Similar testing pattern
- Phase 10F implementation plan - Task 10F.5 requirements
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from src.ui.widgets.now_playing_bar import NowPlayingBar
from src.ui.styles.theme import Theme
from src.audio.resilient_player import ResilientPlayer
from src.database.queries import get_show_by_date, get_top_rated_shows
from src.api.metadata import get_metadata, extract_audio_files


def get_test_url():
    """
    Get a valid test URL from database (following 07-project-guidelines.md).

    Never hardcode URLs - they become invalid over time (404 errors).
    Always get test URLs from the database at runtime.
    """
    print("[INFO] Getting test URL from database...")

    # Try Cornell '77 first (legendary show)
    shows = get_show_by_date('1977-05-08')

    # Fallback to top-rated shows if Cornell not available
    if not shows:
        print("[INFO] Cornell '77 not found, trying top-rated shows...")
        shows = get_top_rated_shows(limit=3, min_reviews=5)

    if not shows:
        print("[ERROR] No shows available in database")
        return None

    # Try each show until we get valid audio
    for show in shows[:3]:
        try:
            print(f"[INFO] Trying show: {show.get('date', 'Unknown')} - {show.get('venue', 'Unknown')}")
            metadata = get_metadata(show['identifier'])
            audio_files = extract_audio_files(metadata)

            if audio_files:
                first_track = audio_files[0]
                url = f"https://archive.org/download/{show['identifier']}/{first_track['name']}"

                return {
                    'url': url,
                    'track_name': first_track.get('title', 'Unknown Track'),
                    'show_date': show.get('date', 'Unknown Date'),
                    'venue': show.get('venue', 'Unknown Venue'),
                    'total_tracks': len(audio_files)
                }
        except Exception as e:
            print(f"[ERROR] Failed to get audio from show: {e}")
            continue

    print("[ERROR] Could not find valid test show with audio")
    return None


class TestWindow(QMainWindow):
    """Test window for NowPlayingBar widget with real player integration"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NowPlayingBar Test - Phase 10F Task 10F.5")
        self.setFixedSize(1280, 720)

        # Apply dark background
        self.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")

        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Main layout
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Info panel at top
        self.info_panel = self._create_info_panel()
        layout.addWidget(self.info_panel)

        # Stretch to push bar to bottom
        layout.addStretch()

        # Create ResilientPlayer
        print("[INFO] Creating ResilientPlayer...")
        self.player = ResilientPlayer()

        # Create NowPlayingBar
        print("[INFO] Creating NowPlayingBar...")
        self.now_playing_bar = NowPlayingBar()

        # Connect bar to player
        self.now_playing_bar.set_player(self.player)

        # Connect bar signals
        self.now_playing_bar.player_requested.connect(self._on_player_requested)
        self.now_playing_bar.play_pause_clicked.connect(self._on_play_pause)
        self.now_playing_bar.next_clicked.connect(self._on_next)
        self.now_playing_bar.previous_clicked.connect(self._on_previous)

        # Add bar to layout (fixed 80px at bottom)
        layout.addWidget(self.now_playing_bar)

        print("[INFO] NowPlayingBar added to layout")

        # Load test track after 1 second
        QTimer.singleShot(1000, self.load_test_track)

        # Show test instructions
        self._print_instructions()

    def _create_info_panel(self):
        """Create info panel with test instructions"""
        panel = QWidget()
        panel.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme.BG_PANEL_DARK};
                border-bottom: 2px solid {Theme.BORDER_PANEL};
                padding: {Theme.SPACING_LARGE}px;
            }}
        """)
        panel.setFixedHeight(200)

        layout = QVBoxLayout(panel)
        layout.setSpacing(Theme.SPACING_SMALL)

        # Title
        title = QLabel("NowPlayingBar Test - Phase 10F Task 10F.5")
        font_title = QFont(Theme.FONT_FAMILY)
        font_title.setPixelSize(Theme.HEADER_MEDIUM)
        font_title.setBold(True)
        title.setFont(font_title)
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY};")
        layout.addWidget(title)

        # Status label (will be updated)
        self.status_label = QLabel("Loading test track...")
        font_status = QFont(Theme.FONT_FAMILY)
        font_status.setPixelSize(Theme.BODY_LARGE)
        self.status_label.setFont(font_status)
        self.status_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        layout.addWidget(self.status_label)

        # Instructions
        instructions = QLabel(
            "Test Checklist:\n"
            "• Visual: Bar is 80px height, black background, proper spacing\n"
            "• Visual: Track info displays correctly\n"
            "• Visual: All buttons are 60x60px\n"
            "• Functional: Play/pause button toggles icon\n"
            "• Functional: Prev/next buttons work\n"
            "• Functional: Click track info to navigate to player"
        )
        font_inst = QFont(Theme.FONT_FAMILY)
        font_inst.setPixelSize(Theme.BODY_SMALL)
        instructions.setFont(font_inst)
        instructions.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        layout.addWidget(instructions)

        return panel

    def _print_instructions(self):
        """Print test instructions to console"""
        print("\n" + "=" * 70)
        print("NOWPLAYINGBAR TEST - PHASE 10F TASK 10F.5")
        print("=" * 70)
        print("\nVISUAL CHECKS:")
        print("  [ ] Bar is 80px height")
        print("  [ ] Bar has black background")
        print("  [ ] Track info on left (bold title, gray show info)")
        print("  [ ] Three buttons on right (prev, play/pause, next)")
        print("  [ ] All buttons are 60x60px")
        print("  [ ] Proper spacing (24px between elements)")
        print("\nFUNCTIONAL CHECKS:")
        print("  [ ] Play/pause button shows correct icon")
        print("  [ ] Play/pause button toggles on click")
        print("  [ ] Previous button works")
        print("  [ ] Next button works")
        print("  [ ] Clicking track info area emits player_requested")
        print("  [ ] Real-time updates from player (200ms)")
        print("\n" + "=" * 70 + "\n")

    def load_test_track(self):
        """Load test track from database"""
        print("[INFO] Loading test track from database...")

        test_data = get_test_url()

        if not test_data:
            self.status_label.setText("[FAIL] Could not load test track from database")
            print("[FAIL] Could not load test track")
            return

        print(f"[OK] Test track found:")
        print(f"     Date: {test_data['show_date']}")
        print(f"     Venue: {test_data['venue']}")
        print(f"     Track: {test_data['track_name']}")
        print(f"     URL: {test_data['url'][:60]}...")

        # Load track info into bar
        self.now_playing_bar.load_track_info(
            track_name=test_data['track_name'],
            show_date=test_data['show_date'],
            show_venue=test_data['venue']
        )

        # Load URL into player
        try:
            self.player.load_url(test_data['url'])
            print("[OK] Track loaded into player")

            # Start playback
            self.player.play()
            print("[OK] Playback started")

            self.status_label.setText(
                f"[PASS] Playing: {test_data['track_name']} - {test_data['show_date']}"
            )

        except Exception as e:
            print(f"[ERROR] Failed to load/play track: {e}")
            self.status_label.setText(f"[FAIL] Error loading track: {e}")

    # Signal handlers

    def _on_player_requested(self):
        """Handle player_requested signal (user clicked track info)"""
        print("\n[SIGNAL] player_requested - User clicked bar to view player")
        self.status_label.setText("[SIGNAL] player_requested - Navigate to player screen")

    def _on_play_pause(self):
        """Handle play/pause button click"""
        print("\n[SIGNAL] play_pause_clicked")

        # Toggle playback
        from src.audio.resilient_player import PlayerState
        state = self.player.get_state()

        if state == PlayerState.PLAYING:
            self.player.pause()
            print("[ACTION] Paused playback")
            self.status_label.setText("[ACTION] Playback paused")
        else:
            self.player.play()
            print("[ACTION] Resumed playback")
            self.status_label.setText("[ACTION] Playback resumed")

    def _on_next(self):
        """Handle next button click"""
        print("\n[SIGNAL] next_clicked")
        print("[INFO] Next track - (would skip to next track in real app)")
        self.status_label.setText("[SIGNAL] next_clicked - Skip to next track")

    def _on_previous(self):
        """Handle previous button click"""
        print("\n[SIGNAL] previous_clicked")
        print("[INFO] Previous track - (would skip to previous track in real app)")
        self.status_label.setText("[SIGNAL] previous_clicked - Skip to previous track")

    def closeEvent(self, event):
        """Clean up on close"""
        print("\n[INFO] Cleaning up...")
        if hasattr(self, 'player') and self.player:
            self.player.stop()
            print("[INFO] Player stopped")
        event.accept()


def run_visual_checks():
    """Print visual check guidelines"""
    print("\n" + "=" * 70)
    print("VISUAL VERIFICATION CHECKLIST")
    print("=" * 70)
    print("\n1. BAR DIMENSIONS:")
    print("   - Height: 80px (measure with ruler or inspect)")
    print("   - Width: Full width of window (1280px)")
    print("   - Position: Bottom of window")
    print("\n2. BAR BACKGROUND:")
    print("   - Color: Pure black (#000000)")
    print("   - Top border: 1px solid border (Theme.BORDER_PANEL)")
    print("\n3. TRACK INFO (Left side):")
    print("   - Track title: Bold, large (20px), white")
    print("   - Show info: Normal, small (14px), gray")
    print("   - Spacing: 8px between labels")
    print("\n4. CONTROL BUTTONS (Right side):")
    print("   - Three buttons: Previous, Play/Pause, Next")
    print("   - Size: 60x60px each")
    print("   - Spacing: 24px between buttons")
    print("   - Previous: Back icon, solid background")
    print("   - Play/Pause: Play or Pause icon, accent (yellow) background")
    print("   - Next: Forward icon, solid background")
    print("\n5. LAYOUT:")
    print("   - Track info: Left-aligned, expanding to fill space")
    print("   - Controls: Right-aligned, fixed width")
    print("   - Padding: 24px left/right, 16px top/bottom")
    print("\n6. INTERACTION:")
    print("   - Hover over track info: Cursor changes to pointing hand")
    print("   - Click track info: Emits player_requested signal")
    print("   - Click buttons: Emit respective signals")
    print("   - Play/pause icon: Toggles based on player state")
    print("\n" + "=" * 70 + "\n")


def run_functional_tests():
    """Print functional test guidelines"""
    print("\n" + "=" * 70)
    print("FUNCTIONAL TEST CHECKLIST")
    print("=" * 70)
    print("\n1. PLAYER INTEGRATION:")
    print("   [ ] Bar connects to ResilientPlayer on init")
    print("   [ ] Timer starts (200ms interval)")
    print("   [ ] Play/pause icon updates automatically")
    print("\n2. TRACK INFO:")
    print("   [ ] Track name displays correctly")
    print("   [ ] Show date displays correctly")
    print("   [ ] Venue displays correctly")
    print("   [ ] Info updates when load_track_info() called")
    print("\n3. PLAY/PAUSE BUTTON:")
    print("   [ ] Shows 'play' icon when paused")
    print("   [ ] Shows 'pause' icon when playing")
    print("   [ ] Icon updates in real-time (200ms)")
    print("   [ ] Click toggles playback")
    print("\n4. PREVIOUS/NEXT BUTTONS:")
    print("   [ ] Previous button emits previous_clicked signal")
    print("   [ ] Next button emits next_clicked signal")
    print("   [ ] Buttons are visually distinct from play/pause")
    print("\n5. NAVIGATION:")
    print("   [ ] Clicking track info emits player_requested")
    print("   [ ] Clicking buttons does NOT emit player_requested")
    print("   [ ] Signal emission works correctly")
    print("\n6. REAL-TIME UPDATES:")
    print("   [ ] Play/pause icon updates every 200ms")
    print("   [ ] Updates continue while player is active")
    print("   [ ] No performance issues (smooth UI)")
    print("\n" + "=" * 70 + "\n")


def main():
    """Run the test application"""
    try:
        app = QApplication(sys.argv)

        # Print test checklists
        run_visual_checks()
        run_functional_tests()

        # Create and show test window
        window = TestWindow()
        window.show()

        print("[INFO] Test window displayed")
        print("[INFO] Watch for console output as you interact with the bar")
        print("[INFO] Close window or press Ctrl+C to quit\n")

        sys.exit(app.exec_())

    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
