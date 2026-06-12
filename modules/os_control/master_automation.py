import os
import shutil
try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    pyautogui = None
    HAS_PYAUTOGUI = False


def organize_desktop():
    """Organize files on the desktop by extension."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    categories = {
        "Documents": [".pdf", ".docx", ".txt", ".pptx"],
        "Images": [".jpg", ".png", ".svg", ".gif"],
        "Media": [".mp4", ".mp3", ".wav"],
        "Executables": [".exe", ".msi"],
        "Archives": [".zip", ".rar", ".7z"],
    }

    count = 0
    for filename in os.listdir(desktop):
        filepath = os.path.join(desktop, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()
            for category, extensions in categories.items():
                if ext in extensions:
                    target_dir = os.path.join(desktop, category)
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.move(filepath, os.path.join(target_dir, filename))
                    count += 1
                    break
    return f"Organized {count} files on the desktop into categories."


def control_software(app_name, action):
    """Deep control for common software."""
    if not HAS_PYAUTOGUI:
        return "pyautogui not installed. Run: pip install pyautogui"
    if "chrome" in app_name.lower():
        if "close tabs" in action.lower():
            pyautogui.hotkey("ctrl", "shift", "w")
            return "Attempted to close all Chrome tabs."

    if "volume" in action.lower():
        if "mute" in action.lower():
            pyautogui.press("volumemute")
            return "Volume muted."

    return f"Action '{action}' for '{app_name}' is not yet mapped, but I'm learning."


def system_cleanup():
    """Clean temporary system files."""
    try:
        temp_dir = os.environ.get("TEMP")
        count = 0
        for f in os.listdir(temp_dir):
            try:
                path = os.path.join(temp_dir, f)
                if os.path.isfile(path):
                    os.remove(path)
                    count += 1
            except Exception:
                continue
        return f"Cleaned {count} temporary files."
    except Exception as e:
        return f"Cleanup failed: {e}"
