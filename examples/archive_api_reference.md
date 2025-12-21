# Internet Archive API Reference - Phase 2.1

## Overview

The Internet Archive provides three main APIs for accessing Grateful Dead concerts:

1. **Advanced Search API** - Find shows by date, venue, year, etc.
2. **Metadata API** - Get full details for a specific show
3. **Download/Streaming URLs** - Direct links to audio files

**Important:** No authentication required for read-only access!

---

## 1. Advanced Search API

### Purpose
Search the entire Grateful Dead collection to find shows matching your criteria.

### Endpoint
```
https://archive.org/advancedsearch.php
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `q` | Search query | `collection:GratefulDead AND date:1977-05-08` |
| `fl` | Fields to return (comma-separated) | `identifier,title,date,venue,avg_rating` |
| `rows` | Number of results | `100` (max: 10000) |
| `output` | Response format | `json` |
| `sort` | Sort order | `date asc` or `avg_rating desc` |

### Common Search Queries

```python
# Search by specific date
q = "collection:GratefulDead AND date:1977-05-08"

# Search by year
q = "collection:GratefulDead AND year:1977"

# Search by date range
q = "collection:GratefulDead AND date:[1977-01-01 TO 1977-12-31]"

# Search by venue (partial match)
q = "collection:GratefulDead AND venue:*Fillmore*"

# Search for soundboards only
q = "collection:GratefulDead AND source:*soundboard*"

# Search by identifier pattern
q = "collection:GratefulDead AND identifier:*sbd*"

# Combine multiple criteria
q = "collection:GratefulDead AND year:1977 AND venue:*Cornell*"
```

### Example Request

```python
import requests

url = "https://archive.org/advancedsearch.php"
params = {
    'q': 'collection:GratefulDead AND date:1977-05-08',
    'fl': 'identifier,title,date,venue,avg_rating',
    'rows': 10,
    'output': 'json',
    'sort': 'avg_rating desc'
}

response = requests.get(url, params=params)
data = response.json()
```

### Example Response

```json
{
  "responseHeader": {
    "status": 0,
    "QTime": 47,
    "params": {
      "query": "collection:GratefulDead AND date:1977-05-08",
      "qin": "collection:GratefulDead AND date:1977-05-08",
      "fields": "identifier,title,date,venue,avg_rating",
      "wt": "json",
      "rows": "10",
      "start": 0
    }
  },
  "response": {
    "numFound": 12,
    "start": 0,
    "docs": [
      {
        "identifier": "gd77-05-08.sbd.hicks.4982.sbeok.shnf",
        "title": "Grateful Dead Live at Barton Hall, Cornell University on 1977-05-08",
        "date": "1977-05-08T00:00:00Z",
        "venue": "Barton Hall, Cornell University",
        "avg_rating": 4.8
      },
      {
        "identifier": "gd1977-05-08.sbd.miller.97065.sbeok.flac16",
        "title": "Grateful Dead Live at Barton Hall, Cornell University on 1977-05-08",
        "date": "1977-05-08T00:00:00Z",
        "venue": "Barton Hall, Cornell University",
        "avg_rating": 4.7
      },
      {
        "identifier": "gd1977-05-08.aud.beverly.331.sbeok.shnf",
        "title": "Grateful Dead Live at Barton Hall, Cornell University on 1977-05-08",
        "date": "1977-05-08T00:00:00Z",
        "venue": "Barton Hall, Cornell University",
        "avg_rating": 4.5
      }
    ]
  }
}
```

### Response Structure

- `response.numFound` - Total number of matching shows
- `response.docs` - Array of show objects
- Each show has fields you requested in `fl` parameter

### Useful Fields

| Field | Description |
|-------|-------------|
| `identifier` | Unique ID (use for metadata API) |
| `title` | Full title of the show |
| `date` | Date in ISO format (YYYY-MM-DD) |
| `venue` | Venue name |
| `coverage` | City, State, Country |
| `source` | Recording source description |
| `taper` | Person who recorded it |
| `transferer` | Person who digitized it |
| `avg_rating` | User rating (0-5 stars) |
| `num_reviews` | Number of user reviews |
| `downloads` | Number of downloads |

---

## 2. Metadata API

### Purpose
Get complete metadata for a specific show, including all available audio files.

### Endpoint
```
https://archive.org/metadata/{identifier}
```

### Example Request

```python
identifier = "gd77-05-08.sbd.hicks.4982.sbeok.shnf"
url = f"https://archive.org/metadata/{identifier}"

