#!/usr/bin/env python3
"""
DeadStream Network Settings Widget
Phase 8, Task 8.2: Network settings implementation

This widget provides WiFi configuration and network status display.
Allows users to view connection status, scan for networks, and connect.
"""

import sys
import os
import subprocess

# Add project root to path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class NetworkSettingsWidget(QWidget):
    """Network settings and WiFi management widget"""
    
    def __init__(self):
        super().__init__()
        self.networks = []  # List of available networks
        self.init_ui()
        
        # Auto-refresh network status every 10 seconds
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_network_info)
        self.refresh_timer.start(10000)  # 10 seconds
        
        # Initial load
        self.refresh_network_info()
    
    def init_ui(self):
        """Initialize the network settings UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header
        header = self._create_header()
        main_layout.addLayout(header)
        
        # WiFi Status Card
        self.status_card = self._create_status_card()
        main_layout.addWidget(self.status_card)
        
        # Available Networks Section
        networks_header = QLabel("Available Networks")
        networks_header.setStyleSheet("""
            color: #ffffff;
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        """)
        main_layout.addWidget(networks_header)
        
        # Scrollable network list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Container for network list
        self.network_list_widget = QWidget()
        self.network_list_layout = QVBoxLayout(self.network_list_widget)
        self.network_list_layout.setContentsMargins(0, 0, 0, 0)
        self.network_list_layout.setSpacing(10)
        
        scroll_area.setWidget(self.network_list_widget)
        main_layout.addWidget(scroll_area, stretch=1)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        refresh_btn = QPushButton("Refresh Networks")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_network_info)
        button_layout.addWidget(refresh_btn)
        
        advanced_btn = QPushButton("Advanced Settings")
        advanced_btn.setStyleSheet("""
            QPushButton {
                background-color: #1f2937;
                color: #ffffff;
                border: 2px solid #374151;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #374151;
            }
            QPushButton:pressed {
                background-color: #4b5563;
            }
        """)
        advanced_btn.clicked.connect(self._show_advanced_settings)
        button_layout.addWidget(advanced_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def _create_header(self):
        """Create the header with title and icon"""
        layout = QHBoxLayout()
        
        # WiFi icon (using text representation)
        icon_label = QLabel("[WiFi]")
        icon_label.setStyleSheet("""
            color: #2563eb;
            font-size: 28px;
            font-weight: bold;
        """)
        layout.addWidget(icon_label)
        
        # Title and subtitle
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        title = QLabel("Network Settings")
        title.setStyleSheet("""
            color: #ffffff;
            font-size: 28px;
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
        
        return layout
    
    def _create_status_card(self):
        """Create the WiFi status information card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border: 2px solid #374151;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        card.setFixedHeight(200)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # WiFi toggle and status
        status_layout = QHBoxLayout()
        
        wifi_label = QLabel("WiFi Status:")
        wifi_label.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 600;")
        status_layout.addWidget(wifi_label)
        
        self.status_indicator = QLabel("Checking...")
        self.status_indicator.setStyleSheet("color: #fbbf24; font-size: 18px;")
        status_layout.addWidget(self.status_indicator)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Current network
        self.current_network_label = QLabel("Network: --")
        self.current_network_label.setStyleSheet("color: #d1d5db; font-size: 16px;")
        layout.addWidget(self.current_network_label)
        
        # Signal strength
        self.signal_strength_label = QLabel("Signal: --")
        self.signal_strength_label.setStyleSheet("color: #d1d5db; font-size: 16px;")
        layout.addWidget(self.signal_strength_label)
        
        # IP address
        self.ip_address_label = QLabel("IP Address: --")
        self.ip_address_label.setStyleSheet("color: #d1d5db; font-size: 16px;")
        layout.addWidget(self.ip_address_label)
        
        layout.addStretch()
        
        return card
    
    def refresh_network_info(self):
        """Refresh WiFi status and available networks"""
        # Get current connection status
        self._update_connection_status()
        
        # Scan for available networks
        self._scan_networks()
        
        # Update network list display
        self._update_network_list()
    
    def _update_connection_status(self):
        """Update current WiFi connection status"""
        try:
            # Get current WiFi connection using nmcli
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'ACTIVE,SSID,SIGNAL,IP4.ADDRESS', 'dev', 'wifi', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                connected = False
                
                for line in lines:
                    if line.startswith('yes:'):
                        # This is the active connection
                        parts = line.split(':')
                        if len(parts) >= 3:
                            ssid = parts[1]
                            signal = parts[2]
                            
                            # Update status indicators
                            self.status_indicator.setText("Connected")
                            self.status_indicator.setStyleSheet("color: #10b981; font-size: 18px;")
                            
                            self.current_network_label.setText(f"Network: {ssid}")
                            self.signal_strength_label.setText(f"Signal: {signal}%")
                            
                            connected = True
                            break
                
                if not connected:
                    self.status_indicator.setText("Not Connected")
                    self.status_indicator.setStyleSheet("color: #ef4444; font-size: 18px;")
                    self.current_network_label.setText("Network: --")
                    self.signal_strength_label.setText("Signal: --")
            
            # Get IP address separately
            ip_result = subprocess.run(
                ['hostname', '-I'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if ip_result.returncode == 0:
                ip_addresses = ip_result.stdout.strip().split()
                if ip_addresses:
                    self.ip_address_label.setText(f"IP Address: {ip_addresses[0]}")
                else:
                    self.ip_address_label.setText("IP Address: --")
            
        except subprocess.TimeoutExpired:
            print("[WARN] Network status check timed out")
            self.status_indicator.setText("Timeout")
            self.status_indicator.setStyleSheet("color: #fbbf24; font-size: 18px;")
        except FileNotFoundError:
            print("[WARN] nmcli not found - network management unavailable")
            self.status_indicator.setText("Unavailable")
            self.status_indicator.setStyleSheet("color: #6b7280; font-size: 18px;")
        except Exception as e:
            print(f"[ERROR] Failed to update connection status: {e}")
            self.status_indicator.setText("Error")
            self.status_indicator.setStyleSheet("color: #ef4444; font-size: 18px;")
    
    def _scan_networks(self):
        """Scan for available WiFi networks"""
        try:
            # Request fresh scan
            subprocess.run(
                ['nmcli', 'dev', 'wifi', 'rescan'],
                capture_output=True,
                timeout=10
            )
            
            # Get network list
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'ACTIVE,SSID,SECURITY,SIGNAL,RATE', 'dev', 'wifi', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.networks = []
                lines = result.stdout.strip().split('\n')
                
                for line in lines:
                    if not line:
                        continue
                    
                    parts = line.split(':')
                    if len(parts) >= 4:
                        network = {
                            'active': parts[0] == 'yes',
                            'ssid': parts[1],
                            'security': parts[2] if parts[2] else 'Open',
                            'signal': parts[3],
                            'rate': parts[4] if len(parts) > 4 else '--'
                        }
                        
                        # Only add if SSID is not empty
                        if network['ssid']:
                            self.networks.append(network)
                
                # Sort: active first, then by signal strength
                self.networks.sort(key=lambda x: (not x['active'], -int(x['signal']) if x['signal'].isdigit() else 0))
        
        except subprocess.TimeoutExpired:
            print("[WARN] Network scan timed out")
        except FileNotFoundError:
            print("[WARN] nmcli not found - cannot scan networks")
        except Exception as e:
            print(f"[ERROR] Failed to scan networks: {e}")
    
    def _update_network_list(self):
        """Update the displayed list of available networks"""
        # Clear existing network cards
        while self.network_list_layout.count():
            item = self.network_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add network cards
        if not self.networks:
            no_networks = QLabel("No networks found. Click 'Refresh Networks' to scan.")
            no_networks.setStyleSheet("color: #9ca3af; font-size: 16px; padding: 20px;")
            self.network_list_layout.addWidget(no_networks)
        else:
            for network in self.networks:
                card = self._create_network_card(network)
                self.network_list_layout.addWidget(card)
        
        # Add stretch at end
        self.network_list_layout.addStretch()
    
    def _create_network_card(self, network):
        """Create a card for a single network"""
        card = QFrame()
        
        # Different styling for active network
        if network['active']:
            card.setStyleSheet("""
                QFrame {
                    background-color: #1e3a8a;
                    border: 2px solid #2563eb;
                    border-radius: 10px;
                    padding: 15px;
                }
                QFrame:hover {
                    background-color: #1e40af;
                }
            """)
        else:
            card.setStyleSheet("""
                QFrame {
                    background-color: #1f2937;
                    border: 2px solid #374151;
                    border-radius: 10px;
                    padding: 15px;
                }
                QFrame:hover {
                    background-color: #374151;
                    cursor: pointer;
                }
            """)
        
        card.setFixedHeight(80)
        card.mousePressEvent = lambda event: self._connect_to_network(network)
        
        layout = QHBoxLayout(card)
        layout.setSpacing(15)
        
        # Network info (left side)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        # SSID with security icon
        ssid_layout = QHBoxLayout()
        ssid_layout.setSpacing(10)
        
        # Security icon
        if network['security'] != 'Open':
            security_icon = QLabel("[Lock]")
            security_icon.setStyleSheet("color: #fbbf24; font-size: 16px;")
            ssid_layout.addWidget(security_icon)
        else:
            public_label = QLabel("[Public]")
            public_label.setStyleSheet("color: #10b981; font-size: 14px;")
            ssid_layout.addWidget(public_label)
        
        ssid_label = QLabel(network['ssid'])
        ssid_label.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 600;")
        ssid_layout.addWidget(ssid_label)
        
        if network['active']:
            checkmark = QLabel("[Connected]")
            checkmark.setStyleSheet("color: #10b981; font-size: 14px; font-weight: 600;")
            ssid_layout.addWidget(checkmark)
        
        ssid_layout.addStretch()
        info_layout.addLayout(ssid_layout)
        
        # Security type
        security_label = QLabel(f"Security: {network['security']}")
        security_label.setStyleSheet("color: #9ca3af; font-size: 14px;")
        info_layout.addWidget(security_label)
        
        layout.addLayout(info_layout, stretch=1)
        
        # Signal strength (right side)
        signal_layout = QVBoxLayout()
        signal_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        signal_label = QLabel(f"{network['signal']}%")
        signal_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        signal_layout.addWidget(signal_label, alignment=Qt.AlignRight)
        
        # Visual signal strength indicator
        signal_strength = self._get_signal_strength_text(network['signal'])
        strength_label = QLabel(signal_strength)
        strength_label.setStyleSheet("color: #9ca3af; font-size: 14px;")
        signal_layout.addWidget(strength_label, alignment=Qt.AlignRight)
        
        layout.addLayout(signal_layout)
        
        return card
    
    def _get_signal_strength_text(self, signal):
        """Convert signal percentage to text description"""
        try:
            signal_int = int(signal)
            if signal_int >= 75:
                return "Excellent"
            elif signal_int >= 50:
                return "Good"
            elif signal_int >= 25:
                return "Fair"
            else:
                return "Weak"
        except ValueError:
            return "Unknown"
    
    def _connect_to_network(self, network):
        """Handle network connection request"""
        if network['active']:
            print(f"[INFO] Already connected to {network['ssid']}")
            return
        
        print(f"[INFO] Attempting to connect to {network['ssid']}")
        # TODO: Implement connection dialog with password input
        # For now, just show that the network was clicked
        print(f"[TODO] Connection dialog for {network['ssid']} (security: {network['security']})")
    
    def _show_advanced_settings(self):
        """Show advanced network settings"""
        print("[INFO] Advanced network settings clicked")
        # TODO: Implement advanced settings dialog
        print("[TODO] Advanced network settings dialog")


# Standalone test
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    widget = NetworkSettingsWidget()
    widget.setStyleSheet("background-color: #0a0a0a;")
    widget.setWindowTitle("Network Settings Test")
    widget.setGeometry(100, 100, 800, 600)
    widget.show()
    
    sys.exit(app.exec_())
