"""
Test script for PillButton component.

Displays all color variants and demonstrates:
- Touch-friendly sizing
- Hover/pressed states
- Variant switching
- Disabled state
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
from src.ui.components.pill_button import PillButton


class PillButtonDemo(QWidget):
    """Demo window showing all PillButton variants."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("PillButton Component Test")
        self.resize(800, 700)
        
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
        title = QLabel("PillButton Component Demo")
        title.setStyleSheet(f"""
            font-size: {Theme.HEADER_MEDIUM}px;
            font-weight: {Theme.WEIGHT_BOLD};
            color: {Theme.TEXT_PRIMARY};
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("All color variants with touch-friendly sizing")
        subtitle.setStyleSheet(f"""
            font-size: {Theme.BODY_LARGE}px;
            color: {Theme.TEXT_SECONDARY};
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        
        # Variant buttons group
        variants_group = self._create_variants_group()
        main_layout.addWidget(variants_group)
        
        # State demonstration group
        states_group = self._create_states_group()
        main_layout.addWidget(states_group)
        
        # Size variants group
        sizes_group = self._create_sizes_group()
        main_layout.addWidget(sizes_group)
        
        # Status label
        self.status_label = QLabel("Click any button to see status message")
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
    
    def _create_variants_group(self):
        """Create group showing all color variants."""
        group = QGroupBox("Color Variants")
        group.setStyleSheet(f"""
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
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(Theme.BUTTON_SPACING)
        
        # Create button for each variant
        variants = [
            ('yellow', 'Yellow (Primary CTA)'),
            ('green', 'Green (Selected/Active)'),
            ('blue', 'Blue (Secondary Action)'),
            ('red', 'Red (Destructive/Exciting)'),
            ('gradient', 'Gradient (Special Effect)'),
        ]
        
        for variant, label in variants:
            btn = PillButton(label, variant=variant)
            btn.clicked.connect(lambda checked, v=variant: self.on_button_clicked(v))
            layout.addWidget(btn)
        
        group.setLayout(layout)
        return group
    
    def _create_states_group(self):
        """Create group showing different button states."""
        group = QGroupBox("Button States")
        group.setStyleSheet(f"""
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
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(Theme.BUTTON_SPACING)
        
        # Normal button
        normal_btn = PillButton("Normal State", variant='yellow')
        normal_btn.clicked.connect(lambda: self.on_button_clicked('normal'))
        layout.addWidget(normal_btn)
        
        # Disabled button
        disabled_btn = PillButton("Disabled State", variant='yellow')
        disabled_btn.setEnabled(False)
        layout.addWidget(disabled_btn)
        
        group.setLayout(layout)
        return group
    
    def _create_sizes_group(self):
        """Create group showing size handling."""
        group = QGroupBox("Size Handling")
        group.setStyleSheet(f"""
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
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(Theme.BUTTON_SPACING)
        
        # Short text button
        short_btn = PillButton("OK", variant='green')
        short_btn.clicked.connect(lambda: self.on_button_clicked('short'))
        layout.addWidget(short_btn)
        
        # Long text button
        long_btn = PillButton("This Is A Much Longer Button Label", variant='blue')
        long_btn.clicked.connect(lambda: self.on_button_clicked('long'))
        layout.addWidget(long_btn)
        
        group.setLayout(layout)
        return group
    
    def on_button_clicked(self, variant):
        """Handle button click."""
        self.status_label.setText(f"[INFO] Clicked: {variant.upper()} variant button")


def main():
    """Run the demo application."""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = app.font()
    font.setFamily(Theme.FONT_FAMILY)
    app.setFont(font)
    
    demo = PillButtonDemo()
    demo.show()
    
    print("\n" + "=" * 60)
    print("[INFO] PillButton Component Demo")
    print("=" * 60)
    print("[INFO] Features demonstrated:")
    print("  - All 5 color variants (yellow, green, blue, red, gradient)")
    print("  - Touch-friendly 60px height")
    print("  - Hover and pressed state feedback")
    print("  - Disabled state styling")
    print("  - Flexible width sizing")
    print("\n[INFO] Try:")
    print("  - Hover over buttons to see highlight")
    print("  - Click and hold to see pressed state")
    print("  - Note minimum 120px width enforcement")
    print("  - Disabled button shows no interaction")
    print("\n[INFO] Press Ctrl+C or close window to exit")
    print("=" * 60 + "\n")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()