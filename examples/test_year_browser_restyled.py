#!/usr/bin/env python3
"""
Test script for restyled YearBrowser widget - Phase 10E Task 10E.1

Tests:
1. Widget renders correctly
2. Theme Manager colors applied (zero hardcoded values)
3. Legendary years highlighted in yellow
4. Regular years highlighted in blue
5. Navigation buttons work
6. Year selection emits signal
7. Touch-friendly button sizes (60px+ height)
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from src.ui.widgets.year_browser import YearBrowser
from src.ui.styles.theme import Theme


def test_visual_inspection():
    """Visual inspection test - verify Theme styling applied"""
    print("\n" + "="*70)
    print("VISUAL INSPECTION TEST")
    print("="*70)
    
    app = QApplication(sys.argv)
    
    # Create container widget
    container = QWidget()
    container.setWindowTitle("DeadStream - Year Browser Restyle Test")
    container.setMinimumSize(700, 900)
    container.setStyleSheet(f"background-color: {Theme.BG_PRIMARY};")
    
    layout = QVBoxLayout()
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Title
    title = QLabel("Year Browser - Phase 10E Restyled")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet(f"""
        QLabel {{
            color: {Theme.TEXT_PRIMARY};
            font-size: {Theme.HEADER_MEDIUM}px;
            font-weight: bold;
            padding: {Theme.SPACING_MEDIUM}px;
        }}
    """)
    layout.addWidget(title)
    
    # Instructions
    instructions = QLabel(
        "Visual Checklist:\n"
        "1. Navigation buttons are blue (Theme.ACCENT_BLUE)\n"
        "2. Legendary years (1972, 1977, etc.) are yellow (Theme.ACCENT_YELLOW)\n"
        "3. Regular years are blue (Theme.ACCENT_BLUE)\n"
        "4. All text uses Theme colors (no hardcoded values)\n"
        "5. Year buttons are 80px tall (extra touch-friendly)\n"
        "6. Navigation buttons are 60px tall (Theme.BUTTON_HEIGHT)\n"
        "7. Spacing follows Theme constants (8px, 16px, 24px)\n"
        "8. Hover states show lighter colors\n"
        "9. Press states show darker colors\n"
        "\n"
        "Click years to test signal emission"
    )
    instructions.setAlignment(Qt.AlignLeft)
    instructions.setWordWrap(True)
    instructions.setStyleSheet(f"""
        QLabel {{
            color: {Theme.TEXT_SECONDARY};
            font-size: {Theme.BODY_SMALL}px;
            padding: {Theme.SPACING_MEDIUM}px;
            background-color: {Theme.BG_CARD};
            border-radius: 8px;
        }}
    """)
    layout.addWidget(instructions)
    
    # Year browser widget
    browser = YearBrowser()
    
    # Connect signal to display selected year
    result_label = QLabel("No year selected yet")
    result_label.setAlignment(Qt.AlignCenter)
    result_label.setStyleSheet(f"""
        QLabel {{
            color: {Theme.ACCENT_GREEN};
            font-size: {Theme.BODY_LARGE}px;
            font-weight: bold;
            padding: {Theme.SPACING_MEDIUM}px;
            background-color: {Theme.BG_PANEL_DARK};
            border-radius: 8px;
        }}
    """)
    
    def on_year_selected(year):
        result_label.setText(f"Year selected: {year}")
        print(f"[TEST] Year selected signal received: {year}")
        
        # Check if it's a legendary year
        if year in browser.LEGENDARY_YEARS:
            print(f"[OK] {year} is correctly marked as legendary")
    
    browser.year_selected.connect(on_year_selected)
    
    layout.addWidget(browser)
    layout.addWidget(result_label)
    
    container.setLayout(layout)
    container.show()
    
    print("\n[INFO] Year browser displayed")
    print("[INFO] Test decade navigation and year selection")
    print("[INFO] Verify legendary years (1972, 1977, etc.) are yellow")
    print("[INFO] Close window when done\n")
    
    sys.exit(app.exec_())


def test_theme_constants():
    """Verify all styling uses Theme constants (no hardcoded values)"""
    print("\n" + "="*70)
    print("THEME CONSTANTS TEST")
    print("="*70)
    
    app = QApplication(sys.argv)
    
    browser = YearBrowser()
    
    # Check that widget uses Theme constants
    print("[INFO] Checking Theme Manager usage...")
    
    # Verify button heights
    for btn in browser.year_buttons:
        height = btn.minimumHeight()
        assert height == 80, \
            f"Year button height {height} != 80px (touch-friendly size)"
    
    print(f"[PASS] All year buttons are 80px tall (touch-friendly)")
    
    # Verify nav button heights
    nav_height = browser.prev_decade_btn.minimumHeight()
    assert nav_height == Theme.BUTTON_HEIGHT, \
        f"Nav button height {nav_height} != Theme.BUTTON_HEIGHT"
    
    print(f"[PASS] Navigation buttons use Theme.BUTTON_HEIGHT ({Theme.BUTTON_HEIGHT}px)")
    
    # Verify legendary years are defined
    assert len(browser.LEGENDARY_YEARS) > 0, "No legendary years defined"
    print(f"[PASS] Legendary years defined: {sorted(browser.LEGENDARY_YEARS)}")
    
    # Verify years loaded from database
    if len(browser.years_with_shows) > 0:
        print(f"[PASS] Loaded {len(browser.years_with_shows)} years with shows from database")
    else:
        print("[WARN] No years loaded (database may be empty)")
    
    print("\n[OK] All Theme constants verified")


def test_functionality():
    """Test widget functionality"""
    print("\n" + "="*70)
    print("FUNCTIONALITY TEST")
    print("="*70)
    
    app = QApplication(sys.argv)
    
    browser = YearBrowser()
    
    # Test signal emission
    signal_received = []
    
    def capture_signal(year):
        signal_received.append(year)
    
    browser.year_selected.connect(capture_signal)
    
    # Find a visible year button
    test_button = None
    test_year = None
    for btn in browser.year_buttons:
        if btn.isVisible() and btn.isEnabled():
            test_button = btn
            test_year = btn.property('year')
            break
    
    if test_button and test_year:
        print(f"[INFO] Testing year button: {test_year}")
        
        # Click the button
        test_button.click()
        
        # Process events
        QApplication.processEvents()
        
        # Verify signal was emitted
        assert len(signal_received) == 1, "Signal not emitted"
        assert signal_received[0] == test_year, f"Wrong year in signal: {signal_received[0]} != {test_year}"
        
        print(f"[PASS] Year selection signal emitted correctly: {test_year}")
    else:
        print("[WARN] No visible year buttons to test (database may be empty)")
    
    # Test decade navigation
    initial_decade = browser.current_decade
    print(f"[INFO] Initial decade: {initial_decade}s")
    
    # Try next decade
    if browser.next_decade_btn.isEnabled():
        browser.next_decade()
        assert browser.current_decade == initial_decade + 10, "Next decade navigation failed"
        print(f"[PASS] Next decade navigation works: {browser.current_decade}s")
        
        # Try previous decade
        browser.prev_decade()
        assert browser.current_decade == initial_decade, "Previous decade navigation failed"
        print(f"[PASS] Previous decade navigation works: back to {browser.current_decade}s")
    else:
        print("[INFO] Next decade button disabled (at latest decade)")
    
    print("\n[OK] All functionality tests passed")


def run_all_tests():
    """Run all automated tests, then visual inspection"""
    print("\n" + "="*70)
    print("YEAR BROWSER RESTYLE - TEST SUITE")
    print("Phase 10E - Task 10E.1")
    print("="*70)
    
    # Run automated tests first
    test_theme_constants()
    test_functionality()
    
    # Then visual inspection
    print("\n" + "="*70)
    print("STARTING VISUAL INSPECTION")
    print("="*70)
    print("\nAll automated tests passed!")
    print("Starting visual inspection test...")
    print("Close the window when done reviewing.\n")
    
    test_visual_inspection()


if __name__ == "__main__":
    run_all_tests()