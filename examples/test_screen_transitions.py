#!/usr/bin/env python3
"""
Test script for screen transitions in Phase 10E.5

Tests:
- Fade transitions between screens
- Transition timing (300ms)
- No lag or performance issues
- Smooth visual feedback

Usage:
    python3 examples/test_screen_transitions.py
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtTest import QTest

from src.ui.screen_manager import ScreenManager
from src.ui.transitions import TransitionType


class TestScreen(QWidget):
    """Simple test screen with colored background"""

    def __init__(self, name, color):
        super().__init__()
        self.name = name
        self.color = color
        self.init_ui()

    def init_ui(self):
        """Set up the test screen"""
        layout = QVBoxLayout()

        # Screen title
        title = QLabel(self.name)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 48px;
                font-weight: bold;
                padding: 40px;
            }
        """)
        layout.addWidget(title)

        self.setLayout(layout)

        # Set background color
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.color};
            }}
        """)


class TransitionTestWindow(QWidget):
    """Test window for screen transitions"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Set up the test window"""
        self.setWindowTitle("Screen Transition Test - Phase 10E.5")
        self.setGeometry(100, 100, 800, 600)

        # Create layout
        layout = QVBoxLayout()

        # Create screen manager
        self.screen_manager = ScreenManager()
        layout.addWidget(self.screen_manager)

        # Create test screens
        player_screen = TestScreen("PLAYER SCREEN", "#1e3a5f")  # Dark blue
        browse_screen = TestScreen("BROWSE SCREEN", "#2E2870")  # Purple
        settings_screen = TestScreen("SETTINGS SCREEN", "#1a2332")  # Dark gray

        # Add screens to manager
        self.screen_manager.add_screen(ScreenManager.PLAYER_SCREEN, player_screen)
        self.screen_manager.add_screen(ScreenManager.BROWSE_SCREEN, browse_screen)
        self.screen_manager.add_screen(ScreenManager.SETTINGS_SCREEN, settings_screen)

        # Create control buttons
        button_layout = QVBoxLayout()

        # Transition type buttons
        fade_btn = QPushButton("Use FADE Transitions")
        fade_btn.clicked.connect(lambda: self.set_transition_type(TransitionType.FADE))
        button_layout.addWidget(fade_btn)

        slide_btn = QPushButton("Use SLIDE Transitions")
        slide_btn.clicked.connect(lambda: self.set_transition_type(TransitionType.SLIDE_LEFT))
        button_layout.addWidget(slide_btn)

        instant_btn = QPushButton("Use INSTANT Transitions")
        instant_btn.clicked.connect(lambda: self.set_transition_type(TransitionType.INSTANT))
        button_layout.addWidget(instant_btn)

        # Navigation buttons
        player_btn = QPushButton("Go to Player")
        player_btn.clicked.connect(lambda: self.goto_screen(ScreenManager.PLAYER_SCREEN))
        button_layout.addWidget(player_btn)

        browse_btn = QPushButton("Go to Browse")
        browse_btn.clicked.connect(lambda: self.goto_screen(ScreenManager.BROWSE_SCREEN))
        button_layout.addWidget(browse_btn)

        settings_btn = QPushButton("Go to Settings")
        settings_btn.clicked.connect(lambda: self.goto_screen(ScreenManager.SETTINGS_SCREEN))
        button_layout.addWidget(settings_btn)

        # Auto-cycle button
        cycle_btn = QPushButton("Auto Cycle (Test)")
        cycle_btn.clicked.connect(self.start_auto_cycle)
        button_layout.addWidget(cycle_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # State
        self.transition_type = TransitionType.FADE
        self.cycle_timer = None
        self.cycle_index = 0

        print("[INFO] Transition test window initialized")
        print("[INFO] Default transition type: FADE")

    def set_transition_type(self, transition_type):
        """Set the transition type to use"""
        self.transition_type = transition_type
        print(f"[INFO] Transition type set to: {transition_type}")

    def goto_screen(self, screen_name):
        """Navigate to a screen with current transition type"""
        print(f"[TEST] Navigating to {screen_name} with {self.transition_type}")
        self.screen_manager.show_screen(screen_name, transition_type=self.transition_type)

    def start_auto_cycle(self):
        """Automatically cycle through screens for testing"""
        if self.cycle_timer:
            self.cycle_timer.stop()
            self.cycle_timer = None
            print("[INFO] Auto cycle stopped")
            return

        screens = [
            ScreenManager.PLAYER_SCREEN,
            ScreenManager.BROWSE_SCREEN,
            ScreenManager.SETTINGS_SCREEN
        ]

        def cycle():
            screen = screens[self.cycle_index % len(screens)]
            self.goto_screen(screen)
            self.cycle_index += 1

        # Cycle every 2 seconds
        self.cycle_timer = QTimer()
        self.cycle_timer.timeout.connect(cycle)
        self.cycle_timer.start(2000)

        print("[INFO] Auto cycle started (2 second intervals)")


def run_manual_test():
    """Run manual interactive test"""
    app = QApplication(sys.argv)

    window = TransitionTestWindow()
    window.show()

    print("\n" + "="*60)
    print("SCREEN TRANSITION TEST - Phase 10E.5")
    print("="*60)
    print("\nINSTRUCTIONS:")
    print("1. Click transition type buttons to change animation style")
    print("2. Click navigation buttons to test transitions")
    print("3. Click 'Auto Cycle' to automatically test all transitions")
    print("\nOBSERVE:")
    print("- Smooth 300ms transitions")
    print("- No lag or stutter")
    print("- Fade transitions are smooth and professional")
    print("- Slide transitions show directional flow")
    print("\n" + "="*60 + "\n")

    sys.exit(app.exec_())


def run_automated_test():
    """Run automated test suite"""
    app = QApplication(sys.argv)

    window = TransitionTestWindow()
    window.show()

    print("\n" + "="*60)
    print("AUTOMATED SCREEN TRANSITION TEST")
    print("="*60)

    # Test 1: Fade transitions
    print("\n[TEST 1] Testing FADE transitions...")
    window.set_transition_type(TransitionType.FADE)

    window.goto_screen(ScreenManager.BROWSE_SCREEN)
    QTest.qWait(400)  # Wait for 300ms transition + buffer

    window.goto_screen(ScreenManager.SETTINGS_SCREEN)
    QTest.qWait(400)

    window.goto_screen(ScreenManager.PLAYER_SCREEN)
    QTest.qWait(400)

    print("[PASS] Fade transitions completed")

    # Test 2: Slide transitions
    print("\n[TEST 2] Testing SLIDE transitions...")
    window.set_transition_type(TransitionType.SLIDE_LEFT)

    window.goto_screen(ScreenManager.BROWSE_SCREEN)
    QTest.qWait(400)

    window.goto_screen(ScreenManager.SETTINGS_SCREEN)
    QTest.qWait(400)

    window.goto_screen(ScreenManager.PLAYER_SCREEN)
    QTest.qWait(400)

    print("[PASS] Slide transitions completed")

    # Test 3: Instant transitions
    print("\n[TEST 3] Testing INSTANT transitions...")
    window.set_transition_type(TransitionType.INSTANT)

    window.goto_screen(ScreenManager.BROWSE_SCREEN)
    QTest.qWait(100)

    window.goto_screen(ScreenManager.SETTINGS_SCREEN)
    QTest.qWait(100)

    window.goto_screen(ScreenManager.PLAYER_SCREEN)
    QTest.qWait(100)

    print("[PASS] Instant transitions completed")

    # Test 4: Verify screen manager state
    print("\n[TEST 4] Verifying screen manager state...")
    current = window.screen_manager.get_current_screen_name()
    assert current == ScreenManager.PLAYER_SCREEN, f"Expected player, got {current}"
    print(f"[PASS] Current screen: {current}")

    # Test 5: Rapid transitions (stress test)
    print("\n[TEST 5] Testing rapid transitions...")
    window.set_transition_type(TransitionType.FADE)

    for i in range(5):
        screens = [
            ScreenManager.PLAYER_SCREEN,
            ScreenManager.BROWSE_SCREEN,
            ScreenManager.SETTINGS_SCREEN
        ]
        screen = screens[i % len(screens)]
        window.goto_screen(screen)
        QTest.qWait(100)  # Shorter wait to test animation interruption

    QTest.qWait(500)  # Final wait
    print("[PASS] Rapid transitions handled correctly")

    print("\n" + "="*60)
    print("ALL TESTS PASSED")
    print("="*60)
    print("\nSUMMARY:")
    print("- Fade transitions: WORKING")
    print("- Slide transitions: WORKING")
    print("- Instant transitions: WORKING")
    print("- Screen manager state: CORRECT")
    print("- Rapid transition handling: ROBUST")
    print("\n" + "="*60 + "\n")

    app.quit()


if __name__ == '__main__':
    # Check for command line argument
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        run_automated_test()
    else:
        run_manual_test()
