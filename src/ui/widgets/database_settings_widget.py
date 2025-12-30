#!/usr/bin/env python3
"""
Database Settings Widget for Settings Screen
Displays database statistics and provides update functionality
"""

import sys
import os

# Add project root to path for imports (4 levels up from src/ui/widgets/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QProgressDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from src.database.queries import (
    get_show_count, 
    get_venue_count,
    get_date_range,
    get_years_with_shows,
    get_show_count_by_year
)


class DatabaseUpdateThread(QThread):
    """
    Background thread for updating the database from Internet Archive
    
    Signals:
        progress(int, str): Progress percentage and status message
        finished(bool, str): Success status and message
    """
    
    progress = pyqtSignal(int, str)  # percent, message
    finished = pyqtSignal(bool, str)  # success, message
    
    def run(self):
        """
        Run the database update process
        
        NOTE: This is a placeholder for Phase 9+ when we implement
        the actual database update mechanism. For now, it simulates
        the update process.
        """
        try:
            # Placeholder for actual update logic
            # In Phase 9+, this will call the populate script with update mode
            
            # Simulate update steps
            self.progress.emit(10, "Connecting to Internet Archive...")
            self.msleep(500)
            
            self.progress.emit(30, "Checking for new shows...")
            self.msleep(500)
            
            self.progress.emit(60, "Downloading metadata...")
            self.msleep(500)
            
            self.progress.emit(90, "Updating database...")
            self.msleep(500)
            
            self.progress.emit(100, "Update complete")
            
            # Report success
            self.finished.emit(True, "Database updated successfully")
            
        except Exception as e:
            self.finished.emit(False, f"Update failed: {str(e)}")


