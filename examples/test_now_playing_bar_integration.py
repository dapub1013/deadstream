#!/usr/bin/env python3
"""
Test script for NowPlayingBar with ResilientPlayer integration - Phase 10F Task 10F.2

Tests:
1. Widget connects to ResilientPlayer successfully
2. Timer-based updates working (200ms interval)
3. Play/pause button shows correct icon based on player state
4. Track info displays correctly
5. Controls affect playback (play/pause, next, previous signals)
6. Real-time updates from player
7. Bar click navigation signal works
8. All styling from Theme Manager (zero hardcoded values)
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from src.ui.widgets.now_playing_bar import NowPlayingBar
from src.ui.styles.theme import Theme
from src.audio.resilient_player import ResilientPlayer


def get_test_url():
    """
    Get a valid test URL from the database.

    Returns:
        str: URL to a test audio file, or None if not available
    """
    try:
        from src.database.queries import get_show_by_date
        from src.api.metadata import get_metadata, extract_audio_files

        # Cornell '77 - famous show
        shows = get_show_by_date('1977-05-08')

        if shows:
            identifier = shows[0]['identifier']
            metadata = get_metadata(identifier)
            audio_files = extract_audio_files(metadata)

            if audio_files:
                url = f"https://archive.org/download/{identifier}/{audio_files[0]['name']}"
                print(f"[PASS] Got test URL from database: {identifier}")
                return url

        print("[WARN] Could not get test URL from database")
        return None

    except Exception as e:
        print(f"[ERROR] Failed to get test URL: {e}")
        return None


def test_player_integration():
    """Test NowPlayingBar integration with ResilientPlayer"""
    print("\n" + "="*70)
    print("NOWPLAYINGBAR + RESILIENTPLAYER INTEGRATION TEST")
    print("="*70)

    app = QApplication(sys.argv)

    # Create container widget
    container = QWidget()
    container.setWindowTitle("DeadStream - Now Playing Bar Integration Test")
    container.setFixedSize(1280, 300)
    container.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # Instructions
    instructions = QLabel(
        "Integration Test Checklist:\n"
        "1. Bar displays at bottom (80px height, black background)\n"
        "2. Track info displays: 'Scarlet Begonias' from Cornell '77\n"
        "3. Play button initially shows 'play' icon\n"
        "4. Click play - icon changes to 'pause' (real-time update)\n"
        "5. Click pause - icon changes back to 'play'\n"
        "6. Next/prev buttons emit signals (check console)\n"
        "7. Click track info area - navigates to player (check console)\n"
        "8. All buttons are 60x60px (touch-friendly)\n"
        "9. Timer updates every 200ms (check console for state changes)\n"
        "10. Volume control affects actual playback\n"
    )
    instructions.setAlignment(Qt.AlignLeft)
    instructions.setWordWrap(True)
    instructions.setStyleSheet(f"""
        QLabel {{
            color: {Theme.TEXT_SECONDARY};
            font-size: {Theme.BODY_SMALL}px;
            padding: {Theme.SPACING_MEDIUM}px;
            background-color: {Theme.BG_CARD};
        }}
    """)
    layout.addWidget(instructions)

    # Spacer to push bar to bottom
    layout.addStretch()

    # Create ResilientPlayer
    print("\n[INFO] Creating ResilientPlayer...")
    player = ResilientPlayer(debug=False)

    # Load test audio
    test_url = get_test_url()
    if test_url:
        print(f"[INFO] Loading test URL: {test_url[:80]}...")
        player.load_url(test_url)
    else:
        print("[WARN] No test URL available - using mock data")

    # Create NowPlayingBar
    print("[INFO] Creating NowPlayingBar...")
    bar = NowPlayingBar()

    # Connect to player (Task 10F.2)
    print("[INFO] Connecting bar to player...")
    bar.set_player(player)

    # Load track info
    bar.load_track_info(
        track_name="Scarlet Begonias",
        show_date="1977-05-08",
        show_venue="Barton Hall, Cornell University"
    )

    # Connect signals to test handlers
    def on_play_pause_clicked():
        print("[TEST] Play/pause clicked - toggling playback")
        if player.is_playing():
            player.pause()
        else:
            player.play()

    def on_next_clicked():
        print("[TEST] Next clicked - would skip to next track")

    def on_previous_clicked():
        print("[TEST] Previous clicked - would skip to previous track")

    def on_player_requested():
        print("[TEST] Bar clicked - would navigate to player screen")

    bar.play_pause_clicked.connect(on_play_pause_clicked)
    bar.next_clicked.connect(on_next_clicked)
    bar.previous_clicked.connect(on_previous_clicked)
    bar.player_requested.connect(on_player_requested)

    # Add bar to layout
    layout.addWidget(bar)

    # Control buttons for testing
    controls_widget = QWidget()
    controls_layout = QVBoxLayout()
    controls_layout.setContentsMargins(Theme.SPACING_MEDIUM, Theme.SPACING_SMALL, Theme.SPACING_MEDIUM, Theme.SPACING_SMALL)

    # Manual play button
    play_btn = QPushButton("Manual Play (Test)")
    play_btn.clicked.connect(lambda: player.play())
    play_btn.setStyleSheet(Theme.get_button_style(Theme.ACCENT_GREEN))
    controls_layout.addWidget(play_btn)

    # Manual pause button
    pause_btn = QPushButton("Manual Pause (Test)")
    pause_btn.clicked.connect(lambda: player.pause())
    pause_btn.setStyleSheet(Theme.get_button_style(Theme.ACCENT_RED))
    controls_layout.addWidget(pause_btn)

    controls_widget.setLayout(controls_layout)
    layout.insertWidget(1, controls_widget)  # Insert after instructions

    container.setLayout(layout)
    container.show()

    # Acceptance criteria checklist
    print("\n" + "="*70)
    print("ACCEPTANCE CRITERIA - Task 10F.2")
    print("="*70)
    print("[ ] Widget connected to ResilientPlayer")
    print("[ ] Timer-based updates working (200ms)")
    print("[ ] Play/pause button shows correct icon")
    print("[ ] Track info updates when track changes")
    print("[ ] Controls affect playback correctly")
    print("[ ] Follow patterns from player_screen.py")
    print("="*70)
    print("\nManual Test Instructions:")
    print("1. Click 'Manual Play (Test)' - bar play button should change to pause icon")
    print("2. Click 'Manual Pause (Test)' - bar pause button should change to play icon")
    print("3. Click bar's play/pause button - should toggle playback")
    print("4. Click bar's next/previous buttons - should print signals")
    print("5. Click track info area - should print navigation signal")
    print("6. Observe console for timer updates every 200ms")
    print("\nPress Ctrl+C to exit")
    print("="*70 + "\n")

    sys.exit(app.exec_())


if __name__ == '__main__':
    test_player_integration()
