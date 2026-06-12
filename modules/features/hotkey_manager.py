import json
import os

import keyboard

BINDINGS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "hotkeys.json"
)
_hotkeys = {}


def _load():
    global _hotkeys
    if os.path.isfile(BINDINGS_FILE):
        with open(BINDINGS_FILE) as f:
            _hotkeys = json.load(f)


def _save():
    mem = os.path.dirname(BINDINGS_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(BINDINGS_FILE, "w") as f:
        json.dump(_hotkeys, f, indent=2)


def bind_hotkey(combo: str, action: str) -> str:
    _load()
    _hotkeys[combo.lower()] = action
    _save()
    try:
        keyboard.add_hotkey(combo, lambda a=action: _execute_action(a))
    except Exception as e:
        return f"Hotkey binding error: {e}"
    return f"Bound '{combo}' to: {action}"


def unbind_hotkey(combo: str) -> str:
    _load()
    if combo.lower() in _hotkeys:
        del _hotkeys[combo.lower()]
        _save()
        try:
            keyboard.remove_hotkey(combo)
        except Exception:
            pass
        return f"Unbound '{combo}'."
    return f"'{combo}' not bound."


def list_hotkeys() -> str:
    _load()
    if not _hotkeys:
        return "No hotkeys configured."
    return "Hotkeys: " + " | ".join(f"{k}: {v}" for k, v in _hotkeys.items())


def _execute_action(action: str):
    import subprocess
    import os

    action = action.strip()
    if action.startswith("cmd:"):
        subprocess.Popen(action[4:], shell=True)
    elif action.startswith("app:"):
        os.startfile(action[4:].strip())
    elif action.startswith("key:"):
        keyboard.press_and_release(action[4:].strip())
    elif action.startswith("type:"):
        keyboard.write(action[5:])


def initialize():
    _load()
    for combo, action in _hotkeys.items():
        try:
            keyboard.add_hotkey(combo, lambda a=action: _execute_action(a))
        except Exception:
            pass
