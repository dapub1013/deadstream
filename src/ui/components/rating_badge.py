"""
RatingBadge - Compact badge displaying star rating.

Used to show concert ratings in list items and detail views.
Displays star emoji and numerical rating (e.g., ⭐ 4.8).
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


class RatingBadge(QLabel):
    """
    Compact badge displaying star rating.
    
    Features:
        - Cyan background (BADGE_RATING color)
        - Star emoji + numerical rating
        - Compact size (80px × 28px)
        - Rounded corners (14px radius)
        - White text on cyan background
    
    Rating Display:
        - Shows single star emoji + number
        - Format: "⭐ 4.8"
        - Supports 0.0 to 5.0 ratings
        - One decimal place precision
    
    Example:
        badge = RatingBadge(4.8)
        layout.addWidget(badge)
    """
    
    def __init__(self, rating, parent=None):
        """
        Initialize RatingBadge.
        
        Args:
            rating (float): Rating value (0.0 to 5.0)
            parent (QWidget): Parent widget
        """
        super().__init__(parent)
        
        # Store rating
        self.rating = rating
        
        # Set text with star and rating
        self.update_rating(rating)
        
        # Apply styling
        self._apply_style()
        
        # Set fixed size
        self.setFixedSize(Theme.BADGE_WIDTH, Theme.BADGE_HEIGHT)
        
        # Center text
        self.setAlignment(Qt.AlignCenter)
    
    def _apply_style(self):
        """Apply theme-based stylesheet."""
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.BADGE_RATING};
                color: {Theme.TEXT_PRIMARY};
                border-radius: {Theme.BADGE_RADIUS}px;
                font-size: {Theme.META_TEXT}px;
                font-weight: {Theme.WEIGHT_BOLD};
                padding: 0px;
            }}
        """)
    
    def update_rating(self, rating):
        """
        Update the displayed rating.
        
        Args:
            rating (float): New rating value (0.0 to 5.0)
        """
        self.rating = rating
        
        # Clamp rating to valid range
        rating = max(0.0, min(5.0, rating))
        
        # Format: star emoji + rating number
        self.setText(f"⭐ {rating:.1f}")
    
    def get_rating(self):
        """
        Get the current rating value.
        
        Returns:
            float: Current rating
        """
        return self.rating