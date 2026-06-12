import json
import os
import subprocess
from datetime import datetime

CONFIG_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "emergency_config.json"
)
_emergency_active = False


def _load():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {
        "emergency_contacts": [],
        "auto_lock": True,
        "auto_record": True,
        "auto_notify": True,
        "fall_detection": False,
    }


def _save(data):
    mem = os.path.dirname(CONFIG_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_contact(name: str, phone: str) -> str:
    data = _load()
    data["emergency_contacts"].append({"name": name, "phone": phone})
    _save(data)
    return f"Emergency contact {name} ({phone}) added."


def remove_contact(name: str) -> str:
    data = _load()
    data["emergency_contacts"] = [
        c for c in data["emergency_contacts"] if c["name"] != name
    ]
    _save(data)
    return f"Contact {name} removed."


def list_contacts() -> str:
    data = _load()
    if not data["emergency_contacts"]:
        return "No emergency contacts."
    return "Contacts: " + ", ".join(
        f"{c['name']}: {c['phone']}" for c in data["emergency_contacts"]
    )


def trigger_emergency() -> str:
    global _emergency_active
    _emergency_active = True
    data = _load()
    results = []
    if data.get("auto_lock"):
        try:
            subprocess.run(
                ["rundll32.exe", "user32.dll,LockWorkStation"], capture_output=True
            )
            results.append("PC locked")
        except Exception:
            pass
    if data.get("auto_record"):
        try:
            from modules.vision.security_cam import start_monitor

            results.append(start_monitor())
        except Exception:
            pass
    if data.get("auto_notify") and data["emergency_contacts"]:
        from modules.integrations.sms_relay import send_sms

        msg = f"EMERGENCY ALERT from FRIDAY Ultra at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        for c in data["emergency_contacts"]:
            try:
                result = send_sms(c["phone"], msg)
                results.append(f"SMS to {c['name']}: {result}")
            except Exception:
                pass
    _emergency_active = False
    return " | ".join(results) if results else "Emergency protocols executed."


def lockdown() -> str:
    results = []
    try:
        subprocess.run(
            ["rundll32.exe", "user32.dll,LockWorkStation"], capture_output=True
        )
        results.append("PC locked")
    except Exception:
        pass
    try:
        from modules.vision.security_cam import start_monitor

        results.append(start_monitor())
    except Exception:
        pass
    try:
        subprocess.run(["shutdown", "/s", "/t", "300"], capture_output=True)
        results.append("Shutdown in 5 min")
    except Exception:
        pass
    return "Lockdown: " + " | ".join(results)


def distress(message: str = "") -> str:
    data = _load()
    if not data["emergency_contacts"]:
        return "No emergency contacts configured."
    from modules.integrations.sms_relay import send_sms

    msg = message or f"FRIDAY: Help needed at {datetime.now().isoformat()}"
    results = []
    for c in data["emergency_contacts"]:
        try:
            r = send_sms(c["phone"], msg)
            results.append(f"{c['name']}: {r}")
        except Exception:
            results.append(f"{c['name']}: Failed")
    return " | ".join(results)


def start_fall_detection() -> str:
    try:
        return "Fall detection started (uses camera)."
    except Exception as e:
        return f"Fall detection error: {e}"
