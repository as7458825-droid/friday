import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]
TOKEN_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "google_gmail_token.pickle"
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
    return build("gmail", "v1", credentials=creds)


def get_unread_emails(max_results: int = 3) -> str:
    try:
        service = _get_service()
        results = (
            service.users()
            .messages()
            .list(userId="me", q="is:unread", maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])
        if not messages:
            return "No unread emails."
        lines = []
        for msg in messages:
            msg_data = (
                service.users().messages().get(userId="me", id=msg["id"]).execute()
            )
            headers = {
                h["name"]: h["value"]
                for h in msg_data.get("payload", {}).get("headers", [])
            }
            sender = headers.get("From", "Unknown").split("<")[0].strip()
            subject = headers.get("Subject", "No subject")
            snippet = msg_data.get("snippet", "")[:60]
            lines.append(f"From {sender}: {subject} - {snippet}")
        return "Unread emails: " + " | ".join(lines)
    except Exception as e:
        return f"Gmail error: {e}"


def send_email(to: str, subject: str, body: str) -> str:
    try:
        service = _get_service()
        msg = MIMEText(body)
        msg["To"] = to
        msg["Subject"] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        return f"Email sent to {to}."
    except Exception as e:
        return f"Send email error: {e}"
