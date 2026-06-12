import os

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "token_calendar.json")

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def connect() -> str:
    return "Use 'calendar auth' to authenticate via OAuth."


def auth() -> str:
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except Exception:
        return "google-auth-oauthlib not installed."
    flow = InstalledAppFlow.from_client_secrets_file("google_credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open("token_calendar.json", "w") as f:
        f.write(creds.to_json())
    return "Calendar authenticated."


def list_events(max_results: int = 5) -> str:
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
    except Exception:
        return "google-api-python-client not installed."
    token = os.path.join(os.path.dirname(__file__), "..", "..", "token_calendar.json")
    if not os.path.isfile(token):
        return "Not authenticated."
    creds = Credentials.from_authorized_user_file(token, SCOPES)
    service = build("calendar", "v3", credentials=creds)
    events = (
        service.events()
        .list(
            calendarId="primary",
            maxResults=max_results,
            orderBy="startTime",
            singleEvents=True,
        )
        .execute()
    )
    items = events.get("items", [])
    if not items:
        return "No upcoming events."
    out = []
    for e in items:
        start = e["start"].get("dateTime", e["start"].get("date", ""))[:10]
        out.append(f"{start}: {e['summary']}")
    return " | ".join(out)


def add(summary: str, date: str, time_str: str = "10:00", duration: int = 60) -> str:
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        from datetime import datetime, timedelta
    except Exception:
        return "google-api-python-client not installed."
    token = os.path.join(os.path.dirname(__file__), "..", "..", "token_calendar.json")
    if not os.path.isfile(token):
        return "Not authenticated."
    creds = Credentials.from_authorized_user_file(token, SCOPES)
    service = build("calendar", "v3", credentials=creds)
    start_dt = f"{date}T{time_str}:00"
    end_dt = (
        datetime.fromisoformat(start_dt) + timedelta(minutes=duration)
    ).isoformat()
    event = {
        "summary": summary,
        "start": {"dateTime": start_dt, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_dt, "timeZone": "Asia/Kolkata"},
    }
    service.events().insert(calendarId="primary", body=event).execute()
    return f"Event added: {summary} on {date} at {time_str}."
