#!/usr/bin/env python3
"""
Test Network Settings Widget
Phase 8, Task 8.2: Network settings implementation

Tests the network settings widget standalone.
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from src.ui.widgets.network_settings_widget import NetworkSettingsWidget


def main():
    """Run the network settings widget test"""
    print("[INFO] Starting Network Settings Widget test...")
    print("[INFO] This test displays the network settings interface")
    print("[INFO] Features:")
    print("  - Current WiFi status and connection info")
    print("  - List of available networks")
    print("  - Signal strength indicators")
    print("  - Auto-refresh every 10 seconds")
    print("  - Click networks to connect (TODO)")
    print("")
    print("[INFO] Close the window to exit")
    print("-" * 60)
    
    app = QApplication(sys.argv)
    
    # Create widget
    widget = NetworkSettingsWidget()
    widget.setStyleSheet("background-color: #0a0a0a;")
    widget.setWindowTitle("Network Settings Test - DeadStream")
    widget.setGeometry(100, 100, 800, 600)
    widget.show()
    
    print("[OK] Window displayed")
    print("[INFO] Testing network scanning...")
    
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
