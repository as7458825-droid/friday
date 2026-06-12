import threading
import time
import logging
from modules.vision.face_recognition import recognize_face
from modules.features.power_manager import lock

log = logging.getLogger("FRIDAY.Security")


class SentinelShield:
    _instance = None
    _running = False
    _thread = None
    _user_name = "Master"  # Default

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SentinelShield, cls).__new__(cls)
        return cls._instance

    def start(self, user_name="Master"):
        if self._running:
            return "Sentinel Shield pehle se hi active hai."

        self._user_name = user_name
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        return (
            f"Sentinel Shield active! Ab main aapke PC ki raksha karungi, {user_name}."
        )

    def stop(self):
        self._running = False
        return "Sentinel Shield deactivated."

    def _monitor_loop(self):
        log.info("Sentinel Shield monitoring started.")
        while self._running:
            try:
                # Every 30 seconds, check if the face matches
                time.sleep(30)

                result = recognize_face()
                log.info(f"Security check: {result}")

                if (
                    "Unknown" in result
                    or "No face" not in result
                    and self._user_name not in result
                ):
                    log.warning(f"UNAUTHORIZED ACCESS DETECTED: {result}")
                    lock()
                    self._running = False  # Stop monitoring after lock to prevent loops
                    break
            except Exception as e:
                log.error(f"Sentinel error: {e}")
                time.sleep(10)


def toggle_sentinel(enable=True, name="Master"):
    shield = SentinelShield()
    if enable:
        return shield.start(name)
    else:
        return shield.stop()
