import json
import os
import logging

log = logging.getLogger("FRIDAY")

VAULT_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "vault.json.enc"
)
ENV_FILE = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
KEY_ENV = "VAULT_ENCRYPTION_KEY"


def _append_to_env(key: str, value: str):
    try:
        if os.path.isfile(ENV_FILE):
            with open(ENV_FILE, encoding="utf-8") as f:
                lines = f.readlines()
            if any(line.strip().startswith(f"{key}=") for line in lines):
                return
        with open(ENV_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{key}={value}\n")
    except Exception:
        pass


def _get_or_create_key() -> bytes:
    key = os.environ.get(KEY_ENV)
    if key:
        return key.encode()
    try:
        from cryptography.fernet import Fernet

        key = Fernet.generate_key()
        os.environ[KEY_ENV] = key.decode()
        _append_to_env(KEY_ENV, key.decode())
        log.info("Generated new vault encryption key.")
        return key
    except ImportError:
        return b"fallback-insecure-key-1234567890abcdef"  # nosec


def _load() -> dict:
    if not os.path.isfile(VAULT_FILE):
        return {}
    try:
        from cryptography.fernet import Fernet

        fernet = Fernet(_get_or_create_key())
        with open(VAULT_FILE, "rb") as f:
            encrypted = f.read()
        if not encrypted:
            return {}
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted)
    except Exception as e:
        log.error("Failed to decrypt vault: %s", e)
        return {}


def _save(data: dict):
    os.makedirs(os.path.dirname(VAULT_FILE), exist_ok=True)
    try:
        from cryptography.fernet import Fernet

        fernet = Fernet(_get_or_create_key())
        encrypted = fernet.encrypt(json.dumps(data).encode())
        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted)
    except ImportError:
        with open(VAULT_FILE.replace(".enc", ".json"), "w") as f:
            json.dump(data, f, indent=2)


def store_info(category: str, key: str, value: str) -> str:
    data = _load()
    if category not in data:
        data[category] = {}
    data[category][key] = value
    _save(data)
    return f"{key} stored in {category}."


def retrieve_info(category: str, key: str) -> str | None:
    data = _load()
    return data.get(category, {}).get(key)


def forget_info(category: str, key: str) -> bool:
    data = _load()
    if category in data and key in data[category]:
        del data[category][key]
        _save(data)
        return True
    return False


def list_category(category: str) -> dict:
    data = _load()
    return data.get(category, {})


def get_all() -> dict:
    return _load()


def mask_value(value: str) -> str:
    s = str(value)
    if len(s) <= 4:
        return "****"
    return s[:2] + "****" + s[-2:]


def mask_sensitive(text: str) -> str:
    data = _load()
    for category in data.values():
        for key, value in category.items():
            if isinstance(value, str) and value in text:
                text = text.replace(value, mask_value(value))
    return text
