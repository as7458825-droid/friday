import json
import os
import threading
import time

import pyperclip

HISTORY_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "clipboard_history.json"
)
_history = []
_watcher_active = False
_watcher_thread = None


def _load():
    global _history
    if os.path.isfile(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            _history = json.load(f)


def _save():
    mem = os.path.dirname(HISTORY_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(_history[-100:], f, indent=2)


def start_watcher():
    global _watcher_active, _watcher_thread
    if _watcher_active:
        return
    _load()
    _watcher_active = True
    _watcher_thread = threading.Thread(target=_watch_loop, daemon=True)
    _watcher_thread.start()


def stop_watcher():
    global _watcher_active
    _watcher_active = False


def _watch_loop():
    last = ""
    while _watcher_active:
        try:
            current = pyperclip.paste()
            if current and current != last:
                last = current
                _history.append({"text": current[:500], "time": time.time()})
                _save()
        except Exception:
            pass
        time.sleep(1)


def get_history(limit: int = 10) -> str:
    _load()
    if not _history:
        return "Clipboard history is empty."
    items = _history[-limit:]
    lines = []
    for i, item in enumerate(items):
        text = item["text"].replace("\n", " ")[:60]
        lines.append(f"{i + 1}. {text}")
    return "Clipboard history: " + " | ".join(lines)


def search_history(query: str) -> str:
    _load()
    results = [h for h in _history if query.lower() in h["text"].lower()]
    if not results:
        return f"No clipboard matches for '{query}'."
    return "Matches: " + " | ".join(
        r["text"].replace("\n", " ")[:60] for r in results[-5:]
    )


def clear_history() -> str:
    global _history
    _history = []
    _save()
    return "Clipboard history cleared."
