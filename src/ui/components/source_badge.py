"""
SourceBadge - Compact badge displaying recording source type.

Used to show recording source (SBD, AUD, MTX) in concert listings.
Displays abbreviated source type with color coding.
"""

import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from src.ui.styles.theme import Theme


class SourceBadge(QLabel):
    """
    Compact badge displaying recording source type.
    
    Features:
        - Color-coded by source type
        - Compact size (80px × 28px)
        - Rounded corners (14px radius)
        - Bold uppercase text
    
    Source Types:
        - SBD: Soundboard (yellow/gold - premium)
        - AUD: Audience (blue - standard)
        - MTX: Matrix (green - blend)
        - FLAC: File format indicator (purple)
    
    Color Scheme:
        - SBD: Yellow background, dark text (premium quality)
        - AUD: Blue background, white text (standard quality)
        - MTX: Green background, white text (mixed sources)
        - FLAC: Purple background, white text (format indicator)
    
    Example:
        badge = SourceBadge('SBD')
        layout.addWidget(badge)
    """
    
    # Source type color mappings
    SOURCE_COLORS = {
        'SBD': (Theme.ACCENT_YELLOW, Theme.TEXT_DARK),      # Gold bg, dark text
        'AUD': (Theme.ACCENT_BLUE, Theme.TEXT_PRIMARY),     # Blue bg, white text
        'MTX': (Theme.ACCENT_GREEN, Theme.TEXT_PRIMARY),    # Green bg, white text
        'FLAC': ('#9C27B0', Theme.TEXT_PRIMARY),            # Purple bg, white text
        'MP3': ('#FF9800', Theme.TEXT_DARK),                # Orange bg, dark text
    }
    
    def __init__(self, source_type, parent=None):
        """
        Initialize SourceBadge.
        
        Args:
            source_type (str): Source type - 'SBD', 'AUD', 'MTX', 'FLAC', 'MP3'
            parent (QWidget): Parent widget
        """
        super().__init__(parent)
        
        # Store and normalize source type
        self.source_type = source_type.upper()
        
        # Set text
        self.setText(self.source_type)
        
        # Apply styling based on source type
        self._apply_style()
        
        # Set fixed size
        self.setFixedSize(Theme.BADGE_WIDTH, Theme.BADGE_HEIGHT)
        
        # Center text
        self.setAlignment(Qt.AlignCenter)
    
    def _apply_style(self):
        """Apply theme-based stylesheet with source-specific colors."""
        # Get colors for this source type, default to yellow if unknown
        bg_color, text_color = self.SOURCE_COLORS.get(
            self.source_type,
            (Theme.ACCENT_YELLOW, Theme.TEXT_DARK)
        )
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: {Theme.BADGE_RADIUS}px;
                font-size: {Theme.META_TEXT}px;
                font-weight: {Theme.WEIGHT_BOLD};
                padding: 0px;
            }}
        """)
    
    def set_source(self, source_type):
        """
        Update the source type.
        
        Args:
            source_type (str): New source type - 'SBD', 'AUD', 'MTX', etc.
        """
        self.source_type = source_type.upper()
        self.setText(self.source_type)
        self._apply_style()
    
    def get_source(self):
        """
        Get the current source type.
        
        Returns:
            str: Current source type
        """
        return self.source_type