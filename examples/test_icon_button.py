"""
Test script for IconButton component.

Displays all icon types and style variants:
- Icon types: home, settings, search, back, forward, close, menu, random
- Variants: solid, transparent, outline, accent
- Interactive hover/pressed feedback
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QGroupBox
)
from PyQt5.QtCore import Qt
from src.ui.styles.theme import Theme
from src.ui.components.icon_button import IconButton


class IconButtonDemo(QWidget):
    """Demo window showing all IconButton types and variants."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("IconButton Component Test")
        self.resize(900, 800)
        
        # Apply global theme
        self.setStyleSheet(Theme.get_global_stylesheet())
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(Theme.SPACING_LARGE)
        main_layout.setContentsMargins(
            Theme.MARGIN_LARGE,
            Theme.MARGIN_LARGE,
            Theme.MARGIN_LARGE,
            Theme.MARGIN_LARGE
        )
        
        # Title
        title = QLabel("IconButton Component Demo")
        title.setStyleSheet(f"""
            font-size: {Theme.HEADER_MEDIUM}px;
            font-weight: {Theme.WEIGHT_BOLD};
            color: {Theme.TEXT_PRIMARY};
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Circular icon buttons for navigation and actions")
        subtitle.setStyleSheet(f"""
            font-size: {Theme.BODY_LARGE}px;
            color: {Theme.TEXT_SECONDARY};
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        
        # Icon types group
        icons_group = self._create_icon_types_group()
        main_layout.addWidget(icons_group)
        
        # Style variants group
        variants_group = self._create_variants_group()
        main_layout.addWidget(variants_group)
        
        # Common layouts group
        layouts_group = self._create_layouts_group()
        main_layout.addWidget(layouts_group)
        
        # Status label
        self.status_label = QLabel("Click any icon button to see status")
        self.status_label.setStyleSheet(f"""
            font-size: {Theme.BODY_MEDIUM}px;
            color: {Theme.TEXT_SECONDARY};
            padding: {Theme.SPACING_MEDIUM}px;
            background-color: {Theme.BG_CARD};
            border-radius: 8px;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def _create_icon_types_group(self):
        """Create group showing all icon types."""
        group = QGroupBox("Icon Types")
        group.setStyleSheet(self._get_group_style())
        
        layout = QHBoxLayout()
        layout.setSpacing(Theme.SPACING_MEDIUM)
        
        # Create button for each icon type
        icon_types = [
            ('home', 'Home'),
            ('settings', 'Settings'),
            ('search', 'Search'),
            ('back', 'Back'),
            ('forward', 'Forward'),
            ('close', 'Close'),
            ('menu', 'Menu'),
            ('random', 'Random'),
        ]
        
        for icon_type, label in icon_types:
            container = QVBoxLayout()
            container.setSpacing(Theme.SPACING_SMALL)
            
            btn = IconButton(icon_type=icon_type, variant='solid')
            btn.clicked.connect(lambda checked, t=icon_type: self.on_icon_clicked(t))
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"""
                font-size: {Theme.BODY_SMALL}px;
                color: {Theme.TEXT_SECONDARY};
            """)
            label_widget.setAlignment(Qt.AlignCenter)
            
            container.addWidget(btn, alignment=Qt.AlignCenter)
            container.addWidget(label_widget)
            
            layout.addLayout(container)
        
        group.setLayout(layout)
        return group
    
    def _create_variants_group(self):
        """Create group showing all style variants."""
        group = QGroupBox("Style Variants")
        group.setStyleSheet(self._get_group_style())
        
        layout = QHBoxLayout()
        layout.setSpacing(Theme.SPACING_LARGE)
        
        # Create button for each variant
        variants = [
            ('solid', 'Solid'),
            ('transparent', 'Transparent'),
            ('outline', 'Outline'),
            ('accent', 'Accent'),
        ]
        
        for variant, label in variants:
            container = QVBoxLayout()
            container.setSpacing(Theme.SPACING_SMALL)
            
            btn = IconButton(icon_type='settings', variant=variant)
            btn.clicked.connect(lambda checked, v=variant: self.on_variant_clicked(v))
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"""
                font-size: {Theme.BODY_SMALL}px;
                color: {Theme.TEXT_SECONDARY};
            """)
            label_widget.setAlignment(Qt.AlignCenter)
            
            container.addWidget(btn, alignment=Qt.AlignCenter)
            container.addWidget(label_widget)
            
            layout.addLayout(container)
        
        group.setLayout(layout)
        return group
    
    def _create_layouts_group(self):
        """Create group showing common layout patterns."""
        group = QGroupBox("Common Layout Patterns")
        group.setStyleSheet(self._get_group_style())
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(Theme.SPACING_LARGE)
        
        # Header with navigation
        header_label = QLabel("Header Navigation (left + right corners)")
        header_label.setStyleSheet(f"""
            font-size: {Theme.BODY_MEDIUM}px;
            color: {Theme.TEXT_SECONDARY};
        """)
        main_layout.addWidget(header_label)
        
        header_layout = QHBoxLayout()
        home_btn = IconButton(icon_type='home', variant='transparent')
        home_btn.clicked.connect(lambda: self.on_action_clicked('home'))
        header_layout.addWidget(home_btn)
        header_layout.addStretch()
        settings_btn = IconButton(icon_type='settings', variant='transparent')
        settings_btn.clicked.connect(lambda: self.on_action_clicked('settings'))
        header_layout.addWidget(settings_btn)
        main_layout.addLayout(header_layout)
        
        # Action bar
        action_label = QLabel("Action Bar (centered controls)")
        action_label.setStyleSheet(f"""
            font-size: {Theme.BODY_MEDIUM}px;
            color: {Theme.TEXT_SECONDARY};
        """)
        main_layout.addWidget(action_label)
        
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        back_btn = IconButton(icon_type='back', variant='solid')
        back_btn.clicked.connect(lambda: self.on_action_clicked('back'))
        action_layout.addWidget(back_btn)
        
        play_btn = IconButton(icon_type='play', variant='accent')
        play_btn.clicked.connect(lambda: self.on_action_clicked('play'))
        action_layout.addWidget(play_btn)
        
        forward_btn = IconButton(icon_type='forward', variant='solid')
        forward_btn.clicked.connect(lambda: self.on_action_clicked('forward'))
        action_layout.addWidget(forward_btn)
        
        action_layout.addStretch()
        main_layout.addLayout(action_layout)
        
        group.setLayout(main_layout)
        return group
    
    def _get_group_style(self):
        """Get consistent group box styling."""
        return f"""
            QGroupBox {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                border: 2px solid {Theme.BORDER_PANEL};
                border-radius: 8px;
                margin-top: {Theme.SPACING_MEDIUM}px;
                padding: {Theme.SPACING_LARGE}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 {Theme.SPACING_SMALL}px;
            }}
        """
    
    def on_icon_clicked(self, icon_type):
        """Handle icon type button click."""
        self.status_label.setText(f"[INFO] Clicked: {icon_type.upper()} icon")
    
    def on_variant_clicked(self, variant):
        """Handle variant button click."""
        self.status_label.setText(f"[INFO] Clicked: {variant.upper()} variant")
    
    def on_action_clicked(self, action):
        """Handle action button click."""
        self.status_label.setText(f"[INFO] Action: {action.upper()}")


def main():
    """Run the demo application."""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = app.font()
    font.setFamily(Theme.FONT_FAMILY)
    app.setFont(font)
    
    demo = IconButtonDemo()
    demo.show()
    
    print("\n" + "=" * 60)
    print("[INFO] IconButton Component Demo")
    print("=" * 60)
    print("[INFO] Features demonstrated:")
    print("  - 8 icon types (home, settings, search, back, etc.)")
    print("  - 4 style variants (solid, transparent, outline, accent)")
    print("  - Circular 60px touch-friendly design")
    print("  - Hover and pressed state feedback")
    print("  - Common layout patterns")
    print("\n[INFO] Try:")
    print("  - Hover over icons to see highlight")
    print("  - Click to see status messages")
    print("  - Compare solid vs transparent backgrounds")
    print("  - Note perfect circular shape")
    print("\n[INFO] Press Ctrl+C or close window to exit")
    print("=" * 60 + "\n")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()