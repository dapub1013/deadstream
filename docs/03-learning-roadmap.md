# Learning Roadmap - Step-by-Step Development

## Philosophy
Each phase builds on the previous. You will:
1. **Learn** the concepts needed
2. **Implement** with guidance and examples
3. **Test** to verify it works
4. **Document** what you learned
5. **Commit** to version control

Do NOT skip ahead. Understanding foundations prevents frustration later.

## Phase 1: Foundation & Setup
**Goal:** Get your development environment ready

### Learning Topics
- Raspberry Pi basics (what it is, how it boots)
- Linux command line fundamentals
- Git basics (clone, commit, push, branch)
- Python virtual environments
- Basic SQLite concepts

### Tasks (with instruction)
- [x] 1.1: Set up Raspberry Pi OS
- [x] 1.2: Install development tools (git, python3, pip)
- [x] 1.3: Create GitHub repository
- [x] 1.4: Clone repository to Pi
- [x] 1.5: Set up Python virtual environment
- [x] 1.6: Test screen functionality
- [x] 1.7: Test audio output (built-in first)

### Deliverables
- Working Pi with SSH access
- GitHub repo initialized
- Python environment configured
- Documentation of setup steps

### Estimated Time
1-2 weeks (depending on hardware arrival)

---

## Phase 2: Internet Archive API Mastery
**Goal:** Understand and interact with the Archive.org API

### Learning Topics
- REST APIs and HTTP requests
- JSON data structures
- Python `requests` library
- Data parsing and validation
- Error handling for network requests

### Tasks (with instruction)
- [x] 2.1: Read Archive.org API documentation
- [x] 2.2: Write simple script to search for one show
- [x] 2.3: Parse and print show metadata
- [x] 2.4: Implement search by date range
- [x] 2.5: Handle API errors gracefully
- [x] 2.6: Understand rate limiting

### Deliverables
- Working API interaction module
- Example scripts in `/examples`
- API documentation in `/docs`
- Unit tests for API functions

### Estimated Time
1-2 weeks

---

## Phase 3: Database Foundation
**Goal:** Build local show catalog system

### Learning Topics
- SQLite database design
- SQL queries (SELECT, INSERT, UPDATE)
- Database schema design
- Python sqlite3 module
- Data normalization

### Tasks (with instruction)
- [x] 3.1: Design database schema
- [x] 3.2: Create tables with proper indexes
- [x] 3.3: Write initial data import script
- [x] 3.4: Download all show metadata (one-time)
- [x] 3.5: Implement query functions
- [x] 3.6: Build update mechanism
- [x] 3.7: Add data validation

### Deliverables
- Complete show database
- Database access layer
- Update script
- Database documentation

### Estimated Time
2-3 weeks

---

## Phase 4: Audio Playback Engine
**Goal:** Actually play music!

### Learning Topics
- Audio formats (MP3, FLAC, OGG)
- Streaming vs downloading
- Python audio libraries (pygame/vlc)
- Playlist management
- Audio state management

### Tasks (with instruction)
- [x] 4.1: Test simple local file playback
- [x] 4.2: Implement URL streaming
- [x] 4.3: Build playlist from setlist
- [x] 4.4: Add play/pause/skip controls
- [x] 4.5: Track playback position
- [x] 4.6: Handle network interruptions
- [x] 4.7: Implement volume control

### Deliverables
- Working audio engine
- Command-line player (no UI yet)
- Playback tests
- Audio troubleshooting guide

### Estimated Time
2-3 weeks

---

## Phase 5: Smart Show Selection ✅ COMPLETE
**Goal:** Pick the best recording automatically

**Status:** COMPLETE (Dec 24, 2025)  
**Duration:** 2 days (70% faster than 1-2 week estimate)

### Learning Topics
- Scoring algorithms ✅
- String matching ✅
- Metadata analysis ✅
- Preference weighting ✅

### Tasks (with instruction)
- [x] 5.1: Analyze recording quality indicators
- [x] 5.2: Build scoring function
- [x] 5.3: Test with multiple versions of same show
- [x] 5.4: Implement user preferences
- [x] 5.5: Add manual override option
- [x] 5.6: Create comparison tool

### Deliverables ✅
- Selection algorithm module (`src/selection/scoring.py`)
- Preference configuration (`src/selection/preferences.py`)
- Show selector (`src/selection/selector.py`)
- Test cases with known good shows
- Documentation of scoring logic
- Comparison tool (`examples/compare_recordings.py`)

### Actual Duration
2 days (vs 1-2 weeks estimated)

### Key Achievements
- Production-ready scoring algorithm
- Three preset preference profiles
- Manual override capability designed
- All tests passing
- Zero technical debt

**See:** `phase-5-completion-summary.md`

---

## Phase 6: Basic UI Framework
**Goal:** Create touchscreen interface foundation

### Learning Topics
- PyQt5 basics
- Event-driven programming
- Touch interface design
- Screen layouts
- Qt Designer (optional)

