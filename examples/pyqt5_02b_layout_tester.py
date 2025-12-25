#!/usr/bin/env python3
"""
PyQt5 Learning Exercise 2B: Layout Tester with Favorites
Demonstrates: Multiple layouts, favorite indicators, fullscreen testing
Tests different button sizes and grid configurations
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                            QGridLayout, QPushButton, QLabel, QGroupBox, 
                            QComboBox, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont

class LayoutTester(QWidget):
    def __init__(self):
        super().__init__()
        self.button_presses = {}
        self.current_layout = '2-column'
        self.button_size = 80
        self.is_fullscreen = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Window setup
        self.setWindowTitle("DeadStream Layout Tester")
        self.setGeometry(100, 100, 800, 600)
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Main layout
        self.main_layout = QVBoxLayout()
        
        # Control panel
        self.create_control_panel()
        
        # Button test area (will be recreated when layout changes)
        self.button_test_widget = None
        self.recreate_button_area()
        
        # Statistics
        self.stats_label = QLabel(self.get_stats_text())
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 14px; margin: 10px; color: #81C784;")
        self.main_layout.addWidget(self.stats_label)
        
        # Set layout
        self.setLayout(self.main_layout)
    
    def create_control_panel(self):
        """Create the control panel with layout options"""
        control_group = QGroupBox("Test Configuration")
        control_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
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
        
        layout = QHBoxLayout()
        
        # Layout selector
        layout_label = QLabel("Grid:")
        layout_label.setStyleSheet("font-size: 12px;")
        layout.addWidget(layout_label)
        
        self.layout_combo = QComboBox()
        self.layout_combo.addItems(['2-column', '3-column', '4-column', '1-row'])
        self.layout_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                background-color: #424242;
                border-radius: 3px;
                min-width: 100px;
            }
        """)
        self.layout_combo.currentTextChanged.connect(self.on_layout_changed)
        layout.addWidget(self.layout_combo)
        
        layout.addSpacing(20)
        
        # Button size selector
        size_label = QLabel("Button Size:")
        size_label.setStyleSheet("font-size: 12px;")
        layout.addWidget(size_label)
        
        self.size_combo = QComboBox()
        self.size_combo.addItems(['60x60', '70x70', '80x80', '90x90', '100x100'])
        self.size_combo.setCurrentText('80x80')
        self.size_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                background-color: #424242;
                border-radius: 3px;
                min-width: 80px;
            }
        """)
        self.size_combo.currentTextChanged.connect(self.on_size_changed)
        layout.addWidget(self.size_combo)
        
        layout.addSpacing(20)
        
        # Fullscreen toggle
        self.fullscreen_checkbox = QCheckBox("Fullscreen (F11)")
        self.fullscreen_checkbox.setStyleSheet("font-size: 12px;")
        self.fullscreen_checkbox.stateChanged.connect(self.toggle_fullscreen)
        layout.addWidget(self.fullscreen_checkbox)
        
        layout.addStretch()
        
        # Reset button
        reset_button = QPushButton("Reset Stats")
        reset_button.setFixedSize(100, 35)
        reset_button.setStyleSheet(self.get_control_button_style("#FF9800"))
        reset_button.clicked.connect(self.reset_stats)
        layout.addWidget(reset_button)
        
        control_group.setLayout(layout)
        self.main_layout.addWidget(control_group)
    
    def recreate_button_area(self):
        """Recreate the button test area with current settings"""
        # Remove old widget if exists
        if self.button_test_widget:
            self.main_layout.removeWidget(self.button_test_widget)
            self.button_test_widget.deleteLater()
        
        # Create new widget
        self.button_test_widget = self.create_button_test_area()
        self.main_layout.insertWidget(1, self.button_test_widget)
    
    def create_button_test_area(self):
        """Create the button testing grid based on current settings"""
        group = QGroupBox(f"Button Test Area - {self.current_layout.upper()}")
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
        layout.setSpacing(20)
        
        # Button configurations based on layout type
        buttons = self.get_button_configurations()
        
        for label, row, col, color, is_favorite in buttons:
            button = self.create_test_button(label, color, is_favorite)
            layout.addWidget(button, row, col, Qt.AlignCenter)
        
        group.setLayout(layout)
        return group
    
    def get_button_configurations(self):
        """Get button configurations for current layout"""
        # All buttons with (label, row, col, color, is_favorite)
        
        if self.current_layout == '2-column':
            return [
                ('Play', 0, 0, '#43A047', True),      # Green - favorite
                ('Pause', 0, 1, '#1E88E5', False),    # Blue
                ('Next', 1, 0, '#FB8C00', False),     # Orange
                ('Previous', 1, 1, '#9C27B0', False), # Purple
            ]
        
        elif self.current_layout == '3-column':
            return [
                ('Prev', 0, 0, '#9C27B0', False),     # Purple
                ('Play', 0, 1, '#43A047', True),      # Green - favorite
                ('Next', 0, 2, '#FB8C00', False),     # Orange
                ('Stop', 1, 0, '#E53935', False),     # Red
                ('Vol-', 1, 1, '#607D8B', False),     # Gray
                ('Vol+', 1, 2, '#607D8B', False),     # Gray
            ]
        
        elif self.current_layout == '4-column':
            return [
                ('Prev', 0, 0, '#9C27B0', False),     # Purple
                ('Play', 0, 1, '#43A047', True),      # Green - favorite
                ('Pause', 0, 2, '#1E88E5', False),    # Blue
                ('Next', 0, 3, '#FB8C00', False),     # Orange
                ('Repeat', 1, 0, '#00ACC1', False),   # Cyan
                ('Vol-', 1, 1, '#607D8B', False),     # Gray
                ('Vol+', 1, 2, '#607D8B', False),     # Gray
                ('Shuffle', 1, 3, '#00ACC1', False),  # Cyan
            ]
        
        else:  # 1-row
            return [
                ('Prev', 0, 0, '#9C27B0', False),     # Purple
                ('Play', 0, 1, '#43A047', True),      # Green - favorite
                ('Pause', 0, 2, '#1E88E5', False),    # Blue
                ('Next', 0, 3, '#FB8C00', False),     # Orange
                ('Stop', 0, 4, '#E53935', False),     # Red
            ]
    
    def create_test_button(self, label, color, is_favorite):
        """Create a test button with optional favorite indicator"""
        button = QPushButton()
        button.setFixedSize(self.button_size, self.button_size)
        
        # Create button text with favorite indicator
        if is_favorite:
            # Star indicator for favorite (ASCII only)
            display_text = f"[*] {label}"
            button_color = color
            border = "border: 3px solid #FFD700;"  # Gold border for favorite
        else:
            display_text = label
            button_color = color
            border = ""
        
        button.setText(display_text)
        button.setStyleSheet(f"""
            QPushButton {{
                font-size: {max(10, self.button_size // 8)}px;
                font-weight: bold;
                background-color: {button_color};
                border-radius: 5px;
                color: white;
                {border}
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(button_color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(button_color)};
            }}
        """)
        
        # Connect to handler
        button.clicked.connect(lambda: self.on_test_button_click(label))
        
        return button
    
    def on_test_button_click(self, label):
        """Handle test button clicks"""
        # Track presses
        if label not in self.button_presses:
            self.button_presses[label] = 0
        self.button_presses[label] += 1
        
        # Update stats
        self.stats_label.setText(self.get_stats_text())
        
        # Console output
        print(f"[INFO] Button pressed: {label} (Total: {self.button_presses[label]})")
    
    def on_layout_changed(self, layout_name):
        """Handle layout selection change"""
        self.current_layout = layout_name
        self.recreate_button_area()
        print(f"[INFO] Layout changed to: {layout_name}")
    
    def on_size_changed(self, size_text):
        """Handle button size change"""
        self.button_size = int(size_text.split('x')[0])
        self.recreate_button_area()
        print(f"[INFO] Button size changed to: {self.button_size}x{self.button_size}")
    
    def toggle_fullscreen(self, state):
        """Toggle fullscreen mode"""
        if state == Qt.Checked:
            self.showFullScreen()
            self.is_fullscreen = True
            print("[INFO] Fullscreen enabled (Press ESC or F11 to exit)")
        else:
            self.showNormal()
            self.is_fullscreen = False
            print("[INFO] Fullscreen disabled")
    
    def keyPressEvent(self, event):
        """Handle keyboard events"""
        if event.key() == Qt.Key_F11:
            # Toggle fullscreen
            self.fullscreen_checkbox.setChecked(not self.is_fullscreen)
        elif event.key() == Qt.Key_Escape and self.is_fullscreen:
            # Exit fullscreen
            self.fullscreen_checkbox.setChecked(False)
    
    def reset_stats(self):
        """Reset all statistics"""
        self.button_presses.clear()
        self.stats_label.setText(self.get_stats_text())
        print("[INFO] Statistics reset")
    
    def get_stats_text(self):
        """Generate statistics display text"""
        if not self.button_presses:
            return "Press Count: (no presses yet)"
        
        stats = " | ".join([f"{btn}: {count}" 
                           for btn, count in sorted(self.button_presses.items())])
        return f"Press Count: {stats}"
    
    def get_control_button_style(self, color):
        """Generate stylesheet for control buttons"""
        return f"""
            QPushButton {{
                font-size: 12px;
                font-weight: bold;
                background-color: {color};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
        """
    
    def lighten_color(self, hex_color):
        """Lighten a hex color for hover state"""
        color_map = {
            '#E53935': '#EF5350', '#FB8C00': '#FFA726',
            '#43A047': '#66BB6A', '#1E88E5': '#42A5F5',
            '#FF9800': '#FFB74D', '#D32F2F': '#F44336',
            '#9C27B0': '#AB47BC', '#607D8B': '#78909C',
            '#00ACC1': '#26C6DA'
        }
        return color_map.get(hex_color, hex_color)
    
    def darken_color(self, hex_color):
        """Darken a hex color for pressed state"""
        color_map = {
            '#E53935': '#C62828', '#FB8C00': '#E65100',
            '#43A047': '#2E7D32', '#1E88E5': '#1565C0',
            '#FF9800': '#EF6C00', '#D32F2F': '#B71C1C',
            '#9C27B0': '#7B1FA2', '#607D8B': '#455A64',
            '#00ACC1': '#00838F'
        }
        return color_map.get(hex_color, hex_color)
    
    def apply_dark_theme(self):
        """Apply dark theme"""
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
    print("[INFO] Starting Layout Tester")
    print("[INFO] Test different layouts and button sizes")
    print("[INFO] Gold border indicates recommended button")
    print("[INFO] Press F11 or check 'Fullscreen' to test at full resolution")
    
    app = QApplication(sys.argv)
    window = LayoutTester()
    window.show()
    
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())