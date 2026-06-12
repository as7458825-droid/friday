import json
import os
import re
from datetime import datetime

FITNESS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "fitness.json"
)


def _load():
    if os.path.isfile(FITNESS_FILE):
        with open(FITNESS_FILE) as f:
            return json.load(f)
    return []


def _save(data):
    mem = os.path.dirname(FITNESS_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(FITNESS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_workout(workout_type: str, duration_min: int, calories: int = 0) -> str:
    data = _load()
    data.append(
        {
            "type": workout_type,
            "duration": duration_min,
            "calories": calories,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
    _save(data)
    return f"Logged {duration_min} min {workout_type}."


def log_calories(amount: int, meal: str = "") -> str:
    data = _load()
    data.append(
        {
            "type": "food",
            "calories": amount,
            "meal": meal or "snack",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
    _save(data)
    return f"Logged {amount} cal for {meal or 'snack'}."


def parse_fitness(command: str) -> str:
    cal_m = re.search(
        r"(\d+)\s*cal(?:ories)?\s*(?:for|in)?\s*(.+)", command, re.IGNORECASE
    )
    if cal_m:
        return log_calories(int(cal_m.group(1)), cal_m.group(2).strip())
    work_m = re.search(
        r"(\d+)\s*(?:min|minutes)\s*(?:of|for)?\s*(.+)", command, re.IGNORECASE
    )
    if work_m:
        return log_workout(work_m.group(2).strip(), int(work_m.group(1)))
    return "Usage: log 30 min of running, log 500 cal for lunch"


def get_summary() -> str:
    data = _load()
    if not data:
        return "No fitness data logged."
    today = datetime.now().strftime("%Y-%m-%d")
    today_entries = [d for d in data if d["date"].startswith(today)]
    workouts = [d for d in today_entries if d["type"] != "food"]
    foods = [d for d in today_entries if d["type"] == "food"]
    total_cal_burned = sum(d.get("calories", 0) for d in workouts)
    total_cal_consumed = sum(d.get("calories", 0) for d in foods)
    mins = sum(d.get("duration", 0) for d in workouts)
    return f"Today: {len(workouts)} workouts ({mins} min, {total_cal_burned} cal), {len(foods)} meals ({total_cal_consumed} cal)."
