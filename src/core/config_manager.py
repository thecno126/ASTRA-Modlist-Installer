"""Configuration and data management for modlist."""
import json
import tempfile
import os
from pathlib import Path

from .constants import CONFIG_FILE, CATEGORIES_FILE, PREFS_FILE


class ConfigManager:
    """Manages configuration files (modlist, categories, preferences)."""
    
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.categories_file = CATEGORIES_FILE
        self.prefs_file = PREFS_FILE
    
    def load_modlist_config(self):
        """Load modlist configuration from JSON file.
        
        Returns:
            dict: Modlist configuration data
        """
        if not self.config_file.exists():
            return self.reset_to_default()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.reset_to_default()
    
    def save_modlist_config(self, data):
        """Save modlist configuration to JSON file atomically.
        
        Args:
            data: Modlist configuration data to save
        """
        try:
            # Ensure parent directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            # Atomic write: write to temp file then replace
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.config_file.parent,
                prefix='.tmp_modlist_',
                suffix='.json'
            )
            try:
                with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                # Atomic replace (preserves file if crash during write)
                os.replace(temp_path, self.config_file)
            except Exception:
                # Cleanup temp file if something failed
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                raise
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def reset_to_default(self):
        """Reset configuration to default values and save.
        
        Returns:
            dict: Default modlist configuration
        """
        default_config = {
            "modlist_name": "ASTRA",
            "version": "1.0",
            "starsector_version": "0.98a-RC8",
            "description": "Starsector Modlist",
            "mods": []
        }
        
        self.save_modlist_config(default_config)
        return default_config
    
    def load_categories(self):
        """Load categories from file or create default ones.
        
        Returns:
            list: List of category names
        """
        if self.categories_file.exists():
            try:
                with open(self.categories_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default categories
        default = ["Required", "Graphics", "Gameplay", "Content", "Quality of Life", "Utility", "Uncategorized"]
        self.save_categories(default)
        return default
    
    def save_categories(self, categories):
        """Save categories to file atomically.
        
        Args:
            categories: List of category names
        """
        try:
            # Ensure parent directory exists
            self.categories_file.parent.mkdir(parents=True, exist_ok=True)
            # Atomic write: write to temp file then replace
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.categories_file.parent,
                prefix='.tmp_categories_',
                suffix='.json'
            )
            try:
                with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                    json.dump(categories, f, indent=2, ensure_ascii=False)
                os.replace(temp_path, self.categories_file)
            except Exception:
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                raise
        except Exception as e:
            print(f"Error saving categories: {e}")
    
    def load_preferences(self):
        """Load user preferences (last Starsector path, theme, etc.)
        
        Returns:
            dict: User preferences
        """
        try:
            if self.prefs_file.exists():
                with open(self.prefs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def save_preferences(self, prefs):
        """Save user preferences atomically.
        
        Args:
            prefs: Dictionary of preferences to save
        """
        try:
            # Ensure parent directory exists
            self.prefs_file.parent.mkdir(parents=True, exist_ok=True)
            # Atomic write: write to temp file then replace
            temp_fd, temp_path = tempfile.mkstemp(
                dir=self.prefs_file.parent,
                prefix='.tmp_prefs_',
                suffix='.json'
            )
            try:
                with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                    json.dump(prefs, f, indent=2)
                os.replace(temp_path, self.prefs_file)
            except Exception:
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                raise
        except Exception as e:
            print(f"Error saving preferences: {e}")
