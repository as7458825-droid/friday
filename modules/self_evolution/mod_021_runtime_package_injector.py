import importlib
import subprocess
import sys


def ensure_package(package_name: str, confirm: bool = True) -> bool:
    try:
        importlib.import_module(package_name.replace("-", "_"))
        return True
    except ImportError:
        pass

    if confirm:
        print(f"\n[INSTALL] Package '{package_name}' is required.")
        answer = input(f"Install {package_name}? (yes/no): ").strip().lower()
        if answer != "yes":
            return False

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        importlib.invalidate_caches()
        importlib.import_module(package_name.replace("-", "_"))
        return True
    except Exception:
        return False
