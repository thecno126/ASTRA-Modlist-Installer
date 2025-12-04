"""System theme detection utilities."""
import sys
import subprocess


def detect_system_theme():
    """Detect if system is in dark mode.
    
    Returns:
        str: 'dark' if system is in dark mode, 'light' otherwise
    """
    try:
        if sys.platform == "darwin":  # macOS
            result = subprocess.run(
                ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                capture_output=True,
                text=True
            )
            return 'dark' if result.returncode == 0 and 'Dark' in result.stdout else 'light'
        elif sys.platform == "win32":  # Windows
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                    r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                return 'light' if value == 1 else 'dark'
            except:
                return 'light'
        else:  # Linux and others
            return 'light'
    except:
        return 'light'
