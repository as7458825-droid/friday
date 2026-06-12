import json
import os

import pyautogui

PROFILES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "form_profiles.json"
)


def _load():
    if os.path.isfile(PROFILES_FILE):
        with open(PROFILES_FILE) as f:
            return json.load(f)
    return {}


def _save(profiles):
    mem = os.path.dirname(PROFILES_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=2)


def create_profile(name: str, fields: dict) -> str:
    profiles = _load()
    profiles[name] = fields
    _save(profiles)
    return f"Profile '{name}' created with {len(fields)} fields."


def fill_profile(profile_name: str) -> str:
    profiles = _load()
    profile = profiles.get(profile_name)
    if not profile:
        avail = ", ".join(profiles.keys())
        return f"Profile '{profile_name}' not found. Available: {avail}"
    import time

    time.sleep(2)
    for field, value in profile.items():
        pyautogui.write(value)
        pyautogui.press("tab")
        time.sleep(0.3)
    return f"Filled profile '{profile_name}'."


def list_profiles() -> str:
    profiles = _load()
    if not profiles:
        return "No form profiles saved."
    return "Profiles: " + ", ".join(
        f"{k} ({len(v)} fields)" for k, v in profiles.items()
    )


def delete_profile(name: str) -> str:
    profiles = _load()
    if name in profiles:
        del profiles[name]
        _save(profiles)
        return f"Profile '{name}' deleted."
    return f"Profile '{name}' not found."
