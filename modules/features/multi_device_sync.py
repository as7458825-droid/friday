import json
import os
import socket
import threading
import time

SYNC_PORT = 9876
SYNC_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "sync_peers.json"
)
_running = False
_server_thread = None
_peers = {}


def _load():
    global _peers
    if os.path.isfile(SYNC_FILE):
        with open(SYNC_FILE) as f:
            _peers = json.load(f)


def _save():
    mem = os.path.dirname(SYNC_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(SYNC_FILE, "w") as f:
        json.dump(_peers, f, indent=2)


def start_server(name: str = "FRIDAY-PC") -> str:
    global _running, _server_thread
    if _running:
        return "Sync server already running."
    _running = True
    _server_thread = threading.Thread(target=_server_loop, args=(name,), daemon=True)
    _server_thread.start()
    return f"Sync server started as '{name}' on port {SYNC_PORT}."


def stop_server() -> str:
    global _running
    _running = False
    return "Sync server stopped."


def _server_loop(name: str):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("0.0.0.0", SYNC_PORT))
        server.listen(5)
        server.settimeout(2)
        while _running:
            try:
                conn, addr = server.accept()
                data = conn.recv(4096).decode()
                if data.startswith("FRIDAY_SYNC"):
                    parts = data.split("|")
                    peer_name = parts[1] if len(parts) > 1 else "Unknown"
                    _load()
                    _peers[peer_name] = {"ip": addr[0], "last_seen": time.time()}
                    _save()
                    conn.send(f"SYNC_OK|{name}".encode())
                conn.close()
            except socket.timeout:
                pass
    except Exception as e:
        print(f"[SYNC] Server error: {e}")
    finally:
        server.close()


def discover_peers(timeout: int = 3) -> str:
    _load()
    my_ip = socket.gethostbyname(socket.gethostname())
    base = ".".join(my_ip.split(".")[:-1])
    found = []
    for i in range(1, 255):
        ip = f"{base}.{i}"
        if ip == my_ip:
            continue
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((ip, SYNC_PORT))
            sock.send(f"FRIDAY_SYNC|FRIDAY-{socket.gethostname()}".encode())
            resp = sock.recv(4096).decode()
            if resp.startswith("SYNC_OK"):
                peer_name = resp.split("|")[1] if "|" in resp else ip
                found.append(f"{peer_name} ({ip})")
            sock.close()
        except Exception:
            pass
    if found:
        return "Discovered: " + ", ".join(found)
    return "No other FRIDAY instances found on network."


def list_peers() -> str:
    _load()
    if not _peers:
        return "No peers discovered."
    return "Peers: " + ", ".join(f"{n} ({p['ip']})" for n, p in _peers.items())


def get_status() -> str:
    return f"{'Running' if _running else 'Stopped'} on port {SYNC_PORT}."
