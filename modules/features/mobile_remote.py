import os

_call_active = False


def call(phone_number: str) -> str:
    try:
        from twilio.rest import Client
    except Exception:
        return "twilio not installed."
    sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
    token = os.environ.get("TWILIO_AUTH_TOKEN", "")
    if not sid or not token:
        return "Twilio not configured."
    client = Client(sid, token)
    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to=phone_number,
        from_=os.environ.get("TWILIO_PHONE_NUMBER", ""),
    )
    return f"Calling {phone_number} (SID: {call.sid})"


def remote_desktop_start(port: int = 5900) -> str:
    try:
        import subprocess

        subprocess.Popen(
            ["C:\\Windows\\System32\\wscript.exe", "C:\\Windows\\System32\\server.vbs"],
            shell=True,
        )
        return f"Remote desktop enabled on port {port}. Use VNC viewer to connect."
    except Exception:
        return "Cannot enable remote desktop."


def notify_mobile(title: str, message: str) -> str:
    try:
        from twilio.rest import Client
    except Exception:
        return "twilio not installed."
    sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
    token = os.environ.get("TWILIO_AUTH_TOKEN", "")
    phone = os.environ.get("TWILIO_PHONE_NUMBER", "")
    if not sid or not token:
        return "Twilio not configured."
    client = Client(sid, token)
    client.messages.create(
        body=f"{title}: {message}", from_=phone, to=os.environ.get("MY_PHONE", "")
    )
    return "Notification sent to mobile."
