import urllib.parse
import urllib.request


def search_web(query: str, num_results: int = 5) -> str:
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        results = []
        import re

        for m in re.finditer(
            r'<a rel="nofollow" class="result__a" href="(.*?)".*?>(.*?)</a>',
            html,
            re.DOTALL,
        ):
            link = m.group(1)
            title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            results.append(f"{title} - {link}")
            if len(results) >= num_results:
                break
        if results:
            return "Search results: " + " | ".join(results)
        return "No search results found."
    except Exception as e:
        return f"Search error: {e}"
