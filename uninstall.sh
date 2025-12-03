#!/bin/bash

# 🌸 Colors 🌸
PINK='\033[38;2;230;143;172m'
RESET='\033[0m'

# Helper function for cute printing
custom_print() {
    echo -e "${PINK}$1${RESET}"
}

# Directories
CONFIG_DIR="$HOME/.config/imgur-it"
DATA_DIR="$HOME/.local/share/imgur-it"
CACHE_DIR="$HOME/.cache/imgur-it"
WRAPPER_PATH="$HOME/.local/bin/imgur-it"

custom_print "🌸 imgur-it Uninstaller 🌸"
custom_print "---------------------------"
custom_print "==== Uninstalling imgur-it~ Let's clean up with sparkles! ✨ ===="

# 1. Remove Wrapper
if [ -f "$WRAPPER_PATH" ]; then
    custom_print "→ Removing wrapper ($WRAPPER_PATH)..."
    rm "$WRAPPER_PATH"
    custom_print "✓ Wrapper removed!"
else
    custom_print "✓ Wrapper not found."
fi

# 2. Remove Data Directory (venv & script)
if [ -d "$DATA_DIR" ]; then
    custom_print "→ Removing data directory ($DATA_DIR)..."
    rm -rf "$DATA_DIR"
    custom_print "✓ Data directory removed."
else
    custom_print "✓ Data directory not found."
fi

# 3. Remove Config Directory
if [ -d "$CONFIG_DIR" ]; then
    custom_print "→ Removing config directory ($CONFIG_DIR)..."
    rm -rf "$CONFIG_DIR"
    custom_print "✓ Config directory removed."
else
    custom_print "✓ Config directory not found."
fi

# 4. Remove Cache (if exists)
if [ -d "$CACHE_DIR" ]; then
    custom_print "→ Removing cache directory ($CACHE_DIR)..."
    rm -rf "$CACHE_DIR"
    custom_print "✓ Cache directory removed."
else
    custom_print "✓ Cache directory not found."
fi

# 5. PATH Warning
custom_print "→ Checking shell config..."
SHELL_RC=""
case "$SHELL" in
    */bash) SHELL_RC="$HOME/.bashrc" ;;
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
esac

if [ -n "$SHELL_RC" ] && [ -f "$SHELL_RC" ]; then
    if grep -q "imgur-it installer" "$SHELL_RC"; then
        custom_print "⚠ Note: You may have a PATH export line in $SHELL_RC added by the installer."
        custom_print "  Please check and remove it manually if desired."
    fi
fi

custom_print "---------------------------"
custom_print "✨ Uninstallation Complete! ✨"