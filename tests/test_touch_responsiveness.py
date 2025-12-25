#!/usr/bin/env python3
"""
DeadStream - Touch Responsiveness Test
Phase 6 Task 6.4

Tests touch interaction with various button sizes and UI elements.
Follows 07-project-guidelines.md standards (ASCII only, no emojis).
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPalette, QColor, QFont

# Project root setup
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


class TouchTestWindow(QMainWindow):
    """
    Main window for touch responsiveness testing.
    Tests various button sizes and touch targets.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeadStream Touch Responsiveness Test")
        
        # Touch test statistics
        self.touch_count = 0
        self.button_sizes = {
            '40px': 0,
            '44px': 0,
            '60px': 0,
            '80px': 0,
            '100px': 0
        }
        self.last_touch_time = None
        
        # Setup UI
        self.init_ui()
        self.setup_theme()
        
    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("Touch Responsiveness Test")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Test touch responsiveness by tapping buttons below.\n"
            "Each button size represents common UI elements.\n"
            "The test will track your touch accuracy and timing."
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        
        # Statistics display
        self.stats_label = QLabel(self.get_stats_text())
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 14px; margin: 10px;")
        main_layout.addWidget(self.stats_label)
        
        # Scrollable test area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll)
        
        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        
        # Test sections
        self.add_button_size_tests(scroll_layout)
        self.add_spacing_tests(scroll_layout)
        self.add_target_density_tests(scroll_layout)
        self.add_edge_case_tests(scroll_layout)
        
        # Control buttons at bottom
        control_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Reset Statistics")
        reset_btn.clicked.connect(self.reset_stats)
        reset_btn.setMinimumHeight(60)
        control_layout.addWidget(reset_btn)
        
        close_btn = QPushButton("Close Test")
        close_btn.clicked.connect(self.close)
        close_btn.setMinimumHeight(60)
        control_layout.addWidget(close_btn)
        
        main_layout.addLayout(control_layout)
        
        # Window sizing
        screen = QApplication.primaryScreen().geometry()
        window_width = min(1280, screen.width() - 100)
        window_height = min(720, screen.height() - 100)
        self.setGeometry(50, 50, window_width, window_height)
        
    def add_button_size_tests(self, layout):
        """Add button size comparison tests"""
        section = self.create_test_section("Button Size Tests")
        section_layout = section.layout()
        
        # Test each standard button size
        sizes = [
            (40, "40x40px - Minimum (too small)"),
            (44, "44x44px - Touch minimum (Apple HIG)"),
            (60, "60x60px - DeadStream standard"),
            (80, "80x80px - Large touch target"),
            (100, "100x100px - Extra large")
        ]
        
        for size, label in sizes:
            row = QHBoxLayout()
            
            desc = QLabel(label)
            desc.setMinimumWidth(300)
            row.addWidget(desc)
            
            btn = QPushButton("Tap Me")
            btn.setFixedSize(size, size)
            btn.clicked.connect(lambda checked, s=f"{size}px": self.record_touch(s))
            row.addWidget(btn)
            
            row.addStretch()
            section_layout.addLayout(row)
        
        layout.addWidget(section)
        
    def add_spacing_tests(self, layout):
        """Test button spacing and grouping"""
        section = self.create_test_section("Spacing Tests")
        section_layout = section.layout()
        
        # Tight spacing (potential mis-taps)
        desc = QLabel("Tight spacing (8px) - Easy to mis-tap:")
        section_layout.addWidget(desc)
        
        tight_row = QHBoxLayout()
        for i in range(5):
            btn = QPushButton(str(i+1))
            btn.setFixedSize(60, 60)
            btn.clicked.connect(lambda checked, num=i+1: self.record_touch(f"tight-{num}"))
            tight_row.addWidget(btn)
        tight_row.addStretch()
        section_layout.addLayout(tight_row)
        
        # Good spacing (easier tapping)
        desc = QLabel("Good spacing (16px) - Comfortable:")
        section_layout.addWidget(desc)
        
        good_row = QHBoxLayout()
        for i in range(5):
            btn = QPushButton(str(i+1))
            btn.setFixedSize(60, 60)
            btn.clicked.connect(lambda checked, num=i+1: self.record_touch(f"good-{num}"))
            good_row.addWidget(btn)
            if i < 4:
                good_row.addSpacing(16)
        good_row.addStretch()
        section_layout.addLayout(good_row)
        
        layout.addWidget(section)
        
    def add_target_density_tests(self, layout):
        """Test high-density touch targets"""
        section = self.create_test_section("Target Density Tests")
        section_layout = section.layout()
        
        desc = QLabel("3x3 grid of 44px buttons - Test accuracy:")
        section_layout.addWidget(desc)
        
        grid_layout = QHBoxLayout()
        for row in range(3):
            col_layout = QVBoxLayout()
            for col in range(3):
                btn = QPushButton(f"{row},{col}")
                btn.setFixedSize(44, 44)
                btn.clicked.connect(lambda checked, r=row, c=col: 
                                  self.record_touch(f"grid-{r}{c}"))
                col_layout.addWidget(btn)
            grid_layout.addLayout(col_layout)
        grid_layout.addStretch()
        section_layout.addLayout(grid_layout)
        
        layout.addWidget(section)
        
    def add_edge_case_tests(self, layout):
        """Test edge cases and corner interactions"""
        section = self.create_test_section("Edge Case Tests")
        section_layout = section.layout()
        
        # Long press test
        desc = QLabel("Press and hold test (will change color):")
        section_layout.addWidget(desc)
        
        hold_btn = QPushButton("Press and Hold")
        hold_btn.setFixedHeight(60)
        hold_btn.pressed.connect(lambda: self.on_button_pressed(hold_btn))
        hold_btn.released.connect(lambda: self.on_button_released(hold_btn))
        section_layout.addWidget(hold_btn)
        
        # Double tap test
        desc = QLabel("Double tap test (tap twice quickly):")
        section_layout.addWidget(desc)
        
        double_btn = QPushButton("Double Tap Me")
        double_btn.setFixedHeight(60)
        double_btn.clicked.connect(self.on_double_tap)
        section_layout.addWidget(double_btn)
        
        layout.addWidget(section)
        
    def create_test_section(self, title):
        """Create a test section with frame and title"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        frame.setLineWidth(2)
        
        layout = QVBoxLayout()
        frame.setLayout(layout)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title_label)
        
        return frame
        
    def record_touch(self, button_id):
        """Record a touch event"""
        self.touch_count += 1
        
        # Record by size if it's a size test
        if button_id in self.button_sizes:
            self.button_sizes[button_id] += 1
        
        # Track timing
        current_time = QTime.currentTime()
        if self.last_touch_time:
            ms_diff = self.last_touch_time.msecsTo(current_time)
            print(f"[INFO] Touch #{self.touch_count}: {button_id} "
                  f"({ms_diff}ms since last)")
        else:
            print(f"[INFO] Touch #{self.touch_count}: {button_id}")
        
        self.last_touch_time = current_time
        
        # Update display
        self.update_stats()
        
    def on_button_pressed(self, button):
        """Handle button press (for long press test)"""
        button.setStyleSheet("background-color: #00ff00;")
        print("[INFO] Button pressed - holding...")
        
    def on_button_released(self, button):
        """Handle button release"""
        button.setStyleSheet("")
        print("[INFO] Button released")
        self.record_touch("long-press")
        
    def on_double_tap(self):
        """Handle double tap"""
        current_time = QTime.currentTime()
        
        if self.last_touch_time:
            ms_diff = self.last_touch_time.msecsTo(current_time)
            if ms_diff < 500:  # Double tap within 500ms
                print("[PASS] Double tap detected!")
            else:
                print(f"[INFO] Single tap ({ms_diff}ms - too slow for double tap)")
        
        self.record_touch("double-tap-attempt")
        
    def get_stats_text(self):
        """Generate statistics text"""
        stats = [
            f"Total Touches: {self.touch_count}",
            "",
            "Touches by Button Size:"
        ]
        
        for size, count in self.button_sizes.items():
            stats.append(f"  {size}: {count}")
        
        return "\n".join(stats)
        
    def update_stats(self):
        """Update statistics display"""
        self.stats_label.setText(self.get_stats_text())
        
    def reset_stats(self):
        """Reset all statistics"""
        self.touch_count = 0
        for key in self.button_sizes:
            self.button_sizes[key] = 0
        self.last_touch_time = None
        self.update_stats()
        print("[INFO] Statistics reset")
        
    def setup_theme(self):
        """Apply dark theme to match DeadStream aesthetic"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
            QLabel {
                color: #ffffff;
            }
            QFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            }
        """)


def main():
    """Run the touch responsiveness test"""
    print("=" * 60)
    print("DeadStream Touch Responsiveness Test")
    print("Phase 6 Task 6.4")
    print("=" * 60)
    print()
    print("[INFO] Starting touch test application...")
    print("[INFO] Test various button sizes and spacing")
    print("[INFO] Statistics will be displayed and logged")
    print()
    
    app = QApplication(sys.argv)
    window = TouchTestWindow()
    window.show()
    
    print("[INFO] Touch test window displayed")
    print("[INFO] Begin testing by tapping buttons")
    print()
    
    exit_code = app.exec_()
    
    print()
    print("=" * 60)
    print("Touch Test Complete")
    print("=" * 60)
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
