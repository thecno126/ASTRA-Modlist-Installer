# ASTRA Modlist Installer - Guide de Build & Distribution

## 🚀 Quick Start

### Création des exécutables

**Sur macOS/Linux :**
```bash
cd build_scripts
chmod +x build.sh  # Première fois uniquement
./build.sh
```

**Sur Windows :**
```cmd
cd build_scripts
build.bat
```

Les exécutables seront créés dans le dossier `../dist/`

---

## Project Structure

```
ASTRA-Modlist-Installer/
├── src/
│   ├── modlist_installer.py      # Main application entry point
│   ├── core/                     # Core modules
│   │   ├── installer.py          # Mod installation logic
│   │   ├── config_manager.py     # Configuration management
│   │   └── constants.py          # App constants
│   ├── gui/                      # GUI components
│   │   ├── main_window.py        # Main window
│   │   ├── dialogs.py            # Dialog windows
│   │   └── ui_builder.py         # UI construction
│   └── utils/                    # Utilities
│       └── theme.py              # Theme detection
├── build_scripts/
│   ├── modlist_installer.spec    # PyInstaller config
│   ├── build.sh                  # macOS/Linux build script
│   ├── build.bat                 # Windows build script
│   └── BUILD.md                  # This file
├── dist/                         # Built executables (after build)
├── requirements.txt              # Python dependencies
├── modlist_config.json           # Modlist configuration
├── categories.json               # Mod categories
└── README.md                     # Main documentation

```

---

## 🛠️ Instructions de Build Manuel

Si vous préférez compiler manuellement :

### 1. Installer PyInstaller
```bash
# Sur macOS/Linux avec Python 3.14+
pip3 install --break-system-packages pyinstaller

# Sur Windows ou avec environnement virtuel
pip install pyinstaller
```

### 2. Compiler l'application
```bash
cd build_scripts
pyinstaller --clean -y --distpath ../dist --workpath ../build modlist_installer.spec
```

---

## 🎨 Personnalisation

### Ajouter une icône

**Pour Windows (.ico) :**
1. Créez/obtenez un fichier `.ico` de 256x256
2. Placez-le à la racine du projet en tant que `icon.ico`
3. Éditez `build_scripts/modlist_installer.spec` :
   ```python
   icon='../icon.ico',  # Pour Windows
   ```

**Pour macOS (.icns) :**
1. Créez/obtenez un fichier `.icns`
2. Placez-le à la racine du projet en tant que `icon.icns`
3. Éditez le fichier `.spec` :
   ```python
   icon='../icon.icns',  # Pour macOS
   ```

### Optimizing Build Size

To reduce executable size, edit `.spec` files:

1. **Enable UPX compression** (already enabled):
   ```python
   upx=True,
   ```

2. **Exclude unused modules** (already configured):
   ```python
   excludes=[
       'matplotlib', 'numpy', 'pandas', 'scipy', 'PIL', 'pytest',
   ],
   ```

3. **One-folder mode** (smaller but multiple files):
   Change in `.spec`:
   ```python
   exe = EXE(
       pyz,
       a.scripts,
       # Comment out these lines for one-folder:
       # a.binaries,
       # a.zipfiles,
       # a.datas,
       ...
   )
   
   coll = COLLECT(
       exe,
       a.binaries,
       a.zipfiles,
       a.datas,
       ...
   )
   ```

---

## Platform-Specific Notes

### macOS

**Code Signing (for distribution):**
```bash
codesign --deep --force --sign - dist/Modlist-Installer.app
```

**Creating a DMG installer:**
```bash
# Install create-dmg if needed
brew install create-dmg

# Create DMG
create-dmg \
  --volname "ASTRA Modlist Installer" \
  --window-size 600 400 \
  --icon-size 100 \
  --app-drop-link 450 150 \
  dist/ASTRA-Modlist-Installer.dmg \
  dist/Modlist-Installer.app
```

**Notarization (for Gatekeeper):**
Requires Apple Developer account. See: https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution

### Windows

**Creating an Installer:**

Use **Inno Setup** (free):
1. Download: https://jrsoftware.org/isdl.php
2. Create script (`installer.iss`):
   ```iss
   [Setup]
   AppName=ASTRA Modlist Installer
   AppVersion=1.0
   DefaultDirName={pf}\ASTRA
   OutputDir=dist
   OutputBaseFilename=ASTRA-Installer-Setup
   
   [Files]
   Source: "dist\Modlist-Installer.exe"; DestDir: "{app}"
   
   [Icons]
   Name: "{group}\Modlist Installer"; Filename: "{app}\Modlist-Installer.exe"
   ```

### Linux

**Creating a .deb package:**
```bash
# Create package structure
mkdir -p astra-installer_1.0/usr/local/bin
cp dist/Modlist-Installer astra-installer_1.0/usr/local/bin/

# Create control file
mkdir -p astra-installer_1.0/DEBIAN
cat > astra-installer_1.0/DEBIAN/control << EOF
Package: astra-installer
Version: 1.0
Architecture: amd64
Maintainer: Your Name
Description: ASTRA Modlist Installer
EOF

# Build package
dpkg-deb --build astra-installer_1.0
```

---

## 🔧 Dépannage

### "ModuleNotFoundError" lors de l'exécution de l'exécutable
- Ajoutez le module manquant à `hiddenimports` dans le fichier `.spec`
- Recompilez avec `./build.sh` ou `build.bat`

### Exécutable trop volumineux
- Activez la compression UPX (`upx=True` - déjà activé)
- Ajoutez les bibliothèques inutilisées à la liste `excludes`
- Utilisez le mode one-folder au lieu de one-file

### macOS : "L'app est endommagée et ne peut pas être ouverte"
```bash
xattr -cr ../dist/Modlist-Installer.app
```

### Windows : Faux positif antivirus
- Signez le code de l'exécutable (nécessite un certificat)
- Ou ajoutez une exception dans l'antivirus

### Python 3.14+ : "externally-managed-environment"
```bash
# Utilisez --break-system-packages (déjà intégré dans build.sh)
pip3 install --break-system-packages pyinstaller

# Ou créez un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install pyinstaller
```

---

## Dependencies

All dependencies are managed via `requirements.txt`:
```
requests>=2.31.0
py7zr>=0.20.0
```

PyInstaller will automatically bundle these.

---

## Distribution Checklist

Before releasing:

- [ ] Test executable on clean machine (no Python installed)
- [ ] Verify all features work (download, extract, UI)
- [ ] Check file size is reasonable
- [ ] Test on target OS version
- [ ] Include `modlist_config.json` example
- [ ] Write release notes
- [ ] Create installer/package (optional but recommended)
- [ ] Code sign (macOS/Windows for trusted distribution)

---

## Advanced: Cross-Platform Builds

**Note:** Generally, you need to build on each target platform.

**Docker alternative (Linux → Windows):**
```bash
docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows
```

**GitHub Actions for automated builds:**
Create `.github/workflows/build.yml` for CI/CD builds on all platforms.
