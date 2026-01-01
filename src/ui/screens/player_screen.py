#!/usr/bin/env python3
"""
Player screen for DeadStream - Now Playing Interface
Phase 9 Task 9.1: Player screen layout

Split-screen layout:
- Left panel: Concert info + scrollable setlist
- Right panel: Now playing info + playback controls
"""

import sys
import os

# Path manipulation for imports (file will be in src/ui/screens/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QSlider, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor


class PlayerScreen(QWidget):
    """
    Now Playing screen with split-screen layout.
    
    Left panel: Concert info + setlist
    Right panel: Now playing + controls
    """
    
    # Signals
    browse_requested = pyqtSignal()  # User wants to browse shows
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()
        
        # Current show data (will be populated when show is loaded)
        self.current_show = None
        self.current_track_index = 0
        self.tracks = []
        self.is_playing = False
        
        # Track list item widgets (for highlighting)
        self.track_widgets = []
        
        self.init_ui()
    
    def init_ui(self):
        """Set up the player screen UI"""
        # Main horizontal layout (split screen)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left panel: Concert info + setlist (50%)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)  # stretch factor 1
        
        # Right panel: Now playing + controls (50%)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)  # stretch factor 1
        
        self.setLayout(main_layout)
        
        # Apply dark theme styling
        self.apply_styling()
    
    def create_left_panel(self):
        """Create left panel with concert info and setlist"""
        panel = QFrame()
        panel.setObjectName("leftPanel")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Concert header (fixed at top)
        header = self.create_concert_header()
        layout.addWidget(header)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #374151;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        
        # Setlist (scrollable)
        setlist_scroll = self.create_setlist_scroll()
        layout.addWidget(setlist_scroll)
        
        panel.setLayout(layout)
        return panel
    
    def create_concert_header(self):
        """Create concert header with title, location, and metadata"""
        header = QFrame()
        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        
        # Concert title (2xl font, semibold)
        self.concert_title_label = QLabel("Select a show to play")
        self.concert_title_label.setFont(QFont("Arial", 22, QFont.DemiBold))
        self.concert_title_label.setWordWrap(True)
        header_layout.addWidget(self.concert_title_label)
        
        # Location (lg font, gray-400)
        self.location_label = QLabel("Browse shows to get started")
        self.location_label.setFont(QFont("Arial", 14))
        self.location_label.setStyleSheet("color: #9CA3AF;")
        header_layout.addWidget(self.location_label)
        
        # Metadata row (source, rating, track count)
        metadata_layout = QHBoxLayout()
        metadata_layout.setSpacing(10)
        
        # Source badge
        self.source_badge = QLabel("Soundboard")
        self.source_badge.setFont(QFont("Arial", 11))
        self.source_badge.setStyleSheet("""
            background-color: #2563EB;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
        """)
        self.source_badge.hide()
        metadata_layout.addWidget(self.source_badge)
        
        # Rating
        self.rating_label = QLabel("[STAR] 4.8/5.0")
        self.rating_label.setFont(QFont("Arial", 11))
        self.rating_label.setStyleSheet("color: #FCD34D;")
        self.rating_label.hide()
        metadata_layout.addWidget(self.rating_label)
        
        # Track count
        self.track_count_label = QLabel("20 tracks")
        self.track_count_label.setFont(QFont("Arial", 11))
        self.track_count_label.setStyleSheet("color: #9CA3AF;")
        self.track_count_label.hide()
        metadata_layout.addWidget(self.track_count_label)
        
        metadata_layout.addStretch()
        
        # Favorite button (heart icon)
        self.favorite_button = QPushButton("[HEART]")
        self.favorite_button.setFont(QFont("Arial", 14))
        self.favorite_button.setFixedSize(44, 44)
        self.favorite_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #6B7280;
                border-radius: 22px;
                color: #6B7280;
            }
            QPushButton:hover {
                border-color: #EF4444;
                color: #EF4444;
            }
            QPushButton:pressed {
                background-color: #1F2937;
            }
        """)
        self.favorite_button.hide()
        metadata_layout.addWidget(self.favorite_button)
        
        header_layout.addLayout(metadata_layout)
        
        header.setLayout(header_layout)
        return header
    
    def create_setlist_scroll(self):
        """Create scrollable setlist area"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Setlist container
        self.setlist_container = QWidget()
        self.setlist_layout = QVBoxLayout()
        self.setlist_layout.setSpacing(2)
        self.setlist_layout.setContentsMargins(0, 0, 0, 0)
        
        # Placeholder text
        placeholder = QLabel("Setlist will appear here when a show is loaded")
        placeholder.setFont(QFont("Arial", 12))
        placeholder.setStyleSheet("color: #6B7280;")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setMinimumHeight(200)
        self.setlist_layout.addWidget(placeholder)
        
        self.setlist_layout.addStretch()
        self.setlist_container.setLayout(self.setlist_layout)
        scroll.setWidget(self.setlist_container)
        
        return scroll
    
    def create_right_panel(self):
        """Create right panel with now playing and controls"""
        panel = QFrame()
        panel.setObjectName("rightPanel")
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Add vertical stretch at top
        layout.addStretch(1)
        
        # Now playing display
        now_playing = self.create_now_playing_display()
        layout.addWidget(now_playing)
        
        layout.addSpacing(20)
        
        # Progress bar
        progress = self.create_progress_bar()
        layout.addWidget(progress)
        
        layout.addSpacing(10)
        
        # Main playback controls
        main_controls = self.create_main_controls()
        layout.addWidget(main_controls)
        
        layout.addSpacing(10)
        
        # 30-second skip controls
        skip_controls = self.create_skip_controls()
        layout.addWidget(skip_controls)
        
        layout.addSpacing(10)
        
        # Track counter
        self.track_counter = QLabel("Track 1 of 20")
        self.track_counter.setFont(QFont("Arial", 11))
        self.track_counter.setStyleSheet("color: #9CA3AF;")
        self.track_counter.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.track_counter)
        
        layout.addSpacing(20)
        
        # Volume control
        volume = self.create_volume_control()
        layout.addWidget(volume)
        
        # Add vertical stretch
        layout.addStretch(2)
        
        # Browse shows button at bottom
        browse_btn = QPushButton("Browse Shows")
        browse_btn.setFont(QFont("Arial", 14, QFont.DemiBold))
        browse_btn.setMinimumHeight(60)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:pressed {
                background-color: #111827;
            }
        """)
        browse_btn.clicked.connect(self.on_browse_clicked)
        layout.addWidget(browse_btn)
        
        panel.setLayout(layout)
        return panel
    
    def create_now_playing_display(self):
        """Create now playing song name and set indicator"""
        container = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # "NOW PLAYING" label
        label = QLabel("NOW PLAYING")
        label.setFont(QFont("Arial", 10, QFont.Bold))
        label.setStyleSheet("color: #6B7280; letter-spacing: 2px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Song name (3xl font, bold)
        self.song_name_label = QLabel("Dark Star")
        self.song_name_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.song_name_label.setAlignment(Qt.AlignCenter)
        self.song_name_label.setWordWrap(True)
        layout.addWidget(self.song_name_label)
        
        # Set indicator (xl font, gray-400)
        self.set_indicator_label = QLabel("SET I")
        self.set_indicator_label.setFont(QFont("Arial", 16))
        self.set_indicator_label.setStyleSheet("color: #9CA3AF;")
        self.set_indicator_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.set_indicator_label)
        
        container.setLayout(layout)
        return container
    
    def create_progress_bar(self):
        """Create progress bar with time stamps"""
        container = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Progress slider
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(1000)  # Will be updated with actual duration
        self.progress_slider.setValue(0)
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                height: 6px;
                background: #374151;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3B82F6, stop:1 #2563EB);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_slider)
        
        # Time stamps
        time_layout = QHBoxLayout()
        
        self.current_time_label = QLabel("0:00")
        self.current_time_label.setFont(QFont("Arial", 11))
        self.current_time_label.setStyleSheet("color: #9CA3AF;")
        time_layout.addWidget(self.current_time_label)
        
        time_layout.addStretch()
        
        self.total_time_label = QLabel("11:45")
        self.total_time_label.setFont(QFont("Arial", 11))
        self.total_time_label.setStyleSheet("color: #9CA3AF;")
        time_layout.addWidget(self.total_time_label)
        
        layout.addLayout(time_layout)
        
        container.setLayout(layout)
        return container
    
    def create_main_controls(self):
        """Create main playback controls (prev, play/pause, next)"""
        container = QFrame()
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Previous track button
        prev_btn = QPushButton("|<")
        prev_btn.setFont(QFont("Arial", 18))
        prev_btn.setFixedSize(60, 60)
        prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: #9CA3AF;
                border: none;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #374151;
                color: white;
            }
            QPushButton:pressed {
                background-color: #111827;
            }
            QPushButton:disabled {
                color: #4B5563;
            }
        """)
        layout.addWidget(prev_btn)
        
        # Play/Pause button (large)
        self.play_pause_btn = QPushButton(">")
        self.play_pause_btn.setFont(QFont("Arial", 28, QFont.Bold))
        self.play_pause_btn.setFixedSize(80, 80)
        self.play_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                border-radius: 40px;
            }
            QPushButton:hover {
                background-color: #F3F4F6;
            }
            QPushButton:pressed {
                background-color: #E5E7EB;
            }
        """)
        self.play_pause_btn.clicked.connect(self.on_play_pause_clicked)
        layout.addWidget(self.play_pause_btn)
        
        # Next track button
        next_btn = QPushButton(">|")
        next_btn.setFont(QFont("Arial", 18))
        next_btn.setFixedSize(60, 60)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: white;
                border: none;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:pressed {
                background-color: #111827;
            }
            QPushButton:disabled {
                color: #4B5563;
            }
        """)
        layout.addWidget(next_btn)
        
        container.setLayout(layout)
        return container
    
    def create_skip_controls(self):
        """Create 30-second skip controls"""
        container = QFrame()
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Rewind 30s
        rewind_btn = QPushButton("<<< 30s")
        rewind_btn.setFont(QFont("Arial", 12))
        rewind_btn.setMinimumHeight(44)
        rewind_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: #9CA3AF;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #374151;
                color: white;
            }
            QPushButton:pressed {
                background-color: #111827;
            }
        """)
        layout.addWidget(rewind_btn)
        
        # Skip 30s
        skip_btn = QPushButton("30s >>>")
        skip_btn.setFont(QFont("Arial", 12))
        skip_btn.setMinimumHeight(44)
        skip_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: #9CA3AF;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #374151;
                color: white;
            }
            QPushButton:pressed {
                background-color: #111827;
            }
        """)
        layout.addWidget(skip_btn)
        
        container.setLayout(layout)
        return container
    
    def create_volume_control(self):
        """Create volume control with mute button and slider"""
        container = QFrame()
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Mute button
        self.mute_btn = QPushButton("[VOL]")
        self.mute_btn.setFont(QFont("Arial", 14))
        self.mute_btn.setFixedSize(44, 44)
        self.mute_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:pressed {
                background-color: #111827;
            }
        """)
        layout.addWidget(self.mute_btn)
        
        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(75)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                height: 6px;
                background: #374151;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3B82F6, stop:1 #2563EB);
                border-radius: 3px;
            }
        """)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        layout.addWidget(self.volume_slider)
        
        # Volume percentage
        self.volume_label = QLabel("75%")
        self.volume_label.setFont(QFont("Arial", 11))
        self.volume_label.setStyleSheet("color: #9CA3AF;")
        self.volume_label.setMinimumWidth(40)
        layout.addWidget(self.volume_label)
        
        container.setLayout(layout)
        return container
    
    def apply_styling(self):
        """Apply dark theme styling to the player screen"""
        self.setStyleSheet("""
            PlayerScreen {
                background-color: #000000;
            }
            QFrame#leftPanel {
                background-color: #111827;
                border-right: 1px solid #374151;
            }
            QFrame#rightPanel {
                background-color: #000000;
            }
            QLabel {
                color: white;
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
    
    def load_show(self, show_data, tracks_data):
        """
        Load a show into the player screen.
        
        Args:
            show_data: Dictionary with show metadata (date, venue, etc.)
            tracks_data: List of track dictionaries (name, duration, set)
        """
        self.current_show = show_data
        self.tracks = tracks_data
        self.current_track_index = 0
        
        # Update concert header
        date = show_data.get('date', 'Unknown Date')
        venue = show_data.get('venue', 'Unknown Venue')
        city = show_data.get('city', '')
        state = show_data.get('state', '')
        
        # Format: YYYY/MM/DD [Venue Name]
        title = f"{date.replace('-', '/')} {venue}"
        self.concert_title_label.setText(title)
        
        # Location: City, State
        location = f"{city}, {state}" if city and state else "Location Unknown"
        self.location_label.setText(location)
        
        # Show metadata badges
        source = show_data.get('source', 'Unknown')
        self.source_badge.setText(source)
        self.source_badge.show()
        
        rating = show_data.get('rating', 0)
        if rating > 0:
            self.rating_label.setText(f"[STAR] {rating:.1f}/5.0")
            self.rating_label.show()
        
        track_count = len(tracks_data)
        self.track_count_label.setText(f"{track_count} tracks")
        self.track_count_label.show()
        
        self.favorite_button.show()
        
        # Build setlist
        self.build_setlist(tracks_data)
        
        # Update now playing
        if tracks_data:
            self.update_now_playing(0)
    
    def build_setlist(self, tracks):
        """Build the setlist display with set headers"""
        # Clear existing setlist
        while self.setlist_layout.count():
            item = self.setlist_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.track_widgets = []
        current_set = None
        
        for i, track in enumerate(tracks):
            # Add set header if set changed
            track_set = track.get('set', 'SET I')
            if track_set != current_set:
                set_header = QLabel(track_set)
                set_header.setFont(QFont("Arial", 10, QFont.Bold))
                set_header.setStyleSheet("""
                    color: #6B7280;
                    letter-spacing: 2px;
                    padding: 10px 0 5px 0;
                """)
                self.setlist_layout.addWidget(set_header)
                current_set = track_set
            
            # Create track item
            track_item = self.create_track_item(i, track)
            self.setlist_layout.addWidget(track_item)
            self.track_widgets.append(track_item)
        
        self.setlist_layout.addStretch()
    
    def create_track_item(self, index, track):
        """Create a single track item for the setlist"""
        item = QFrame()
        item.setObjectName(f"trackItem_{index}")
        item.setMinimumHeight(44)  # Touch-friendly
        item.setCursor(Qt.PointingHandCursor)
        item.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border-radius: 4px;
                padding: 8px;
            }
            QFrame:hover {
                background-color: #1F2937;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(10)
        
        # Track number
        num_label = QLabel(f"{index + 1:02d}")
        num_label.setFont(QFont("Arial", 11))
        num_label.setStyleSheet("color: #6B7280;")
        num_label.setFixedWidth(30)
        layout.addWidget(num_label)
        
        # Song name
        name_label = QLabel(track.get('name', 'Unknown'))
        name_label.setFont(QFont("Arial", 12))
        layout.addWidget(name_label)
        
        layout.addStretch()
        
        # Duration
        duration = track.get('duration', '0:00')
        duration_label = QLabel(duration)
        duration_label.setFont(QFont("Arial", 11))
        duration_label.setStyleSheet("color: #6B7280;")
        duration_label.setAlignment(Qt.AlignRight)
        layout.addWidget(duration_label)
        
        item.setLayout(layout)
        
        # Store index for click handling
        item.track_index = index
        
        # Make clickable
        item.mousePressEvent = lambda event, idx=index: self.on_track_clicked(idx)
        
        return item
    
    def update_now_playing(self, track_index):
        """Update the now playing display for a given track"""
        if 0 <= track_index < len(self.tracks):
            track = self.tracks[track_index]
            self.current_track_index = track_index
            
            # Update song name
            self.song_name_label.setText(track.get('name', 'Unknown'))
            
            # Update set indicator
            self.set_indicator_label.setText(track.get('set', 'SET I'))
            
            # Update track counter
            self.track_counter.setText(f"Track {track_index + 1} of {len(self.tracks)}")
            
            # Highlight current track in setlist
            self.highlight_current_track(track_index)
    
    def highlight_current_track(self, index):
        """Highlight the current track in the setlist"""
        for i, widget in enumerate(self.track_widgets):
            if i == index:
                widget.setStyleSheet("""
                    QFrame {
                        background-color: #1F2937;
                        border-radius: 4px;
                        padding: 8px;
                    }
                """)
            else:
                widget.setStyleSheet("""
                    QFrame {
                        background-color: transparent;
                        border-radius: 4px;
                        padding: 8px;
                    }
                    QFrame:hover {
                        background-color: #1F2937;
                    }
                """)
    
    def on_track_clicked(self, index):
        """Handle track click - jump to that track"""
        print(f"[INFO] Track {index + 1} clicked")
        self.update_now_playing(index)
        # TODO: Actually start playing this track when audio is integrated
    
    def on_play_pause_clicked(self):
        """Handle play/pause button click"""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_pause_btn.setText("||")
            print("[INFO] Play button clicked")
        else:
            self.play_pause_btn.setText(">")
            print("[INFO] Pause button clicked")
        # TODO: Connect to actual audio player
    
    def on_volume_changed(self, value):
        """Handle volume slider change"""
        self.volume_label.setText(f"{value}%")
        print(f"[INFO] Volume changed to {value}%")
        # TODO: Connect to actual audio player
    
    def on_browse_clicked(self):
        """Handle browse button click"""
        print("[INFO] Browse button clicked from Player screen")
        self.browse_requested.emit()


# Standalone test
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create player screen
    player = PlayerScreen()
    player.setWindowTitle("DeadStream - Player Screen Test")
    player.resize(1024, 600)
    
    # Load test data
    test_show = {
        'date': '1977-05-08',
        'venue': 'Barton Hall, Cornell University',
        'city': 'Ithaca',
        'state': 'NY',
        'source': 'Soundboard',
        'rating': 4.8
    }
    
    test_tracks = [
        {'name': 'New Minglewood Blues', 'duration': '4:32', 'set': 'SET I'},
        {'name': 'Loser', 'duration': '7:15', 'set': 'SET I'},
        {'name': 'El Paso', 'duration': '4:41', 'set': 'SET I'},
        {'name': 'They Love Each Other', 'duration': '7:23', 'set': 'SET I'},
        {'name': 'Jack Straw', 'duration': '5:12', 'set': 'SET I'},
        {'name': 'Deal', 'duration': '5:34', 'set': 'SET I'},
        {'name': 'Lazy Lightning', 'duration': '3:12', 'set': 'SET I'},
        {'name': 'Supplication', 'duration': '4:45', 'set': 'SET I'},
        {'name': 'Scarlet Begonias', 'duration': '10:48', 'set': 'SET II'},
        {'name': 'Fire on the Mountain', 'duration': '10:23', 'set': 'SET II'},
        {'name': 'Estimated Prophet', 'duration': '9:34', 'set': 'SET II'},
        {'name': 'St. Stephen', 'duration': '7:12', 'set': 'SET II'},
        {'name': 'Not Fade Away', 'duration': '8:45', 'set': 'SET II'},
        {'name': 'St. Stephen', 'duration': '1:23', 'set': 'SET II'},
        {'name': 'Morning Dew', 'duration': '11:45', 'set': 'SET II'},
        {'name': 'One More Saturday Night', 'duration': '5:12', 'set': 'ENCORE'},
    ]
    
    player.load_show(test_show, test_tracks)
    
    player.show()
    
    print("[INFO] Player screen test running...")
    print("[INFO] - Try clicking tracks in the setlist")
    print("[INFO] - Try the play/pause button")
    print("[INFO] - Try the volume slider")
    print("[INFO] - Try the 'Browse Shows' button")
    
    sys.exit(app.exec_())
