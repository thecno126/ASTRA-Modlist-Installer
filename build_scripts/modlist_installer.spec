# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Modlist Installer
Optimized for Windows and macOS builds
"""

block_cipher = None

a = Analysis(
    ['../src/modlist_installer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'requests',
        'py7zr',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        # Application modules
        'utils',
        'utils.theme',
        'core',
        'core.config_manager',
        'core.downloader',
        'gui',
        'gui.main_window',
        'gui.dialogs',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Modlist-Installer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows specific
    icon=None,  # Add 'icon.ico' here if you have one
    # macOS specific
    # icon='icon.icns',  # Uncomment and add icon file for macOS
)

# macOS app bundle (only used on macOS)
app = BUNDLE(
    exe,
    name='Modlist-Installer.app',
    icon=None,  # Add 'icon.icns' here for macOS
    bundle_identifier='com.astra.modlist.installer',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
    },
)
