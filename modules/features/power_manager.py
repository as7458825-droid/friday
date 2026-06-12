import subprocess


def shutdown(seconds: int = 60) -> str:
    try:
        subprocess.run(
            ["shutdown", "/s", "/t", str(seconds)], check=True, capture_output=True
        )
        return f"Shutting down in {seconds} seconds."
    except Exception as e:
        return f"Shutdown error: {e}"


def restart(seconds: int = 30) -> str:
    try:
        subprocess.run(
            ["shutdown", "/r", "/t", str(seconds)], check=True, capture_output=True
        )
        return f"Restarting in {seconds} seconds."
    except Exception as e:
        return f"Restart error: {e}"


def hibernate() -> str:
    try:
        subprocess.run(["shutdown", "/h"], check=True, capture_output=True)
        return "Hibernating..."
    except Exception as e:
        return f"Hibernate error: {e}"


def sleep() -> str:
    try:
        subprocess.run(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
            check=True,
            capture_output=True,
        )
        return "Going to sleep..."
    except Exception as e:
        return f"Sleep error: {e}"


def abort_shutdown() -> str:
    try:
        subprocess.run(["shutdown", "/a"], check=True, capture_output=True)
        return "Shutdown aborted."
    except Exception as e:
        return f"Abort error: {e}"


def lock() -> str:
    try:
        subprocess.run(
            ["rundll32.exe", "user32.dll,LockWorkStation"],
            check=True,
            capture_output=True,
        )
        return "Workstation locked."
    except Exception as e:
        return f"Lock error: {e}"


def schedule_shutdown(time_str: str) -> str:
    try:
        import re
        from datetime import datetime, timedelta

        now = datetime.now()
        m = re.match(r"(\d{1,2}):(\d{2})\s*(am|pm)?", time_str, re.IGNORECASE)
        if m:
            h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3)
            if ap and ap.lower() == "pm" and h < 12:
                h += 12
            elif ap and ap.lower() == "am" and h == 12:
                h = 0
            target = now.replace(hour=h, minute=mi, second=0, microsecond=0)
            if target < now:
                target += timedelta(days=1)
            seconds = int((target - now).total_seconds())
            return shutdown(seconds)
        m2 = re.match(r"in (\d+) (minutes?|hours?|seconds?)", time_str, re.IGNORECASE)
        if m2:
            val = int(m2.group(1))
            unit = m2.group(2).lower()
            mult = {"second": 1, "minute": 60, "hour": 3600}
            seconds = val * mult.get(unit.rstrip("s"), 60)
            return shutdown(seconds)
        return "Could not parse time. Use format: at 10pm, or in 30 minutes"
    except Exception as e:
        return f"Schedule error: {e}"
