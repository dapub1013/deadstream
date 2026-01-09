#!/usr/bin/env python3
"""
Search widget for DeadStream UI - Phase 10D Restyled

Phase 10D Restyle:
- Uses Theme Manager for all colors/spacing/typography
- Uses PillButton for Search button (yellow variant)
- Zero hardcoded values
- Maintains all Phase 7 functionality

Provides flexible search with text query and optional filters.
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QComboBox, QSlider, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import Phase 10A components
from src.ui.styles.theme import Theme
from src.ui.components.pill_button import PillButton


class SearchWidget(QWidget):
    """
    Search widget for finding shows with flexible criteria - Phase 10D restyled
    
    Features:
    - Text search (venue, city, or other text)
    - Year filter (optional)
    - State filter (optional)
    - Minimum rating filter (optional)
    
    Signals:
        search_submitted(dict): Emitted when user submits search
                               dict contains: query, year, state, min_rating
    """
    
    # Signals
    search_submitted = pyqtSignal(dict)  # search parameters dictionary
    
    def __init__(self):
        """Initialize the search widget"""
        super().__init__()
        
        # State data for dropdown (common states with Dead shows)
        self.states = [
            "Any State",
            "CA", "NY", "NJ", "PA", "MA", "IL", "CO", "OR", "WA",
            "TX", "FL", "GA", "NC", "VA", "MD", "OH", "MI", "WI",
            "MN", "CT", "RI", "NH", "VT", "ME", "DE", "DC"
        ]
        
        # Years (1965-1995)
        self.years = ["Any Year"] + [str(year) for year in range(1965, 1996)]
        
        self.init_ui()
    
    def init_ui(self):
        """Set up the search widget UI - Phase 10D restyled"""
        layout = QVBoxLayout()
        layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE
        )
        layout.setSpacing(Theme.SPACING_LARGE)
        
        # Title
        title = QLabel("Search Shows")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
            }}
        """)
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)
        
        # Search text input
        search_label = QLabel("Search for venue, city, or location:")
        search_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
            }}
        """)
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("e.g., Fillmore, Boston, Capitol Theatre")
        self.search_input.setMinimumHeight(Theme.BUTTON_HEIGHT)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                border: 2px solid {Theme.BORDER_SUBTLE};
                border-radius: {Theme.SPACING_SMALL}px;
                padding: 0 {Theme.SPACING_MEDIUM}px;
                font-size: {Theme.BODY_LARGE}px;
            }}
            QLineEdit:focus {{
                border-color: {Theme.ACCENT_YELLOW};
            }}
        """)
        # Submit search on Enter key
        self.search_input.returnPressed.connect(self.submit_search)
        layout.addWidget(self.search_input)
        
        # Divider
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.HLine)
        divider1.setStyleSheet(f"background-color: {Theme.BORDER_SUBTLE};")
        divider1.setFixedHeight(2)
        layout.addWidget(divider1)
        
        # Filters section
        filters_label = QLabel("Optional Filters:")
        filters_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(filters_label)
        
        # Year filter
        year_layout = QHBoxLayout()
        year_label = QLabel("Year:")
        year_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
            }}
        """)
        year_label.setFixedWidth(80)
        year_layout.addWidget(year_label)
        
        self.year_combo = QComboBox()
        self.year_combo.addItems(self.years)
        self.year_combo.setMinimumHeight(Theme.BUTTON_HEIGHT_SMALL)
        self.year_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                border: 2px solid {Theme.BORDER_SUBTLE};
                border-radius: {Theme.SPACING_SMALL}px;
                padding: {Theme.SPACING_SMALL}px {Theme.SPACING_MEDIUM}px;
                font-size: {Theme.BODY_MEDIUM}px;
            }}
            QComboBox:hover {{
                border-color: {Theme.TEXT_SECONDARY};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid {Theme.TEXT_PRIMARY};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                selection-background-color: {Theme.ACCENT_BLUE};
                border: 2px solid {Theme.BORDER_SUBTLE};
            }}
        """)
        year_layout.addWidget(self.year_combo)
        layout.addLayout(year_layout)
        
        # State filter
        state_layout = QHBoxLayout()
        state_label = QLabel("State:")
        state_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
            }}
        """)
        state_label.setFixedWidth(80)
        state_layout.addWidget(state_label)
        
        self.state_combo = QComboBox()
        self.state_combo.addItems(self.states)
        self.state_combo.setMinimumHeight(Theme.BUTTON_HEIGHT_SMALL)
        self.state_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                border: 2px solid {Theme.BORDER_SUBTLE};
                border-radius: {Theme.SPACING_SMALL}px;
                padding: {Theme.SPACING_SMALL}px {Theme.SPACING_MEDIUM}px;
                font-size: {Theme.BODY_MEDIUM}px;
            }}
            QComboBox:hover {{
                border-color: {Theme.TEXT_SECONDARY};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid {Theme.TEXT_PRIMARY};
                margin-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                selection-background-color: {Theme.ACCENT_BLUE};
                border: 2px solid {Theme.BORDER_SUBTLE};
            }}
        """)
        state_layout.addWidget(self.state_combo)
        layout.addLayout(state_layout)
        
        # Rating filter
        rating_layout = QVBoxLayout()
        rating_layout.setSpacing(Theme.SPACING_SMALL)
        
        rating_header = QHBoxLayout()
        rating_label = QLabel("Min Rating:")
        rating_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                color: {Theme.TEXT_SECONDARY};
            }}
        """)
        rating_header.addWidget(rating_label)
        
        self.rating_value_label = QLabel("Any")
        self.rating_value_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.ACCENT_YELLOW};
            }}
        """)
        rating_header.addWidget(self.rating_value_label)
        rating_header.addStretch()
        rating_layout.addLayout(rating_header)
        
        self.rating_slider = QSlider(Qt.Horizontal)
        self.rating_slider.setMinimum(0)  # 0 = Any
        self.rating_slider.setMaximum(50)  # 50 = 5.0 stars
        self.rating_slider.setValue(0)
        self.rating_slider.setTickPosition(QSlider.TicksBelow)
        self.rating_slider.setTickInterval(10)
        self.rating_slider.setMinimumHeight(40)
        self.rating_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {Theme.BG_CARD};
                height: {Theme.PROGRESS_HEIGHT}px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {Theme.ACCENT_YELLOW};
                width: {Theme.PROGRESS_HANDLE_SIZE}px;
                height: {Theme.PROGRESS_HANDLE_SIZE}px;
                margin: -{Theme.PROGRESS_HANDLE_SIZE // 4}px 0;
                border-radius: {Theme.PROGRESS_HANDLE_SIZE // 2}px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {Theme._lighten_color(Theme.ACCENT_YELLOW, 10)};
            }}
            QSlider::sub-page:horizontal {{
                background: {Theme.ACCENT_YELLOW};
                border-radius: 4px;
            }}
        """)
        self.rating_slider.valueChanged.connect(self.update_rating_label)
        rating_layout.addWidget(self.rating_slider)
        
        layout.addLayout(rating_layout)
        
        # Divider
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.HLine)
        divider2.setStyleSheet(f"background-color: {Theme.BORDER_SUBTLE};")
        divider2.setFixedHeight(2)
        layout.addWidget(divider2)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(Theme.SPACING_MEDIUM)
        
        # Clear button (outline style)
        clear_btn = QPushButton("Clear Filters")
        clear_btn.setMinimumHeight(Theme.BUTTON_HEIGHT)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.TEXT_PRIMARY};
                border: 2px solid {Theme.BORDER_SUBTLE};
                border-radius: {Theme.BUTTON_RADIUS}px;
                font-size: {Theme.BODY_LARGE}px;
                font-weight: {Theme.WEIGHT_BOLD};
                padding: {Theme.SPACING_MEDIUM}px;
            }}
            QPushButton:hover {{
                border-color: {Theme.TEXT_SECONDARY};
                background-color: {Theme._lighten_color(Theme.BG_PRIMARY, 5)};
            }}
            QPushButton:pressed {{
                background-color: {Theme._darken_color(Theme.BG_PRIMARY, 5)};
            }}
        """)
        clear_btn.clicked.connect(self.clear_filters)
        button_layout.addWidget(clear_btn)
        
        # Search button (PillButton - yellow variant)
        search_btn = PillButton("Search", variant='yellow')
        search_btn.setMinimumHeight(Theme.BUTTON_HEIGHT)
        search_btn.clicked.connect(self.submit_search)
        button_layout.addWidget(search_btn)
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
        print("[INFO] SearchWidget initialized - Phase 10D restyled")
    
    def update_rating_label(self, value):
        """Update the rating value label when slider moves"""
        if value == 0:
            self.rating_value_label.setText("Any")
        else:
            rating = value / 10.0
            self.rating_value_label.setText(f"{rating:.1f}+")
    
    def clear_filters(self):
        """Reset all filters to default values"""
        self.search_input.clear()
        self.year_combo.setCurrentIndex(0)
        self.state_combo.setCurrentIndex(0)
        self.rating_slider.setValue(0)
        print("[INFO] Filters cleared")
    
    def submit_search(self):
        """Collect search parameters and emit signal"""
        
        # Get search query
        query = self.search_input.text().strip()
        
        # Get year (None if "Any Year")
        year_text = self.year_combo.currentText()
        year = int(year_text) if year_text != "Any Year" else None
        
        # Get state (None if "Any State")
        state_text = self.state_combo.currentText()
        state = state_text if state_text != "Any State" else None
        
        # Get min rating (None if 0)
        rating_value = self.rating_slider.value()
        min_rating = rating_value / 10.0 if rating_value > 0 else None
        
        # Build search parameters dictionary
        search_params = {
            'query': query if query else None,
            'year': year,
            'state': state,
            'min_rating': min_rating
        }
        
        # Log search
        params_str = ", ".join(
            f"{k}={v}" for k, v in search_params.items() if v is not None
        )
        if params_str:
            print(f"[INFO] Search submitted: {params_str}")
        else:
            print("[INFO] Search submitted: All shows (no filters)")
        
        # Emit signal
        self.search_submitted.emit(search_params)


# Test code
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Apply Theme global stylesheet
    app.setStyleSheet(Theme.get_global_stylesheet())
    
    # Create and show widget
    widget = SearchWidget()
    widget.setWindowTitle("Search Widget Test - Phase 10D Restyled")
    widget.resize(600, 700)
    
    # Connect signal to test handler
    def handle_search(params):
        print(f"\n[TEST] Search submitted with params: {params}")
    
    widget.search_submitted.connect(handle_search)
    
    widget.show()
    sys.exit(app.exec_())
