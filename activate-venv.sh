#!/bin/bash
# DeadStream Virtual Environment Activation Script
# 
# Usage: source activate-venv.sh
# (Note: Must use 'source' or '.' to activate in current shell)

echo "🎸 Activating DeadStream Virtual Environment..."
source venv/bin/activate

echo ""
echo "✅ Virtual environment activated (with system site-packages)!"
echo ""
echo "📍 Python location: $(which python3)"
echo "🐍 Python version: $(python3 --version)"
echo "📦 Pip version: $(pip --version | cut -d' ' -f1-2)"
echo ""
echo "💿 Key packages available:"
echo "   - PyQt5 (system package)"
echo "   - python-vlc (system package)"
pip list --format=columns | grep -E "requests|PyYAML|pytest"
echo ""
echo "📝 To deactivate when done: deactivate"
echo ""
echo "⚡💀🌹 Ready to code!"
