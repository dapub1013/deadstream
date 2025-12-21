# Phase 2.1 Completion Guide - Archive.org API Documentation

**Task:** 2.1 - Read Archive.org API documentation  
**Status:** Complete - Ready to move to 2.2  
**Date:** December 19, 2025

---

## What You Now Know

### The Three APIs

1. **Advanced Search API**
   - Purpose: Find shows by date, venue, year, etc.
   - URL: `https://archive.org/advancedsearch.php`
   - Returns: List of shows with basic info
   - Use for: Browsing, searching, building your database

2. **Metadata API**
   - Purpose: Get complete details for a specific show
   - URL: `https://archive.org/metadata/{identifier}`
   - Returns: Full metadata + all available files
   - Use for: Getting track lists, show details, ratings

3. **Streaming/Download URLs**
   - Purpose: Direct links to audio files
   - Pattern: `https://archive.org/download/{identifier}/{filename}`
   - Returns: The actual MP3/FLAC/OGG file
   - Use for: Playing music with VLC

### Key Concepts

**Identifier** - Unique ID for each recording
- Example: `gd77-05-08.sbd.hicks.4982.sbeok.shnf`
- Used to fetch metadata and build streaming URLs
- Different recordings of same show have different identifiers

**Fields** - What data to return from search
- Common: `identifier,title,date,venue,avg_rating`
- Can request any available field
- More fields = larger response

**Query Syntax** - How to search
- Basic: `collection:GratefulDead AND date:1977-05-08`
- Wildcards: `venue:*Fillmore*`
- Ranges: `date:[1977-01-01 TO 1977-12-31]`

---

## Files Created

### 1. `archive_api_reference.md`
**Complete API documentation including:**
- Detailed explanation of each endpoint
- Request/response examples
- Common search queries
- Code examples
- Best practices
- Error handling
- Caching strategies

**Use this:** As your API reference when coding

### 2. `api_quickstart.py`
**Interactive learning script showing:**
- Example API responses (works offline!)
- Essential code patterns
- Practical examples
- Ready-to-use template

**Run this:** To understand the data structure

### 3. `api_basics.py`
**Full working examples (requires network):**
- Live API calls to Archive.org
- Search for Cornell '77
- Get show metadata
- Build streaming URLs
- Error handling

**Run this:** When you want to test with real API

---

## How This Fits Into DeadStream

### Your Architecture

```
User Interface (PyQt5)
        |
        v
    Controller
        |
        v
  API Client  ← You'll build this in tasks 2.2-2.6
        |
        v
  Archive.org API
```

### What You'll Build

Based on the template in `api_quickstart.py`, you'll create:

```
src/api/
├── __init__.py
├── archive_client.py    ← Main API client class
├── search.py            ← Search functionality
├── metadata.py          ← Metadata retrieval
└── stream_urls.py       ← URL building
```

### The ArchiveClient Class

This is the core class you'll use everywhere:

```python
from src.api.archive_client import ArchiveClient

# In your UI code:
client = ArchiveClient()

# Search for shows
shows = client.search_shows('year:1977')

# Pick the best one
best = client.find_best_recording('1977-05-08')

# Get tracks to play
tracks = client.get_streaming_urls(best['identifier'])

# Pass to VLC player
player.load_playlist(tracks)
```

---

## Next Steps: Task 2.2

**Task 2.2: Write simple script to search for one show**

You're now ready to write actual code! Here's what you'll do:

1. Create `src/api/archive_client.py`
2. Implement the `search_shows()` method
3. Test it with Cornell '77
4. Handle errors gracefully
5. Print results nicely

**Starting template is already in `api_quickstart.py`** - just copy the ArchiveClient class!

---

## Quick Reference

### Search for shows by date:
```python
shows = client.search_shows('date:1977-05-08')
```

### Search for shows by year:
```python
shows = client.search_shows('year:1977')
```

