import json
import os
import socket
import threading
from datetime import datetime

DEVICES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "iot_devices.json"
)

_device_registry = {}
_registry_lock = threading.Lock()


def _ensure_file():
    mem_dir = os.path.dirname(DEVICES_FILE)
    if not os.path.isdir(mem_dir):
        os.makedirs(mem_dir, exist_ok=True)
    if os.path.isfile(DEVICES_FILE):
        with open(DEVICES_FILE) as f:
            global _device_registry
            with _registry_lock:
                _device_registry = json.load(f)


def _save():
    with _registry_lock:
        mem_dir = os.path.dirname(DEVICES_FILE)
        if not os.path.isdir(mem_dir):
            os.makedirs(mem_dir, exist_ok=True)
        with open(DEVICES_FILE, "w") as f:
            json.dump(_device_registry, f, indent=2)


def register_device(
    name: str,
    ip: str,
    port: int = 80,
    device_type: str = "generic",
    commands: dict = None,
):
    _ensure_file()
    with _registry_lock:
        _device_registry[name.lower()] = {
            "name": name,
            "ip": ip,
            "port": port,
            "type": device_type,
            "commands": commands or {},
            "added": datetime.now().isoformat(),
        }
    _save()
    return f"Device '{name}' registered at {ip}:{port}"


def remove_device(name: str):
    _ensure_file()
    with _registry_lock:
        if name.lower() in _device_registry:
            del _device_registry[name.lower()]
            _save()
            return f"Device '{name}' removed."
    return f"Device '{name}' not found."


def list_devices():
    _ensure_file()
    with _registry_lock:
        if not _device_registry:
            return "No devices registered."
        return "Registered devices: " + ", ".join(
            f"{d['name']} ({d['type']} at {d['ip']}:{d['port']})"
            for d in _device_registry.values()
        )


def _send_tcp(ip: str, port: int, command: str) -> str:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))
        sock.sendall(command.encode())
        resp = sock.recv(1024).decode().strip()
        sock.close()
        return resp or "Command sent."
    except socket.timeout:
        return "Device not responding (timeout)."
    except ConnectionRefusedError:
        return "Connection refused. Is the device listening?"
    except Exception as e:
        return f"Error: {e}"


def control_device(name: str, action: str) -> str:
    _ensure_file()
    with _registry_lock:
        device = _device_registry.get(name.lower())
    if not device:
        return f"Device '{name}' not found. Register it first."
    cmd_map = device.get("commands", {})
    cmd = cmd_map.get(action.lower(), action)
    return _send_tcp(device["ip"], device["port"], cmd)


def control_hue_light(bridge_ip: str, light_id: int, action: str, **kwargs):
    """Control Philips Hue lights."""
    try:
        from phue import Bridge

        b = Bridge(bridge_ip)
        b.connect()  # Requires physical button press on first run

        if action.lower() == "on":
            b.set_light(light_id, "on", True)
        elif action.lower() == "off":
            b.set_light(light_id, "on", False)
        elif action.lower() == "brightness":
            bri = kwargs.get("brightness", 127)
            b.set_light(light_id, "bri", bri)
        return f"Hue light {light_id} set to {action}."
    except Exception as e:
        return f"Hue Error: {e}"


def discover_advanced():
    """Discover devices using multiple protocols (UPnP, mDNS, etc.)"""
    # This is a placeholder for advanced discovery logic
    # In a full implementation, we'd use 'zeroconf' or similar
    return (
        "Advanced discovery initialized. Searching for Hue, TP-Link, and MQTT nodes..."
    )
