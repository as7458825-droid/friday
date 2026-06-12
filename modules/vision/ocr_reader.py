import os

from PIL import ImageGrab, Image


def read_screen_text() -> str:
    try:
        import pytesseract
    except ImportError:
        return "Tesseract not installed. Run: pip install pytesseract"
    try:
        img = ImageGrab.grab()
        text = pytesseract.image_to_string(img)
        text = text.strip()
        return text[:2000] if text else "No text found on screen."
    except Exception as e:
        return f"OCR error: {e}"


def read_image_text(image_path: str) -> str:
    try:
        import pytesseract
    except ImportError:
        return "Tesseract not installed."
    if not os.path.isfile(image_path):
        return f"File not found: {image_path}"
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        text = text.strip()
        return text[:2000] if text else "No text found in image."
    except Exception as e:
        return f"OCR error: {e}"


def read_selection_text(x: int, y: int, w: int, h: int) -> str:
    try:
        import pytesseract
    except ImportError:
        return "Tesseract not installed."
    try:
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        text = pytesseract.image_to_string(img)
        return text.strip()[:2000] or "No text found in selection."
    except Exception as e:
        return f"OCR error: {e}"
