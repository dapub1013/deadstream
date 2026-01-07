"""
Test script for badge components (RatingBadge and SourceBadge).

Displays various ratings and source types:
- Rating badges with different values
- Source badges for all types (SBD, AUD, MTX, FLAC, MP3)
- Combined badge displays (as used in concert lists)
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
from src.ui.components.rating_badge import RatingBadge
from src.ui.components.source_badge import SourceBadge


class BadgeDemo(QWidget):
    """Demo window showing all badge components."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("Badge Components Test")
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
        title = QLabel("Badge Components Demo")
        title.setStyleSheet(f"""
            font-size: {Theme.HEADER_MEDIUM}px;
            font-weight: {Theme.WEIGHT_BOLD};
            color: {Theme.TEXT_PRIMARY};
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Compact badges for ratings and source types")
        subtitle.setStyleSheet(f"""
            font-size: {Theme.BODY_LARGE}px;
            color: {Theme.TEXT_SECONDARY};
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        
        # Rating badges group
        ratings_group = self._create_ratings_group()
        main_layout.addWidget(ratings_group)
        
        # Source badges group
        sources_group = self._create_sources_group()
        main_layout.addWidget(sources_group)
        
        # Combined badges group
        combined_group = self._create_combined_group()
        main_layout.addWidget(combined_group)
        
        # Concert list simulation
        concert_list = self._create_concert_list()
        main_layout.addWidget(concert_list)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def _create_ratings_group(self):
        """Create group showing rating badges."""
        group = QGroupBox("Rating Badges")
        group.setStyleSheet(self._get_group_style())
        
        layout = QHBoxLayout()
        layout.setSpacing(Theme.SPACING_MEDIUM)
        
        # Various rating values
        ratings = [5.0, 4.8, 4.5, 4.0, 3.5, 3.0]
        
        for rating in ratings:
            container = QVBoxLayout()
            container.setSpacing(Theme.SPACING_SMALL)
            
            badge = RatingBadge(rating)
            
            label = QLabel(f"{rating:.1f} stars")
            label.setStyleSheet(f"""
                font-size: {Theme.BODY_SMALL}px;
                color: {Theme.TEXT_SECONDARY};
            """)
            label.setAlignment(Qt.AlignCenter)
            
            container.addWidget(badge, alignment=Qt.AlignCenter)
            container.addWidget(label)
            
            layout.addLayout(container)
        
        group.setLayout(layout)
        return group
    
    def _create_sources_group(self):
        """Create group showing source badges."""
        group = QGroupBox("Source Type Badges")
        group.setStyleSheet(self._get_group_style())
        
        layout = QHBoxLayout()
        layout.setSpacing(Theme.SPACING_MEDIUM)
        
        # All source types
        sources = [
            ('SBD', 'Soundboard'),
            ('AUD', 'Audience'),
            ('MTX', 'Matrix'),
            ('FLAC', 'FLAC Format'),
            ('MP3', 'MP3 Format'),
        ]
        
        for source_type, description in sources:
            container = QVBoxLayout()
            container.setSpacing(Theme.SPACING_SMALL)
            
            badge = SourceBadge(source_type)
            
            label = QLabel(description)
            label.setStyleSheet(f"""
                font-size: {Theme.BODY_SMALL}px;
                color: {Theme.TEXT_SECONDARY};
            """)
            label.setAlignment(Qt.AlignCenter)
            
            container.addWidget(badge, alignment=Qt.AlignCenter)
            container.addWidget(label)
            
            layout.addLayout(container)
        
        group.setLayout(layout)
        return group
    
    def _create_combined_group(self):
        """Create group showing combined badge usage."""
        group = QGroupBox("Combined Badge Display")
        group.setStyleSheet(self._get_group_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_MEDIUM)
        
        # Example combinations as they appear in concert lists
        combinations = [
            (4.8, 'SBD', 'Premium soundboard recording'),
            (4.5, 'AUD', 'High-quality audience recording'),
            (4.2, 'MTX', 'Matrix blend of multiple sources'),
        ]
        
        for rating, source, description in combinations:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(Theme.SPACING_MEDIUM)
            
            # Description
            desc_label = QLabel(description)
            desc_label.setStyleSheet(f"""
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_PRIMARY};
            """)
            row_layout.addWidget(desc_label)
            
            row_layout.addStretch()
            
            # Source badge
            source_badge = SourceBadge(source)
            row_layout.addWidget(source_badge)
            
            # Rating badge
            rating_badge = RatingBadge(rating)
            row_layout.addWidget(rating_badge)
            
            layout.addLayout(row_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_concert_list(self):
        """Create simulated concert list with badges."""
        group = QGroupBox("Concert List Example")
        group.setStyleSheet(self._get_group_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_SMALL)
        
        # Simulated concert entries
        concerts = [
            ('1977-05-08', 'Barton Hall, Cornell University', 4.8, 'SBD'),
            ('1972-05-11', 'Olympia Theatre, Paris', 4.5, 'AUD'),
            ('1974-05-19', 'Portland Memorial Coliseum', 4.3, 'MTX'),
            ('1973-11-10', 'Winterland Arena', 4.7, 'SBD'),
        ]
        
        for date, venue, rating, source in concerts:
            concert_layout = QHBoxLayout()
            concert_layout.setSpacing(Theme.SPACING_MEDIUM)
            
            # Concert info
            info_layout = QVBoxLayout()
            info_layout.setSpacing(2)
            
            date_label = QLabel(date)
            date_label.setStyleSheet(f"""
                font-size: {Theme.BODY_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
            """)
            info_layout.addWidget(date_label)
            
            venue_label = QLabel(venue)
            venue_label.setStyleSheet(f"""
                font-size: {Theme.BODY_SMALL}px;
                color: {Theme.TEXT_SECONDARY};
            """)
            info_layout.addWidget(venue_label)
            
            concert_layout.addLayout(info_layout, stretch=1)
            
            # Badges
            source_badge = SourceBadge(source)
            concert_layout.addWidget(source_badge)
            
            rating_badge = RatingBadge(rating)
            concert_layout.addWidget(rating_badge)
            
            # Add to main layout with separator
            layout.addLayout(concert_layout)
            
            # Separator line
            if concert != concerts[-1]:  # Don't add after last item
                separator = QLabel()
                separator.setStyleSheet(f"""
                    background-color: {Theme.BORDER_SUBTLE};
                    max-height: 1px;
                """)
                separator.setFixedHeight(1)
                layout.addWidget(separator)
        
        group.setLayout(layout)
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


def main():
    """Run the demo application."""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = app.font()
    font.setFamily(Theme.FONT_FAMILY)
    app.setFont(font)
    
    demo = BadgeDemo()
    demo.show()
    
    print("\n" + "=" * 60)
    print("[INFO] Badge Components Demo")
    print("=" * 60)
    print("[INFO] Components demonstrated:")
    print("  - RatingBadge: Star ratings (cyan background)")
    print("  - SourceBadge: Recording sources (color-coded)")
    print("\n[INFO] Badge types:")
    print("  - Rating: 0.0-5.0 stars with single star emoji")
    print("  - Source: SBD (gold), AUD (blue), MTX (green)")
    print("  - Format: FLAC (purple), MP3 (orange)")
    print("\n[INFO] Features:")
    print("  - Compact 80px × 28px size")
    print("  - Rounded 14px corners")
    print("  - Color-coded by type")
    print("  - Ready for concert list integration")
    print("\n[INFO] Use cases:")
    print("  - Concert list items (rating + source)")
    print("  - Player screen (show metadata)")
    print("  - Browse screen (quality indicators)")
    print("\n[INFO] Press Ctrl+C or close window to exit")
    print("=" * 60 + "\n")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()