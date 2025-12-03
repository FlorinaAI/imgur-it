# 🌸 imgur-it

A easy-to-use Python tool for uploading images to Imgur, managing links, and downloading images directly from your Linux terminal. Simply use the `imgur-it` command to handle all your Imgur operations!

## ✨ Features

- 🎀 Upload single images or entire folders to Imgur
- 📋 Save uploaded image links to a `.txt` file automatically
- 📥 Download images from Imgur links (single or batch from file)
- 🛡️ Non-invasive: Uses XDG Base Directory specification
- 📦 Automatic Installation: Installs to `~/.local/bin` (no sudo required!)
- 💖 Beautiful colored output with loading animations
- 🔒 Secure API key storage

## 📦 Requirements

- Python 3.6+ (with venv support)
- A Linux terminal
- Imgur API credentials ([Create a client](https://api.imgur.com/oauth2/addclient))

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FlorinaAI/imgur-it.git
   ```

2. **Navigate to the project folder:**
   ```bash
   cd imgur-it
   ```

3. **Run the installation script:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

4. **During installation, you'll be prompted to enter your Imgur API credentials.**

The installer will:
1. Create a virtual environment in `~/.local/share/imgur-it/venv`
2. Install dependencies automatically
3. Add `imgur-it` to your PATH (if needed)
4. Save your API keys securely

Once installation is complete, you can use the `imgur-it` command from anywhere in your terminal!

## 🗑️ Uninstallation

```bash
cd imgur-it
chmod +x uninstall.sh
./uninstall.sh
```

This will remove the wrapper, config, virtual environment, and cache. Clean as a whistle! ✨

## ❄️ Usage

For current information and all options: `imgur-it -h`

### Command Line Options

- `-f, --folder` - Upload all images in a folder
- `-w, --write` - Save upload links to a file
- `-i, --imgur` - Download from Imgur link or file
- `-q, --quiet` - Suppress logo and non-essential output (useful for scripts)
- `-v, --version` - Show version information
- `-h, --help` - Show help message


### 1. Upload a single image

Upload a specific image file to Imgur (link automatically copied to clipboard):

```bash
imgur-it /path/to/image.png
```

### 2. Upload all images in a folder

Upload all images in a specified folder to Imgur:

```bash
imgur-it -f /path/to/folder/
```

### 3. Save links to a .txt file

Save uploaded image links to a `.txt` file:

```bash
imgur-it -f /path/to/folder/ -w
```

Specify a custom location for the .txt file:

```bash
imgur-it -f /path/to/folder/ -w /path/to/links.txt
```

### 4. Download images

Download an image from an Imgur link:

```bash
imgur-it -i https://i.imgur.com/example.png
```

Download multiple images from a text file containing Imgur links:

```bash
imgur-it -i /path/to/links.txt
```

Example `links.txt` file:
```
https://i.imgur.com/example1.png
https://i.imgur.com/example2.png
https://i.imgur.com/example3.png
```

## 🍦 Configuration

Configuration files are stored according to XDG Base Directory specification:

- **Config:** `~/.config/imgur-it/keys.txt` - Your API credentials
- **Data:** `~/.local/share/imgur-it/` - Virtual environment and script
- **Binary:** `~/.local/bin/imgur-it` - Executable wrapper

### API Keys Format

The `keys.txt` file should contain:
```
IMGUR_CLIENT_ID = your_client_id_here
IMGUR_CLIENT_SECRET = your_client_secret_here
```

## 🎀 Directory Structure

After installation:
```
~/.local/share/imgur-it/    # Data directory
  ├── venv/                   # Virtual environment
  └── imgur-it.py             # Main script

~/.config/imgur-it/          # Config directory
  └── keys.txt                # API credentials

~/.local/bin/imgur-it        # Executable wrapper
```

## 🌸 Troubleshooting

### "imgur-it: command not found"
- Make sure `~/.local/bin` is in your PATH
- Restart your terminal or run: `source ~/.bashrc` (or `~/.zshrc` for zsh)
- Or manually add to your shell RC file:
  ```bash
  export PATH="$HOME/.local/bin:$PATH"
  ```

### "Configuration file not found"
- Make sure you ran the installer and entered your API keys
- Check that `~/.config/imgur-it/keys.txt` exists
- Re-run the installer if needed

### Upload/Download Failures
- Verify your internet connection
- Check that your API credentials are valid
- For rate limiting errors, wait a few minutes and try again

## 🧁 Credits

Made with ♡ by [FlorinaAI](https://github.com/FlorinaAI)

Inspired by the clean architecture of [moefetch](https://github.com/FlorinaAI/moefetch)
