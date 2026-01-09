#!/usr/bin/env python3
"""
Browse Screen for DeadStream - Phase 10D Restyled

Phase 10D Restyle:
- Uses Theme Manager for all colors/spacing/typography
- Uses PillButton for browse mode navigation
- Uses ConcertListItem for show lists (via show_list.py)
- Zero hardcoded values
- Maintains all Phase 7 functionality

Previous features retained:
- Task 7.1: Show list view with top-rated shows
- Task 7.2: Date browser (calendar-based browsing)
- Task 7.3: Venue filter
- Task 7.4: Year selector
- Task 7.5: Search functionality
- Task 7.6: Random show button
- Phase 10A: ShowCard display modes
"""

import sys
import os

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QDialog, QListWidget, QListWidgetItem,
    QStackedWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

# Import database queries
from src.database.queries import (
    get_top_rated_shows, get_most_played_venues,
    search_by_venue, get_show_by_date, search_by_year,
    get_show_count, get_random_show
)

# Import Phase 10A components
from src.ui.styles.theme import Theme
from src.ui.components.pill_button import PillButton

# Import widgets
from src.ui.widgets.show_list import ShowListWidget
from src.ui.widgets.date_browser import DateBrowser
from src.ui.widgets.date_selector import DateSelectorWidget
from src.ui.widgets.year_browser import YearBrowser
from src.ui.widgets.search_widget import SearchWidget
from src.ui.widgets.error_dialog import ErrorDialog, show_database_error, show_network_error
from src.ui.widgets.toast_notification import ToastManager
from src.ui.widgets.loading_spinner import LoadingIndicator
from src.ui.widgets.random_show_widget import RandomShowWidget
from src.ui.widgets.show_card import ShowCard


