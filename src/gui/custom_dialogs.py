"""  
Custom styled dialog boxes for ASTRA Modlist Installer.
Provides modern, themed alternatives to standard tkinter messageboxes.
"""
import tkinter as tk


class StyledDialog:
    """Base class for custom styled dialogs."""
    
    def __init__(self, parent, title, message, dialog_type="info", buttons=None):
        """
        Create a styled dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Message to display
            dialog_type: Type of dialog - "info", "success", "error", "warning", "question"
            buttons: List of (label, value) tuples for buttons
        """
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Main content frame
        content_frame = tk.Frame(self.dialog)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Icon and message
        message_frame = tk.Frame(content_frame)
        message_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Icon
        icons = {"info": "ℹ", "success": "✓", "warning": "⚠", "error": "✗", "question": "?"}
        tk.Label(message_frame, text=icons.get(dialog_type, "ℹ"), 
                font=("Arial", 36, "bold")).pack(side=tk.LEFT, padx=(0, 15))
        
        # Message
        tk.Label(message_frame, text=message, font=("Arial", 11),
                wraplength=350, justify=tk.LEFT).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill=tk.X)
        
        # Default buttons
        if buttons is None:
            buttons = [("Yes", True), ("No", False)] if dialog_type == "question" else [("OK", True)]
        
        # Create buttons (reversed for right-to-left packing)
        for i, (label, value) in enumerate(reversed(buttons)):
            tk.Button(button_frame, text=label, command=lambda v=value: self._on_button_click(v),
                     font=("Arial", 10, "bold"), cursor="hand2", padx=20, 
                     pady=10).pack(side=tk.RIGHT, padx=(0, 5) if i > 0 else 0)
        
        # Keyboard bindings
        self.dialog.bind("<Return>", lambda e: self._on_button_click(buttons[0][1]))
        self.dialog.bind("<Escape>", lambda e: self._on_button_click(False if dialog_type == "question" else True))
        
        # Center on parent
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.dialog.winfo_height()) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
    def _on_button_click(self, value):
        """Handle button click."""
        self.result = value
        self.dialog.destroy()
        
    def show(self):
        """Show dialog and wait for result."""
        self.dialog.wait_window()
        return self.result


# Helper functions
def _show_dialog(dialog_type, title, message, parent=None, buttons=None):
    """Internal helper to show any dialog type."""
    if parent is None:
        parent = tk._default_root
    return StyledDialog(parent, title, message, dialog_type, buttons).show()


def showinfo(title, message, parent=None):
    """Show an info dialog."""
    return _show_dialog("info", title, message, parent)


def showsuccess(title, message, parent=None):
    """Show a success dialog."""
    return _show_dialog("success", title, message, parent)


def showerror(title, message, parent=None):
    """Show an error dialog."""
    return _show_dialog("error", title, message, parent)


def showwarning(title, message, parent=None):
    """Show a warning dialog."""
    return _show_dialog("warning", title, message, parent)


def askyesno(title, message, parent=None):
    """Show a yes/no question dialog."""
    return _show_dialog("question", title, message, parent, [("Yes", True), ("No", False)])


def askokcancel(title, message, parent=None):
    """Show an OK/Cancel question dialog."""
    return _show_dialog("question", title, message, parent, [("OK", True), ("Cancel", False)])
