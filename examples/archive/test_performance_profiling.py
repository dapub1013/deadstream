#!/usr/bin/env python3
"""
DeadStream Performance Profiling Suite
Phase 10, Task 10.6: Performance Profiling and Optimization

Measures and profiles:
1. Application startup time
2. Screen transition performance
3. Memory usage over time
4. Database query performance
5. UI responsiveness
6. Playback buffer performance

Target Platform: Raspberry Pi 4 (4GB RAM)
Development Platform: macOS (for baseline)
"""

import sys
import os
import time
import psutil
from datetime import datetime

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import QTimer

from src.ui.main_window import MainWindow
from src.database.queries import get_top_rated_shows, get_show_by_date
from src.settings import get_settings


class PerformanceProfiler:
    """Performance profiling and benchmarking tool"""

    def __init__(self):
        self.results = {}
        self.process = psutil.Process()
        self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB

    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)

    def measure_time(self, name, func, *args, **kwargs):
        """Measure execution time of a function"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000  # Convert to ms

        self.results[name] = {
            'time_ms': elapsed,
            'result': result
        }

        return result, elapsed

    def get_memory_usage(self):
        """Get current memory usage in MB"""
        return self.process.memory_info().rss / 1024 / 1024

    def get_cpu_percent(self):
        """Get current CPU usage percentage"""
        return self.process.cpu_percent(interval=0.1)

    def print_metric(self, name, value, unit="ms", status=None):
        """Print a performance metric"""
        if status is None:
            # Auto-determine status based on common thresholds
            if unit == "ms":
                if value < 100:
                    status = "EXCELLENT"
                elif value < 500:
                    status = "GOOD"
                elif value < 1000:
                    status = "ACCEPTABLE"
                else:
                    status = "SLOW"

        status_symbol = {
            "EXCELLENT": "✓✓",
            "GOOD": "✓",
            "ACCEPTABLE": "~",
            "SLOW": "✗",
            "PASS": "✓",
            "FAIL": "✗"
        }.get(status, " ")

        print(f"  [{status_symbol}] {name}: {value:.2f} {unit} ({status})")

    # ========================================================================
    # TEST 1: Application Startup Performance
    # ========================================================================

    def test_startup_performance(self, app):
        """Measure application startup time"""
        self.print_header("TEST 1: APPLICATION STARTUP PERFORMANCE")

        print("\n[TEST] Measuring startup components...")

        # Measure total startup
        def create_window():
            window = MainWindow()
            window.show()
            QTest.qWait(700)  # Wait for initial screen transition
            return window

        window, startup_time = self.measure_time("Total Startup", create_window)

        # Print results
        print("\nStartup Breakdown:")
        self.print_metric("Total startup time", startup_time)

        # Target: < 2000ms on Raspberry Pi, < 1000ms on desktop
        target = 2000
        if startup_time < target:
            print(f"\n✓ Startup time meets target (< {target}ms)")
        else:
            print(f"\n✗ Startup time exceeds target ({startup_time:.0f}ms > {target}ms)")

        return window

    # ========================================================================
    # TEST 2: Screen Transition Performance
    # ========================================================================

    def test_screen_transitions(self, window):
        """Measure screen transition performance"""
        self.print_header("TEST 2: SCREEN TRANSITION PERFORMANCE")

        transitions = []

        # Browse → Settings
        start = time.perf_counter()
        window.show_settings()
        QTest.qWait(350)  # Wait for 300ms animation + buffer
        transitions.append(("Browse → Settings", (time.perf_counter() - start) * 1000))

        # Settings → Browse
        start = time.perf_counter()
        window.show_browse()
        QTest.qWait(350)
        transitions.append(("Settings → Browse", (time.perf_counter() - start) * 1000))

        # Browse → Player
        start = time.perf_counter()
        window.show_player()
        QTest.qWait(350)
        transitions.append(("Browse → Player", (time.perf_counter() - start) * 1000))

        # Player → Browse
        start = time.perf_counter()
        window.show_browse()
        QTest.qWait(350)
        transitions.append(("Player → Browse", (time.perf_counter() - start) * 1000))

        # Print results
        print("\nTransition Times:")
        total_time = 0
        for name, elapsed in transitions:
            self.print_metric(name, elapsed)
            total_time += elapsed

        avg_time = total_time / len(transitions)
        self.print_metric("Average transition", avg_time)

        # Target: < 400ms (300ms animation + 100ms overhead)
        if avg_time < 400:
            print(f"\n✓ Transitions are smooth (avg {avg_time:.0f}ms)")
        else:
            print(f"\n✗ Transitions may feel sluggish (avg {avg_time:.0f}ms)")

    # ========================================================================
    # TEST 3: Memory Usage Profile
    # ========================================================================

    def test_memory_usage(self, window):
        """Profile memory usage"""
        self.print_header("TEST 3: MEMORY USAGE PROFILE")

        print("\n[TEST] Measuring memory footprint...")

        # Initial memory
        initial_mem = self.get_memory_usage()
        print(f"\nInitial memory: {initial_mem:.2f} MB")

        # Navigate through all screens multiple times
        print("\nNavigating through screens...")
        for i in range(3):
            window.show_browse()
            QTest.qWait(350)
            window.show_settings()
            QTest.qWait(350)
            window.show_player()
            QTest.qWait(350)

        # Final memory
        final_mem = self.get_memory_usage()
        memory_increase = final_mem - initial_mem

        print(f"\nMemory after navigation cycles:")
        print(f"  Current memory: {final_mem:.2f} MB")
        print(f"  Memory increase: {memory_increase:.2f} MB")
        print(f"  Total from start: {final_mem - self.start_memory:.2f} MB")

        # Target: < 20MB increase (memory leak check)
        if memory_increase < 20:
            print(f"\n✓ No significant memory leaks detected")
        else:
            print(f"\n✗ Possible memory leak (increased {memory_increase:.2f}MB)")

        return final_mem

    # ========================================================================
    # TEST 4: Database Query Performance
    # ========================================================================

    def test_database_performance(self):
        """Profile database query performance"""
        self.print_header("TEST 4: DATABASE QUERY PERFORMANCE")

        print("\n[TEST] Measuring database query times...")

        # Test 1: Get top rated shows
        def query_top_rated():
            return get_top_rated_shows(limit=50)

        shows, query_time = self.measure_time("Top Rated Shows (50)", query_top_rated)
        self.print_metric("Query: Top 50 shows", query_time)

        # Test 2: Get specific date
        def query_by_date():
            return get_show_by_date('1977-05-08')

        date_shows, date_time = self.measure_time("Query by Date", query_by_date)
        self.print_metric("Query: Shows by date", date_time)

        # Test 3: Multiple sequential queries
        start = time.perf_counter()
        for _ in range(10):
            get_top_rated_shows(limit=10)
        multi_time = (time.perf_counter() - start) * 1000
        self.print_metric("10 sequential queries", multi_time)

        avg_query_time = multi_time / 10
        self.print_metric("Average query time", avg_query_time)

        # Target: < 100ms for typical queries
        if avg_query_time < 100:
            print(f"\n✓ Database queries are fast (avg {avg_query_time:.2f}ms)")
        else:
            print(f"\n✗ Database queries are slow (avg {avg_query_time:.2f}ms)")

    # ========================================================================
    # TEST 5: UI Responsiveness
    # ========================================================================

    def test_ui_responsiveness(self, window):
        """Test UI responsiveness during operations"""
        self.print_header("TEST 5: UI RESPONSIVENESS")

        print("\n[TEST] Testing UI during heavy operations...")

        # Measure CPU usage during screen transitions
        window.show_browse()
        QTest.qWait(50)

        cpu_samples = []
        for _ in range(5):
            window.show_settings()
            QTest.qWait(50)
            cpu = self.get_cpu_percent()
            cpu_samples.append(cpu)

            window.show_browse()
            QTest.qWait(50)
            cpu = self.get_cpu_percent()
            cpu_samples.append(cpu)

        avg_cpu = sum(cpu_samples) / len(cpu_samples)
        max_cpu = max(cpu_samples)

        print(f"\nCPU Usage during transitions:")
        print(f"  Average: {avg_cpu:.1f}%")
        print(f"  Peak: {max_cpu:.1f}%")

        # Target: < 50% average CPU on Raspberry Pi
        if avg_cpu < 50:
            print(f"\n✓ CPU usage is reasonable (avg {avg_cpu:.1f}%)")
        else:
            print(f"\n~ CPU usage is high (avg {avg_cpu:.1f}%)")

    # ========================================================================
    # TEST 6: Settings Performance
    # ========================================================================

    def test_settings_performance(self):
        """Test settings load/save performance"""
        self.print_header("TEST 6: SETTINGS PERFORMANCE")

        print("\n[TEST] Measuring settings operations...")

        settings = get_settings()

        # Test setting read
        start = time.perf_counter()
        for _ in range(100):
            _ = settings.get('audio', 'default_volume', 77)
        read_time = (time.perf_counter() - start) * 1000

        self.print_metric("100 settings reads", read_time)
        self.print_metric("Avg read time", read_time / 100)

        # Test setting write
        start = time.perf_counter()
        for i in range(10):
            settings.set('audio', 'default_volume', 70 + i)
        write_time = (time.perf_counter() - start) * 1000

        self.print_metric("10 settings writes", write_time)
        self.print_metric("Avg write time", write_time / 10)

        # Restore original value
        settings.set('audio', 'default_volume', 80)

        # Target: < 1ms for reads, < 50ms for writes
        if (read_time / 100) < 1 and (write_time / 10) < 50:
            print(f"\n✓ Settings operations are fast")
        else:
            print(f"\n~ Settings operations could be optimized")

    # ========================================================================
    # RUN ALL TESTS
    # ========================================================================

    def run_all_tests(self, app):
        """Run complete performance profiling suite"""
        self.print_header("DEADSTREAM PERFORMANCE PROFILING SUITE")
        print("Phase 10, Task 10.6: Performance Analysis")
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Platform: {sys.platform}")
        print(f"Python: {sys.version.split()[0]}")

        # System info
        print(f"\nSystem Information:")
        print(f"  CPU Count: {psutil.cpu_count()}")
        print(f"  Total RAM: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f} GB")
        print(f"  Available RAM: {psutil.virtual_memory().available / 1024 / 1024 / 1024:.1f} GB")

        # Run tests
        window = self.test_startup_performance(app)
        self.test_screen_transitions(window)
        final_mem = self.test_memory_usage(window)
        self.test_database_performance()
        self.test_ui_responsiveness(window)
        self.test_settings_performance()

        # Final summary
        self.print_header("PERFORMANCE SUMMARY")

        print("\nKey Metrics:")
        startup = self.results.get("Total Startup", {}).get('time_ms', 0)
        print(f"  Startup Time: {startup:.0f}ms")
        print(f"  Memory Usage: {final_mem:.1f}MB")
        print(f"  Memory Growth: {final_mem - self.start_memory:.1f}MB")

        print("\nTarget Specifications (Raspberry Pi 4):")
        print("  ✓ Startup: < 2000ms")
        print("  ✓ Screen Transitions: < 400ms")
        print("  ✓ Memory Usage: < 200MB")
        print("  ✓ Database Queries: < 100ms")
        print("  ✓ CPU Usage: < 50%")

        print("\nPerformance Rating:")
        if startup < 2000 and final_mem < 200:
            print("  EXCELLENT - Ready for Raspberry Pi deployment")
        elif startup < 3000 and final_mem < 300:
            print("  GOOD - Should work well on Raspberry Pi")
        else:
            print("  NEEDS OPTIMIZATION - May struggle on Raspberry Pi")

        print("\n" + "=" * 70)
        print("Performance profiling complete!")
        print("Window will close in 2 seconds...")
        print("=" * 70)

        return window


def main():
    """Main test entry point"""
    app = QApplication(sys.argv)

    profiler = PerformanceProfiler()
    window = profiler.run_all_tests(app)

    # Auto-close after 2 seconds
    QTimer.singleShot(2000, app.quit)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
