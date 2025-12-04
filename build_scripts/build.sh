#!/bin/bash
# Build script for ASTRA Modlist Installer
# Builds executables for the current platform (Windows/macOS/Linux)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== ASTRA Modlist Installer Build Script ===${NC}"
echo ""

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    PLATFORM="Windows"
else
    PLATFORM="Linux"
fi

echo -e "${BLUE}Detected platform: ${PLATFORM}${NC}"
echo ""

# Check for virtual environment and use it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv"
if [ ! -d "$VENV_PATH" ]; then
    VENV_PATH="$PROJECT_ROOT/venv"
fi

if [ -d "$VENV_PATH" ]; then
    echo -e "${BLUE}Using virtual environment...${NC}"
    PYTHON_CMD="$VENV_PATH/bin/python"
    PIP_CMD="$VENV_PATH/bin/pip"
else
    echo -e "${YELLOW}No virtual environment found, using system Python...${NC}"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

# Ensure dependencies are installed
echo -e "${BLUE}Checking dependencies...${NC}"
"$PIP_CMD" install -q -r "$PROJECT_ROOT/requirements.txt" 2>/dev/null || "$PIP_CMD" install -r "$PROJECT_ROOT/requirements.txt"

# Check if PyInstaller is installed
if ! "$PIP_CMD" show pyinstaller &> /dev/null; then
    echo -e "${RED}PyInstaller not found. Installing...${NC}"
    "$PIP_CMD" install pyinstaller
fi

# Use the venv's pyinstaller
if [ -d "$VENV_PATH" ]; then
    PYINSTALLER_CMD="$VENV_PATH/bin/pyinstaller"
else
    PYINSTALLER_CMD="pyinstaller"
fi

# Create dist directory if it doesn't exist
mkdir -p ../dist

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf ../build ../dist/*.app ../dist/*.exe ../dist/Modlist-Installer ../dist/Modlist-Configurator

# Build Installer
echo ""
echo -e "${GREEN}Building Modlist Installer...${NC}"
"$PYINSTALLER_CMD" --clean -y --distpath ../dist --workpath ../build modlist_installer.spec

# Platform-specific post-build steps
if [[ "$PLATFORM" == "macOS" ]]; then
    echo ""
    echo -e "${GREEN}macOS build complete!${NC}"
    echo -e "Executables created in: ${YELLOW}../dist/${NC}"
    echo "  - Modlist-Installer.app"
    echo ""
    echo -e "${YELLOW}Note: To distribute on macOS, you may need to sign the app:${NC}"
    echo "  codesign --deep --force --sign - ../dist/Modlist-Installer.app"
elif [[ "$PLATFORM" == "Windows" ]]; then
    echo ""
    echo -e "${GREEN}Windows build complete!${NC}"
    echo -e "Executables created in: ${YELLOW}../dist/${NC}"
    echo "  - Modlist-Installer.exe"
else
    echo ""
    echo -e "${GREEN}Linux build complete!${NC}"
    echo -e "Executables created in: ${YELLOW}../dist/${NC}"
    echo "  - Modlist-Installer"
fi

echo ""
echo -e "${GREEN}Build completed successfully!${NC}"
echo ""
echo -e "${YELLOW}To test the executable:${NC}"
if [[ "$PLATFORM" == "macOS" ]]; then
    echo "  open ../dist/Modlist-Installer.app"
elif [[ "$PLATFORM" == "Windows" ]]; then
    echo "  ..\\dist\\Modlist-Installer.exe"
else
    echo "  ../dist/Modlist-Installer"
fi
