import threading
import time

from plyer import notification

_timer_active = False
_timer_thread = None
_timer_type = ""
_remaining = 0


def start_pomodoro(minutes: int = 25) -> str:
    global _timer_active, _timer_thread, _timer_type, _remaining
    if _timer_active:
        return "Timer already running."
    _timer_active = True
    _timer_type = "pomodoro"
    _remaining = minutes * 60
    _timer_thread = threading.Thread(target=_countdown, daemon=True)
    _timer_thread.start()
    return f"Pomodoro started for {minutes} minutes."


def start_short_break(minutes: int = 5) -> str:
    global _timer_active, _timer_thread, _timer_type, _remaining
    if _timer_active:
        return "Timer already running."
    _timer_active = True
    _timer_type = "short_break"
    _remaining = minutes * 60
    _timer_thread = threading.Thread(target=_countdown, daemon=True)
    _timer_thread.start()
    return f"Short break for {minutes} minutes."


def start_long_break(minutes: int = 15) -> str:
    global _timer_active, _timer_thread, _timer_type, _remaining
    if _timer_active:
        return "Timer already running."
    _timer_active = True
    _timer_type = "long_break"
    _remaining = minutes * 60
    _timer_thread = threading.Thread(target=_countdown, daemon=True)
    _timer_thread.start()
    return f"Long break for {minutes} minutes."


def stop_timer() -> str:
    global _timer_active
    if not _timer_active:
        return "No timer running."
    _timer_active = False
    return "Timer stopped."


def timer_status() -> str:
    if not _timer_active:
        return "No timer running."
    mins = _remaining // 60
    secs = _remaining % 60
    return f"{_timer_type}: {mins:02d}:{secs:02d} remaining."


def _countdown():
    global _remaining, _timer_active
    while _timer_active and _remaining > 0:
        time.sleep(1)
        _remaining -= 1
    if _timer_active:
        _timer_active = False
        try:
            notification.notify(
                title="FRIDAY Timer", message=f"{_timer_type} completed!", timeout=10
            )
        except Exception:
            pass
        print(f"[POMODORO] {_timer_type} completed!")
