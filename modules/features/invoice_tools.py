import json
import os

from datetime import datetime

DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "invoices.json"
)


def _load():
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []


def _save(data):
    d = os.path.dirname(DATA_FILE)
    if not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add(path: str, vendor: str = "", amount: float = 0, date: str = "") -> str:
    d = _load()
    d.append(
        {
            "path": path,
            "vendor": vendor,
            "amount": amount,
            "date": date or datetime.now().isoformat()[:10],
        }
    )
    _save(d)
    return f"Invoice added: {vendor} ₹{amount}"


def extract(path: str) -> str:
    try:
        import pytesseract
        from PIL import Image

        text = pytesseract.image_to_string(Image.open(path))
    except Exception:
        return "OCR not available."
    import re

    amounts = re.findall(r"[₹$]\s*(\d+[\d,.]*)", text)
    return f"Extracted: {text[:200]}\nAmounts found: {amounts}"


def summary() -> str:
    d = _load()
    total = sum(i.get("amount", 0) for i in d)
    return f"{len(d)} invoices. Total: ₹{total:.0f}"


def monthly_report(month: str = "") -> str:
    d = _load()
    if not month:
        month = datetime.now().strftime("%Y-%m")
    monthly = [i for i in d if i.get("date", "").startswith(month)]
    total = sum(i.get("amount", 0) for i in monthly)
    return f"{len(monthly)} invoices in {month}. Total: ₹{total:.0f}"


def find_duplicates() -> str:
    d = _load()
    paths = [i.get("path", "") for i in d if i.get("path")]
    dupes = [p for p in paths if paths.count(p) > 1]
    return f"Duplicates: {set(dupes)}" if dupes else "No duplicates found."
