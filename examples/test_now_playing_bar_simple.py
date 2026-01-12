#!/usr/bin/env python3
"""
Simple test for NowPlayingBar + ResilientPlayer integration - Phase 10F Task 10F.2

This is a lightweight test that doesn't require database access.
Tests the core integration functionality.
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

from src.ui.widgets.now_playing_bar import NowPlayingBar
from src.ui.styles.theme import Theme
from src.audio.resilient_player import ResilientPlayer


def main():
    """Simple integration test"""
    print("\n" + "="*70)
    print("NOWPLAYINGBAR INTEGRATION TEST (SIMPLE)")
    print("="*70)

    app = QApplication(sys.argv)

    # Create container
    container = QWidget()
    container.setWindowTitle("DeadStream - Now Playing Bar Test (Simple)")
    container.setFixedSize(1280, 200)
    container.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # Title
    title = QLabel("Now Playing Bar - Integration Test")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet(f"""
        QLabel {{
            color: {Theme.TEXT_PRIMARY};
            font-size: {Theme.HEADER_MEDIUM}px;
            font-weight: bold;
            padding: {Theme.SPACING_MEDIUM}px;
        }}
    """)
    layout.addWidget(title)

    # Spacer
    layout.addStretch()

    # Create player
    print("[INFO] Creating ResilientPlayer...")
    player = ResilientPlayer(debug=False)

    # Create bar
    print("[INFO] Creating NowPlayingBar...")
    bar = NowPlayingBar()

    # Connect to player (TASK 10F.2)
    print("[INFO] Connecting bar to player...")
    bar.set_player(player)
    print("[PASS] Bar connected to player successfully")

    # Load track info
    bar.load_track_info(
        track_name="Scarlet Begonias > Fire on the Mountain",
        show_date="1977-05-08",
        show_venue="Barton Hall, Cornell University"
    )
    print("[PASS] Track info loaded")

    # Connect signals
    signal_test_results = {
        'play_pause': False,
        'next': False,
        'previous': False,
        'player_requested': False
    }

    def test_play_pause():
        signal_test_results['play_pause'] = True
        print("[PASS] Play/pause signal received")

    def test_next():
        signal_test_results['next'] = True
        print("[PASS] Next signal received")

    def test_previous():
        signal_test_results['previous'] = True
        print("[PASS] Previous signal received")

    def test_player_requested():
        signal_test_results['player_requested'] = True
        print("[PASS] Player requested signal received")

    bar.play_pause_clicked.connect(test_play_pause)
    bar.next_clicked.connect(test_next)
    bar.previous_clicked.connect(test_previous)
    bar.player_requested.connect(test_player_requested)

    # Add bar to layout
    layout.addWidget(bar)

    container.setLayout(layout)
    container.show()

    # Print test instructions
    print("\n" + "="*70)
    print("MANUAL TEST INSTRUCTIONS")
    print("="*70)
    print("Visual Checks:")
    print("  [ ] Bar is 80px tall with black background")
    print("  [ ] Track title shows: 'Scarlet Begonias > Fire on the Mountain'")
    print("  [ ] Show info shows: '1977-05-08 - Barton Hall, Cornell University'")
    print("  [ ] Three control buttons visible (prev, play, next)")
    print("  [ ] All buttons are 60x60px")
    print("  [ ] Play button has accent (yellow) background")
    print("  [ ] Top border visible")
    print("\nFunctional Checks:")
    print("  1. Click play/pause button - should see [PASS] message")
    print("  2. Click next button - should see [PASS] message")
    print("  3. Click previous button - should see [PASS] message")
    print("  4. Click track info area - should see [PASS] message")
    print("\nIntegration Checks:")
    print("  [ ] Timer updates visible in console every 200ms")
    print("  [ ] Play button icon updates based on player state")
    print("="*70)
    print("\nClick buttons to test signal emission")
    print("Press Ctrl+C to exit\n")

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
