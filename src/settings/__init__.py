"""
DeadStream Settings Module
Phase 8, Task 8.4: Settings data persistence

This package provides centralized settings management for the application.
"""

from src.settings.settings_manager import SettingsManager, get_settings

__all__ = ['SettingsManager', 'get_settings']
