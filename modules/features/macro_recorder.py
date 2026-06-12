import json
import os
import threading
import time

import pyautogui
from pynput import mouse, keyboard

MACROS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "memory_db", "macros")
_recording = False
_playing = False
_events = []
_listener = None
_record_thread = None


def _ensure_dir():
    if not os.path.isdir(MACROS_DIR):
        os.makedirs(MACROS_DIR, exist_ok=True)


def start_recording() -> str:
    global _recording, _events, _record_thread
    if _recording:
        return "Already recording."
    _recording = True
    _events = []
    _record_thread = threading.Thread(target=_record_loop, daemon=True)
    _record_thread.start()
    return "Macro recording started. Perform your actions."


def stop_recording(name: str = "macro") -> str:
    global _recording
    if not _recording:
        return "Not recording."
    _recording = False
    if _record_thread:
        _record_thread.join(timeout=3)
    _ensure_dir()
    path = os.path.join(MACROS_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(_events, f, indent=2)
    return f"Macro saved as '{name}' ({len(_events)} events)."


def play_macro(name: str) -> str:
    global _playing
    if _playing:
        return "Already playing a macro."
    _ensure_dir()
    path = os.path.join(MACROS_DIR, f"{name}.json")
    if not os.path.isfile(path):
        avail = list_macros()
        return f"Macro '{name}' not found. {avail}"
    with open(path) as f:
        events = json.load(f)
    _playing = True
    threading.Thread(target=_play_events, args=(events,), daemon=True).start()
    return f"Playing macro '{name}'..."


def _play_events(events):
    global _playing
    try:
        for event in events:
            if not _playing:
                break
            etype = event["type"]
            delay = event.get("delay", 0.1)
            time.sleep(delay)
            if etype == "click":
                pyautogui.click(
                    event["x"], event["y"], button=event.get("button", "left")
                )
            elif etype == "move":
                pyautogui.moveTo(event["x"], event["y"], duration=0.1)
            elif etype == "drag":
                pyautogui.drag(event["x"], event["y"], duration=0.2)
            elif etype == "scroll":
                pyautogui.scroll(event["dy"])
            elif etype == "key":
                pyautogui.write(event["key"])
            elif etype == "hotkey":
                pyautogui.hotkey(*event["keys"])
            elif etype == "sleep":
                time.sleep(event["seconds"])
    finally:
        _playing = False


def stop_playing() -> str:
    global _playing
    _playing = False
    return "Macro playback stopped."


def list_macros() -> str:
    _ensure_dir()
    files = [f[:-5] for f in os.listdir(MACROS_DIR) if f.endswith(".json")]
    if not files:
        return "No saved macros."
    return "Macros: " + ", ".join(files)


def _record_loop():
    global _events
    last_time = time.time()

    def on_click(x, y, button, pressed):
        nonlocal last_time
        global _events
        if not _recording:
            return False
        now = time.time()
        delay = now - last_time
        last_time = now
        _events.append(
            {
                "type": "click",
                "x": x,
                "y": y,
                "button": str(button),
                "pressed": pressed,
                "delay": round(delay, 3),
            }
        )

    def on_move(x, y):
        if not _recording:
            return False

    def on_scroll(x, y, dx, dy):
        nonlocal last_time
        global _events
        if not _recording:
            return False
        now = time.time()
        delay = now - last_time
        last_time = now
        _events.append(
            {
                "type": "scroll",
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "delay": round(delay, 3),
            }
        )

    def on_press(key):
        nonlocal last_time
        global _events
        if not _recording:
            return False
        try:
            k = key.char
        except Exception:
            k = str(key)
        now = time.time()
        delay = now - last_time
        last_time = now
        _events.append({"type": "key", "key": k, "delay": round(delay, 3)})

    mouse_listener = mouse.Listener(
        on_click=on_click, on_move=on_move, on_scroll=on_scroll
    )
    key_listener = keyboard.Listener(on_press=on_press)
    mouse_listener.start()
    key_listener.start()
    while _recording:
        time.sleep(0.1)
    mouse_listener.stop()
    key_listener.stop()
