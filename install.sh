#!/bin/bash

# 🌸 Colors 🌸
PINK='\033[38;2;230;143;172m'
RESET='\033[0m'

# Helper function for cute printing
custom_print() {
    echo -e "${PINK}$1${RESET}"
}

# Directories (XDG compliant)
CONFIG_DIR="$HOME/.config/imgur-it"
DATA_DIR="$HOME/.local/share/imgur-it"
INSTALL_DIR="$DATA_DIR"
BIN_DIR="$HOME/.local/bin"
VENV_DIR="$INSTALL_DIR/venv"
SCRIPT_DEST="$INSTALL_DIR/imgur-it.py"
WRAPPER_DEST="$BIN_DIR/imgur-it"

# Source files
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_SRC="$BASE_DIR/imgur-it.py"

custom_print "🌸 imgur-it Installer 🌸"
custom_print "-------------------------"

# 1. Create Directories
custom_print "→ Creating directories..."
mkdir -p "$INSTALL_DIR"
if [ $? -ne 0 ]; then
    custom_print "✗ Error: Failed to create $INSTALL_DIR."
    exit 1
fi
mkdir -p "$CONFIG_DIR"
if [ $? -ne 0 ]; then
    custom_print "✗ Error: Failed to create $CONFIG_DIR."
    exit 1
fi
mkdir -p "$BIN_DIR"
if [ $? -ne 0 ]; then
    custom_print "✗ Error: Failed to create $BIN_DIR."
    exit 1
fi

# 2. Copy Script
custom_print "→ Copying script..."
if [ ! -f "$SCRIPT_SRC" ]; then
    custom_print "✗ Error: imgur-it.py not found in current directory."
    exit 1
fi
cp "$SCRIPT_SRC" "$SCRIPT_DEST"
if [ $? -ne 0 ]; then
    custom_print "✗ Error: Failed to copy script."
    exit 1
fi

# 3. Create Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    custom_print "→ Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        custom_print "✗ Error: Failed to create venv. Please install python3-venv.💔)"
        exit 1
    fi
else
    custom_print "✓ Virtual environment already exists."
fi

# 4. Install Dependencies
custom_print "→ Installing dependencies (imgurpython, termcolor, requests, pyperclip)..."
"$VENV_DIR/bin/pip" install -q --upgrade pip
"$VENV_DIR/bin/pip" install -q imgurpython termcolor requests pyperclip
if [ $? -ne 0 ]; then
    custom_print "✗ Error: Failed to install dependencies."
    exit 1
fi

# 5. Setup API Keys
KEYS_FILE="$CONFIG_DIR/keys.txt"
if [ ! -f "$KEYS_FILE" ]; then
    custom_print "→ Setting up Imgur API keys..."
    echo ""
    custom_print "Please enter your Imgur API credentials:"
    custom_print "(You can get these from: https://api.imgur.com/oauth2/addclient)"
    echo ""
    read -p "IMGUR_CLIENT_ID: " IMGUR_CLIENT_ID
    read -p "IMGUR_CLIENT_SECRET: " IMGUR_CLIENT_SECRET
    
    echo "IMGUR_CLIENT_ID = $IMGUR_CLIENT_ID" > "$KEYS_FILE"
    echo "IMGUR_CLIENT_SECRET = $IMGUR_CLIENT_SECRET" >> "$KEYS_FILE"
    
    chmod 600 "$KEYS_FILE"
    custom_print "✓ API keys saved securely to keys.txt."
else
    custom_print "✓ API keys already configured."
fi

# 6. Create Wrapper
custom_print "→ Creating executable wrapper..."
cat > "$WRAPPER_DEST" <<EOF
#!/bin/bash
exec "$VENV_DIR/bin/python" "$SCRIPT_DEST" "\$@"
EOF
chmod +x "$WRAPPER_DEST"
if [ $? -ne 0 ]; then
    custom_print "✗ Error: Failed to make wrapper executable."
    exit 1
fi

# 7. PATH Setup
custom_print "→ Checking PATH..."
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    custom_print "⚠ '$BIN_DIR' is not in your PATH."
    SHELL_RC=""
    case "$SHELL" in
        */bash) SHELL_RC="$HOME/.bashrc" ;;
        */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    esac

    if [ -n "$SHELL_RC" ] && [ -f "$SHELL_RC" ]; then
        custom_print "→ Adding to $SHELL_RC..."
        echo "" >> "$SHELL_RC"
        echo "# Added by imgur-it installer" >> "$SHELL_RC"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        custom_print "✓ Added to PATH. Please restart your terminal or run 'source $SHELL_RC'."
    else
        custom_print "⚠ Could not detect shell config file. Please add '$BIN_DIR' to your PATH manually."
    fi
else
    custom_print "✓ '$BIN_DIR' is already in your PATH."
fi

custom_print "-------------------------"
custom_print "✨ Installation Complete! ✨"
custom_print "Try running: imgur-it -h"
