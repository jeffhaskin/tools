# file_utils.py
import os
from pathlib import Path

def get_desktop_path():
    """
    Get the path to the user's desktop
    
    Returns:
        Path object pointing to the desktop directory
    """
    if os.name == 'nt':  # Windows
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    else:  # Linux/Mac
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        # If Desktop doesn't exist, try localized name
        if not os.path.exists(desktop):
            try:
                import subprocess
                desktop = subprocess.check_output(['xdg-user-dir', 'DESKTOP']).decode().strip()
            except (subprocess.SubprocessError, FileNotFoundError):
                desktop = os.path.expanduser('~')  # Fallback to home directory

    return Path(desktop)

def ensure_directory(path):
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        path: str or Path object
    """
    Path(path).mkdir(parents=True, exist_ok=True)

def get_file_extension(filename):
    """
    Get the extension of a file
    
    Args:
        filename: str, name of the file
    Returns:
        str: extension without the dot
    """
    return Path(filename).suffix[1:].lower()
