import gc
import threading
import time

import psutil

_THRESHOLD_MB = 512
_monitor_active = False


def _monitor_loop():
    global _monitor_active
    while _monitor_active:
        process = psutil.Process()
        mem_mb = process.memory_info().rss / 1024 / 1024
        if mem_mb > _THRESHOLD_MB:
            print(f"[MEMORY] {mem_mb:.0f} MB — running garbage collection...")
            gc.collect()
            after = process.memory_info().rss / 1024 / 1024
            print(f"[MEMORY] Freed {mem_mb - after:.0f} MB (now {after:.0f} MB)")
        time.sleep(30)


def start_monitor():
    global _monitor_active
    if not _monitor_active:
        _monitor_active = True
        t = threading.Thread(target=_monitor_loop, daemon=True)
        t.start()
        print("[MEMORY] Monitor started.")


def stop_monitor():
    global _monitor_active
    _monitor_active = False


def get_memory_usage_mb() -> float:
    return psutil.Process().memory_info().rss / 1024 / 1024
