# DeadStream - Grateful Dead Concert Player

A dedicated Raspberry Pi device for streaming Grateful Dead concerts from the Internet Archive.

## Hardware

- Raspberry Pi 4 Model B (4GB RAM)
- 7" Touchscreen Display (landscape orientation)
- IQaudio DAC Pro
- Custom 3D-printed enclosure

## Software Stack

- **OS:** Raspberry Pi OS Desktop (64-bit)
- **Language:** Python 3.13+
- **UI Framework:** PyQt5
- **Audio:** VLC (python-vlc)
- **Database:** SQLite
- **Data Source:** Internet Archive (archive.org)

## Features (Planned)

- Stream 15,000+ Grateful Dead concerts
- Browse by date, venue, year, or curated lists
- "On This Day" in Dead history
- Automatic selection of best recording quality
- Touch-friendly interface optimized for 7" screen
- High-quality audio output via DAC

## Documents Overview

### 00-api-analysis.md
Complete analysis of the Internet Archive API, including:
- How the API works
- What data is available
- Implementation strategies
- Update mechanisms
- Example API calls and responses

**Read this first** to understand the data source.

### 01-project-charter.md
The project's mission, goals, and philosophy:
- What we're building and why
- Learning objectives
- Success criteria
- Development approach
- Timeline expectations

**Read this second** to understand the project scope.

### 02-github-structure.md
Complete repository organization plan:
- Folder structure
- Branching strategy
- Commit message conventions
- .gitignore configuration

**Use this** when setting up your repository.

### 03-learning-roadmap.md
Phase-by-phase breakdown of the entire project:
- 13 phases from foundation to completion
- Learning topics for each phase
- Specific tasks with checkboxes
- Deliverables and time estimates

**This is your roadmap** - bookmark it!

### 04-instruction-template.md
How to request help for specific tasks:
- Template for asking questions
- What to expect in responses
- Tips for effective learning
- Example learning sessions

**Use this** when you're ready to start a new phase or task.

### 05-technical-decisions.md
Complete record of all technical choices:
- Hardware specifications
- Software stack
- Architecture patterns
- Why we chose what we chose
- Alternatives considered
- Performance targets

**Reference this** when making implementation decisions.

### ui-design-specification.md
Complete user interface design specification:
- All screen layouts and wireframes
- Detailed component specifications
- Color scheme and visual design
- Navigation flows and interactions
- Features included in v1.0 vs deferred
- Implementation notes for PyQt5 conversion

**Essential for Phase 6+** when building the user interface.

## How to Use These Documents

### For Project Setup
1. Read `00-api-analysis.md` to understand the data
2. Read `01-project-charter.md` to align on goals
3. Use `02-github-structure.md` to create your repository
4. Review `05-technical-decisions.md` for the tech stack
5. Review `ui-design-specification.md` to understand the UI vision

### For Development
1. Check `03-learning-roadmap.md` to see your current phase
2. Use `04-instruction-template.md` to request specific help
3. Reference `ui-design-specification.md` when building UI components (Phase 6+)
4. Document your own learning in the repository's `/docs/learning-notes/` folder
5. Update `05-technical-decisions.md` when you make significant choices

### For Troubleshooting
- Check `05-technical-decisions.md` for "Why we chose X"
- Review `00-api-analysis.md` for API-related issues
- Look at the roadmap for prerequisite phases you may have skipped

## Project Progress

### Completed Phases

**Phase 1: Foundation & Setup** (Complete - Dec 18, 2025)
- See: `phase-1-completion-summary.md`
- Raspberry Pi environment established
- All development tools installed and tested
- Zero critical issues

**Phase 2: Internet Archive API Mastery** (Complete - Dec 20, 2025)
- See: `phase-2-completion-summary.md`
- Complete API interaction layer
- Production-ready error handling and rate limiting
- All tests passing

**Phase 3: Database Foundation** (Complete - Dec 21, 2025)
- See: `phase-3-completion-summary.md`
- 12,268 shows catalogued with 99.5% data quality
- 20+ query functions implemented
- Update mechanism working

**Phase 4: Audio Playback Engine** (Complete - Dec 23, 2025)
- See: `phase-4-completion-summary.md`
- VLC-based streaming with network resilience
- Position tracking and volume control
- All playback controls implemented

**Phase 5: Smart Show Selection** (Complete - Dec 24, 2025)
- See: `phase-5-completion-summary.md`
- Intelligent recording scoring algorithm
- User preference system with presets
- Manual override capability
- All tests passing, production-ready

**Phase 6: Basic UI Framework** (Complete - Dec 25, 2025)
- See: `phase-6-completion-summary.md`
- PyQt5 UI framework established
- Touch-responsive navigation system
- Screen transitions with animations
- Comprehensive keyboard shortcuts

**Current Phase:** Phase 7 - Player Screen (Starting)
- [x] 7.1: Design player screen layout
- [x] 7.2: Display show information
- [x] 7.3: Show current track info
- [x] 7.4: Implement playback controls
- [ ] 7.5: Add progress bar
- [ ] 7.6: Implement volume control
- [ ] 7.7: Test full integration

### Next Phases
- Phase 8: Playback interface
- Phase 9: Integration and testing

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Concert recordings courtesy of the Internet Archive
- Thanks to all the tapers who preserved these performances