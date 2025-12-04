import io
import zipfile
from pathlib import Path

import pytest

from src.core.installer import ModInstaller


class Logger:
    def __init__(self):
        self.messages = []
    def __call__(self, msg, error=False):
        self.messages.append((msg, error))


def make_in_memory_zip(files):
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, mode="w") as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    bio.seek(0)
    return bio.getvalue()


def test_extract_zip_success(tmp_path, monkeypatch):
    # Crée un ZIP simple avec un dossier racine unique
    zip_bytes = make_in_memory_zip({
        "TestMod/README.txt": "hello",
        "TestMod/mod_info.json": "{}",
    })

    # Écrire l'archive sur disque pour passer au flux de l'installer
    archive_path = tmp_path / "archive.zip"
    archive_path.write_bytes(zip_bytes)

    # Mock requests.get pour renvoyer le contenu du ZIP
    class FakeResp:
        status_code = 200
        headers = {"Content-Type": "application/zip"}
        def iter_content(self, chunk_size=8192):
            yield zip_bytes
        def raise_for_status(self):
            return None
    monkeypatch.setattr("src.core.installer.requests.get", lambda url, stream=True, timeout=30: FakeResp())

    logs = Logger()
    installer = ModInstaller(logs)

    mods_dir = tmp_path / "Starsector" / "mods"
    mods_dir.mkdir(parents=True)

    mod = {"name": "TestMod", "download_url": "http://example.com/mod.zip"}
    ok = installer.install_mod(mod, mods_dir)
    assert ok is True
    assert (mods_dir / "TestMod").exists()


def test_zip_slip_blocked(tmp_path, monkeypatch):
    # ZIP avec tentative de traversal
    zip_bytes = make_in_memory_zip({
        "../evil.txt": "boom",
        "TestMod/file.txt": "safe",
    })
    class FakeResp:
        status_code = 200
        headers = {"Content-Type": "application/zip"}
        def iter_content(self, chunk_size=8192):
            yield zip_bytes
        def raise_for_status(self):
            return None
    monkeypatch.setattr("src.core.installer.requests.get", lambda url, stream=True, timeout=30: FakeResp())

    logs = Logger()
    installer = ModInstaller(logs)

    mods_dir = tmp_path / "Starsector" / "mods"
    mods_dir.mkdir(parents=True)

    mod = {"name": "BadMod", "download_url": "http://example.com/bad.zip"}
    ok = installer.install_mod(mod, mods_dir)
    assert ok is False
    # Doit logguer un message de sécurité
    assert any("Security" in m[0] for m in logs.messages)


def test_network_error(tmp_path, monkeypatch):
    class FakeResp:
        def raise_for_status(self):
            raise Exception("Network down")
    monkeypatch.setattr("src.core.installer.requests.get", lambda url, stream=True, timeout=30: FakeResp())

    logs = Logger()
    installer = ModInstaller(logs)
    mods_dir = tmp_path / "Starsector" / "mods"
    mods_dir.mkdir(parents=True)
    ok = installer.install_mod({"name": "NetFail", "download_url": "http://example.com/x.zip"}, mods_dir)
    assert ok is False
    assert any("Download error" in m[0] or "Unexpected" in m[0] for m in logs.messages)


def test_already_installed_single_root(tmp_path, monkeypatch):
    # Create zip with single root folder
    zip_bytes = make_in_memory_zip({
        "ExistingMod/README.txt": "x"
    })
    class FakeResp:
        status_code = 200
        headers = {"Content-Type": "application/zip"}
        def iter_content(self, chunk_size=8192):
            yield zip_bytes
        def raise_for_status(self):
            return None
    monkeypatch.setattr("src.core.installer.requests.get", lambda url, stream=True, timeout=30: FakeResp())

    logs = Logger()
    installer = ModInstaller(logs)
    mods_dir = tmp_path / "Starsector" / "mods"
    (mods_dir / "ExistingMod").mkdir(parents=True)
    ok = installer.install_mod({"name": "ExistingMod", "download_url": "http://example.com/mod.zip"}, mods_dir)
    assert ok is False
    assert any("already installed" in m[0] for m in logs.messages)


def test_overlap_at_root(tmp_path, monkeypatch):
    # Zip with file at root will overlap existing
    zip_bytes = make_in_memory_zip({
        "readme.txt": "x"
    })
    class FakeResp:
        status_code = 200
        headers = {"Content-Type": "application/zip"}
        def iter_content(self, chunk_size=8192):
            yield zip_bytes
        def raise_for_status(self):
            return None
    monkeypatch.setattr("src.core.installer.requests.get", lambda url, stream=True, timeout=30: FakeResp())

    logs = Logger()
    installer = ModInstaller(logs)
    mods_dir = tmp_path / "Starsector" / "mods"
    mods_dir.mkdir(parents=True)
    # Pre-create overlapping file
    (mods_dir / "readme.txt").write_text("existing")
    ok = installer.install_mod({"name": "RootOverlap", "download_url": "http://example.com/mod.zip"}, mods_dir)
    assert ok is False
    assert any(("overlap" in m[0].lower()) or ("skipping" in m[0].lower()) for m in logs.messages)


def test_extract_7z_if_available(tmp_path, monkeypatch):
    try:
        import py7zr  # noqa: F401
    except Exception:
        pytest.skip("py7zr not available")

    # Build a minimal 7z archive in memory using py7zr
    import py7zr
    sevenz_path = tmp_path / "mod.7z"
    with py7zr.SevenZipFile(sevenz_path, 'w') as archive:
        file_path = tmp_path / "TestMod" / "file.txt"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("hello")
        archive.writeall(file_path.parent, arcname="TestMod")

    data = sevenz_path.read_bytes()

    class FakeResp:
        status_code = 200
        headers = {"Content-Type": "application/x-7z-compressed"}
        def iter_content(self, chunk_size=8192):
            yield data
        def raise_for_status(self):
            return None
    monkeypatch.setattr("src.core.installer.requests.get", lambda url, stream=True, timeout=30: FakeResp())

    logs = Logger()
    installer = ModInstaller(logs)
    mods_dir = tmp_path / "Starsector" / "mods"
    mods_dir.mkdir(parents=True)
    ok = installer.install_mod({"name": "SevenZ", "download_url": "http://example.com/mod.7z"}, mods_dir)
    assert ok is True
    assert (mods_dir / "TestMod").exists()
