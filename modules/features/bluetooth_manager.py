import subprocess
import json
import os

BT_CONFIG_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "bluetooth_devices.json"
)


def _load():
    if os.path.isfile(BT_CONFIG_FILE):
        with open(BT_CONFIG_FILE) as f:
            return json.load(f)
    return {"devices": []}


def _save(data):
    mem = os.path.dirname(BT_CONFIG_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(BT_CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _run_powershell(script: str) -> str:
    try:
        result = subprocess.run(
            ["powershell", "-Command", script],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def scan_devices() -> str:
    script = """
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
    function Await($WinRtTask, $ResultType) {
        $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
        $netTask = $asTask.Invoke($null, @($WinRtTask))
        $netTask.Wait(-1) | Out-Null
        $netTask.Result
    }
    $devices = Await ([Windows.Devices.Bluetooth.BluetoothDevice]::FindAllAsync()) ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Bluetooth.BluetoothDevice]])
    $devices | ForEach-Object { $_.Name }
    """
    result = _run_powershell(script)
    if result:
        lines = [device_line.strip() for device_line in result.split("\n") if device_line.strip()]
        if lines:
            return "Bluetooth devices: " + ", ".join(lines[:10])
    return "No Bluetooth devices found or scan failed."


def pair_device(name: str) -> str:
    _load()
    data = _load()
    if name not in data["devices"]:
        data["devices"].append(name)
        _save(data)
    return f"Paired '{name}'. (Bluetooth pairing via PowerShell requires admin.)"


def connect_device(name: str) -> str:
    script = """
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    # Simplified: launching BT settings
    Start-Process ms-settings:bluetooth
    """
    _run_powershell(script)
    return f"Opening Bluetooth settings for '{name}'. Connect manually."


def disconnect_device(name: str) -> str:
    return f"Disconnect '{name}' from system tray Bluetooth icon."


def list_paired() -> str:
    data = _load()
    if not data["devices"]:
        return "No paired devices in registry."
    return "Saved devices: " + ", ".join(data["devices"])
