import subprocess
import time
import sys
import os


def launch():
    print("--- FRIDAY Ultra: Web Dashboard Launcher ---")

    # 1. Start Python API Bridge
    print("[1/2] Starting Python API Bridge (FastAPI)...")
    api_process = subprocess.Popen(
        [sys.executable, "bridge_api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # 2. Start React Dashboard
    print("[2/2] Starting React Dashboard (Vite)...")
    os.chdir("dashboard")
    ui_process = subprocess.Popen(
        ["npm", "run", "dev"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # 3. Start Holographic Pet
    print("[3/3] Starting Holographic Desktop Pet...")
    pet_process = subprocess.Popen(
        [sys.executable, "holographic_pet.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    print("\nSUCCESS: System is initializing.")
    print("➜ API: http://localhost:8000")
    print("➜ Dashboard: http://localhost:5173")
    print("➜ Holographic Pet: Active (Bottom Right)")
    print("\nPress Ctrl+C to shut down all services.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down FRIDAY Web services...")
        api_process.terminate()
        ui_process.terminate()
        pet_process.terminate()
        print("Goodbye.")


if __name__ == "__main__":
    launch()
