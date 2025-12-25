"""
Keyboard input handler for DeadStream UI
Provides keyboard shortcuts for testing and navigation
"""

from PyQt5.QtCore import Qt, QObject, pyqtSignal


class KeyboardHandler(QObject):
    """
    Handles keyboard shortcuts for UI navigation and control
    
    Signals emitted for:
    - Navigation (arrow keys, page up/down)
    - Playback control (space, media keys)
    - UI actions (escape, enter, etc)
    """
    
    # Navigation signals
    navigate_up = pyqtSignal()
    navigate_down = pyqtSignal()
    navigate_left = pyqtSignal()
    navigate_right = pyqtSignal()
    page_up = pyqtSignal()
    page_down = pyqtSignal()
    
    # Playback signals
    play_pause = pyqtSignal()
    next_track = pyqtSignal()
    previous_track = pyqtSignal()
    volume_up = pyqtSignal()
    volume_down = pyqtSignal()
    
    # UI action signals
    back = pyqtSignal()
    select = pyqtSignal()
    menu = pyqtSignal()
    quit_app = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._enabled = True
    
    def handle_key_press(self, event):
        """
        Handle keyboard key press events
        
        Args:
            event: QKeyEvent from Qt
            
        Returns:
            bool: True if key was handled, False otherwise
        """
        if not self._enabled:
            return False
        
        key = event.key()
        
        # Navigation keys
        if key == Qt.Key_Up:
            self.navigate_up.emit()
            return True
        elif key == Qt.Key_Down:
            self.navigate_down.emit()
            return True
        elif key == Qt.Key_Left:
            self.navigate_left.emit()
            return True
        elif key == Qt.Key_Right:
            self.navigate_right.emit()
            return True
        elif key == Qt.Key_PageUp:
            self.page_up.emit()
            return True
        elif key == Qt.Key_PageDown:
            self.page_down.emit()
            return True
        
        # Playback controls
        elif key == Qt.Key_Space:
            self.play_pause.emit()
            return True
        elif key == Qt.Key_N:
            self.next_track.emit()
            return True
        elif key == Qt.Key_P:
            self.previous_track.emit()
            return True
        elif key == Qt.Key_Plus or key == Qt.Key_Equal:
            self.volume_up.emit()
            return True
        elif key == Qt.Key_Minus:
            self.volume_down.emit()
            return True
        
        # UI actions
        elif key == Qt.Key_Escape:
            self.back.emit()
            return True
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            self.select.emit()
            return True
        elif key == Qt.Key_M:
            self.menu.emit()
            return True
        elif key == Qt.Key_Q:
            self.quit_app.emit()
            return True
        
        # Key not handled
        return False
    
    def enable(self):
        """Enable keyboard input handling"""
        self._enabled = True
    
    def disable(self):
        """Disable keyboard input handling"""
        self._enabled = False
    
    def is_enabled(self):
        """Check if keyboard handling is enabled"""
        return self._enabled
    
    def get_shortcuts_help(self):
        """
        Get list of keyboard shortcuts for help display
        
        Returns:
            dict: Dictionary of categories with shortcuts
        """
        return {
            'Navigation': {
                'Up/Down/Left/Right': 'Navigate menu items',
                'Page Up/Down': 'Scroll through lists',
                'Enter': 'Select item',
                'Escape': 'Go back',
                'M': 'Toggle menu'
            },
            'Playback': {
                'Space': 'Play/Pause',
                'N': 'Next track',
                'P': 'Previous track',
                '+/-': 'Volume up/down'
            },
            'System': {
                'Q': 'Quit application'
            }
        }