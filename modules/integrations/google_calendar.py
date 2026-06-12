import datetime
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TOKEN_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "google_calendar_token.pickle"
)
CREDENTIALS_FILE = os.environ.get("GOOGLE_CREDENTIALS_PATH", "google_credentials.json")


def _get_service():
    creds = None
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return build("calendar", "v3", credentials=creds)


def get_upcoming_events(max_results: int = 5) -> str:
    try:
        service = _get_service()
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        if not events:
            return "No upcoming events found."
        lines = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "No title")
            lines.append(f"{summary} at {start}")
        return "Upcoming events: " + "; ".join(lines)
    except Exception as e:
        return f"Calendar error: {e}"


def get_events_today() -> str:
    try:
        service = _get_service()
        now = datetime.datetime.utcnow()
        end_of_day = now.replace(hour=23, minute=59, second=59)
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now.isoformat() + "Z",
                timeMax=end_of_day.isoformat() + "Z",
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        if not events:
            return "No events scheduled for today."
        lines = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "No title")
            time_str = start.split("T")[1][:5] if "T" in start else start
            lines.append(f"{summary} at {time_str}")
        return "Today's events: " + "; ".join(lines)
    except Exception as e:
        return f"Calendar error: {e}"
