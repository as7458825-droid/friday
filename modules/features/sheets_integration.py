import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "token_sheets.json")


def auth() -> str:
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except Exception:
        return "google-auth-oauthlib not installed."
    flow = InstalledAppFlow.from_client_secrets_file("google_credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())
    return "Sheets authenticated."


def read(spreadsheet_id: str, range_name: str = "Sheet1!A1:E10") -> str:
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
    except Exception:
        return "google-api-python-client not installed."
    if not os.path.isfile(TOKEN_FILE):
        return "Not authenticated."
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build("sheets", "v4", credentials=creds)
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    rows = result.get("values", [])
    return " | ".join(", ".join(row) for row in rows[:5])


def write(spreadsheet_id: str, range_name: str, values_csv: str) -> str:
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
    except Exception:
        return "google-api-python-client not installed."
    if not os.path.isfile(TOKEN_FILE):
        return "Not authenticated."
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build("sheets", "v4", credentials=creds)
    rows = [[v.strip() for v in row.split(",")] for row in values_csv.split(";")]
    body = {"values": rows}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )
    return f"{result.get('updatedCells', 0)} cells updated."