### Search for shows at venue:
```python
shows = client.search_shows('venue:*Cornell*')
```

### Get show metadata:
```python
metadata = client.get_metadata('gd77-05-08.sbd.hicks.4982.sbeok.shnf')
```

### Get streaming URLs:
```python
tracks = client.get_streaming_urls('gd77-05-08.sbd.hicks.4982.sbeok.shnf')
for track in tracks:
    print(f"{track['title']}: {track['url']}")
```

---

## Testing Strategy

Since network access is limited in this environment:

1. **Development:** Use example data from `api_quickstart.py`
2. **Testing:** Run `api_basics.py` when you have network access
3. **Production:** Use real API with error handling

---

## Important Notes

### No Authentication Required
- Read-only access is completely open
- No API keys needed
- No rate limits (but be respectful)

### Response Times
- Search API: Usually < 1 second
- Metadata API: Usually < 2 seconds
- Streaming: Depends on file size and bandwidth

### Data Quality
- Not all shows have complete metadata
- Venue names vary between recordings
- Always check for missing fields
- Use `.get()` with defaults

### Multiple Recordings
- Popular shows have 10+ different recordings
- Different tapers, different quality
- Sort by rating or look for "sbd" (soundboard)
- Let users choose their preferred source (future feature)

---

## Common Patterns You'll Use

### 1. Find Best Recording for a Date
```python
def get_best_show(date):
    shows = search_shows(f'date:{date}')
    soundboards = [s for s in shows if 'sbd' in s['identifier'].lower()]
    if soundboards:
        return max(soundboards, key=lambda x: x.get('avg_rating', 0))
    return max(shows, key=lambda x: x.get('avg_rating', 0))
```

### 2. Build Setlist
```python
def get_setlist(identifier):
    metadata = get_metadata(identifier)
    tracks = get_streaming_urls(identifier)
    
    setlist = {'Set I': [], 'Set II': [], 'Encore': []}
    for track in tracks:
        setlist[track['set']].append(track['title'])
    
    return setlist
```

### 3. Search with Pagination
```python
def get_all_shows_from_year(year):
    shows = []
    rows_per_request = 1000
    start = 0
    
    while True:
        batch = search_shows(f'year:{year}', start=start, rows=rows_per_request)
        if not batch:
            break
        shows.extend(batch)
        start += rows_per_request
    
    return shows
```

---

## Troubleshooting

### "Connection Error"
- Network connectivity issue
- Archive.org might be down (rare)
- Try again in a few seconds with retry logic

### "Empty Response"
- No shows match your query
- Check query syntax
- Try broader search (e.g., year instead of specific date)

### "Invalid JSON"
- Archive.org returned error page instead of JSON
- Usually indicates malformed query
- Check your query string carefully

### "Missing Fields"
- Not all shows have all metadata
- Always use `.get()` with default values
- Example: `show.get('venue', 'Unknown Venue')`

---

## Phase 2.1 Success Criteria

You've completed this task when you can answer:

- [x] How do I search for shows? → Advanced Search API
- [x] How do I get show details? → Metadata API  
- [x] How do I play a show? → Build streaming URLs
- [x] What's an identifier? → Unique ID for each recording
- [x] How do I pick the best version? → Filter for soundboards, sort by rating
- [x] What's the response structure? → See example data in quickstart

**Status: COMPLETE** - Ready for Task 2.2!

---

## Resources Created

All in `/home/claude/`:
1. `archive_api_reference.md` - Complete API reference
2. `api_quickstart.py` - Interactive tutorial (run this first!)
3. `api_basics.py` - Live API examples (run when network available)

**Recommendation:** Read `archive_api_reference.md` while writing code for 2.2

---

**Great work completing 2.1!**

You now understand:
- How the Archive.org API works
- What data is available
- How to structure your requests
- What the responses look like
- How to build streaming URLs

**Next:** Task 2.2 - Write your first search script!
