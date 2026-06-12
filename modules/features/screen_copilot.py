import threading
import time
from datetime import datetime

try:
    import pytesseract
    from PIL import ImageGrab

    HAS_OCR = True
except Exception:
    HAS_OCR = False

try:
    from modules.llm.llm_manager import query_llm, TaskType

    HAS_LLM = True
except Exception:
    HAS_LLM = False

_watching = False
_watch_thread = None
_last_context = ""
_suggestion_log = []
_last_suggestions = {}


def start() -> str:
    global _watching, _watch_thread
    if _watching:
        return "Already watching."
    if not HAS_OCR:
        return "OCR not available (pytesseract)."
    _watching = True
    _watch_thread = threading.Thread(target=_watch_loop, daemon=True)
    _watch_thread.start()
    return "Screen Co-Pilot started. I'll offer help when I see something."


def stop() -> str:
    global _watching
    _watching = False
    return "Screen Co-Pilot stopped."


def _watch_loop():
    global _last_context, _last_suggestions
    import pygetwindow as gw

    last_window = ""
    while _watching:
        try:
            active = gw.getActiveWindow()
            if active:
                title = active.title
            else:
                title = ""
            if title != last_window:
                last_window = title
                if HAS_LLM:
                    suggestion = query_llm(
                        f"You are a co-pilot. The user is using: '{title}'. "
                        "Suggest ONE helpful tip or shortcut (1 sentence, no greetings):",
                        task_type=TaskType.FAST_CONVERSATION,
                    )
                    if suggestion and len(suggestion) > 5:
                        _last_suggestions[title] = suggestion
                        _show_suggestion(suggestion)
            time.sleep(5)
        except Exception:
            time.sleep(10)


def _show_suggestion(text: str):
    try:
        from plyer import notification

        notification.notify(
            title="FRIDAY Co-Pilot",
            message=text[:200],
            timeout=6,
        )
    except Exception:
        pass
    _suggestion_log.append({"time": datetime.now().isoformat(), "text": text})
    print(f"[CO-PILOT] {text}")


def analyze_screen() -> str:
    if not HAS_OCR:
        return "OCR not available."
    img = ImageGrab.grab()
    text = pytesseract.image_to_string(img).strip()[:500]
    if not text:
        return "No text found on screen."
    if HAS_LLM:
        analysis = query_llm(
            f"What is the user doing based on this screen text? Answer in 1 sentence:\n{text}",
            task_type=TaskType.FAST_CONVERSATION,
        )
        return analysis[:200] if analysis else text[:200]
    return text[:200]


def get_suggestions() -> str:
    if not _last_suggestions:
        return "No suggestions yet."
    return " | ".join(
        f"{app}: {tip}" for app, tip in list(_last_suggestions.items())[:3]
    )


def status() -> str:
    return f"{'Watching' if _watching else 'Stopped'}. {len(_suggestion_log)} suggestions given."
