# Virtual Environment Usage Guide

## What is a Virtual Environment?

A virtual environment is an isolated Python environment that keeps your project's dependencies separate from your system Python and other projects. Think of it like a separate "container" for your project that has its own Python packages installed.

## Why Use a Virtual Environment?

1. **Isolation**: Each project can have different versions of packages without conflicts
2. **Reproducibility**: Easy to recreate the exact same environment on another machine
3. **Clean**: Doesn't clutter your system Python with project-specific packages
4. **Safety**: If something breaks, it only affects this project, not your whole system

## Basic Commands

### Activate the Virtual Environment
```bash
# From your project directory (~/deadstream)
source venv/bin/activate

# Alternative syntax (also works)
. venv/bin/activate
```

**What this does:** Changes your shell so that when you type `python3` or `pip`, it uses the versions inside `venv/` instead of the system versions.

**You'll know it's activated when** your terminal prompt shows `(venv)` at the beginning:
```
(venv) pi@raspberrypi:~/deadstream $
```

### Deactivate the Virtual Environment
```bash
deactivate
```

**What this does:** Returns your shell to using the system Python. The `(venv)` prefix disappears.

### Check Which Python You're Using
```bash
which python3
```

- **Inside venv:** `/home/pi/deadstream/venv/bin/python3`
- **Outside venv:** `/usr/bin/python3`

## Working with Packages

### Install a Single Package
```bash
# Make sure venv is activated first!
pip install package_name
```

### Install All Requirements
```bash
# From project directory with venv activated
pip install -r requirements.txt
```

### See What's Installed
```bash
pip list
```

### Save Current Environment
```bash
pip freeze > requirements.txt
```

**Note:** We already have a requirements.txt, so you usually won't need this command. It's useful if you add new packages and want to update the file.

## Daily Workflow

### Starting Work on DeadStream
```bash
cd ~/deadstream
source venv/bin/activate
# Now you can run your Python scripts
python3 src/main.py
```

### Finishing Work
```bash
deactivate
# Or just close the terminal
```

## Important Tips

### DO's ✓
- **Always activate the venv** before running Python code or installing packages
- **Keep venv/ in .gitignore** (it's already there - never commit this to git)
- **Commit requirements.txt** so others can recreate your environment
- **Verify you're in venv** with `which python3` if unsure

### DON'Ts ✗
- **Don't install packages without activating venv** - they'll go to system Python
- **Don't commit the venv/ folder to git** - it's huge and machine-specific
- **Don't manually edit files in venv/** - let pip manage it
- **Don't use sudo with pip** in a virtual environment

## Troubleshooting

### "Command not found: pip"
- Make sure venv is activated: `source venv/bin/activate`
- If still failing, use: `python3 -m pip install package_name`

### "Permission denied" when installing packages
- Make sure you're in the venv (check for `(venv)` in prompt)
- **Never use `sudo pip`** inside a venv - you shouldn't need sudo

### Forgot to activate venv and installed globally
```bash
# Remove the package from system (if you can)
sudo pip uninstall package_name

# Activate venv and install properly
source venv/bin/activate
pip install package_name
```

### Need to recreate venv from scratch
```bash
# Deactivate if currently active
deactivate

# Remove old venv
rm -rf venv

# Create fresh venv
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install everything
pip install --upgrade pip
pip install -r requirements.txt
```

## What's in the venv/ Folder?
```
venv/
├── bin/          # Executables (python3, pip, activate script)
├── include/      # C headers for compiling Python extensions
├── lib/          # Installed packages live here
│   └── python3.13/
│       └── site-packages/  # All your pip-installed packages
└── pyvenv.cfg    # Configuration file
```

**Important:** This folder is auto-generated and should never be edited manually or committed to git.

## Integration with Your Editor

### VS Code
VS Code should auto-detect the venv. If not:
1. Open Command Palette (Ctrl+Shift+P)
2. Type "Python: Select Interpreter"
3. Choose `./venv/bin/python3`

### Other Editors
Point your editor to: `/home/pi/deadstream/venv/bin/python3`

## Verification Checklist

After setting up venv, verify:
- [ ] `which python3` shows venv path
- [ ] `python3 --version` shows correct version
- [ ] `pip list` shows installed packages (PyQt5, python-vlc, etc.)
- [ ] `python3 -c "from PyQt5.QtWidgets import QApplication"` works
- [ ] `python3 -c "import vlc"` works

## Quick Reference Card
```bash
# Activate (start working)
source venv/bin/activate

# Deactivate (stop working)
deactivate

# Install packages
pip install package_name

# Check installed packages
pip list

# Verify you're in venv
which python3

# Run your Python scripts
python3 your_script.py
```

---

**Remember:** Always activate the venv before working on the project!

🎸⚡💀🌹
