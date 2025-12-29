#!/usr/bin/env python3
"""
Network Settings Widget for DeadStream Settings Screen
Provides WiFi management interface for Raspberry Pi

Author: DeadStream Development Team
Created: December 29, 2025
Phase: 8, Task: 8.2
"""

import subprocess
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont


class NetworkSettingsWidget(QWidget):
    """
    Network settings panel with WiFi management
    
    Features:
    - WiFi status display
    - Network scanning
    - Connection management
    - Signal strength indicators
    """
    
    def __init__(self):
        super().__init__()
        self.networks = []
        self.current_ssid = None
        self.is_connected = False
        
        self.setup_ui()
        self.refresh_status()
    
    # ========================================================================
    # UI SETUP
    # ========================================================================
    
    def setup_ui(self):
        """Initialize the network settings interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #111827;
            }
            QScrollBar:vertical {
                background-color: #1f2937;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4b5563;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6b7280;
            }
        """)
        
        # Content container
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(20)
        
        # WiFi Status Card
        self.status_card = self.create_status_card()
        content_layout.addWidget(self.status_card)
        
        # Available Networks Section
        networks_section = self.create_networks_section()
        content_layout.addWidget(networks_section)
        
        # Action Buttons
        actions = self.create_action_buttons()
        content_layout.addWidget(actions)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def create_header(self):
        """Create the header section"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-bottom: 2px solid #374151;
            }
        """)
        header.setFixedHeight(100)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 20, 24, 20)
        
        # Icon placeholder (WiFi symbol)
        icon_label = QLabel("[WiFi]")
        icon_label.setStyleSheet("""
            color: #3b82f6;
            font-size: 32px;
            font-weight: bold;
        """)
        layout.addWidget(icon_label)
        
        # Title and subtitle
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title = QLabel("Network Settings")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        text_layout.addWidget(title)
        
        subtitle = QLabel("Manage WiFi and network connections")
        subtitle.setStyleSheet("""
            color: #9ca3af;
            font-size: 14px;
        """)
        text_layout.addWidget(subtitle)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        return header
    
    def create_status_card(self):
        """Create WiFi status display card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border: 2px solid #374151;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Card title
        title = QLabel("WiFi Status")
        title.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        # Connection status
        self.status_label = QLabel("Checking...")
        self.status_label.setStyleSheet("""
            color: #9ca3af;
            font-size: 16px;
        """)
        layout.addWidget(self.status_label)
        
        # Network name
        self.network_label = QLabel("")
        self.network_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: 600;
        """)
        layout.addWidget(self.network_label)
        
        # Signal strength
        self.signal_label = QLabel("")
        self.signal_label.setStyleSheet("""
            color: #9ca3af;
            font-size: 14px;
        """)
        layout.addWidget(self.signal_label)
        
        # IP address
        self.ip_label = QLabel("")
        self.ip_label.setStyleSheet("""
            color: #9ca3af;
            font-size: 14px;
            font-family: monospace;
        """)
        layout.addWidget(self.ip_label)
        
        return card
    
    def create_networks_section(self):
        """Create available networks list section"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        
        # Section header
        header = QLabel("Available Networks")
        header.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        layout.addWidget(header)
        
        # Networks list container
        self.networks_container = QWidget()
        self.networks_layout = QVBoxLayout(self.networks_container)
        self.networks_layout.setSpacing(8)
        self.networks_layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(self.networks_container)
        
        # Loading message (initially)
        loading_label = QLabel("Click 'Refresh Networks' to scan for WiFi networks")
        loading_label.setStyleSheet("""
            color: #6b7280;
            font-size: 14px;
            padding: 20px;
        """)
        self.networks_layout.addWidget(loading_label)
        
        return container
    
    def create_action_buttons(self):
        """Create action buttons"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(12)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Networks")
        refresh_btn.setFixedHeight(50)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_networks)
        layout.addWidget(refresh_btn)
        
        # Advanced settings button (placeholder for future)
        advanced_btn = QPushButton("Advanced Settings")
        advanced_btn.setFixedHeight(50)
        advanced_btn.setStyleSheet("""
            QPushButton {
                background-color: #374151;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
            QPushButton:pressed {
                background-color: #6b7280;
            }
        """)
        advanced_btn.clicked.connect(self.show_advanced_settings)
        layout.addWidget(advanced_btn)
        
        return container
    
    # ========================================================================
    # NETWORK OPERATIONS
    # ========================================================================
    
    def refresh_status(self):
        """Refresh WiFi connection status"""
        try:
            # Get current connection info
            result = subprocess.run(
                ['iwgetid', '-r'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # Connected to a network
                self.current_ssid = result.stdout.strip()
                self.is_connected = True
                
                # Get signal strength
                signal_strength = self.get_signal_strength()
                
                # Get IP address
                ip_address = self.get_ip_address()
                
                # Update status display
                self.status_label.setText("[OK] Connected")
                self.status_label.setStyleSheet("""
                    color: #10b981;
                    font-size: 16px;
                    font-weight: bold;
                """)
                
                self.network_label.setText(self.current_ssid)
                self.signal_label.setText(f"Signal: {signal_strength}")
                self.ip_label.setText(f"IP: {ip_address}")
                
            else:
                # Not connected
                self.is_connected = False
                self.current_ssid = None
                
                self.status_label.setText("[WARN] Not Connected")
                self.status_label.setStyleSheet("""
                    color: #f59e0b;
                    font-size: 16px;
                    font-weight: bold;
                """)
                
                self.network_label.setText("No network connection")
                self.signal_label.setText("")
                self.ip_label.setText("")
        
        except Exception as e:
            print(f"[ERROR] Failed to check WiFi status: {e}")
            self.status_label.setText("[ERROR] Status Unknown")
            self.status_label.setStyleSheet("""
                color: #ef4444;
                font-size: 16px;
                font-weight: bold;
            """)
    
    def get_signal_strength(self):
        """Get WiFi signal strength"""
        try:
            result = subprocess.run(
                ['iwconfig'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            # Parse signal level from iwconfig output
            # Format: "Link Quality=70/70  Signal level=-40 dBm"
            match = re.search(r'Signal level=(-?\d+) dBm', result.stdout)
            if match:
                signal_dbm = int(match.group(1))
                
                # Convert to quality description
                if signal_dbm >= -50:
                    return "Excellent"
                elif signal_dbm >= -60:
                    return "Good"
                elif signal_dbm >= -70:
                    return "Fair"
                else:
                    return "Weak"
            
            return "Unknown"
        
        except Exception as e:
            print(f"[ERROR] Failed to get signal strength: {e}")
            return "Unknown"
    
    def get_ip_address(self):
        """Get current IP address"""
        try:
            result = subprocess.run(
                ['hostname', '-I'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                # Get first IP address
                ips = result.stdout.strip().split()
                if ips:
                    return ips[0]
            
            return "Unknown"
        
        except Exception as e:
            print(f"[ERROR] Failed to get IP address: {e}")
            return "Unknown"
    
    def refresh_networks(self):
        """Scan for available WiFi networks"""
        print("[INFO] Scanning for WiFi networks...")
        
        # Clear existing networks
        while self.networks_layout.count():
            child = self.networks_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Show scanning message
        scanning_label = QLabel("Scanning for networks...")
        scanning_label.setStyleSheet("""
            color: #3b82f6;
            font-size: 14px;
            padding: 20px;
        """)
        self.networks_layout.addWidget(scanning_label)
        
        # Perform scan in the background (simplified for now)
        # In production, this would use QThread to avoid blocking UI
        QTimer.singleShot(500, self.load_networks)
    
    def load_networks(self):
        """Load scanned networks"""
        try:
            # Scan for networks using iwlist
            result = subprocess.run(
                ['sudo', 'iwlist', 'wlan0', 'scan'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse scan results
                networks = self.parse_scan_results(result.stdout)
                
                # Clear scanning message
                while self.networks_layout.count():
                    child = self.networks_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                
                if networks:
                    # Display networks
                    for network in networks:
                        network_card = self.create_network_card(network)
                        self.networks_layout.addWidget(network_card)
                    
                    print(f"[OK] Found {len(networks)} networks")
                else:
                    # No networks found
                    no_networks = QLabel("No networks found")
                    no_networks.setStyleSheet("""
                        color: #6b7280;
                        font-size: 14px;
                        padding: 20px;
                    """)
                    self.networks_layout.addWidget(no_networks)
            else:
                raise Exception("Scan failed")
        
        except Exception as e:
            print(f"[ERROR] Network scan failed: {e}")
            
            # Clear scanning message
            while self.networks_layout.count():
                child = self.networks_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            error_label = QLabel("Failed to scan networks. Try again.")
            error_label.setStyleSheet("""
                color: #ef4444;
                font-size: 14px;
                padding: 20px;
            """)
            self.networks_layout.addWidget(error_label)
    
    def parse_scan_results(self, scan_output):
        """
        Parse iwlist scan output into network list
        
        Returns list of dicts with keys: ssid, signal, security
        """
        networks = []
        current_network = {}
        
        for line in scan_output.split('\n'):
            line = line.strip()
            
            # New cell (network) starts
            if 'Cell' in line and 'Address:' in line:
                if current_network.get('ssid'):
                    networks.append(current_network)
                current_network = {
                    'ssid': '',
                    'signal': 0,
                    'security': 'Open'
                }
            
            # SSID
            elif 'ESSID:' in line:
                match = re.search(r'ESSID:"(.+)"', line)
                if match:
                    current_network['ssid'] = match.group(1)
            
            # Signal strength
            elif 'Quality=' in line:
                match = re.search(r'Quality=(\d+)/(\d+)', line)
                if match:
                    quality = int(match.group(1))
                    max_quality = int(match.group(2))
                    # Convert to percentage
                    current_network['signal'] = int((quality / max_quality) * 100)
            
            # Security
            elif 'Encryption key:on' in line:
                current_network['security'] = 'Secured'
        
        # Add last network
        if current_network.get('ssid'):
            networks.append(current_network)
        
        # Filter out empty SSIDs and sort by signal strength
        networks = [n for n in networks if n['ssid']]
        networks.sort(key=lambda x: x['signal'], reverse=True)
        
        return networks
    
    def create_network_card(self, network):
        """Create a network card widget"""
        card = QFrame()
        
        # Different style for current network
        is_current = (network['ssid'] == self.current_ssid)
        
        if is_current:
            card.setStyleSheet("""
                QFrame {
                    background-color: #1e40af;
                    border: 2px solid #3b82f6;
                    border-radius: 8px;
                }
                QFrame:hover {
                    background-color: #1e3a8a;
                }
            """)
        else:
            card.setStyleSheet("""
                QFrame {
                    background-color: #1f2937;
                    border: 2px solid #374151;
                    border-radius: 8px;
                }
                QFrame:hover {
                    background-color: #374151;
                    border-color: #4b5563;
                }
            """)
        
        card.setMinimumHeight(70)
        card.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Network info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        # SSID
        ssid_layout = QHBoxLayout()
        
        ssid_label = QLabel(network['ssid'])
        ssid_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: 600;
        """)
        ssid_layout.addWidget(ssid_label)
        
        # Current network indicator
        if is_current:
            current_badge = QLabel("[CONNECTED]")
            current_badge.setStyleSheet("""
                color: #10b981;
                font-size: 12px;
                font-weight: bold;
            """)
            ssid_layout.addWidget(current_badge)
        
        ssid_layout.addStretch()
        info_layout.addLayout(ssid_layout)
        
        # Security and signal
        details = f"{network['security']} - Signal: {network['signal']}%"
        details_label = QLabel(details)
        details_label.setStyleSheet("""
            color: #9ca3af;
            font-size: 13px;
        """)
        info_layout.addWidget(details_label)
        
        layout.addLayout(info_layout)
        
        # Connect button (if not current network)
        if not is_current:
            connect_btn = QPushButton("Connect")
            connect_btn.setFixedSize(100, 40)
            connect_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
                QPushButton:pressed {
                    background-color: #1d4ed8;
                }
            """)
            connect_btn.clicked.connect(
                lambda: self.connect_to_network(network['ssid'])
            )
            layout.addWidget(connect_btn)
        
        return card
    
    def connect_to_network(self, ssid):
        """Connect to a WiFi network"""
        print(f"[INFO] Connecting to network: {ssid}")
        
        # Show message
        msg = QMessageBox(self)
        msg.setWindowTitle("Connect to Network")
        msg.setText(f"Connecting to '{ssid}'...")
        msg.setInformativeText("This feature will be fully implemented in Task 8.3")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1f2937;
            }
            QLabel {
                color: white;
            }
        """)
        msg.exec_()
        
        # TODO: Implement actual connection logic in Task 8.3
        # Will need to handle password input for secured networks
    
    def show_advanced_settings(self):
        """Show advanced network settings (placeholder)"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Advanced Settings")
        msg.setText("Advanced network settings")
        msg.setInformativeText(
            "Features like static IP, DNS configuration, etc. "
            "will be added in a future update."
        )
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1f2937;
            }
            QLabel {
                color: white;
            }
        """)
        msg.exec_()


# Test code
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create test window
    window = QWidget()
    window.setWindowTitle("Network Settings Test")
    window.setGeometry(100, 100, 800, 600)
    window.setStyleSheet("background-color: #111827;")
    
    layout = QVBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)
    
    # Add network settings widget
    network_widget = NetworkSettingsWidget()
    layout.addWidget(network_widget)
    
    window.show()
    sys.exit(app.exec_())
