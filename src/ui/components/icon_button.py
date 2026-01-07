"""
IconButton - Circular icon button for navigation and actions.

Used for home, settings, search, and other icon-based controls.
Touch-friendly 60px × 60px size with circular appearance.
"""

import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from src.ui.styles.theme import Theme


class IconButton(QPushButton):
    """
    Circular icon button for navigation and actions.
    
    Icon Types:
        - 'home': House symbol for home/back navigation
        - 'settings': Gear symbol for settings
        - 'search': Search symbol for search
        - 'back': Left triangle for back navigation
        - 'forward': Right triangle for forward navigation
        - 'close': X mark for close/dismiss
        - 'menu': Hamburger menu (three lines)
        - 'random': Die face for random/shuffle
        - 'play': Play button for media playback
        - 'pause': Pause button for media control
        - 'skip': Next track button
        - 'star': Star for favorites/ratings
        - 'heart': Heart for favorites
        - 'volume': Music note for audio
        - 'info': Information icon
        - 'plus': Plus sign for add actions
        - 'minus': Minus sign for remove actions
    
    Variants:
        - 'solid': Opaque background (default)
        - 'transparent': Semi-transparent background
        - 'outline': No fill, just outline
        - 'accent': Yellow accent background
    
    Features:
        - Touch-friendly 60px × 60px target
        - Circular appearance
        - Automatic hover/pressed states
        - Supports custom icons via text override
        - Uses Unicode symbols for cross-platform compatibility
    
    Example:
        home_btn = IconButton('home', variant='transparent')
        home_btn.clicked.connect(self.go_home)
    """
    
    # Icon character mappings (Unicode symbols and emojis)
    # Using cross-platform compatible characters for Raspberry Pi
    ICONS = {
        'home': '⌂',            # House symbol (Unicode, no variant)
        'settings': '⚙',        # Gear symbol (verified working)
        'search': '⌕',          # Search symbol (Unicode alternative)
        'back': '◀',            # Left-pointing triangle
        'forward': '▶',         # Right-pointing triangle
        'close': '✕',           # Heavy multiplication X
        'menu': '☰',            # Trigram (hamburger menu)
        'random': '⚄',          # Die face (Unicode dice symbol)
        'play': '▶',            # Play triangle
        'pause': '⏸',           # Pause button
        'skip': '⏭',            # Next track button
        'star': '★',            # Star (Unicode, no variant)
        'heart': '♥',           # Heart (Unicode, no variant)
        'volume': '♪',          # Music note (Unicode alternative)
        'info': 'ℹ',            # Information (verified working)
        'plus': '➕',           # Plus/add
        'minus': '➖',          # Minus/remove
    }
    
    def __init__(self, icon_type='home', variant='solid', parent=None):
        """
        Initialize IconButton.
        
        Args:
            icon_type (str): Icon type - 'home', 'settings', 'search', etc.
            variant (str): Style variant - 'solid', 'transparent', 'outline'
            parent (QWidget): Parent widget
        """
        super().__init__(parent)
        
        # Store configuration
        self.icon_type = icon_type
        self.variant = variant
        
        # Set icon text
        icon_char = self.ICONS.get(icon_type, '\u2302')  # Default to home
        self.setText(icon_char)
        
        # Set large font for icon
        font = QFont()
        font.setFamily(Theme.FONT_FAMILY)
        font.setPixelSize(Theme.ICON_MEDIUM)
        self.setFont(font)
        
        # Apply styling
        self._apply_style()
        
        # Set fixed size (square touch target)
        self.setFixedSize(Theme.BUTTON_HEIGHT, Theme.BUTTON_HEIGHT)
        
        # Set cursor
        self.setCursor(Qt.PointingHandCursor)
    
    def _apply_style(self):
        """Apply theme-based stylesheet for current variant."""
        
        if self.variant == 'solid':
            # Opaque background
            bg_color = Theme.BG_CARD
            text_color = Theme.TEXT_PRIMARY
            hover_bg = Theme._lighten_color(bg_color, 15)
            pressed_bg = Theme._darken_color(bg_color, 10)
            
            stylesheet = f"""
                QPushButton {{
                    background-color: {bg_color};
                    color: {text_color};
                    border: none;
                    border-radius: {Theme.BUTTON_HEIGHT // 2}px;
                }}
                QPushButton:hover {{
                    background-color: {hover_bg};
                }}
                QPushButton:pressed {{
                    background-color: {pressed_bg};
                }}
            """
        
        elif self.variant == 'transparent':
            # Semi-transparent background
            bg_color = Theme.BG_CARD
            text_color = Theme.TEXT_PRIMARY
            
            # Create semi-transparent version of bg_color
            stylesheet = f"""
                QPushButton {{
                    background-color: rgba(30, 41, 54, 0.6);
                    color: {text_color};
                    border: none;
                    border-radius: {Theme.BUTTON_HEIGHT // 2}px;
                }}
                QPushButton:hover {{
                    background-color: rgba(30, 41, 54, 0.8);
                }}
                QPushButton:pressed {{
                    background-color: rgba(30, 41, 54, 0.9);
                }}
            """
        
        elif self.variant == 'outline':
            # Just outline, no fill
            text_color = Theme.TEXT_PRIMARY
            border_color = Theme.BORDER_SUBTLE
            
            stylesheet = f"""
                QPushButton {{
                    background-color: transparent;
                    color: {text_color};
                    border: 2px solid {border_color};
                    border-radius: {Theme.BUTTON_HEIGHT // 2}px;
                }}
                QPushButton:hover {{
                    border-color: {Theme.TEXT_PRIMARY};
                    background-color: rgba(255, 255, 255, 0.1);
                }}
                QPushButton:pressed {{
                    background-color: rgba(255, 255, 255, 0.2);
                }}
            """
        
        elif self.variant == 'accent':
            # Colored background (yellow accent)
            bg_color = Theme.ACCENT_YELLOW
            text_color = Theme.TEXT_DARK
            hover_bg = Theme._lighten_color(bg_color, 10)
            pressed_bg = Theme._darken_color(bg_color, 10)
            
            stylesheet = f"""
                QPushButton {{
                    background-color: {bg_color};
                    color: {text_color};
                    border: none;
                    border-radius: {Theme.BUTTON_HEIGHT // 2}px;
                }}
                QPushButton:hover {{
                    background-color: {hover_bg};
                }}
                QPushButton:pressed {{
                    background-color: {pressed_bg};
                }}
            """
        
        else:
            # Default to solid
            bg_color = Theme.BG_CARD
            text_color = Theme.TEXT_PRIMARY
            
            stylesheet = f"""
                QPushButton {{
                    background-color: {bg_color};
                    color: {text_color};
                    border: none;
                    border-radius: {Theme.BUTTON_HEIGHT // 2}px;
                }}
            """
        
        self.setStyleSheet(stylesheet)
    
    def set_variant(self, variant):
        """
        Change button variant.
        
        Args:
            variant (str): New variant - 'solid', 'transparent', 'outline', 'accent'
        """
        self.variant = variant
        self._apply_style()
    
    def set_icon(self, icon_type):
        """
        Change the icon.
        
        Args:
            icon_type (str): New icon type - 'home', 'settings', 'search', etc.
        """
        self.icon_type = icon_type
        icon_char = self.ICONS.get(icon_type, '\u2302')
        self.setText(icon_char)
    
    def set_custom_icon(self, icon_text):
        """
        Set a custom icon character.
        
        Args:
            icon_text (str): Custom character to display
        """
        self.setText(icon_text)
    
    def sizeHint(self):
        """
        Provide preferred size hint.
        
        Returns:
            QSize: Preferred button size (60x60)
        """
        return QSize(Theme.BUTTON_HEIGHT, Theme.BUTTON_HEIGHT)