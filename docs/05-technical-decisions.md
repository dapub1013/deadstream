# Technical Decisions Record

## Hardware
- **Raspberry Pi:** Pi 4 Model B (4GB)
- **DAC:** IQaudio DAC Pro
- **Screen:** Touch Display 2 - best support, perfect size
- **Storage:** 32GB microSD - adequate for OS and database
- **Power:** Official 5V 3A USB-C supply

## Software Stack
- **OS:** Raspberry Pi OS
- **Language:** Python 3.9+
- **UI Framework:** PyQt5 (mature, well-documented, touch-friendly)
- **Audio:** VLC Python bindings (robust streaming, format support)
- **Database:** SQLite (serverless, reliable, built-in)
- **API:** Python requests library (simple, standard)

## Architecture Patterns
- **MVC separation:** Model (data/API), View (UI), Controller (logic)
- **Single responsibility:** Each module has one clear job
- **Configuration-driven:** Settings in YAML, not hardcoded
- **Testable:** Unit tests for all critical functions

## API Strategy
- **Pre-download master list:** Faster, offline-capable browsing
- **Lazy metadata loading:** Only fetch full details when needed
- **Smart caching:** Cache common queries, respect rate limits
- **Weekly updates:** Check for new shows Sunday 3 AM

## UI Principles
- **Touch-first design:** Big buttons, swipe gestures
- **Minimal typing:** Lists and pickers over keyboards
- **High contrast:** Readable in various lighting
- **Forgiving:** Easy to go back, hard to break

## Why These Choices?
Each decision prioritizes:
1. Learning value (common tools you can use elsewhere)
2. Community support (good documentation, active forums)
3. Reliability (proven, stable technologies)
4. Simplicity (no over-engineering)

## Alternative Approaches Considered

### Why Not Volumio/MusicBox?
- Less learning - mostly configuration
- Limited customization for our specific use case
- We want to understand every component

### Why Not Flutter/React Native?
- Steeper learning curve for first project
- Overkill for a single-purpose device
- Python ecosystem better for Pi

### Why Not Arduino?
- Not powerful enough for audio streaming
- Limited UI capabilities
- Can't handle WiFi + streaming + display simultaneously

### Why Not Android Tablet?
- Less fun - just an app on a tablet
- Doesn't teach hardware integration
- Not as custom/unique

### Why PyQt5 Instead of Kivy?
- PyQt5: More mature, better documentation, larger community
- Kivy: More modern but less stable, fewer tutorials
- Both work well on Pi, PyQt5 slightly better performance

### Why SQLite Instead of PostgreSQL?
- SQLite: Serverless, zero configuration, perfect for embedded
- PostgreSQL: Overkill, requires separate server process
- Our data is simple, SQLite is ideal

### Why VLC Instead of pygame.mixer?
- VLC: Better format support, robust streaming, handles errors gracefully
- pygame.mixer: Simpler but less reliable for network streaming
- VLC has better buffer management for streaming

## Database Schema Decisions

### Shows Table
```sql
CREATE TABLE shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    venue TEXT,
    city TEXT,
    state TEXT,
    identifier TEXT UNIQUE NOT NULL,
    avg_rating REAL,
    num_reviews INTEGER,
    source_type TEXT,  -- 'sbd', 'aud', 'matrix'
    taper TEXT,
    transferer TEXT,
    last_updated TEXT,
    UNIQUE(date, identifier)
);

CREATE INDEX idx_date ON shows(date);
CREATE INDEX idx_venue ON shows(venue);
CREATE INDEX idx_rating ON shows(avg_rating);
```

### Why This Schema?
- One record per recording (not per show date)
- Multiple recordings per date handled naturally
- Indexed on common search fields
- Simple enough to understand, complex enough to be useful

## Audio Playback Decisions

### Streaming vs Downloading
- **Choice:** Stream only (no local caching of audio files)
- **Why:** 
  - Archive.org bandwidth is excellent
  - Saves storage space
  - Always get latest/best version
  - Simpler code
- **Tradeoff:** Requires internet connection

### Playlist Management
- **Choice:** Build full playlist upfront from setlist
- **Why:**
  - Smoother track transitions
  - Can show "up next"
  - Easier to implement skip forward/back
- **Alternative:** Load tracks one at a time (more complex)

## Configuration Management

### YAML vs JSON vs INI
- **Choice:** YAML for human-editable config
- **Why:**
  - More readable than JSON
  - Supports comments (unlike JSON)
  - Less fussy than INI for nested data
- **Files:**
  - `default_config.yaml` - Committed to git
  - `user_config.yaml` - Local only, overrides defaults

## Error Handling Philosophy

