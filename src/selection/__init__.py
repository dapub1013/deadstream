"""
Smart show selection system.

Automatically selects the best recording when multiple versions exist.
"""

from .scoring import RecordingScorer

__all__ = ['RecordingScorer']