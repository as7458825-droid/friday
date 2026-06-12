import socket
import subprocess
import threading
import time

_scan_active = False
_scan_thread = None
_discovered_hosts = []


def ping_host(ip: str) -> bool:
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ip],
            capture_output=True,
            text=True,
            timeout=2,
        )
        return "Reply from" in result.stdout
    except Exception:
        return False


def scan_network(subnet: str = "192.168.1") -> str:
    global _discovered_hosts
    _discovered_hosts = []
    found = []
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        if ping_host(ip):
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except Exception:
                hostname = "Unknown"
            found.append(f"{ip} ({hostname})")
    _discovered_hosts = found
    if found:
        return f"Found {len(found)} hosts: " + ", ".join(found[:20])
    return "No hosts found."


def continuous_scan(subnet: str = "192.168.1", interval: int = 60):
    global _scan_active, _scan_thread
    if _scan_active:
        return "Already scanning."
    _scan_active = True

    def _loop():
        while _scan_active:
            scan_network(subnet)
            time.sleep(interval)

    _scan_thread = threading.Thread(target=_loop, daemon=True)
    _scan_thread.start()
    return f"Continuous scan started every {interval}s on {subnet}.0/24"


def stop_scan():
    global _scan_active
    _scan_active = False
    return "Network scanning stopped."


def check_port(host: str, port: int) -> str:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return f"Port {port} on {host} is OPEN"
        return f"Port {port} on {host} is CLOSED"
    except Exception as e:
        return f"Port check error: {e}"


def network_status() -> str:
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        gateways = []
        try:
            result = subprocess.run(
                ["ipconfig"], capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if "Default Gateway" in line and ":" in line:
                    gw = line.split(":")[-1].strip()
                    if gw and gw != ":":
                        gateways.append(gw)
        except Exception:
            pass
        gw_str = f", Gateway: {gateways[0]}" if gateways else ""
        ping = "Connected" if ping_host("8.8.8.8") else "No internet"
        return f"Host: {hostname}, IP: {ip}{gw_str}, Internet: {ping}"
    except Exception as e:
        return f"Network status error: {e}"
