import threading
import time

import psutil

_connected_devices: set[str] = set()


def _list_usb_devices() -> list[str]:
    devices = []
    for part in psutil.disk_partitions():
        if "removable" in part.opts or "cdrom" in part.opts:
            devices.append(part.device)
    return devices


def _monitor_loop(interval: int = 5):
    global _connected_devices
    while True:
        current = set(_list_usb_devices())
        new_devices = current - _connected_devices
        removed_devices = _connected_devices - current

        for dev in new_devices:
            print(f"[USB] Device connected: {dev}")

        for dev in removed_devices:
            print(f"[USB] Device removed: {dev}")

        _connected_devices = current
        time.sleep(interval)


def start_usb_monitor():
    t = threading.Thread(target=_monitor_loop, daemon=True)
    t.start()
    print("[USB] Monitor started.")


def get_connected_devices() -> list[str]:
    return list(_connected_devices)
