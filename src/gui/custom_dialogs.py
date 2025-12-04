"""
Custom styled dialog boxes for ASTRA Modlist Installer.
Provides modern, themed alternatives to standard tkinter messageboxes.
"""
import tkinter as tk
from utils import ThemeManager


class StyledDialog:
    """Base class for custom styled dialogs."""
    
    def __init__(self, parent, title, message, dialog_type="info", buttons=None, theme_manager=None):
        """
        Create a styled dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Message to display
            dialog_type: Type of dialog - "info", "success", "error", "warning", "question"
            buttons: List of button labels (defaults based on dialog_type)
            theme_manager: ThemeManager instance (will create one if not provided)
        """
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog modal and centered
        self.dialog.resizable(False, False)
        
        # Use provided theme manager or create new one
        self.theme_manager = theme_manager or ThemeManager()
        
        # Get colors from theme manager
        self.color_scheme = self.theme_manager.get_dialog_colors(dialog_type)
        
        # Configure dialog appearance
        self.dialog.configure(bg=self.color_scheme["bg"])
        
        # Main content frame with padding
        content_frame = tk.Frame(self.dialog, bg=self.color_scheme["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icon and message frame
        message_frame = tk.Frame(content_frame, bg=self.color_scheme["bg"])
        message_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Icon (emoji-style)
        icon_map = {
            "info": "ℹ",
            "success": "✓",
            "warning": "⚠",
            "error": "✗",
            "question": "?"
        }
        icon = icon_map.get(dialog_type, "ℹ")
        
        icon_label = tk.Label(
            message_frame,
            text=icon,
            font=("Arial", 36, "bold"),
            fg=self.color_scheme["icon"],
            bg=self.color_scheme["bg"]
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Message text
        message_label = tk.Label(
            message_frame,
            text=message,
            font=("Arial", 11),
            fg=self.color_scheme["fg"],
            bg=self.color_scheme["bg"],
            wraplength=350,
            justify=tk.LEFT
        )
        message_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Buttons frame
        button_frame = tk.Frame(content_frame, bg=self.color_scheme["bg"])
        button_frame.pack(fill=tk.X)
        
        # Default buttons based on type
        if buttons is None:
            if dialog_type == "question":
                buttons = [("Yes", True), ("No", False)]
            else:
                buttons = [("OK", True)]
        
        # Create buttons (reversed iteration since we pack from right)
        for i, (label, value) in enumerate(reversed(buttons)):
            # All buttons use secondary (No/Cancel) style
            btn_colors = self.theme_manager.get_button_colors(is_primary=False)
            
            btn = tk.Button(
                button_frame,
                text=label,
                command=lambda v=value: self._on_button_click(v),
                font=("Arial", 10, "bold"),
                bg=btn_colors['bg'],
                fg=btn_colors['fg'],
                activebackground=btn_colors['hover'],
                activeforeground=btn_colors['fg'],
                disabledforeground=btn_colors['fg'],
                relief=tk.FLAT,
                cursor="hand2",
                padx=20,
                pady=10,
                borderwidth=0,
                highlightthickness=0,
                highlightbackground=btn_colors['bg'],
                highlightcolor=btn_colors['bg']
            )
            btn.pack(side=tk.RIGHT, padx=(0, 5) if i > 0 else 0)
            
            # Hover effects with theme colors
            btn.bind("<Enter>", lambda e, b=btn, colors=btn_colors: 
                     b.configure(bg=colors['hover'], fg=colors['fg']))
            btn.bind("<Leave>", lambda e, b=btn, colors=btn_colors: 
                     b.configure(bg=colors['bg'], fg=colors['fg']))
        
        # Keyboard bindings
        self.dialog.bind("<Return>", lambda e: self._on_button_click(buttons[0][1]))
        if dialog_type == "question":
            self.dialog.bind("<Escape>", lambda e: self._on_button_click(False))
        else:
            self.dialog.bind("<Escape>", lambda e: self._on_button_click(True))
        
        # Center dialog on parent
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
    def _on_button_click(self, value):
        """Handle button click."""
        self.result = value
        self.dialog.destroy()
        
    def show(self):
        """Show dialog and wait for result."""
        self.dialog.wait_window()
        return self.result


def showinfo(title, message, parent=None, theme_manager=None):
    """Show an info dialog."""
    if parent is None:
        parent = tk._default_root
    dialog = StyledDialog(parent, title, message, "info", theme_manager=theme_manager)
    return dialog.show()


def showsuccess(title, message, parent=None, theme_manager=None):
    """Show a success dialog."""
    if parent is None:
        parent = tk._default_root
    dialog = StyledDialog(parent, title, message, "success", theme_manager=theme_manager)
    return dialog.show()


def showerror(title, message, parent=None, theme_manager=None):
    """Show an error dialog."""
    if parent is None:
        parent = tk._default_root
    dialog = StyledDialog(parent, title, message, "error", theme_manager=theme_manager)
    return dialog.show()


def showwarning(title, message, parent=None, theme_manager=None):
    """Show a warning dialog."""
    if parent is None:
        parent = tk._default_root
    dialog = StyledDialog(parent, title, message, "warning", theme_manager=theme_manager)
    return dialog.show()


def askyesno(title, message, parent=None, theme_manager=None):
    """Show a yes/no question dialog."""
    if parent is None:
        parent = tk._default_root
    dialog = StyledDialog(parent, title, message, "question", [("Yes", True), ("No", False)], theme_manager=theme_manager)
    return dialog.show()


def askokcancel(title, message, parent=None, theme_manager=None):
    """Show an OK/Cancel question dialog."""
    if parent is None:
        parent = tk._default_root
    dialog = StyledDialog(parent, title, message, "question", [("OK", True), ("Cancel", False)], theme_manager=theme_manager)
    return dialog.show()
