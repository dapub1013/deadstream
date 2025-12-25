#!/usr/bin/env python3
"""
Screen manager for DeadStream UI navigation.
Manages transitions between Player, Browse, and Settings screens with smooth animations.
"""
import sys
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import pyqtSignal

# Add project root to path
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from src.ui.transitions import ScreenTransition, TransitionType


class ScreenManager(QStackedWidget):
    """
    Manages screen transitions for the DeadStream application.
    
    Handles navigation between:
    - Player Screen (now playing)
    - Browse Screen (find shows)
    - Settings Screen (configuration)
    
    Features smooth animated transitions between screens.
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
        
        # Initialize transition manager
        self.transition = ScreenTransition(self)
        
        # Track screen history for back navigation
        self.screen_history = []
        
        print("[INFO] ScreenManager initialized with transitions")
    
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
                self.show_screen(screen_name, transition_type=TransitionType.INSTANT)
                
        except Exception as e:
            print(f"[ERROR] Failed to add screen '{screen_name}': {e}")
    
    def show_screen(self, screen_name, transition_type=TransitionType.SLIDE_LEFT):
        """
        Switch to the specified screen with animation
        
        Args:
            screen_name: Name of screen to show
            transition_type: Type of transition animation (default: SLIDE_LEFT)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if screen_name not in self.screens:
                print(f"[ERROR] Screen '{screen_name}' not found")
                return False
            
            # Get screen info
            screen_info = self.screens[screen_name]
            to_index = screen_info['index']
            
            # If already on this screen, do nothing
            if self.current_screen_name == screen_name:
                print(f"[INFO] Already on screen '{screen_name}'")
                return True
            
            # Get current screen index
            from_index = self.currentIndex()
            
            # Determine transition direction
            if transition_type == TransitionType.SLIDE_LEFT or transition_type == TransitionType.SLIDE_RIGHT:
                # Determine slide direction based on screen order
                direction = self._determine_slide_direction(self.current_screen_name, screen_name)
                
                # Perform slide transition
                success = self.transition.slide_to_screen(from_index, to_index, direction)
                
            elif transition_type == TransitionType.FADE:
                # Perform fade transition
                success = self.transition.fade_to_screen(from_index, to_index)
                
            else:  # INSTANT
                # No animation
                self.transition.instant_transition(to_index)
                success = True
            
            if success:
                # Update screen history
                if self.current_screen_name:
                    self.screen_history.append(self.current_screen_name)
                
                # Update state
                old_screen = self.current_screen_name
                self.current_screen_name = screen_name
                
                # Emit signal
                self.screen_changed.emit(screen_name)
                
                if old_screen:
                    print(f"[INFO] Screen transition: {old_screen} -> {screen_name}")
                else:
                    print(f"[INFO] Initial screen: {screen_name}")
            
            return success
            
        except Exception as e:
            print(f"[ERROR] Failed to show screen '{screen_name}': {e}")
            return False
    
    def _determine_slide_direction(self, from_screen, to_screen):
        """
        Determine the slide direction based on screen order
        
        Args:
            from_screen: Current screen name
            to_screen: Target screen name
            
        Returns:
            str: "left" or "right"
        """
        # Define screen order: Player -> Browse -> Settings
        screen_order = [
            self.PLAYER_SCREEN,
            self.BROWSE_SCREEN,
            self.SETTINGS_SCREEN
        ]
        
        try:
            from_pos = screen_order.index(from_screen)
            to_pos = screen_order.index(to_screen)
            
            # Moving forward in the order -> slide left
            # Moving backward in the order -> slide right
            return "left" if to_pos > from_pos else "right"
            
        except ValueError:
            # Default to left if screens not in defined order
            return "left"
    
    def go_back(self):
        """
        Navigate to the previous screen in history
        
        Returns:
            bool: True if navigation successful, False if no history
        """
        if not self.screen_history:
            print("[INFO] No screen history to go back to")
            return False
        
        # Get previous screen
        previous_screen = self.screen_history.pop()
        
        # Navigate with slide right animation
        return self.show_screen(previous_screen, transition_type=TransitionType.SLIDE_RIGHT)
    
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
    
    def clear_history(self):
        """Clear the navigation history"""
        self.screen_history = []
        print("[INFO] Screen history cleared")
