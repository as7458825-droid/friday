from modules.browser_engine.mod_041_playwright_instance_core import get_browser


def scrape_text() -> str:
    browser = get_browser()
    return browser.get_page_text()


def scrape_with_url(url: str) -> str:
    from modules.browser_engine.mod_041_playwright_instance_core import goto

    goto(url)
    return scrape_text()
