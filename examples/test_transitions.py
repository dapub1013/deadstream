#!/usr/bin/env python3
"""
Test screen transitions for DeadStream UI.
Tests slide and fade animations between screens.
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from src.ui.main_window import MainWindow
from src.ui.transitions import TransitionType


class TransitionTestWindow(MainWindow):
    """
    Extended main window with transition testing controls
    """
    
    def __init__(self):
        """Initialize test window"""
        super().__init__()
        
        # Add test controls
        self.add_test_controls()
        
        print("[INFO] Transition test window initialized")
    
    def add_test_controls(self):
        """Add testing controls to the window"""
        # Create test control panel
        test_panel = QWidget()
        test_layout = QVBoxLayout()
        
        # Title
        title = QLabel("TRANSITION TEST CONTROLS")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        test_layout.addWidget(title)
        
        # Current screen indicator
        self.screen_indicator = QLabel(f"Current: {self.screen_manager.get_current_screen_name()}")
        self.screen_indicator.setAlignment(Qt.AlignCenter)
        test_layout.addWidget(self.screen_indicator)
        
        # Update indicator when screen changes
        self.screen_manager.screen_changed.connect(self.update_screen_indicator)
        
        # Slide transition tests
        slide_label = QLabel("Slide Transitions:")
        test_layout.addWidget(slide_label)
        
        slide_layout = QHBoxLayout()
        
        player_slide = QPushButton("Player (Slide)")
        player_slide.clicked.connect(lambda: self.test_transition("player", TransitionType.SLIDE_LEFT))
        slide_layout.addWidget(player_slide)
        
        browse_slide = QPushButton("Browse (Slide)")
        browse_slide.clicked.connect(lambda: self.test_transition("browse", TransitionType.SLIDE_LEFT))
        slide_layout.addWidget(browse_slide)
        
        settings_slide = QPushButton("Settings (Slide)")
        settings_slide.clicked.connect(lambda: self.test_transition("settings", TransitionType.SLIDE_LEFT))
        slide_layout.addWidget(settings_slide)
        
        test_layout.addLayout(slide_layout)
        
        # Fade transition tests
        fade_label = QLabel("Fade Transitions:")
        test_layout.addWidget(fade_label)
        
        fade_layout = QHBoxLayout()
        
        player_fade = QPushButton("Player (Fade)")
        player_fade.clicked.connect(lambda: self.test_transition("player", TransitionType.FADE))
        fade_layout.addWidget(player_fade)
        
        browse_fade = QPushButton("Browse (Fade)")
        browse_fade.clicked.connect(lambda: self.test_transition("browse", TransitionType.FADE))
        fade_layout.addWidget(browse_fade)
        
        settings_fade = QPushButton("Settings (Fade)")
        settings_fade.clicked.connect(lambda: self.test_transition("settings", TransitionType.FADE))
        fade_layout.addWidget(settings_fade)
        
        test_layout.addLayout(fade_layout)
        
        # Instant transition tests
        instant_label = QLabel("Instant Transitions:")
        test_layout.addWidget(instant_label)
        
        instant_layout = QHBoxLayout()
        
        player_instant = QPushButton("Player (Instant)")
        player_instant.clicked.connect(lambda: self.test_transition("player", TransitionType.INSTANT))
        instant_layout.addWidget(player_instant)
        
        browse_instant = QPushButton("Browse (Instant)")
        browse_instant.clicked.connect(lambda: self.test_transition("browse", TransitionType.INSTANT))
        instant_layout.addWidget(browse_instant)
        
        settings_instant = QPushButton("Settings (Instant)")
        settings_instant.clicked.connect(lambda: self.test_transition("settings", TransitionType.INSTANT))
        instant_layout.addWidget(settings_instant)
        
        test_layout.addLayout(instant_layout)
        
        # Auto-cycle test
        cycle_layout = QHBoxLayout()
        
        self.auto_cycle_btn = QPushButton("Start Auto-Cycle Test")
        self.auto_cycle_btn.clicked.connect(self.toggle_auto_cycle)
        cycle_layout.addWidget(self.auto_cycle_btn)
        
        test_layout.addLayout(cycle_layout)
        
        test_panel.setLayout(test_layout)
        
        # Add test panel to main layout (create a container)
        main_container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.centralWidget())
        main_layout.addWidget(test_panel)
        main_container.setLayout(main_layout)
        
        self.setCentralWidget(main_container)
        
        # Auto-cycle state
        self.auto_cycling = False
        self.cycle_timer = QTimer()
        self.cycle_timer.timeout.connect(self.cycle_screens)
        self.cycle_index = 0
    
    def update_screen_indicator(self, screen_name):
        """
        Update the current screen indicator
        
        Args:
            screen_name: Name of the new current screen
        """
        self.screen_indicator.setText(f"Current: {screen_name}")
    
    def test_transition(self, screen_name, transition_type):
        """
        Test a specific transition
        
        Args:
            screen_name: Target screen name
            transition_type: Type of transition to use
        """
        print(f"\n[TEST] Transitioning to {screen_name} with {transition_type}")
        self.screen_manager.show_screen(screen_name, transition_type=transition_type)
    
    def toggle_auto_cycle(self):
        """Toggle auto-cycle testing"""
        if self.auto_cycling:
            self.auto_cycling = False
            self.cycle_timer.stop()
            self.auto_cycle_btn.setText("Start Auto-Cycle Test")
            print("[TEST] Auto-cycle stopped")
        else:
            self.auto_cycling = True
            self.cycle_index = 0
            self.cycle_timer.start(2000)  # Cycle every 2 seconds
            self.auto_cycle_btn.setText("Stop Auto-Cycle Test")
            print("[TEST] Auto-cycle started")
    
    def cycle_screens(self):
        """Cycle through screens automatically"""
        screens = [
            ("player", TransitionType.SLIDE_LEFT),
            ("browse", TransitionType.SLIDE_LEFT),
            ("settings", TransitionType.SLIDE_LEFT),
            ("browse", TransitionType.SLIDE_RIGHT),
            ("player", TransitionType.SLIDE_RIGHT),
            ("settings", TransitionType.FADE),
        ]
        
        if self.cycle_index >= len(screens):
            self.cycle_index = 0
        
        screen_name, transition_type = screens[self.cycle_index]
        print(f"\n[AUTO-CYCLE] Screen {self.cycle_index + 1}/{len(screens)}: {screen_name} ({transition_type})")
        
        self.screen_manager.show_screen(screen_name, transition_type=transition_type)
        self.cycle_index += 1


def main():
    """Run the transition test"""
    print("[INFO] Starting transition test...")
    print("[INFO] Testing screen transitions with animations")
    print("")
    
    app = QApplication(sys.argv)
    
    # Create and show test window
    window = TransitionTestWindow()
    window.show()
    
    print("\n[INFO] Transition test window displayed")
    print("[INFO] Use the test controls to try different transition types")
    print("[INFO] Try the Auto-Cycle Test to see all transitions in sequence")
    print("")
    
    # Run application
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
