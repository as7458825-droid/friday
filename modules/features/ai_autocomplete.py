import threading
import time

import keyboard
import pyperclip

_active = False
_thread = None
_last_text = ""

try:
    from modules.llm.llm_manager import query_llm, TaskType

    HAS_LLM = True
except Exception:
    HAS_LLM = False


def start_autocomplete() -> str:
    global _active, _thread
    if _active:
        return "Already running."
    if not HAS_LLM:
        return "LLM not available. Enable real_ai_brain."
    _active = True
    _thread = threading.Thread(target=_autocomplete_loop, daemon=True)
    _thread.start()
    return "AI auto-complete started. Press Alt+Space for suggestions."


def stop_autocomplete() -> str:
    global _active
    _active = False
    return "Auto-complete stopped."


def _autocomplete_loop():
    global _last_text
    while _active:
        try:
            if keyboard.is_pressed("alt+space"):
                time.sleep(0.2)
                clipboard_before = pyperclip.paste()
                keyboard.send("ctrl+c")
                time.sleep(0.1)
                selected = pyperclip.paste()
                if selected and selected != clipboard_before and selected != _last_text:
                    _last_text = selected
                    suggestion = query_llm(
                        f"Complete this text naturally (return only the completion, 1-2 sentences max): {selected}",
                        task_type=TaskType.FAST_CONVERSATION,
                    )
                    if suggestion:
                        suggestion = suggestion.strip().strip("\"'")
                        pyperclip.copy(suggestion)
                        print(f"[AUTO-COMPLETE] Copied: {suggestion[:80]}")
        except Exception:
            pass
        time.sleep(0.3)
