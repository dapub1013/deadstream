"""
Quick visual test of theme colors and sizes.
Useful for experimenting with theme changes.
"""
import sys
from pathlib import Path

# Add project root to Python path dynamically
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                              QPushButton, QLabel)
from src.ui.styles.theme import Theme

def main():
    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle("Theme Test")
    window.resize(600, 500)
    window.setStyleSheet(Theme.get_global_stylesheet())
    
    layout = QVBoxLayout()
    layout.setSpacing(Theme.SPACING_MEDIUM)
    layout.setContentsMargins(
        Theme.MARGIN_LARGE,
        Theme.MARGIN_LARGE,
        Theme.MARGIN_LARGE,
        Theme.MARGIN_LARGE
    )
    
    # Test all button color variants
    button_variants = [
        ("Yellow Button", Theme.ACCENT_YELLOW, Theme.TEXT_DARK),
        ("Green Button", Theme.ACCENT_GREEN, Theme.TEXT_PRIMARY),
        ("Blue Button", Theme.ACCENT_BLUE, Theme.TEXT_PRIMARY),
        ("Red Button", Theme.ACCENT_RED, Theme.TEXT_PRIMARY),
    ]
    
    for text, bg_color, text_color in button_variants:
        btn = QPushButton(text)
        btn.setStyleSheet(Theme.get_button_style(bg_color, text_color))
        layout.addWidget(btn)
    
    # Test typography sizes
    typography_tests = [
        (Theme.HEADER_LARGE, "Header Large (48px)"),
        (Theme.HEADER_MEDIUM, "Header Medium (36px)"),
        (Theme.HEADER_SMALL, "Header Small (24px)"),
        (Theme.BODY_LARGE, "Body Large (20px)"),
        (Theme.BODY_MEDIUM, "Body Medium (16px)"),
        (Theme.BODY_SMALL, "Body Small (14px)"),
    ]
    
    for size, text in typography_tests:
        label = QLabel(text)
        label.setStyleSheet(f"font-size: {size}px; color: {Theme.TEXT_PRIMARY};")
        layout.addWidget(label)
    
    window.setLayout(layout)
    window.show()
    
    print("\n[INFO] Theme Test Window Opened")
    print("[INFO] Change values in src/ui/styles/theme.py and rerun to see updates")
    print("[INFO] Press Ctrl+C or close window to exit\n")
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
