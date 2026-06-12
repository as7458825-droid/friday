import hashlib
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "config.py")
_CHECKSUM_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "config_checksum.txt"
)


def _compute_checksum() -> str:
    if not os.path.isfile(CONFIG_FILE):
        return ""
    with open(CONFIG_FILE, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def save_checksum():
    chk = _compute_checksum()
    os.makedirs(os.path.dirname(_CHECKSUM_FILE), exist_ok=True)
    with open(_CHECKSUM_FILE, "w") as f:
        f.write(chk)


def verify_config_integrity() -> bool:
    if not os.path.isfile(_CHECKSUM_FILE):
        save_checksum()
        return True
    with open(_CHECKSUM_FILE) as f:
        saved = f.read().strip()
    return _compute_checksum() == saved


def protect_config():
    if os.path.isfile(CONFIG_FILE):
        os.chmod(CONFIG_FILE, 0o444)


def unprotect_config():
    if os.path.isfile(CONFIG_FILE):
        os.chmod(CONFIG_FILE, 0o644)
