import logging
import os
import re
import subprocess
import time

log = logging.getLogger("FRIDAY")

try:
    import pyautogui

    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

try:
    import win32gui
    import win32con
    import win32process

    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    from pywinauto import Application

    HAS_PYWINAUTO = True
except ImportError:
    HAS_PYWINAUTO = False

# ---------------------------------------------------------------------------
# App presets
# ---------------------------------------------------------------------------

APP_PRESETS = {
    "vs code": {
        "process": "Code.exe",
        "shortcuts": {
            "save": "ctrl+s",
            "format": "shift+alt+",
            "run": "ctrl+f5",
            "close tab": "ctrl+w",
            "open file": "ctrl+o",
            "find": "ctrl+",
            "terminal": "ctrl+`",
        },
    },
    "chrome": {
        "process": "chrome.exe",
        "shortcuts": {
            "new tab": "ctrl+t",
            "close tab": "ctrl+w",
            "refresh": "ctrl+r",
            "go to url": "ctrl+l",
            "bookmark": "ctrl+d",
            "history": "ctrl+h",
            "zoom in": "ctrl+plus",
            "zoom out": "ctrl+minus",
        },
    },
    "word": {
        "process": "WINWORD.EXE",
        "shortcuts": {
            "save": "ctrl+s",
            "print": "ctrl+p",
            "undo": "ctrl+z",
            "redo": "ctrl+y",
            "new": "ctrl+n",
            "bold": "ctrl+b",
            "italic": "ctrl+i",
        },
    },
    "excel": {
        "process": "EXCEL.EXE",
        "shortcuts": {
            "save": "ctrl+s",
            "print": "ctrl+p",
            "undo": "ctrl+z",
            "redo": "ctrl+y",
            "new": "ctrl+n",
            "bold": "ctrl+b",
            "italic": "ctrl+i",
        },
    },
    "notepad": {
        "process": "notepad.exe",
        "shortcuts": {
            "save": "ctrl+s",
            "print": "ctrl+p",
            "undo": "ctrl+z",
            "new": "ctrl+n",
            "find": "ctrl+f",
        },
    },
    "whatsapp": {
        "process": "WhatsApp.exe",
        "shortcuts": {
            "new chat": "ctrl+n",
            "search": "ctrl+",
            "mute": "ctrl+shift+m",
        },
    },
    "telegram": {
        "process": "Telegram.exe",
        "shortcuts": {
            "search": "ctrl+",
            "new chat": "ctrl+n",
            "jump": "ctrl+0",
        },
    },
}

_app_cache: dict[str, int] = {}


# ---------------------------------------------------------------------------
# Window helpers
# ---------------------------------------------------------------------------


def _find_window_handle(app_name: str) -> int | None:
    key = app_name.lower().strip()

    if key in _app_cache:
        hwnd = _app_cache[key]
        if win32gui.IsWindow(hwnd):
            return hwnd

    if not HAS_WIN32:
        return None

    def enum_callback(hwnd: int, results: list):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd).lower()
        if key in title or key in title.replace(" ", ""):
            results.append(hwnd)

    matches: list[int] = []
    win32gui.EnumWindows(enum_callback, matches)

    if matches:
        _app_cache[key] = matches[0]
        return matches[0]

    try:
        if HAS_PSUTIL:
            for proc in psutil.process_iter(["pid", "name"]):
                pname = proc.info["name"] or ""
                if key in pname.lower() or key in pname.lower().replace(".exe", ""):
                    hwnd = _find_hwnd_by_pid(proc.info["pid"])
                    if hwnd:
                        _app_cache[key] = hwnd
                        return hwnd
    except Exception:
        pass

    return None


def _find_hwnd_by_pid(pid: int) -> int | None:
    if not HAS_WIN32:
        return None

    def enum_callback(hwnd: int, results: list):
        if not win32gui.IsWindowVisible(hwnd):
            return
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            results.append(hwnd)

    matches: list[int] = []
    win32gui.EnumWindows(enum_callback, matches)
    return matches[0] if matches else None


def _get_preset(app_name: str) -> dict | None:
    key = app_name.lower().strip()
    for preset_key, preset in APP_PRESETS.items():
        if key in preset_key or preset_key in key:
            return preset
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def launch_app(app_name: str, path: str = "") -> str:
    if path and os.path.isfile(path):
        subprocess.Popen(path, shell=True)
        time.sleep(1)
        return f"Launched {app_name}."
    preset = _get_preset(app_name)
    if preset:
        exe = preset["process"]
        try:
            subprocess.Popen(exe, shell=True)
            time.sleep(1)
            return f"Launched {app_name}."
        except Exception as e:
            return f"Failed to launch {app_name}: {e}"
    return f"Don't know how to launch {app_name}. Provide a path."


def focus_app(app_name: str) -> str:
    hwnd = _find_window_handle(app_name)
    if hwnd and HAS_WIN32:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.3)
        return f"Switched to {app_name}."
    return f"Could not find {app_name} window."