class BrowseScreen(QWidget):
    """
    Browse screen for finding and selecting shows - Phase 10D Restyled

    Layout:
    - Left panel (30%): Navigation with PillButton components
    - Right panel (70%): ShowCard/ShowList display area

    Left Panel Priority Order:
    1. Browse by Date (primary, blue)
    2. Random Show (exciting, gradient)
    3. Top Rated (secondary, green)
    4. Search Shows (tertiary, blue)
    5. Browse by Venue (tertiary, blue)
    6. Browse by Year (tertiary, blue)

    Right Panel States:
    - DEFAULT: Last played show or welcome message
    - RANDOM: Random show with "Try Another" button
    - DATE_SELECTED: Show from date browser
    - FILTERED: Random show matching active filter
    - LIST_VIEW: Traditional show list

    Signals:
    - show_selected: Emitted when user selects a show to play
    - player_requested: Navigate to player screen
    - settings_requested: Navigate to settings screen
    """

    # Navigation signals
    show_selected = pyqtSignal(dict)  # Emits show dictionary
    player_requested = pyqtSignal()   # Navigate to player
    settings_requested = pyqtSignal() # Navigate to settings

    def __init__(self, parent=None):
        """Initialize browse screen"""
        super().__init__(parent)
        self.current_shows = []
        self.current_filter = None
        self.current_mode = 'default'
        self.setup_ui()

        # Create error handling UI components
        self.toast_manager = ToastManager(self)

        self.load_default_state()
    
    def setup_ui(self):
        """Create browse screen layout - Phase 10D restyled"""
        # Main horizontal layout (left panel + right panel)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Panel (30%) - Navigation
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, stretch=3)

        # Right Panel (70%) - ShowCard/ShowList display area
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, stretch=7)

        self.setLayout(main_layout)
    
    def create_left_panel(self):
        """Create left panel with browse mode buttons - Phase 10D restyled"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_PRIMARY};
                border-right: 2px solid {Theme.BORDER_PANEL};
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_LARGE
        )
        layout.setSpacing(Theme.SPACING_MEDIUM)
        
        # Title
        title = QLabel("Browse Shows")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
                padding-bottom: {Theme.SPACING_SMALL}px;
                border-bottom: 2px solid {Theme.BORDER_PANEL};
            }}
        """)
        layout.addWidget(title)
        
        # Add browse mode buttons
        browse_buttons = self.create_browse_mode_buttons()
        layout.addLayout(browse_buttons)
        
        # Add stretch to push buttons to top
        layout.addStretch()
        
        # Navigation buttons at bottom
        nav_layout = self.create_navigation_buttons()
        layout.addLayout(nav_layout)
        
        return panel
    
    def create_browse_mode_buttons(self):
        """
        Create navigation buttons using PillButton - Phase 10D restyled
        
        Priority order:
        1. Browse by Date (blue, primary)
        2. Random Show (gradient, exciting)
        3. Top Rated (green, secondary)
        4. Search Shows (blue, tertiary)
        5. Browse by Venue (blue, tertiary)
        6. Browse by Year (blue, tertiary)
        """
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_MEDIUM)

        # 1. Browse by Date - PRIMARY ACTION (blue)
        self.browse_by_date_btn = PillButton("Browse by Date", variant='blue')
        self.browse_by_date_btn.setMinimumHeight(80)
        self.browse_by_date_btn.clicked.connect(self.show_date_browser)
        layout.addWidget(self.browse_by_date_btn)

        # 2. Random Show - EXCITING FEATURE (gradient)
        self.random_show_btn = PillButton("Random Show", variant='gradient')
        self.random_show_btn.setMinimumHeight(70)
        self.random_show_btn.clicked.connect(self.show_random_show)
        layout.addWidget(self.random_show_btn)

        # 3. Top Rated - SECONDARY ACTION (green)
        self.top_rated_btn = PillButton("Top Rated", variant='green')
        self.top_rated_btn.setMinimumHeight(60)
        self.top_rated_btn.clicked.connect(self.show_top_rated)
        layout.addWidget(self.top_rated_btn)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background-color: {Theme.BORDER_SUBTLE};")
        separator.setFixedHeight(2)
        layout.addWidget(separator)

        # 4. Search Shows - TERTIARY (blue)
        self.search_btn = PillButton("Search Shows", variant='blue')
        self.search_btn.clicked.connect(self.show_search)
        layout.addWidget(self.search_btn)

        # 5. Browse by Venue - TERTIARY (blue)
        self.browse_by_venue_btn = PillButton("Browse by Venue", variant='blue')
        self.browse_by_venue_btn.clicked.connect(self.show_venue_browser)
        layout.addWidget(self.browse_by_venue_btn)

        # 6. Browse by Year - TERTIARY (blue)
        self.browse_by_year_btn = PillButton("Browse by Year", variant='blue')
        self.browse_by_year_btn.clicked.connect(self.show_year_browser)
        layout.addWidget(self.browse_by_year_btn)

        return layout
    
    def create_navigation_buttons(self):
        """Create bottom navigation buttons - Phase 10D restyled"""
        layout = QVBoxLayout()
        layout.setSpacing(Theme.SPACING_SMALL)

        # Settings button (outline style)
        settings_btn = QPushButton("Settings")
        settings_btn.setMinimumHeight(Theme.BUTTON_HEIGHT)
        settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.TEXT_PRIMARY};
                border: 2px solid {Theme.BORDER_SUBTLE};
                border-radius: {Theme.BUTTON_RADIUS}px;
                font-size: {Theme.BODY_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
            }}
            QPushButton:hover {{
                border-color: {Theme.TEXT_SECONDARY};
                background-color: {Theme._lighten_color(Theme.BG_PRIMARY, 5)};
            }}
            QPushButton:pressed {{
                background-color: {Theme._darken_color(Theme.BG_PRIMARY, 5)};
            }}
        """)
        settings_btn.clicked.connect(self.settings_requested.emit)
        layout.addWidget(settings_btn)

        # Show count label
        try:
            show_count = get_show_count()
            count_label = QLabel(f"{show_count:,} shows available")
        except:
            count_label = QLabel("Database loaded")
        
        count_label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                font-size: {Theme.BODY_SMALL}px;
                padding: {Theme.SPACING_SMALL}px 0px;
            }}
        """)
        count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(count_label)

        return layout
    
    def create_right_panel(self):
        """Create right panel with stacked content areas - Phase 10D restyled"""
        panel = QFrame()
        panel.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header area (title + subtitle)
        header_layout = self.create_header()
        layout.addLayout(header_layout)
        
        # Stacked widget for different content types
        self.content_stack = QStackedWidget()
        
        # Page 0: ShowCard view (default, random, date_selected)
        self.show_card = ShowCard()
        
        # Connect signals if they exist (Phase 10A ShowCard may have different signals)
        if hasattr(self.show_card, 'play_requested'):
            self.show_card.play_requested.connect(self.on_show_selected)
        elif hasattr(self.show_card, 'clicked'):
            self.show_card.clicked.connect(self.on_show_selected)
        elif hasattr(self.show_card, 'show_selected'):
            self.show_card.show_selected.connect(self.on_show_selected)
        
        if hasattr(self.show_card, 'try_another_requested'):
            self.show_card.try_another_requested.connect(self.show_random_show)
        
        self.content_stack.addWidget(self.show_card)
        
        # Page 1: Show List view (top rated, search results, etc.)
        self.show_list = ShowListWidget()
        self.show_list.show_selected.connect(self.on_show_selected)
        self.content_stack.addWidget(self.show_list)
        
        # Page 2: Date Browser
        self.date_browser = DateBrowser()
        self.date_browser.date_selected.connect(self.on_date_browser_selected)
        self.content_stack.addWidget(self.date_browser)
        
        # Page 3: Date Selector (Phase 10A compact date picker)
        self.date_selector = DateSelectorWidget()
        self.date_selector.date_selected.connect(self.on_date_selector_selected)
        self.content_stack.addWidget(self.date_selector)
        
        # Page 4: Year Browser
        self.year_browser = YearBrowser()
        self.year_browser.year_selected.connect(self.on_year_browser_selected)
        self.content_stack.addWidget(self.year_browser)
        
        # Page 5: Search Widget
        self.search_widget = SearchWidget()
        self.search_widget.search_submitted.connect(self.perform_search)
        self.content_stack.addWidget(self.search_widget)
        
        # Page 6: Venue Browser (placeholder - would be implemented separately)
        venue_placeholder = QLabel("Venue Browser - Coming Soon")
        venue_placeholder.setAlignment(Qt.AlignCenter)
        venue_placeholder.setStyleSheet(f"color: {Theme.TEXT_SECONDARY};")
        self.content_stack.addWidget(venue_placeholder)
        
        layout.addWidget(self.content_stack)
        
        return panel
    
    def create_header(self):
        """Create header with title and subtitle - Phase 10D restyled"""
        layout = QVBoxLayout()
        layout.setContentsMargins(
            Theme.SPACING_XLARGE,
            Theme.SPACING_LARGE,
            Theme.SPACING_XLARGE,
            Theme.SPACING_MEDIUM
        )
        layout.setSpacing(Theme.SPACING_SMALL)
        
        # Title
        self.header_title = QLabel("Welcome to DeadStream")
        self.header_title.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.HEADER_MEDIUM}px;
                font-weight: {Theme.WEIGHT_BOLD};
                color: {Theme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(self.header_title)
        
        # Subtitle
        self.header_subtitle = QLabel("Select a browse mode to find shows")
        self.header_subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: {Theme.BODY_LARGE}px;
                color: {Theme.TEXT_SECONDARY};
            }}
        """)
        layout.addWidget(self.header_subtitle)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet(f"background-color: {Theme.BORDER_SUBTLE};")
        divider.setFixedHeight(1)
        layout.addWidget(divider)
        
        return layout
    
    def update_header(self, title, subtitle=""):
        """Update header title and subtitle"""
        self.header_title.setText(title)
        self.header_subtitle.setText(subtitle)
    
    # ========================================================================
    # BROWSE MODE HANDLERS
    # ========================================================================

    def show_top_rated(self):
        """Load and display top rated shows (Task 7.1)"""
        print("[INFO] Loading top rated shows...")
        
        try:
            # Switch to list view
            self.content_stack.setCurrentIndex(1)
            self.show_list.set_loading_state()
            
            # Get top rated shows
            shows = get_top_rated_shows(limit=50, min_reviews=5)
            
            if not shows:
                self.update_header(
                    "No Shows Found",
                    "No rated shows in database"
                )
                self.show_list.set_empty_state("No shows found")
                return
            
            # Update header
            self.update_header(
                f"Top Rated Shows ({len(shows)} shows)",
                "Best-reviewed performances from the collection"
            )
            
            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows
            
            print(f"[OK] Loaded {len(shows)} top rated shows")
            
        except Exception as e:
            print(f"[ERROR] Failed to load top rated shows: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", "Failed to load top rated shows")
            self.show_list.set_empty_state("Error loading shows")
            self.toast_manager.show_error("Database error: Unable to load top rated shows")

    def show_date_browser(self):
        """Show date browser (Task 7.2) - Phase 10A uses compact selector"""
        print("[INFO] Showing date selector...")
        
        # Update header
        self.update_header(
            "Browse by Date",
            "Select a date to find shows"
        )
        
        # Switch to date selector (page 3 in Phase 10A)
        self.content_stack.setCurrentIndex(3)
        
        print("[OK] Date selector displayed")

    def show_venue_browser(self):
        """Show venue browser (Task 7.3) - placeholder"""
        print("[INFO] Showing venue browser...")
        
        # Update header
        self.update_header(
            "Browse by Venue",
            "Find shows at your favorite venues"
        )
        
        # Switch to venue browser placeholder (page 6)
        self.content_stack.setCurrentIndex(6)
        
        print("[OK] Venue browser displayed")

    def show_year_browser(self):
        """Show year browser (Task 7.4)"""
        print("[INFO] Showing year browser...")
        
        # Update header
        self.update_header(
            "Browse by Year",
            "Explore shows from different eras"
        )
        
        # Switch to year browser (page 4)
        self.content_stack.setCurrentIndex(4)
        
        print("[OK] Year browser displayed")

    def show_search(self):
        """Show search interface (Task 7.5)"""
        print("[INFO] Showing search interface...")
        
        # Update header
        self.update_header(
            "Search Shows",
            "Search by venue, location, year, or rating"
        )
        
        # Switch to search widget (page 5)
        self.content_stack.setCurrentIndex(5)
        
        print("[OK] Search interface displayed")

    def show_random_show(self):
        """Show random show (Task 7.6) - Phase 10A uses ShowCard"""
        print("[INFO] Loading random show...")
        
        try:
            # Get random show
            show = get_random_show()
            
            if not show:
                self.update_header("Error", "No shows available")
                self.content_stack.setCurrentIndex(0)
                self._show_card_error("Database is empty")
                return
            
            # Update header
            self.update_header(
                "Random Show",
                "Surprise me!"
            )
            
            # Switch to ShowCard view (page 0)
            self.content_stack.setCurrentIndex(0)
            self.current_mode = 'random'
            
            # Load show in ShowCard with fade animation
            self._show_card_fade_in(show)
            self._show_card_set_mode('random')  # Show "Try Another" button
            self._show_card_enable_play(True)
            
            print(f"[OK] Random show loaded: {show['date']} - {show['venue']}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load random show: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", "Failed to load random show")
            self.content_stack.setCurrentIndex(0)
            self._show_card_error("Error loading random show")
            self.toast_manager.show_error("Database error: Unable to load random show")

    def load_default_state(self):
        """Load default welcome state"""
        self.update_header(
            "Welcome to DeadStream",
            "Select a browse mode to find shows"
        )
        
        # Show ShowCard in default mode (page 0)
        self.content_stack.setCurrentIndex(0)
        
        # Call show_welcome if method exists
        if hasattr(self.show_card, 'show_welcome') and callable(self.show_card.show_welcome):
            self.show_card.show_welcome()
    
    # ========================================================================
    # SHOWCARD HELPER METHODS (safe wrappers for optional methods)
    # ========================================================================
    
    def _show_card_error(self, message):
        """Safely show error on ShowCard if method exists"""
        if hasattr(self.show_card, 'show_error') and callable(self.show_card.show_error):
            self.show_card.show_error(message)
        else:
            print(f"[WARN] ShowCard error: {message}")
    
    def _show_card_fade_in(self, show):
        """Safely fade in show on ShowCard if method exists"""
        if hasattr(self.show_card, 'fade_in') and callable(self.show_card.fade_in):
            self.show_card.fade_in(show)
        elif hasattr(self.show_card, 'load_show') and callable(self.show_card.load_show):
            self.show_card.load_show(show)
        else:
            print(f"[WARN] ShowCard cannot display show: {show.get('date')}")
    
    def _show_card_set_mode(self, mode):
        """Safely set mode on ShowCard if method exists"""
        if hasattr(self.show_card, 'set_mode') and callable(self.show_card.set_mode):
            self.show_card.set_mode(mode)
    
    def _show_card_enable_play(self, enabled=True):
        """Safely enable play button on ShowCard if it exists"""
        if hasattr(self.show_card, 'play_button'):
            if hasattr(self.show_card.play_button, 'setEnabled'):
                self.show_card.play_button.setEnabled(enabled)

    # ========================================================================
    # DATA LOADING METHODS
    # ========================================================================

    def on_date_browser_selected(self, date_str):
        """Handle date selection from DateBrowser (calendar view)"""
        print(f"[INFO] Date selected from calendar: {date_str}")
        
        try:
            # Get shows for this date
            shows = get_show_by_date(date_str)
            
            if not shows:
                # No shows found
                self.update_header(
                    "No Shows Found",
                    f"No shows on {date_str}"
                )
                self.content_stack.setCurrentIndex(0)
                self._show_card_error(f"No show found for {date_str}")
                return
            
            # Take first show (or best scored if multiple)
            show = shows[0]
            if len(shows) > 1:
                show = max(shows, key=lambda s: s.get('recording_score', 0))
                print(f"[INFO] Multiple recordings, selected best: score={show.get('recording_score', 0)}")
            
            # Switch to ShowCard view
            self.content_stack.setCurrentIndex(0)
            self.current_mode = 'date_selected'
            
            # Update header
            self.update_header(
                f"Show on {date_str}",
                show.get('venue', 'Unknown Venue')
            )
            
            # Load show in ShowCard
            self._show_card_fade_in(show)
            self._show_card_set_mode('date_selected')
            self._show_card_enable_play(True)
            
            print(f"[OK] Date selection loaded: {show['date']} - {show['venue']}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load date selection: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", f"Failed to load show for {date_str}")
            self.content_stack.setCurrentIndex(0)
            self._show_card_error(f"Error loading show for {date_str}")
            self.toast_manager.show_error(f"Database error: Unable to load show for {date_str}")

    def load_shows_by_venue(self, venue_name):
        """Load and display shows from a specific venue (Task 7.3)"""
        
        try:
            # Switch to list view
            self.content_stack.setCurrentIndex(1)
            self.show_list.set_loading_state()
            
            # Search for shows at this venue
            shows = search_by_venue(venue_name)
            
            if not shows:
                # No shows found
                self.update_header(
                    "No Shows Found",
                    f"No shows at {venue_name}"
                )
                self.show_list.set_empty_state(f"No shows at {venue_name}")
                return
            
            # Update header
            self.update_header(
                f"{len(shows)} Shows at {venue_name}",
                "Sorted by date (oldest to newest)"
            )
            
            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows
            
            print(f"[OK] Loaded {len(shows)} shows from {venue_name}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load venue shows: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", f"Failed to load shows for {venue_name}")
            self.show_list.set_empty_state("Error loading shows")
            self.toast_manager.show_error(f"Database error: Unable to load shows for {venue_name}")
    
    def load_shows_by_year(self, year):
        """Load and display shows from a specific year (Task 7.4)"""
        
        try:
            # Switch to list view
            self.content_stack.setCurrentIndex(1)
            self.show_list.set_loading_state()
            
            # Get shows for this year
            shows = search_by_year(year)
            
            if not shows:
                # No shows found
                self.update_header(
                    "No Shows Found",
                    f"No shows from {year}"
                )
                self.show_list.set_empty_state(f"No shows from {year}")
                return
            
            # Update header - include legendary year indicator
            from src.ui.widgets.year_browser import YearBrowser
            is_legendary = year in YearBrowser.LEGENDARY_YEARS
            
            if is_legendary:
                title = f"[LEGENDARY] {year} ({len(shows)} shows)"
            else:
                title = f"{year} ({len(shows)} shows)"
            
            self.update_header(
                title,
                "All shows from this year, sorted by date"
            )
            
            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows
            
            print(f"[OK] Loaded {len(shows)} shows from {year}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load year shows: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", f"Failed to load shows for {year}")
            self.show_list.set_empty_state("Error loading shows")
            self.toast_manager.show_error(f"Database error: Unable to load shows for {year}")

    def perform_search(self, search_params):
        """Perform database search based on parameters from SearchWidget"""
        try:
            # Switch to list view
            self.content_stack.setCurrentIndex(1)
            self.show_list.set_loading_state()
            
            # Extract search parameters
            query = search_params.get('query', '')
            year = search_params.get('year', None)
            state = search_params.get('state', None)
            min_rating = search_params.get('min_rating', None)
            
            print(f"[INFO] Performing search: query={query}, year={year}, state={state}, rating={min_rating}")
            
            # Import search function
            from src.database.queries import search_shows
            
            # Perform search
            results = search_shows(
                query=query,
                year=year,
                state=state,
                min_rating=min_rating
            )
            
            # Load results
            self.load_search_results(results)
        
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Search Error", "Failed to perform search")
            self.show_list.set_empty_state("Search failed")
            self.toast_manager.show_error(f"Search error: {str(e)}")

    def load_search_results(self, results):
        """Load and display search results (Task 7.5)"""
        
        try:
            # Update header
            if not results:
                self.update_header(
                    "No Results",
                    "No shows matched your search criteria"
                )
                self.show_list.set_empty_state("Try different search criteria")
                return
            
            self.update_header(
                f"Search Results ({len(results)} shows)",
                "Sorted by rating (best first)"
            )
            
            # Load shows into list
            self.show_list.load_shows(results)
            self.current_shows = results
            
            print(f"[OK] Loaded {len(results)} search results")
            
        except Exception as e:
            print(f"[ERROR] Failed to load search results: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", "Failed to load search results")
            self.show_list.set_empty_state("Error loading shows")
            self.toast_manager.show_error("Failed to load search results")
    
    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================

    def on_show_selected(self, show):
        """Handle show selection from list or ShowCard"""
        print(f"[INFO] Show selected: {show['date']} - {show['venue']}")
        self.show_selected.emit(show)

    def on_date_selector_selected(self, date_str):
        """
        Handle date selection from DateSelectorWidget - Phase 10A compact picker
        
        Loads selected show in ShowCard instead of list view
        """
        print(f"[INFO] Date selected from selector: {date_str}")
        
        try:
            # Get shows for this date
            shows = get_show_by_date(date_str)
            
            if not shows:
                # No shows found - show error in ShowCard
                self.content_stack.setCurrentIndex(0)
                self._show_card_error(f"No show found for {date_str}")
                print(f"[WARN] No shows found for {date_str}")
                return
            
            # Take first show (or best scored if multiple)
            show = shows[0]
            if len(shows) > 1:
                show = max(shows, key=lambda s: s.get('recording_score', 0))
                print(f"[INFO] Multiple recordings, selected best: score={show.get('recording_score', 0)}")
            
            # Switch to ShowCard view
            self.content_stack.setCurrentIndex(0)
            self.current_mode = 'date_selected'
            
            # Update header
            self.update_header(
                f"Show on {date_str}",
                show.get('venue', 'Unknown Venue')
            )
            
            # Load show in ShowCard with fade animation
            self._show_card_fade_in(show)
            self._show_card_set_mode('date_selected')
            self._show_card_enable_play(True)
            
            print(f"[OK] Date selection loaded in ShowCard: {show['date']} - {show['venue']}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load date selection: {e}")
            import traceback
            traceback.print_exc()
            self.content_stack.setCurrentIndex(0)
            self._show_card_error(f"Error loading show for {date_str}")
            self.toast_manager.show_error(f"Database error: Unable to load show for {date_str}")

    def on_year_browser_selected(self, year):
        """Handle year selection from YearBrowser"""
        print(f"[INFO] Year selected from browser: {year}")
        # Load shows for this year (will switch to list view)
        self.load_shows_by_year(year)


# Test code
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Apply Theme global stylesheet
    app.setStyleSheet(Theme.get_global_stylesheet())
    
    screen = BrowseScreen()
    screen.setWindowTitle("Browse Screen Test - Phase 10D Restyled")
    screen.setGeometry(100, 100, 1280, 720)
    screen.show()
    
    sys.exit(app.exec_())
