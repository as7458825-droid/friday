import os

import cv2

KNOWN_FACES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "known_faces"
)
_capture_active = False
_capture_thread = None


def _ensure_dir():
    if not os.path.isdir(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR, exist_ok=True)


def register_face(name: str) -> str:
    _ensure_dir()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "No webcam found."
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    captured = False
    for _ in range(60):
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_img = frame[y : y + h, x : x + w]
            fpath = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
            cv2.imwrite(fpath, face_img)
            captured = True
            break
    cap.release()
    if captured:
        return f"Face registered for {name}."
    return "No face detected. Ensure good lighting."


def recognize_face() -> str:
    _ensure_dir()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "No webcam found."
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    recognizer = (
        cv2.face.LBPHFaceRecognizer_create()
        if hasattr(cv2.face, "LBPHFaceRecognizer_create")
        else None
    )
    known_images = []
    known_names = []
    if not os.path.isdir(KNOWN_FACES_DIR):
        cap.release()
        return "No known faces registered. Register a face first."
    for fname in os.listdir(KNOWN_FACES_DIR):
        if fname.endswith(".jpg"):
            img = cv2.imread(os.path.join(KNOWN_FACES_DIR, fname), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                known_images.append(img)
                known_names.append(fname[:-4])
    if not known_images:
        cap.release()
        return "No known faces registered."
    for _ in range(30):
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for x, y, w, h in faces:
            face_roi = gray[y : y + h, x : x + w]
            face_roi = cv2.resize(face_roi, (200, 200))
            if recognizer:
                best_match = "Unknown"
                best_conf = 999
                for i, known in enumerate(known_images):
                    cv2.resize(known, (200, 200))
                    try:
                        label, conf = recognizer.predict(face_roi)
                    except Exception:
                        conf = 999
                    if conf < best_conf:
                        best_conf = conf
                        best_match = known_names[i] if conf < 80 else "Unknown"
                cap.release()
                return f"I see {best_match}."
            else:
                cap.release()
                return "Face detected but recognition requires opencv-contrib-python."
    cap.release()
    return "No face detected."


def detect_faces() -> str:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return "No webcam found."
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    for _ in range(30):
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        cap.release()
        count = len(faces)
        if count == 0:
            return "No faces detected."
        if count == 1:
            return "I see 1 face."
        return f"I see {count} faces."
    cap.release()
    return "No faces detected."
