import numpy as np

try:
    import pyautogui

    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False


def capture_screen() -> np.ndarray | None:
    if not HAS_PYAUTOGUI:
        return None
    screenshot = pyautogui.screenshot()
    return np.array(screenshot)


def preprocess_frame(frame: np.ndarray) -> np.ndarray:
    return frame.copy()


def get_screen_array() -> np.ndarray | None:
    return capture_screen()
