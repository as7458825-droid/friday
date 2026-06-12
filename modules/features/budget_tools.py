import json
import os
from datetime import datetime

DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "budget.json"
)


def _load():
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"income": 0, "budget": {}, "expenses": []}


def _save(data):
    d = os.path.dirname(DATA_FILE)
    if not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def set_income(amount: float) -> str:
    data = _load()
    data["income"] = amount
    _save(data)
    return f"Monthly income set to ₹{amount}"


def set_budget(category: str, amount: float) -> str:
    data = _load()
    data["budget"][category.lower()] = amount
    _save(data)
    return f"Budget for {category}: ₹{amount}"


def add_expense(category: str, amount: float, note: str = "") -> str:
    data = _load()
    data["expenses"].append(
        {
            "category": category.lower(),
            "amount": amount,
            "note": note,
            "date": datetime.now().isoformat()[:10],
        }
    )
    _save(data)
    return f"Expense added: ₹{amount} on {category}"


def get_status() -> str:
    data = _load()
    total_expense = sum(e["amount"] for e in data["expenses"])
    remaining = data["income"] - total_expense
    return f"Income: ₹{data['income']:.0f} | Spent: ₹{total_expense:.0f} | Remaining: ₹{remaining:.0f}"


def budget_health() -> str:
    data = _load()
    alerts = []
    for cat, limit in data.get("budget", {}).items():
        spent = sum(e["amount"] for e in data["expenses"] if e["category"] == cat)
        if spent > limit:
            alerts.append(f"{cat}: ₹{spent:.0f} (limit ₹{limit:.0f}) OVER")
        else:
            alerts.append(f"{cat}: ₹{spent:.0f}/{limit:.0f}")
    return " | ".join(alerts) if alerts else "No budgets set."


def upi_parse(text: str) -> str:
    import re

    amounts = re.findall(r"(?:Rs|₹|INR)\s*(\d+[\d,.]*)", text, re.IGNORECASE)
    return (
        f"Detected payments: {[float(a.replace(',', '')) for a in amounts]}"
        if amounts
        else "No UPI amounts found."
    )


def split_bill(amounts_csv: str) -> str:
    amounts = [float(a.strip()) for a in amounts_csv.split(",") if a.strip()]
    if not amounts:
        return "No amounts provided."
    total = sum(amounts)
    each = total / len(amounts)
    return f"Total: ₹{total:.0f} | Each pays: ₹{each:.0f}"
