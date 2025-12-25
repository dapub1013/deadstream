#!/usr/bin/env python3
"""
Browse screen placeholder for DeadStream UI.
Allows users to find and select shows.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class BrowseScreen(QWidget):
    """
    Placeholder for the Browse screen.
    Will be fully implemented in Phase 7.
    """
    
    # Signals
    player_requested = pyqtSignal()    # Return to player
    settings_requested = pyqtSignal()  # Go to settings
    
    def __init__(self):
        """Initialize browse screen placeholder"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Set up the placeholder UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title = QLabel("BROWSE SCREEN")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Info text
        info = QLabel("Show browser interface\n(Placeholder - Phase 7)")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        # Button container
        button_layout = QHBoxLayout()
        
        # Back to player button
        player_btn = QPushButton("Back to Player")
        player_btn.setMinimumSize(200, 60)
        player_btn.clicked.connect(self.on_player_clicked)
        button_layout.addWidget(player_btn)
        
        # Settings button
        settings_btn = QPushButton("Settings")
        settings_btn.setMinimumSize(200, 60)
        settings_btn.clicked.connect(self.on_settings_clicked)
        button_layout.addWidget(settings_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        print("[INFO] BrowseScreen placeholder initialized")
    
    def on_player_clicked(self):
        """Handle back to player button click"""
        print("[INFO] Player button clicked from Browse screen")
        self.player_requested.emit()
    
    def on_settings_clicked(self):
        """Handle settings button click"""
        print("[INFO] Settings button clicked from Browse screen")
        self.settings_requested.emit()