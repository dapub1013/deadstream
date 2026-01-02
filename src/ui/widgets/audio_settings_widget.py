#!/usr/bin/env python3
"""
DeadStream Audio Settings Widget
Phase 8, Task 8.5: Audio output and quality settings

Provides controls for:
- Default volume level
- Audio quality preferences (FLAC vs MP3)
- Audio output information
"""

import sys
import os

# Path manipulation for imports (4 levels up from src/ui/widgets/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QFrame, QPushButton, QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from src.settings import get_settings


class AudioSettingsWidget(QWidget):
    """Widget for audio configuration settings"""
    
    # Signal emitted when settings change
    volume_changed = pyqtSignal(int)  # New default volume
    quality_changed = pyqtSignal(str)  # 'flac' or 'mp3'
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # Load settings from SettingsManager
        settings = get_settings()
        self.default_volume = settings.get('audio', 'default_volume', 77)

        # Map quality_preference to UI format (balanced -> flac, audiophile -> flac, crowd_favorite -> mp3)
        quality_pref = settings.get('audio', 'quality_preference', 'balanced')
        if quality_pref == 'audiophile':
            self.preferred_quality = 'flac'
        elif quality_pref == 'crowd_favorite':
            self.preferred_quality = 'mp3'
        else:  # balanced (default)
            self.preferred_quality = 'flac'

        self.init_ui()
    
    def init_ui(self):
        """Initialize the audio settings UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(30)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Volume settings card
        volume_card = self._create_volume_card()
        main_layout.addWidget(volume_card)
        
        # Quality settings card
        quality_card = self._create_quality_card()
        main_layout.addWidget(quality_card)
        
        # Audio output info card
        output_card = self._create_output_info_card()
        main_layout.addWidget(output_card)
        
        # Stretch at bottom
        main_layout.addStretch()
    
    def _create_header(self):
        """Create the header section"""
        header = QWidget()
        layout = QVBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("Audio Settings")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Configure volume and audio quality preferences")
        subtitle.setStyleSheet("""
            color: #9ca3af;
            font-size: 14px;
        """)
        layout.addWidget(subtitle)
        
        return header
    
    def _create_volume_card(self):
        """Create the volume settings card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1f1f1f;
                border: 1px solid #333333;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Card title
        title = QLabel("Default Volume Level")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Set the initial volume level when starting playback")
        desc.setStyleSheet("""
            color: #9ca3af;
            font-size: 13px;
        """)
        layout.addWidget(desc)
        
        # Volume slider with label
        slider_layout = QHBoxLayout()
        slider_layout.setSpacing(15)
        
        # Volume icon/label
        vol_label = QLabel("Volume:")
        vol_label.setStyleSheet("""
            color: #ffffff;
            font-size: 14px;
            font-weight: 500;
        """)
        slider_layout.addWidget(vol_label)
        
        # Slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.default_volume)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.setTickInterval(25)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #333333;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #8b5cf6;
                width: 24px;
                height: 24px;
                margin: -8px 0;
                border-radius: 12px;
            }
            QSlider::handle:horizontal:hover {
                background: #a78bfa;
            }
            QSlider::sub-page:horizontal {
                background: #8b5cf6;
                border-radius: 4px;
            }
        """)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        slider_layout.addWidget(self.volume_slider, stretch=1)
        
        # Volume percentage label
        self.volume_value_label = QLabel(f"{self.default_volume}%")
        self.volume_value_label.setFixedWidth(50)
        self.volume_value_label.setStyleSheet("""
            color: #ffffff;
            font-size: 16px;
            font-weight: bold;
        """)
        slider_layout.addWidget(self.volume_value_label)
        
        layout.addLayout(slider_layout)
        
        # Info note
        note = QLabel("[INFO] This sets the volume when you first start playing a show. "
                     "You can adjust volume during playback.")
        note.setWordWrap(True)
        note.setStyleSheet("""
            color: #6b7280;
            font-size: 12px;
            font-style: italic;
        """)
        layout.addWidget(note)
        
        return card
    
    def _create_quality_card(self):
        """Create the audio quality preference card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1f1f1f;
                border: 1px solid #333333;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Card title
        title = QLabel("Preferred Audio Quality")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Choose which audio format to prefer when multiple versions are available")
        desc.setWordWrap(True)
        desc.setStyleSheet("""
            color: #9ca3af;
            font-size: 13px;
        """)
        layout.addWidget(desc)
        
        # Radio button group
        self.quality_group = QButtonGroup(self)
        
        # FLAC option
        flac_radio = QRadioButton("FLAC (Lossless)")
        flac_radio.setStyleSheet("""
            QRadioButton {
                color: #ffffff;
                font-size: 14px;
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QRadioButton::indicator:unchecked {
                background: #333333;
                border: 2px solid #6b7280;
                border-radius: 10px;
            }
            QRadioButton::indicator:checked {
                background: #8b5cf6;
                border: 2px solid #8b5cf6;
                border-radius: 10px;
            }
        """)
        flac_radio.setChecked(True)  # Default
        self.quality_group.addButton(flac_radio, 0)
        layout.addWidget(flac_radio)
        
        # FLAC description
        flac_desc = QLabel("    Highest quality, larger file size, may use more bandwidth")
        flac_desc.setStyleSheet("""
            color: #6b7280;
            font-size: 12px;
        """)
        layout.addWidget(flac_desc)
        
        # MP3 option
        mp3_radio = QRadioButton("MP3 (Compressed)")
        mp3_radio.setStyleSheet("""
            QRadioButton {
                color: #ffffff;
                font-size: 14px;
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QRadioButton::indicator:unchecked {
                background: #333333;
                border: 2px solid #6b7280;
                border-radius: 10px;
            }
            QRadioButton::indicator:checked {
                background: #8b5cf6;
                border: 2px solid #8b5cf6;
                border-radius: 10px;
            }
        """)
        self.quality_group.addButton(mp3_radio, 1)
        layout.addWidget(mp3_radio)
        
        # MP3 description
        mp3_desc = QLabel("    Good quality, smaller file size, faster streaming")
        mp3_desc.setStyleSheet("""
            color: #6b7280;
            font-size: 12px;
        """)
        layout.addWidget(mp3_desc)
        
        # Connect signal
        self.quality_group.buttonClicked.connect(self._on_quality_changed)
        
        # Info note
        note = QLabel("[INFO] DeadStream's smart selection already considers quality. "
                     "This preference applies when multiple high-quality versions exist.")
        note.setWordWrap(True)
        note.setStyleSheet("""
            color: #6b7280;
            font-size: 12px;
            font-style: italic;
            margin-top: 10px;
        """)
        layout.addWidget(note)
        
        return card
    
    def _create_output_info_card(self):
        """Create the audio output information card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1f1f1f;
                border: 1px solid #333333;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Card title
        title = QLabel("Audio Output Information")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff;")
        layout.addWidget(title)
        
        # Info rows
        info_items = [
            ("Output Device:", "Raspberry Pi Audio (ALSA)"),
            ("Sample Rate:", "44.1 kHz / 16-bit"),
            ("Channels:", "Stereo (2.0)"),
            ("Buffer Size:", "8000 ms (network streaming)"),
        ]
        
        for label_text, value_text in info_items:
            row = QHBoxLayout()
            row.setSpacing(10)
            
            label = QLabel(label_text)
            label.setStyleSheet("""
                color: #9ca3af;
                font-size: 13px;
            """)
            row.addWidget(label)
            
            value = QLabel(value_text)
            value.setStyleSheet("""
                color: #ffffff;
                font-size: 13px;
                font-weight: 500;
            """)
            row.addWidget(value, stretch=1)
            
            layout.addLayout(row)
        
        # Note about DAC
        note = QLabel("[INFO] Advanced audio configuration (DAC output) will be available "
                     "in a future update.")
        note.setWordWrap(True)
        note.setStyleSheet("""
            color: #6b7280;
            font-size: 12px;
            font-style: italic;
            margin-top: 10px;
        """)
        layout.addWidget(note)
        
        return card
    
    def _on_volume_changed(self, value):
        """Handle volume slider changes"""
        self.default_volume = value
        self.volume_value_label.setText(f"{value}%")

        # Persist to SettingsManager
        settings = get_settings()
        settings.set('audio', 'default_volume', value)
        print(f"[INFO] Audio: Default volume saved to settings: {value}%")

        self.volume_changed.emit(value)
    
    def _on_quality_changed(self, button):
        """Handle quality preference changes"""
        button_id = self.quality_group.id(button)

        if button_id == 0:  # FLAC
            self.preferred_quality = 'flac'
        else:  # MP3
            self.preferred_quality = 'mp3'

        # Persist to SettingsManager (map UI choice to quality_preference)
        settings = get_settings()
        if self.preferred_quality == 'flac':
            settings.set('audio', 'quality_preference', 'audiophile')
        else:  # mp3
            settings.set('audio', 'quality_preference', 'crowd_favorite')
        print(f"[INFO] Audio: Quality preference saved to settings: {self.preferred_quality}")

        self.quality_changed.emit(self.preferred_quality)
    
    def get_volume(self):
        """Get the current default volume setting"""
        return self.default_volume
    
    def set_volume(self, volume):
        """Set the default volume (0-100)"""
        if 0 <= volume <= 100:
            self.volume_slider.setValue(volume)
    
    def get_quality(self):
        """Get the preferred quality setting"""
        return self.preferred_quality
    
    def set_quality(self, quality):
        """Set the preferred quality ('flac' or 'mp3')"""
        if quality == 'flac':
            self.quality_group.button(0).setChecked(True)
        elif quality == 'mp3':
            self.quality_group.button(1).setChecked(True)


# Test function for standalone testing
def test_audio_settings():
    """Test the audio settings widget"""
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Create and show widget
    widget = AudioSettingsWidget()
    widget.setStyleSheet("background-color: #121212;")
    widget.resize(700, 600)
    widget.show()
    
    # Connect signals for testing
    widget.volume_changed.connect(
        lambda v: print(f"[TEST] Volume changed to: {v}%")
    )
    widget.quality_changed.connect(
        lambda q: print(f"[TEST] Quality changed to: {q}")
    )
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    test_audio_settings()