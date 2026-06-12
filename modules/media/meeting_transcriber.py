import os
import threading
import tempfile
import wave
from datetime import datetime

import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

_listening = False
_transcriber_thread = None
_audio_frames = []


def start_transcribing() -> str:
    global _listening, _transcriber_thread, _audio_frames
    if _listening:
        return "Already transcribing."
    import importlib.util

    if importlib.util.find_spec("whisper") is None:
        return "Whisper not installed. Run: pip install openai-whisper"
    _listening = True
    _audio_frames = []
    _transcriber_thread = threading.Thread(target=_record_audio, daemon=True)
    _transcriber_thread.start()
    return "Listening... I will transcribe what I hear."


def stop_transcribing() -> str:
    global _listening
    if not _listening:
        return "Not transcribing."
    _listening = False
    if _transcriber_thread:
        _transcriber_thread.join(timeout=5)
    if not _audio_frames:
        return "No audio captured."
    try:
        import whisper

        model = whisper.load_model("base")
        temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp.close()
        wf = wave.open(temp.name, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(_audio_frames))
        wf.close()
        result = model.transcribe(temp.name)
        text = result["text"].strip()
        os.unlink(temp.name)
        transcripts_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", "transcripts"
        )
        if not os.path.isdir(transcripts_dir):
            os.makedirs(transcripts_dir, exist_ok=True)
        fname = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(os.path.join(transcripts_dir, fname), "w", encoding="utf-8") as f:
            f.write(text)
        return f"Transcription saved: {text[:500]}" if text else "No speech detected."
    except Exception as e:
        return f"Transcription error: {e}"


def _record_audio():
    global _audio_frames
    p = pyaudio.PyAudio()
    try:
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        while _listening:
            data = stream.read(CHUNK, exception_on_overflow=False)
            _audio_frames.append(data)
        stream.stop_stream()
        stream.close()
    finally:
        p.terminate()