class DatabaseSettingsWidget(QWidget):
    """
    Database settings and statistics
    
    Features:
    - Display database statistics (show count, venues, date range)
    - Manual database update button
    - Database maintenance options (future)
    - Last update timestamp (future)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.update_thread = None
        self.init_ui()
        self.load_statistics()
    
    def init_ui(self):
        """Initialize the database settings UI"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        
        # Title
        title = QLabel("Database")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Show database information and updates")
        subtitle.setStyleSheet("color: #9ca3af; font-size: 14px;")
        header_layout.addWidget(subtitle)
        
        main_layout.addLayout(header_layout)
        
        # Statistics section
        stats_card = self.create_statistics_card()
        main_layout.addWidget(stats_card)
        
        # Update section
        update_card = self.create_update_card()
        main_layout.addWidget(update_card)
        
        # Maintenance section (placeholder for future)
        maintenance_card = self.create_maintenance_card()
        main_layout.addWidget(maintenance_card)
        
        # Spacer
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def create_statistics_card(self):
        """Create database statistics display card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Card title
        card_title = QLabel("Database Statistics")
        card_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(card_title)
        
        # Statistics rows
        self.stat_labels = {}
        
        stats = [
            ("total_shows", "Total Shows", "0"),
            ("unique_venues", "Unique Venues", "0"),
            ("years_covered", "Years Covered", "0"),
            ("date_range", "Date Range", "Loading..."),
            ("last_update", "Last Update", "Never")
        ]
        
        for key, label_text, initial_value in stats:
            stat_row, value_label = self.create_stat_row(label_text, initial_value)
            layout.addWidget(stat_row)
            # Store reference to value label for updates
            self.stat_labels[key] = value_label
        
        card.setLayout(layout)
        return card
    
    def create_stat_row(self, label_text, value_text):
        """Create a statistics row with label and value
        
        Returns:
            tuple: (row_widget, value_label) for easy reference
        """
        row = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        
        # Label
        label = QLabel(label_text)
        label.setStyleSheet("color: #9ca3af; font-size: 16px;")
        row_layout.addWidget(label)
        
        # Spacer
        row_layout.addStretch()
        
        # Value
        value = QLabel(value_text)
        value.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        row_layout.addWidget(value)
        
        row.setLayout(row_layout)
        return row, value  # Return both the row and the value label
    
    def create_update_card(self):
        """Create database update controls card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Card title
        card_title = QLabel("Database Updates")
        card_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(card_title)
        
        # Description
        desc = QLabel(
            "Check Internet Archive for new shows and recordings. "
            "This will download new show metadata but won't affect existing data."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #9ca3af; font-size: 14px;")
        layout.addWidget(desc)
        
        # Update button
        self.update_btn = QPushButton("Update Database")
        self.update_btn.setMinimumHeight(50)
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #6b7280;
            }
        """)
        self.update_btn.clicked.connect(self.start_database_update)
        layout.addWidget(self.update_btn)
        
        # Status label (hidden by default)
        self.update_status = QLabel("")
        self.update_status.setStyleSheet("color: #9ca3af; font-size: 14px;")
        self.update_status.setWordWrap(True)
        self.update_status.hide()
        layout.addWidget(self.update_status)
        
        card.setLayout(layout)
        return card
    
    def create_maintenance_card(self):
        """Create database maintenance card (placeholder for future)"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Card title
        card_title = QLabel("Database Maintenance")
        card_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(card_title)
        
        # Description
        desc = QLabel(
            "Advanced database maintenance options. "
            "These features will be available in a future update."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #9ca3af; font-size: 14px;")
        layout.addWidget(desc)
        
        # Placeholder buttons (disabled)
        buttons = [
            ("Rebuild Database", "Rebuild database indexes for better performance"),
            ("Backup Database", "Create a backup of the database"),
            ("Reset Database", "Clear all data and start fresh (requires confirmation)")
        ]
        
        for btn_text, tooltip in buttons:
            btn = QPushButton(btn_text)
            btn.setMinimumHeight(44)
            btn.setEnabled(False)
            btn.setToolTip(tooltip)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #374151;
                    color: #6b7280;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    padding: 10px;
                }
            """)
            layout.addWidget(btn)
        
        card.setLayout(layout)
        return card
    
    def load_statistics(self):
        """Load and display current database statistics"""
        try:
            # Get total show count
            total_shows = get_show_count()
            self.stat_labels["total_shows"].setText(f"{total_shows:,}")
            
            # Get unique venue count
            venue_count = get_venue_count()
            self.stat_labels["unique_venues"].setText(f"{venue_count:,}")
            
            # Get years covered
            years = get_years_with_shows()
            if years:
                years_count = len(years)
                self.stat_labels["years_covered"].setText(f"{years_count}")
                
                # Get date range
                earliest = min(years)
                latest = max(years)
                self.stat_labels["date_range"].setText(f"{earliest} - {latest}")
            else:
                self.stat_labels["years_covered"].setText("0")
                self.stat_labels["date_range"].setText("No data")
            
            # Last update (placeholder - will be implemented with settings persistence)
            self.stat_labels["last_update"].setText("Not tracked yet")
            
        except Exception as e:
            print(f"[ERROR] Failed to load database statistics: {e}")
            # Show error in first stat
            self.stat_labels["total_shows"].setText("Error loading stats")
    
    def start_database_update(self):
        """Start the database update process in background thread"""
        # Disable update button
        self.update_btn.setEnabled(False)
        self.update_btn.setText("Updating...")
        
        # Show status
        self.update_status.setText("Starting database update...")
        self.update_status.show()
        
        # Create and start update thread
        self.update_thread = DatabaseUpdateThread()
        self.update_thread.progress.connect(self.on_update_progress)
        self.update_thread.finished.connect(self.on_update_finished)
        self.update_thread.start()
    
    def on_update_progress(self, percent, message):
        """Handle update progress updates"""
        self.update_status.setText(f"{message} ({percent}%)")
    
    def on_update_finished(self, success, message):
        """Handle update completion"""
        # Re-enable update button
        self.update_btn.setEnabled(True)
        self.update_btn.setText("Update Database")
        
        # Show result
        self.update_status.setText(message)
        
        if success:
            # Reload statistics
            self.load_statistics()
            
            # Show success message
            QMessageBox.information(
                self,
                "Update Complete",
                "Database has been updated successfully."
            )
        else:
            # Show error message
            QMessageBox.warning(
                self,
                "Update Failed",
                f"Database update failed:\n\n{message}"
            )


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    """Test the database settings widget standalone"""
    from PyQt5.QtWidgets import QApplication
    
    print("[INFO] Testing DatabaseSettingsWidget standalone...")
    
    app = QApplication(sys.argv)
    
    # Create test window
    widget = DatabaseSettingsWidget()
    widget.setWindowTitle("Database Settings Test")
    widget.setGeometry(100, 100, 600, 800)
    widget.show()
    
    print("[INFO] Database settings widget displayed")
    print("[INFO] Test the following:")
    print("  1. Verify statistics are loaded and displayed")
    print("  2. Click 'Update Database' button")
    print("  3. Observe update progress simulation")
    print("  4. Verify statistics refresh after update")
    print("\n[INFO] Close window to exit test")
    
    sys.exit(app.exec_())
