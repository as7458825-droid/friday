import threading
import time

import psutil

_known_ports: set[int] = set()
_alert_ports: list[dict] = []

COMMON_PORTS = {80, 443, 22, 21, 3306, 5432, 27017, 6379, 8080, 8443, 53, 123}


def _scan_connections() -> list[dict]:
    results = []
    try:
        for conn in psutil.net_connections():
            if conn.status == "LISTEN" and conn.laddr:
                results.append(
                    {
                        "port": conn.laddr.port,
                        "pid": conn.pid,
                        "status": conn.status,
                    }
                )
    except (psutil.AccessDenied, PermissionError):
        pass
    return results


def _monitor_loop():
    global _known_ports
    while True:
        current = {c["port"] for c in _scan_connections()}
        new_ports = current - _known_ports - COMMON_PORTS
        for port in new_ports:
            alert = {
                "port": port,
                "time": time.strftime("%H:%M:%S"),
                "type": "unknown",
            }
            _alert_ports.append(alert)
            print(f"[NET] Unknown port opened: {port}")
        _known_ports = current
        time.sleep(10)


def start_port_monitor():
    t = threading.Thread(target=_monitor_loop, daemon=True)
    t.start()


def get_alerts() -> list[dict]:
    return list(_alert_ports)
