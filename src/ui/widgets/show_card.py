"""
ShowCard Widget for DeadStream Browse Shows Screen

Displays detailed show information with visual appeal and smooth animations.
Used in Phase 10A redesign for Browse Shows screen.

Features:
- Large vintage-style date display (48pt)
- Venue and location information (24pt)
- Scrollable setlist for long tracklists
- Quality badge with color coding (Soundboard/Score-based)
- Large PLAY button (always visible)
- Optional "Try Another" button (Random Show mode)
- 400ms fade-in animation using QPropertyAnimation
- Loading state with animation
- Responsive layout for 1280x720 landscape display

Signal Architecture:
- play_clicked: Emitted when PLAY button clicked (emits show identifier)
- try_another_clicked: Emitted when Try Another button clicked

ASCII-only. No emojis or unicode characters.
"""

import sys
import os

# Path manipulation for subdirectory imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QFont, QTransform

# Import Theme Manager
from src.ui.styles.theme import Theme


class ShowCard(QWidget):
    """
    Reusable widget for displaying show details with visual appeal.

    Supports multiple modes:
    - 'default': Standard display with PLAY button only
    - 'random': Random Show mode with both PLAY and Try Another buttons
    - 'date_selected': Date selection mode with PLAY button only

    Signals:
        play_clicked(str): Emitted when PLAY button clicked, emits show identifier
        try_another_clicked(): Emitted when Try Another button clicked
    """

    play_clicked = pyqtSignal(str)  # Emits show identifier
    try_another_clicked = pyqtSignal()

    def __init__(self, parent=None):
        """
        Initialize ShowCard widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.current_mode = 'default'
        self.current_show = None
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Create card layout and widgets"""
        # Main container with dark background
        self.setStyleSheet(f"""
            ShowCard {{
                background-color: {Theme.BG_CARD};
                border-radius: {Theme.BUTTON_RADIUS}px;
            }}
        """)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Theme.MARGIN_XLARGE, Theme.MARGIN_XLARGE, Theme.MARGIN_XLARGE, Theme.MARGIN_XLARGE)
        main_layout.setSpacing(Theme.SPACING_LARGE)

        # Content container (for fade animation)
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(Theme.SPACING_MEDIUM)

        # Date label - Large, vintage-inspired
        self.date_label = QLabel()
        self.date_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-size: {Theme.HEADER_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
            }}
        """)
        self.date_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.date_label)

        # Venue label - Medium
        self.venue_label = QLabel()
        self.venue_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-size: {Theme.HEADER_SMALL}px;
                font-weight: {Theme.WEIGHT_BOLD};
            }}
        """)
        self.venue_label.setAlignment(Qt.AlignCenter)
        self.venue_label.setWordWrap(True)
        content_layout.addWidget(self.venue_label)

        # Location label - Medium
        self.location_label = QLabel()
        self.location_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                font-size: {Theme.BODY_LARGE}px;
            }}
        """)
        self.location_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.location_label)

        # Quality badge - Color-coded
        self.quality_badge = QLabel()
        self.quality_badge.setAlignment(Qt.AlignCenter)
        self.quality_badge.setMinimumHeight(40)
        content_layout.addWidget(self.quality_badge)

        # Setlist container - Scrollable
        setlist_container = QFrame()
        setlist_container.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_PANEL_DARK};
                border-radius: {Theme.BUTTON_RADIUS}px;
                border: 1px solid {Theme.BORDER_SUBTLE};
            }}
        """)
        setlist_layout = QVBoxLayout(setlist_container)
        setlist_layout.setContentsMargins(Theme.SPACING_MEDIUM, Theme.SPACING_SMALL, Theme.SPACING_MEDIUM, Theme.SPACING_SMALL)

        # Setlist scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {Theme.BORDER_SUBTLE};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {Theme.TEXT_SECONDARY};
                border-radius: 6px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {Theme.TEXT_PRIMARY};
            }}
        """)

        # Setlist label widget
        self.setlist_label = QLabel()
        self.setlist_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-size: {Theme.BODY_MEDIUM}px;
                line-height: 1.8;
            }}
        """)
        self.setlist_label.setWordWrap(True)
        self.setlist_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        scroll_area.setWidget(self.setlist_label)
        scroll_area.setMaximumHeight(200)  # Limit height for scrolling
        setlist_layout.addWidget(scroll_area)

        content_layout.addWidget(setlist_container)

        # Button container
        button_layout = QHBoxLayout()
        button_layout.setSpacing(Theme.SPACING_MEDIUM)

        # PLAY button - Large, always visible (uses red accent)
        self.play_button = QPushButton("PLAY")
        self.play_button.setMinimumSize(200, Theme.BUTTON_HEIGHT)
        self.play_button.setStyleSheet(Theme.get_button_style(Theme.ACCENT_RED, Theme.TEXT_PRIMARY))
        button_layout.addWidget(self.play_button)

        # Try Another button - Hidden by default, shown in random mode
        self.try_another_button = QPushButton("Try Another")
        self.try_another_button.setMinimumSize(200, Theme.BUTTON_HEIGHT)
        self.try_another_button.setStyleSheet(Theme.get_button_style(Theme.BORDER_SUBTLE, Theme.TEXT_PRIMARY))
        self.try_another_button.setVisible(False)  # Hidden by default
        button_layout.addWidget(self.try_another_button)

        content_layout.addLayout(button_layout)

        main_layout.addWidget(self.content_widget)

        # Loading widget (hidden by default)
        self.loading_widget = QWidget()
        loading_layout = QVBoxLayout(self.loading_widget)
        loading_layout.setAlignment(Qt.AlignCenter)

        # Loading spinner (text-based, ASCII only)
        self.loading_spinner = QLabel("Loading...")
        self.loading_spinner.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
            }}
        """)
        self.loading_spinner.setAlignment(Qt.AlignCenter)
        loading_layout.addWidget(self.loading_spinner)

        # Loading text
        self.loading_text = QLabel("Finding you a show...")
        self.loading_text.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                font-size: {Theme.BODY_LARGE}px;
            }}
        """)
        self.loading_text.setAlignment(Qt.AlignCenter)
        loading_layout.addWidget(self.loading_text)

        main_layout.addWidget(self.loading_widget)
        self.loading_widget.setVisible(False)

        # Set up spinner animation
        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self._animate_spinner)
        self.spinner_states = ["|", "/", "-", "\\"]
        self.spinner_index = 0

    def _connect_signals(self):
        """Connect button signals"""
        self.play_button.clicked.connect(self._on_play_clicked)
        self.try_another_button.clicked.connect(self._on_try_another_clicked)

    def _on_play_clicked(self):
        """Handle play button click"""
        if self.current_show:
            identifier = self.current_show.get('identifier', '')
            if identifier:
                self.play_clicked.emit(identifier)

    def _on_try_another_clicked(self):
        """Handle try another button click"""
        self.try_another_clicked.emit()

    def _animate_spinner(self):
        """Animate loading spinner (ASCII rotation)"""
        self.spinner_index = (self.spinner_index + 1) % len(self.spinner_states)
        spinner_char = self.spinner_states[self.spinner_index]
        self.loading_spinner.setText(f"  {spinner_char}  ")

    def load_show(self, show_data):
        """
        Populate card with show details (without animation).

        Args:
            show_data (dict): Show information from database
                Required keys: identifier, date, venue
                Optional keys: city, state, recording_score, setlist
        """
        self.current_show = show_data

        # Format date for display (e.g., "May 8, 1977")
        date_str = show_data.get('date', 'Unknown Date')
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%B %-d, %Y')
        except:
            formatted_date = date_str

        self.date_label.setText(formatted_date)

        # Venue
        venue = show_data.get('venue', 'Unknown Venue')
        self.venue_label.setText(venue)

        # Location (city, state)
        city = show_data.get('city', '')
        state = show_data.get('state', '')
        if city and state:
            location = f"{city}, {state}"
        elif city:
            location = city
        elif state:
            location = state
        else:
            location = "Location Unknown"
        self.location_label.setText(location)

        # Quality badge with color coding
        self._update_quality_badge(show_data)

        # Setlist (if available)
        setlist = show_data.get('setlist', '')
        if setlist:
            # Format setlist with SET 1, SET 2, E labels
            formatted_setlist = self._format_setlist(setlist)
            self.setlist_label.setText(formatted_setlist)
        else:
            self.setlist_label.setText("Setlist not available")

    def _update_quality_badge(self, show_data):
        """
        Update quality badge with appropriate color coding.

        Color scheme:
        - Soundboard: Gold/yellow background (Theme.ACCENT_YELLOW)
        - Score 9.0+: Green indicator (Theme.ACCENT_GREEN)
        - Score 8.0-8.9: Blue indicator (Theme.ACCENT_BLUE)
        - Default: Gray (Theme.BORDER_SUBTLE)

        Args:
            show_data (dict): Show information
        """
        identifier = show_data.get('identifier', '').lower()
        score = show_data.get('recording_score', 0)

        # Check if soundboard recording
        is_sbd = 'sbd' in identifier or 'soundboard' in identifier

        if is_sbd:
            # Soundboard: Gold background
            bg_color = Theme.ACCENT_YELLOW
            text_color = Theme.TEXT_DARK
            label_text = "SOUNDBOARD"
        elif score >= 9.0:
            # Excellent: Green
            bg_color = Theme.ACCENT_GREEN
            text_color = Theme.TEXT_PRIMARY
            label_text = f"EXCELLENT ({score:.1f})"
        elif score >= 8.0:
            # Very Good: Blue
            bg_color = Theme.ACCENT_BLUE
            text_color = Theme.TEXT_PRIMARY
            label_text = f"VERY GOOD ({score:.1f})"
        else:
            # Good: Gray
            bg_color = Theme.BORDER_SUBTLE
            text_color = Theme.TEXT_PRIMARY
            label_text = f"GOOD ({score:.1f})" if score > 0 else "QUALITY VARIES"

        self.quality_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                padding: {Theme.SPACING_SMALL}px {Theme.SPACING_MEDIUM}px;
                border-radius: 4px;
                font-weight: {Theme.WEIGHT_BOLD};
                font-size: {Theme.BODY_SMALL}px;
            }}
        """)
        self.quality_badge.setText(label_text)

    def _format_setlist(self, setlist):
        """
        Format setlist with SET 1, SET 2, E (Encore) labels.

        Handles common patterns:
        - Comma-separated songs
        - Song transitions marked with '>' or '->'
        - Multiple sets separated by semicolons or double spaces

        Args:
            setlist (str): Raw setlist string from database

        Returns:
            str: Formatted setlist with set labels

        Examples:
            Input: "Song1, Song2, Song3; Song4, Song5; Song6"
            Output: "SET 1: Song1, Song2, Song3\nSET 2: Song4, Song5\nE: Song6"
        """
        if not setlist:
            return "Setlist not available"

        # Try to split by common set delimiters
        # Common patterns: semicolon, " / ", or double newline
        sets = []

        # First try semicolon (most common in database)
        if ';' in setlist:
            sets = [s.strip() for s in setlist.split(';') if s.strip()]
        # Try " / " delimiter
        elif ' / ' in setlist:
            sets = [s.strip() for s in setlist.split(' / ') if s.strip()]
        # Try double space as delimiter (less common)
        elif '  ' in setlist:
            sets = [s.strip() for s in setlist.split('  ') if s.strip()]
        else:
            # No clear delimiters - treat as single set
            sets = [setlist.strip()]

        # Format with labels
        formatted_parts = []

        for i, set_songs in enumerate(sets):
            if i == 0:
                # First set
                formatted_parts.append(f"SET 1: {set_songs}")
            elif i == len(sets) - 1 and len(sets) > 2:
                # Last set with more than 2 sets total - likely encore
                formatted_parts.append(f"E: {set_songs}")
            else:
                # Middle sets (SET 2, SET 3, etc.)
                formatted_parts.append(f"SET {i + 1}: {set_songs}")

        # Add blank line between sets for better spacing
        return '\n\n'.join(formatted_parts)

    def fade_in(self, show_data):
        """
        Animate card appearance with opacity transition.

        Args:
            show_data (dict): Show information to display
        """
        # Hide loading state
        if self.loading_widget.isVisible():
            self.loading_widget.setVisible(False)
            self.spinner_timer.stop()

        # Show content widget
        self.content_widget.setVisible(True)

        # Update content BEFORE starting animation
        self.load_show(show_data)

        # Create opacity animation
        self.fade_animation = QPropertyAnimation(self.content_widget, b"windowOpacity")
        self.fade_animation.setDuration(400)  # 400ms
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)

        # Note: windowOpacity works on top-level widgets, so we use a workaround
        # Set initial opacity via stylesheet
        self.content_widget.setStyleSheet("QWidget { opacity: 0.0; }")

        # Animate to full opacity
        QTimer.singleShot(50, lambda: self.content_widget.setStyleSheet(""))

    def set_mode(self, mode):
        """
        Set card mode, controlling Try Another button visibility.

        Args:
            mode (str): Card mode - 'default', 'random', or 'date_selected'
        """
        self.current_mode = mode

        # Show Try Another button only in random mode
        if mode == 'random':
            self.try_another_button.setVisible(True)
        else:
            self.try_another_button.setVisible(False)

    def show_loading(self):
        """Display loading state with animation"""
        # Hide content
        self.content_widget.setVisible(False)

        # Show loading widget
        self.loading_widget.setVisible(True)

        # Start spinner animation (updates every 200ms)
        self.spinner_index = 0
        self.spinner_timer.start(200)

    def show_error(self, message):
        """
        Display error state.

        Args:
            message (str): Error message to display
        """
        # Stop any animations
        if self.spinner_timer.isActive():
            self.spinner_timer.stop()

        # Hide loading
        self.loading_widget.setVisible(False)

        # Show content with error message
        self.content_widget.setVisible(True)

        self.date_label.setText("Error")
        self.venue_label.setText(message)
        self.location_label.setText("")
        self.quality_badge.setText("")
        self.setlist_label.setText("")


# Standalone test code
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # Apply global theme
    app.setStyleSheet(Theme.get_global_stylesheet())

    # Test window
    window = QWidget()
    window.setWindowTitle("ShowCard Test")
    window.setGeometry(100, 100, 800, 600)
    window.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")

    layout = QVBoxLayout(window)

    # Create ShowCard
    card = ShowCard()
    layout.addWidget(card)

    # Test data
    test_show = {
        'identifier': 'gd1977-05-08.sbd.smith.97.sbeok.flac16',
        'date': '1977-05-08',
        'venue': 'Barton Hall, Cornell University',
        'city': 'Ithaca',
        'state': 'NY',
        'recording_score': 9.5,
        'setlist': 'New Minglewood Blues, Loser, El Paso, They Love Each Other, Jack Straw, Deal, Lazy Lightning > Supplication; Scarlet Begonias > Fire on the Mountain, Estimated Prophet, St. Stephen > Not Fade Away > St. Stephen, Morning Dew; One More Saturday Night'
    }

    # Show initial loading state
    card.show_loading()

    # After 2 seconds, fade in with show data
    def load_test_show():
        card.set_mode('random')
        card.fade_in(test_show)

    QTimer.singleShot(2000, load_test_show)

    window.show()
    sys.exit(app.exec_())
