#!/usr/bin/env python3
"""
Random Show Widget for DeadStream

Displays detailed information about a randomly selected show including:
- Show metadata (date, venue, location, rating)
- Setlist with tracks
- "Try Again" button to load a different random show
- "Play Show" button to start playback
"""

# Path manipulation for imports (file in src/ui/widgets/)
import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from src.ui.styles.button_styles import (
    PRIMARY_BUTTON_STYLE, SECONDARY_BUTTON_STYLE,
    BG_GRAY_800, BG_GRAY_900, BG_GRAY_700, TEXT_WHITE, TEXT_GRAY_400
)
from src.ui.styles.text_styles import TITLE_SECTION_STYLE, TEXT_SUPPORTING_STYLE
from src.database.queries import get_random_show
from src.api.metadata import get_metadata, extract_audio_files


class RandomShowWidget(QWidget):
    """
    Widget that displays a random show with full details and setlist.

    Signals:
        show_selected: Emitted when user clicks "Play Show" (emits show dict)
        reload_requested: Emitted when user clicks "Try Again"
    """

    # Signals
    show_selected = pyqtSignal(dict)
    reload_requested = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize random show widget"""
        super().__init__(parent)

        self.current_show = None
        self.tracks = []

        self.init_ui()

    def init_ui(self):
        """Set up the widget layout"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scrollable container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {BG_GRAY_800};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {BG_GRAY_800};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {BG_GRAY_700};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #6B7280;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """)

        # Content container
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_container.setLayout(self.content_layout)

        scroll_area.setWidget(self.content_container)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

        # Show loading state initially
        self.show_loading()

    def show_loading(self):
        """Display loading state"""
        self.clear_content()

        loading_label = QLabel("Loading random show...")
        loading_label.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_GRAY_400};
                font-size: 18px;
                padding: 40px;
            }}
        """)
        loading_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(loading_label)
        self.content_layout.addStretch()

    def show_error(self, message):
        """Display error state"""
        self.clear_content()

        error_label = QLabel(f"Error: {message}")
        error_label.setStyleSheet(f"""
            QLabel {{
                color: #EF4444;
                font-size: 16px;
                padding: 40px;
            }}
        """)
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setWordWrap(True)
        self.content_layout.addWidget(error_label)

        # Add retry button
        retry_btn = QPushButton("Try Again")
        retry_btn.setStyleSheet(PRIMARY_BUTTON_STYLE)
        retry_btn.setMinimumHeight(50)
        retry_btn.clicked.connect(self.reload_requested.emit)
        self.content_layout.addWidget(retry_btn)

        self.content_layout.addStretch()

    def clear_content(self):
        """Clear all content widgets"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_random_show(self):
        """Load and display a random show"""
        try:
            self.show_loading()

            # Get random show from database
            show = get_random_show()

            if not show:
                self.show_error("No shows found in database")
                return

            self.current_show = show

            # Fetch metadata from Archive.org to get setlist
            try:
                metadata = get_metadata(show['identifier'])
                audio_files = extract_audio_files(metadata)

                # Parse tracks from audio files
                self.tracks = self.parse_tracks(audio_files)

            except Exception as e:
                print(f"[WARN] Failed to fetch metadata for {show['identifier']}: {e}")
                self.tracks = []

            # Display the show
            self.display_show()

        except Exception as e:
            print(f"[ERROR] Failed to load random show: {e}")
            import traceback
            traceback.print_exc()
            self.show_error(f"Failed to load random show: {str(e)}")

    def parse_tracks(self, audio_files):
        """
        Parse audio files into track list with set detection.

        Args:
            audio_files: List of audio file dicts from metadata

        Returns:
            List of track dicts with title, duration, set_name
        """
        tracks = []
        current_set = "SET I"
        set_2_started = False
        encore_started = False

        for idx, file_info in enumerate(audio_files):
            filename = file_info.get('name', '')

            # Extract track name from filename (remove extension and track number)
            track_name = filename.rsplit('.', 1)[0]  # Remove extension

            # Remove common prefixes (gd77-05-08d1t01 -> track name)
            parts = track_name.split('_')
            if len(parts) > 1:
                track_name = '_'.join(parts[1:])
            else:
                # Try to extract after 't' (track number)
                import re
                match = re.search(r't\d+(.+)', track_name)
                if match:
                    track_name = match.group(1)

            # Clean up track name
            track_name = track_name.replace('_', ' ').strip()
            if not track_name:
                track_name = f"Track {idx + 1}"

            # Detect set changes based on track name keywords
            track_lower = track_name.lower()
            if any(keyword in track_lower for keyword in ['drums', 'drum solo']) and not set_2_started:
                current_set = "SET II"
                set_2_started = True
            elif any(keyword in track_lower for keyword in ['encore', 'e:', 'e-']) and not encore_started:
                current_set = "ENCORE"
                encore_started = True

            # Get duration (convert to MM:SS format)
            duration_str = "0:00"
            if 'length' in file_info:
                try:
                    seconds = float(file_info['length'])
                    minutes = int(seconds // 60)
                    secs = int(seconds % 60)
                    duration_str = f"{minutes}:{secs:02d}"
                except (ValueError, TypeError):
                    pass

            tracks.append({
                'title': track_name,
                'duration': duration_str,
                'set_name': current_set,
                'filename': filename
            })

        return tracks

    def display_show(self):
        """Display the loaded show with all details"""
        self.clear_content()

        if not self.current_show:
            self.show_error("No show loaded")
            return

        show = self.current_show

        # Show header section
        header = self.create_show_header(show)
        self.content_layout.addWidget(header)

        # Action buttons (Play Show and Try Again)
        buttons_layout = self.create_action_buttons()
        self.content_layout.addLayout(buttons_layout)

        # Setlist section
        if self.tracks:
            setlist_section = self.create_setlist_section()
            self.content_layout.addWidget(setlist_section)
        else:
            no_setlist_label = QLabel("Setlist information not available")
            no_setlist_label.setStyleSheet(f"""
                QLabel {{
                    color: {TEXT_GRAY_400};
                    font-size: 14px;
                    padding: 20px;
                }}
            """)
            no_setlist_label.setAlignment(Qt.AlignCenter)
            self.content_layout.addWidget(no_setlist_label)

        self.content_layout.addStretch()

    def create_show_header(self, show):
        """Create the show header with metadata"""
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_GRAY_900};
                border: 2px solid {BG_GRAY_700};
                border-radius: 8px;
                padding: 20px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Title (Date + Venue)
        title = QLabel(f"{show['date']} - {show['venue']}")
        title.setStyleSheet(f"""
            QLabel {{
                {TITLE_SECTION_STYLE}
            }}
        """)
        title.setWordWrap(True)
        layout.addWidget(title)

        # Location
        location = QLabel(f"{show['city']}, {show['state']}")
        location.setStyleSheet(f"""
            QLabel {{
                {TEXT_SUPPORTING_STYLE}
                font-size: 16px;
            }}
        """)
        layout.addWidget(location)

        # Metadata badges row
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(8)

        # Rating badge (if available)
        if show.get('avg_rating') and show['avg_rating'] > 0:
            rating_badge = QLabel(f"[Star] {show['avg_rating']:.1f}/5.0")
            rating_badge.setStyleSheet("""
                QLabel {
                    background-color: #374151;
                    color: #FCD34D;
                    padding: 6px 14px;
                    border-radius: 12px;
                    font-size: 13px;
                    font-weight: bold;
                }
            """)
            badges_layout.addWidget(rating_badge)

        # Review count badge (if available)
        if show.get('num_reviews') and show['num_reviews'] > 0:
            reviews_badge = QLabel(f"{show['num_reviews']} reviews")
            reviews_badge.setStyleSheet("""
                QLabel {
                    background-color: #374151;
                    color: #9CA3AF;
                    padding: 6px 14px;
                    border-radius: 12px;
                    font-size: 13px;
                }
            """)
            badges_layout.addWidget(reviews_badge)

        # Track count badge (if tracks loaded)
        if self.tracks:
            tracks_badge = QLabel(f"{len(self.tracks)} tracks")
            tracks_badge.setStyleSheet("""
                QLabel {
                    background-color: #374151;
                    color: #9CA3AF;
                    padding: 6px 14px;
                    border-radius: 12px;
                    font-size: 13px;
                }
            """)
            badges_layout.addWidget(tracks_badge)

        badges_layout.addStretch()
        layout.addLayout(badges_layout)

        header.setLayout(layout)
        return header

    def create_action_buttons(self):
        """Create Play Show and Try Again buttons"""
        layout = QHBoxLayout()
        layout.setSpacing(12)

        # Play Show button (primary action)
        play_btn = QPushButton("Play Show")
        play_btn.setStyleSheet(PRIMARY_BUTTON_STYLE)
        play_btn.setMinimumHeight(60)
        play_btn.clicked.connect(self.on_play_clicked)
        layout.addWidget(play_btn, 2)

        # Try Again button (secondary action)
        retry_btn = QPushButton("Try Again")
        retry_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        retry_btn.setMinimumHeight(60)
        retry_btn.clicked.connect(self.on_retry_clicked)
        layout.addWidget(retry_btn, 1)

        return layout

    def create_setlist_section(self):
        """Create the setlist display section"""
        section = QFrame()
        section.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_GRAY_900};
                border: 2px solid {BG_GRAY_700};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Setlist header
        header_label = QLabel("Setlist")
        header_label.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_WHITE};
                font-size: 18px;
                font-weight: bold;
                padding: 16px 20px;
                border-bottom: 2px solid {BG_GRAY_700};
            }}
        """)
        layout.addWidget(header_label)

        # Track list
        current_set = None
        for idx, track in enumerate(self.tracks):
            # Insert set header if set changed
            if track.get('set_name') != current_set:
                current_set = track.get('set_name', '')
                if current_set:
                    set_header = QLabel(current_set)
                    set_header.setStyleSheet(f"""
                        QLabel {{
                            background-color: {BG_GRAY_800};
                            color: #6B7280;
                            padding: 10px 20px;
                            font-size: 12px;
                            font-weight: bold;
                            letter-spacing: 1px;
                        }}
                    """)
                    layout.addWidget(set_header)

            # Track item
            track_item = self.create_track_item(idx, track)
            layout.addWidget(track_item)

        section.setLayout(layout)
        return section

    def create_track_item(self, index, track):
        """Create a track list item"""
        item = QFrame()
        item.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_GRAY_900};
                border-bottom: 1px solid {BG_GRAY_700};
                padding: 10px 20px;
            }}
        """)

        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # Track number
        track_num = QLabel(f"{index + 1:02d}")
        track_num.setFixedWidth(30)
        track_num.setStyleSheet(f"""
            color: {TEXT_GRAY_400};
            font-size: 13px;
        """)
        layout.addWidget(track_num)

        # Song name
        song_name = QLabel(track.get('title', 'Unknown Track'))
        song_name.setStyleSheet(f"""
            color: {TEXT_WHITE};
            font-size: 14px;
        """)
        layout.addWidget(song_name, 1)

        # Duration
        duration = QLabel(track.get('duration', '0:00'))
        duration.setStyleSheet(f"""
            color: {TEXT_GRAY_400};
            font-size: 13px;
        """)
        duration.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(duration)

        item.setLayout(layout)
        return item

    def on_play_clicked(self):
        """Handle Play Show button click"""
        if self.current_show:
            print(f"[INFO] Play show clicked: {self.current_show['date']} - {self.current_show['venue']}")
            self.show_selected.emit(self.current_show)

    def on_retry_clicked(self):
        """Handle Try Again button click"""
        print("[INFO] Try Again clicked - loading new random show")
        self.reload_requested.emit()
        self.load_random_show()


if __name__ == "__main__":
    """Test the random show widget"""
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Apply dark theme
    app.setStyleSheet(f"""
        QWidget {{
            background-color: {BG_GRAY_800};
            color: {TEXT_WHITE};
        }}
    """)

    widget = RandomShowWidget()
    widget.setGeometry(100, 100, 800, 900)
    widget.setWindowTitle("Random Show Widget Test")

    # Load a random show
    widget.load_random_show()

    # Handle signals
    widget.show_selected.connect(lambda show: print(f"[TEST] Show selected: {show['date']}"))
    widget.reload_requested.connect(lambda: print("[TEST] Reload requested"))

    widget.show()
    sys.exit(app.exec_())
