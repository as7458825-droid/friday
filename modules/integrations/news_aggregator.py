import urllib.request
import urllib.parse
import re

RSS_FEEDS = {
    "top": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "tech": "https://feeds.feedburner.com/TechCrunch/",
    "world": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "india": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "science": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    "business": "https://feeds.feedburner.com/entrepreneur/latest",
}


def get_news(category: str = "top", limit: int = 5) -> str:
    feed_url = RSS_FEEDS.get(category.lower())
    if not feed_url:
        avail = ", ".join(RSS_FEEDS.keys())
        return f"Category '{category}' not found. Available: {avail}"
    try:
        req = urllib.request.Request(
            feed_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml = resp.read().decode("utf-8", errors="replace")
        titles = []
        for m in re.finditer(r"<title>(?!CDATA)(.*?)</title>", xml):
            t = m.group(1).strip()
            if t and t not in (
                "",
                "Headlines",
                "Top Stories",
                "TechCrunch",
                "NYT > Science",
                "NYT > World",
            ):
                titles.append(t)
        if not titles:
            for m in re.finditer(r"<title><!\[CDATA\[(.*?)\]\]></title>", xml):
                t = m.group(1).strip()
                if t:
                    titles.append(t)
        if not titles:
            return "No news headlines found."
        selected = titles[1 : limit + 1] if len(titles) > 1 else titles[:limit]
        return f"{category.title()} news: " + " | ".join(selected)
    except Exception as e:
        return f"News fetch error: {e}"


def list_categories():
    return "News categories: " + ", ".join(RSS_FEEDS.keys())
