import json
import os
from pathlib import Path

import pytest

from src.core.config_manager import ConfigManager
from src.core.constants import CONFIG_FILE, CATEGORIES_FILE, PREFS_FILE


def test_load_default_when_missing(tmp_path, monkeypatch):
    # Rediriger les chemins de config vers un dossier temporaire
    base = tmp_path
    monkeypatch.setenv("PYTEST_BASE_DIR", str(base))

    # Simuler des chemins en remplaçant les attributs de l'instance
    cm = ConfigManager()
    cm.config_file = base / "config" / "modlist_config.json"
    cm.categories_file = base / "config" / "categories.json"
    cm.prefs_file = base / "config" / "installer_prefs.json"

    data = cm.load_modlist_config()
    assert isinstance(data, dict)
    assert data.get("mods") == []
    assert cm.config_file.exists(), "Le fichier de config doit être créé lors du reset"


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    base = tmp_path
    cm = ConfigManager()
    cm.config_file = base / "config" / "modlist_config.json"

    payload = {
        "modlist_name": "ASTRA",
        "version": "1.1",
        "starsector_version": "0.98a",
        "description": "desc",
        "mods": [{"name": "TestMod", "download_url": "http://example.com/mod.zip"}]
    }

    cm.save_modlist_config(payload)
    loaded = cm.load_modlist_config()
    assert loaded == payload


def test_categories_roundtrip(tmp_path):
    cm = ConfigManager()
    cm.categories_file = tmp_path / "config" / "categories.json"

    cats = ["Required", "Gameplay", "QoL"]
    cm.save_categories(cats)
    assert cm.categories_file.exists()
    loaded = cm.load_categories()
    assert loaded == cats


def test_preferences_roundtrip(tmp_path):
    cm = ConfigManager()
    cm.prefs_file = tmp_path / "config" / "installer_prefs.json"

    prefs = {"last_starsector_path": str(tmp_path), "theme": "dark"}
    cm.save_preferences(prefs)
    loaded = cm.load_preferences()
    assert loaded == prefs
