import subprocess
import importlib.util

HAS_REQUESTS = importlib.util.find_spec("requests") is not None


def check_ollama() -> bool:
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def query_ollama(prompt: str, model: str = "llama3.2") -> str | None:
    if not check_ollama():
        return None
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def fallback_respond(prompt: str) -> str:
    if check_ollama():
        response = query_ollama(prompt)
        if response:
            return response
    return (
        "Offline fallback: I'm running in offline mode. Some features may be limited."
    )
