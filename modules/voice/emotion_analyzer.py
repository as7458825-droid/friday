import librosa
import numpy as np


def analyze_emotion(audio_path):
    """Analyze audio for emotional tone based on pitch and energy."""
    try:
        y, sr = librosa.load(audio_path)
        # Pitch (F0)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        avg_pitch = np.mean(pitches[pitches > 0])

        # Energy (RMS)
        rms = librosa.feature.rms(y=y)[0]
        avg_energy = np.mean(rms)

        # Simple heuristic mapping
        if avg_energy > 0.05 and avg_pitch > 200:
            return "excited"
        elif avg_energy < 0.01:
            return "sad/tired"
        elif avg_pitch > 250:
            return "angry/stressed"
        else:
            return "neutral/calm"
    except Exception as e:
        return f"unknown ({e})"


# Note: This will be integrated into the voice listening loop.
