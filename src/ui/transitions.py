#!/usr/bin/env python3
"""
Screen transition animations for DeadStream UI.
Provides smooth animated transitions between screens.
"""
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint, pyqtProperty
from PyQt5.QtWidgets import QGraphicsOpacityEffect


class TransitionType:
    """Types of screen transitions"""
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    FADE = "fade"
    INSTANT = "instant"


class ScreenTransition:
    """
    Handles animated transitions between screens.
    
    Provides smooth visual feedback when navigating between
    Player, Browse, and Settings screens.
    """
    
    # Transition duration in milliseconds
    # 300ms provides responsive feel while maintaining smooth 60fps animation
    DURATION = 300
    
    def __init__(self, container):
        """
        Initialize transition manager
        
        Args:
            container: QStackedWidget that contains the screens
        """
        self.container = container
        self.animation = None
        self.is_animating = False
        
        print("[INFO] ScreenTransition initialized")
    
    def slide_to_screen(self, from_index, to_index, direction="left"):
        """
        Perform slide transition between screens
        
        Args:
            from_index: Index of current screen
            to_index: Index of target screen
            direction: "left" or "right" for slide direction
        
        Returns:
            bool: True if transition started, False if already animating
        """
        if self.is_animating:
            print("[WARN] Transition already in progress")
            return False
        
        try:
            self.is_animating = True
            
            # Get widgets
            from_widget = self.container.widget(from_index)
            to_widget = self.container.widget(to_index)
            
            if not from_widget or not to_widget:
                print("[ERROR] Invalid screen indices for transition")
                self.is_animating = False
                return False
            
            # Get container dimensions
            width = self.container.width()
            
            # Calculate starting and ending positions
            if direction == "left":
                # New screen slides in from right
                to_start = QPoint(width, 0)
                to_end = QPoint(0, 0)
                from_end = QPoint(-width, 0)
            else:  # right
                # New screen slides in from left
                to_start = QPoint(-width, 0)
                to_end = QPoint(0, 0)
                from_end = QPoint(width, 0)
            
            # Position the incoming screen
            to_widget.setGeometry(to_start.x(), to_start.y(), width, self.container.height())
            to_widget.show()
            to_widget.raise_()
            
            # Create animation for incoming screen
            self.animation = QPropertyAnimation(to_widget, b"pos")
            self.animation.setDuration(self.DURATION)
            self.animation.setStartValue(to_start)
            self.animation.setEndValue(to_end)
            self.animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # When animation completes, update the container
            self.animation.finished.connect(lambda: self._on_slide_finished(to_index))
            
            # Start animation
            self.animation.start()
            
            print(f"[INFO] Slide transition started: {direction}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Slide transition failed: {e}")
            self.is_animating = False
            # Fall back to instant transition
            self.container.setCurrentIndex(to_index)
            return False
    
    def _on_slide_finished(self, new_index):
        """
        Handle slide animation completion
        
        Args:
            new_index: Index of the new current screen
        """
        try:
            # Update the stacked widget's current index
            self.container.setCurrentIndex(new_index)
            
            # Reset animation state
            self.animation = None
            self.is_animating = False
            
            print("[INFO] Slide transition complete")
            
        except Exception as e:
            print(f"[ERROR] Error completing transition: {e}")
            self.is_animating = False
    
    def fade_to_screen(self, from_index, to_index):
        """
        Perform fade transition between screens
        
        Args:
            from_index: Index of current screen
            to_index: Index of target screen
            
        Returns:
            bool: True if transition started, False if already animating
        """
        if self.is_animating:
            print("[WARN] Transition already in progress")
            return False
        
        try:
            self.is_animating = True
            
            # Get widgets
            to_widget = self.container.widget(to_index)
            
            if not to_widget:
                print("[ERROR] Invalid screen index for transition")
                self.is_animating = False
                return False
            
            # Create opacity effect
            opacity_effect = QGraphicsOpacityEffect()
            to_widget.setGraphicsEffect(opacity_effect)
            
            # Switch to new screen
            self.container.setCurrentIndex(to_index)
            
            # Animate opacity from 0 to 1
            self.animation = QPropertyAnimation(opacity_effect, b"opacity")
            self.animation.setDuration(self.DURATION)
            self.animation.setStartValue(0.0)
            self.animation.setEndValue(1.0)
            self.animation.setEasingCurve(QEasingCurve.InOutQuad)
            
            # Clean up when done
            self.animation.finished.connect(lambda: self._on_fade_finished(to_widget))
            
            # Start animation
            self.animation.start()
            
            print("[INFO] Fade transition started")
            return True
            
        except Exception as e:
            print(f"[ERROR] Fade transition failed: {e}")
            self.is_animating = False
            # Fall back to instant transition
            self.container.setCurrentIndex(to_index)
            return False
    
    def _on_fade_finished(self, widget):
        """
        Handle fade animation completion
        
        Args:
            widget: The widget that was faded in
        """
        try:
            # Remove the opacity effect to restore normal rendering
            widget.setGraphicsEffect(None)
            
            # Reset animation state
            self.animation = None
            self.is_animating = False
            
            print("[INFO] Fade transition complete")
            
        except Exception as e:
            print(f"[ERROR] Error completing fade transition: {e}")
            self.is_animating = False
    
    def instant_transition(self, to_index):
        """
        Instantly switch to screen without animation
        
        Args:
            to_index: Index of target screen
        """
        self.container.setCurrentIndex(to_index)
        print("[INFO] Instant transition")