### Tasks (with instruction)
- [x] 6.1: Learn PyQt5 fundamentals
- [x] 6.2: Create main window
- [x] 6.3: Build basic navigation
- [x] 6.4: Test touch responsiveness
- [x] 6.5: Implement screen transitions
- [ ] 6.6: Add keyboard input (for testing)

### Deliverables
- UI framework
- Example screens
- Navigation system
- Touch testing results

### Estimated Time
2-3 weeks

---

## Phase 7: Browse Interface
**Goal:** Let users find shows

### Learning Topics
- List views and scrolling
- Search/filter UI patterns
- Date pickers
- User input validation

### Tasks (with instruction)
- [ ] 7.1: Build show list view
- [ ] 7.2: Implement date browser
- [ ] 7.3: Add venue filter
- [ ] 7.4: Create year selector
- [ ] 7.5: Build search functionality
- [ ] 7.6: Add "random show" button

### Deliverables
- Browse screens
- Filter system
- Search implementation
- User testing notes

### Estimated Time
2-3 weeks

---

## Phase 8: Playback Interface
**Goal:** Beautiful now-playing screen

### Learning Topics
- Real-time UI updates
- Progress bars
- Custom widgets
- Responsive layouts

### Tasks (with instruction)
- [ ] 8.1: Design playback screen layout
- [ ] 8.2: Show current track info
- [ ] 8.3: Display setlist
- [ ] 8.4: Add playback controls
- [ ] 8.5: Show progress bar
- [ ] 8.6: Implement next/previous
- [ ] 8.7: Add volume slider

### Deliverables
- Complete playback UI
- Control integration
- Visual polish
- Usability testing

### Estimated Time
2-3 weeks

---

## Phase 9: Integration & Testing
**Goal:** Make everything work together smoothly

### Learning Topics
- Integration testing
- Performance profiling
- Memory management
- Error logging

### Tasks (with instruction)
- [ ] 9.1: Connect all modules
- [ ] 9.2: Test complete workflows
- [ ] 9.3: Optimize performance
- [ ] 9.4: Fix bugs
- [ ] 9.5: Add error handling
- [ ] 9.6: Implement logging
- [ ] 9.7: Create startup script

### Deliverables
- Fully integrated application
- Test suite
- Performance benchmarks
- Bug tracker

### Estimated Time
2-3 weeks

---

## Phase 10: Hardware Integration
**Goal:** Install DAC and optimize audio

### Learning Topics
- GPIO pin configuration
- DAC setup and drivers
- ALSA audio system
- Audio routing

### Tasks (with instruction)
- [ ] 10.1: Install HiFiBerry DAC
- [ ] 10.2: Configure drivers
- [ ] 10.3: Set default audio output
- [ ] 10.4: Test audio quality
- [ ] 10.5: Optimize buffer sizes
- [ ] 10.6: Add audio level monitoring

### Deliverables
- Working DAC integration
- Audio configuration guide
- Quality comparison notes
- Troubleshooting guide

### Estimated Time
1 week

---

## Phase 11: Polish & Features
**Goal:** Add the special touches

### Learning Topics
- Settings persistence
- Favorites/bookmarks
- History tracking
- Themes and styling

### Tasks (with instruction)
- [ ] 11.1: Build settings screen
- [ ] 11.2: Add favorites system
- [ ] 11.3: Implement play history
- [ ] 11.4: Create visual themes
- [ ] 11.5: Add "on this day" feature
- [ ] 11.6: Easter eggs!

### Deliverables
- Settings system
- Enhanced features
- Visual polish
- User manual

### Estimated Time
2-3 weeks

---

## Phase 12: Physical Build
**Goal:** Create the enclosure

### Learning Topics
- 3D modeling basics
- Enclosure design principles
- Component fitting
- Assembly techniques

### Tasks (with instruction)
- [ ] 12.1: Measure all components
- [ ] 12.2: Design case in CAD
- [ ] 12.3: 3D print prototype
- [ ] 12.4: Test fit and iterate
- [ ] 12.5: Print final case
- [ ] 12.6: Assemble device
- [ ] 12.7: Add finishing touches

### Deliverables
- 3D model files
- Printed enclosure
- Assembly documentation
- Photos of final build

### Estimated Time
2-4 weeks

---

## Phase 13: Documentation & Release
**Goal:** Document everything

### Learning Topics
- Technical writing
- README best practices
- User documentation
- Video tutorials (optional)

### Tasks (with instruction)
- [ ] 13.1: Write comprehensive README
- [ ] 13.2: Create user guide
- [ ] 13.3: Document code thoroughly
- [ ] 13.4: Build troubleshooting guide
- [ ] 13.5: Create demo video
- [ ] 13.6: Final testing
- [ ] 13.7: Tag v1.0 release

### Deliverables
- Complete documentation
- User guide
- Release notes
- Celebration!

### Estimated Time
1-2 weeks

---

## Total Estimated Timeline
**Realistic casual pace:** 4-6 months
**Focused effort:** 2-3 months
**Leisurely learning:** 6-12 months

Remember: This is a journey, not a race!
