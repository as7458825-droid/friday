try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    HAS_CRYPTO = True
except ImportError:
    AES = None
    get_random_bytes = None
    HAS_CRYPTO = False
import logging

logger = logging.getLogger(__name__)


class SecuritySentinel:
    """Advanced Encryption & Security Sentinel for FRIDAY"""

    def encrypt_data(self, data, key=None):
        if not HAS_CRYPTO:
            return "pycryptodome not installed. Run: pip install pycryptodome"
        try:
            key = key or get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data.encode())
            return f"Data encrypted successfully. Key (Hex): {key.hex()}"
        except Exception as e:
            return f"Encryption Error: {e}"


def security_update(command):
    ss = SecuritySentinel()
    if "encrypt" in command or "lock" in command:
        secret = command.split("encrypt")[-1].strip() or "Sample Secret"
        return ss.encrypt_data(secret)
    return "Security Sentinel active. Commands: encrypt [text]."
