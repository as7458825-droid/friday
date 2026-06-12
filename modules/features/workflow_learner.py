import json
import os
import threading
import time
from datetime import datetime

import psutil

RECORDER_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "workflows.json"
)

_recording = False
_recorder_thread = None
_events = []
_workflows = {}
_active = False


def _load():
    global _workflows
    if os.path.isfile(RECORDER_FILE):
        with open(RECORDER_FILE) as f:
            _workflows = json.load(f)


def _save():
    mem = os.path.dirname(RECORDER_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(RECORDER_FILE, "w") as f:
        json.dump(_workflows, f, indent=2)


def start_recording() -> str:
    global _recording, _events, _recorder_thread
    if _recording:
        return "Already recording."
    _recording = True
    _events = []
    _recorder_thread = threading.Thread(target=_record_loop, daemon=True)
    _recorder_thread.start()
    return "Workflow recording started. Perform your task normally. Say 'stop recording workflow' when done."


def stop_recording(name: str = "") -> str:
    global _recording
    if not _recording:
        return "Not recording."
    _recording = False
    if _recorder_thread:
        _recorder_thread.join(timeout=5)
    if len(_events) < 3:
        return "Not enough events recorded (min 3)."
    if not name:
        name = f"workflow_{datetime.now().strftime('%H%M%S')}"
    _load()
    _workflows[name] = {
        "events": _events,
        "created": datetime.now().isoformat(),
        "count": len(_events),
    }
    _save()
    return f"Workflow '{name}' saved ({len(_events)} steps)."


def _record_loop():
    global _events
    last_apps = set()
    while _recording:
        try:
            apps = set()
            for proc in psutil.process_iter(["name"]):
                try:
                    if proc.info["name"]:
                        apps.add(proc.info["name"])
                except Exception:
                    pass
            new_apps = apps - last_apps
            for app in new_apps:
                _events.append(
                    {
                        "type": "app_open",
                        "app": app,
                        "time": time.time(),
                    }
                )
            last_apps = apps
        except Exception:
            pass
        time.sleep(2)
    workflow = _detect_pattern(_events)
    if workflow:
        _events = workflow


def _detect_pattern(events: list) -> list:
    if len(events) < 5:
        return events
    deduped = []
    seen = set()
    for e in events:
        key = f"{e.get('type')}:{e.get('app', '')}:{e.get('file', '')}"
        if key not in seen:
            seen.add(key)
            deduped.append(e)
        else:
            deduped[-1]["repeat"] = deduped[-1].get("repeat", 1) + 1
    return deduped


def replay_workflow(name: str) -> str:
    _load()
    workflow = _workflows.get(name)
    if not workflow:
        avail = ", ".join(_workflows.keys())
        return f"Workflow '{name}' not found. Available: {avail}"
    try:
        import subprocess
    except Exception:
        pass
    count = 0
    for event in workflow["events"]:
        if event.get("type") == "app_open" and event.get("app"):
            try:
                app = event["app"]
                if app.endswith(".exe"):
                    subprocess.Popen([app], shell=True)
                count += 1
            except Exception:
                pass
        time.sleep(1)
    return f"Replayed workflow '{name}' ({count} actions)."


def list_workflows() -> str:
    _load()
    if not _workflows:
        return "No saved workflows. Record one first."
    return "Workflows: " + ", ".join(
        f"{name} ({w['count']} steps)" for name, w in _workflows.items()
    )


def delete_workflow(name: str) -> str:
    _load()
    if name in _workflows:
        del _workflows[name]
        _save()
        return f"Workflow '{name}' deleted."
    return f"Workflow '{name}' not found."


def status() -> str:
    _load()
    return (
        f"{'Recording' if _recording else 'Idle'}. {len(_workflows)} saved workflows."
    )
