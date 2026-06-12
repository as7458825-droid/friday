import threading
import time

import cv2
import numpy as np
from PIL import ImageGrab

_active = False
_thread = None
_overlay_data = []


def start_overlay() -> str:
    global _active, _thread
    if _active:
        return "Already running."
    _active = True
    _thread = threading.Thread(target=_overlay_loop, daemon=True)
    _thread.start()
    return "Desktop AR started. Objects will be highlighted."


def stop_overlay() -> str:
    global _active
    _active = False
    return "Desktop AR stopped."


def _overlay_loop():
    try:
        from ultralytics import YOLO

        model = YOLO("yolov8n.pt")
    except Exception:
        global _active
        _active = False
        return
    while _active:
        try:
            img = ImageGrab.grab()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = model(frame, verbose=False)
            if results and results[0].boxes is not None:
                annot = results[0].plot()
                cv2.imshow("FRIDAY AR Overlay", annot)
                cv2.setWindowProperty("FRIDAY AR Overlay", cv2.WND_PROP_TOPMOST, 1)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        except Exception:
            pass
        time.sleep(0.5)
    cv2.destroyAllWindows()


def highlight_objects(class_names: list = None) -> str:
    try:
        from ultralytics import YOLO
    except Exception:
        return "YOLO not installed."
    img = ImageGrab.grab()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    model = YOLO("yolov8n.pt")
    results = model(frame, verbose=False)
    if results and results[0].boxes is not None:
        names = results[0].names
        detected = []
        for box in results[0].boxes:
            cls = int(box.cls[0])
            label = names[cls]
            if not class_names or label in class_names:
                detected.append(label)
        if detected:
            annot = results[0].plot()
            cv2.imshow("FRIDAY Detection", annot)
            cv2.setWindowProperty("FRIDAY Detection", cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
            return f"Found: {', '.join(set(detected))}"
        return "No matching objects found."
    return "No objects detected."
