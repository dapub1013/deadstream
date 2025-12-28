#!/usr/bin/env python3
"""
Test script for search functionality (Task 7.5).
Tests SearchWidget standalone and integration with database queries.

Usage:
    python examples/test_search.py
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.ui.widgets.search_widget import SearchWidget
from src.database.queries import search_shows


class SearchTestWindow(QMainWindow):
    """Test window for search functionality"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Widget Test")
        self.setGeometry(100, 100, 800, 900)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Search Widget Test")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Search widget
        self.search_widget = SearchWidget()
        self.search_widget.search_submitted.connect(self.handle_search)
        layout.addWidget(self.search_widget)
        
        # Results label
        self.results_label = QLabel("Submit a search to see results...")
        self.results_label.setFont(QFont("Arial", 12))
        self.results_label.setStyleSheet("color: #9ca3af; padding: 20px;")
        self.results_label.setAlignment(Qt.AlignCenter)
        self.results_label.setWordWrap(True)
        layout.addWidget(self.results_label)
        
        # Test buttons
        test_layout = QVBoxLayout()
        test_layout.setSpacing(10)
        
        test_title = QLabel("Quick Tests:")
        test_title.setFont(QFont("Arial", 14, QFont.Bold))
        test_title.setStyleSheet("color: white;")
        test_layout.addWidget(test_title)
        
        # Test 1: Fillmore
        test1_btn = QPushButton("Test 1: Search 'fillmore'")
        test1_btn.clicked.connect(lambda: self.run_test_search("fillmore"))
        test1_btn.setStyleSheet(self.get_button_style())
        test_layout.addWidget(test1_btn)
        
        # Test 2: Capitol Theatre
        test2_btn = QPushButton("Test 2: Search 'capitol theatre'")
        test2_btn.clicked.connect(lambda: self.run_test_search("capitol theatre"))
        test2_btn.setStyleSheet(self.get_button_style())
        test_layout.addWidget(test2_btn)
        
        # Test 3: Year 1977
        test3_btn = QPushButton("Test 3: Search year 1977")
        test3_btn.clicked.connect(lambda: self.run_test_search(None, 1977))
        test3_btn.setStyleSheet(self.get_button_style())
        test_layout.addWidget(test3_btn)
        
        # Test 4: New York
        test4_btn = QPushButton("Test 4: Search 'new york'")
        test4_btn.clicked.connect(lambda: self.run_test_search("new york"))
        test4_btn.setStyleSheet(self.get_button_style())
        test_layout.addWidget(test4_btn)
        
        # Test 5: Complex search
        test5_btn = QPushButton("Test 5: Complex (fillmore, 1977, CA, 4.0+)")
        test5_btn.clicked.connect(self.run_complex_test)
        test5_btn.setStyleSheet(self.get_button_style())
        test_layout.addWidget(test5_btn)
        
        # Test 6: Empty results
        test6_btn = QPushButton("Test 6: Empty results (zzzzzzz)")
        test6_btn.clicked.connect(lambda: self.run_test_search("zzzzzzz"))
        test6_btn.setStyleSheet(self.get_button_style())
        test_layout.addWidget(test6_btn)
        
        layout.addLayout(test_layout)
        
        # Apply dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #111827;
            }
            QWidget {
                background-color: #111827;
            }
        """)
        
        print("[INFO] SearchTestWindow initialized")
        print("[INFO] Use the search widget above or click quick test buttons")
    
    def get_button_style(self):
        """Return button stylesheet"""
        return """
            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #6b7280;
            }
        """
    
    def handle_search(self, search_params):
        """Handle search submission from widget"""
        print("\n" + "="*60)
        print("[TEST] Search submitted from widget")
        print("="*60)
        
        # Display parameters
        print("\nSearch Parameters:")
        for key, value in search_params.items():
            if value is not None:
                print(f"  - {key}: {value}")
        
        # Execute search
        self.execute_search(search_params)
    
    def run_test_search(self, query=None, year=None, state=None, min_rating=None):
        """Run a programmatic test search"""
        print("\n" + "="*60)
        print("[TEST] Running programmatic search")
        print("="*60)
        
        search_params = {
            'query': query,
            'year': year,
            'state': state,
            'min_rating': min_rating
        }
        
        # Display parameters
        print("\nSearch Parameters:")
        for key, value in search_params.items():
            if value is not None:
                print(f"  - {key}: {value}")
        
        # Execute search
        self.execute_search(search_params)
    
    def run_complex_test(self):
        """Run complex search test"""
        self.run_test_search(
            query="fillmore",
            year=1977,
            state="CA",
            min_rating=4.0
        )
    
    def execute_search(self, search_params):
        """Execute database search and display results"""
        try:
            # Call database search function
            shows = search_shows(
                query=search_params.get('query'),
                year=search_params.get('year'),
                venue=None,  # Not using venue filter in search widget
                state=search_params.get('state'),
                min_rating=search_params.get('min_rating'),
                limit=100
            )
            
            print(f"\n[OK] Database search returned {len(shows)} results")
            
            if not shows:
                # No results
                self.results_label.setText("No shows found matching your search criteria.")
                self.results_label.setStyleSheet("color: #ef4444; padding: 20px; font-size: 14px;")
                print("[INFO] No shows matched criteria")
                return
            
            # Display first few results
            print("\nFirst 5 results:")
            for i, show in enumerate(shows[:5], 1):
                print(f"  {i}. {show['date']} - {show['venue']} ({show['city']}, {show['state']})")
                if 'avg_rating' in show and show['avg_rating']:
                    print(f"     Rating: {show['avg_rating']:.2f}")
            
            if len(shows) > 5:
                print(f"  ... and {len(shows) - 5} more")
            
            # Update results label
            result_text = f"Found {len(shows)} show(s) matching your criteria\n\n"
            result_text += "Sample results:\n"
            for show in shows[:3]:
                result_text += f"- {show['date']} at {show['venue']}\n"
            
            if len(shows) > 3:
                result_text += f"... and {len(shows) - 3} more"
            
            self.results_label.setText(result_text)
            self.results_label.setStyleSheet("color: #10b981; padding: 20px; font-size: 12px;")
            
        except Exception as e:
            print(f"\n[ERROR] Search failed: {e}")
            import traceback
            traceback.print_exc()
            
            self.results_label.setText(f"Error during search: {str(e)}")
            self.results_label.setStyleSheet("color: #ef4444; padding: 20px; font-size: 14px;")


def run_console_tests():
    """Run console-based tests without GUI"""
    print("\n" + "="*60)
    print("CONSOLE SEARCH TESTS")
    print("="*60)
    
    test_cases = [
        {
            'name': "Test 1: Simple text search",
            'params': {'query': 'fillmore'},
        },
        {
            'name': "Test 2: Year search",
            'params': {'year': 1977},
        },
        {
            'name': "Test 3: State search",
            'params': {'state': 'CA'},
        },
        {
            'name': "Test 4: Rating filter",
            'params': {'min_rating': 4.5},
        },
        {
            'name': "Test 5: Combined search",
            'params': {'query': 'capitol', 'year': 1977},
        },
        {
            'name': "Test 6: Complex search",
            'params': {'query': 'boston', 'year': 1977, 'min_rating': 4.0},
        },
        {
            'name': "Test 7: Empty results",
            'params': {'query': 'zzzzzzz'},
        },
    ]
    
    for test in test_cases:
        print(f"\n{test['name']}")
        print("-" * 60)
        print(f"Parameters: {test['params']}")
        
        try:
            shows = search_shows(
                query=test['params'].get('query'),
                year=test['params'].get('year'),
                state=test['params'].get('state'),
                min_rating=test['params'].get('min_rating'),
                limit=100
            )
            
            print(f"[OK] Found {len(shows)} show(s)")
            
            if shows:
                print("\nFirst 3 results:")
                for show in shows[:3]:
                    rating_str = ""
                    if 'avg_rating' in show and show['avg_rating']:
                        rating_str = f" (Rating: {show['avg_rating']:.2f})"
                    print(f"  - {show['date']} at {show['venue']}, {show['city']}, {show['state']}{rating_str}")
            else:
                print("  (No results)")
        
        except Exception as e:
            print(f"[ERROR] Test failed: {e}")
    
    print("\n" + "="*60)
    print("CONSOLE TESTS COMPLETE")
    print("="*60)


def main():
    """Main test function"""
    print("\n" + "="*60)
    print("SEARCH FUNCTIONALITY TEST (Task 7.5)")
    print("="*60)
    print("\nThis test validates:")
    print("  1. SearchWidget UI and interactions")
    print("  2. Database search_shows() function")
    print("  3. Various search criteria combinations")
    print("  4. Error handling")
    print("\n" + "="*60)
    
    # Ask user which test to run
    print("\nAvailable tests:")
    print("  1. GUI Test (interactive search widget)")
    print("  2. Console Test (automated test suite)")
    print("  3. Both")
    
    choice = input("\nSelect test (1/2/3): ").strip()
    
    if choice == "2":
        # Console tests only
        run_console_tests()
    
    elif choice == "3":
        # Run console tests first
        run_console_tests()
        
        # Then GUI
        print("\n\nStarting GUI test...")
        app = QApplication(sys.argv)
        window = SearchTestWindow()
        window.show()
        sys.exit(app.exec_())
    
    else:
        # GUI test (default)
        app = QApplication(sys.argv)
        window = SearchTestWindow()
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
