from deep_translator import GoogleTranslator

try:
    import pytesseract
    from PIL import ImageGrab

    HAS_OCR = True
except ImportError:
    HAS_OCR = False


def translate_text(text: str, target: str = "en", source: str = "auto") -> str:
    try:
        result = GoogleTranslator(source=source, target=target).translate(text[:2000])
        return result or "Translation failed."
    except Exception as e:
        return f"Translation error: {e}"


def translate_screen(target: str = "en") -> str:
    if not HAS_OCR:
        return "OCR not available. Install pytesseract."
    try:
        img = ImageGrab.grab()
        text = pytesseract.image_to_string(img)
        text = text.strip()
        if not text:
            return "No text found on screen."
        translated = GoogleTranslator(source="auto", target=target).translate(
            text[:2000]
        )
        return f"Original: {text[:100]}... Translated: {translated[:200]}"
    except Exception as e:
        return f"Screen translate error: {e}"


def translate_clipboard(target: str = "en") -> str:
    try:
        import pyperclip

        text = pyperclip.paste()
        if not text:
            return "Clipboard is empty."
        translated = GoogleTranslator(source="auto", target=target).translate(
            text[:2000]
        )
        pyperclip.copy(translated)
        return f"Translated and copied: {translated[:200]}"
    except Exception as e:
        return f"Clipboard translate error: {e}"
