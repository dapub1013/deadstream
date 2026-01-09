#!/bin/bash
# Phase 10 Integration Test Runner
# Quick script to run all Phase 10 pre-hardware tests

set -e  # Exit on error

echo "======================================================================"
echo "  DeadStream - Phase 10 Pre-Hardware Test Suite"
echo "======================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if in project root
if [ ! -f "src/ui/main_window.py" ]; then
    echo -e "${RED}[ERROR]${NC} Must run from project root directory"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}[WARN]${NC} Virtual environment not activated"
    echo "[INFO] Attempting to activate venv..."

    if [ -d "venv" ]; then
        source venv/bin/activate
        echo -e "${GREEN}[PASS]${NC} Virtual environment activated"
    else
        echo -e "${RED}[ERROR]${NC} Virtual environment not found"
        echo "[INFO] Create one with: python3 -m venv venv"
        exit 1
    fi
fi

# Check for required dependencies
echo "[INFO] Checking dependencies..."

python3 -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} PyQt5 not installed"
    echo "[INFO] Install with: pip install PyQt5"
    exit 1
fi

echo -e "${GREEN}[PASS]${NC} Dependencies OK"
echo ""

# Run the integration test suite
echo "======================================================================"
echo "  Running Automated Test Suite"
echo "======================================================================"
echo ""

python3 tests/phase_10_integration_test.py
TEST_EXIT_CODE=$?

echo ""
echo "======================================================================"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}[PASS]${NC} All automated tests passed!"
    echo ""
    echo "[INFO] Next steps:"
    echo "  1. Complete manual test checklist: docs/phase-10-test-checklist.md"
    echo "  2. Test on Raspberry Pi hardware"
    echo "  3. If all tests pass, ready for Phase 11"
    echo ""
    exit 0
else
    echo -e "${RED}[FAIL]${NC} Some tests failed"
    echo ""
    echo "[INFO] Fix failing tests before proceeding to Phase 11"
    echo "[INFO] Review test output above for details"
    echo ""
    exit 1
fi
