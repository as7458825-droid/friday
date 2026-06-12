import json
import os
import threading
import time
from datetime import datetime

import psutil

LOG_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "screen_time.json"
)
_active = False
_thread = None
_current_app = ""
_total_seconds = 0
_app_times = {}


def _load():
    global _app_times
    if os.path.isfile(LOG_FILE):
        with open(LOG_FILE) as f:
            _app_times = json.load(f)


def _save():
    mem = os.path.dirname(LOG_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(LOG_FILE, "w") as f:
        json.dump(_app_times, f, indent=2)


def _track_loop():
    global _current_app, _total_seconds
    _load()
    start_time = time.time()
    datetime.now().strftime("%Y-%m-%d")
    while _active:
        try:
            current = psutil.Process(os.getpid()).name()
            for proc in psutil.process_iter(["name", "create_time"]):
                try:
                    if (
                        proc.info["create_time"]
                        and proc.info["create_time"] > time.time() - 300
                    ):
                        current = proc.info["name"]
                except Exception:
                    pass
            # use foreground window method via pywin32
            try:
                import ctypes

                user32 = ctypes.windll.user32
                hwnd = user32.GetForegroundWindow()
                length = user32.GetWindowTextLengthW(hwnd)
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                if buf.value:
                    current = buf.value
            except Exception:
                pass
            if current != _current_app:
                if _current_app:
                    elapsed = time.time() - start_time
                    _app_times[_current_app] = _app_times.get(_current_app, 0) + elapsed
                    _total_seconds += elapsed
                _current_app = current
                start_time = time.time()
            _save()
        except Exception:
            pass
        time.sleep(5)


def start_tracking():
    global _active, _thread
    if _active:
        return
    _active = True
    _thread = threading.Thread(target=_track_loop, daemon=True)
    _thread.start()


def stop_tracking():
    global _active
    _active = False


def get_report() -> str:
    _load()
    if not _app_times:
        return "No screen time data yet."
    total = sum(_app_times.values())
    top = sorted(_app_times.items(), key=lambda x: -x[1])[:5]
    lines = []
    for app, secs in top:
        mins = int(secs / 60)
        pct = (secs / total) * 100 if total > 0 else 0
        lines.append(f"{app}: {mins} min ({pct:.0f}%)")
    return "Screen time: " + " | ".join(lines[:5])


def get_app_time(app_name: str) -> str:
    _load()
    secs = _app_times.get(app_name, 0)
    mins = int(secs / 60)
    return f"Time on {app_name}: {mins} minutes."
