#!/usr/bin/env python3
"""
Player screen placeholder for DeadStream UI.
Shows now-playing interface with playback controls.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class PlayerScreen(QWidget):
    """
    Placeholder for the Player screen.
    Will be fully implemented in Phase 8.
    """
    
    # Signals
    browse_requested = pyqtSignal()  # User wants to browse shows
    
    def __init__(self):
        """Initialize player screen placeholder"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Set up the placeholder UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title = QLabel("PLAYER SCREEN")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Info text
        info = QLabel("Now playing interface\n(Placeholder - Phase 8)")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        # Browse button
        browse_btn = QPushButton("Browse Shows")
        browse_btn.setMinimumSize(200, 60)
        browse_btn.clicked.connect(self.on_browse_clicked)
        layout.addWidget(browse_btn)
        
        self.setLayout(layout)
        print("[INFO] PlayerScreen placeholder initialized")
    
    def on_browse_clicked(self):
        """Handle browse button click"""
        print("[INFO] Browse button clicked from Player screen")
        self.browse_requested.emit()