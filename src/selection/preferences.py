#!/usr/bin/env python3
"""
User Preferences Management

Handles loading, saving, and validating user preferences for
recording selection scoring weights.
"""

import os
import yaml
from typing import Dict, Optional

class PreferenceManager:
    """
    Manages user preferences for recording selection.
    
    Handles loading preferences from YAML config file, validating them,
    and providing defaults when needed.
    """
    
    # Default scoring weights
    DEFAULT_WEIGHTS = {
        'source_type': 0.35,      # Soundboard vs audience
        'format_quality': 0.25,   # FLAC vs MP3
        'community_rating': 0.20, # User ratings
        'lineage': 0.10,          # Generations from master
        'taper': 0.10             # Taper reputation
    }
    
    # Preset profiles for different listening preferences
    PRESETS = {
        'audiophile': {
            'source_type': 0.40,
            'format_quality': 0.35,
            'community_rating': 0.10,
            'lineage': 0.10,
            'taper': 0.05
        },
        'crowd_favorite': {
            'source_type': 0.20,
            'format_quality': 0.15,
            'community_rating': 0.50,
            'lineage': 0.05,
            'taper': 0.10
        },
        'balanced': DEFAULT_WEIGHTS.copy()
    }
    
    def __init__(self, config_path=None):
        """
        Initialize preference manager.
        
        Args:
            config_path: Path to preferences YAML file. If None, uses default.
        """
        if config_path is None:
            # Default to config/preferences.yaml
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            self.config_path = os.path.join(project_root, 'config', 'preferences.yaml')
        else:
            self.config_path = config_path
        
        self.preferences = self._load_preferences()
    
    def _load_preferences(self) -> Dict:
        """
        Load preferences from YAML file.
        
        Returns:
            Dict containing user preferences
        """
        if not os.path.exists(self.config_path):
            print(f"[INFO] No preferences file found at {self.config_path}")
            print("[INFO] Using default preferences")
            return {'weights': self.DEFAULT_WEIGHTS.copy()}
        
        try:
            with open(self.config_path, 'r') as f:
                prefs = yaml.safe_load(f)
            
            if prefs is None:
                print("[WARN] Empty preferences file, using defaults")
                return {'weights': self.DEFAULT_WEIGHTS.copy()}
            
            # Validate loaded preferences
            if 'weights' in prefs:
                self._validate_weights(prefs['weights'])
            else:
                print("[WARN] No weights in preferences file, using defaults")
                prefs['weights'] = self.DEFAULT_WEIGHTS.copy()
            
            return prefs
            
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse preferences YAML: {e}")
            print("[INFO] Using default preferences")
            return {'weights': self.DEFAULT_WEIGHTS.copy()}
        except Exception as e:
            print(f"[ERROR] Failed to load preferences: {e}")
            print("[INFO] Using default preferences")
            return {'weights': self.DEFAULT_WEIGHTS.copy()}
    
    def _validate_weights(self, weights: Dict) -> None:
        """
        Validate that weights are proper.
        
        Args:
            weights: Dict of weight values
            
        Raises:
            ValueError: If weights are invalid
        """
        required_keys = set(self.DEFAULT_WEIGHTS.keys())
        provided_keys = set(weights.keys())
        
        # Check for missing or extra keys
        if required_keys != provided_keys:
            missing = required_keys - provided_keys
            extra = provided_keys - required_keys
            raise ValueError(
                f"Invalid weights. Missing: {missing}, Extra: {extra}"
            )
        
        # Check that weights sum to approximately 1.0
        total = sum(weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"Weights must sum to 1.0, got {total}"
            )
        
        # Check that all weights are positive
        for key, value in weights.items():
            if value < 0 or value > 1:
                raise ValueError(
                    f"Weight '{key}' must be between 0 and 1, got {value}"
                )
    
    def get_weights(self) -> Dict:
        """
        Get current scoring weights.
        
        Returns:
            Dict of weight values
        """
        return self.preferences.get('weights', self.DEFAULT_WEIGHTS).copy()
    
    def set_weights(self, weights: Dict) -> None:
        """
        Set new scoring weights.
        
        Args:
            weights: Dict of new weight values
            
        Raises:
            ValueError: If weights are invalid
        """
        self._validate_weights(weights)
        self.preferences['weights'] = weights.copy()
    
    def use_preset(self, preset_name: str) -> None:
        """
        Load a preset preference profile.
        
        Args:
            preset_name: Name of preset ('audiophile', 'crowd_favorite', 'balanced')
            
        Raises:
            ValueError: If preset name is invalid
        """
        if preset_name not in self.PRESETS:
            available = ', '.join(self.PRESETS.keys())
            raise ValueError(
                f"Unknown preset '{preset_name}'. Available: {available}"
            )
        
        self.preferences['weights'] = self.PRESETS[preset_name].copy()
        self.preferences['preset'] = preset_name
    
    def save_preferences(self) -> bool:
        """
        Save current preferences to YAML file.
        
        Returns:
            True if save successful, False otherwise
        """
        try:
            # Create config directory if it doesn't exist
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                yaml.dump(self.preferences, f, default_flow_style=False)
            
            print(f"[PASS] Preferences saved to {self.config_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save preferences: {e}")
            return False
    
    def reset_to_defaults(self) -> None:
        """Reset all preferences to default values."""
        self.preferences = {'weights': self.DEFAULT_WEIGHTS.copy()}
    
    def get_preset_names(self) -> list:
        """Get list of available preset names."""
        return list(self.PRESETS.keys())
    
    def display_current_preferences(self) -> None:
        """Print current preferences in a readable format."""
        print("\n[INFO] Current Preferences:")
        print("=" * 50)
        
        if 'preset' in self.preferences:
            print(f"Active Preset: {self.preferences['preset']}")
        else:
            print("Active Preset: custom")
        
        print("\nScoring Weights:")
        weights = self.get_weights()
        for key, value in sorted(weights.items()):
            percentage = value * 100
            bar = '#' * int(percentage / 5)
            print(f"  {key:20s}: {percentage:5.1f}% {bar}")
        
        print(f"\nTotal: {sum(weights.values()) * 100:.1f}%")
        print("=" * 50)


