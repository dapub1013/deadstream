#!/usr/bin/env python3
"""Simple test to see if random show screen displays"""

import sys
sys.path.insert(0, '.')

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QTimer
from src.ui.screens.randomshow_screen import RandomShowScreen

app = QApplication(sys.argv)

print("[INFO] Creating random show screen...")
try:
    screen = RandomShowScreen()
    screen.setGeometry(100, 100, 800, 600)
    screen.setWindowTitle("Test Random Show Screen")
    screen.show()
    print("[INFO] Screen created and shown")
    print(f"[INFO] Screen size: {screen.width()}x{screen.height()}")
    print(f"[INFO] Has random_show_widget: {hasattr(screen, 'random_show_widget')}")

    if hasattr(screen, 'random_show_widget'):
        widget = screen.random_show_widget
        print(f"[INFO] Widget size: {widget.width()}x{widget.height()}")
        print(f"[INFO] Widget visible: {widget.isVisible()}")

    # Auto-close after 3 seconds
    QTimer.singleShot(3000, app.quit)

    sys.exit(app.exec_())

except Exception as e:
    print(f"[ERROR] Failed: {e}")
    import traceback
    traceback.print_exc()
