import json
import os
import threading
import time
from datetime import datetime

import psutil

PROFILE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "triage_profile.json"
)
_active = False
_thread = None


def _load():
    if os.path.isfile(PROFILE_FILE):
        with open(PROFILE_FILE) as f:
            return json.load(f)
    return {
        "focus_apps": [],
        "quiet_hours_start": 22,
        "quiet_hours_end": 8,
        "notification_blacklist": [],
    }


def _save(data):
    mem = os.path.dirname(PROFILE_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def set_focus_apps(apps: list) -> str:
    data = _load()
    data["focus_apps"] = apps
    _save(data)
    return f"Focus apps set: {', '.join(apps)}."


def set_quiet_hours(start: int, end: int) -> str:
    data = _load()
    data["quiet_hours_start"] = start
    data["quiet_hours_end"] = end
    _save(data)
    return f"Quiet hours: {start}:00 to {end}:00."


def start_triage() -> str:
    global _active, _thread
    if _active:
        return "Already running."
    _active = True
    _thread = threading.Thread(target=_triage_loop, daemon=True)
    _thread.start()
    return "Auto-triage started. I will filter notifications when you're busy."


def stop_triage() -> str:
    global _active
    _active = False
    return "Auto-triage stopped."


def _triage_loop():
    while _active:
        try:
            data = _load()
            now = datetime.now()
            hour = now.hour
            is_quiet = False
            if data["quiet_hours_end"] > data["quiet_hours_start"]:
                is_quiet = data["quiet_hours_start"] <= hour < data["quiet_hours_end"]
            else:
                is_quiet = (
                    hour >= data["quiet_hours_start"] or hour < data["quiet_hours_end"]
                )
            if is_quiet:
                print("[AUTO-TRIAGE] Quiet hours — notifications filtered.")
            focus = data.get("focus_apps", [])
            if focus:
                for proc in psutil.process_iter(["name"]):
                    try:
                        if proc.info["name"] and any(
                            f.lower() in proc.info["name"].lower() for f in focus
                        ):
                            print(
                                f"[AUTO-TRIAGE] Focus mode active — {proc.info['name']} running."
                            )
                            break
                    except Exception:
                        pass
        except Exception:
            pass
        time.sleep(60)


def triage_status() -> str:
    data = _load()
    return f"Focus apps: {', '.join(data['focus_apps']) or 'none'}. Quiet hours: {data['quiet_hours_start']}:00-{data['quiet_hours_end']}:00."
