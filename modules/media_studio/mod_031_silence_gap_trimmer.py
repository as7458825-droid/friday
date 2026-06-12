import os

try:
    from pydub import AudioSegment

    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False


def trim_silence(
    audio_path: str, output_path: str = None, threshold_db: int = -40
) -> str:
    if not HAS_PYDUB:
        return "pydub not installed. Run: pip install pydub"

    if output_path is None:
        base, ext = os.path.splitext(audio_path)
        output_path = f"{base}_trimmed{ext}"

    audio = AudioSegment.from_file(audio_path)
    non_silent = audio.strip_silence(
        silence_len=200, silence_thresh=threshold_db, padding=100
    )
    non_silent.export(output_path, format=os.path.splitext(output_path)[1][1:])
    return output_path
