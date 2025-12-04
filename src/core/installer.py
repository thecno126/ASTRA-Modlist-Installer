"""
Mod installation logic for the Modlist Installer.
Handles downloading and extracting mod archives.
"""

import requests
import zipfile
import threading
import tempfile
import os
from pathlib import Path

try:
    import py7zr
    HAS_7ZIP = True
except ImportError:
    HAS_7ZIP = False

from .constants import REQUEST_TIMEOUT, CHUNK_SIZE


class ModInstaller:
    """Handles the installation of mods from URLs."""
    
    def __init__(self, log_callback):
        """
        Initialize the mod installer.
        
        Args:
            log_callback: Function to call for logging messages
        """
        self.log = log_callback
    
    def install_mod(self, mod, mods_dir):
        """
        Install a single mod (download + extract). For parallel workflows,
        prefer calling download_archive() in threads then extract_archive() sequentially.
        """
        try:
            mod_version = mod.get('version')
            if mod_version:
                self.log(f"  Downloading {mod['name']} v{mod_version}...")
            else:
                self.log(f"  Downloading {mod['name']}...")
            
            self.log(f"  From: {mod['download_url']}")
            
            temp_file, is_7z = self.download_archive(mod)
            if temp_file is None:
                return False
            try:
                self.log(f"  Inspecting archive contents...")
                success = self.extract_archive(temp_file, mods_dir, is_7z)
                if success:
                    self.log(f"  ✓ {mod['name']} installed successfully")
                return success
            finally:
                try:
                    if temp_file and Path(temp_file).exists():
                        Path(temp_file).unlink()
                except Exception:
                    pass
            
        except requests.exceptions.RequestException as e:
            self.log(f"  ✗ Download error: {e}", error=True)
            return False
        except zipfile.BadZipFile:
            self.log(f"  ✗ Error: Corrupted ZIP file", error=True)
            return False
        except Exception as e:
            self.log(f"  ✗ Unexpected error: {e}", error=True)
            return False

    def download_archive(self, mod):
        """Download mod archive to a temporary file. Returns (path, is_7z) or (None, False) on error."""
        try:
            response = requests.get(mod['download_url'], stream=True, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            url_lower = mod['download_url'].lower()
            content_type = response.headers.get('Content-Type', '').lower()
            is_7z = '.7z' in url_lower or '7z' in content_type
            temp_fd = None
            suffix = '.7z' if is_7z else '.zip'
            temp_fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix='modlist_')
            with os.fdopen(temp_fd, 'wb') as f:
                temp_fd = None
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            return temp_path, is_7z
        except requests.exceptions.RequestException as e:
            self.log(f"  ✗ Download error: {e}", error=True)
            try:
                if temp_fd is not None:
                    os.close(temp_fd)
            except Exception:
                pass
            return None, False
        except Exception as e:
            self.log(f"  ✗ Unexpected error during download: {e}", error=True)
            try:
                if temp_fd is not None:
                    os.close(temp_fd)
            except Exception:
                pass
            return None, False
    
    def extract_archive(self, temp_file, mods_dir, is_7z):
        """
        Extract an archive file to the mods directory.
        
        Args:
            temp_file: Path to the temporary archive file
            mods_dir: Path to the Starsector mods directory
            is_7z: Boolean indicating if the file is a 7z archive
            
        Returns:
            bool: True if extraction succeeded, False otherwise
        """
        try:
            if is_7z:
                return self._extract_7z(temp_file, mods_dir)
            else:
                return self._extract_zip(temp_file, mods_dir)
        except Exception as e:
            self.log(f"  ✗ Extraction error: {e}", error=True)
            return False
    
    def _extract_7z(self, temp_file, mods_dir):
        """Extract a 7z archive."""
        if not HAS_7ZIP:
            self.log("  ✗ Error: py7zr library not installed. Install with: pip install py7zr", error=True)
            return False
        
        try:
            with py7zr.SevenZipFile(temp_file, 'r') as archive:
                all_names = archive.getnames()
                members = [m for m in all_names if m and not m.endswith('/')]
                
                if not members:
                    self.log("  ✗ Error: Archive is empty", error=True)
                    return False

                # Check if mod already installed
                already_result = self._is_already_installed(members, mods_dir)
                if already_result:
                    return already_result

                # Validate all members for zip-slip protection
                mods_dir_resolved = mods_dir.resolve()
                for member in all_names:
                    member_path = (mods_dir / member).resolve()
                    try:
                        member_path.relative_to(mods_dir_resolved)
                    except ValueError:
                        self.log(f"  ✗ Security: Attempted path traversal detected in archive (blocked)", error=True)
                        return False

                self.log("  Extracting...")
                archive.extractall(path=mods_dir)
                return True
                
        except py7zr.Bad7zFile:
            self.log(f"  ✗ Error: Corrupted 7z file", error=True)
            return False
    
    def _extract_zip(self, temp_file, mods_dir):
        """Extract a ZIP archive with zip-slip protection."""
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            members = [m for m in zip_ref.namelist() if m and not m.endswith('/')]
            
            if not members:
                self.log("  ✗ Error: Archive is empty", error=True)
                return False

            # Check if mod already installed
            already_result = self._is_already_installed(members, mods_dir)
            if already_result:
                return already_result

            # Validate all members for zip-slip protection
            mods_dir_resolved = mods_dir.resolve()
            for member in zip_ref.namelist():
                member_path = (mods_dir / member).resolve()
                try:
                    member_path.relative_to(mods_dir_resolved)
                except ValueError:
                    self.log(f"  ✗ Security: Attempted path traversal detected in archive (blocked)", error=True)
                    return False

            self.log("  Extracting...")
            zip_ref.extractall(mods_dir)
            return True
    
    def _is_already_installed(self, members, mods_dir):
        """
        Check if a mod is already installed.
        
        Args:
            members: List of file paths in the archive
            mods_dir: Path to the Starsector mods directory
            
        Returns:
            bool: True if mod is already installed, False otherwise
        """
        top_level = set(Path(m).parts[0] for m in members if Path(m).parts)

        if len(top_level) == 1:
            # Archive has a single root folder
            root_dir = next(iter(top_level))
            mod_root = mods_dir / root_dir
            if mod_root.exists():
                self.log(f"  ℹ Skipped: Mod '{root_dir}' already installed", info=True)
                return 'skipped'
        else:
            # Archive has multiple files at root level
            for member in members:
                dest = mods_dir / Path(member)
                if dest.exists():
                    self.log("  ℹ Skipped: Installation would overlap existing files", info=True)
                    return 'skipped'
        
        return False
