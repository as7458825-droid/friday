import json
import os
import shutil
import threading
import time
from datetime import datetime

BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "backups")
CONFIG_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "backup_config.json"
)

_scheduler_active = False
_scheduler_thread = None


def _ensure_dir():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    mem = os.path.dirname(CONFIG_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)


def _load_config() -> dict:
    _ensure_dir()
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"sources": [], "interval_hours": 24}


def _save_config(cfg: dict):
    _ensure_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def add_backup_source(path: str) -> str:
    cfg = _load_config()
    abs_path = os.path.abspath(path)
    if abs_path in cfg["sources"]:
        return f"{abs_path} already in backup list."
    cfg["sources"].append(abs_path)
    _save_config(cfg)
    return f"Added {abs_path} to backup sources."


def remove_backup_source(path: str) -> str:
    cfg = _load_config()
    abs_path = os.path.abspath(path)
    if abs_path in cfg["sources"]:
        cfg["sources"].remove(abs_path)
        _save_config(cfg)
        return f"Removed {abs_path} from backup sources."
    return "Path not in backup list."


def list_sources() -> str:
    cfg = _load_config()
    if not cfg["sources"]:
        return "No backup sources configured."
    return "Backup sources: " + ", ".join(cfg["sources"])


def run_backup() -> str:
    cfg = _load_config()
    if not cfg["sources"]:
        return "No backup sources configured."
    _ensure_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    count = 0
    errors = 0
    for src in cfg["sources"]:
        if not os.path.exists(src):
            errors += 1
            continue
        dest = os.path.join(BACKUP_DIR, f"{os.path.basename(src)}_{timestamp}")
        try:
            if os.path.isfile(src):
                shutil.copy2(src, dest)
            else:
                shutil.copytree(src, dest, dirs_exist_ok=True)
            count += 1
        except Exception:
            errors += 1
    return f"Backup complete: {count} items backed up, {errors} errors."


def set_interval(hours: int) -> str:
    cfg = _load_config()
    cfg["interval_hours"] = hours
    _save_config(cfg)
    return f"Backup interval set to {hours} hours."


def start_scheduler():
    global _scheduler_active, _scheduler_thread
    if _scheduler_active:
        return
    _scheduler_active = True
    _scheduler_thread = threading.Thread(target=_scheduler_loop, daemon=True)
    _scheduler_thread.start()


def stop_scheduler():
    global _scheduler_active
    _scheduler_active = False


def _scheduler_loop():
    while _scheduler_active:
        cfg = _load_config()
        if cfg["sources"]:
            run_backup()
        time.sleep(cfg["interval_hours"] * 3600)
