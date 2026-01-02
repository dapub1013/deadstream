"""
Centralized button stylesheets for DeadStream UI.

Based on Tailwind color values from deadhead-player-landscape-fixed.jsx.
All colors use exact hex values to ensure consistent visual design.

ASCII-only. No emojis or unicode characters.
"""

# Background Colors
BG_BLACK = "#000000"
BG_GRAY_900 = "#111827"
BG_GRAY_800 = "#1F2937"
BG_GRAY_700 = "#374151"
BG_GRAY_600 = "#4B5563"

# Text Colors
TEXT_WHITE = "#FFFFFF"
TEXT_GRAY_400 = "#9CA3AF"
TEXT_GRAY_500 = "#6B7280"
TEXT_GRAY_600 = "#4B5563"

# Accent Colors - Blue (primary)
BLUE_600 = "#3B82F6"
BLUE_700 = "#2563EB"
BLUE_800 = "#1D4ED8"

# Accent Colors - Other
GREEN_400 = "#4ADE80"
GREEN_500 = "#22C55E"
ORANGE_400 = "#FB923C"
ORANGE_600 = "#EA580C"
PURPLE_500 = "#A855F7"
PURPLE_600 = "#9333EA"
RED_500 = "#EF4444"
YELLOW_500 = "#EAB308"

# Border Radius
BORDER_RADIUS = "8px"

# Button Padding
BUTTON_PADDING_V = "12px"
BUTTON_PADDING_H = "16px"

# Primary button style (blue accent)
PRIMARY_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {BLUE_600};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: {BUTTON_PADDING_V} {BUTTON_PADDING_H};
        font-weight: 600;
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {BLUE_700};
    }}
    QPushButton:pressed {{
        background-color: {BLUE_800};
    }}
    QPushButton:disabled {{
        background-color: {BG_GRAY_600};
        color: {TEXT_GRAY_500};
    }}
"""

# Secondary button style (gray)
SECONDARY_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {BG_GRAY_800};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: {BUTTON_PADDING_V} {BUTTON_PADDING_H};
        font-weight: 600;
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_700};
    }}
    QPushButton:pressed {{
        background-color: {BG_GRAY_600};
    }}
    QPushButton:disabled {{
        background-color: {BG_GRAY_900};
        color: {TEXT_GRAY_600};
    }}
"""

# Dark button style (darker gray for browse mode buttons)
DARK_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {BG_GRAY_900};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: {BUTTON_PADDING_V} {BUTTON_PADDING_H};
        font-weight: 600;
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_800};
    }}
    QPushButton:pressed {{
        background-color: {BG_GRAY_700};
    }}
    QPushButton:disabled {{
        background-color: {BG_GRAY_900};
        color: {TEXT_GRAY_600};
        opacity: 0.5;
    }}
"""

# Browse mode button (selected state)
BROWSE_MODE_BUTTON_SELECTED = f"""
    QPushButton {{
        background-color: {BG_GRAY_700};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: 16px;
        font-weight: 600;
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_600};
    }}
"""

# Browse mode button (unselected state)
BROWSE_MODE_BUTTON_UNSELECTED = f"""
    QPushButton {{
        background-color: {BG_GRAY_900};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: 16px;
        font-weight: 600;
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_800};
    }}
    QPushButton:pressed {{
        background-color: {BG_GRAY_700};
    }}
"""

# Settings category button (selected state)
SETTINGS_CATEGORY_SELECTED = f"""
    QPushButton {{
        background-color: {BLUE_600};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: 16px;
        font-weight: 600;
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {BLUE_700};
    }}
"""

# Settings category button (unselected state)
SETTINGS_CATEGORY_UNSELECTED = f"""
    QPushButton {{
        background-color: {BG_GRAY_900};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: 16px;
        font-weight: 600;
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_800};
    }}
    QPushButton:pressed {{
        background-color: {BG_GRAY_700};
    }}
"""

# Playback control button (prev/next)
PLAYBACK_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {TEXT_WHITE};
        border: none;
        border-radius: 50%;
        padding: 16px;
        min-width: 60px;
        min-height: 60px;
        max-width: 60px;
        max-height: 60px;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_800};
    }}
    QPushButton:pressed {{
        background-color: {BG_GRAY_700};
    }}
    QPushButton:disabled {{
        color: {BG_GRAY_600};
    }}
"""

# Play/pause button (large white circle)
PLAY_PAUSE_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {TEXT_WHITE};
        color: {BG_BLACK};
        border: none;
        border-radius: 50%;
        padding: 24px;
        min-width: 96px;
        min-height: 96px;
        max-width: 96px;
        max-height: 96px;
    }}
    QPushButton:hover {{
        background-color: {TEXT_GRAY_400};
    }}
    QPushButton:pressed {{
        background-color: {TEXT_GRAY_500};
    }}
"""

# Small control button (30s skip, etc.)
SMALL_CONTROL_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {BG_GRAY_800};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: 8px 16px;
        font-weight: 600;
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_700};
    }}
    QPushButton:pressed {{
        background-color: {BG_GRAY_600};
    }}
"""

# Icon button (heart, settings, etc.)
ICON_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {TEXT_GRAY_400};
        border: none;
        border-radius: 50%;
        padding: 8px;
        min-width: 40px;
        min-height: 40px;
        max-width: 40px;
        max-height: 40px;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_800};
    }}
    QPushButton:pressed {{
        background-color: {BG_GRAY_700};
    }}
"""

# Special button - Orange accent (for "On This Day")
ORANGE_ACCENT_BUTTON = f"""
    QPushButton {{
        background-color: {ORANGE_600};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: {BUTTON_PADDING_V} {BUTTON_PADDING_H};
        font-weight: 600;
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {ORANGE_400};
    }}
"""

# Special button - Green accent
GREEN_ACCENT_BUTTON = f"""
    QPushButton {{
        background-color: {GREEN_500};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: {BUTTON_PADDING_V} {BUTTON_PADDING_H};
        font-weight: 600;
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {GREEN_400};
    }}
"""

# Special button - Purple accent
PURPLE_ACCENT_BUTTON = f"""
    QPushButton {{
        background-color: {PURPLE_600};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: {BUTTON_PADDING_V} {BUTTON_PADDING_H};
        font-weight: 600;
        font-size: 18px;
    }}
    QPushButton:hover {{
        background-color: {PURPLE_500};
    }}
"""

# List item button (for show list, setlist, etc.)
LIST_ITEM_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {TEXT_GRAY_400};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: 12px;
        text-align: left;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_900};
        color: {TEXT_WHITE};
    }}
    QPushButton:pressed {{
        background-color: {BG_GRAY_800};
        color: {TEXT_WHITE};
    }}
"""

# List item button (selected state)
LIST_ITEM_BUTTON_SELECTED = f"""
    QPushButton {{
        background-color: {BG_GRAY_800};
        color: {TEXT_WHITE};
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: 12px;
        text-align: left;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {BG_GRAY_700};
    }}
"""
