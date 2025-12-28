#!/usr/bin/env python3
"""
Search widget for DeadStream UI.
Provides flexible search with text query and optional filters.

Phase 7, Task 7.5: Implement search functionality
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


class SearchWidget(QWidget):
    """
    Search widget for finding shows with flexible criteria.
    
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
        """Set up the search widget UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Search Shows")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        # Search text input
        search_label = QLabel("Search for venue, city, or location:")
        search_label.setFont(QFont("Arial", 12))
        search_label.setStyleSheet("color: #9ca3af;")
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("e.g., Fillmore, Boston, Capitol Theatre")
        self.search_input.setMinimumHeight(60)
        self.search_input.setFont(QFont("Arial", 14))
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #1f2937;
                color: white;
                border: 2px solid #374151;
                border-radius: 8px;
                padding: 0 16px;
            }
            QLineEdit:focus {
                border-color: #f59e0b;
            }
        """)
        # Submit search on Enter key
        self.search_input.returnPressed.connect(self.submit_search)
        layout.addWidget(self.search_input)
        
        # Divider
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.HLine)
        divider1.setStyleSheet("background-color: #374151;")
        divider1.setFixedHeight(2)
        layout.addWidget(divider1)
        
        # Filters section
        filters_label = QLabel("Optional Filters:")
        filters_label.setFont(QFont("Arial", 14, QFont.Bold))
        filters_label.setStyleSheet("color: white;")
        layout.addWidget(filters_label)
        
        # Year filter
        year_layout = QHBoxLayout()
        year_label = QLabel("Year:")
        year_label.setFont(QFont("Arial", 12))
        year_label.setStyleSheet("color: #9ca3af;")
        year_label.setFixedWidth(80)
        year_layout.addWidget(year_label)
        
        self.year_combo = QComboBox()
        self.year_combo.addItems(self.years)
        self.year_combo.setMinimumHeight(50)
        self.year_combo.setFont(QFont("Arial", 13))
        self.year_combo.setStyleSheet("""
            QComboBox {
                background-color: #1f2937;
                color: white;
                border: 2px solid #374151;
                border-radius: 8px;
                padding: 8px 12px;
            }
            QComboBox:hover {
                border-color: #4b5563;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid white;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #1f2937;
                color: white;
                selection-background-color: #374151;
                border: 2px solid #374151;
            }
        """)
        year_layout.addWidget(self.year_combo)
        layout.addLayout(year_layout)
        
        # State filter
        state_layout = QHBoxLayout()
        state_label = QLabel("State:")
        state_label.setFont(QFont("Arial", 12))
        state_label.setStyleSheet("color: #9ca3af;")
        state_label.setFixedWidth(80)
        state_layout.addWidget(state_label)
        
        self.state_combo = QComboBox()
        self.state_combo.addItems(self.states)
        self.state_combo.setMinimumHeight(50)
        self.state_combo.setFont(QFont("Arial", 13))
        self.state_combo.setStyleSheet("""
            QComboBox {
                background-color: #1f2937;
                color: white;
                border: 2px solid #374151;
                border-radius: 8px;
                padding: 8px 12px;
            }
            QComboBox:hover {
                border-color: #4b5563;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid white;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #1f2937;
                color: white;
                selection-background-color: #374151;
                border: 2px solid #374151;
            }
        """)
        state_layout.addWidget(self.state_combo)
        layout.addLayout(state_layout)
        
        # Rating filter
        rating_layout = QVBoxLayout()
        rating_layout.setSpacing(8)
        
        rating_header = QHBoxLayout()
        rating_label = QLabel("Min Rating:")
        rating_label.setFont(QFont("Arial", 12))
        rating_label.setStyleSheet("color: #9ca3af;")
        rating_header.addWidget(rating_label)
        
        self.rating_value_label = QLabel("Any")
        self.rating_value_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.rating_value_label.setStyleSheet("color: #f59e0b;")
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
        self.rating_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #374151;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #f59e0b;
                width: 24px;
                height: 24px;
                margin: -8px 0;
                border-radius: 12px;
            }
            QSlider::handle:horizontal:hover {
                background: #d97706;
            }
            QSlider::sub-page:horizontal {
                background: #f59e0b;
                border-radius: 4px;
            }
        """)
        self.rating_slider.valueChanged.connect(self.update_rating_label)
        rating_layout.addWidget(self.rating_slider)
        
        layout.addLayout(rating_layout)
        
        # Divider
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.HLine)
        divider2.setStyleSheet("background-color: #374151;")
        divider2.setFixedHeight(2)
        layout.addWidget(divider2)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Clear button
        clear_btn = QPushButton("Clear Filters")
        clear_btn.setMinimumHeight(60)
        clear_btn.setFont(QFont("Arial", 14))
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #6b7280;
            }
        """)
        clear_btn.clicked.connect(self.clear_filters)
        button_layout.addWidget(clear_btn)
        
        # Search button
        search_btn = QPushButton("Search")
        search_btn.setMinimumHeight(60)
        search_btn.setFont(QFont("Arial", 14, QFont.Bold))
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #d97706;
            }
            QPushButton:pressed {
                background-color: #b45309;
            }
        """)
        search_btn.clicked.connect(self.submit_search)
        button_layout.addWidget(search_btn)
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
        print("[INFO] SearchWidget initialized")
    
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
    
    # Create and show widget
    widget = SearchWidget()
    widget.setStyleSheet("background-color: #111827;")
    widget.setWindowTitle("Search Widget Test")
    widget.resize(600, 700)
    
    # Connect signal to test handler
    def handle_search(params):
        print(f"\n[TEST] Search submitted with params: {params}")
    
    widget.search_submitted.connect(handle_search)
    
    widget.show()
    sys.exit(app.exec_())
