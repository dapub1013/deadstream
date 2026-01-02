"""
Display Settings Widget
Provides controls for screen brightness, timeout, and theme preferences
"""

import sys
import os

# Path manipulation for subdirectory execution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSlider, QComboBox, QPushButton, QFrame, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from src.settings import get_settings


class DisplaySettingsWidget(QWidget):
    """Widget for managing display settings"""
    
    # Signals
    settings_changed = pyqtSignal(str, object)  # (setting_name, value)
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()
        self.load_current_settings()
    
    def init_ui(self):
        """Initialize the display settings UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(25)
        
        # Header
        header = self._create_header()
        layout.addWidget(header)
        
        # Settings sections
        layout.addWidget(self._create_brightness_section())
        layout.addWidget(self._create_divider())
        layout.addWidget(self._create_timeout_section())
        layout.addWidget(self._create_divider())
        layout.addWidget(self._create_theme_section())
        
        layout.addStretch()
        
        # Action buttons
        layout.addWidget(self._create_action_buttons())
    
    def _create_header(self):
        """Create the header section"""
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)
        
        # Title
        title = QLabel("Display Settings")
        title.setStyleSheet("color: #ffffff; font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Brightness, screen timeout, and theme preferences")
        subtitle.setStyleSheet("color: #999999; font-size: 16px;")
        header_layout.addWidget(subtitle)
        
        return header
    
    def _create_brightness_section(self):
        """Create brightness control section"""
        section = QWidget()
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)
        
        # Section title
        title = QLabel("Screen Brightness")
        title.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 600;")
        section_layout.addWidget(title)
        
        # Brightness card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        
        # Current brightness label
        self.brightness_label = QLabel("Brightness: 75%")
        self.brightness_label.setStyleSheet("color: #ffffff; font-size: 18px;")
        card_layout.addWidget(self.brightness_label)
        
        # Brightness slider
        slider_container = QWidget()
        slider_layout = QHBoxLayout(slider_container)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setSpacing(15)
        
        # Low icon/label
        low_label = QLabel("Low")
        low_label.setStyleSheet("color: #999999; font-size: 14px;")
        slider_layout.addWidget(low_label)
        
        # Slider
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(10)  # Minimum 10% to keep screen visible
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(75)
        self.brightness_slider.setTickPosition(QSlider.TicksBelow)
        self.brightness_slider.setTickInterval(10)
        self.brightness_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #333333;
                height: 8px;
                background: #262626;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2563eb;
                border: 2px solid #1e40af;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #3b82f6;
            }
            QSlider::sub-page:horizontal {
                background: #2563eb;
                border-radius: 4px;
            }
        """)
        self.brightness_slider.valueChanged.connect(self._on_brightness_changed)
        slider_layout.addWidget(self.brightness_slider)
        
        # High icon/label
        high_label = QLabel("High")
        high_label.setStyleSheet("color: #999999; font-size: 14px;")
        slider_layout.addWidget(high_label)
        
        card_layout.addWidget(slider_container)
        
        # Auto-brightness option (placeholder for future)
        auto_brightness_label = QLabel("Auto-brightness based on ambient light (not available)")
        auto_brightness_label.setStyleSheet("color: #666666; font-size: 14px; font-style: italic;")
        card_layout.addWidget(auto_brightness_label)
        
        section_layout.addWidget(card)
        
        return section
    
    def _create_timeout_section(self):
        """Create screen timeout section"""
        section = QWidget()
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)
        
        # Section title
        title = QLabel("Screen Timeout")
        title.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 600;")
        section_layout.addWidget(title)
        
        # Timeout card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        
        # Description
        desc = QLabel("Turn off display after period of inactivity")
        desc.setStyleSheet("color: #999999; font-size: 16px;")
        card_layout.addWidget(desc)
        
        # Timeout selector
        timeout_container = QWidget()
        timeout_layout = QHBoxLayout(timeout_container)
        timeout_layout.setContentsMargins(0, 0, 0, 0)
        timeout_layout.setSpacing(15)
        
        timeout_label = QLabel("Timeout after:")
        timeout_label.setStyleSheet("color: #ffffff; font-size: 16px;")
        timeout_layout.addWidget(timeout_label)
        
        self.timeout_combo = QComboBox()
        self.timeout_combo.addItems([
            "Never",
            "1 minute",
            "2 minutes",
            "5 minutes",
            "10 minutes",
            "15 minutes",
            "30 minutes"
        ])
        self.timeout_combo.setStyleSheet("""
            QComboBox {
                background-color: #262626;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 16px;
                min-width: 200px;
            }
            QComboBox:hover {
                border-color: #2563eb;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 7px solid #ffffff;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #262626;
                color: #ffffff;
                border: 2px solid #333333;
                selection-background-color: #2563eb;
                outline: none;
            }
        """)
        self.timeout_combo.currentTextChanged.connect(self._on_timeout_changed)
        timeout_layout.addWidget(self.timeout_combo)
        
        timeout_layout.addStretch()
        
        card_layout.addWidget(timeout_container)
        
        section_layout.addWidget(card)
        
        return section
    
    def _create_theme_section(self):
        """Create theme preferences section"""
        section = QWidget()
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(15)
        
        # Section title
        title = QLabel("Theme Preferences")
        title.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 600;")
        section_layout.addWidget(title)
        
        # Theme card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        
        # Current theme info
        current_theme = QLabel("Current Theme: Dark (default)")
        current_theme.setStyleSheet("color: #ffffff; font-size: 16px;")
        card_layout.addWidget(current_theme)
        
        # Theme note
        theme_note = QLabel(
            "DeadStream uses a dark theme optimized for viewing concerts in low-light "
            "environments. Additional themes may be added in future versions."
        )
        theme_note.setWordWrap(True)
        theme_note.setStyleSheet("color: #999999; font-size: 14px;")
        card_layout.addWidget(theme_note)
        
        section_layout.addWidget(card)
        
        return section
    
    def _create_divider(self):
        """Create a visual divider line"""
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: #333333; max-height: 1px;")
        return divider
    
    def _create_action_buttons(self):
        """Create action buttons"""
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)
        
        # Reset to defaults button
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #262626;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #333333;
                border-color: #666666;
            }
        """)
        reset_btn.clicked.connect(self._reset_to_defaults)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        return button_container
    
    def _on_brightness_changed(self, value):
        """Handle brightness slider changes"""
        self.brightness_label.setText(f"Brightness: {value}%")

        # Save to SettingsManager
        settings = get_settings()
        settings.set('display', 'brightness', value)
        self.settings_changed.emit('brightness', value)

        # Note: Actual brightness control would require system-level access
        # This is a UI-only implementation for now
        print(f"[INFO] Display: Brightness saved to settings: {value}%")
    
    def _on_timeout_changed(self, value):
        """Handle timeout selection changes"""
        # Save to SettingsManager
        settings = get_settings()
        settings.set('display', 'screen_timeout', value)
        self.settings_changed.emit('screen_timeout', value)

        print(f"[INFO] Display: Screen timeout saved to settings: {value}")
    
    def _reset_to_defaults(self):
        """Reset all display settings to defaults"""
        # Reset brightness to 75%
        self.brightness_slider.setValue(75)
        
        # Reset timeout to "10 minutes"
        self.timeout_combo.setCurrentText("10 minutes")
        
        print("[INFO] Display settings reset to defaults")
    
    def load_current_settings(self):
        """Load current settings from SettingsManager"""
        settings = get_settings()

        # Load brightness
        brightness = settings.get('display', 'brightness', 82)
        self.brightness_slider.setValue(brightness)

        # Load timeout (ensure it's a string for findText)
        timeout = settings.get('display', 'screen_timeout', '10 minutes')
        timeout = str(timeout)  # Convert to string in case YAML loaded it as int
        index = self.timeout_combo.findText(timeout)
        if index >= 0:
            self.timeout_combo.setCurrentIndex(index)


# Standalone test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    widget = DisplaySettingsWidget()
    widget.setStyleSheet("background-color: #121212;")
    widget.setWindowTitle("Display Settings Test")
    widget.setGeometry(100, 100, 1024, 600)
    
    # Connect signals for testing
    widget.settings_changed.connect(
        lambda name, value: print(f"[SIGNAL] Setting changed: {name} = {value}")
    )
    
    widget.show()
    
    print("[INFO] Display settings widget loaded")
    print("[INFO] Try adjusting brightness slider")
    print("[INFO] Try changing screen timeout")
    print("[INFO] Current brightness:", widget.brightness_slider.value())
    print("[INFO] Current timeout:", widget.timeout_combo.currentText())
    
    sys.exit(app.exec_())
