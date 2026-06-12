import json
import os

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "token_notion.json")
BASE = "https://api.notion.com/v1"


def set_token(token: str) -> str:
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token}, f)
    return "Notion token saved."


def _headers():
    tok = ""
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            tok = json.load(f).get("token", "")
    return (
        {
            "Authorization": f"Bearer {tok}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        if tok
        else {}
    )


def query(db_id: str) -> str:
    try:
        import requests

        h = _headers()
        if not h:
            return "Set token first."
        r = requests.post(f"{BASE}/databases/{db_id}/query", headers=h)
        results = r.json().get("results", [])
        items = []
        for res in results[:5]:
            title = "Untitled"
            props = res.get("properties", {})
            for p in props.values():
                if p.get("type") == "title":
                    title = "".join(t.get("plain_text", "") for t in p.get("title", []))
            items.append(title)
        return " | ".join(items)
    except Exception:
        return "Error querying Notion."


def create_page(db_id: str, title: str) -> str:
    try:
        import requests

        h = _headers()
        if not h:
            return "Set token first."
        data = {
            "parent": {"database_id": db_id},
            "properties": {"title": {"title": [{"text": {"content": title}}]}},
        }
        r = requests.post(f"{BASE}/pages", headers=h, json=data)
        return f"Page created: {r.json().get('url', '')}"
    except Exception:
        return "Error creating page."
