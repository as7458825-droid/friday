import os
import threading
import time
from datetime import datetime

import cv2

_monitoring = False
_monitor_thread = None
_last_motion = None
_motion_threshold = 5000


def start_monitor(save_path: str = "") -> str:
    global _monitoring, _monitor_thread
    if _monitoring:
        return "Already monitoring."
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "No webcam found."
    cap.release()
    _monitoring = True
    _monitor_thread = threading.Thread(
        target=_monitor_loop, args=(save_path,), daemon=True
    )
    _monitor_thread.start()
    return "Security camera started. I will alert you on motion."


def stop_monitor() -> str:
    global _monitoring
    if not _monitoring:
        return "Not monitoring."
    _monitoring = False
    if _monitor_thread:
        _monitor_thread.join(timeout=3)
    return "Security camera stopped."


def _monitor_loop(save_path: str = ""):
    global _last_motion, _monitoring
    if not save_path:
        save_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "security_footage"
        )
    os.makedirs(save_path, exist_ok=True)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        _monitoring = False
        return
    ret, prev_frame = cap.read()
    if not ret:
        cap.release()
        _monitoring = False
        return
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)
    while _monitoring:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        diff = cv2.absdiff(prev_gray, gray)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for c in contours:
            if cv2.contourArea(c) < _motion_threshold:
                continue
            now = datetime.now()
            _last_motion = now.isoformat()
            fname = f"motion_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
            fpath = os.path.join(save_path, fname)
            cv2.imwrite(fpath, frame)
            print(f"[SECURITY CAM] Motion detected! Saved {fname}")
            break
        prev_gray = gray
        time.sleep(0.5)
    cap.release()


def motion_status() -> str:
    if _last_motion:
        return f"Last motion detected at {_last_motion}."
    return "No motion detected yet."