response = requests.get(url)
metadata = response.json()
```

### Example Response (Abbreviated)

```json
{
  "created": 1234567890,
  "d1": "ia902605.us.archive.org",
  "d2": "ia802605.us.archive.org",
  "dir": "/17/items/gd77-05-08.sbd.hicks.4982.sbeok.shnf",
  "files": [
    {
      "name": "gd77-05-08d1t01.mp3",
      "source": "derivative",
      "format": "VBR MP3",
      "original": "gd77-05-08d1t01.shn",
      "mtime": "1234567890",
      "size": "5242880",
      "md5": "abc123...",
      "crc32": "def456...",
      "sha1": "ghi789...",
      "length": "221.45",
      "height": "0",
      "width": "0",
      "title": "New Minglewood Blues",
      "track": "01",
      "album": "1977-05-08 - Barton Hall, Cornell University"
    },
    {
      "name": "gd77-05-08d1t02.mp3",
      "source": "derivative",
      "format": "VBR MP3",
      "size": "4718592",
      "length": "196.89",
      "title": "Loser",
      "track": "02"
    }
    // ... more files
  ],
  "metadata": {
    "identifier": "gd77-05-08.sbd.hicks.4982.sbeok.shnf",
    "mediatype": "etree",
    "collection": ["GratefulDead", "etree"],
    "title": "Grateful Dead Live at Barton Hall, Cornell University on 1977-05-08",
    "creator": "Grateful Dead",
    "date": "1977-05-08",
    "year": "1977",
    "venue": "Barton Hall, Cornell University",
    "coverage": "Ithaca, NY",
    "source": "Soundboard",
    "lineage": "SBD > Reel > ...",
    "taper": "Unknown (Betty Boards)",
    "transferer": "Doug Hicks",
    "description": "One of the most legendary shows...",
    "notes": "...setlist and notes...",
    "avg_rating": "4.80",
    "num_reviews": "142",
    "subject": ["Grateful Dead", "Live concert", "1977"]
  },
  "reviews": [
    {
      "reviewer": "deadhead123",
      "reviewtitle": "Best show ever!",
      "reviewbody": "This is the Cornell '77 show...",
      "stars": "5",
      "createdate": "2010-05-08 12:34:56"
    }
  ],
  "server": "ia902605.us.archive.org",
  "uniq": 123456,
  "workable_servers": ["ia902605.us.archive.org", "ia802605.us.archive.org"]
}
```

### Key Sections

**`metadata`** - Basic show information
- Date, venue, location
- Source type (Soundboard, Audience, Matrix)
- Taper and transfer info
- User ratings

**`files`** - All available files
- Audio files (MP3, FLAC, OGG)
- Text files (setlists, notes)
- Image files (covers, photos)
- Each file has format, size, length

**`reviews`** - User reviews and ratings

### Audio File Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `VBR MP3` | Variable bitrate MP3 | Streaming (smaller files) |
| `Ogg Vorbis` | Ogg audio | Alternative streaming format |
| `Flac` | Lossless audio | Best quality (larger files) |
| `Shorten` | Original lossless | Archival format |

**For DeadStream:** Use VBR MP3 for streaming (good quality, manageable size)

### Identifying Sets

Look at file names and track numbers:
- `d1t01` = Disc 1, Track 01 (Set I)
- `d1t08` = Disc 1, Track 08 (Set I)
- `d2t01` = Disc 2, Track 01 (Set II)
- `d3t01` = Disc 3, Track 01 (Encore)

Or use `title` field if available.

---

## 3. Download/Streaming URLs

### Purpose
Direct links to audio files for streaming or downloading.

### URL Pattern
```
https://archive.org/download/{identifier}/{filename}
```

### Example
```python
identifier = "gd77-05-08.sbd.hicks.4982.sbeok.shnf"
filename = "gd77-05-08d1t01.mp3"

url = f"https://archive.org/download/{identifier}/{filename}"
# Result: https://archive.org/download/gd77-05-08.sbd.hicks.4982.sbeok.shnf/gd77-05-08d1t01.mp3
```

### Building a Playlist

```python
def build_playlist(metadata):
    """Extract MP3 URLs from metadata"""
    identifier = metadata['metadata']['identifier']
    files = metadata['files']
    
    # Get only MP3 files
    mp3_files = [f for f in files if f.get('format') == 'VBR MP3']
    
    # Sort by track number
    mp3_files.sort(key=lambda x: x.get('name', ''))
    
    # Build URLs
    urls = []
    for f in mp3_files:
        url = f"https://archive.org/download/{identifier}/{f['name']}"
        urls.append({
            'url': url,
            'title': f.get('title', 'Unknown'),
            'track': f.get('track', '?'),
            'length': f.get('length', '0')
        })
    
    return urls
```

### Streaming with VLC

```python
import vlc

instance = vlc.Instance()
player = instance.media_player_new()

