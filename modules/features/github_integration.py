import json
import os

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "token_github.json")


def set_token(token: str) -> str:
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token}, f)
    return "GitHub token saved."


def _get_token() -> str:
    env_token = os.environ.get("GITHUB_TOKEN", "")
    if env_token:
        return env_token
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return json.load(f).get("token", "")
    return ""


def create_issue(repo: str, title: str, body: str = "") -> str:
    token = _get_token()
    if not token:
        return "Set token first: 'github set token [PAT]'"
    try:
        import requests

        r = requests.post(
            f"https://api.github.com/repos/{repo}/issues",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            json={"title": title, "body": body or ""},
        )
        if r.status_code in (200, 201):
            return f"Issue created: {r.json().get('html_url', '')}"
        return f"Error: {r.json().get('message', '')}"
    except Exception:
        return "requests not available."


def create_pr(repo: str, title: str, head: str, base: str) -> str:
    token = _get_token()
    if not token:
        return "Set token first."
    try:
        import requests

        r = requests.post(
            f"https://api.github.com/repos/{repo}/pulls",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            json={"title": title, "head": head, "base": base},
        )
        if r.status_code in (200, 201):
            return f"PR created: {r.json().get('html_url', '')}"
        return f"Error: {r.json().get('message', '')}"
    except Exception:
        return "requests not available."


def list_issues(repo: str, state: str = "open") -> str:
    try:
        import requests

        r = requests.get(f"https://api.github.com/repos/{repo}/issues?state={state}")
        issues = r.json()
        return " | ".join(f"#{i['number']} {i['title']}" for i in issues[:5])
    except Exception:
        return "requests not available."
