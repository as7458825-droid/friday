import re

_privacy_mode = False

# Patterns for Indian and global PII
PATTERNS = {
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "phone": re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\d{10}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "aadhaar": re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"),
    "pan": re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
}


def enable_privacy_mode():
    global _privacy_mode
    _privacy_mode = True


def disable_privacy_mode():
    global _privacy_mode
    _privacy_mode = False


def is_privacy_mode() -> bool:
    return _privacy_mode


def mask_sensitive_text(text: str) -> str:
    if not _privacy_mode:
        return text
    for name, pattern in PATTERNS.items():
        text = pattern.sub(f"[{name.upper()}:***]", text)
    return text
