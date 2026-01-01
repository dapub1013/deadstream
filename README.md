# DeadStream

A dedicated Raspberry Pi device for streaming Grateful Dead concerts from the Internet Archive.

![Project Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What is DeadStream?

DeadStream is a purpose-built music player for Deadheads, designed to bring the magic of the Grateful Dead's live performances into your home with a simple, beautiful interface. Stream over 12,000 concerts from the Internet Archive's collection on a dedicated Raspberry Pi device with a touchscreen interface and high-quality audio output.

### Key Features

🎸 **12,000+ Concerts** - Access the complete Internet Archive Grateful Dead collection  
🎯 **Smart Recording Selection** - Automatically chooses the best available recording quality  
📅 **Browse by Date, Venue, or Year** - Find shows your way  
⭐ **Top Rated Shows** - Discover community favorites  
🎲 **Random Show** - Let fate choose your next listening session  
🔊 **Audiophile-Grade Audio** - High-quality DAC for the best sound  
👆 **Touch-Friendly Interface** - Designed for 7" touchscreen  
🌐 **Network Resilient** - Handles interruptions gracefully with automatic recovery  

---

## Hardware Requirements

### Core Components
- **Raspberry Pi 4 Model B** (2GB RAM minimum, 4GB recommended)
- **Official 7" Touchscreen Display** (800x480 resolution)
- **IQaudio DAC Pro** or similar high-quality DAC
- **MicroSD Card** (32GB minimum, 64GB recommended)
- **Power Supply** (Official Raspberry Pi 4 power supply recommended)

### Optional Components
- **Custom 3D-Printed Case** (STL files included in `/hardware/`)
- **Speakers** or amplifier for audio output
- **Ethernet Cable** (for more reliable streaming than Wi-Fi)

---

## Software Stack

- **Operating System:** Raspberry Pi OS Desktop (64-bit)
- **Programming Language:** Python 3.9+
- **UI Framework:** PyQt5
- **Audio Engine:** VLC (python-vlc bindings)
- **Database:** SQLite
- **Data Source:** Internet Archive API

---

## Installation

### Quick Start (Automated)

```bash
# Clone the repository
git clone https://github.com/yourusername/deadstream.git
cd deadstream

# Run the installation script
./scripts/install.sh
```

The installation script will:
- Install system dependencies (Python, PyQt5, VLC, SQLite)
- Create a Python virtual environment
- Install Python packages
- Download the show database from Internet Archive
- Configure audio settings for your DAC
- Set up automatic startup (optional)

### Manual Installation

See [docs/installation-guide.md](docs/installation-guide.md) for detailed step-by-step instructions.

---

## Usage

### Starting DeadStream

```bash
cd ~/deadstream
source venv/bin/activate
python3 src/ui/main_window.py
```

### Basic Navigation

- **Browse Screen** - Tap a browse mode (Top Rated, Date, Venue, Year, Search, Random)
- **Show List** - Scroll and tap a show to play
- **Now Playing** - Control playback, see show info
- **Settings** - Configure network, audio, and display preferences

### Browse Modes

**Top Rated** - Shows sorted by community ratings from archive.org  
**Date** - Browse by performance date (chronologically)  
**Venue** - Browse by venue name (alphabetically)  
**Year** - Browse by year (1965-1995)  
**Search** - Search by date, venue, or year  
**Random Show** - Instant playback of a randomly selected show  

---

## Configuration

### First-Time Setup

1. **Network Configuration**
   - Connect to Wi-Fi or Ethernet
   - Settings → Network → Configure

2. **Audio Settings**
   - Select your DAC output device
   - Settings → Audio → Device Selection
   - Adjust buffer size if experiencing dropouts

3. **Display Settings**
   - Adjust brightness for your environment
   - Settings → Display → Brightness

### Advanced Configuration

Edit `config/user_config.yaml` for advanced settings:

```yaml
audio:
  output_device: "DAC"
  buffer_size: 5000
  
network:
  prefer_ethernet: true
  retry_attempts: 3
  
show_selection:
  prefer_soundboard: true
  minimum_rating: 3.0
```

---

## Database

### Initial Database Download

The installation script automatically downloads the show database (~150MB). To manually update:

```bash
python3 scripts/update_database.py
```

### Database Statistics

- **Total Shows:** 12,268
- **Date Range:** 1965-1995
- **Average Recordings per Show:** 3.2
- **Database Size:** ~150MB
- **Update Frequency:** Monthly (check for new additions)

---

## Development

### Project Structure

```
deadstream/
├── src/              # Source code
│   ├── api/          # Internet Archive API
│   ├── audio/        # Audio playback engine
│   ├── database/     # SQLite database management
│   ├── ui/           # PyQt5 user interface
│   └── utils/        # Utility functions
├── tests/            # Test suite
├── scripts/          # Utility scripts
├── config/           # Configuration files
├── docs/             # Documentation
└── hardware/         # 3D models and schematics
```

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_api.py

# Run with coverage
python3 -m pytest --cov=src tests/
```

### Contributing

This is currently a personal learning project, but suggestions and bug reports are welcome! Please open an issue to discuss proposed changes.

---

## Roadmap

### Current Status: Phase 9 (Integration & Polish)

✅ **Completed Phases:**
- Phase 1: Foundation & Development Environment
- Phase 2: Internet Archive API Integration
- Phase 3: Database Design & Population
- Phase 4: Smart Show Selection Algorithms
- Phase 5: Audio Playback Engine
- Phase 6: PyQt5 UI Framework
- Phase 7: Browse Interface Implementation
- Phase 8: Settings Screen Implementation

🚧 **In Progress:**
- Phase 9: Integration & Polish

📋 **Upcoming:**
- Phase 10: Now Playing Screen
- Phase 11: Hardware Integration (Touchscreen + DAC)
- Phase 12: Case Design & Assembly
- Phase 13: Testing, Documentation & Release

See [docs/roadmap.md](docs/roadmap.md) for detailed phase breakdowns.

---

## Documentation

- **[Installation Guide](docs/installation-guide.md)** - Detailed setup instructions
- **[User Guide](docs/user-guide.md)** - How to use DeadStream
- **[Hardware Guide](docs/hardware-guide.md)** - Assembly instructions
- **[API Documentation](docs/api-documentation.md)** - Internet Archive API notes
- **[Development Guide](docs/development-guide.md)** - For contributors
- **[Design Decisions](docs/design-decisions.md)** - Why we built it this way

---

## Credits & Acknowledgments

### Data Source
- **Internet Archive** - For preserving and providing access to the Grateful Dead's live performances
- **Grateful Dead Archive** - For the incredible taping community and decades of recordings

### Technology
- **Raspberry Pi Foundation** - For creating accessible, powerful hardware
- **Python Software Foundation** - For the Python programming language
- **Qt Project** - For the PyQt5 framework
- **VideoLAN** - For VLC media player

### Inspiration
- The **Grateful Dead taping community** - For decades of dedication to preserving live music
- **Deadheads everywhere** - For keeping the music alive

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Note on Content
This software provides access to publicly available recordings from the Internet Archive. All Grateful Dead recordings accessed through this application are from the Archive's public collection and are used in accordance with the Grateful Dead's long-standing taping policy.

---

## Support

Having issues? Found a bug? Have a feature request?

- **Issues:** [GitHub Issues](https://github.com/yourusername/deadstream/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/deadstream/discussions)
- **Email:** your.email@example.com

---

## Project Status

DeadStream is under active development as a learning project. Features and functionality are being added systematically through a phased approach. Check the [CHANGELOG.md](CHANGELOG.md) for recent updates.

**Current Version:** 0.9.0 (Pre-Release)  
**Target Release:** 1.0.0 (Q2 2025)

---

*Built with ❤️ for the Deadhead community*

⚡💀🌹
