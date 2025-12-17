# Data Directory

This directory stores local data files that should NOT be committed to git.

## What Goes Here

- `shows.db` - SQLite database of all Grateful Dead shows
- `cache/` - Cached API responses
- `downloads/` - Downloaded show metadata
- User preferences and settings

## Important

All files in this directory are gitignored except this README and `.gitkeep`.

The database will be created during initial setup in Phase 3.
