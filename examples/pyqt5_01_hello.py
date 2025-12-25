#!/usr/bin/env python3
"""
PyQt5 Learning Exercise 1: Hello DeadStream
Demonstrates: Basic window, signals/slots, dark theme
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

class HelloDeadStream(QWidget):
    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Window setup
        self.setWindowTitle("Hello DeadStream")
        self.setGeometry(100, 100, 400, 300)
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add label
        self.label = QLabel("Welcome to DeadStream!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; margin: 20px;")
        layout.addWidget(self.label)
        
        # Add counter label
        self.counter_label = QLabel("Clicks: 0")
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("font-size: 18px; color: #64B5F6;")
        layout.addWidget(self.counter_label)
        
        # Add button (60x60px standard from Phase 1)
        self.button = QPushButton("Click Me!")
        self.button.setFixedSize(120, 60)  # Double width for text
        self.button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: #1976D2;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        
        # Connect signal to slot
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        
        # Add quit button
        quit_button = QPushButton("Quit")
        quit_button.setFixedSize(120, 60)
        quit_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: #D32F2F;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F44336;
            }
        """)
        quit_button.clicked.connect(self.close)
        layout.addWidget(quit_button, alignment=Qt.AlignCenter)
        
        # Set layout
        self.setLayout(layout)
    
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
    
    def on_button_click(self):
        """Handle button click (signal/slot demonstration)"""
        self.click_count += 1
        self.counter_label.setText(f"Clicks: {self.click_count}")
        
        # Update label text
        if self.click_count == 1:
            self.label.setText("Getting the hang of it!")
        elif self.click_count == 5:
            self.label.setText("You're a natural!")
        elif self.click_count == 10:
            self.label.setText("Grateful for your patience!")

def main():
    print("[INFO] Starting Hello DeadStream")
    
    app = QApplication(sys.argv)
    window = HelloDeadStream()
    window.show()
    
    print("[INFO] Window displayed - Click the button to test signals/slots")
    
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())