### Fail Gracefully
- Network errors: Show friendly message, retry logic
- Bad data: Log error, use sensible defaults
- API failures: Fall back to cached data when possible

### Never Crash
- Catch all exceptions at top level
- Log errors for debugging
- Show user-friendly error messages
- Always let user return to browse screen

## Testing Strategy

### What to Test
- API interactions (with mocked responses)
- Database queries
- Show selection algorithm
- Audio state management

### What NOT to Test
- UI appearance (manual testing)
- Network connectivity (too variable)
- Hardware-specific audio output

## Performance Targets

- **Boot time:** < 30 seconds to ready
- **Search response:** < 1 second
- **Playback start:** < 3 seconds from selection
- **UI responsiveness:** < 100ms for touch response
- **Memory usage:** < 500MB
- **Database query:** < 100ms for typical searches

## Security Considerations

### What We DON'T Need
- User authentication (single-user device)
- Encryption (streaming public domain content)
- HTTPS for Archive.org (nice to have, not critical)

### What We DO Need
- Input validation for search queries
- Safe file path handling
- No arbitrary code execution
- Graceful handling of malformed API responses

## Future Extensibility

### Design for Possible Enhancements
- Bluetooth audio output (built into Pi 4)
- Battery power (USB-C PD compatible)
- Other bands/collections (modular API layer)
- Remote control (web interface on local network)

### Don't Over-Engineer For
- Multi-user support
- Cloud sync
- Mobile apps
- Commercial distribution

## Lessons for Future Projects

Track what works well and what doesn't:
- Document pain points
- Note what was easier than expected
- Record "if I did this again..." thoughts
- Keep a "next project ideas" list

## Decision Change Log

**Note:** This document shows original planning decisions made before implementation. This change log tracks what actually changed during the build process.

| Date | Decision | Reason |
|------|----------|--------|
| 2025-11 | Initial tech stack chosen | Based on research and requirements |
| 2025-12-16 | **Changed: Raspberry Pi OS Desktop (64-bit) instead of Lite** | GUI development with PyQt5 requires desktop environment. Wayland works perfectly. "Lite" would require manually installing everything Desktop includes. Can optimize to boot-to-app later if needed. |
| 2025-12-16 | **Changed: 4GB RAM model instead of 2GB** | Actually owned hardware. 4GB provides comfortable development environment with room for future features. |
| 2025-12-16 | **Changed: 64GB microSD instead of 32GB** | Actually owned hardware (SanDisk Pixtor UHS-I, 80MB/s). Provides ample space for development, testing, and future show caching if needed. |
| 2025-12-16 | **Changed: IQaudio DAC Pro instead of HiFiBerry DAC2 HD** | Better price-to-performance ratio. $25 vs $60-70 = $35-45 savings. Excellent audio quality (112dB SNR, PCM5242 DAC chip). Audiophile community confirms quality matches/exceeds HiFiBerry DAC+ Pro. Perfect for streaming use case. Purchase deferred to Phase 10. |
| 2025-12-16 | **Clarified: Touch Display 2 - 7" in landscape orientation** | Resolution: 1280x720 (rotated from native 720x1280). Landscape better for music player UI (controls in row, split-view layouts possible). More "appliance-like" form factor. Natural for desktop/shelf placement. Purchase deferred to Phase 11. |
| 2025-12-16 | **Added: Development strategy - software first, hardware incremental** | Build and test all software on monitor with mouse/keyboard (Phase 1-9). Add DAC in Phase 10 for audio quality testing. Add touchscreen in Phase 11 for final build. Reduces risk, allows iterative testing, saves money upfront. |
| 2025-12-16 | **Added: Virtual environment with --system-site-packages flag** | Allows access to system-installed PyQt5 and VLC (compiled binaries for Pi) while maintaining project dependency isolation. Best of both worlds for Pi development. |
| 2025-12-18 | **Confirmed: Python 3.13.5** | Newer than planned minimum (3.9+). No compatibility issues encountered. Excellent performance and latest features available. |
| 2025-12-18 | **Established: UI button sizing standard** | 60x60px confirmed optimal for touch targets through testing. 44x44px minimum (too small for comfort), 80x80px wastes space. Will use 60x60px as standard for primary controls. |
| 2025-12-18 | **Established: Remote development workflow** | Primary development via Raspberry Pi Connect and SSH. VS Code on desktop for editing, Git for synchronization, Pi for testing. Very efficient for this project. |
| 2025-12-20 | **Phase 3: Shows-only database schema** | Simpler implementation sufficient for browsing functionality. Tracks table deferred to Phase 4 when needed for actual playback. Matches "lazy metadata loading" strategy from original technical decisions. Faster initial population (15-30 min vs 1-2 hours). |
| 2025-12-20 | **Phase 3: Minimal field approach for initial population** | Download only essential fields (identifier, date, venue, coverage, avg_rating, num_reviews) during initial database population. Faster download, smaller database (~5-10MB), lazy load additional metadata on-demand. Contains everything needed for browse functionality. |
| 2025-12-20 | **Phase 3: Database storage in project directory** | Database file located at `~/deadstream/data/shows.db`. Keeps project self-contained, easy to manage, already gitignored, simple backup. Natural for single-user device. |
| 2025-12-20 | **Phase 3: Idempotent insert pattern for error recovery** | Use `INSERT OR IGNORE` for safe re-runs instead of checkpoint system. Simpler implementation, adequate for 15-30 minute process. Safe to re-run entire populate script if interrupted. Database handles duplicates automatically. |
| 2025-12-20 | **Phase 3: Console-based progress indication** | Simple print statements for progress during database population. No extra dependencies, easy to debug, sufficient for 15-30 minute process. Can upgrade to progress bar later if desired. |
| 2025-12-20 | **Phase 3: Manual testing + sample dataset approach** | Test with sample years (1977-1978) before full download. Manual testing adequate for CRUD operations. Unit tests deferred to Phase 9 if needed. Focus on getting working functionality first. |

