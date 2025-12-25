#!/usr/bin/env python3
"""
Screen manager for DeadStream UI navigation.
Manages transitions between Player, Browse, and Settings screens.
"""
import sys
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import pyqtSignal

# Add project root to path
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


class ScreenManager(QStackedWidget):
    """
    Manages screen transitions for the DeadStream application.
    
    Handles navigation between:
    - Player Screen (now playing)
    - Browse Screen (find shows)
    - Settings Screen (configuration)
    """
    
    # Signals for screen changes
    screen_changed = pyqtSignal(str)  # Emits screen name
    
    # Screen constants
    PLAYER_SCREEN = "player"
    BROWSE_SCREEN = "browse"
    SETTINGS_SCREEN = "settings"
    
    def __init__(self):
        """Initialize the screen manager"""
        super().__init__()
        
        self.current_screen_name = None
        self.screens = {}
        
        print("[INFO] ScreenManager initialized")
    
    def add_screen(self, screen_name, screen_widget):
        """
        Add a screen to the manager
        
        Args:
            screen_name: Name identifier (PLAYER_SCREEN, BROWSE_SCREEN, SETTINGS_SCREEN)
            screen_widget: QWidget instance for the screen
        """
        try:
            if screen_name in self.screens:
                print(f"[WARN] Screen '{screen_name}' already exists, replacing")
            
            # Add to stacked widget
            index = self.addWidget(screen_widget)
            
            # Store reference
            self.screens[screen_name] = {
                'widget': screen_widget,
                'index': index
            }
            
            print(f"[INFO] Added screen '{screen_name}' at index {index}")
            
            # Set as current if first screen
            if len(self.screens) == 1:
                self.show_screen(screen_name)
                
        except Exception as e:
            print(f"[ERROR] Failed to add screen '{screen_name}': {e}")
    
    def show_screen(self, screen_name):
        """
        Switch to the specified screen
        
        Args:
            screen_name: Name of screen to show
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if screen_name not in self.screens:
                print(f"[ERROR] Screen '{screen_name}' not found")
                return False
            
            # Get screen info
            screen_info = self.screens[screen_name]
            index = screen_info['index']
            
            # Switch to screen
            self.setCurrentIndex(index)
            
            # Update state
            old_screen = self.current_screen_name
            self.current_screen_name = screen_name
            
            # Emit signal
            self.screen_changed.emit(screen_name)
            
            if old_screen:
                print(f"[INFO] Screen transition: {old_screen} -> {screen_name}")
            else:
                print(f"[INFO] Initial screen: {screen_name}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to show screen '{screen_name}': {e}")
            return False
    
    def get_current_screen_name(self):
        """Get the name of the currently displayed screen"""
        return self.current_screen_name
    
    def get_screen_widget(self, screen_name):
        """
        Get the widget for a specific screen
        
        Args:
            screen_name: Name of screen
            
        Returns:
            QWidget or None if screen not found
        """
        if screen_name in self.screens:
            return self.screens[screen_name]['widget']
        return None