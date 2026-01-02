#!/usr/bin/env python3
"""
Browse Screen for DeadStream - Phase 10A Redesign

This version implements Phase 10A Task 1.2: Refactored Browse Shows Layout.

Phase 10A redesign:
- ShowCard widget as primary display (right panel 70%)
- Prioritized navigation (left panel 30%)
- Browse by Date as primary action
- Random Show as prominent feature
- State-aware ShowCard display (default, random, date_selected modes)

Previous features retained:
- Task 7.1: Show list view with top-rated shows
- Task 7.2: Date browser (calendar-based browsing)
- Task 7.3: Venue filter
- Task 7.4: Year selector
- Task 7.5: Search functionality
- Task 7.6: Random show button
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

# Import centralized styles
from src.ui.styles.button_styles import (
    BROWSE_MODE_BUTTON_SELECTED, BROWSE_MODE_BUTTON_UNSELECTED,
    SECONDARY_BUTTON_STYLE, PRIMARY_BUTTON_STYLE, GREEN_ACCENT_BUTTON,
    PURPLE_ACCENT_BUTTON, ORANGE_ACCENT_BUTTON, BG_GRAY_800, BG_GRAY_900,
    BG_GRAY_700, TEXT_WHITE, TEXT_GRAY_400, BLUE_600, BLUE_700, BLUE_800,
    BORDER_RADIUS
)
from src.ui.styles.text_styles import (
    TITLE_SECTION_STYLE, TEXT_SUPPORTING_STYLE, FONT_2XL, FONT_BASE
)

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
    Browse screen for finding and selecting shows - Phase 10A Redesign

    Layout (Phase 10A):
    - Left panel (30%): Prioritized navigation buttons
    - Right panel (70%): ShowCard display area with multiple states

    Left Panel Priority Order:
    1. Browse by Date (primary, larger)
    2. Random Show (medium, prominent)
    3. Filters (medium - Phase 10A Task 3)
    4. Top Rated (optional, smaller)

    Right Panel States:
    - DEFAULT: Last played show or welcome message
    - RANDOM: Random show with "Try Another" button
    - DATE_SELECTED: Show from date browser
    - FILTERED: Random show matching active filter
    - LIST_VIEW: Traditional show list (retained for some modes)

    Browse modes retained from Phase 7:
    - Top Rated
    - Browse by Date
    - Browse by Venue
    - Browse by Year
    - Search Shows
    - Random Show

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
        self.current_filter = None  # Track active filter (Phase 10A Task 3)
        self.current_mode = 'default'  # Track current display mode
        self.setup_ui()

        # Create error handling UI components
        self.toast_manager = ToastManager(self)

        self.load_default_state()
    
    def setup_ui(self):
        """Create browse screen layout - Phase 10A redesign"""
        # Main horizontal layout (left panel + right panel)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Panel (30%) - Prioritized navigation
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, stretch=3)

        # Right Panel (70%) - ShowCard display area
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, stretch=7)

        self.setLayout(main_layout)
    
    def create_left_panel(self):
        """Create left panel with browse mode buttons"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_GRAY_800};
                border-right: 2px solid {BG_GRAY_700};
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("Browse Shows")
        title.setStyleSheet(f"""
            QLabel {{
                {TITLE_SECTION_STYLE}
                padding-bottom: 8px;
                border-bottom: 2px solid {BG_GRAY_700};
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
        Create prioritized navigation buttons - Phase 10A redesign

        Priority order:
        1. Browse by Date (larger, primary)
        2. Random Show (medium, exciting)
        3. Filters (medium, secondary) - Task 3
        4. Additional modes (smaller, tertiary)
        """
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # 1. Browse by Date - PRIMARY ACTION (larger, 80px)
        self.browse_by_date_btn = QPushButton("Browse by Date")
        self.browse_by_date_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BLUE_600};
                color: {TEXT_WHITE};
                border: none;
                border-radius: {BORDER_RADIUS};
                font-size: 20px;
                font-weight: 700;
                padding: 16px 24px;
            }}
            QPushButton:hover {{
                background-color: {BLUE_700};
            }}
            QPushButton:pressed {{
                background-color: {BLUE_800};
            }}
        """)
        self.browse_by_date_btn.setMinimumHeight(80)
        self.browse_by_date_btn.clicked.connect(self.show_date_browser)
        layout.addWidget(self.browse_by_date_btn)

        # 2. Random Show - PROMINENT FEATURE (medium, 70px, exciting color)
        self.random_show_btn = QPushButton("Random Show")
        self.random_show_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PURPLE_ACCENT_BUTTON.split('{')[1].split('}')[0].split(':')[1].strip().split(';')[0]};
                color: {TEXT_WHITE};
                border: none;
                border-radius: {BORDER_RADIUS};
                font-size: 18px;
                font-weight: 700;
                padding: 14px 20px;
            }}
            QPushButton:hover {{
                background-color: #7c3aed;
            }}
            QPushButton:pressed {{
                background-color: #6d28d9;
            }}
        """)
        self.random_show_btn.setMinimumHeight(70)
        self.random_show_btn.clicked.connect(self.on_random_show_clicked)
        layout.addWidget(self.random_show_btn)

        # 3. Filters - PLACEHOLDER for Task 3 (medium, 70px)
        self.filters_btn = QPushButton("Filters")
        self.filters_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.filters_btn.setMinimumHeight(70)
        self.filters_btn.clicked.connect(self.show_filters_placeholder)
        layout.addWidget(self.filters_btn)

        # Add separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background-color: {BG_GRAY_700}; max-height: 2px;")
        layout.addWidget(separator)

        # Additional modes (smaller, tertiary)
        # Top Rated Shows
        top_rated_btn = QPushButton("Top Rated Shows")
        top_rated_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        top_rated_btn.setMinimumHeight(55)
        top_rated_btn.clicked.connect(self.load_default_shows)
        layout.addWidget(top_rated_btn)

        # Browse by Venue
        venue_btn = QPushButton("Browse by Venue")
        venue_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        venue_btn.setMinimumHeight(55)
        venue_btn.clicked.connect(self.show_venue_browser)
        layout.addWidget(venue_btn)

        # Browse by Year
        year_btn = QPushButton("Browse by Year")
        year_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        year_btn.setMinimumHeight(55)
        year_btn.clicked.connect(self.show_year_browser)
        layout.addWidget(year_btn)

        # Search Shows
        search_btn = QPushButton("Search Shows")
        search_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        search_btn.setMinimumHeight(55)
        search_btn.clicked.connect(self.show_search_dialog)
        layout.addWidget(search_btn)

        return layout
    
    def create_right_panel(self):
        """
        Create right panel - Phase 10A redesign

        Primary display: ShowCard widget with multiple states
        Retained: Show list, date selector, year browser (stacked)
        """
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_GRAY_800};
            }}
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Stacked widget for different view modes
        self.content_stack = QStackedWidget()

        # Page 0: ShowCard display (PRIMARY - Phase 10A)
        showcard_page = QWidget()
        showcard_layout = QVBoxLayout(showcard_page)
        showcard_layout.setContentsMargins(20, 20, 20, 20)
        showcard_layout.setSpacing(16)

        # ShowCard widget - new primary display
        self.show_card = ShowCard()
        self.show_card.play_clicked.connect(self.on_showcard_play_clicked)
        self.show_card.try_another_clicked.connect(self.on_random_show_clicked)
        showcard_layout.addWidget(self.show_card)

        self.content_stack.addWidget(showcard_page)

        # Page 1: Show list view (with header) - RETAINED
        list_page = QWidget()
        list_layout = QVBoxLayout(list_page)
        list_layout.setContentsMargins(20, 20, 20, 20)
        list_layout.setSpacing(16)

        # Header widget (separate from ShowListWidget!)
        self.header_widget = QWidget()
        header_layout = QVBoxLayout(self.header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)

        # Title label
        self.header_title = QLabel("Top Rated Shows")
        self.header_title.setStyleSheet(f"""
            QLabel {{
                {TITLE_SECTION_STYLE}
            }}
        """)
        header_layout.addWidget(self.header_title)

        # Subtitle label
        self.header_subtitle = QLabel("Shows with 5+ reviews")
        self.header_subtitle.setStyleSheet(f"""
            QLabel {{
                {TEXT_SUPPORTING_STYLE}
            }}
        """)
        header_layout.addWidget(self.header_subtitle)

        list_layout.addWidget(self.header_widget)

        # Show list widget
        self.show_list = ShowListWidget()
        self.show_list.show_selected.connect(self.on_show_selected)
        list_layout.addWidget(self.show_list)

        self.content_stack.addWidget(list_page)

        # Page 2: Date selector view - RETAINED
        self.date_selector_widget = DateSelectorWidget()
        self.date_selector_widget.date_selected.connect(self.on_date_selector_selected)
        self.content_stack.addWidget(self.date_selector_widget)

        # Page 3: Year browser view - RETAINED
        self.year_browser_widget = YearBrowser()
        self.year_browser_widget.year_selected.connect(self.on_year_browser_selected)
        self.content_stack.addWidget(self.year_browser_widget)

        layout.addWidget(self.content_stack)

        return panel

    def create_navigation_buttons(self):
        """Create navigation buttons (Player, Settings)"""
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Back to Player button
        player_btn = QPushButton("Back to Player")
        player_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        player_btn.setMinimumHeight(50)
        player_btn.clicked.connect(self.player_requested.emit)
        layout.addWidget(player_btn)

        # Settings button
        settings_btn = QPushButton("Settings")
        settings_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        settings_btn.setMinimumHeight(50)
        settings_btn.clicked.connect(self.settings_requested.emit)
        layout.addWidget(settings_btn)

        return layout

    def update_header(self, title, subtitle):
        """Update header title and subtitle"""
        self.header_title.setText(title)
        self.header_subtitle.setText(subtitle)
    
    # ========================================================================
    # BROWSE MODE HANDLERS - PHASE 10A
    # ========================================================================

    def load_default_state(self):
        """
        Load default state on screen initialization - Phase 10A

        Shows last played show if available, otherwise displays welcome message
        """
        # Switch to ShowCard view (page 0)
        self.content_stack.setCurrentIndex(0)
        self.current_mode = 'default'

        # TODO: Query playback_history table for last played show
        # For now, show a welcome message
        self.show_card.date_label.setText("Welcome to DeadStream")
        self.show_card.venue_label.setText("Select a browse mode to find shows")
        self.show_card.location_label.setText("")
        self.show_card.quality_badge.setText("")
        self.show_card.setlist_label.setText(
            "Browse by Date: Explore shows from any date in history\n\n"
            "Random Show: Discover a high-quality random show\n\n"
            "Filters: Find shows by era, series, or quality"
        )
        self.show_card.set_mode('default')
        self.show_card.play_button.setEnabled(False)  # No show loaded yet

        print("[INFO] Browse screen initialized in default state")

    def on_random_show_clicked(self):
        """
        Handle Random Show button click - Phase 10A Task 2

        Loads random high-quality show and displays in ShowCard
        """
        try:
            # Switch to ShowCard view
            self.content_stack.setCurrentIndex(0)
            self.current_mode = 'random'

            # Show loading state
            self.show_card.show_loading()

            # Get random show from database
            # Using get_random_show for now (Phase 7 implementation)
            # Task 2.1 will add get_random_excellent_show with min_score and filter support
            show = get_random_show()

            if show:
                # Animate ShowCard update
                self.show_card.fade_in(show)
                self.show_card.set_mode('random')  # Shows "Try Another" button
                self.show_card.play_button.setEnabled(True)

                print(f"[OK] Random show loaded: {show['date']} - {show['venue']}")
            else:
                # No shows found (edge case)
                self.show_card.show_error("No shows found matching criteria")
                print("[WARN] No random show found")

        except Exception as e:
            print(f"[ERROR] Failed to load random show: {e}")
            import traceback
            traceback.print_exc()
            self.show_card.show_error("Unable to load random show")
            self.toast_manager.show_error("Database error: Unable to load random show")

    def on_showcard_play_clicked(self, identifier):
        """
        Handle play button click from ShowCard - Phase 10A

        Args:
            identifier (str): Show identifier to play
        """
        print(f"[INFO] Play requested from ShowCard: {identifier}")

        # Get full show data to emit
        # For now, we'll need to query the database
        # The ShowCard should store the full show dict
        if self.show_card.current_show:
            self.show_selected.emit(self.show_card.current_show)
        else:
            print("[ERROR] ShowCard has no current show data")

    def show_filters_placeholder(self):
        """
        Placeholder for Filters button - Phase 10A Task 3

        Will be replaced with actual filter dialog in Task 3.2
        """
        self.toast_manager.show_error(
            "Filters feature coming soon! (Phase 10A Task 3)"
        )
        print("[INFO] Filters button clicked (placeholder)")

    # ========================================================================
    # BROWSE MODE HANDLERS - PHASE 7 (RETAINED)
    # ========================================================================

    def load_default_shows(self):
        """Load top-rated shows (default view) - Phase 7 retained"""
        try:
            # Switch to list view (page 1 in Phase 10A)
            self.content_stack.setCurrentIndex(1)

            self.show_list.set_loading_state()

            shows = get_top_rated_shows(limit=50, min_reviews=5)

            self.update_header(
                "Top Rated Shows",
                f"{len(shows)} shows with 5+ reviews"
            )

            self.show_list.load_shows(shows)
            self.current_shows = shows

            print(f"[OK] Loaded {len(shows)} top-rated shows")

        except Exception as e:
            print(f"[ERROR] Failed to load top rated shows: {e}")
            import traceback
            traceback.print_exc()

            # Show error to user
            self.update_header("Error", "Failed to load shows")
            self.show_list.set_empty_state("Failed to load top rated shows")
            self.toast_manager.show_error(
                "Database error: Unable to load top rated shows. Check database connection."
            )

    def show_date_browser(self):
        """Show date selector in right panel (redesigned interface)"""
        # Switch to date selector view (page 2)
        self.content_stack.setCurrentIndex(2)

        # Reset selection in case it was used before
        self.date_selector_widget.reset_selection()

        print("[INFO] Date selector activated")
    
    def show_venue_browser(self):
        """Show venue browser dialog (Task 7.3)"""
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Browse by Venue")
        dialog.setModal(True)
        dialog.setMinimumSize(600, 500)
        
        # Apply dark theme
        dialog.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
            QLabel {
                color: white;
            }
            QListWidget {
                background-color: #1f2937;
                color: white;
                border: 2px solid #374151;
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #374151;
            }
            QListWidget::item:selected {
                background-color: #10b981;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #374151;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:enabled {
                background-color: #10b981;
                color: white;
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
            QPushButton:hover:enabled {
                background-color: #059669;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("Select a Venue")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        # Venue list
        venue_list = QListWidget()
        
        # Load venues
        venues = get_most_played_venues(limit=100)
        for venue_name, show_count in venues:
            item = QListWidgetItem(f"{venue_name} ({show_count} shows)")
            item.setData(Qt.UserRole, venue_name)
            venue_list.addItem(item)
        
        layout.addWidget(venue_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Select button
        select_btn = QPushButton("Load Shows")
        select_btn.setEnabled(False)  # Disabled until selection
        
        def on_selection_changed():
            """Enable button when venue selected"""
            select_btn.setEnabled(venue_list.currentItem() is not None)
        
        venue_list.itemSelectionChanged.connect(on_selection_changed)
        
        def on_select():
            """Load shows for selected venue"""
            current_item = venue_list.currentItem()
            if current_item:
                venue_name = current_item.data(Qt.UserRole)
                dialog.accept()
                self.load_shows_by_venue(venue_name)
        
        select_btn.clicked.connect(on_select)
        venue_list.itemDoubleClicked.connect(lambda: on_select())
        
        button_layout.addWidget(select_btn)
        layout.addLayout(button_layout)
        
        # Show dialog
        dialog.exec_()
    
    def show_year_browser(self):
        """Show year browser in right panel (Task 7.4)"""
        # Switch to year browser view (page 3)
        self.content_stack.setCurrentIndex(3)

        # Reload year data in case it's stale
        self.year_browser_widget.load_year_data()
        self.year_browser_widget.update_year_grid()

        print("[INFO] Year browser activated")
    
    def show_search_dialog(self):
        """Show search dialog (Task 7.5)"""
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Search Shows")
        dialog.setModal(True)
        dialog.setMinimumSize(600, 500)
        
        # Apply dark theme
        dialog.setStyleSheet("""
            QDialog {
                background-color: #111827;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add search widget
        search_widget = SearchWidget()
        search_widget.search_submitted.connect(lambda params: (
        dialog.accept(),
        self.perform_search(params)
))
        layout.addWidget(search_widget)
        
        # Show dialog
        dialog.exec_()
    
    def load_shows_by_date(self, date_str):
        """Load and display shows from a specific date (Task 7.2) - Phase 7 retained"""

        try:
            # Switch to list view (page 1 in Phase 10A)
            self.content_stack.setCurrentIndex(1)

            self.show_list.set_loading_state()

            # Get shows for this date
            shows = get_show_by_date(date_str)

            if not shows:
                # No shows found
                self.update_header(
                    "No Shows Found",
                    f"No shows on {date_str}"
                )
                self.show_list.set_empty_state(f"No shows on {date_str}")
                return

            # Update header
            self.update_header(
                f"Shows on {date_str}",
                f"{len(shows)} recording(s) from this date"
            )

            # Load shows into list
            self.show_list.load_shows(shows)
            self.current_shows = shows

            print(f"[OK] Loaded {len(shows)} shows from {date_str}")

        except Exception as e:
            print(f"[ERROR] Failed to load date shows: {e}")
            import traceback
            traceback.print_exc()
            self.update_header("Error", f"Failed to load shows for {date_str}")
            self.show_list.set_empty_state("Error loading shows")
            self.toast_manager.show_error(f"Database error: Unable to load shows for {date_str}")
    
    def load_shows_by_venue(self, venue_name):
        """Load and display shows from a specific venue (Task 7.3) - Phase 7 retained"""

        try:
            # Switch to list view (page 1 in Phase 10A)
            self.content_stack.setCurrentIndex(1)

            self.show_list.set_loading_state()

            # Get shows for this venue
            shows = search_by_venue(venue_name, exact_match=False)

            if not shows:
                # No shows found
                self.update_header(
                    "No Shows Found",
                    f"No shows found at {venue_name}"
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
        """Load and display shows from a specific year (Task 7.4) - Phase 7 retained"""

        try:
            # Switch to list view (page 1 in Phase 10A)
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
            self.show_list.set_loading_state()
            
            # Extract search parameters
            query = search_params.get('query', '')
            venue = search_params.get('venue', '')
            year = search_params.get('year', None)
            min_rating = search_params.get('min_rating', None)
            
            print(f"[INFO] Performing search: query={query}, venue={venue}, year={year}, rating={min_rating}")
            
            # Import search function
            from src.database.queries import search_shows
            
            # Perform search
            results = search_shows(
                query=query,
                venue=venue,
                year=year,
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
        """Load and display search results (Task 7.5) - Phase 7 retained"""

        try:
            # Switch to list view (page 1 in Phase 10A)
            self.content_stack.setCurrentIndex(1)

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
        """Handle show selection from list"""
        print(f"[INFO] Show selected: {show['date']} - {show['venue']}")
        self.show_selected.emit(show)

    def on_date_selector_selected(self, date_str):
        """
        Handle date selection from DateSelectorWidget - Phase 10A Task 1.3

        Loads selected show in ShowCard instead of list view
        """
        print(f"[INFO] Date selected from selector: {date_str}")

        try:
            # Get shows for this date
            shows = get_show_by_date(date_str)

            if not shows:
                # No shows found - show error in ShowCard
                self.content_stack.setCurrentIndex(0)
                self.show_card.show_error(f"No show found for {date_str}")
                print(f"[WARN] No shows found for {date_str}")
                return

            # Take first show (or best scored show if multiple)
            show = shows[0]
            if len(shows) > 1:
                # If multiple recordings, pick the best one
                show = max(shows, key=lambda s: s.get('recording_score', 0))
                print(f"[INFO] Multiple recordings found, selected best: score={show.get('recording_score', 0)}")

            # Switch to ShowCard view (page 0)
            self.content_stack.setCurrentIndex(0)
            self.current_mode = 'date_selected'

            # Load show in ShowCard with fade animation
            self.show_card.fade_in(show)
            self.show_card.set_mode('date_selected')  # No "Try Another" button
            self.show_card.play_button.setEnabled(True)

            print(f"[OK] Date selection loaded in ShowCard: {show['date']} - {show['venue']}")

        except Exception as e:
            print(f"[ERROR] Failed to load date selection: {e}")
            import traceback
            traceback.print_exc()
            self.content_stack.setCurrentIndex(0)
            self.show_card.show_error(f"Error loading show for {date_str}")
            self.toast_manager.show_error(f"Database error: Unable to load show for {date_str}")

    def on_year_browser_selected(self, year):
        """Handle year selection from YearBrowser"""
        print(f"[INFO] Year selected from browser: {year}")
        # Load shows for this year (will switch back to list view)
        self.load_shows_by_year(year)


# Test code
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Apply dark theme
    app.setStyleSheet("""
        QWidget {
            background-color: #000000;
            color: #f3f4f6;
        }
    """)
    
    screen = BrowseScreen()
    screen.setWindowTitle("Browse Screen Test - WITH RANDOM SHOW")
    screen.setGeometry(100, 100, 1280, 720)
    screen.show()
    
    sys.exit(app.exec_())
