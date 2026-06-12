import threading
import time
try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    pyautogui = None
    HAS_PYAUTOGUI = False

_auto_clicking = False
_click_thread = None
_click_count = 0


def start_clicker(interval: float = 0.1, button: str = "left") -> str:
    global _auto_clicking, _click_thread, _click_count
    if _auto_clicking:
        return "Already clicking."
    if not HAS_PYAUTOGUI:
        return "pyautogui not installed. Run: pip install pyautogui"
    _auto_clicking = True
    _click_count = 0
    _click_thread = threading.Thread(
        target=_click_loop, args=(interval, button), daemon=True
    )
    _click_thread.start()
    return f"Auto-clicker started (every {interval}s). Say 'stop clicking' to end."


def stop_clicker() -> str:
    global _auto_clicking
    _auto_clicking = False
    return f"Auto-clicker stopped. {_click_count} clicks performed."


def _click_loop(interval: float, button: str):
    global _click_count
    while _auto_clicking:
        pyautogui.click(button=button)
        _click_count += 1
        time.sleep(interval)


def fps_overlay() -> str:
    try:
        pass
    except Exception:
        return "pygetwindow not installed."
    return "FPS overlay is a visual feature. Use MSI Afterburner for now."


def start_grind(interval: float = 60) -> str:
    global _auto_clicking, _click_thread
    if not HAS_PYAUTOGUI:
        return "pyautogui not installed. Run: pip install pyautogui"
    _auto_clicking = True
    _click_thread = threading.Thread(target=_grind_loop, args=(interval,), daemon=True)
    _click_thread.start()
    return f"Auto-grind started (every {interval}s)."


def _grind_loop(interval: float):
    global _click_count
    while _auto_clicking:
        pyautogui.press("f")
        _click_count += 1
        time.sleep(interval)
