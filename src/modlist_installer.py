"""
ASTRA Modlist Installer - Entry point
Main executable script for the modlist installer application.
"""

import tkinter as tk
from tkinter import ttk

# Import the main window class
from gui import ModlistInstaller


def main():
    """Main entry point for the application."""
    # Create splash screen
    splash_root = tk.Tk()
    splash_root.title("")
    splash_root.overrideredirect(True)
    
    # Get screen dimensions
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    
    # Splash dimensions
    splash_width = 400
    splash_height = 200
    
    # Center splash screen
    x = (screen_width - splash_width) // 2
    y = (screen_height - splash_height) // 2
    splash_root.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
    
    # Splash content
    splash_frame = tk.Frame(splash_root, bg="#2c3e50", bd=2, relief=tk.RAISED)
    splash_frame.pack(fill=tk.BOTH, expand=True)
    
    title_label = tk.Label(
        splash_frame,
        text="Modlist Installer",
        font=("Arial", 24, "bold"),
        bg="#2c3e50",
        fg="white"
    )
    title_label.pack(pady=(40, 10))
    
    loading_label = tk.Label(
        splash_frame,
        text="Loading...",
        font=("Arial", 12),
        bg="#2c3e50",
        fg="#ecf0f1"
    )
    loading_label.pack(pady=10)
    
    # Progress bar
    progress = ttk.Progressbar(
        splash_frame,
        mode='indeterminate',
        length=300
    )
    progress.pack(pady=20)
    progress.start(10)
    
    splash_root.update()
    
    # Function to close splash and show main window
    def show_main_window():
        progress.stop()
        splash_root.destroy()
        root = tk.Tk()
        app = ModlistInstaller(root)
        root.mainloop()
    
    # Schedule main window after delay
    splash_root.after(1500, show_main_window)
    splash_root.mainloop()


if __name__ == "__main__":
    main()
