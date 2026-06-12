import os
import tempfile
import wave

import numpy as np
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3

_analyzer = None


def analyze_stress() -> str:
    try:
        import librosa
    except ImportError:
        return "librosa not installed. Run: pip install librosa"
    p = pyaudio.PyAudio()
    frames = []
    try:
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        stream.stop_stream()
        stream.close()
    finally:
        p.terminate()
    if not frames:
        return "No audio captured."
    temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp.close()
    wf = wave.open(temp.name, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    try:
        y, sr = librosa.load(temp.name, sr=None)
        os.unlink(temp.name)
        features = {}
        features["pitch_mean"] = (
            float(librosa.yin(y, fmin=50, fmax=300).mean()) if len(y) > 0 else 0
        )
        features["energy"] = (
            float(np.mean(librosa.feature.rms(y=y))) if len(y) > 0 else 0
        )
        features["zero_crossings"] = (
            float(np.mean(librosa.feature.zero_crossing_rate(y))) if len(y) > 0 else 0
        )
        features["speech_rate"] = min(features["zero_crossings"] * 100, 100)
        features["pitch_var"] = features["pitch_mean"] * 0.1
        stress_score = 0
        if features["pitch_mean"] > 200:
            stress_score += 30
        if features["energy"] > 0.1:
            stress_score += 25
        if features["zero_crossings"] > 0.1:
            stress_score += 25
        if features["speech_rate"] > 50:
            stress_score += 20
        stress_score = min(stress_score, 100)
        if stress_score < 30:
            level = "calm"
        elif stress_score < 60:
            level = "moderate"
        else:
            level = "stressed"
        return f"Stress analysis: {level} ({stress_score:.0f}%). Pitch: {features['pitch_mean']:.0f} Hz, Energy: {features['energy']:.3f}."
    except Exception as e:
        try:
            os.unlink(temp.name)
        except Exception:
            pass
        return f"Analysis error: {e}"
