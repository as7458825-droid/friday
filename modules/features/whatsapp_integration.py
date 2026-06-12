import json
import os

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "token_whatsapp.json")


def set_session(session_path: str = "") -> str:
    if session_path:
        data = {"session_path": session_path}
    else:
        data = {"use_web": True}
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)
    return "WhatsApp session saved."


def send(phone: str, message: str) -> str:
    try:
        from twilio.rest import Client
    except Exception:
        return "twilio not installed."
    sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
    token = os.environ.get("TWILIO_AUTH_TOKEN", "")
    if not sid or not token:
        return "Twilio not configured."
    client = Client(sid, token)
    msg = client.messages.create(
        body=message, from_=os.environ.get("TWILIO_PHONE_NUMBER", ""), to=phone
    )
    return f"WhatsApp sent to {phone} (SID: {msg.sid})"


def send_signal(phone: str, message: str) -> str:
    try:
        import subprocess

        subprocess.run(
            [
                "signal-cli",
                "-u",
                os.environ.get("SIGNAL_NUMBER", ""),
                "send",
                "-m",
                message,
                phone,
            ],
            timeout=10,
        )
        return f"Signal sent to {phone}."
    except Exception:
        return "signal-cli not installed."
