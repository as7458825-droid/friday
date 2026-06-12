import json
import os
from datetime import datetime

FINANCIAL_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "financial_plan.json"
)


def _load():
    if os.path.isfile(FINANCIAL_FILE):
        with open(FINANCIAL_FILE) as f:
            return json.load(f)
    return {"monthly_budget": {}, "savings_goal": 0, "income": 0}


def _save(data):
    mem = os.path.dirname(FINANCIAL_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(FINANCIAL_FILE, "w") as f:
        json.dump(data, f, indent=2)


def set_income(amount: float) -> str:
    data = _load()
    data["income"] = amount
    _save(data)
    return f"Monthly income set to ₹{amount:.0f}."


def set_budget(category: str, amount: float) -> str:
    data = _load()
    data["monthly_budget"][category] = amount
    _save(data)
    return f"Budget for {category}: ₹{amount:.0f}/month."


def set_savings_goal(amount: float) -> str:
    data = _load()
    data["savings_goal"] = amount
    _save(data)
    return f"Savings goal set to ₹{amount:.0f}."


def get_report() -> str:
    data = _load()
    try:
        from modules.features.expense_tracker import _load as load_expenses

        expenses = load_expenses()
    except Exception:
        expenses = []
    current_month = datetime.now().strftime("%Y-%m")
    month_exp = [e for e in expenses if e["date"].startswith(current_month)]
    total_spent = sum(e["amount"] for e in month_exp)
    by_cat = {}
    for e in month_exp:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["amount"]
    lines = []
    income = data.get("income", 0)
    if income:
        remaining = income - total_spent
        lines.append(f"Income: ₹{income:.0f}")
        lines.append(f"Spent: ₹{total_spent:.0f}")
        lines.append(f"Remaining: ₹{remaining:.0f}")
    else:
        lines.append(f"Total spent this month: ₹{total_spent:.0f}")
    for cat, budget in data.get("monthly_budget", {}).items():
        spent = by_cat.get(cat, 0)
        pct = (spent / budget * 100) if budget > 0 else 0
        alert = "⚠️" if pct > 80 else "✅" if pct < 50 else "⚡"
        lines.append(f"{cat}: ₹{spent:.0f}/{budget:.0f} ({pct:.0f}%) {alert}")
    goal = data.get("savings_goal", 0)
    if goal:
        progress = min(100, (total_spent / goal) * 100) if goal else 0
        lines.append(f"Savings goal: ₹{goal:.0f} ({progress:.0f}%)")
    return " | ".join(lines)


def forecast(days: int = 30) -> str:
    data = _load()
    try:
        from modules.features.expense_tracker import _load as load_expenses

        expenses = load_expenses()
    except Exception:
        return "Expense tracker not available."
    if not expenses:
        return "No expense data for forecast."
    recent = expenses[-30:] if len(expenses) > 30 else expenses
    avg_daily = sum(e["amount"] for e in recent) / max(len(recent), 1)
    projected = avg_daily * days
    income = data.get("income", 0)
    if income:
        monthly_income = income
        balance = monthly_income - projected
        return f"Projected spending next {days}d: ₹{projected:.0f}. Balance: ₹{balance:.0f}."
    return f"Projected spending next {days}d: ₹{projected:.0f}."
