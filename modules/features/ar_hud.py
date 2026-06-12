import json
import socket
import threading

HUD_PORT = 9877
_active = False
_server_thread = None


def start_bridge() -> str:
    global _active, _server_thread
    if _active:
        return "HUD bridge already running."
    _active = True
    _server_thread = threading.Thread(target=_bridge_loop, daemon=True)
    _server_thread.start()
    return f"AR HUD bridge started on port {HUD_PORT}. Connect from your headset."


def stop_bridge() -> str:
    global _active
    _active = False
    return "HUD bridge stopped."


def _bridge_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("0.0.0.0", HUD_PORT))
        server.listen(5)
        server.settimeout(2)
        while _active:
            try:
                conn, addr = server.accept()
                data = conn.recv(4096).decode()
                if data == "GET_HUD":
                    import psutil
                    from datetime import datetime

                    hud = {
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "cpu": psutil.cpu_percent(interval=0.1),
                        "ram": psutil.virtual_memory().percent,
                        "greeting": "FRIDAY Ultra Online",
                    }
                    conn.send(json.dumps(hud).encode())
                conn.close()
            except socket.timeout:
                pass
    except Exception as e:
        print(f"[AR-HUD] Error: {e}")
    finally:
        server.close()


def get_hud_data() -> dict:
    import psutil
    from datetime import datetime

    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "cpu": psutil.cpu_percent(interval=0.1),
        "ram": psutil.virtual_memory().percent,
        "cpu_temp": "N/A",
        "greeting": "FRIDAY Ultra Online",
    }


def status() -> str:
    return f"HUD bridge {'active' if _active else 'inactive'} on port {HUD_PORT}."
