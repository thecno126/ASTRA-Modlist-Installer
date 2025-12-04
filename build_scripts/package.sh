#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=== Creating Distribution Package ==="
echo

cd "$(dirname "$0")"

DIST_DIR="../dist"
PACKAGE_DIR="$DIST_DIR/ASTRA Modlist Installer"
ZIP_NAME="ASTRA-Modlist-Installer.zip"

# Clean dist directory completely first
echo -e "${YELLOW}Cleaning dist directory...${NC}"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Create package directory
echo -e "${BLUE}Creating package directory...${NC}"
mkdir -p "$PACKAGE_DIR"

# Build applications first
echo -e "${BLUE}Building applications...${NC}"
./build.sh
echo

# Move applications to package directory
echo -e "${BLUE}Organizing applications...${NC}"
if [ -d "$DIST_DIR/Modlist-Installer.app" ]; then
    mv "$DIST_DIR/Modlist-Installer.app" "$PACKAGE_DIR/"
    echo "  ✓ Modlist-Installer.app"
else
    echo -e "${RED}  ✗ Modlist-Installer.app not found${NC}"
    exit 1
fi

# Clean up redundant executable files in dist root
echo -e "${BLUE}Cleaning up...${NC}"
rm -f "$DIST_DIR/Modlist-Installer" "$DIST_DIR/Modlist-Configurator" "$DIST_DIR/.DS_Store"

# Copy configuration files
echo -e "${BLUE}Setting up configuration files...${NC}"

# Copy modlist_config.json
if [ -f "../modlist_config.json" ]; then
    cp "../modlist_config.json" "$PACKAGE_DIR/"
    echo "  ✓ Copied modlist_config.json"
else
    echo -e "${YELLOW}  ! modlist_config.json not found${NC}"
fi

# Copy categories.json
if [ -f "../categories.json" ]; then
    cp "../categories.json" "$PACKAGE_DIR/"
    echo "  ✓ Copied categories.json"
else
    echo -e "${YELLOW}  ! categories.json not found${NC}"
fi

# Copy README if exists
if [ -f "../README.md" ]; then
    cp "../README.md" "$PACKAGE_DIR/"
    echo "  ✓ Copied README.md"
fi

# Create a simple instructions file
cat > "$PACKAGE_DIR/README.txt" << 'EOF'
ASTRA Modlist Installer
=======================

This package contains:
- Modlist-Installer.app: Install mods from the modlist
- modlist_config.json: Your modlist configuration
- categories.json: Mod categories configuration

How to use:
1. Open Modlist-Installer.app
2. Select your Starsector installation folder
3. Click "Install All Mods" to install all mods from the modlist

You can also:
- Add/remove mods using the built-in editor
- Import/export modlists as CSV files
- Organize mods by categories

Important: Keep all files in this folder together!

For more information, see README.md
EOF

echo
echo -e "${GREEN}✓ Package created successfully!${NC}"
echo
echo "Package location: $PACKAGE_DIR"
echo
echo "Contents:"
ls -1 "$PACKAGE_DIR"
echo
echo -e "${GREEN}Ready for distribution!${NC}"
echo
echo -e "${YELLOW}Note: You can manually create a ZIP archive if needed:${NC}"
echo "  cd $DIST_DIR && zip -r ASTRA-Modlist-Installer.zip \"ASTRA Modlist Installer\""
