import hashlib
import os

VOICE_PASS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "voice_pass.json"
)


def _get_hash(text: str) -> str:
    return hashlib.sha256(text.lower().strip().encode()).hexdigest()


def set_voice_password(password: str) -> str:
    mem = os.path.dirname(VOICE_PASS_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    with open(VOICE_PASS_FILE, "w") as f:
        f.write(_get_hash(password))
    return "Voice password set."


def check_voice_password(password: str) -> bool:
    if not os.path.isfile(VOICE_PASS_FILE):
        return True
    with open(VOICE_PASS_FILE) as f:
        stored = f.read().strip()
    return _get_hash(password) == stored


def lock_system(voice_obj=None) -> str:
    import subprocess

    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], capture_output=True)
    return "System locked by voice."


def unlock_system(voice_obj) -> str:
    if not os.path.isfile(VOICE_PASS_FILE):
        return "No voice password set. Say 'set voice password to secret' first."
    for attempt in range(3):
        voice_obj.speak("Say your voice password.")
        pwd = voice_obj.listen()
        if pwd and check_voice_password(pwd):
            return "Voice password correct. System unlocked."
        voice_obj.speak("Incorrect password. Try again.")
    return "Too many failed attempts."
