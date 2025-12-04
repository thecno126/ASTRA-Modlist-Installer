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


class ThemeManager:
    """Centralized theme manager to ensure consistency across all UI components."""
    
    def __init__(self):
        """Initialize theme manager with system theme detection."""
        self.current_theme = detect_system_theme()
        self.colors = {
            'light': {
                'bg': '#f0f0f0',
                'fg': '#000000',
                'listbox_bg': '#ffffff',
                'listbox_fg': '#000000',
                'category_bg': '#34495e',
                'category_fg': '#ffffff',
                'selected_bg': '#3498db',
                'selected_fg': '#ffffff',
                'header_bg': '#34495e',
                'header_fg': '#ffffff',
                # Dialog colors
                'dialog_bg': '#ffffff',
                'dialog_fg': '#2c3e50',
                'dialog_icon_info': '#3498db',
                'dialog_icon_success': '#27ae60',
                'dialog_icon_warning': '#f39c12',
                'dialog_icon_error': '#e74c3c',
                'dialog_icon_question': '#9b59b6',
                # Button colors
                'button_primary_bg': '#2980b9',
                'button_primary_hover': '#1f6799',
                'button_primary_fg': '#ffffff',
                'button_secondary_bg': '#95a5a6',
                'button_secondary_hover': '#7f8c8d',
                'button_secondary_fg': '#2c3e50'
            },
            'dark': {
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'listbox_bg': '#1e1e1e',
                'listbox_fg': '#ffffff',
                'category_bg': '#34495e',
                'category_fg': '#ffffff',
                'selected_bg': '#3498db',
                'selected_fg': '#ffffff',
                'header_bg': '#34495e',
                'header_fg': '#ffffff',
                # Dialog colors
                'dialog_bg': '#2c3e50',
                'dialog_fg': '#ecf0f1',
                'dialog_icon_info': '#5dade2',
                'dialog_icon_success': '#58d68d',
                'dialog_icon_warning': '#f5b041',
                'dialog_icon_error': '#ec7063',
                'dialog_icon_question': '#af7ac5',
                # Button colors
                'button_primary_bg': '#3498db',
                'button_primary_hover': '#2980b9',
                'button_primary_fg': '#ffffff',
                'button_secondary_bg': '#5a6668',
                'button_secondary_hover': '#4a5456',
                'button_secondary_fg': '#ecf0f1'
            }
        }
    
    def get_colors(self):
        """Get current theme colors."""
        return self.colors[self.current_theme]
    
    def get_color(self, key):
        """Get specific color from current theme."""
        return self.colors[self.current_theme].get(key, '#ffffff')
    
    def is_dark_mode(self):
        """Check if dark mode is active."""
        return self.current_theme == 'dark'
    
    def get_dialog_colors(self, dialog_type="info"):
        """
        Get dialog-specific colors for a given dialog type.
        
        Args:
            dialog_type: Type of dialog - "info", "success", "error", "warning", "question"
            
        Returns:
            dict: Dictionary with icon, bg, and fg colors
        """
        theme = self.colors[self.current_theme]
        icon_key = f'dialog_icon_{dialog_type}'
        
        return {
            'icon': theme.get(icon_key, theme['dialog_icon_info']),
            'bg': theme['dialog_bg'],
            'fg': theme['dialog_fg']
        }
    
    def get_button_colors(self, is_primary=True):
        """
        Get button colors.
        
        Args:
            is_primary: If True, returns primary button colors, else secondary
            
        Returns:
            dict: Dictionary with bg, hover, and fg colors
        """
        theme = self.colors[self.current_theme]
        prefix = 'button_primary' if is_primary else 'button_secondary'
        
        return {
            'bg': theme[f'{prefix}_bg'],
            'hover': theme[f'{prefix}_hover'],
            'fg': theme[f'{prefix}_fg']
        }
