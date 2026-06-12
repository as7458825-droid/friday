import os
import queue
import threading
import time

try:
    import keyboard
    HAS_KEYBOARD = True
except ImportError:
    keyboard = None
    HAS_KEYBOARD = False
try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    pyautogui = None
    HAS_PYAUTOGUI = False
import pyperclip

_active = False
_dictating = False
_audio_queue = queue.Queue()
_hotkey = "ctrl+alt+v"

HOTKEY_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "voice_os_config.json"
)


def _save_config(key: str):
    d = os.path.dirname(HOTKEY_FILE)
    if not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    import json

    with open(HOTKEY_FILE, "w") as f:
        json.dump({"hotkey": key}, f)


def _load_config() -> str:
    import json

    if os.path.isfile(HOTKEY_FILE):
        return json.load(f).get("hotkey", "ctrl+alt+v")
    return "ctrl+alt+v"


def start() -> str:
    global _active, _hotkey
    if not HAS_KEYBOARD:
        return "keyboard library not installed. Run: pip install keyboard"
    if not HAS_PYAUTOGUI:
        return "pyautogui library not installed. Run: pip install pyautogui"
    _hotkey = _load_config()
    _active = True
    try:
        keyboard.add_hotkey(_hotkey, _on_hotkey)
    except Exception:
        return f"Could not register hotkey {_hotkey}."
    threading.Thread(target=_listen_loop, daemon=True).start()
    return f"Voice OS started. Press {_hotkey} to dictate anywhere."


def stop() -> str:
    global _active
    _active = False
    try:
        keyboard.remove_hotkey(_hotkey)
    except Exception:
        pass
    return "Voice OS stopped."


def set_hotkey(key: str) -> str:
    global _hotkey
    old = _hotkey
    try:
        keyboard.remove_hotkey(old)
    except Exception:
        pass
    _hotkey = key
    if _active:
        try:
            keyboard.add_hotkey(key, _on_hotkey)
        except Exception:
            return f"Invalid hotkey: {key}"
    _save_config(key)
    return f"Hotkey changed to {key}"


def _on_hotkey():
    global _dictating
    if _dictating:
        return
    _dictating = True
    try:
        import pyaudio
        import wave
        import speech_recognition as sr
    except Exception:
        _type_text("Speech recognition not available.")
        _dictating = False
        return

    chunk = 1024
    format_p = pyaudio.paInt16
    channels = 1
    rate = 16000
    record_seconds = 5

    p = pyaudio.PyAudio()
    stream = p.open(
        format=format_p,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
    )

    frames = []
    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    import tempfile

    wf_path = os.path.join(tempfile.gettempdir(), "voice_os_input.wav")
    wf = wave.open(wf_path, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format_p))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()

    r = sr.Recognizer()
    with sr.AudioFile(wf_path) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        _type_text(text)
    except sr.UnknownValueError:
        _type_text("[Could not understand]")
    except sr.RequestError:
        _type_text("[Speech service error]")

    _dictating = False


def _type_text(text: str):
    if not HAS_PYAUTOGUI:
        return
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.1)


def _listen_loop():
    while _active:
        time.sleep(0.5)


def status() -> str:
    return f"Voice OS: {'active' if _active else 'stopped'}. Hotkey: {_hotkey}"


def mode_command() -> str:
    return "Voice OS mode active. Press hotkey to dictate anywhere."
