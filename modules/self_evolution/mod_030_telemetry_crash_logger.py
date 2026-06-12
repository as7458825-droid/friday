import json
import os
import traceback
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "logs")


def log_crash(exc: Exception, context: str = "") -> str:
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crash_{timestamp}.json"
    path = os.path.join(LOG_DIR, filename)

    report = {
        "timestamp": timestamp,
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(),
        "context": context,
    }

    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"[CRASH] Logged to {path}")
    return path


def list_crashes() -> list[str]:
    if not os.path.isdir(LOG_DIR):
        return []
    return sorted(
        os.path.join(LOG_DIR, f)
        for f in os.listdir(LOG_DIR)
        if f.startswith("crash_") and f.endswith(".json")
    )
