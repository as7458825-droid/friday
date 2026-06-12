import json
import os

MEMORY_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "user_prefs.json"
)


def _load() -> dict:
    if not os.path.isfile(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE) as f:
        return json.load(f)


def _save(data: dict) -> None:
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_preference(key: str, value) -> None:
    data = _load()
    data[key] = value
    _save(data)


def get_preference(key: str, default=None):
    return _load().get(key, default)


def get_all_preferences() -> dict:
    return _load()
