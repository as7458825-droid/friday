import json
import os
import re
from datetime import datetime

EXPENSES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "expenses.json"
)


def _load():
    if os.path.isfile(EXPENSES_FILE):
        with open(EXPENSES_FILE) as f:
            return json.load(f)
    return []


def _save(expenses):
    mem = os.path.dirname(EXPENSES_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(EXPENSES_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(amount: float, category: str, description: str = "") -> str:
    expenses = _load()
    expenses.append(
        {
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    )
    _save(expenses)
    return f"Logged ₹{amount} for {category}."


def parse_expense(command: str) -> str:
    m = re.search(
        r"(\d+\.?\d*)\s*(?:rs|rupees|₹)?\s*(?:for|on|in)?\s*(.+)",
        command,
        re.IGNORECASE,
    )
    if m:
        amount = float(m.group(1))
        rest = m.group(2).strip()
        parts = rest.split()
        cat = parts[0] if parts else "general"
        desc = " ".join(parts[1:]) if len(parts) > 1 else ""
        return add_expense(amount, cat, desc)
    return "Usage: expense 500 for food, expense 2000 on groceries"


def get_total() -> str:
    expenses = _load()
    if not expenses:
        return "No expenses logged."
    total = sum(e["amount"] for e in expenses)
    by_cat = {}
    for e in expenses:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["amount"]
    cats = ", ".join(f"{c}: ₹{v:.0f}" for c, v in sorted(by_cat.items()))
    return f"Total expenses: ₹{total:.0f}. Breakdown: {cats}."


def get_today() -> str:
    expenses = _load()
    today = datetime.now().strftime("%Y-%m-%d")
    today_exp = [e for e in expenses if e["date"].startswith(today)]
    if not today_exp:
        return "No expenses today."
    total = sum(e["amount"] for e in today_exp)
    return f"Today: ₹{total:.0f} in {len(today_exp)} expenses."


def get_monthly() -> str:
    expenses = _load()
    month = datetime.now().strftime("%Y-%m")
    month_exp = [e for e in expenses if e["date"].startswith(month)]
    if not month_exp:
        return "No expenses this month."
    total = sum(e["amount"] for e in month_exp)
    return f"This month: ₹{total:.0f} in {len(month_exp)} expenses."


def clear_all() -> str:
    _save([])
    return "All expenses cleared."
