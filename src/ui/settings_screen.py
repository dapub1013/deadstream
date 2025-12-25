#!/usr/bin/env python3
"""
Settings screen placeholder for DeadStream UI.
Device configuration and preferences.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class SettingsScreen(QWidget):
    """
    Placeholder for the Settings screen.
    Configuration options for the device.
    """
    
    # Signals
    browse_requested = pyqtSignal()  # Return to browse
    
    def __init__(self):
        """Initialize settings screen placeholder"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Set up the placeholder UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title = QLabel("SETTINGS SCREEN")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Info text
        info = QLabel("Configuration options\n(Placeholder)")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        # Back button
        back_btn = QPushButton("Back to Browse")
        back_btn.setMinimumSize(200, 60)
        back_btn.clicked.connect(self.on_back_clicked)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)
        print("[INFO] SettingsScreen placeholder initialized")
    
    def on_back_clicked(self):
        """Handle back button click"""
        print("[INFO] Back button clicked from Settings screen")
        self.browse_requested.emit()