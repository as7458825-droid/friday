import json
import os
import re
from datetime import datetime, timedelta

SCHEDULED_MEETINGS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "meetings.json"
)


def _load():
    if os.path.isfile(SCHEDULED_MEETINGS_FILE):
        with open(SCHEDULED_MEETINGS_FILE) as f:
            return json.load(f)
    return []


def _save(meetings):
    mem = os.path.dirname(SCHEDULED_MEETINGS_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(SCHEDULED_MEETINGS_FILE, "w") as f:
        json.dump(meetings, f, indent=2)


def schedule_meeting(
    title: str, date_str: str, time_str: str, duration_min: int = 30
) -> str:
    meetings = _load()
    dt_str = f"{date_str} {time_str}"
    try:
        datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return "Date format: YYYY-MM-DD, Time format: HH:MM (24h)"
    meetings.append(
        {
            "title": title,
            "datetime": dt_str,
            "duration": duration_min,
            "created": datetime.now().isoformat(),
        }
    )
    _save(meetings)
    return f"Meeting '{title}' scheduled for {dt_str}."


def schedule_from_natural(command: str) -> str:
    now = datetime.now()
    m = re.search(r"tomorrow", command, re.IGNORECASE)
    if m:
        date = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date = now.strftime("%Y-%m-%d")
    m = re.search(r"(\d{1,2}):(\d{2})\s*(am|pm)?", command, re.IGNORECASE)
    if m:
        h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3)
        if ap and ap.lower() == "pm" and h < 12:
            h += 12
        elif ap and ap.lower() == "am" and h == 12:
            h = 0
        time_str = f"{h:02d}:{mi:02d}"
    else:
        time_str = now.strftime("%H:%M")
    title = re.sub(
        r"(schedule|meeting|tomorrow|at|for|with)\s+", "", command, flags=re.IGNORECASE
    ).strip()
    if not title:
        title = "Meeting"
    return schedule_meeting(title, date, time_str)


def list_meetings(upcoming_only: bool = True) -> str:
    meetings = _load()
    if not meetings:
        return "No meetings scheduled."
    now = datetime.now()
    if upcoming_only:
        meetings = [
            m
            for m in meetings
            if datetime.strptime(m["datetime"], "%Y-%m-%d %H:%M") > now
        ]
    if not meetings:
        return "No upcoming meetings."
    lines = [
        f"{m['title']} at {m['datetime']} ({m['duration']}min)" for m in meetings[:10]
    ]
    return "Meetings: " + " | ".join(lines)


def cancel_meeting(title: str) -> str:
    meetings = _load()
    for i, m in enumerate(meetings):
        if title.lower() in m["title"].lower():
            cancelled = meetings.pop(i)
            _save(meetings)
            return f"Cancelled: {cancelled['title']} at {cancelled['datetime']}"
    return f"Meeting '{title}' not found."


def find_free_slot(date_str: str, duration_min: int = 30) -> str:
    meetings = _load()
    day_meetings = [m for m in meetings if m["datetime"].startswith(date_str)]
    if not day_meetings:
        return f"All day free on {date_str}."
    day_meetings.sort(key=lambda m: m["datetime"])
    start = 9
    for m in day_meetings:
        m_time = datetime.strptime(m["datetime"], "%Y-%m-%d %H:%M")
        m_hour = m_time.hour
        if m_hour - start >= duration_min / 60:
            return f"Free slot at {start:02d}:00 on {date_str}."
        start = m_hour + m["duration"] / 60
    if 18 - start >= duration_min / 60:
        return f"Free slot at {int(start):02d}:00 on {date_str}."
    return f"No free slots on {date_str}."
