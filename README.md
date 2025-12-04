# ASTRA Modlist Installer

![Tests](https://github.com/VOTRE_USERNAME/ASTRA-Modlist-Installer/workflows/Tests/badge.svg)
![Build](https://github.com/VOTRE_USERNAME/ASTRA-Modlist-Installer/workflows/Build%20and%20Release/badge.svg)

Outil pour gérer et installer des modlists Starsector avec téléchargements parallèles et interface graphique intuitive.

## ✨ Fonctionnalités

- 📦 Installation automatique de mods depuis des URLs
- ⚡ Téléchargements parallèles (3 workers par défaut)
- 🔒 Protection zip-slip et validation des archives
- 📊 Gestion de catégories et réorganisation des mods
- 💾 Sauvegarde atomique des configurations
- 🎨 Interface Tkinter moderne avec barre de progression
- 📋 Import/Export CSV pour partager vos modlists
- ✅ 10 tests unitaires avec pytest

## 🚀 Quick Start

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Utilisation

**Installer les mods :**
```bash
python src/modlist_installer.py
```

### 📦 Création d'exécutables

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

Les exécutables seront créés dans le dossier `dist/`

Pour plus de détails, consultez [build_scripts/BUILD.md](build_scripts/BUILD.md)

### 🤖 Build automatique avec GitHub Actions

**Pour chaque release (tag `v*`)** :
1. Créez un tag : `git tag v1.0.0 && git push origin v1.0.0`
2. GitHub Actions compile automatiquement pour :
   - 🍎 macOS (.app)
   - 🪟 Windows (.exe)
   - 🐧 Linux (binaire)
3. Les exécutables sont attachés à la release GitHub

**Tests automatiques** : Chaque push sur `main` ou `develop` lance les tests.

## 📁 Structure du projet

```
ASTRA-Modlist-Installer/
├── .github/
│   └── workflows/            # CI/CD automatisé
│       ├── build-release.yml # Build multi-plateforme
│       └── tests.yml         # Tests automatiques
├── src/                      # Code source
│   ├── modlist_installer.py  # Point d'entrée
│   ├── core/                 # Logique métier
│   │   ├── constants.py      # Constantes et chemins
│   │   ├── config_manager.py # Gestion config (atomique)
│   │   └── installer.py      # Téléchargement et extraction
│   ├── gui/                  # Interface utilisateur
│   │   ├── main_window.py    # Fenêtre principale
│   │   ├── dialogs.py        # Boîtes de dialogue
│   │   └── ui_builder.py     # Constructeur UI
│   └── utils/                # Utilitaires
│       └── theme.py          # Détection thème système
├── tests/                    # Tests unitaires
│   ├── test_config_manager.py
│   └── test_installer.py
├── build_scripts/            # Scripts de compilation
│   ├── modlist_installer.spec
│   ├── build.sh / build.bat
│   └── BUILD.md
├── config/                   # Fichiers de configuration
│   ├── modlist_config.json
│   ├── categories.json
│   └── installer_prefs.json
└── requirements.txt          # Dépendances Python
```

## 📚 Documentation

- **README.md** (ce fichier) - Guide de démarrage rapide
- **build_scripts/BUILD.md** - Guide de compilation et distribution
- **tests/README.md** - Documentation des tests

## ✨ Fonctionnalités détaillées

**Modlist Installer** - Install and manage Starsector mods

**Core Features:**
- Auto-detect Starsector installation path (Windows/macOS/Linux)
- GUI for managing mods (add, remove, reorder, categorize)
- Import/export modlists from CSV
- Install mods from URLs (ZIP and 7z archives)
- Skip already-installed mods automatically
- Progress tracking and detailed logging
- System theme detection (light/dark mode)
- Mod categories management

**Usage:**
```bash
python src/modlist_installer.py
```

**Managing Mods:**
- Use the GUI to add mods individually with URL validation
- Import mods from CSV files
- Organize mods by categories
- Reorder mods within categories
- Export your modlist to CSV

**CSV Import Format** (via GUI):
```csv
name,category,download_url,version
LazyLib,Required,https://example.com/lazylib.zip,2.8
Nexerelin,Gameplay,https://example.com/nexerelin.7z,0.11.2b
```
- `version` et `category` sont optionnels
- Supporte également `url` comme nom de colonne au lieu de `download_url`

**Modlist metadata** (optional CSV header):
```csv
modlist_name,modlist_version,starsector_version,modlist_description
My Modlist,1.0,0.97a-RC11,Description de ma modlist
name,category,download_url,version
LazyLib,Required,https://example.com/lazylib.zip,2.8
```

The first line can contain modlist metadata (detected if it lacks a `download_url` field).

## ⚙️ Configuration

Les mods sont stockés dans `modlist_config.json` :

```json
{
  "modlist_name": "My Custom Modlist",
  "version": "1.0",
  "starsector_version": "0.97a-RC11",
  "description": "A selection of mods",
  "mods": [
    {
      "name": "LazyLib",
      "download_url": "https://example.com/lazylib.zip",
      "version": "2.8"
    }
  ]
}
```

**Champs obligatoires par mod :**
- `name` : Nom du mod
- `download_url` : Lien de téléchargement direct (ZIP ou 7z)

**Champs optionnels :**
- `version` : Version du mod (affichage uniquement)

## 📦 Dépendances

Installez les bibliothèques requises :
```bash
pip install -r requirements.txt
```

**Bibliothèques nécessaires :**
- `requests>=2.31.0` - Téléchargements HTTP et validation d'URL
- `py7zr>=0.20.0` - Support des archives 7zip (optionnel, fonctionne sans pour ZIP uniquement)

## 🔄 Workflow

1. **Ajouter des mods :** Utilisez l'interface graphique pour construire votre modlist
   - Ajoutez des mods individuellement via le bouton "Add Mod"
   - Ou importez depuis un fichier CSV ("Import CSV")
   - Organisez par catégories et réordonnez selon vos préférences
2. **Installer les mods :** Cliquez sur "Install Modlist" pour tout télécharger et installer
   - Détection automatique du chemin Starsector
   - Support ZIP et 7z
   - Détection des doublons et mods déjà installés

## 📝 Notes

- Les mods en double (par nom ou URL) sont automatiquement évités
- Le type d'archive (ZIP/7z) est détecté automatiquement depuis l'extension d'URL ou l'en-tête Content-Type
- Les mods avec un dossier de premier niveau unique sont installés tels quels
- Les archives multi-fichiers sont extraites directement
- Les mods déjà installés sont ignorés automatiquement
