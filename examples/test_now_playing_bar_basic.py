#!/usr/bin/env python3
"""
Test script for NowPlayingBar widget (Phase 10F Task 10F.1)

Tests basic rendering, layout, and signal emission.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

from src.ui.widgets.now_playing_bar import NowPlayingBar


class TestWindow(QMainWindow):
    """Test window for NowPlayingBar widget"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NowPlayingBar Test - Phase 10F Task 10F.1")
        self.setFixedSize(1280, 720)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Layout
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Spacer to push bar to bottom
        layout.addStretch()

        # Info label
        info_label = QPushButton("NowPlayingBar Test\n\nBar should appear at bottom with:\n- Track info on left\n- 3 buttons on right (prev, play, next)\n- 80px height\n- Black background\n\nClick track info to emit player_requested signal\nClick buttons to emit their respective signals")
        info_label.setStyleSheet("""
            QPushButton {
                background-color: #1A2332;
                color: white;
                border: none;
                padding: 20px;
                font-size: 14px;
            }
        """)
        info_label.setEnabled(False)
        layout.addWidget(info_label)

        layout.addStretch()

        # Create now playing bar
        self.now_playing_bar = NowPlayingBar()

        # Load test track info
        self.now_playing_bar.load_track_info(
            "Scarlet Begonias",
            "1977-05-08",
            "Barton Hall, Cornell University"
        )

        # Connect signals
        self.now_playing_bar.player_requested.connect(self.on_player_requested)
        self.now_playing_bar.play_pause_clicked.connect(self.on_play_pause)
        self.now_playing_bar.next_clicked.connect(self.on_next)
        self.now_playing_bar.previous_clicked.connect(self.on_previous)

        # Add to layout
        layout.addWidget(self.now_playing_bar)

        print("[INFO] Test window initialized")
        print("[INFO] Now playing bar should be visible at bottom")

    def on_player_requested(self):
        """Handle player navigation request"""
        print("[PASS] player_requested signal emitted - would navigate to player")

    def on_play_pause(self):
        """Handle play/pause"""
        print("[PASS] play_pause_clicked signal emitted")

    def on_next(self):
        """Handle next track"""
        print("[PASS] next_clicked signal emitted")

    def on_previous(self):
        """Handle previous track"""
        print("[PASS] previous_clicked signal emitted")


def main():
    """Run the test"""
    app = QApplication(sys.argv)

    print("\n" + "=" * 60)
    print("NOWPLAYINGBAR TEST - Phase 10F Task 10F.1")
    print("=" * 60)
    print("\nVisual Checks:")
    print("  [CHECK] Widget renders with correct layout")
    print("  [CHECK] Height is 80px")
    print("  [CHECK] Black background with top border")
    print("  [CHECK] Track info displays correctly")
    print("  [CHECK] All buttons are 60x60px")
    print("  [CHECK] Buttons have proper spacing")
    print("\nFunctional Checks:")
    print("  [CHECK] Click track info -> player_requested signal")
    print("  [CHECK] Click prev button -> previous_clicked signal")
    print("  [CHECK] Click play button -> play_pause_clicked signal")
    print("  [CHECK] Click next button -> next_clicked signal")
    print("=" * 60 + "\n")

    window = TestWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
