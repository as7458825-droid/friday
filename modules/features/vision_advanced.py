import os
import tempfile
import cv2


def detect_pose() -> str:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Camera not available."
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return "No frame captured."
    path = os.path.join(tempfile.gettempdir(), "pose.jpg")
    cv2.imwrite(path, frame)
    return "Photo saved. Use YOLO for pose detection."


def read_barcode() -> str:
    try:
        from pyzbar.pyzbar import decode
    except Exception:
        return "pyzbar not installed. Run: pip install pyzbar"
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return "Camera not available."
    barcodes = decode(frame)
    if barcodes:
        return " | ".join(b.data.decode() for b in barcodes)
    return "No barcode detected."


def read_qr() -> str:
    try:
        from pyzbar.pyzbar import decode
    except Exception:
        return "pyzbar not installed."
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return "Camera not available."
    qrs = decode(frame)
    if qrs:
        return " | ".join(q.data.decode() for q in qrs)
    return "No QR code detected."


def read_license_plate(image_path: str = "") -> str:
    try:
        import pytesseract
    except Exception:
        return "pytesseract not installed."
    if not image_path:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return "Camera not available."
        image_path = os.path.join(tempfile.gettempdir(), "plate.jpg")
        cv2.imwrite(image_path, frame)
    text = pytesseract.image_to_string(cv2.imread(image_path))
    import re

    plates = re.findall(r"[A-Z]{2}\s*\d{1,2}\s*[A-Z]{1,2}\s*\d{4}", text)
    return f"Plates: {plates}" if plates else "No license plate text found."
