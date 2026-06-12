import threading
import time

import cv2

_active = False
_thread = None


def start_gesture_control() -> str:
    global _active, _thread
    if _active:
        return "Gesture control already running."
    _active = True
    _thread = threading.Thread(target=_gesture_loop, daemon=True)
    _thread.start()
    return "Gesture control started. Wave to control volume, peace sign to play/pause."


def stop_gesture_control() -> str:
    global _active
    if not _active:
        return "Not running."
    _active = False
    if _thread:
        _thread.join(timeout=3)
    return "Gesture control stopped."


def _gesture_loop():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        global _active
        _active = False
        return
    try:
        import pyautogui
    except ImportError:
        cap.release()
        _active = False
        return
    cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    prev_gesture = ""
    cooldown = 0
    while _active:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (35, 35), 0)
        _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if cooldown > 0:
            cooldown -= 1
        if contours and cooldown == 0:
            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)
            if area > 30000:
                hull = cv2.convexHull(largest)
                hull_area = cv2.contourArea(hull)
                if hull_area > 0:
                    solidity = float(area) / hull_area
                    if solidity < 0.7:
                        gesture = "wave"
                        pyautogui.press("volumedown")
                    else:
                        gesture = "fist"
                        pyautogui.press("playpause")
                    if gesture != prev_gesture:
                        prev_gesture = gesture
                        cooldown = 10
        time.sleep(0.1)
    cap.release()
