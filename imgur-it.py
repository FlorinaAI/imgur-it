#!/usr/bin/env python3
import os
import sys
import time
import argparse
import threading
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple
import pyperclip

try:
    from imgurpython import ImgurClient
except ImportError:
    print("Error: imgurpython not installed. Run installer first.")
    sys.exit(1)

try:
    from termcolor import colored
except ImportError:
    print("Error: termcolor not installed. Run installer first.")
    sys.exit(1)

# Version
__version__ = "1.1"

# XDG Base Directory Specification
XDG_CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))

CONFIG_DIR = XDG_CONFIG_HOME / "imgur-it"
CONFIG_PATH = CONFIG_DIR / "keys.txt"

# 🌸 Colors 🌸
PINK = '\033[38;2;230;143;172m'
CYAN = '\033[36m'
MAGENTA = '\033[35m'
RED = '\033[31m'
RESET = '\033[0m'


def custom_print(text: str, color: str = PINK) -> None:
    """Print colored text with cute formatting."""
    print(f"{color}{text}{RESET}")


def say(message: str, link: Optional[str] = None) -> None:
    """Print a message with timestamp and optional link."""
    current_time = datetime.now().strftime("%H:%M")
    formatted_time = f"[{colored(current_time, 'magenta')}]"
    formatted_message = colored(message, 'cyan')
    if link:
        formatted_message += colored(f" {link}", 'red')
    print(f"{formatted_time} {formatted_message}")


class LoadingAnimation:
    """Context manager for animated loading with hearts."""
    
    def __init__(self, message: str, enabled: bool = True):
        self.message = message
        self.enabled = enabled
        self.stop_event = threading.Event()
        self.thread = None

    def _animate(self):
        hearts_cycle = ["♡", "♡♡", "♡♡♡"]
        idx = 0
        while not self.stop_event.is_set():
            print(f"\r{PINK}{self.message} {hearts_cycle[idx]}{RESET}", end="", flush=True)
            idx = (idx + 1) % 3
            time.sleep(0.3)
        print()  # New line when done

    def __enter__(self):
        if not self.enabled:
            return self
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
        return self

    def __exit__(self, *args):
        if not self.enabled:
            return
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=1)


