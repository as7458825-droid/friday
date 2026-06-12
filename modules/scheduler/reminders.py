import json
import os
import threading
import time
from datetime import datetime, timedelta
from plyer import notification

SCHEDULE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "schedule.json"
)

_schedule = []
_schedule_lock = threading.Lock()
_scheduler_thread = None
_running = False


def _ensure_file():
    mem_dir = os.path.dirname(SCHEDULE_FILE)
    if not os.path.isdir(mem_dir):
        os.makedirs(mem_dir, exist_ok=True)
    if os.path.isfile(SCHEDULE_FILE):
        with open(SCHEDULE_FILE) as f:
            global _schedule
            with _schedule_lock:
                _schedule = json.load(f)


def _save():
    with _schedule_lock:
        mem_dir = os.path.dirname(SCHEDULE_FILE)
        if not os.path.isdir(mem_dir):
            os.makedirs(mem_dir, exist_ok=True)
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(_schedule, f, indent=2)


def set_reminder(text: str, when: str) -> str:
    _ensure_file()
    try:
        datetime.strptime(when, "%Y-%m-%d %H:%M")
    except ValueError:
        return "Time format should be YYYY-MM-DD HH:MM (e.g. 2025-12-25 18:30)."
    with _schedule_lock:
        _schedule.append({"text": text, "time": when, "done": False})
    _save()
    return f"Reminder set for {when}: {text}"


def set_reminder_natural(command: str) -> str:
    import re

    now = datetime.now()
    time_map = {
        r"in (\d+) (seconds?|secs?)": ("seconds", 1),
        r"in (\d+) (minutes?|mins?)": ("minutes", 1),
        r"in (\d+) (hours?)": ("hours", 1),
        r"in (\d+) (days?)": ("days", 1),
        r"(?:at|by) (\d{1,2}):(\d{2})\s*(am|pm)": ("time", None),
    }
    reminder_text = re.sub(
        r"(remind me|reminder|set reminder|to|for|at|in)\s+",
        "",
        command,
        flags=re.IGNORECASE,
    ).strip()
    for pattern, (unit, _) in time_map.items():
        m = re.search(pattern, command, re.IGNORECASE)
        if m:
            if unit == "time":
                h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3).lower()
                if ap == "pm" and h < 12:
                    h += 12
                elif ap == "am" and h == 12:
                    h = 0
                reminder_time = now.replace(hour=h, minute=mi, second=0, microsecond=0)
                if reminder_time < now:
                    reminder_time += timedelta(days=1)
            else:
                val = int(m.group(1))
                kwargs = {unit: val}
                reminder_time = now + timedelta(**kwargs)
            reminder_text = re.sub(pattern, "", command, flags=re.IGNORECASE).strip()
            reminder_text = re.sub(
                r"(remind me|reminder|set reminder|to)\s+",
                "",
                reminder_text,
                flags=re.IGNORECASE,
            ).strip()
            return set_reminder(reminder_text, reminder_time.strftime("%Y-%m-%d %H:%M"))
    return "Could not parse time. Use format: remind me to do something in 10 minutes"


def get_reminders() -> str:
    _ensure_file()
    with _schedule_lock:
        pending = [r for r in _schedule if not r.get("done")]
        if not pending:
            return "No pending reminders."
        lines = []
        for r in pending:
            lines.append(f"{r['text']} at {r['time']}")
        return "Reminders: " + ". ".join(lines)


def _check_loop():
    global _running
    _running = True
    while _running:
        try:
            _ensure_file()
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            triggered = []
            with _schedule_lock:
                for r in _schedule:
                    if not r.get("done") and r["time"] <= now:
                        r["done"] = True
                        triggered.append(r["text"])
                if triggered:
                    _save()
            for t in triggered:
                try:
                    notification.notify(
                        title="FRIDAY Reminder",
                        message=t,
                        timeout=10,
                    )
                except Exception:
                    pass
                print(f"[REMINDER] {t}")
        except Exception:
            pass
        time.sleep(30)


def start_scheduler():
    global _scheduler_thread
    if _scheduler_thread is None or not _scheduler_thread.is_alive():
        _scheduler_thread = threading.Thread(target=_check_loop, daemon=True)
        _scheduler_thread.start()


def stop_scheduler():
    global _running
    _running = False


def schedule_daily(time_str: str, task: str) -> str:
    _ensure_file()
    with _schedule_lock:
        _schedule.append({"text": task, "time": time_str, "done": False, "daily": True})
    _save()
    return f"Daily task scheduled at {time_str}: {task}"


def list_scheduled_tasks() -> str:
    _ensure_file()
    with _schedule_lock:
        daily = [r for r in _schedule if r.get("daily")]
        if not daily:
            return "No daily scheduled tasks."
        return "Scheduled tasks: " + ". ".join(
            f"{r['text']} at {r['time']}" for r in daily
        )
