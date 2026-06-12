import platform
import subprocess
import threading
import time

_attempts: list[float] = []


def _check_auth_log() -> list[str]:
    system = platform.system()
    failures = []

    if system == "Linux":
        try:
            result = subprocess.run(
                ["journalctl", "-u", "sshd", "--since", "1 minute ago", "--no-pager"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            for line in result.stdout.split("\n"):
                if "Failed password" in line:
                    failures.append(line)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    elif system == "Windows":
        try:
            result = subprocess.run(
                [
                    "wevtutil",
                    "qe",
                    "Security",
                    "/q:*[System[(EventID=4625)]]",
                    "/c:10",
                    "/rd:true",
                    "/format:text",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            for line in result.stdout.split("\n"):
                if line.strip():
                    failures.append(line)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    return failures


def _monitor_loop():
    global _attempts
    while True:
        now = time.time()
        new = _check_auth_log()
        for _ in new:
            _attempts.append(now)

        _attempts = [t for t in _attempts if now - t < 60]

        if len(_attempts) >= 5:
            print("[SECURITY] 5+ failed login attempts in 1 minute!")
            _attempts = []

        time.sleep(15)


def start_auth_monitor():
    t = threading.Thread(target=_monitor_loop, daemon=True)
    t.start()
