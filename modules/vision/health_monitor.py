import threading
import time

import cv2
import numpy as np

_monitoring = False
_monitor_thread = None
_last_hr = 0
_last_hrv = 0


def start_monitor() -> str:
    global _monitoring, _monitor_thread
    if _monitoring:
        return "Already monitoring."
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "No webcam found."
    cap.release()
    _monitoring = True
    _monitor_thread = threading.Thread(target=_monitor_loop, daemon=True)
    _monitor_thread.start()
    return "Health monitoring started. Looking at your face..."


def stop_monitor() -> str:
    global _monitoring
    _monitoring = False
    return "Health monitoring stopped."


def _monitor_loop():
    global _last_hr, _last_hrv
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        _monitoring = False
        return
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    fps = 15
    signals = []
    while _monitoring:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for x, y, w, h in faces:
            roi = frame[y : y + h, x : x + w]
            avg_color = roi.mean(axis=(0, 1))
            green_val = avg_color[1]
            signals.append(green_val)
            if len(signals) > 150:
                signals.pop(0)
            if len(signals) >= 30:
                sig = np.array(signals)
                sig = sig - sig.mean()
                fft = np.fft.rfft(sig)
                freqs = np.fft.rfftfreq(len(sig), d=1.0 / fps)
                mask = (freqs >= 0.8) & (freqs <= 3.0)
                if mask.any():
                    peak_freq = freqs[mask][np.argmax(np.abs(fft[mask]))]
                    hr = int(peak_freq * 60)
                    if 40 <= hr <= 200:
                        _last_hr = hr
                        _last_hrv = int(np.std(sig[-30:]) * 10)
            break
        time.sleep(1.0 / fps)
    cap.release()


def get_health() -> str:
    if not _last_hr:
        return "No data yet. Keep facing the camera."
    status = (
        "normal" if 60 <= _last_hr <= 100 else "elevated" if _last_hr > 100 else "low"
    )
    return f"Heart rate: {_last_hr} BPM ({status}). HRV: {_last_hrv}."


def status() -> str:
    return f"{'Monitoring' if _monitoring else 'Stopped'}. Last HR: {_last_hr} BPM."
