import os

try:
    import whisper

    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False


def generate_subtitles(video_path: str, output_srt_path: str = None) -> str:
    if not HAS_WHISPER:
        return "Whisper not installed. Run: pip install openai-whisper"

    if output_srt_path is None:
        base = os.path.splitext(video_path)[0]
        output_srt_path = f"{base}.srt"

    model = whisper.load_model("base")
    result = model.transcribe(video_path)

    with open(output_srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"], 1):
            start = _fmt(seg["start"])
            end = _fmt(seg["end"])
            f.write(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n\n")

    return output_srt_path


def _fmt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
