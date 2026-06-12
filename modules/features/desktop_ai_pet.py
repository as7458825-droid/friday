import math
import random
import threading
import time

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    pyautogui = None
    HAS_PYAUTOGUI = False

try:
    import tkinter as tk

    HAS_TK = True
except Exception:
    HAS_TK = False

_pet_window = None
_pet_thread = None
_active = False
_mood = "happy"
_x, _y = 100, 100
_target_x, _target_y = 100, 100
_velocity_x = 0
_velocity_y = 0

FRAMES = {
    "idle": ["◕‿◕", "◕◡◕", "◕ᴗ◕"],
    "happy": ["≧◡≦", "✧◡✧", "◕‿◕✿"],
    "sleep": ["◕‿◕💤", "◡‿◡💤", "ᴗ‿ᴗ💤"],
    "excited": ["✧⁠▽✧", "☆⁠▽☆", "★⁠ᴗ★"],
    "confused": ["◕_◕", "◕¿◕", "⊙﹏⊙"],
    "wave": ["◕‿◕)/", "◕‿◕\\", "◕‿◕)/"],
}

EMOTES = {
    "idle": "I'm watching you...",
    "happy": "Having fun!",
    "sleep": "Time for a nap... zzz",
    "excited": "Ooh! Something interesting!",
    "confused": "Hmm, what are you doing?",
    "wave": "Hi there!",
}


def _create_window():
    global _pet_window
    _pet_window = tk.Tk()
    _pet_window.overrideredirect(True)
    _pet_window.attributes("-topmost", True)
    _pet_window.attributes("-transparentcolor", "black")
    _pet_window.geometry(f"80x50+{_x}+{_y}")
    _pet_window.configure(bg="black")
    _label = tk.Label(
        _pet_window, text="◕‿◕", font=("Segoe UI", 18), bg="black", fg="#00ff88"
    )
    _label.pack(expand=True)
    _speech = tk.Label(
        _pet_window, text="", font=("Segoe UI", 8), bg="black", fg="#aaaaaa"
    )
    _speech.pack()
    return _pet_window, _label, _speech


def _pet_loop():
    global _pet_window, _active, _x, _y, _mood
    if not HAS_TK:
        return
    win, label, speech = _create_window()
    frame_idx = 0
    mood_timer = time.time()
    speech_timer = time.time()
    speech_text = ""
    while _active:
        try:
            win.update()
            if HAS_PYAUTOGUI:
                mx, my = pyautogui.position()
                dx = mx - (int(win.winfo_x()) + 40)
                dy = my - (int(win.winfo_y()) + 25)
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < 50:
                    _mood = "happy"
                    _x += random.uniform(-1, 1)
                    _y += random.uniform(-1, 1)
                elif random.random() < 0.01:
                    _mood = random.choice(list(FRAMES.keys()))
                    speech_text = EMOTES[_mood]
                    speech_timer = time.time()
                    mood_timer = time.time()
                elif time.time() - mood_timer > 15:
                    _mood = random.choice(["idle", "sleep"])
                    mood_timer = time.time()
                if dist > 100:
                    _x += (dx / dist) * 0.5 if dist > 0 else 0
                    _y += (dy / dist) * 0.5 if dist > 0 else 0
            if win.winfo_x() < 0:
                _x = 0
            if win.winfo_y() < 0:
                _y = 0
            if win.winfo_x() > win.winfo_screenwidth() - 80:
                _x = win.winfo_screenwidth() - 80
            if win.winfo_y() > win.winfo_screenheight() - 50:
                _y = win.winfo_screenheight() - 50
            win.geometry(f"80x50+{int(_x)}+{int(_y)}")
            frames = FRAMES.get(_mood, FRAMES["idle"])
            label.config(text=frames[frame_idx % len(frames)])
            frame_idx += 1
            if time.time() - speech_timer < 3:
                speech.config(text=speech_text)
            else:
                speech.config(text="")
            time.sleep(0.3)
        except Exception:
            break
    try:
        win.destroy()
    except Exception:
        pass


def start_pet() -> str:
    global _active, _pet_thread
    if _active:
        return "Pet already running."
    if not HAS_TK:
        return "tkinter not available."
    _active = True
    _pet_thread = threading.Thread(target=_pet_loop, daemon=True)
    _pet_thread.start()
    return "Desktop AI Pet started! Look for the cute face."


def stop_pet() -> str:
    global _active
    _active = False
    return "Desktop AI Pet stopped."


def set_mood(mood: str) -> str:
    global _mood
    if mood in FRAMES:
        _mood = mood
        return f"Mood set to {mood}."
    return f"Available moods: {', '.join(FRAMES.keys())}"


def pet_status() -> str:
    return f"Pet is {'running' if _active else 'stopped'}. Mood: {_mood}."
