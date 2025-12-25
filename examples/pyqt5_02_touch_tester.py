#!/usr/bin/env python3
"""
PyQt5 Learning Exercise 2: Touch Button Tester
Demonstrates: Grid layouts, button sizing, state management, dynamic styling
Tests the 60x60px button standard from Phase 1
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout, 
                            QPushButton, QLabel, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

class TouchButtonTester(QWidget):
    def __init__(self):
        super().__init__()
        self.last_button = "None"
        self.button_presses = {
            '40x40': 0,
            '44x44': 0, 
            '60x60': 0,
            '80x80': 0
        }
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Window setup
        self.setWindowTitle("DeadStream Touch Button Tester")
        self.setGeometry(100, 100, 600, 500)
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Touch Target Size Comparison")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; margin: 15px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Click each button size to compare ease of use")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 14px; margin-bottom: 10px; color: #90CAF9;")
        main_layout.addWidget(instructions)
        
        # Status label
        self.status_label = QLabel("Last pressed: None")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; margin: 10px; color: #64B5F6;")
        main_layout.addWidget(self.status_label)
        
        # Button test area
        button_group = self.create_button_test_area()
        main_layout.addWidget(button_group)
        
        # Statistics
        self.stats_label = QLabel(self.get_stats_text())
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 14px; margin: 15px; color: #81C784;")
        main_layout.addWidget(self.stats_label)
        
        # Control buttons
        control_layout = QGridLayout()
        
        reset_button = QPushButton("Reset Stats")
        reset_button.setFixedSize(140, 50)
        reset_button.setStyleSheet(self.get_control_button_style("#FF9800"))
        reset_button.clicked.connect(self.reset_stats)
        control_layout.addWidget(reset_button, 0, 0)
        
        quit_button = QPushButton("Quit")
        quit_button.setFixedSize(140, 50)
        quit_button.setStyleSheet(self.get_control_button_style("#D32F2F"))
        quit_button.clicked.connect(self.close)
        control_layout.addWidget(quit_button, 0, 1)
        
        main_layout.addLayout(control_layout)
        
        # Set layout
        self.setLayout(main_layout)
    
    def create_button_test_area(self):
        """Create the button testing grid"""
        group = QGroupBox("Button Sizes (Phase 1 Standard)")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #424242;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(30)  # Space between buttons
        
        # Button configurations: (size, label, row, col, color)
        buttons = [
            (40, '40x40', 0, 0, '#E53935'),   # Red - too small
            (44, '44x44', 0, 1, '#FB8C00'),   # Orange - borderline  
            (60, '60x60', 1, 0, '#43A047'),   # Green - optimal
            (80, '80x80', 1, 1, '#1E88E5'),   # Blue - large
        ]
        
        for size, label, row, col, color in buttons:
            button = self.create_test_button(size, label, color)
            # Center the button in its grid cell
            layout.addWidget(button, row, col, Qt.AlignCenter)
        
        group.setLayout(layout)
        return group
    
    def create_test_button(self, size, label, color):
        """Create a test button with specified size and styling"""
        button = QPushButton(label)
        button.setFixedSize(size, size)
        button.setStyleSheet(f"""
            QPushButton {{
                font-size: 12px;
                font-weight: bold;
                background-color: {color};
                border-radius: 5px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """)
        
        # Connect to handler
        button.clicked.connect(lambda: self.on_test_button_click(label))
        
        return button
    
    def on_test_button_click(self, size):
        """Handle test button clicks"""
        self.last_button = size
        self.button_presses[size] += 1
        
        # Update status
        self.status_label.setText(f"Last pressed: {size}")
        
        # Update stats
        self.stats_label.setText(self.get_stats_text())
        
        # Print to console (for learning)
        print(f"[INFO] Button pressed: {size} (Total: {self.button_presses[size]})")
    
    def reset_stats(self):
        """Reset all statistics"""
        for key in self.button_presses:
            self.button_presses[key] = 0
        self.last_button = "None"
        self.status_label.setText("Last pressed: None")
        self.stats_label.setText(self.get_stats_text())
        print("[INFO] Statistics reset")
    
    def get_stats_text(self):
        """Generate statistics display text"""
        stats = " | ".join([f"{size}: {count}" 
                           for size, count in self.button_presses.items()])
        return f"Press Count: {stats}"
    
    def get_control_button_style(self, color):
        """Generate stylesheet for control buttons"""
        return f"""
            QPushButton {{
                font-size: 14px;
                font-weight: bold;
                background-color: {color};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """
    
    def lighten_color(self, hex_color):
        """Lighten a hex color for hover state"""
        # Simple color lightening (you'll learn more sophisticated methods later)
        color_map = {
            '#E53935': '#EF5350',
            '#FB8C00': '#FFA726',
            '#43A047': '#66BB6A',
            '#1E88E5': '#42A5F5',
            '#FF9800': '#FFB74D',
            '#D32F2F': '#F44336'
        }
        return color_map.get(hex_color, hex_color)
    
    def darken_color(self, hex_color):
        """Darken a hex color for pressed state"""
        color_map = {
            '#E53935': '#C62828',
            '#FB8C00': '#E65100',
            '#43A047': '#2E7D32',
            '#1E88E5': '#1565C0',
            '#FF9800': '#EF6C00',
            '#D32F2F': '#B71C1C'
        }
        return color_map.get(hex_color, hex_color)
    
    def apply_dark_theme(self):
        """Apply dark theme (from Phase 1 testing)"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.setPalette(palette)

def main():
    print("[INFO] Starting Touch Button Tester")
    print("[INFO] This validates the 60x60px button standard from Phase 1")
    
    app = QApplication(sys.argv)
    window = TouchButtonTester()
    window.show()
    
    print("[INFO] Window displayed - Test different button sizes")
    print("[INFO] Click each button multiple times to compare ease of use")
    
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())