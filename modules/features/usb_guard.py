import json
import os
import subprocess
import threading
import time

USB_WHITELIST_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "usb_whitelist.json"
)
_active = False
_thread = None


def _load():
    if os.path.isfile(USB_WHITELIST_FILE):
        with open(USB_WHITELIST_FILE) as f:
            return json.load(f)
    return {"whitelist": [], "block_unknown": True}


def _save(data):
    mem = os.path.dirname(USB_WHITELIST_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(USB_WHITELIST_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _get_usb_devices() -> list:
    try:
        result = subprocess.run(
            ["wmic", "path", "Win32_USBControllerDevice", "get", "Dependent"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        ids = []
        for line in result.stdout.split("\n"):
            if "DeviceID=" in line:
                m = __import__("re").search(r'DeviceID="([^"]+)"', line)
                if m:
                    ids.append(m.group(1))
        return ids
    except Exception:
        return []


def add_to_whitelist(device_id: str) -> str:
    data = _load()
    if device_id not in data["whitelist"]:
        data["whitelist"].append(device_id)
        _save(data)
        return f"Device '{device_id}' added to whitelist."
    return "Device already whitelisted."


def remove_from_whitelist(device_id: str) -> str:
    data = _load()
    if device_id in data["whitelist"]:
        data["whitelist"].remove(device_id)
        _save(data)
        return f"Device '{device_id}' removed from whitelist."
    return "Device not in whitelist."


def start_guard() -> str:
    global _active, _thread
    if _active:
        return "USB guard already running."
    _active = True
    _thread = threading.Thread(target=_guard_loop, daemon=True)
    _thread.start()
    return "USB guard started."


def stop_guard() -> str:
    global _active
    _active = False
    return "USB guard stopped."


def _guard_loop():
    known = set()
    while _active:
        current = set(_get_usb_devices())
        new = current - known
        data = _load()
        for dev in new:
            if data.get("block_unknown") and dev not in data["whitelist"]:
                print(f"[USB GUARD] Unknown device detected: {dev}")
        known = current
        time.sleep(5)


def guard_status() -> str:
    data = _load()
    wl = data.get("whitelist", [])
    return f"USB guard: {'active' if _active else 'inactive'}. {len(wl)} whitelisted devices."
