import json
import os
from datetime import datetime, date

HABITS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "habits.json"
)


def _load():
    if os.path.isfile(HABITS_FILE):
        with open(HABITS_FILE) as f:
            return json.load(f)
    return {}


def _save(habits):
    mem = os.path.dirname(HABITS_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(HABITS_FILE, "w") as f:
        json.dump(habits, f, indent=2)


def add_habit(name: str) -> str:
    habits = _load()
    if name in habits:
        return f"Habit '{name}' already exists."
    habits[name] = {"logs": [], "created": datetime.now().isoformat()}
    _save(habits)
    return f"Habit '{name}' added."


def log_habit(name: str) -> str:
    habits = _load()
    if name not in habits:
        return f"Habit '{name}' not found."
    today = date.today().isoformat()
    if today in habits[name]["logs"]:
        return f"Habit '{name}' already logged today."
    habits[name]["logs"].append(today)
    _save(habits)
    streak = _calc_streak(habits[name]["logs"])
    return f"Habit '{name}' logged. {streak}"


def remove_habit(name: str) -> str:
    habits = _load()
    if name in habits:
        del habits[name]
        _save(habits)
        return f"Habit '{name}' removed."
    return f"Habit '{name}' not found."


def list_habits() -> str:
    habits = _load()
    if not habits:
        return "No habits tracked."
    lines = []
    for name, info in habits.items():
        count = len(info["logs"])
        streak = _calc_streak(info["logs"])
        lines.append(f"{name}: {count} days, {streak}")
    return "Habits: " + " | ".join(lines)


def _calc_streak(logs: list) -> str:
    if not logs:
        return "no streak"
    sorted_dates = sorted(set(logs), reverse=True)
    streak = 0
    from datetime import timedelta

    check = date.today()
    while check.isoformat() in sorted_dates:
        streak += 1
        check -= timedelta(days=1)
    return f"{streak}-day streak" if streak > 0 else "no current streak"


def habit_status(name: str) -> str:
    habits = _load()
    if name not in habits:
        return f"Habit '{name}' not found."
    info = habits[name]
    count = len(info["logs"])
    streak = _calc_streak(info["logs"])
    return f"{name}: logged {count} times, {streak}."
