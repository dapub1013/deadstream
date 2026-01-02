"""
Centralized typography styles for DeadStream UI.

Based on Tailwind typography from deadhead-player-landscape-fixed.jsx.
Defines font sizes, colors, and text formatting constants.

ASCII-only. No emojis or unicode characters.
"""

# Font Sizes (px)
FONT_3XL = "30px"  # Main titles, current track
FONT_2XL = "24px"  # Section headers, concert title
FONT_XL = "20px"   # Subsection headers, dates
FONT_LG = "18px"   # Body, venue names
FONT_BASE = "16px" # Standard text
FONT_SM = "14px"   # Supporting text, metadata
FONT_XS = "12px"   # Fine print, labels

# Text Colors
TEXT_WHITE = "#FFFFFF"
TEXT_GRAY_300 = "#D1D5DB"
TEXT_GRAY_400 = "#9CA3AF"
TEXT_GRAY_500 = "#6B7280"
TEXT_GRAY_600 = "#4B5563"

# Accent Text Colors
TEXT_BLUE_500 = "#3B82F6"
TEXT_GREEN_400 = "#4ADE80"
TEXT_ORANGE_400 = "#FB923C"
TEXT_PURPLE_500 = "#A855F7"
TEXT_RED_500 = "#EF4444"
TEXT_YELLOW_500 = "#EAB308"

# Font Weights
WEIGHT_NORMAL = "normal"
WEIGHT_SEMIBOLD = "600"
WEIGHT_BOLD = "bold"

# Text Alignment
ALIGN_LEFT = "left"
ALIGN_CENTER = "center"
ALIGN_RIGHT = "right"

# Line Height Multipliers
LINE_HEIGHT_TIGHT = 1.2
LINE_HEIGHT_NORMAL = 1.5
LINE_HEIGHT_RELAXED = 1.7

# Typography Styles for Common Elements

# Main page title (3xl, bold)
TITLE_MAIN_STYLE = f"""
    font-size: {FONT_3XL};
    font-weight: {WEIGHT_BOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_TIGHT};
"""

# Section header (2xl, bold)
TITLE_SECTION_STYLE = f"""
    font-size: {FONT_2XL};
    font-weight: {WEIGHT_BOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_TIGHT};
"""

# Subsection header (xl, semibold)
TITLE_SUBSECTION_STYLE = f"""
    font-size: {FONT_XL};
    font-weight: {WEIGHT_SEMIBOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_TIGHT};
"""

# Body text (lg, normal)
TEXT_BODY_STYLE = f"""
    font-size: {FONT_LG};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_400};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Standard text (base, normal)
TEXT_STANDARD_STYLE = f"""
    font-size: {FONT_BASE};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Supporting text (sm, normal, gray)
TEXT_SUPPORTING_STYLE = f"""
    font-size: {FONT_SM};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_400};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Label text (xs, normal, gray)
TEXT_LABEL_STYLE = f"""
    font-size: {FONT_XS};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_500};
    line-height: {LINE_HEIGHT_NORMAL};
    text-transform: uppercase;
    letter-spacing: 0.05em;
"""

# Current track name (3xl, bold, white)
TRACK_TITLE_STYLE = f"""
    font-size: {FONT_3XL};
    font-weight: {WEIGHT_BOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_TIGHT};
"""

# Concert date/venue (2xl, semibold)
CONCERT_TITLE_STYLE = f"""
    font-size: {FONT_2XL};
    font-weight: {WEIGHT_SEMIBOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_TIGHT};
"""

# Venue/location text (lg, normal, gray)
VENUE_TEXT_STYLE = f"""
    font-size: {FONT_LG};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_400};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Metadata text (sm, normal, gray)
METADATA_TEXT_STYLE = f"""
    font-size: {FONT_SM};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_400};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Now playing label (sm, uppercase, gray)
NOW_PLAYING_LABEL_STYLE = f"""
    font-size: {FONT_SM};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_500};
    line-height: {LINE_HEIGHT_NORMAL};
    text-transform: uppercase;
    letter-spacing: 0.1em;
"""

# Set header (sm, uppercase, semibold, gray)
SET_HEADER_STYLE = f"""
    font-size: {FONT_SM};
    font-weight: {WEIGHT_SEMIBOLD};
    color: {TEXT_GRAY_500};
    line-height: {LINE_HEIGHT_NORMAL};
    text-transform: uppercase;
    letter-spacing: 0.1em;
"""

# Track name in setlist (base, normal)
SETLIST_TRACK_STYLE = f"""
    font-size: {FONT_BASE};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_300};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Track name in setlist (selected)
SETLIST_TRACK_SELECTED_STYLE = f"""
    font-size: {FONT_BASE};
    font-weight: {WEIGHT_SEMIBOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Track duration (sm, gray)
TRACK_DURATION_STYLE = f"""
    font-size: {FONT_SM};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_500};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Show date in browse list (xl, semibold)
SHOW_DATE_STYLE = f"""
    font-size: {FONT_XL};
    font-weight: {WEIGHT_SEMIBOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_TIGHT};
"""

# Show venue in browse list (lg, gray)
SHOW_VENUE_STYLE = f"""
    font-size: {FONT_LG};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_400};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Show location in browse list (sm, gray)
SHOW_LOCATION_STYLE = f"""
    font-size: {FONT_SM};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_500};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Rating text (xl, bold)
RATING_TEXT_STYLE = f"""
    font-size: {FONT_XL};
    font-weight: {WEIGHT_BOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_TIGHT};
"""

# Browse mode count (2xl, bold)
BROWSE_COUNT_STYLE = f"""
    font-size: {FONT_2XL};
    font-weight: {WEIGHT_BOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_TIGHT};
"""

# Browse mode description (sm, gray)
BROWSE_DESC_STYLE = f"""
    font-size: {FONT_SM};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_500};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Settings label (lg, semibold)
SETTINGS_LABEL_STYLE = f"""
    font-size: {FONT_LG};
    font-weight: {WEIGHT_SEMIBOLD};
    color: {TEXT_WHITE};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Settings value (base, normal, gray)
SETTINGS_VALUE_STYLE = f"""
    font-size: {FONT_BASE};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GRAY_400};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Error message (base, red)
ERROR_TEXT_STYLE = f"""
    font-size: {FONT_BASE};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_RED_500};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Success message (base, green)
SUCCESS_TEXT_STYLE = f"""
    font-size: {FONT_BASE};
    font-weight: {WEIGHT_NORMAL};
    color: {TEXT_GREEN_400};
    line-height: {LINE_HEIGHT_NORMAL};
"""

# Helper function to create QLabel stylesheet
def create_label_style(font_size, font_weight=WEIGHT_NORMAL, color=TEXT_WHITE, align=ALIGN_LEFT):
    """
    Create a QLabel stylesheet with specified properties.

    Args:
        font_size: Font size constant (e.g., FONT_LG)
        font_weight: Font weight constant (default: WEIGHT_NORMAL)
        color: Text color hex value (default: TEXT_WHITE)
        align: Text alignment (default: ALIGN_LEFT)

    Returns:
        str: Complete QLabel stylesheet
    """
    return f"""
        QLabel {{
            font-size: {font_size};
            font-weight: {font_weight};
            color: {color};
            text-align: {align};
            background: transparent;
            border: none;
        }}
    """

# Helper function to apply text elision
def apply_elision_mode():
    """
    Returns Qt.TextElideMode.ElideRight for truncating long text.
    Use with QLabel.setTextElideMode() or similar methods.
    """
    from PyQt5.QtCore import Qt
    return Qt.TextElideMode.ElideRight
