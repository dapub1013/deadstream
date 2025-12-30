#!/usr/bin/env python3
"""
DeadStream Phase 8 Test Launcher
Task 8.8: Interactive test menu for integration testing

Provides easy access to all Phase 8 tests:
- Automated integration tests
- Individual component tests
- Visual inspection mode
"""

import sys
import os
import subprocess

PROJECT_ROOT = '/home/david/deadstream'


def print_header():
    """Print the test menu header"""
    print("\n" + "="*70)
    print(" "*15 + "DeadStream Phase 8 Test Suite")
    print(" "*15 + "Settings Screen Integration Testing")
    print("="*70)


def print_menu():
    """Print the main menu"""
    print("\nAvailable Tests:")
    print("  1. Run Full Integration Test Suite (automated)")
    print("  2. Test Settings Persistence Only")
    print("  3. Launch Settings Screen (visual inspection)")
    print("  4. View Manual Testing Checklist")
    print("  5. Test Individual Settings Category")
    print("  6. Run All Tests + Generate Report")
    print("  Q. Quit")
    print()


def run_full_integration_tests():
    """Run the complete automated integration test suite"""
    print("\n" + "-"*70)
    print("Running Full Integration Test Suite...")
    print("-"*70)
    
    test_script = os.path.join(PROJECT_ROOT, 'test_phase8_integration.py')
    
    if not os.path.exists(test_script):
        print(f"[ERROR] Test script not found: {test_script}")
        return
    
    try:
        result = subprocess.run(
            ['python3', test_script],
            cwd=PROJECT_ROOT,
            check=False
        )
        
        if result.returncode == 0:
            print("\n[SUCCESS] All integration tests passed!")
        else:
            print("\n[WARNING] Some tests failed. Review output above.")
            
    except Exception as e:
        print(f"[ERROR] Failed to run tests: {e}")


def test_settings_persistence():
    """Test just the settings persistence functionality"""
    print("\n" + "-"*70)
    print("Testing Settings Persistence...")
    print("-"*70)
    
    sys.path.insert(0, PROJECT_ROOT)
    
    from test_phase8_integration import test_settings_persistence
    
    result = test_settings_persistence()
    
    if result:
        print("\n[SUCCESS] Settings persistence test passed!")
    else:
        print("\n[FAIL] Settings persistence test failed!")


def launch_visual_inspection():
    """Launch the settings screen for visual inspection"""
    print("\n" + "-"*70)
    print("Launching Settings Screen for Visual Inspection...")
    print("-"*70)
    print("The main window will open to the Settings screen.")
    print("Use this to manually inspect the UI and test interactions.")
    print("Close the window when done.")
    print("-"*70 + "\n")
    
    try:
        subprocess.run(
            ['python3', 'src/ui/main_window.py', '--screen=settings'],
            cwd=PROJECT_ROOT
        )
    except Exception as e:
        print(f"[ERROR] Failed to launch visual inspection: {e}")
        print("Try running manually: python3 src/ui/main_window.py")


def view_manual_checklist():
    """Display the manual testing checklist"""
    print("\n" + "-"*70)
    print("Opening Manual Testing Checklist...")
    print("-"*70)
    
    checklist_file = os.path.join(PROJECT_ROOT, 'phase8_manual_testing_checklist.md')
    
    if not os.path.exists(checklist_file):
        print(f"[ERROR] Checklist not found: {checklist_file}")
        return
    
    # Try to open with less, fall back to cat
    try:
        subprocess.run(['less', checklist_file])
    except:
        try:
            with open(checklist_file, 'r') as f:
                print(f.read())
        except Exception as e:
            print(f"[ERROR] Could not read checklist: {e}")


def test_individual_category():
    """Test a specific settings category"""
    print("\n" + "-"*70)
    print("Individual Category Testing")
    print("-"*70)
    print("\nWhich category would you like to test?")
    print("  1. Network Settings")
    print("  2. Audio Settings")
    print("  3. Display Settings")
    print("  4. Date & Time Settings")
    print("  5. About Page")
    print("  B. Back to main menu")
    
    choice = input("\nEnter choice: ").strip().upper()
    
    category_tests = {
        '1': 'test_network_widget.py',
        '2': 'test_audio_widget.py',
        '3': 'test_display_widget.py',
        '4': 'test_datetime_widget.py',
        '5': 'test_about_widget.py'
    }
    
    if choice in category_tests:
        test_file = os.path.join(PROJECT_ROOT, 'examples', category_tests[choice])
        
        if os.path.exists(test_file):
            print(f"\n[INFO] Running {category_tests[choice]}...")
            subprocess.run(['python3', test_file], cwd=PROJECT_ROOT)
        else:
            print(f"[WARN] Test file not found: {test_file}")
            print("This test may not have been created yet.")
    elif choice == 'B':
        return
    else:
        print("[ERROR] Invalid choice")


def run_all_and_report():
    """Run all tests and generate a summary report"""
    print("\n" + "-"*70)
    print("Running All Tests and Generating Report...")
    print("-"*70)
    
    report_file = os.path.join(PROJECT_ROOT, 'phase8_test_report.txt')
    
    print(f"\n[INFO] Test results will be saved to: {report_file}")
    print("[INFO] This may take a minute...\n")
    
    with open(report_file, 'w') as f:
        f.write("DeadStream Phase 8 Integration Test Report\n")
        f.write("="*70 + "\n")
        f.write(f"Generated: {os.popen('date').read()}")
        f.write("="*70 + "\n\n")
        
        f.write("AUTOMATED TESTS\n")
        f.write("-"*70 + "\n")
        
        # Run automated tests and capture output
        test_script = os.path.join(PROJECT_ROOT, 'test_phase8_integration.py')
        if os.path.exists(test_script):
            result = subprocess.run(
                ['python3', test_script],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )
            f.write(result.stdout)
            if result.stderr:
                f.write("\nERRORS:\n")
                f.write(result.stderr)
        else:
            f.write("[ERROR] Integration test script not found\n")
        
        f.write("\n\n")
        f.write("MANUAL TESTING\n")
        f.write("-"*70 + "\n")
        f.write("See: phase8_manual_testing_checklist.md\n")
        f.write("Complete the manual testing checklist and attach results.\n")
        
        f.write("\n\n")
        f.write("END OF REPORT\n")
        f.write("="*70 + "\n")
    
    print(f"[SUCCESS] Report generated: {report_file}")
    print("\nWould you like to view the report now? (y/n): ", end='')
    view = input().strip().lower()
    
    if view == 'y':
        try:
            subprocess.run(['less', report_file])
        except:
            with open(report_file, 'r') as f:
                print(f.read())


def main():
    """Main menu loop"""
    while True:
        print_header()
        print_menu()
        
        choice = input("Enter your choice: ").strip().upper()
        
        if choice == '1':
            run_full_integration_tests()
        elif choice == '2':
            test_settings_persistence()
        elif choice == '3':
            launch_visual_inspection()
        elif choice == '4':
            view_manual_checklist()
        elif choice == '5':
            test_individual_category()
        elif choice == '6':
            run_all_and_report()
        elif choice == 'Q':
            print("\nExiting test launcher. Goodbye!")
            break
        else:
            print("\n[ERROR] Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest launcher interrupted. Goodbye!")
        sys.exit(0)
