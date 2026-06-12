import threading
import time

_connected = False
_connection = None
_monitoring = False
_monitor_thread = None


def connect(port: str = "auto") -> str:
    global _connected, _connection
    try:
        import obd
    except ImportError:
        return "python-OBD not installed. Run: pip install obd"
    try:
        if port == "auto":
            _connection = obd.OBD()
        else:
            _connection = obd.OBD(port)
        _connected = _connection.is_connected()
        if _connected:
            return f"Connected to vehicle via {_connection.port_name()}."
        return "Could not connect. Ensure OBD-II adapter is paired."
    except Exception as e:
        return f"OBD error: {e}"


def disconnect() -> str:
    global _connected, _connection, _monitoring
    _monitoring = False
    if _connection:
        _connection.close()
    _connected = False
    return "Disconnected from vehicle."


def get_rpm() -> str:
    if not _connected:
        return "Not connected. Say 'connect obd' first."
    try:
        import obd

        resp = _connection.query(obd.commands.RPM)
        if resp and resp.value:
            return f"RPM: {resp.value.magnitude:.0f}"
        return "RPM unavailable."
    except Exception as e:
        return f"RPM error: {e}"


def get_speed() -> str:
    if not _connected:
        return "Not connected."
    try:
        import obd

        resp = _connection.query(obd.commands.SPEED)
        if resp and resp.value:
            return f"Speed: {resp.value.magnitude:.0f} km/h"
        return "Speed unavailable."
    except Exception as e:
        return f"Speed error: {e}"


def get_fuel() -> str:
    if not _connected:
        return "Not connected."
    try:
        import obd

        resp = _connection.query(obd.commands.FUEL_LEVEL)
        if resp and resp.value:
            return f"Fuel: {resp.value.magnitude:.0f}%"
        return "Fuel level unavailable."
    except Exception as e:
        return f"Fuel error: {e}"


def get_coolant_temp() -> str:
    if not _connected:
        return "Not connected."
    try:
        import obd

        resp = _connection.query(obd.commands.COOLANT_TEMP)
        if resp and resp.value:
            return f"Coolant: {resp.value.magnitude:.0f}°C"
        return "Coolant temp unavailable."
    except Exception as e:
        return f"Temp error: {e}"


def get_dtc() -> str:
    if not _connected:
        return "Not connected."
    try:
        import obd

        resp = _connection.query(obd.commands.GET_DTC)
        if resp and resp.value:
            codes = [str(c) for c in resp.value]
            return f"Trouble codes: {', '.join(codes)}"
        return "No trouble codes."
    except Exception as e:
        return f"DTC error: {e}"


def get_dashboard() -> str:
    return " | ".join(
        filter(None, [get_rpm(), get_speed(), get_fuel(), get_coolant_temp()])
    )


def start_monitoring(interval: int = 5) -> str:
    global _monitoring, _monitor_thread
    if _monitoring:
        return "Already monitoring."
    if not _connected:
        return "Not connected to vehicle."
    _monitoring = True
    _monitor_thread = threading.Thread(
        target=_monitor_loop, args=(interval,), daemon=True
    )
    _monitor_thread.start()
    return "Vehicle monitoring started."


def stop_monitoring() -> str:
    global _monitoring
    _monitoring = False
    return "Monitoring stopped."


def _monitor_loop(interval: int):
    while _monitoring:
        try:
            line = get_dashboard()
            if line:
                print(f"[OBD] {line}")
        except Exception:
            pass
        time.sleep(interval)


def status() -> str:
    if _connected:
        return f"Connected to vehicle. Monitoring: {'active' if _monitoring else 'inactive'}."
    return "Not connected. Say 'connect obd' with adapter plugged in."
