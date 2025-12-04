# Tests

Suite de tests unitaires pour ASTRA Modlist Installer.

## Exécution

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer tous les tests
pytest

# Avec verbosité
pytest -v

# Tests spécifiques
pytest tests/test_config_manager.py
pytest tests/test_installer.py
```

## Couverture

- `test_config_manager.py`: Tests pour ConfigManager (load/save/reset pour modlist, catégories, préférences)
- `test_installer.py`: Tests pour ModInstaller (téléchargement, extraction ZIP/7z, protection zip-slip, détection déjà installé)

## Structure

```
tests/
├── README.md                  # Ce fichier
├── test_config_manager.py     # Tests ConfigManager
└── test_installer.py          # Tests ModInstaller
```
