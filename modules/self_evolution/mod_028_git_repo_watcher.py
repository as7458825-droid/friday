import os
import subprocess

WATCHED_REPOS = {
    "friday": {
        "url": "https://github.com/anthropics/claude-code.git",
        "local": os.path.join(os.path.dirname(__file__), "..", ".."),
    }
}


def check_for_updates(repo_name: str = "friday") -> str | None:
    info = WATCHED_REPOS.get(repo_name)
    if not info:
        return None

    local = info["local"]
    git_dir = os.path.join(local, ".git")
    if not os.path.isdir(git_dir):
        return f"No git repository at {local}"

    try:
        subprocess.run(
            ["git", "-C", local, "remote", "update"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        result = subprocess.run(
            ["git", "-C", local, "status", "-uno"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if "Your branch is behind" in result.stdout:
            return "Updates available."
        return "Up to date."
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "Git check failed."


def pull_updates(repo_name: str = "friday") -> str:
    info = WATCHED_REPOS.get(repo_name)
    if not info:
        return "Unknown repo."
    try:
        result = subprocess.run(
            ["git", "-C", info["local"], "pull"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout[:300]
        return f"Pull failed: {result.stderr[:200]}"
    except Exception as e:
        return f"Pull error: {e}"