---

## Implementation Notes (Added During Phase 1)

### Hardware Acquisition Strategy
Following the "software first, hardware incremental" approach:

**Phase 1-9 (Current - Software Development):**
- Hardware: Pi 4 (4GB) + case + fan + HDMI monitor + keyboard/mouse
- Cost: $0 (all owned)
- Focus: Complete software development on existing hardware

**Phase 10 (Audio Quality):**
- Add: IQaudio DAC Pro ($25)
- Test: Audio quality, compare built-in 3.5mm vs DAC
- Continue: Development on monitor + keyboard/mouse

**Phase 11-12 (Final Build):**
- Add: 7" Touch Display 2 ($60)
- Complete: Physical enclosure, final assembly
- Total additional hardware cost: ~$85

### OS Choice Validation
Raspberry Pi OS Desktop (64-bit) proved to be the correct choice:
- Wayland display server works perfectly with PyQt5
- All required development tools available via apt
- No compilation needed for PyQt5 or VLC
- Can boot directly to application in final build if desired

### Phased Approach Benefits Realized
- Reduced upfront cost ($85 deferred until Phases 10-11)
- Faster development (large monitor, physical keyboard)
- Easier debugging (multiple windows, documentation access)
- Proof of concept before hardware investment
- Direct comparison possible (built-in audio vs DAC)

---

### Phase 3 Database Design (Added December 20, 2025)

**Final Schema:**
```sql
CREATE TABLE shows (
    identifier TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    venue TEXT,
    city TEXT,
    state TEXT,
    avg_rating REAL,
    num_reviews INTEGER,
    source_type TEXT,  -- 'sbd', 'aud', 'matrix'
    taper TEXT,
    last_updated TEXT
);

CREATE INDEX idx_date ON shows(date);
CREATE INDEX idx_venue ON shows(venue);
CREATE INDEX idx_rating ON shows(avg_rating);
CREATE INDEX idx_year ON shows(substr(date, 1, 4));
CREATE INDEX idx_state ON shows(state);
```

**Rationale for Single-Table Design:**
- Phase 3 goal: Build browsable show catalog
- Tracks not needed until Phase 4 (playback)
- Simpler = faster to implement and understand
- Can add tracks table when needed

**Population Strategy:**
1. Query Archive.org API year by year (1965-1995)
2. Download minimal fields for fast initial load
3. Use idempotent inserts (INSERT OR IGNORE)
4. Estimated time: 15-30 minutes for ~15,000 shows
5. Lazy load additional metadata on-demand

**Future Enhancement Path:**
- Phase 4: Add tracks table with foreign key to shows
- Phase 5: Add selection scoring fields if needed
- Phase 9: Add optimizations if performance issues arise

---

**Last Updated:** December 20, 2025 (Phase 3 Planning Complete)

## Open Questions

Questions we'll answer as we build:
- [ ] Do we need a cache layer for API responses?
- [ ] Should we support offline mode with downloaded shows?
- [ ] What's the optimal buffer size for streaming?
- [ ] Do we want keyboard shortcuts in addition to touch?
- [ ] Should favorites sync across devices? (probably not for v1)

## Resources & References

- Raspberry Pi Documentation: https://www.raspberrypi.com/documentation/
- PyQt5 Tutorial: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- Internet Archive API: https://archive.org/developers/
- HiFiBerry Setup: https://www.hifiberry.com/docs/
- SQLite Documentation: https://www.sqlite.org/docs.html
- Python VLC: https://wiki.videolan.org/Python_bindings
