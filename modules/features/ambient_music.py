import os

try:
    import pygame

    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False

_playing = False
_player_thread = None
_current_mood = "calm"
_volume = 0.5

AMBIENT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ambient_sounds")


# Generate simple ambient sounds using numpy
def _generate_tone(freq: float, duration: float, sample_rate: int = 22050) -> None:
    try:
        import numpy as np

        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(freq * t * 2 * np.pi) * 0.3
        wave += np.sin(freq * 1.5 * t * 2 * np.pi) * 0.1
        wave += np.sin(freq * 0.5 * t * 2 * np.pi) * 0.15
        fade = np.linspace(0, 1, int(sample_rate * 0.5))
        fade_out = np.linspace(1, 0, int(sample_rate * 0.5))
        wave[: len(fade)] *= fade
        wave[-len(fade_out) :] *= fade_out
        import struct
        import wave as wav_module

        os.makedirs(AMBIENT_DIR, exist_ok=True)
        fpath = os.path.join(AMBIENT_DIR, f"ambient_{_current_mood}.wav")
        with wav_module.open(fpath, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(
                struct.pack(f"{len(wave)}h", *(int(s * 32767) for s in wave))
            )
        return fpath
    except ImportError:
        return ""


MOOD_FREQS = {
    "calm": 200,
    "focus": 400,
    "relax": 150,
    "energy": 600,
    "sleep": 100,
    "rain": 80,
    "nature": 250,
}


def play(mood: str = "calm") -> str:
    global _playing, _current_mood
    if not HAS_PYGAME:
        return "pygame not installed. Run: pip install pygame"
    if _playing:
        stop()
    _current_mood = mood.lower()
    if _current_mood not in MOOD_FREQS:
        _current_mood = "calm"
    fpath = _generate_tone(MOOD_FREQS[_current_mood], 30.0)
    if not fpath:
        return "Could not generate ambient sound."
    pygame.mixer.init(frequency=22050)
    try:
        pygame.mixer.music.load(fpath)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(_volume)
        _playing = True
        return f"Playing ambient {_current_mood} music."
    except Exception as e:
        return f"Playback error: {e}"


def stop() -> str:
    global _playing
    if _playing and HAS_PYGAME:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    _playing = False
    return "Ambient music stopped."


def set_volume(vol: float) -> str:
    global _volume
    _volume = max(0.0, min(1.0, vol))
    if _playing and HAS_PYGAME:
        try:
            pygame.mixer.music.set_volume(_volume)
        except Exception:
            pass
    return f"Volume set to {int(_volume * 100)}%."


def status() -> str:
    moods = ", ".join(MOOD_FREQS.keys())
    return f"{'Playing' if _playing else 'Stopped'}. Mood: {_current_mood}. Available moods: {moods}."