def read_keys_from_file(file_path: Path) -> Tuple[Optional[str], Optional[str]]:
    """Read Imgur API keys from configuration file.
    
    Args:
        file_path: Path to the keys.txt file
        
    Returns:
        Tuple of (client_id, client_secret) or (None, None) if not found
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            client_id = None
            client_secret = None
            
            for line in lines:
                if line.startswith('IMGUR_CLIENT_ID'):
                    client_id = line.split('=')[1].strip()
                elif line.startswith('IMGUR_CLIENT_SECRET'):
                    client_secret = line.split('=')[1].strip()

            return client_id, client_secret
    except FileNotFoundError:
        say(f"Configuration file not found: {file_path}")
        say("Please run the installer first or create the config file manually.")
        return None, None


def upload_image(image_path: str, client_id: str, client_secret: str) -> str:
    """Upload a single image to Imgur.
    
    Args:
        image_path: Path to the image file
        client_id: Imgur API client ID
        client_secret: Imgur API client secret
        
    Returns:
        Imgur URL of uploaded image
        
    Raises:
        Exception: If upload fails
    """
    client = ImgurClient(client_id, client_secret)
    response = client.upload_from_path(image_path, anon=True)
    return response['link']


def upload_images_in_folder(folder_path: str, client_id: str, client_secret: str, 
                           write_to_file: Optional[str] = None) -> List[Tuple[str, str]]:
    """Upload all images in a folder to Imgur.
    
    Args:
        folder_path: Path to folder containing images
        client_id: Imgur API client ID
        client_secret: Imgur API client secret
        write_to_file: Optional path to save links
        
    Returns:
        List of tuples (image_name, imgur_link)
    """
    imgur_links = []
    supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    
    image_files = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(folder_path)
        for file in files if file.lower().endswith(supported_formats)
    ]
    
    if not image_files:
        say("No images found in the specified folder.")
        return imgur_links
    
    say(f"Found {len(image_files)} images. Starting upload...")
    
    for idx, image_path in enumerate(image_files, start=1):
        try:
            say(f"{idx}/{len(image_files)}: Uploading {os.path.basename(image_path)}...")
            
            with LoadingAnimation(f"Uploading image {idx}/{len(image_files)}"):
                imgur_link = upload_image(image_path, client_id, client_secret)
            
            imgur_links.append((os.path.basename(image_path), imgur_link))
            say("Image uploaded successfully!", imgur_link)
            
        except Exception as e:
            say(f"Upload failed for {os.path.basename(image_path)}: {e}")
    
    if write_to_file and imgur_links:
        try:
            with open(write_to_file, 'w') as file:
                for image_name, link in imgur_links:
                    file.write(f"{image_name} : {link}\n")
            say(f"All links saved to {write_to_file}")
        except Exception as e:
            say(f"Failed to write links to file: {e}")
    
    return imgur_links


def download_image(imgur_link: str, download_path: str) -> None:
    """Download an image from Imgur.
    
    Args:
        imgur_link: Imgur URL to download from
        download_path: Local path to save the image
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    retries = 3
    
    for attempt in range(retries):
        try:
            with LoadingAnimation(f"Downloading image (attempt {attempt + 1}/{retries})"):
                response = requests.get(imgur_link, headers=headers, timeout=10)
            
            if response.status_code == 200:
                with open(download_path, 'wb') as file:
                    file.write(response.content)
                say(f"Image downloaded successfully to {download_path}")
                return
            elif response.status_code == 429:
                say("Rate limit error. Waiting 60 seconds...")
                time.sleep(60)
            else:
                say(f"Failed to download image. HTTP status code: {response.status_code}")
                return
                
        except requests.RequestException as e:
            say(f"Error while downloading image: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return
    
    say("Maximum retries reached. Failed to download image.")


def download_images_from_file(file_path: str) -> None:
    """Download all images from URLs listed in a text file.
    
    Args:
        file_path: Path to text file containing Imgur URLs
    """
    if not os.path.isfile(file_path):
        say(f"Link file not found: {file_path}")
        return
    
    try:
        with open(file_path, 'r') as file:
            links = file.readlines()
    except Exception as e:
        say(f"Error reading link file: {e}")
        return

    links = [link.strip() for link in links if link.strip()]
    
    if not links:
        say("No links found in file.")
        return
    
    say(f"Found {len(links)} links. Starting download...")
    
    for idx, link in enumerate(links, start=1):
        say(f"{idx}/{len(links)}: Downloading {link}...")
        
        # Extract file extension from URL or default to .png
        ext = '.png'
        if '.' in link.split('/')[-1]:
            ext = '.' + link.split('.')[-1].split('?')[0]
        
        download_image(link, f"downloaded_image_{idx}{ext}")


def show_version() -> None:
    """Display version information."""
    print(f"imgur-it version {__version__}")
    print("Made with ♡ by FlorinaAI")
    print("https://github.com/FlorinaAI/imgur-it")


def main() -> None:
    """Main entry point for imgur-it."""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Upload and download images from Imgur with ease! ♡",
        epilog="Example: imgur-it image.png"
    )
    parser.add_argument(
        "image_path", 
        type=str, 
        nargs='?', 
        help="Path to the image file to upload"
    )
    parser.add_argument(
        "-f", "--folder", 
        type=str, 
        help="Path to folder containing images to upload"
    )
    parser.add_argument(
        "-w", "--write", 
        type=str, 
        nargs='?', 
        const='', 
        help="Save links to specified file (defaults to links.txt in same folder)"
    )
    parser.add_argument(
        "-i", "--imgur", 
        type=str, 
        help="Download image from Imgur link or from a .txt file containing links"
    )
    parser.add_argument(
        "-q", "--quiet",
        action='store_true',
        help="Quiet mode - suppress logo and non-essential output"
    )
    parser.add_argument(
        "-v", "--version",
        action='store_true',
        help="Show version information and exit"
    )
    
    args = parser.parse_args()
    
    # Handle version flag
    if args.version:
        show_version()
        return
    
    # If no arguments, show help
    if not (args.image_path or args.folder or args.imgur):
        parser.print_help()
        return
    
    # For downloads, we don't need API keys
    if args.imgur:
        if args.imgur.endswith('.txt'):
            download_images_from_file(args.imgur)
        else:
            try:
                download_image(args.imgur, "downloaded_image.png")
            except Exception as e:
                say(f"Error during download: {e}")
        return
    
    # For uploads, we need API keys
    IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET = read_keys_from_file(CONFIG_PATH)
    
    if not IMGUR_CLIENT_ID or not IMGUR_CLIENT_SECRET:
        say("Imgur API keys could not be read. Please check your keys.txt file.")
        say(f"Expected location: {CONFIG_PATH}")
        sys.exit(1)
    
    imgur_links = []
    write_to_file = None
    
    # Handle single image upload
    if args.image_path:
        if not os.path.isfile(args.image_path):
            say(f"Image file not found: {args.image_path}")
            sys.exit(1)
        
        try:
            with LoadingAnimation("Uploading image"):
                imgur_link = upload_image(args.image_path, IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
            
            pyperclip.copy(imgur_link)
            say("Image uploaded successfully and copied to clipboard!", imgur_link)
            imgur_links.append((os.path.basename(args.image_path), imgur_link))
            
        except Exception as e:
            say(f"Upload error: {e}")
            sys.exit(1)
    
    # Handle folder upload
    elif args.folder:
        if not os.path.isdir(args.folder):
            say(f"Invalid folder path: {args.folder}")
            sys.exit(1)
        
        if args.write is not None:
            if args.write == '':
                write_to_file = os.path.join(args.folder, "links.txt")
            else:
                write_to_file = args.write
        
        imgur_links = upload_images_in_folder(
            args.folder, 
            IMGUR_CLIENT_ID, 
            IMGUR_CLIENT_SECRET, 
            write_to_file=write_to_file
        )
    
    # Summary
    if imgur_links:
        custom_print(f"\n✨ Upload complete! Successfully uploaded {len(imgur_links)} images. ✨\n")


if __name__ == "__main__":
    main()
