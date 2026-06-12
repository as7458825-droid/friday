import subprocess
import threading
import time

import cv2

_face_lock_active = False
_lock_thread = None
_last_face_time = time.time()
_face_timeout = 30


def start_face_lock(timeout_seconds: int = 30) -> str:
    global _face_lock_active, _lock_thread, _face_timeout
    _face_lock_active = True
    _face_timeout = timeout_seconds
    _lock_thread = threading.Thread(target=_face_loop, daemon=True)
    _lock_thread.start()
    return f"Face lock started. Timeout: {timeout_seconds}s"


def stop_face_lock() -> str:
    global _face_lock_active
    _face_lock_active = False
    return "Face lock stopped."


def _face_loop():
    global _last_face_time
    try:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
    except Exception:
        return
    cap = cv2.VideoCapture(0)
    while _face_lock_active:
        try:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) > 0:
                    _last_face_time = time.time()
            if time.time() - _last_face_time > _face_timeout:
                subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
                _last_face_time = time.time()
        except Exception:
            pass
        time.sleep(2)
    cap.release()


def screen_lock_timer(minutes: int = 5) -> str:
    def lock():
        time.sleep(minutes * 60)
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])

    threading.Thread(target=lock, daemon=True).start()
    return f"Screen will lock in {minutes} minutes."


def password_audit() -> str:
    try:
        subprocess.run(
            [
                "cmd",
                "/c",
                "dir",
                "C:\\Users\\*\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data",
                "/s",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return "Chrome password store found. Use a password manager like Bitwarden."
    except Exception:
        return "Password audit unavailable."


def encrypt_notes(text: str) -> str:
    try:
        from cryptography.fernet import Fernet
    except Exception:
        return "cryptography not installed."
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(text.encode()).decode()
    return f"Encrypted: {encrypted[:50]}... Key: {key.decode()[:20]}... (save this key)"
