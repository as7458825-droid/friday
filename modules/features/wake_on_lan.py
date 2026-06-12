import json
import os
import socket
import struct

DEVICES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "wol_devices.json"
)


def _load():
    if os.path.isfile(DEVICES_FILE):
        with open(DEVICES_FILE) as f:
            return json.load(f)
    return {}


def _save(devices):
    mem = os.path.dirname(DEVICES_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(DEVICES_FILE, "w") as f:
        json.dump(devices, f, indent=2)


def register_wol_device(
    name: str, mac: str, ip: str = "255.255.255.255", port: int = 9
) -> str:
    mac = mac.replace("-", ":").lower()
    devices = _load()
    devices[name] = {"mac": mac, "ip": ip, "port": port}
    _save(devices)
    return f"WOL device '{name}' registered with MAC {mac}."


def wake_device(name: str) -> str:
    devices = _load()
    device = devices.get(name)
    if not device:
        avail = ", ".join(devices.keys())
        return f"Device '{name}' not found. Available: {avail}"
    try:
        mac_bytes = struct.pack("!6B", *[int(x, 16) for x in device["mac"].split(":")])
        magic = b"\xff" * 6 + mac_bytes * 16
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic, (device["ip"], device["port"]))
        sock.close()
        return f"Magic packet sent to {name} ({device['mac']})."
    except Exception as e:
        return f"WOL error: {e}"


def list_wol_devices() -> str:
    devices = _load()
    if not devices:
        return "No WOL devices registered."
    return "WOL devices: " + ", ".join(f"{k} ({v['mac']})" for k, v in devices.items())
