#!/usr/bin/env python3
"""
Player screen for DeadStream - Now Playing Interface
Matches the reference React design exactly

Phase 9 Task 9.1.1: Styling refinement based on perfect reference
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
    Now Playing screen - exact match to React reference design.
    
    Left panel: Concert info + scrollable setlist
    Right panel: Now playing + playback controls
    """
    
    # Signals
    browse_requested = pyqtSignal()  # User wants to browse shows
    
    def __init__(self):
        """Initialize player screen"""
        super().__init__()
        
        # Current show data
        self.current_show = None
        self.current_track_index = 0
        self.tracks = []
        self.is_playing = False
        self.is_favorited = False
        
        # Track list item widgets (for highlighting)
        self.track_widgets = []
        
        self.init_ui()
    
    def init_ui(self):
        """Set up the player screen UI"""
        # Main horizontal layout (50/50 split)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left panel: Concert info + setlist
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel: Now playing + controls
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        
        # Apply dark theme styling
        self.apply_styling()
    
    def create_left_panel(self):
        """Create left panel with concert info and setlist"""
        panel = QFrame()
        panel.setObjectName("leftPanel")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Concert header (fixed at top)
        header = self.create_concert_header()
        layout.addWidget(header)
        
        # Setlist (scrollable)
        setlist_scroll = self.create_setlist_scroll()
        layout.addWidget(setlist_scroll)
        
        panel.setLayout(layout)
        return panel
    
    def create_concert_header(self):
        """Create concert header - matches React reference exactly"""
        header = QFrame()
        header.setObjectName("concertHeader")
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(24, 20, 24, 20)
        header_layout.setSpacing(12)
        
        # Top row: Title + Favorite button
        top_row = QHBoxLayout()
        top_row.setSpacing(16)
        
        # Title container
        title_container = QVBoxLayout()
        title_container.setSpacing(4)
        
        # Concert title
        self.concert_title_label = QLabel("Select a show to play")
        self.concert_title_label.setFont(QFont("SF Pro Display, system-ui, sans-serif", 24, QFont.DemiBold))
        self.concert_title_label.setWordWrap(True)
        title_container.addWidget(self.concert_title_label)
        
        # Location
        self.location_label = QLabel("Browse shows to get started")
        self.location_label.setFont(QFont("SF Pro Display, system-ui, sans-serif", 18))
        self.location_label.setStyleSheet("color: #9CA3AF;")
        title_container.addWidget(self.location_label)
        
        top_row.addLayout(title_container, 1)
        
        # Favorite button - using lucide-react Heart icon styling
        self.favorite_button = QPushButton("♥")
        self.favorite_button.setFont(QFont("SF Pro Display, system-ui, sans-serif", 28))
        self.favorite_button.setFixedSize(56, 56)
        self.favorite_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 28px;
                color: #9CA3AF;
            }
            QPushButton:hover {
                background-color: rgba(31, 41, 55, 0.5);
            }
        """)
        self.favorite_button.clicked.connect(self.on_favorite_clicked)
        self.favorite_button.hide()
        top_row.addWidget(self.favorite_button, 0, Qt.AlignTop)
        
        header_layout.addLayout(top_row)
        
        # Metadata row
        metadata_row = QHBoxLayout()
        metadata_row.setSpacing(16)
        
        # Source badge
        self.source_badge = QLabel("Soundboard")
        self.source_badge.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        self.source_badge.setStyleSheet("""
            QLabel {
                background-color: #1F2937;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
            }
        """)
        self.source_badge.hide()
        metadata_row.addWidget(self.source_badge)
        
        # Rating
        self.rating_label = QLabel("★ 4.8/5.0")
        self.rating_label.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        self.rating_label.setStyleSheet("color: #9CA3AF;")
        self.rating_label.hide()
        metadata_row.addWidget(self.rating_label)
        
        # Bullet separator
        bullet = QLabel("•")
        bullet.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        bullet.setStyleSheet("color: #4B5563;")
        bullet.hide()
        self.separator_bullet = bullet
        metadata_row.addWidget(bullet)
        
        # Track count
        self.track_count_label = QLabel("20 tracks")
        self.track_count_label.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        self.track_count_label.setStyleSheet("color: #9CA3AF;")
        self.track_count_label.hide()
        metadata_row.addWidget(self.track_count_label)
        
        metadata_row.addStretch()
        
        header_layout.addLayout(metadata_row)
        
        header.setLayout(header_layout)
        return header
    
    def create_setlist_scroll(self):
        """Create scrollable setlist area"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setObjectName("setlistScroll")
        
        # Setlist container
        self.setlist_container = QWidget()
        self.setlist_layout = QVBoxLayout()
        self.setlist_layout.setSpacing(0)
        self.setlist_layout.setContentsMargins(24, 16, 24, 16)
        
        # Placeholder text
        placeholder = QLabel("Setlist will appear here when a show is loaded")
        placeholder.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
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
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(0)
        
        # Main content (centered vertically)
        layout.addStretch(1)
        
        # Now playing section
        now_playing = self.create_now_playing_section()
        layout.addWidget(now_playing)
        
        layout.addSpacing(32)
        
        # Progress bar
        progress = self.create_progress_bar()
        layout.addWidget(progress)
        
        layout.addSpacing(32)
        
        # Playback controls
        controls = self.create_playback_controls()
        layout.addWidget(controls)
        
        layout.addSpacing(24)
        
        # Track counter
        self.track_counter = QLabel("Track 1 of 20")
        self.track_counter.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        self.track_counter.setStyleSheet("color: #6B7280;")
        self.track_counter.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.track_counter)
        
        layout.addSpacing(24)
        
        # Volume control
        volume = self.create_volume_control()
        layout.addWidget(volume)
        
        layout.addStretch(1)
        
        # Browse button at bottom
        browse_btn = QPushButton("Browse Shows")
        browse_btn.setFont(QFont("SF Pro Text, system-ui, sans-serif", 16, QFont.DemiBold))
        browse_btn.setMinimumHeight(64)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: white;
                border: none;
                border-radius: 8px;
                border-top: 1px solid #374151;
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
    
    def create_now_playing_section(self):
        """Create now playing section - matches React reference"""
        container = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # "NOW PLAYING" label
        now_playing_label = QLabel("NOW PLAYING")
        now_playing_label.setFont(QFont("SF Pro Text, system-ui, sans-serif", 12, QFont.Medium))
        now_playing_label.setStyleSheet("color: #6B7280; letter-spacing: 1.5px;")
        layout.addWidget(now_playing_label)
        
        # Song name (large, bold)
        self.song_name_label = QLabel("Dark Star")
        self.song_name_label.setFont(QFont("SF Pro Display, system-ui, sans-serif", 36, QFont.Bold))
        self.song_name_label.setWordWrap(True)
        layout.addWidget(self.song_name_label)
        
        # Set name
        self.set_name_label = QLabel("SET I")
        self.set_name_label.setFont(QFont("SF Pro Display, system-ui, sans-serif", 20))
        self.set_name_label.setStyleSheet("color: #9CA3AF;")
        layout.addWidget(self.set_name_label)
        
        container.setLayout(layout)
        return container
    
    def create_progress_bar(self):
        """Create progress bar with time labels"""
        container = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(16, 0, 16, 0)
        
        # Progress slider
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(1000)
        self.progress_slider.setValue(0)
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: none;
                height: 8px;
                background: #374151;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #3B82F6;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_slider)
        
        # Time labels
        time_layout = QHBoxLayout()
        
        self.current_time_label = QLabel("3:42")
        self.current_time_label.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        self.current_time_label.setStyleSheet("color: #6B7280;")
        time_layout.addWidget(self.current_time_label)
        
        time_layout.addStretch()
        
        self.total_time_label = QLabel("11:45")
        self.total_time_label.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        self.total_time_label.setStyleSheet("color: #6B7280;")
        time_layout.addWidget(self.total_time_label)
        
        layout.addLayout(time_layout)
        
        container.setLayout(layout)
        return container
    
    def create_playback_controls(self):
        """Create playback controls - matches React reference exactly"""
        container = QFrame()
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)
        
        # Main controls row (prev, play/pause, next)
        main_controls = QHBoxLayout()
        main_controls.setSpacing(24)
        main_controls.setAlignment(Qt.AlignCenter)
        
        # Previous button
        prev_btn = QPushButton("⏮")
        prev_btn.setFont(QFont("SF Pro Display, system-ui, sans-serif", 28))
        prev_btn.setFixedSize(64, 64)
        prev_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 32px;
            }
            QPushButton:hover {
                background-color: rgba(31, 41, 55, 0.5);
            }
            QPushButton:pressed {
                background-color: #1F2937;
            }
        """)
        main_controls.addWidget(prev_btn)
        
        # Play/Pause button (large white circle)
        self.play_pause_btn = QPushButton("⏸")
        self.play_pause_btn.setFont(QFont("SF Pro Display, system-ui, sans-serif", 40))
        self.play_pause_btn.setFixedSize(96, 96)
        self.play_pause_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                border-radius: 48px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
            QPushButton:pressed {
                background-color: #D1D5DB;
            }
        """)
        self.play_pause_btn.clicked.connect(self.on_play_pause_clicked)
        main_controls.addWidget(self.play_pause_btn)
        
        # Next button
        next_btn = QPushButton("⏭")
        next_btn.setFont(QFont("SF Pro Display, system-ui, sans-serif", 28))
        next_btn.setFixedSize(64, 64)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 32px;
            }
            QPushButton:hover {
                background-color: rgba(31, 41, 55, 0.5);
            }
            QPushButton:pressed {
                background-color: #1F2937;
            }
        """)
        main_controls.addWidget(next_btn)
        
        layout.addLayout(main_controls)
        
        # 30-second skip controls
        skip_controls = QHBoxLayout()
        skip_controls.setSpacing(16)
        skip_controls.setAlignment(Qt.AlignCenter)
        
        # Rewind 30s - icon + text layout
        rewind_btn = QPushButton("⟲  30s")
        rewind_btn.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14, QFont.DemiBold))
        rewind_btn.setMinimumHeight(40)
        rewind_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:pressed {
                background-color: #111827;
            }
        """)
        skip_controls.addWidget(rewind_btn)
        
        # Skip 30s - text + icon layout
        skip_btn = QPushButton("30s  ⟳")
        skip_btn.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14, QFont.DemiBold))
        skip_btn.setMinimumHeight(40)
        skip_btn.setStyleSheet("""
            QPushButton {
                background-color: #1F2937;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:pressed {
                background-color: #111827;
            }
        """)
        skip_controls.addWidget(skip_btn)
        
        layout.addLayout(skip_controls)
        
        container.setLayout(layout)
        return container
    
    def create_volume_control(self):
        """Create volume control - matches React reference"""
        container = QFrame()
        layout = QHBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(16, 0, 16, 0)
        
        # Mute button
        self.mute_btn = QPushButton("🔊")
        self.mute_btn.setFont(QFont("SF Pro Display, system-ui, sans-serif", 20))
        self.mute_btn.setFixedSize(48, 48)
        self.mute_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #9CA3AF;
                border: none;
                border-radius: 24px;
            }
            QPushButton:hover {
                background-color: rgba(31, 41, 55, 0.5);
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
                height: 8px;
                background: #374151;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 0px;
                height: 0px;
            }
            QSlider::sub-page:horizontal {
                background: #3B82F6;
                border-radius: 4px;
            }
        """)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        layout.addWidget(self.volume_slider)
        
        # Volume percentage
        self.volume_label = QLabel("75%")
        self.volume_label.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        self.volume_label.setStyleSheet("color: #9CA3AF;")
        self.volume_label.setMinimumWidth(48)
        self.volume_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.volume_label)
        
        container.setLayout(layout)
        return container
    
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
                set_header = QLabel(track_set.upper())
                set_header.setFont(QFont("SF Pro Text, system-ui, sans-serif", 12, QFont.DemiBold))
                set_header.setStyleSheet("""
                    color: #6B7280;
                    letter-spacing: 1.5px;
                    padding: 16px 12px 8px 12px;
                """)
                self.setlist_layout.addWidget(set_header)
                current_set = track_set
            
            # Create track item
            track_item = self.create_track_item(i, track)
            self.setlist_layout.addWidget(track_item)
            self.track_widgets.append(track_item)
        
        self.setlist_layout.addStretch()
    
    def create_track_item(self, index, track):
        """Create a single track item - matches React reference"""
        item = QFrame()
        item.setObjectName(f"trackItem_{index}")
        item.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)
        
        # Track number
        num_label = QLabel(f"{index + 1}")
        num_label.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        num_label.setStyleSheet("color: #6B7280;")
        num_label.setFixedWidth(24)
        layout.addWidget(num_label)
        
        # Song name
        name_label = QLabel(track.get('name', 'Unknown'))
        name_label.setFont(QFont("SF Pro Text, system-ui, sans-serif", 16))
        layout.addWidget(name_label, 1)
        
        # Duration
        duration_label = QLabel(track.get('duration', '0:00'))
        duration_label.setFont(QFont("SF Pro Text, system-ui, sans-serif", 14))
        duration_label.setStyleSheet("color: #6B7280;")
        duration_label.setAlignment(Qt.AlignRight)
        layout.addWidget(duration_label)
        
        item.setLayout(layout)
        
        # Store index
        item.track_index = index
        
        # Make clickable
        item.mousePressEvent = lambda event, idx=index: self.on_track_clicked(idx)
        
        return item
    
    def apply_styling(self):
        """Apply dark theme styling"""
        self.setStyleSheet("""
            PlayerScreen {
                background-color: #000000;
            }
            QFrame#leftPanel {
                background-color: #000000;
                border-right: 1px solid #1F2937;
            }
            QFrame#concertHeader {
                border-bottom: 1px solid #1F2937;
            }
            QFrame#setlistScroll {
                background-color: #000000;
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
            QFrame[objectName^="trackItem_"] {
                background-color: transparent;
                border-radius: 8px;
            }
            QFrame[objectName^="trackItem_"]:hover {
                background-color: rgba(17, 24, 39, 0.5);
            }
        """)
    
    def load_show(self, show_data, tracks_data):
        """Load a show into the player screen"""
        self.current_show = show_data
        self.tracks = tracks_data
        self.current_track_index = 0
        
        # Update header
        date = show_data.get('date', 'Unknown Date')
        venue = show_data.get('venue', 'Unknown Venue')
        city = show_data.get('city', '')
        state = show_data.get('state', '')
        
        # Format: YYYY/MM/DD Venue Name
        title = f"{date.replace('-', '/')} {venue}"
        self.concert_title_label.setText(title)
        
        # Location
        location = f"{city}, {state}" if city and state else ""
        self.location_label.setText(location)
        
        # Metadata
        source = show_data.get('source', 'Unknown')
        self.source_badge.setText(source)
        self.source_badge.show()
        
        rating = show_data.get('rating', 0)
        if rating > 0:
            self.rating_label.setText(f"★ {rating:.1f}/5.0")
            self.rating_label.show()
            self.separator_bullet.show()
        
        track_count = len(tracks_data)
        self.track_count_label.setText(f"{track_count} tracks")
        self.track_count_label.show()
        
        self.favorite_button.show()
        
        # Build setlist
        self.build_setlist(tracks_data)
        
        # Update now playing
        if tracks_data:
            self.update_now_playing(0)
    
    def update_now_playing(self, track_index):
        """Update now playing display"""
        if 0 <= track_index < len(self.tracks):
            track = self.tracks[track_index]
            self.current_track_index = track_index
            
            # Update display
            self.song_name_label.setText(track.get('name', 'Unknown'))
            self.set_name_label.setText(track.get('set', 'SET I'))
            self.track_counter.setText(f"Track {track_index + 1} of {len(self.tracks)}")
            
            # Highlight track
            self.highlight_current_track(track_index)
    
    def highlight_current_track(self, index):
        """Highlight the current track"""
        for i, widget in enumerate(self.track_widgets):
            if i == index:
                widget.setStyleSheet("""
                    QFrame {
                        background-color: #1F2937;
                        border-radius: 8px;
                    }
                    QLabel {
                        color: white;
                    }
                """)
                # Make track name bold
                for child in widget.findChildren(QLabel):
                    if "Unknown" in child.text() or any(char.isalpha() for char in child.text()[:5]):
                        font = child.font()
                        font.setWeight(QFont.DemiBold)
                        child.setFont(font)
            else:
                widget.setStyleSheet("""
                    QFrame {
                        background-color: transparent;
                        border-radius: 8px;
                    }
                    QFrame:hover {
                        background-color: rgba(17, 24, 39, 0.5);
                    }
                """)
    
    def on_track_clicked(self, index):
        """Handle track click"""
        print(f"[INFO] Track {index + 1} clicked")
        self.update_now_playing(index)
    
    def on_play_pause_clicked(self):
        """Handle play/pause"""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_pause_btn.setText("⏸")
            print("[INFO] Playing")
        else:
            self.play_pause_btn.setText("▶")
            print("[INFO] Paused")
    
    def on_favorite_clicked(self):
        """Handle favorite toggle"""
        self.is_favorited = not self.is_favorited
        if self.is_favorited:
            self.favorite_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 28px;
                    color: #EF4444;
                }
                QPushButton:hover {
                    background-color: rgba(31, 41, 55, 0.5);
                }
            """)
            print("[INFO] Favorited")
        else:
            self.favorite_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 28px;
                    color: #9CA3AF;
                }
                QPushButton:hover {
                    background-color: rgba(31, 41, 55, 0.5);
                }
            """)
            print("[INFO] Unfavorited")
    
    def on_volume_changed(self, value):
        """Handle volume change"""
        self.volume_label.setText(f"{value}%")
        print(f"[INFO] Volume: {value}%")
    
    def on_browse_clicked(self):
        """Handle browse button"""
        print("[INFO] Browse Shows clicked")
        self.browse_requested.emit()


# Standalone test
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    player = PlayerScreen()
    player.setWindowTitle("DeadStream - Player (Reference Design)")
    player.setFixedSize(1280, 720)
    
    # Load Cornell '77
    test_show = {
        'date': '1977-05-08',
        'venue': 'Barton Hall, Cornell University',
        'city': 'Ithaca',
        'state': 'NY',
        'source': 'Soundboard',
        'rating': 4.8
    }
    
    test_tracks = [
        {'name': 'New Minglewood Blues', 'duration': '5:42', 'set': 'Set I'},
        {'name': 'Loser', 'duration': '7:08', 'set': 'Set I'},
        {'name': 'El Paso', 'duration': '4:38', 'set': 'Set I'},
        {'name': 'They Love Each Other', 'duration': '7:26', 'set': 'Set I'},
        {'name': 'Jack Straw', 'duration': '5:15', 'set': 'Set I'},
        {'name': 'Deal', 'duration': '5:26', 'set': 'Set I'},
        {'name': 'Scarlet Begonias', 'duration': '10:22', 'set': 'Set II'},
        {'name': 'Fire on the Mountain', 'duration': '14:51', 'set': 'Set II'},
        {'name': 'Morning Dew', 'duration': '11:51', 'set': 'Set II'},
        {'name': 'One More Saturday Night', 'duration': '4:58', 'set': 'Encore'},
    ]
    
    player.load_show(test_show, test_tracks)
    player.show()
    
    print("[INFO] Reference design player running...")
    print("[INFO] This matches the React reference exactly")
    
    sys.exit(app.exec_())
