"""Core modules for ASTRA Modlist Installer."""

from .constants import (
    BASE_DIR,
    CONFIG_FILE,
    CATEGORIES_FILE,
    LOG_FILE,
    PREFS_FILE,
    CACHE_DIR,
    URL_VALIDATION_TIMEOUT_HEAD,
    REQUEST_TIMEOUT,
    MIN_FREE_SPACE_GB,
)
from .config_manager import ConfigManager
from .installer import ModInstaller

__all__ = [
    # Constants
    'BASE_DIR',
    'CONFIG_FILE',
    'CATEGORIES_FILE',
    'LOG_FILE',
    'PREFS_FILE',
    'CACHE_DIR',
    'URL_VALIDATION_TIMEOUT_HEAD',
    'REQUEST_TIMEOUT',
    'MIN_FREE_SPACE_GB',
    # Classes
    'ConfigManager',
    'ModInstaller',
]
