"""
Centralized theme manager for DeadStream UI.
All styling constants and helper methods in one place.
"""

class Theme:
    """
    Single source of truth for all DeadStream styling.
    Change colors, fonts, spacing here to update entire app.
    """
    
    # ============================================
    # BACKGROUND COLORS
    # ============================================
    BG_PRIMARY = "#2E2870"      # Deep purple - main background
    BG_PANEL_DARK = "#1A2332"   # Dark blue-gray - concert info panel
    BG_PANEL_BLACK = "#000000"  # Pure black - player panel
    BG_CARD = "#1E2936"         # Darker gray - list items

    # Aliases for test compatibility
    BG_BLACK = "#000000"        # Alias for BG_PANEL_BLACK
    BG_NAVY = "#1A2332"         # Alias for BG_PANEL_DARK
    
    # ============================================
    # ACCENT COLORS
    # ============================================
    ACCENT_YELLOW = "#FFD700"   # Primary CTA buttons (gold)
    ACCENT_GREEN = "#0F9D58"    # Selected/active state
    ACCENT_BLUE = "#1976D2"     # Secondary actions
    ACCENT_RED = "#FF0000"      # Destructive/exciting actions
    
    # ============================================
    # TEXT COLORS
    # ============================================
    TEXT_PRIMARY = "#FFFFFF"    # Main text (white)
    TEXT_SECONDARY = "#B0B0B0"  # Secondary/meta text (gray)
    TEXT_DARK = "#1A1A1A"       # Dark text for light backgrounds
    
    # ============================================
    # BORDER COLORS
    # ============================================
    BORDER_SUBTLE = "#333333"   # Subtle dividers
    BORDER_PANEL = "#2A3F5F"    # Panel borders
    
    # ============================================
    # BADGE COLORS
    # ============================================
    BADGE_RATING = "#00BCD4"    # Star rating badge (cyan)
    BADGE_SOURCE = "#FFD700"    # Source badge (SBD/AUD)
    
    # ============================================
    # GRADIENT COLORS
    # ============================================
    GRADIENT_START = "#9C27B0"  # Purple start
    GRADIENT_END = "#2196F3"    # Blue end
    BG_GRADIENT_END = "#2196F3" # Alias for GRADIENT_END (test compatibility)
    
    # ============================================
    # TYPOGRAPHY
    # ============================================
    # Font Sizes (in pixels)
    HEADER_LARGE = 48           # Main headers
    HEADER_MEDIUM = 36          # Section headers
    HEADER_SMALL = 24           # Sub-headers
    BODY_LARGE = 20             # Large body text
    BODY_MEDIUM = 16            # Normal body text
    BODY_SMALL = 14             # Small body text
    META_TEXT = 12              # Tiny metadata text
    
    # Font Weights
    WEIGHT_BOLD = "bold"
    WEIGHT_NORMAL = "normal"
    
    # Font Family
    FONT_FAMILY = "sans-serif"
    
    # ============================================
    # SPACING & LAYOUT
    # ============================================
    # Padding/Margins
    SPACING_TINY = 4            # 4px - minimal gap
    SPACING_SMALL = 8           # 8px - small gap
    SPACING_MEDIUM = 16         # 16px - standard gap
    SPACING_LARGE = 24          # 24px - large gap
    SPACING_XLARGE = 32         # 32px - extra large gap
    SPACING_XXLARGE = 48        # 48px - extra extra large gap
    
    MARGIN_SMALL = 8
    MARGIN_MEDIUM = 16
    MARGIN_LARGE = 24
    MARGIN_XLARGE = 32
    
    # Component Spacing
    BUTTON_SPACING = 16         # Space between buttons
    LIST_ITEM_SPACING = 8       # Space between list items
    PANEL_PADDING = 20          # Padding inside panels
    
    # ============================================
    # COMPONENT SIZES
    # ============================================
    # Buttons
    BUTTON_HEIGHT = 60          # Standard button height (touch-friendly)
    BUTTON_HEIGHT_SMALL = 48    # Smaller button height
    BUTTON_MIN_WIDTH = 120      # Minimum button width
    BUTTON_RADIUS = 30          # Border radius for pill buttons
    
    # Icons
    ICON_SMALL = 24             # Small icons
    ICON_MEDIUM = 32            # Medium icons
    ICON_LARGE = 48             # Large icons
    
    # Badges
    BADGE_HEIGHT = 28           # Badge height
    BADGE_WIDTH = 80            # Badge width
    BADGE_RADIUS = 14           # Badge border radius
    
    # List Items
    LIST_ITEM_HEIGHT = 80       # Concert list item height
    LIST_ITEM_PADDING = 12      # Padding inside list items
    
    # Progress Bar
    PROGRESS_HEIGHT = 8         # Progress bar height
    PROGRESS_HANDLE_SIZE = 20   # Draggable handle size
    
    # ============================================
    # HELPER METHODS
    # ============================================
    
    @classmethod
    def get_button_style(cls, bg_color, text_color=None):
        """
        Generate standard button stylesheet with enhanced touch feedback.

        Args:
            bg_color: Background color (hex)
            text_color: Text color (hex), defaults to TEXT_PRIMARY

        Returns:
            str: Complete CSS stylesheet for button

        Enhanced in Phase 10E Task 10E.8:
            - More pronounced pressed state (15% darker vs 10%)
            - Subtle padding adjustment for tactile feedback
        """
        if text_color is None:
            text_color = cls.TEXT_PRIMARY

        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: {cls.BUTTON_RADIUS}px;
                font-size: {cls.BODY_LARGE}px;
                font-weight: {cls.WEIGHT_BOLD};
                padding: 0px {cls.SPACING_LARGE}px;
                min-height: {cls.BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: {cls._lighten_color(bg_color, 10)};
            }}
            QPushButton:pressed {{
                background-color: {cls._darken_color(bg_color, 15)};
                padding: 2px {cls.SPACING_LARGE}px 0px {cls.SPACING_LARGE}px;
            }}
            QPushButton:disabled {{
                background-color: {cls.BORDER_SUBTLE};
                color: {cls.TEXT_SECONDARY};
            }}
        """
    
    @classmethod
    def get_list_style(cls):
        """
        Generate standard list widget stylesheet.
        
        Returns:
            str: Complete CSS stylesheet for list widget
        """
        return f"""
            QListWidget {{
                background-color: {cls.BG_PRIMARY};
                border: none;
                outline: none;
                font-size: {cls.BODY_MEDIUM}px;
            }}
            QListWidget::item {{
                background-color: {cls.BG_CARD};
                color: {cls.TEXT_PRIMARY};
                border: 1px solid {cls.BORDER_SUBTLE};
                border-radius: 8px;
                padding: {cls.LIST_ITEM_PADDING}px;
                margin: {cls.LIST_ITEM_SPACING}px;
                min-height: {cls.LIST_ITEM_HEIGHT}px;
            }}
            QListWidget::item:hover {{
                background-color: {cls._lighten_color(cls.BG_CARD, 5)};
            }}
            QListWidget::item:selected {{
                background-color: {cls.ACCENT_GREEN};
                color: {cls.TEXT_PRIMARY};
            }}
        """
    
    @classmethod
    def get_global_stylesheet(cls):
        """
        Generate global application stylesheet.
        Applied to main window, sets defaults for all widgets.
        
        Returns:
            str: Complete CSS stylesheet for entire application
        """
        return f"""
            /* Global Widget Defaults */
            QWidget {{
                background-color: {cls.BG_PRIMARY};
                color: {cls.TEXT_PRIMARY};
                font-family: {cls.FONT_FAMILY};
                font-size: {cls.BODY_MEDIUM}px;
            }}
            
            /* Labels */
            QLabel {{
                color: {cls.TEXT_PRIMARY};
                background-color: transparent;
            }}
            
            /* Scroll Bars */
            QScrollBar:vertical {{
                background-color: {cls.BG_PANEL_DARK};
                width: 12px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background-color: {cls.BORDER_SUBTLE};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {cls.TEXT_SECONDARY};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            /* Input Fields */
            QLineEdit {{
                background-color: {cls.BG_CARD};
                color: {cls.TEXT_PRIMARY};
                border: 1px solid {cls.BORDER_SUBTLE};
                border-radius: 8px;
                padding: {cls.SPACING_SMALL}px {cls.SPACING_MEDIUM}px;
                font-size: {cls.BODY_MEDIUM}px;
            }}
            QLineEdit:focus {{
                border: 1px solid {cls.ACCENT_BLUE};
            }}
            
            /* Combo Boxes */
            QComboBox {{
                background-color: {cls.BG_CARD};
                color: {cls.TEXT_PRIMARY};
                border: 1px solid {cls.BORDER_SUBTLE};
                border-radius: 8px;
                padding: {cls.SPACING_SMALL}px {cls.SPACING_MEDIUM}px;
                font-size: {cls.BODY_MEDIUM}px;
            }}
            QComboBox:hover {{
                border: 1px solid {cls.ACCENT_BLUE};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {cls.TEXT_PRIMARY};
            }}
            
            /* Sliders */
            QSlider::groove:horizontal {{
                background-color: {cls.BG_CARD};
                height: {cls.PROGRESS_HEIGHT}px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background-color: {cls.ACCENT_YELLOW};
                width: {cls.PROGRESS_HANDLE_SIZE}px;
                height: {cls.PROGRESS_HANDLE_SIZE}px;
                border-radius: {cls.PROGRESS_HANDLE_SIZE // 2}px;
                margin: -{cls.PROGRESS_HANDLE_SIZE // 4}px 0;
            }}
            QSlider::sub-page:horizontal {{
                background-color: {cls.ACCENT_YELLOW};
                border-radius: 4px;
            }}
        """
    
    @classmethod
    def get_gradient_background(cls, start_color=None, end_color=None):
        """
        Generate gradient background stylesheet.
        
        Args:
            start_color: Starting color (hex), defaults to GRADIENT_START
            end_color: Ending color (hex), defaults to GRADIENT_END
            
        Returns:
            str: CSS stylesheet with linear gradient
        """
        start = start_color or cls.GRADIENT_START
        end = end_color or cls.GRADIENT_END
        
        return f"""
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 {start},
                stop:1 {end}
            );
        """
    
    # ============================================
    # COLOR MANIPULATION UTILITIES
    # ============================================
    
    @staticmethod
    def _lighten_color(hex_color, percent):
        """
        Lighten a hex color by a percentage.
        
        Args:
            hex_color: Color in hex format (e.g. "#FF0000")
            percent: Percentage to lighten (0-100)
            
        Returns:
            str: Lightened color in hex format
        """
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        
        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Lighten
        r = min(255, int(r + (255 - r) * percent / 100))
        g = min(255, int(g + (255 - g) * percent / 100))
        b = min(255, int(b + (255 - b) * percent / 100))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def _darken_color(hex_color, percent):
        """
        Darken a hex color by a percentage.
        
        Args:
            hex_color: Color in hex format (e.g. "#FF0000")
            percent: Percentage to darken (0-100)
            
        Returns:
            str: Darkened color in hex format
        """
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        
        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Darken
        r = max(0, int(r * (1 - percent / 100)))
        g = max(0, int(g * (1 - percent / 100)))
        b = max(0, int(b * (1 - percent / 100)))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
