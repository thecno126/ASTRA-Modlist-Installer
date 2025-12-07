"""
Tests for Google Drive URL fixing functionality.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from gui.dialogs import fix_google_drive_url
from core.installer import ModInstaller


def test_fix_google_drive_url_with_file_d_format():
    """Test fixing Google Drive URL with /file/d/ID/view format."""
    original = "https://drive.google.com/file/d/1ABC123xyz/view?usp=sharing"
    expected = "https://drive.usercontent.google.com/download?id=1ABC123xyz&export=download&confirm=t"
    assert fix_google_drive_url(original) == expected


def test_fix_google_drive_url_with_id_param():
    """Test fixing Google Drive URL with ?id=ID format."""
    original = "https://drive.google.com/uc?id=1ABC123xyz&export=download"
    expected = "https://drive.usercontent.google.com/download?id=1ABC123xyz&export=download&confirm=t"
    assert fix_google_drive_url(original) == expected


def test_fix_google_drive_url_non_google():
    """Test that non-Google Drive URLs are not modified."""
    original = "https://example.com/mod.zip"
    assert fix_google_drive_url(original) == original


def test_fix_google_drive_url_no_id():
    """Test Google Drive URL without extractable ID."""
    original = "https://drive.google.com/invalid"
    assert fix_google_drive_url(original) == original

