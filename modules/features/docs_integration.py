import os

SCOPES = ["https://www.googleapis.com/auth/documents"]
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "token_docs.json")


def auth() -> str:
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except Exception:
        return "google-auth-oauthlib not installed."
    flow = InstalledAppFlow.from_client_secrets_file("google_credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())
    return "Docs authenticated."


def create(title: str, content: str = "") -> str:
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
    except Exception:
        return "google-api-python-client not installed."
    if not os.path.isfile(TOKEN_FILE):
        return "Not authenticated."
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build("docs", "v1", credentials=creds)
    doc = service.documents().create(body={"title": title}).execute()
    doc_id = doc.get("documentId", "")
    if content:
        requests_body = {
            "requests": [{"insertText": {"location": {"index": 1}, "text": content}}]
        }
        service.documents().batchUpdate(documentId=doc_id, body=requests_body).execute()
    return f"Doc created: https://docs.google.com/document/d/{doc_id}"


def read(doc_id: str) -> str:
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
    except Exception:
        return "google-api-python-client not installed."
    if not os.path.isfile(TOKEN_FILE):
        return "Not authenticated."
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build("docs", "v1", credentials=creds)
    doc = service.documents().get(documentId=doc_id).execute()
    text = ""
    for el in doc.get("body", {}).get("content", []):
        if "paragraph" in el:
            for t in el["paragraph"].get("elements", []):
                text += t.get("textRun", {}).get("content", "")
    return text[:500] or "Empty document."
