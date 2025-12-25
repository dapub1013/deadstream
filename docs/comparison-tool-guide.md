# Recording Comparison Tool Guide

## Purpose

The comparison tool helps you understand how the DeadStream scoring algorithm selects the "best" recording when multiple versions of the same show exist.

## Basic Usage
```bash
# Compare all recordings for a specific date
python examples/compare_recordings.py --date YYYY-MM-DD
```

## Examples

### Cornell '77 (Many Recordings)
```bash
python examples/compare_recordings.py --date 1977-05-08
```

Shows all available recordings with detailed scoring breakdown.

### Using Presets

**Audiophile Mode** (prioritizes sound quality):
```bash
python examples/compare_recordings.py --date 1977-05-08 --preset audiophile
```

**Crowd Favorite Mode** (prioritizes community ratings):
```bash
python examples/compare_recordings.py --date 1977-05-08 --preset crowd_favorite
```

**Balanced Mode** (equal consideration):
```bash
python examples/compare_recordings.py --date 1977-05-08 --preset balanced
```

### Using Custom Weights
```bash
# Edit config/preferences.yaml first, then:
python examples/compare_recordings.py --date 1977-05-08 --weights custom
```

## Understanding the Output

### Total Score
- Range: 0-100
- Higher is better
- Weighted combination of all factors

### Component Scores
- **Source Type**: Soundboard > Matrix > Audience
- **Format Quality**: FLAC > MP3 High > MP3 Low
- **Community Rating**: Based on Archive.org ratings
- **Lineage**: Fewer generations = better
- **Taper**: Known quality tapers get bonus

### Visual Bar Graph
```
TOTAL SCORE:  87.50/100 [###################################-----]
```

The bar shows relative quality at a glance.

## Testing Strategy

### Find Shows with Multiple Recordings
```bash
# Use the database to find shows with alternatives
python examples/find_multiple_recordings.py
```

### Common Test Shows
- `1977-05-08` - Cornell '77 (10+ recordings)
- `1972-05-11` - Rotterdam '72
- `1974-05-19` - Portland Memorial
- `1970-02-13` - Fillmore East

## Validating the Algorithm

Use the comparison tool to verify:

1. **Soundboards score higher than audience tapes**
2. **FLAC scores higher than MP3**
3. **High ratings boost total score**
4. **Known tapers get appropriate bonus**
5. **Presets change rankings as expected**

## Troubleshooting

### "No shows found for date"
- Check date format (YYYY-MM-DD)
- Verify show exists in database

### "Failed to score recording"
- API might be slow/unavailable
- Try again in a moment

### Unexpected winner
- Check the component scores
- Verify your weights/preset
- Some shows have surprising "best" versions

## Integration with Player

Once validated, the selection algorithm will automatically:
1. Find all recordings for a show date
2. Score them using your preferences
3. Select the highest-scoring recording
4. Stream it to the audio player

The comparison tool lets you preview and validate these decisions.
