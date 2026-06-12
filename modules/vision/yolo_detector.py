import os
import cv2


def detect_objects() -> str:
    try:
        from ultralytics import YOLO
    except ImportError:
        return "YOLO not installed. Run: pip install ultralytics"
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "No webcam found."
    model = YOLO("yolov8n.pt")
    try:
        for _ in range(30):
            ret, frame = cap.read()
            if not ret:
                continue
            results = model(frame, verbose=False)
            if results and results[0].boxes is not None:
                names = results[0].names
                detected = {}
                for box in results[0].boxes:
                    cls = int(box.cls[0])
                    label = names[cls]
                    detected[label] = detected.get(label, 0) + 1
                cap.release()
                if detected:
                    desc = ", ".join(f"{v}x {k}" for k, v in sorted(detected.items()))
                    return f"I see: {desc}."
                return "I see nothing detected."
            break
        cap.release()
        return "No objects detected."
    except Exception as e:
        cap.release()
        return f"Detection error: {e}"


def detect_objects_from_file(image_path: str) -> str:
    try:
        from ultralytics import YOLO
    except ImportError:
        return "YOLO not installed."
    if not os.path.isfile(image_path):
        return f"File not found: {image_path}"
    try:
        model = YOLO("yolov8n.pt")
        results = model(image_path, verbose=False)
        if results and results[0].boxes is not None:
            names = results[0].names
            detected = {}
            for box in results[0].boxes:
                cls = int(box.cls[0])
                label = names[cls]
                detected[label] = detected.get(label, 0) + 1
            if detected:
                return ", ".join(f"{v}x {k}" for k, v in sorted(detected.items()))
        return "No objects detected."
    except Exception as e:
        return f"Detection error: {e}"
