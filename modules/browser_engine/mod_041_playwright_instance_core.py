try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    sync_playwright = None
    HAS_PLAYWRIGHT = False


class PlaywrightBrowser:
    def __init__(self, headless: bool = False):
        self._playwright = None
        self.browser = None
        self.page = None
        self.headless = headless

    def start(self):
        if not HAS_PLAYWRIGHT:
            raise ImportError("playwright not installed. Run: pip install playwright && playwright install")
        self._playwright = sync_playwright().start()
        self.browser = self._playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        return self

    def goto(self, url: str):
        if not url.startswith("http"):
            url = f"https://{url}"
        self.page.goto(url, wait_until="domcontentloaded")
        return self.page.title()

    def screenshot(self, path: str = "screenshot.png"):
        self.page.screenshot(path=path)
        return path

    def get_page_text(self) -> str:
        return self.page.inner_text("body")

    def click(self, selector: str):
        self.page.click(selector)

    def fill(self, selector: str, text: str):
        self.page.fill(selector, text)

    def close(self):
        if self.browser:
            self.browser.close()
        if self._playwright:
            self._playwright.stop()


_browser_instance: "PlaywrightBrowser | None" = None


def get_browser() -> "PlaywrightBrowser":
    global _browser_instance
    if not HAS_PLAYWRIGHT:
        raise ImportError("playwright not installed. Run: pip install playwright && playwright install")
    if _browser_instance is None:
        _browser_instance = PlaywrightBrowser()
        _browser_instance.start()
    return _browser_instance


def close_browser():
    global _browser_instance
    if _browser_instance:
        _browser_instance.close()
        _browser_instance = None


def goto(url: str) -> str:
    return get_browser().goto(url)


def screenshot(path: str = "screenshot.png") -> str:
    return get_browser().screenshot(path)


def get_page_text() -> str:
    return get_browser().get_page_text()


def click(selector: str):
    get_browser().click(selector)


def fill(selector: str, text: str):
    get_browser().fill(selector, text)


def close():
    close_browser()
