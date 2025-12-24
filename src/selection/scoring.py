"""
Recording Quality Scoring System

Scores recordings based on multiple quality indicators to automatically
select the best version when multiple recordings exist for the same show.
"""

class RecordingScorer:
    """
    Scores recordings based on quality indicators.
    
    Scoring Factors:
    - Source type (soundboard > audience > matrix)
    - Audio format (FLAC > MP3 high > MP3 low)
    - Community rating (avg_rating, num_reviews)
    - Lineage quality (generations from master)
    - Taper reputation (if known)
    """
    
    # Default scoring weights (0-1 scale, must sum to 1.0)
    DEFAULT_WEIGHTS = {
        'source_type': 0.35,      # Most important - SBD vs AUD
        'format_quality': 0.25,   # Second - FLAC vs MP3
        'community_rating': 0.20, # Third - What Deadheads think
        'lineage': 0.10,          # Fourth - Generations from master
        'taper': 0.10             # Fifth - Taper reputation
    }
    
    # Source type scores (0-100 scale)
    SOURCE_SCORES = {
        'soundboard': 100,
        'sbd': 100,
        'matrix': 75,
        'audience': 50,
        'aud': 50,
        'unknown': 25
    }
    
    # Format quality scores (0-100 scale)
    FORMAT_SCORES = {
        'flac': 100,
        'shn': 95,     # Shorten (lossless)
        'mp3_320': 80,
        'mp3_vbr': 75,
        'mp3_256': 70,
        'mp3_192': 60,
        'mp3_160': 50,
        'mp3_128': 40,
        'mp3_low': 30,
        'unknown': 20
    }
    
    # Known quality tapers (0-100 scale)
    TAPER_SCORES = {
        'miller': 100,      # Charlie Miller - legendary
        'bertha': 95,       # Bertha Board series
        'vernon': 90,       # Dan Healy/Vernon - official crew
        'unknown': 50
    }
    
    def __init__(self, weights=None, preference_manager=None):
        """
        Initialize scorer with custom weights or from preference manager.
        
        Args:
            weights: Optional dict of scoring weights. Must sum to 1.0.
            preference_manager: Optional PreferenceManager instance to load weights from.
                               If both weights and preference_manager provided, weights takes precedence.
        """
        if weights is not None:
            # Explicit weights provided - use those
            self._validate_weights(weights)
            self.weights = weights
        elif preference_manager is not None:
            # Load from preference manager
            self.weights = preference_manager.get_weights()
        else:
            # Use defaults
            self.weights = self.DEFAULT_WEIGHTS.copy()
    
    def _validate_weights(self, weights):
        """Ensure weights are valid (sum to 1.0, all keys present)."""
        required_keys = set(self.DEFAULT_WEIGHTS.keys())
        provided_keys = set(weights.keys())
        
        if required_keys != provided_keys:
            missing = required_keys - provided_keys
            extra = provided_keys - required_keys
            raise ValueError(
                f"Invalid weights. Missing: {missing}, Extra: {extra}"
            )
        
        total = sum(weights.values())
        if not (0.99 <= total <= 1.01):  # Allow tiny floating point error
            raise ValueError(
                f"Weights must sum to 1.0, got {total}"
            )
    
    def score_recording(self, metadata):
        """
        Calculate total score for a recording.
        
        Args:
            metadata: Dict with recording metadata. Expected keys:
                - identifier: str (required)
                - source: str (optional, e.g. 'soundboard', 'audience')
                - format: str (optional, e.g. 'VBR MP3', 'Flac')
                - avg_rating: float (optional, 0-5)
                - num_reviews: int (optional)
                - lineage: str (optional)
                - taper: str (optional)
        
        Returns:
            Dict with 'total_score' (0-100) and component scores
        """
        # Calculate component scores
        source_score = self._score_source_type(metadata.get('source', ''))
        format_score = self._score_format(metadata.get('format', ''))
        rating_score = self._score_community_rating(
            metadata.get('avg_rating'),
            metadata.get('num_reviews')
        )
        lineage_score = self._score_lineage(metadata.get('lineage', ''))
        taper_score = self._score_taper(metadata.get('taper', ''))
        
        # Calculate weighted total (0-100 scale)
        total_score = (
            source_score * self.weights['source_type'] +
            format_score * self.weights['format_quality'] +
            rating_score * self.weights['community_rating'] +
            lineage_score * self.weights['lineage'] +
            taper_score * self.weights['taper']
        )
        
        return {
            'total_score': round(total_score, 2),
            'source_score': source_score,
            'format_score': format_score,
            'rating_score': rating_score,
            'lineage_score': lineage_score,
            'taper_score': taper_score,
            'identifier': metadata.get('identifier', 'unknown')
        }
    
    def _score_source_type(self, source):
        """Score based on recording source type."""
        if not source:
            return self.SOURCE_SCORES['unknown']
        
        source_lower = source.lower()
        
        # Check for exact matches first
        if source_lower in self.SOURCE_SCORES:
            return self.SOURCE_SCORES[source_lower]
        
        # Check for partial matches
        if 'sbd' in source_lower or 'soundboard' in source_lower:
            return self.SOURCE_SCORES['soundboard']
        elif 'matrix' in source_lower:
            return self.SOURCE_SCORES['matrix']
        elif 'aud' in source_lower or 'audience' in source_lower:
            return self.SOURCE_SCORES['audience']
        
        return self.SOURCE_SCORES['unknown']
    
    def _score_format(self, format_str):
        """Score based on audio format quality."""
        if not format_str:
            return self.FORMAT_SCORES['unknown']
        
        format_lower = format_str.lower()
        
        # FLAC (lossless)
        if 'flac' in format_lower:
            return self.FORMAT_SCORES['flac']
        
        # Shorten (lossless)
        if 'shn' in format_lower or 'shorten' in format_lower:
            return self.FORMAT_SCORES['shn']
        
        # MP3 - need to determine bitrate
        if 'mp3' in format_lower:
            if '320' in format_str or '320k' in format_lower:
                return self.FORMAT_SCORES['mp3_320']
            elif 'vbr' in format_lower or 'v0' in format_lower:
                return self.FORMAT_SCORES['mp3_vbr']
            elif '256' in format_str:
                return self.FORMAT_SCORES['mp3_256']
            elif '192' in format_str:
                return self.FORMAT_SCORES['mp3_192']
            elif '160' in format_str:
                return self.FORMAT_SCORES['mp3_160']
            elif '128' in format_str:
                return self.FORMAT_SCORES['mp3_128']
            elif '64' in format_str or '96' in format_str:
                return self.FORMAT_SCORES['mp3_low']
            # MP3 with unknown bitrate - assume mid-quality
            return 60
        
        return self.FORMAT_SCORES['unknown']
    
    def _score_community_rating(self, avg_rating, num_reviews):
        """
        Score based on community ratings from Archive.org.
        
        Combines average rating (0-5) with review count.
        More reviews = more confidence in rating.
        """
        if avg_rating is None or num_reviews is None:
            return 50  # Neutral score if no rating data
        
        # Convert avg_rating (0-5) to 0-100 scale
        rating_score = (avg_rating / 5.0) * 100
        
        # Apply confidence multiplier based on review count
        # More reviews = more reliable rating
        if num_reviews >= 20:
            confidence = 1.0      # Full confidence
        elif num_reviews >= 10:
            confidence = 0.95
        elif num_reviews >= 5:
            confidence = 0.90
        elif num_reviews >= 3:
            confidence = 0.80
        elif num_reviews >= 1:
            confidence = 0.70
        else:
            return 50  # No reviews = neutral
        
        # Blend with neutral (50) based on confidence
        # Low confidence pulls toward neutral
        final_score = rating_score * confidence + 50 * (1 - confidence)
        
        return round(final_score, 2)
    
    def _score_lineage(self, lineage):
        """
        Score based on recording lineage (generations from master).
        
        Lower generations = better quality.
        Example: "Master Reel > DAT > CDR > FLAC" is 3 generations
        """
        if not lineage:
            return 50  # Unknown lineage = neutral
        
        # Count generation markers
        lineage_lower = lineage.lower()
        
        # Direct from master sources
        if 'master' in lineage_lower and '>' not in lineage:
            return 100  # Direct master copy
        
        # Count generation steps (indicated by '>')
        generations = lineage.count('>')
        
        if generations == 0:
            return 90   # First generation
        elif generations == 1:
            return 80   # Second generation
        elif generations == 2:
            return 70   # Third generation
        elif generations == 3:
            return 60   # Fourth generation
        else:
            return max(50 - (generations - 3) * 10, 20)  # Fifth+ generation
    
    def _score_taper(self, taper):
        """Score based on taper reputation."""
        if not taper:
            return self.TAPER_SCORES['unknown']
        
        taper_lower = taper.lower()
        
        # Check for known quality tapers
        for known_taper, score in self.TAPER_SCORES.items():
            if known_taper in taper_lower:
                return score
        
        return self.TAPER_SCORES['unknown']
    
    def compare_recordings(self, recordings):
        """
        Score and rank multiple recordings.
        
        Args:
            recordings: List of metadata dicts
        
        Returns:
            List of scored recordings, sorted best to worst
        """
        scored = []
        for recording in recordings:
            score_result = self.score_recording(recording)
            scored.append(score_result)
        
        # Sort by total_score descending
        scored.sort(key=lambda x: x['total_score'], reverse=True)
        
        return scored
    
    def select_best(self, recordings):
        """
        Select the best recording from a list.
        
        Args:
            recordings: List of metadata dicts
        
        Returns:
            Identifier of best recording, or None if list empty
        """
        if not recordings:
            return None
        
        scored = self.compare_recordings(recordings)
        return scored[0]['identifier']