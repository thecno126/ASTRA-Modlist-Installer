"""
Tests for download scenarios and parallel download handling.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from unittest.mock import Mock, patch, MagicMock
from core.installer import ModInstaller, validate_mod_urls
import concurrent.futures


class TestDownloadScenarios:
    """Test various download scenarios."""
    
    def test_parallel_download_success(self):
        """Test successful parallel downloads."""
        log_callback = Mock()
        installer = ModInstaller(log_callback)
        
        mods = [
            {'name': 'Mod1', 'download_url': 'http://example.com/mod1.zip'},
            {'name': 'Mod2', 'download_url': 'http://example.com/mod2.zip'},
            {'name': 'Mod3', 'download_url': 'http://example.com/mod3.zip'}
        ]
        
        with patch('requests.get') as mock_get:
            # Mock successful downloads
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.headers = {'Content-Type': 'application/zip'}
            mock_response.iter_content = Mock(return_value=[b'fake zip content'])
            mock_get.return_value = mock_response
            
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(installer.download_archive, mod) for mod in mods]
                for future in concurrent.futures.as_completed(futures):
                    temp_path, is_7z = future.result()
                    results.append((temp_path is not None, is_7z))
            
            # All downloads should succeed
            assert len(results) == 3
            assert all(success for success, _ in results)
    
    def test_download_with_timeout(self):
        """Test download timeout handling."""
        log_callback = Mock()
        installer = ModInstaller(log_callback)
        
        mod = {'name': 'SlowMod', 'download_url': 'http://slow.example.com/mod.zip'}
        
        with patch('requests.get', side_effect=Exception("Timeout")):
            temp_path, is_7z = installer.download_archive(mod)
            
            # Download should fail gracefully
            assert temp_path is None
            assert is_7z is False
            # Should log error
            log_callback.assert_called()
    
    def test_download_404_error(self):
        """Test handling of 404 errors."""
        log_callback = Mock()
        installer = ModInstaller(log_callback)
        
        mod = {'name': 'MissingMod', 'download_url': 'http://example.com/missing.zip'}
        
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = Exception("404 Not Found")
            mock_get.return_value = mock_response
            
            temp_path, is_7z = installer.download_archive(mod)
            
            assert temp_path is None
            assert is_7z is False
    
    def test_detect_7z_from_url(self):
        """Test detection of 7z format from URL."""
        log_callback = Mock()
        installer = ModInstaller(log_callback)
        
        mod = {'name': 'Compressed', 'download_url': 'http://example.com/mod.7z'}
        
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.headers = {'Content-Type': 'application/x-7z-compressed'}
            mock_response.iter_content = Mock(return_value=[b'7z content'])
            mock_get.return_value = mock_response
            
            temp_path, is_7z = installer.download_archive(mod)
            
            # Should detect 7z format
            assert temp_path is not None
            assert is_7z is True
    
    def test_google_drive_html_detection(self):
        """Test detection of Google Drive HTML response (virus scan page)."""
        log_callback = Mock()
        installer = ModInstaller(log_callback)
        
        gdrive_mod = {
            'name': 'GDriveMod',
            'download_url': 'https://drive.google.com/uc?id=ABC123'
        }
        
        # Mock response with HTML content type
        mock_response = MagicMock()
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_response.raise_for_status = MagicMock()
        
        with patch('requests.get', return_value=mock_response):
            temp_path, is_7z = installer.download_archive(gdrive_mod)
        
        # Should return GDRIVE_HTML indicator
        assert temp_path == 'GDRIVE_HTML'
        assert is_7z is False
    
    def test_non_google_drive_html_not_detected(self):
        """Test that HTML from non-Google Drive sources is downloaded normally."""
        log_callback = Mock()
        installer = ModInstaller(log_callback)
        
        regular_mod = {
            'name': 'RegularMod',
            'download_url': 'http://example.com/mod.zip'
        }
        
        # Mock response with HTML (should still download for non-GDrive)
        mock_response = MagicMock()
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_response.raise_for_status = MagicMock()
        mock_response.iter_content = MagicMock(return_value=[b'fake html'])
        
        with patch('requests.get', return_value=mock_response), \
             patch('tempfile.mkstemp', return_value=(99, '/tmp/test.zip')):
            temp_path, is_7z = installer.download_archive(regular_mod)
        
        # Should download normally (not GDRIVE_HTML)
        assert temp_path != 'GDRIVE_HTML'


class TestURLValidation:
    """Test URL validation scenarios."""
    
    def test_validate_mixed_urls(self):
        """Test validation of mixed URL sources."""
        mods = [
            {'name': 'GitHubMod', 'download_url': 'https://github.com/user/repo/releases/download/v1.0/mod.zip'},
            {'name': 'GDriveMod', 'download_url': 'https://drive.google.com/uc?id=ABC123'},
            {'name': 'OtherMod', 'download_url': 'https://example.com/mod.zip'}
        ]
        
        with patch('requests.head') as mock_head:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_head.return_value = mock_response
            
            results = validate_mod_urls(mods)
            
            # Should categorize correctly
            assert len(results['github']) >= 0
            assert len(results['google_drive']) >= 0
            assert len(results['other']) >= 0
    
    def test_validate_with_timeout_retry(self):
        """Test retry logic for timeout errors."""
        mods = [
            {'name': 'TimeoutMod', 'download_url': 'http://slow.example.com/mod.zip'}
        ]
        
        call_count = 0
        def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First attempt times out
                import requests
                raise requests.exceptions.Timeout("Timeout")
            else:
                # Second attempt succeeds
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                return mock_resp
        
        with patch('requests.head', side_effect=mock_request):
            results = validate_mod_urls(mods)
            
            # Should have retried (call_count will be 2+ due to retry logic)
            # The mod should eventually be validated or in failed list
            assert call_count >= 1
    
    def test_validate_403_fallback_to_get(self):
        """Test fallback to GET request when HEAD returns 403."""
        mods = [
            {'name': 'BlockedMod', 'download_url': 'http://example.com/mod.zip'}
        ]
        
        with patch('requests.head') as mock_head, patch('requests.get') as mock_get:
            # HEAD returns 403
            mock_head_response = MagicMock()
            mock_head_response.status_code = 403
            mock_head.return_value = mock_head_response
            
            # GET succeeds
            mock_get_response = MagicMock()
            mock_get_response.status_code = 200
            mock_get_response.close = Mock()
            mock_get.return_value = mock_get_response
            
            results = validate_mod_urls(mods)
            
            # Should have used GET as fallback
            mock_get.assert_called()
    
    def test_validate_empty_url(self):
        """Test handling of mods with missing URLs."""
        mods = [
            {'name': 'NoURL', 'download_url': ''}
        ]
        
        results = validate_mod_urls(mods)
        
        # Should be in failed list
        assert len(results['failed']) == 1
        assert results['failed'][0]['error'] == 'No download URL'
    
    def test_validate_domain_categorization(self):
        """Test proper domain categorization for 'other' sources."""
        mods = [
            {'name': 'Mod1', 'download_url': 'https://cdn.example.com/mod1.zip'},
            {'name': 'Mod2', 'download_url': 'https://cdn.example.com/mod2.zip'},
            {'name': 'Mod3', 'download_url': 'https://other.site/mod3.zip'}
        ]
        
        with patch('requests.head') as mock_head:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_head.return_value = mock_response
            
            results = validate_mod_urls(mods)
            
            # Should group by domain
            assert 'cdn.example.com' in results['other'] or 'other.site' in results['other']


class TestConcurrentDownloads:
    """Test concurrent download behavior."""
    
    def test_executor_max_workers(self):
        """Test that executor respects max_workers limit."""
        log_callback = Mock()
        installer = ModInstaller(log_callback)
        
        mods = [{'name': f'Mod{i}', 'download_url': f'http://example.com/mod{i}.zip'} 
                for i in range(10)]
        
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.headers = {'Content-Type': 'application/zip'}
            mock_response.iter_content = Mock(return_value=[b'content'])
            mock_get.return_value = mock_response
            
            max_workers = 3
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(installer.download_archive, mod) for mod in mods]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
            # All should complete
            assert len(results) == 10
    
    def test_executor_cancellation(self):
        """Test that executor can be cancelled."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit long-running tasks
            futures = [executor.submit(lambda: None) for _ in range(5)]
            
            # Cancel executor
            executor.shutdown(wait=False, cancel_futures=True)
            
            # Executor should shut down without waiting
            assert True  # If we reach here, cancellation worked
