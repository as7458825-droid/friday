import os

TWILIO_SID = os.getenv("TWILIO_API_KEY_SID") or os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_API_KEY_SECRET") or os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM = os.getenv("TWILIO_PHONE_NUMBER", "")


def send_sms(to: str, message: str) -> str:
    if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM]):
        return "Twilio not configured. Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER to .env"
    try:
        from twilio.rest import Client

        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg = client.messages.create(
            body=message[:1600],
            from_=TWILIO_FROM,
            to=to,
        )
        return f"SMS sent to {to}. SID: {msg.sid}"
    except ImportError:
        return "twilio not installed. Run: pip install twilio"
    except Exception as e:
        return f"SMS error: {e}"


def send_sms_contact(name_or_number: str, message: str) -> str:
    import re

    number = re.sub(r"[^0-9+]", "", name_or_number)
    if not number or len(number) < 10:
        return f"Invalid phone number: {name_or_number}"
    return send_sms(number, message)


def status() -> str:
    if all([TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM]):
        return f"SMS relay ready (from: {TWILIO_FROM})."
    return "SMS relay not configured. Add Twilio credentials to .env"
