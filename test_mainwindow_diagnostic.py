#!/usr/bin/env python3
"""
Simple diagnostic test for MainWindow screen attributes
"""

import sys
sys.path.insert(0, '/home/david/deadstream')

from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()

print("\n" + "="*60)
print("MainWindow Attribute Diagnostic")
print("="*60)

# Check if attributes exist
attrs_to_check = ['player_screen', 'browse_screen', 'settings_screen', 'screen_manager']

for attr in attrs_to_check:
    if hasattr(window, attr):
        obj = getattr(window, attr)
        print(f"[OK] window.{attr} exists - type: {type(obj).__name__}")
    else:
        print(f"[FAIL] window.{attr} does NOT exist")

# Check screen_manager contents
print("\n" + "-"*60)
print("ScreenManager Screens Dictionary:")
print("-"*60)
if hasattr(window, 'screen_manager'):
    if hasattr(window.screen_manager, 'screens'):
        for name, info in window.screen_manager.screens.items():
            print(f"  {name}: index={info['index']}, widget={type(info['widget']).__name__}")
    else:
        print("[WARN] screen_manager has no 'screens' attribute")
else:
    print("[ERROR] No screen_manager attribute")

print("\n" + "="*60)
print("End of Diagnostic")
print("="*60)