def send_shortcut(app_name: str, keys: str) -> str:
    focus_result = focus_app(app_name)
    if "Could not" in focus_result:
        return focus_result
    time.sleep(0.2)
    if HAS_PYAUTOGUI:
        pyautogui.hotkey(*keys.split("+"))
        return f"Sent {keys} to {app_name}."
    return "pyautogui is required for shortcuts."


def send_app_shortcut(app_name: str, action: str) -> str:
    preset = _get_preset(app_name)
    if not preset:
        return f"No preset for {app_name}."
    keys = preset["shortcuts"].get(action.lower())
    if not keys:
        return f"Action '{action}' not found for {app_name}. Available: {', '.join(preset['shortcuts'].keys())}."
    return send_shortcut(app_name, keys)


def type_in_app(app_name: str, text: str) -> str:
    focus_result = focus_app(app_name)
    if "Could not" in focus_result:
        return focus_result
    time.sleep(0.3)
    if HAS_PYAUTOGUI:
        pyautogui.typewrite(text, interval=0.02)
        return f"Typed into {app_name}."
    return "pyautogui is required for typing."


def click_button(app_name: str, button_name: str) -> str:
    hwnd = _find_window_handle(app_name)
    if not hwnd:
        return f"Could not find {app_name} window."
    if HAS_PYWINAUTO:
        try:
            app = Application().connect(handle=hwnd)
            dlg = app.window(handle=hwnd)
            btn = dlg.child_window(title=button_name, control_type="Button")
            if btn.exists():
                btn.click()
                return f"Clicked '{button_name}' in {app_name}."
            btn = dlg.child_window(title_re=re.compile(button_name, re.IGNORECASE))
            if btn.exists():
                btn.click()
                return f"Clicked '{button_name}' in {app_name}."
            return f"Button '{button_name}' not found in {app_name}."
        except Exception as e:
            return f"Failed to click button: {e}"
    elif HAS_PYAUTOGUI:
        try:
            loc = pyautogui.locateOnScreen(f"{button_name}.png", confidence=0.8)
            if loc:
                pyautogui.click(loc)
                return f"Clicked '{button_name}' in {app_name}."
            return f"Could not find button '{button_name}' via image search."
        except Exception:
            return "Button click failed. Install pywinauto for better results."
    return "pywinauto or pyautogui required for button clicks."


def read_text_from_window(app_name: str) -> str:
    hwnd = _find_window_handle(app_name)
    if not hwnd:
        return f"Could not find {app_name} window."
    if HAS_PYWINAUTO:
        try:
            app = Application().connect(handle=hwnd)
            dlg = app.window(handle=hwnd)
            text = dlg.window_text()
            if text:
                return text[:2000]
            texts = []
            for ctrl in dlg.descendants():
                try:
                    t = ctrl.window_text()
                    if t:
                        texts.append(t)
                except Exception:
                    pass
            result = "\n".join(texts)
            return result[:2000] if result else "No text found in window."
        except Exception as e:
            return f"Failed to read text: {e}"
    if HAS_PYAUTOGUI:
        return "pywinauto provides better text reading. Install it for full support."
    return "pywinauto is required for reading text from windows."


def resize_window(app_name: str, width: int, height: int) -> str:
    hwnd = _find_window_handle(app_name)
    if hwnd and HAS_WIN32:
        win32gui.SetWindowPos(
            hwnd, 0, 0, 0, width, height, win32con.SWP_NOMOVE | win32con.SWP_NOZORDER
        )
        return f"Resized {app_name} to {width}x{height}."
    return f"Could not resize {app_name}."


def move_window(app_name: str, x: int, y: int) -> str:
    hwnd = _find_window_handle(app_name)
    if hwnd and HAS_WIN32:
        win32gui.SetWindowPos(
            hwnd, 0, x, y, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
        )
        return f"Moved {app_name} to ({x}, {y})."
    return f"Could not move {app_name}."


# ---------------------------------------------------------------------------
# App-specific helpers
# ---------------------------------------------------------------------------


def chrome_go_to_url(url: str) -> str:
    r = send_app_shortcut("chrome", "go to url")
    if "Could not" in r:
        return r
    time.sleep(0.3)
    if HAS_PYAUTOGUI:
        pyautogui.typewrite(url, interval=0.02)
        pyautogui.press("enter")
        return f"Chrome navigating to {url}."
    return "pyautogui required."


def messager_send(contact: str, message: str, app: str = "whatsapp") -> str:
    focus_result = focus_app(app)
    if "Could not" in focus_result:
        return focus_result
    time.sleep(0.5)
    if HAS_PYAUTOGUI:
        pyautogui.typewrite(contact, interval=0.03)
        time.sleep(0.5)
        pyautogui.press("down")
        pyautogui.press("enter")
        time.sleep(0.3)
        pyautogui.typewrite(message, interval=0.02)
        pyautogui.press("enter")
        return f"Sent message to {contact} via {app}."
    return "pyautogui required."
