import os

API_KEY = os.environ.get("GMAIL_API_KEY", "")
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]


def connect() -> str:
    return "Use 'gmail auth' to authenticate via OAuth."


def list_inbox(max_results: int = 5) -> str:
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
    except Exception:
        return "google-api-python-client not installed. Run: pip install google-api-python-client google-auth-oauthlib"
    token = os.path.join(os.path.dirname(__file__), "..", "..", "token_gmail.json")
    if not os.path.isfile(token):
        return "Not authenticated. Say 'gmail auth' first."
    creds = Credentials.from_authorized_user_file(token, SCOPES)
    service = build("gmail", "v1", credentials=creds)
    results = (
        service.users().messages().list(userId="me", maxResults=max_results).execute()
    )
    msgs = results.get("messages", [])
    if not msgs:
        return "No messages."
    out = []
    for m in msgs:
        msg = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=m["id"],
                format="metadata",
                metadataHeaders=["From", "Subject"],
            )
            .execute()
        )
        headers = {
            h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])
        }
        out.append(f"{headers.get('From', '')} - {headers.get('Subject', '')}")
    return " | ".join(out[:5])


def send(to: str, subject: str, body: str) -> str:
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        from googleapiclient.errors import HttpError
        from email.mime.text import MIMEText
        import base64
    except Exception:
        return "google-api-python-client not installed."
    token = os.path.join(os.path.dirname(__file__), "..", "..", "token_gmail.json")
    if not os.path.isfile(token):
        return "Not authenticated."
    creds = Credentials.from_authorized_user_file(token, SCOPES)
    service = build("gmail", "v1", credentials=creds)
    msg = MIMEText(body)
    msg["To"] = to
    msg["Subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    try:
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        return f"Email sent to {to}."
    except HttpError as e:
        return f"Error: {e}"


def smart_reply(email_text: str) -> str:
    try:
        from advanced.llm.llm_manager import query_llm, TaskType

        result = query_llm(
            f"Write a professional reply to this email:\n{email_text}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return result or "Reply generated."
    except Exception:
        return "LLM not available."


def auth() -> str:
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except Exception:
        return "google-auth-oauthlib not installed."
    flow = InstalledAppFlow.from_client_secrets_file("google_credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open("token_gmail.json", "w") as f:
        f.write(creds.to_json())
    return "Gmail authenticated. You can now read/send emails."
