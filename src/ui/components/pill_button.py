"""
PillButton - Large rounded button with configurable color variants.

Used for primary actions throughout the DeadStream UI.
Touch-friendly with 60px minimum height.
"""

import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize
from src.ui.styles.theme import Theme


class PillButton(QPushButton):
    """
    Large rounded button with theme-based color variants.
    
    Variants:
        - 'yellow': Primary CTA (gold background, dark text)
        - 'green': Selected/active state (green background, white text)
        - 'blue': Secondary action (blue background, white text)
        - 'red': Destructive/exciting action (red background, white text)
        - 'gradient': Special effect (purple to blue gradient, white text)
    
    Features:
        - Touch-friendly 60px minimum height
        - Automatic hover/pressed state styling
        - Consistent rounded corners (30px radius)
        - Disabled state support
    
    Example:
        btn = PillButton("Find a Show", variant='yellow')
        btn.clicked.connect(self.on_find_show)
    """
    
    def __init__(self, text, variant='yellow', parent=None):
        """
        Initialize PillButton.
        
        Args:
            text (str): Button label text
            variant (str): Color variant - 'yellow', 'green', 'blue', 'red', 'gradient'
            parent (QWidget): Parent widget
        """
        super().__init__(text, parent)
        
        # Store variant
        self.variant = variant
        
        # Apply theme-based styling
        self._apply_style()
        
        # Set touch-friendly minimum size
        self.setMinimumSize(Theme.BUTTON_MIN_WIDTH, Theme.BUTTON_HEIGHT)
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
        # Set cursor to pointing hand
        self.setCursor(Qt.PointingHandCursor)
    
    def _apply_style(self):
        """Apply theme-based stylesheet for current variant."""
        
        # Map variants to theme colors
        if self.variant == 'yellow':
            bg_color = Theme.ACCENT_YELLOW
            text_color = Theme.TEXT_DARK
        elif self.variant == 'green':
            bg_color = Theme.ACCENT_GREEN
            text_color = Theme.TEXT_PRIMARY
        elif self.variant == 'blue':
            bg_color = Theme.ACCENT_BLUE
            text_color = Theme.TEXT_PRIMARY
        elif self.variant == 'red':
            bg_color = Theme.ACCENT_RED
            text_color = Theme.TEXT_PRIMARY
        elif self.variant == 'gradient':
            # Gradient variant handled separately
            self._apply_gradient_style()
            return
        else:
            # Default to yellow if unknown variant
            bg_color = Theme.ACCENT_YELLOW
            text_color = Theme.TEXT_DARK
        
        # Use Theme helper method to generate stylesheet
        self.setStyleSheet(Theme.get_button_style(bg_color, text_color))
    
    def _apply_gradient_style(self):
        """
        Apply gradient background styling with enhanced touch feedback.

        Enhanced in Phase 10E Task 10E.8:
            - More pronounced pressed state (15% darker vs 10%)
            - Subtle padding adjustment for tactile feedback
        """
        gradient_style = f"""
            QPushButton {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Theme.GRADIENT_START},
                    stop:1 {Theme.GRADIENT_END}
                );
                color: {Theme.TEXT_PRIMARY};
                border: none;
                border-radius: {Theme.BUTTON_RADIUS}px;
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                padding: 0px {Theme.SPACING_LARGE}px;
                min-height: {Theme.BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Theme._lighten_color(Theme.GRADIENT_START, 10)},
                    stop:1 {Theme._lighten_color(Theme.GRADIENT_END, 10)}
                );
            }}
            QPushButton:pressed {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Theme._darken_color(Theme.GRADIENT_START, 15)},
                    stop:1 {Theme._darken_color(Theme.GRADIENT_END, 15)}
                );
                padding: 2px {Theme.SPACING_LARGE}px 0px {Theme.SPACING_LARGE}px;
            }}
            QPushButton:disabled {{
                background-color: {Theme.BORDER_SUBTLE};
                color: {Theme.TEXT_SECONDARY};
            }}
        """
        self.setStyleSheet(gradient_style)
    
    def set_variant(self, variant):
        """
        Change button color variant.
        
        Args:
            variant (str): New variant - 'yellow', 'green', 'blue', 'red', 'gradient'
        """
        self.variant = variant
        self._apply_style()
    
    def sizeHint(self):
        """
        Provide preferred size hint.
        
        Returns:
            QSize: Preferred button size
        """
        return QSize(Theme.BUTTON_MIN_WIDTH, Theme.BUTTON_HEIGHT)