url = "https://archive.org/download/gd77-05-08.sbd.hicks.4982.sbeok.shnf/gd77-05-08d1t01.mp3"
media = instance.media_new(url)
player.set_media(media)
player.play()
```

---

## Code Examples for DeadStream

### Example 1: Search for Shows by Year

```python
def get_shows_by_year(year, max_results=100):
    """Get all shows from a specific year"""
    url = "https://archive.org/advancedsearch.php"
    params = {
        'q': f'collection:GratefulDead AND year:{year}',
        'fl': 'identifier,title,date,venue,coverage,avg_rating',
        'rows': max_results,
        'output': 'json',
        'sort': 'date asc'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return data['response']['docs']

# Usage
shows_1977 = get_shows_by_year(1977)
print(f"Found {len(shows_1977)} shows from 1977")
```

### Example 2: Get Best Recording for a Date

```python
def get_best_recording(date):
    """Find the highest-rated recording for a specific date"""
    url = "https://archive.org/advancedsearch.php"
    params = {
        'q': f'collection:GratefulDead AND date:{date}',
        'fl': 'identifier,title,avg_rating,source',
        'rows': 100,
        'output': 'json',
        'sort': 'avg_rating desc'  # Highest rated first
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    shows = data['response']['docs']
    
    if not shows:
        return None
    
    # Prefer soundboards if available
    soundboards = [s for s in shows if 'sbd' in s.get('identifier', '').lower()]
    if soundboards:
        return soundboards[0]
    
    # Otherwise return highest rated
    return shows[0]

# Usage
best = get_best_recording('1977-05-08')
print(f"Best recording: {best['identifier']}")
print(f"Rating: {best.get('avg_rating', 'N/A')}")
```

### Example 3: Get Playable Tracks

```python
def get_playable_tracks(identifier):
    """Get streaming URLs for all tracks in a show"""
    url = f"https://archive.org/metadata/{identifier}"
    response = requests.get(url)
    metadata = response.json()
    
    # Extract MP3 files
    files = metadata['files']
    mp3_files = [f for f in files if f.get('format') == 'VBR MP3']
    mp3_files.sort(key=lambda x: x.get('name', ''))
    
    # Build track list
    tracks = []
    for f in mp3_files:
        track = {
            'url': f"https://archive.org/download/{identifier}/{f['name']}",
            'title': f.get('title', f['name']),
            'track_number': f.get('track', '?'),
            'duration': float(f.get('length', 0)),
            'set': determine_set(f['name'])  # Custom function
        }
        tracks.append(track)
    
    return tracks

def determine_set(filename):
    """Determine which set a track belongs to"""
    if 'd1t' in filename:
        return 'Set I'
    elif 'd2t' in filename:
        return 'Set II'
    elif 'd3t' in filename:
        return 'Encore'
    else:
        return 'Unknown'

# Usage
tracks = get_playable_tracks('gd77-05-08.sbd.hicks.4982.sbeok.shnf')
for track in tracks:
    print(f"{track['set']} - {track['title']}")
```

---

## API Best Practices

### 1. Error Handling
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raises HTTPError for bad status
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Network connection failed")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except json.JSONDecodeError:
    print("Invalid JSON response")
```

### 2. Rate Limiting
- Archive.org doesn't have strict rate limits
- Be reasonable: don't hammer the API
- Cache results when possible
- Use batch queries instead of many small ones

### 3. Caching Strategy
```python
import time

cache = {}
CACHE_DURATION = 3600  # 1 hour

def cached_request(url):
    """Simple cache to avoid repeated API calls"""
    now = time.time()
    
    if url in cache:
        data, timestamp = cache[url]
        if now - timestamp < CACHE_DURATION:
            return data
    
    response = requests.get(url)
    data = response.json()
    cache[url] = (data, now)
    
    return data
```

### 4. Retry Logic
```python
import time

def retry_request(url, max_retries=3):
    """Retry failed requests with exponential backoff"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise  # Give up after max retries
            
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
            time.sleep(wait_time)
```

---

## Common Pitfalls

### 1. Inconsistent Metadata
- Not all shows have complete metadata
- Venue names vary ("Fillmore West" vs "The Fillmore West")
- Use fuzzy matching for venue searches
- Always check for missing fields

### 2. Multiple Recordings Per Date
- Popular shows have 10+ different recordings
- Sort by rating or source type to pick the best
- Consider letting users choose their preferred source

### 3. File Naming Conventions
- Not standardized across all shows
- Track numbers may be missing
- Use filename sorting as fallback

### 4. Large Responses
- Some queries return thousands of results
- Use pagination (`rows` and `start` parameters)
- Download only what you need

---

## Next Steps

Now that you understand the API:

1. **Test the examples** - Modify queries, try different dates
2. **Explore the data** - Look at actual JSON responses
3. **Build your own functions** - Combine Search + Metadata APIs
4. **Think about caching** - How to store show data locally
5. **Plan your database** - What fields do you need?

---

## Reference Links

- Archive.org Advanced Search: https://archive.org/advancedsearch.php
- API Documentation: https://archive.org/developers/
- Grateful Dead Collection: https://archive.org/details/GratefulDead
- Search Syntax Guide: https://archive.org/developers/query-syntax.html

---

**Created for DeadStream Project - Phase 2.1**  
**Date:** December 19, 2025
