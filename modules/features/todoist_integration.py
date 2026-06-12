import json
import os
import requests

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "token_todoist.json")


def set_token(token: str) -> str:
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token}, f)
    return "Todoist token saved."


def _get_token() -> str:
    env_token = os.environ.get("TODOIST_API_TOKEN", "")
    if env_token:
        return env_token
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return json.load(f).get("token", "")
    return ""


def list_tasks() -> str:
    tok = _get_token()
    if not tok:
        return "Set token first or add TODOIST_API_TOKEN to .env"
    r = requests.get(
        "https://api.todoist.com/rest/v2/tasks",
        headers={"Authorization": f"Bearer {tok}"},
    )
    tasks = r.json()
    return " | ".join(t["content"] for t in tasks[:5]) if tasks else "No tasks."


def add_task(task: str, project_id: str = "") -> str:
    tok = _get_token()
    if not tok:
        return "Set token first or add TODOIST_API_TOKEN to .env"
    data = {"content": task}
    if project_id:
        data["project_id"] = project_id
    requests.post(
        "https://api.todoist.com/rest/v2/tasks",
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
        json=data,
    )
    return f"Task added: {task}"


def complete(task_id: str) -> str:
    tok = _get_token()
    if not tok:
        return "Set token first or add TODOIST_API_TOKEN to .env"
    requests.post(
        f"https://api.todoist.com/rest/v2/tasks/{task_id}/close",
        headers={"Authorization": f"Bearer {tok}"},
    )
    return f"Task {task_id} completed."
