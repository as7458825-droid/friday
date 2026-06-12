import numpy as np

try:
    import librosa

    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False

try:
    import soundfile as sf

    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False


def extract_vocals(music_path: str, output_path: str = "vocals.wav") -> str:
    if not HAS_LIBROSA or not HAS_SOUNDFILE:
        return "Install librosa and soundfile: pip install librosa soundfile"

    y, sr = librosa.load(music_path, sr=None)
    S_full, phase = librosa.magphase(librosa.stft(y))
    S_filter = librosa.decompose.nn_filter(
        S_full, aggregate=np.median, metric="cosine", width=3
    )
    S_filter = np.minimum(S_full, S_filter)
    margin_v = 10
    mask_v = librosa.util.softmask(S_full - S_filter, margin_v * S_filter, power=2)
    y_vocals = librosa.istft(mask_v * phase)

    sf.write(output_path, y_vocals, sr)
    return output_path
