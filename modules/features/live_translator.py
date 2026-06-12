import os
import tempfile
import threading
import wave

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    pyaudio = None
    HAS_PYAUDIO = False

_translating = False
_thread = None
_source_lang = "auto"
_target_lang = "en"

CHUNK = 1024
try:
    FORMAT = pyaudio.paInt16
except NameError:
    FORMAT = 8
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 4


def start(source: str = "auto", target: str = "en") -> str:
    global _translating, _thread, _source_lang, _target_lang
    if _translating:
        return "Already translating."
    if not HAS_PYAUDIO:
        return "pyaudio not installed. Run: pip install pyaudio"
    import importlib.util

    if importlib.util.find_spec("whisper") is None:
        return "whisper not installed."
    _translating = True
    _source_lang = source
    _target_lang = target
    _thread = threading.Thread(target=_translate_loop, daemon=True)
    _thread.start()
    return f"Live translation started: {source} -> {target}. Speak now."


def stop() -> str:
    global _translating
    _translating = False
    return "Translation stopped."


def _translate_loop():
    import whisper

    model = whisper.load_model("base")
    from deep_translator import GoogleTranslator

    p = pyaudio.PyAudio()
    try:
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        while _translating:
            frames = []
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            if not frames:
                continue
            temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp.close()
            wf = wave.open(temp.name, "wb")
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))
            wf.close()
            try:
                result = model.transcribe(
                    temp.name, language=_source_lang if _source_lang != "auto" else None
                )
                text = result["text"].strip()
                if text:
                    translated = GoogleTranslator(
                        source="auto", target=_target_lang
                    ).translate(text[:1000])
                    print(f"[TRANSLATE] {text} -> {translated}")
            except Exception:
                pass
            try:
                os.unlink(temp.name)
            except Exception:
                pass
        stream.stop_stream()
        stream.close()
    finally:
        p.terminate()


def translate_once(text: str, target: str = "en") -> str:
    from deep_translator import GoogleTranslator

    try:
        return GoogleTranslator(source="auto", target=target).translate(text[:2000])
    except Exception as e:
        return f"Translation error: {e}"
