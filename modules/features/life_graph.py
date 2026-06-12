import json
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "memory_db")


def _load_json(filename: str) -> list:
    path = os.path.join(DATA_DIR, filename)
    if os.path.isfile(path):
        with open(path) as f:
            return json.load(f)
    return []


def get_timeline(days: int = 7) -> str:
    timeline = []
    expenses = _load_json("expenses.json")
    habits = _load_json("habits.json") or {}
    _load_json("screen_time.json") or {}
    fitness = _load_json("fitness.json")

    datetime.now() - timedelta(days=days)
    for e in expenses:
        if "date" in e:
            timeline.append(
                {
                    "type": "expense",
                    "value": e["amount"],
                    "category": e.get("category", ""),
                    "date": e["date"],
                }
            )
    for name, info in habits.items():
        for log_date in info.get("logs", []):
            timeline.append({"type": "habit", "value": name, "date": log_date})
    for f_entry in fitness:
        if "date" in f_entry:
            timeline.append(
                {
                    "type": "fitness",
                    "value": f_entry.get("duration", 0),
                    "detail": f_entry.get("type", ""),
                    "date": f_entry["date"],
                }
            )
    timeline.sort(key=lambda x: x.get("date", ""), reverse=True)
    lines = []
    for item in timeline[:30]:
        t = item.get("type", "")
        date = item.get("date", "")[:10]
        if t == "expense":
            lines.append(
                f"[{date}] 💰 Spent ₹{item.get('value', 0)} on {item.get('category', '')}"
            )
        elif t == "habit":
            lines.append(f"[{date}] ✅ {item.get('value', '')}")
        elif t == "fitness":
            lines.append(
                f"[{date}] 🏃 {item.get('detail', '')} {item.get('value', 0)}min"
            )
    if not lines:
        return (
            f"No data in last {days} days. Start logging expenses, habits, or fitness."
        )
    return " | ".join(lines[:20])


def get_correlations() -> str:
    expenses = _load_json("expenses.json")
    fitness = _load_json("fitness.json")
    habits_data = _load_json("habits.json") or {}
    if not expenses and not fitness:
        return "Not enough data for correlations."
    days_with_exercise = set()
    days_without_exercise = set()
    for f in fitness:
        date = f.get("date", "")[:10]
        if f.get("type") != "food":
            days_with_exercise.add(date)
        else:
            days_without_exercise.add(date)
    total_expenses_exercise = 0
    total_expenses_no_exercise = 0
    count_exercise = 0
    count_no_exercise = 0
    for e in expenses:
        date = e.get("date", "")[:10]
        if date in days_with_exercise:
            total_expenses_exercise += e.get("amount", 0)
            count_exercise += 1
        else:
            total_expenses_no_exercise += e.get("amount", 0)
            count_no_exercise += 1
    lines = []
    if count_exercise > 0:
        avg_ex = total_expenses_exercise / count_exercise
        avg_no = total_expenses_no_exercise / max(count_no_exercise, 1)
        diff = ((avg_no - avg_ex) / max(avg_ex, 1)) * 100
        if diff > 10:
            lines.append(f"Exercise days spend {diff:.0f}% less on average 📊")
        elif diff < -10:
            lines.append(f"Exercise days spend {-diff:.0f}% more 🤔")
        else:
            lines.append("Exercise has minimal impact on spending ✅")
    habits_logs = []
    for name, info in habits_data.items():
        habits_logs.extend(info.get("logs", []))
    set(habits_logs)
    sleep_lines = []
    for f in fitness:
        if "sleep" in f.get("type", "").lower() or f.get("calories", 0) == 0:
            sleep_lines.append(f)
    if sleep_lines:
        lines.append(f"Logged {len(sleep_lines)} sleep/rest periods.")
    if not lines:
        return "More data needed for correlations."
    return " | ".join(lines)


def get_summary() -> str:
    expenses = _load_json("expenses.json")
    fitness = _load_json("fitness.json")
    habits_data = _load_json("habits.json") or {}
    total_expense = sum(e.get("amount", 0) for e in expenses)
    total_workouts = sum(1 for f in fitness if f.get("type") != "food")
    total_cal = sum(f.get("calories", 0) for f in fitness if f.get("type") != "food")
    habit_count = sum(len(info.get("logs", [])) for info in habits_data.values())
    return f"📊 Life Summary: ₹{total_expense:.0f} spent | {total_workouts} workouts ({total_cal} cal) | {habit_count} habit logs"


def get_insight() -> str:
    try:
        from modules.llm.llm_manager import query_llm, TaskType

        summary = get_summary()
        prompt = (
            f"Based on this data, give 1 short life insight (1 sentence): {summary}"
        )
        result = query_llm(prompt, task_type=TaskType.FAST_CONVERSATION)
        return result[:200] if result else summary
    except Exception:
        return get_summary()
