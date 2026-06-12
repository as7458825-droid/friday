import re

try:
    import pytesseract
    from PIL import ImageGrab

    HAS_OCR = True
except Exception:
    HAS_OCR = False


def read_game_region(x: int = 0, y: int = 0, w: int = 300, h: int = 100) -> str:
    if not HAS_OCR:
        return "OCR not available."
    try:
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        text = pytesseract.image_to_string(img).strip()
        return text or "No text found."
    except Exception as e:
        return f"OCR error: {e}"


def read_health() -> str:
    text = read_game_region(50, 50, 200, 50)
    if text:
        nums = re.findall(r"\d+", text)
        if nums:
            return f"Health: {nums[0]}"
    return "Could not read health."


def read_ammo() -> str:
    text = read_game_region(50, 500, 200, 50)
    if text:
        nums = re.findall(r"\d+", text)
        if nums:
            return f"Ammo: {nums[0]}/{nums[1] if len(nums) > 1 else '?'}"
    return "Could not read ammo."


def get_tips(game_name: str = "") -> str:
    try:
        from modules.llm.llm_manager import query_llm, TaskType

        prompt = f"Give 3 quick gaming tips for {game_name or 'any popular game'} (2 lines each):"
        result = query_llm(prompt, task_type=TaskType.FAST_CONVERSATION)
        return result[:500] if result else "No tips available."
    except Exception:
        return "LLM not available."


def auto_grind(keys: list) -> str:
    try:
        import pyautogui
        import time

        def _grind():
            for _ in range(100):
                for key in keys:
                    pyautogui.press(key)
                    time.sleep(0.05)

        import threading

        threading.Thread(target=_grind, daemon=True).start()
        return f"Auto-grinding with {keys}..."
    except Exception:
        return "Auto-grind requires pyautogui."
