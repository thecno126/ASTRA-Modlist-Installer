# Build Scripts

## Automated Builds via GitHub Actions

This project uses **GitHub Actions** for automated builds across all platforms:
- Linux (Ubuntu)
- Windows
- macOS

### How it works

1. Push a tag starting with `v` (e.g., `v1.0.0`)
2. GitHub Actions automatically builds executables for all platforms
3. Artifacts are uploaded to the GitHub Release

### Build Configuration

The build process is defined in `.github/workflows/build-release.yml` and uses the PyInstaller spec file:
- `modlist_installer.spec` - PyInstaller configuration

### Manual Local Build (Optional)

If you need to build locally for testing:

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build
pyinstaller build_scripts/modlist_installer.spec --clean --noconfirm
```

**Note:** Local builds are only needed for testing. All official releases are built by GitHub Actions.
