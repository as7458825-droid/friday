import json
import os
import subprocess

HUE_CONFIG = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "hue_bridge.json"
)
_hue_bridge_ip = ""
_hue_username = ""


def discover_hue() -> str:
    try:
        result = subprocess.run(
            ["python", "-m", "phue", "discover"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return f"Hue bridges: {result.stdout[:200]}"
        return "No Hue bridges discovered."
    except Exception:
        return "phue not installed. Run: pip install phue"


def connect_hue(ip: str = "") -> str:
    global _hue_bridge_ip, _hue_username
    if not ip:
        return "Provide bridge IP: connect hue bridge at 192.168.1.100"
    _hue_bridge_ip = ip
    try:
        from phue import Bridge

        b = Bridge(ip)
        b.connect()
        _hue_username = b.username
        os.makedirs(os.path.dirname(HUE_CONFIG), exist_ok=True)
        with open(HUE_CONFIG, "w") as f:
            json.dump({"ip": ip, "username": b.username}, f)
        return f"Connected to Hue bridge at {ip}. Press link button first."
    except Exception as e:
        return f"Hue error: {e}"


def hue_on() -> str:
    try:
        from phue import Bridge

        cfg = _load_hue_config()
        b = Bridge(cfg["ip"])
        b.connect()
        for light in b.lights:
            light.on = True
        return "All Hue lights turned on."
    except Exception as e:
        return f"Hue error: {e}"


def hue_off() -> str:
    try:
        from phue import Bridge

        cfg = _load_hue_config()
        b = Bridge(cfg["ip"])
        b.connect()
        for light in b.lights:
            light.on = False
        return "All Hue lights turned off."
    except Exception as e:
        return f"Hue error: {e}"


def hue_dim(level: int) -> str:
    try:
        from phue import Bridge

        cfg = _load_hue_config()
        b = Bridge(cfg["ip"])
        b.connect()
        for light in b.lights:
            light.brightness = max(1, min(254, int(level * 2.54)))
        return f"Hue lights dimmed to {level}%."
    except Exception as e:
        return f"Hue error: {e}"


def _load_hue_config() -> dict:
    if os.path.isfile(HUE_CONFIG):
        with open(HUE_CONFIG) as f:
            return json.load(f)
    return {}


def hue_status() -> str:
    cfg = _load_hue_config()
    if cfg:
        return f"Hue bridge configured at {cfg.get('ip', 'unknown')}."
    return "No Hue bridge configured. Say 'connect hue bridge at 192.168.1.100'"


def matter_commission() -> str:
    return "Matter support requires Python Matter Server. Run: pip install python-matter-server"


def nest_status() -> str:
    return "Nest API requires Google Cloud project + API key. Check .env for GOOGLE_API_KEY."
