import os
import subprocess
from cryptography.fernet import Fernet

KEY_FILE = os.path.join(os.path.dirname(__file__), "..", "..", ".env.key")
ENV_FILE = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
ENCRYPTED_FILE = ENV_FILE + ".encrypted"
JAVA_BIN = os.path.join(os.path.dirname(__file__), "VaultEncryptor")


def _run_java_vault(mode: str, data: str) -> str:
    """Execute Java-based high-speed encryption."""
    try:
        # Get the directory of this file to run java from the right place
        vault_dir = os.path.dirname(__file__)
        process = subprocess.Popen(
            ["java", "-cp", vault_dir, "VaultEncryptor", mode, data, KEY_FILE],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()
        if "RESULT:" in stdout:
            return stdout.split("RESULT:")[1].strip()
        return None
    except Exception as e:
        print(f"[SECURITY] Java Vault Error: {e}")
        return None


def _load_or_create_key() -> bytes:
    if os.path.isfile(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print(f"[SECURITY] Encryption key saved to {KEY_FILE}")
    return key


def encrypt_env_file() -> str:
    if not os.path.isfile(ENV_FILE):
        return "No .env file found."

    with open(ENV_FILE, "r") as env:
        data = env.read()

    # Try Java First (High Speed)
    encrypted = _run_java_vault("encrypt", data)
    if encrypted:
        with open(ENCRYPTED_FILE, "w") as out:
            out.write(encrypted)
        return f"Encrypted using Java Vault to {ENCRYPTED_FILE}"

    # Fallback to Python Cryptography
    key = _load_or_create_key()
    f = Fernet(key)
    encrypted_py = f.encrypt(data.encode())
    with open(ENCRYPTED_FILE, "wb") as out:
        out.write(encrypted_py)

    return f"Encrypted using Python Fallback to {ENCRYPTED_FILE}"


def decrypt_env_file() -> str:
    if not os.path.isfile(ENCRYPTED_FILE) or not os.path.isfile(KEY_FILE):
        return "No encrypted file or key found."

    with open(ENCRYPTED_FILE, "r") as ef:
        encrypted_data = ef.read()

    # Try Java Decryption
    decrypted = _run_java_vault("decrypt", encrypted_data)

    if not decrypted:
        # Try Python Fallback
        try:
            with open(KEY_FILE, "rb") as kf:
                key = kf.read()
            f = Fernet(key)
            with open(ENCRYPTED_FILE, "rb") as ef_py:
                encrypted_py = ef_py.read()
            decrypted = f.decrypt(encrypted_py).decode()
        except Exception:
            return "Decryption failed in both Java and Python."

    # Load into current environment
    for line in decrypted.strip().split("\n"):
        if "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

    return "Environment loaded successfully (High-Speed Java Vault)."
