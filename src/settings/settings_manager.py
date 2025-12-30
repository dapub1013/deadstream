#!/usr/bin/env python3
"""
DeadStream Settings Manager
Phase 8, Task 8.4: Settings data persistence

Centralized settings management for all application configuration.
Handles loading, saving, and validation of user preferences.
"""

import os
import yaml
from typing import Dict, Any, Optional
from datetime import datetime
from copy import deepcopy


class SettingsManager:
    """
    Manages all application settings with persistent storage.
    
    Settings are stored in YAML format at config/settings.yaml
    Provides defaults, validation, and easy access from UI components.
    """
    
    # Default settings for new installations
    DEFAULT_SETTINGS = {
        'network': {
            'auto_connect': True,
            'last_connected_ssid': None,
            'prefer_5ghz': True,
        },
        'audio': {
            'default_volume': 75,
            'quality_preference': 'balanced',  # balanced, audiophile, crowd_favorite
            'auto_play_on_startup': False,
            'crossfade_enabled': False,
        },
        'display': {
            'brightness': 80,
            'auto_brightness': False,
            'screen_timeout': 300,  # seconds (5 minutes)
            'theme': 'dark',  # dark or light (future)
        },
        'datetime': {
            'timezone': 'America/New_York',
            'time_format_24h': False,
            'date_format': 'US',  # US (MM/DD/YYYY) or International (DD/MM/YYYY)
        },
        'app': {
            'last_screen': 'browse',  # player, browse, settings
            'show_splash': True,
            'check_updates': True,
            'last_update_check': None,
        },
        'version': '0.1.0',
        'last_modified': None,
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize settings manager.
        
        Args:
            config_path: Path to settings YAML file. If None, uses default location.
        """
        if config_path is None:
            # Default to config/settings.yaml in project root
            # We're in src/settings/, so go up two levels
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            config_dir = os.path.join(project_root, 'config')
            
            # Create config directory if it doesn't exist
            os.makedirs(config_dir, exist_ok=True)
            
            self.config_path = os.path.join(config_dir, 'settings.yaml')
        else:
            self.config_path = config_path
        
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """
        Load settings from YAML file.
        
        Returns:
            Dictionary of settings (uses defaults if file doesn't exist)
        """
        if not os.path.exists(self.config_path):
            print(f"[INFO] Settings file not found, creating with defaults: {self.config_path}")
            self._save_settings(deepcopy(self.DEFAULT_SETTINGS))
            return deepcopy(self.DEFAULT_SETTINGS)
        
        try:
            with open(self.config_path, 'r') as f:
                loaded = yaml.safe_load(f)
                
            if loaded is None:
                print("[WARN] Settings file empty, using defaults")
                return deepcopy(self.DEFAULT_SETTINGS)
            
            # Merge loaded settings with defaults (in case new settings added)
            settings = self._merge_with_defaults(loaded)
            
            print(f"[OK] Settings loaded from {self.config_path}")
            return settings
            
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse settings file: {e}")
            print("[INFO] Using default settings")
            return deepcopy(self.DEFAULT_SETTINGS)
        except Exception as e:
            print(f"[ERROR] Failed to load settings: {e}")
            print("[INFO] Using default settings")
            return deepcopy(self.DEFAULT_SETTINGS)
    
    def _merge_with_defaults(self, loaded: Dict) -> Dict:
        """
        Merge loaded settings with defaults.
        
        This ensures new settings added in updates are present even if
        the user's settings file is from an older version.
        
        Args:
            loaded: Settings loaded from file
            
        Returns:
            Merged settings dictionary
        """
        merged = deepcopy(self.DEFAULT_SETTINGS)
        
        for category, defaults in self.DEFAULT_SETTINGS.items():
            if category in loaded and isinstance(defaults, dict):
                # Merge category settings
                merged[category] = deepcopy(defaults)
                if isinstance(loaded[category], dict):
                    merged[category].update(loaded[category])
            elif category in loaded:
                # Direct value (version, last_modified)
                merged[category] = loaded[category]
        
        return merged
    
    def _save_settings(self, settings: Dict) -> bool:
        """
        Save settings to YAML file.
        
        Args:
            settings: Settings dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Update last modified timestamp
            settings['last_modified'] = datetime.now().isoformat()
            
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(settings, f, default_flow_style=False, sort_keys=False)
            
            print(f"[OK] Settings saved to {self.config_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save settings: {e}")
            return False
    
    def get(self, category: str, key: str, default: Any = None) -> Any:
        """
        Get a specific setting value.
        
        Args:
            category: Settings category (network, audio, display, etc.)
            key: Setting key within category
            default: Value to return if setting not found
            
        Returns:
            Setting value or default
            
        Example:
            >>> manager = SettingsManager()
            >>> volume = manager.get('audio', 'default_volume')
            >>> print(volume)
            75
        """
        if category not in self.settings:
            return default
        
        if not isinstance(self.settings[category], dict):
            return default
        
        return self.settings[category].get(key, default)
    
    def set(self, category: str, key: str, value: Any) -> bool:
        """
        Set a specific setting value and save.
        
        Args:
            category: Settings category
            key: Setting key within category
            value: New value
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> manager = SettingsManager()
            >>> manager.set('audio', 'default_volume', 80)
            [OK] Settings saved to /path/to/config/settings.yaml
            True
        """
        if category not in self.settings:
            print(f"[WARN] Creating new category: {category}")
            self.settings[category] = {}
        
        if not isinstance(self.settings[category], dict):
            print(f"[ERROR] Category {category} is not a dictionary")
            return False
        
        self.settings[category][key] = value
        return self._save_settings(self.settings)
    
    def get_category(self, category: str) -> Dict[str, Any]:
        """
        Get all settings in a category.
        
        Args:
            category: Settings category name
            
        Returns:
            Dictionary of settings in that category
            
        Example:
            >>> manager = SettingsManager()
            >>> audio_settings = manager.get_category('audio')
            >>> print(audio_settings)
            {'default_volume': 75, 'quality_preference': 'balanced', ...}
        """
        if category not in self.settings:
            return {}
        
        if not isinstance(self.settings[category], dict):
            return {}
        
        return deepcopy(self.settings[category])
    
    def set_category(self, category: str, settings: Dict[str, Any]) -> bool:
        """
        Set all settings in a category at once.
        
        Args:
            category: Settings category name
            settings: Dictionary of settings to set
            
        Returns:
            True if successful, False otherwise
            
        Example:
            >>> manager = SettingsManager()
            >>> new_audio = {'default_volume': 90, 'quality_preference': 'audiophile'}
            >>> manager.set_category('audio', new_audio)
            [OK] Settings saved to /path/to/config/settings.yaml
            True
        """
        if not isinstance(settings, dict):
            print("[ERROR] Settings must be a dictionary")
            return False
        
        self.settings[category] = settings
        return self._save_settings(self.settings)
    
    def reset_category(self, category: str) -> bool:
        """
        Reset a category to default settings.
        
        Args:
            category: Settings category to reset
            
        Returns:
            True if successful, False otherwise
        """
        if category not in self.DEFAULT_SETTINGS:
            print(f"[ERROR] Unknown category: {category}")
            return False
        
        self.settings[category] = deepcopy(self.DEFAULT_SETTINGS[category])
        return self._save_settings(self.settings)
    
    def reset_all(self) -> bool:
        """
        Reset all settings to defaults.
        
        Returns:
            True if successful, False otherwise
        """
        self.settings = deepcopy(self.DEFAULT_SETTINGS)
        return self._save_settings(self.settings)
    
    def export_settings(self, export_path: str) -> bool:
        """
        Export current settings to a file (backup).
        
        Args:
            export_path: Path to export file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(export_path, 'w') as f:
                yaml.safe_dump(self.settings, f, default_flow_style=False, sort_keys=False)
            print(f"[OK] Settings exported to {export_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to export settings: {e}")
            return False
    
    def import_settings(self, import_path: str) -> bool:
        """
        Import settings from a file (restore from backup).
        
        Args:
            import_path: Path to import file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(import_path, 'r') as f:
                imported = yaml.safe_load(f)
            
            if imported is None:
                print("[ERROR] Import file is empty")
                return False
            
            # Merge with defaults to ensure all required settings present
            self.settings = self._merge_with_defaults(imported)
            success = self._save_settings(self.settings)
            
            if success:
                print(f"[OK] Settings imported from {import_path}")
            return success
            
        except Exception as e:
            print(f"[ERROR] Failed to import settings: {e}")
            return False
    
    def validate_settings(self) -> list:
        """
        Validate current settings for potential issues.
        
        Returns:
            List of validation warnings (empty if all OK)
        """
        warnings = []
        
        # Validate audio settings
        volume = self.get('audio', 'default_volume', 75)
        if not (0 <= volume <= 100):
            warnings.append(f"Invalid volume: {volume} (must be 0-100)")
        
        quality = self.get('audio', 'quality_preference', 'balanced')
        valid_qualities = ['balanced', 'audiophile', 'crowd_favorite']
        if quality not in valid_qualities:
            warnings.append(f"Invalid quality preference: {quality}")
        
        # Validate display settings
        brightness = self.get('display', 'brightness', 80)
        if not (0 <= brightness <= 100):
            warnings.append(f"Invalid brightness: {brightness} (must be 0-100)")
        
        timeout = self.get('display', 'screen_timeout', 300)
        if timeout < 0:
            warnings.append(f"Invalid screen timeout: {timeout} (must be >= 0)")
        
        # Validate app settings
        last_screen = self.get('app', 'last_screen', 'browse')
        valid_screens = ['player', 'browse', 'settings']
        if last_screen not in valid_screens:
            warnings.append(f"Invalid last_screen: {last_screen}")
        
        return warnings
    
    def display_current_settings(self):
        """Print current settings in a formatted way (for debugging)"""
        print("\n" + "=" * 60)
        print("CURRENT SETTINGS")
        print("=" * 60)
        
        for category in ['network', 'audio', 'display', 'datetime', 'app']:
            if category in self.settings and isinstance(self.settings[category], dict):
                print(f"\n[{category.upper()}]")
                for key, value in self.settings[category].items():
                    print(f"  {key}: {value}")
        
        print(f"\nVersion: {self.settings.get('version', 'unknown')}")
        print(f"Last Modified: {self.settings.get('last_modified', 'never')}")
        print("=" * 60 + "\n")


# Convenience function for getting a global settings instance
_global_settings = None

def get_settings() -> SettingsManager:
    """
    Get the global settings manager instance.
    
    Creates one if it doesn't exist yet.
    
    Returns:
        Global SettingsManager instance
        
    Example:
        >>> from src.settings.settings_manager import get_settings
        >>> settings = get_settings()
        >>> volume = settings.get('audio', 'default_volume')
    """
    global _global_settings
    if _global_settings is None:
        _global_settings = SettingsManager()
    return _global_settings


if __name__ == '__main__':
    """
    Test the settings manager
    """
    print("[INFO] Testing Settings Manager")
    print("-" * 60)
    
    # Create settings manager
    manager = SettingsManager()
    
    # Display current settings
    manager.display_current_settings()
    
    # Test getting values
    print("[TEST] Getting individual settings:")
    volume = manager.get('audio', 'default_volume')
    print(f"  Default volume: {volume}")
    
    brightness = manager.get('display', 'brightness')
    print(f"  Brightness: {brightness}")
    
    last_screen = manager.get('app', 'last_screen')
    print(f"  Last screen: {last_screen}")
    
    # Test setting values
    print("\n[TEST] Setting new values:")
    manager.set('audio', 'default_volume', 85)
    manager.set('display', 'brightness', 90)
    
    # Display after changes
    manager.display_current_settings()
    
    # Test category operations
    print("[TEST] Getting audio category:")
    audio_settings = manager.get_category('audio')
    print(f"  {audio_settings}")
    
    # Test validation
    print("\n[TEST] Validating settings:")
    warnings = manager.validate_settings()
    if warnings:
        print("[WARN] Validation warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("[OK] All settings valid")
    
    print("\n[INFO] Settings manager test complete")
    print(f"[INFO] Settings file: {manager.config_path}")
