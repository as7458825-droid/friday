import os
import tempfile
from datetime import datetime


def screenshot(url: str) -> str:
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return "playwright not installed. Run: pip install playwright && python -m playwright install chromium"
    path = os.path.join(
        tempfile.gettempdir(), f"screenshot_{int(datetime.now().timestamp())}.png"
    )
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=path)
        browser.close()
    os.startfile(path)
    return f"Screenshot saved to {path}"


def test_url(url: str) -> str:
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return "playwright not installed."
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        title = page.title()
        console_logs = []
        page.on("console", lambda msg: console_logs.append(msg.text))
        status = "OK" if page.title() else "Empty"
        browser.close()
        return f"{title} - {status}. Console: {' | '.join(console_logs[:3])}"


def fill_form(url: str, fields: str) -> str:
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return "playwright not installed."
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        pairs = [f.strip().split("=", 1) for f in fields.split(",") if "=" in f]
        for selector, value in pairs:
            try:
                page.fill(selector.strip(), value.strip())
            except Exception:
                pass
        browser.close()
        return f"Filled {len(pairs)} fields."


def list_console(url: str) -> str:
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return "playwright not installed."
    logs = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
        page.goto(url)
        browser.close()
    return " | ".join(logs[:10]) if logs else "No console logs."