def create_default_preferences_file(config_path=None):
    """
    Create a default preferences.yaml file with documentation.
    
    Args:
        config_path: Path where to create the file. If None, uses default location.
    """
    if config_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        config_path = os.path.join(project_root, 'config', 'preferences.yaml')
    
    # Create config directory if needed
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # Default preferences with comments
    content = """# DeadStream User Preferences
# 
# This file controls how recordings are scored and selected.
# Weights must be between 0 and 1 and must sum to 1.0.
#
# You can use one of the presets by uncommenting it, or customize weights below.

# Presets (uncomment one to use):
# preset: balanced      # Equal consideration of all factors
# preset: audiophile    # Prioritizes sound quality over community ratings
# preset: crowd_favorite # Prioritizes what other Deadheads love

# Custom weights (edit values below):
weights:
  source_type: 0.35      # Soundboard > audience (0-1)
  format_quality: 0.25   # FLAC > MP3 quality (0-1)
  community_rating: 0.20 # Archive.org user ratings (0-1)
  lineage: 0.10          # Generations from master tape (0-1)
  taper: 0.10            # Taper reputation (0-1)

# Note: Weights must sum to 1.0
"""
    
    try:
        with open(config_path, 'w') as f:
            f.write(content)
        print(f"[PASS] Created default preferences at {config_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create preferences file: {e}")
        return False


# Command-line interface for testing
if __name__ == '__main__':
    import sys
    
    print("\n=== DeadStream Preference Manager ===\n")
    
    # Create or load preferences
    pm = PreferenceManager()
    pm.display_current_preferences()
    
    # Show available presets
    print("\n[INFO] Available Presets:")
    for preset_name in pm.get_preset_names():
        print(f"  - {preset_name}")
    
    print("\n[INFO] To customize, edit: config/preferences.yaml")
    print("[INFO] Or use presets: pm.use_preset('audiophile')")