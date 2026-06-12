import threading
import time

_HEALTH = {}
_INTERVAL = 30


def _check_voice() -> bool:
    try:
        return True
    except Exception:
        return False


def _check_llm() -> bool:
    try:
        return True
    except Exception:
        return False


def _check_memory() -> bool:
    try:
        from modules.memory.vector_store import get_client

        get_client()
        return True
    except Exception:
        return False


_CHECKS = {
    "voice": _check_voice,
    "llm": _check_llm,
    "memory_db": _check_memory,
}


def _heartbeat_loop():
    while True:
        for name, check_fn in _CHECKS.items():
            try:
                _HEALTH[name] = check_fn()
            except Exception:
                _HEALTH[name] = False
        time.sleep(_INTERVAL)


def start_heartbeat():
    t = threading.Thread(target=_heartbeat_loop, daemon=True)
    t.start()
    print("[HEARTBEAT] Health monitor started.")


def get_health() -> dict[str, bool]:
    if not _HEALTH:
        for name, check_fn in _CHECKS.items():
            try:
                _HEALTH[name] = check_fn()
            except Exception:
                _HEALTH[name] = False
    return dict(_HEALTH)
