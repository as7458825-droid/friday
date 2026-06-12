import subprocess
import os
import json

VPN_CONFIG_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "vpn_config.json"
)


def _load():
    if os.path.isfile(VPN_CONFIG_FILE):
        with open(VPN_CONFIG_FILE) as f:
            return json.load(f)
    return {"provider": "manual", "config_path": ""}


def _save(data):
    mem = os.path.dirname(VPN_CONFIG_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(VPN_CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def set_vpn(command: str) -> str:
    _save({"provider": "manual", "config_path": command})
    return f"VPN command set: {command}"


def vpn_on() -> str:
    cfg = _load()
    cmd = cfg.get("config_path", "")
    if not cmd:
        return "No VPN configured. Say 'set vpn to your-command' first."
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return f"VPN enabled: {result.stdout[:100]}"
        return f"VPN failed: {result.stderr[:100]}"
    except Exception as e:
        return f"VPN error: {e}"


def vpn_off() -> str:
    return "Disconnect VPN manually or configure a disconnect script."


def vpn_status() -> str:
    try:
        result = subprocess.run(["rasdial"], capture_output=True, text=True, timeout=5)
        lines = [
            line.strip()
            for line in result.stdout.split("\n")
            if line.strip() and "Microsoft" not in line
        ]
        if lines:
            return "Active VPN: " + ", ".join(lines[:3])
        return "No VPN connection detected."
    except Exception:
        return "VPN status check failed."
