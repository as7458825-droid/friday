import json
import os

COOKIE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "browser_cookies.json"
)


def save_cookies(page) -> None:
    cookies = page.context.cookies()
    os.makedirs(os.path.dirname(COOKIE_FILE), exist_ok=True)
    with open(COOKIE_FILE, "w") as f:
        json.dump(cookies, f, indent=2)


def load_cookies(page) -> bool:
    if not os.path.isfile(COOKIE_FILE):
        return False
    with open(COOKIE_FILE) as f:
        cookies = json.load(f)
    page.context.add_cookies(cookies)
    return True


def clear_cookies() -> None:
    if os.path.isfile(COOKIE_FILE):
        os.remove(COOKIE_FILE)
