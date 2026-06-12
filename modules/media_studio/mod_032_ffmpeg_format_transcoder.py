import os
import subprocess


def _ffmpeg_available() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False


def convert_format(input_path: str, output_format: str) -> str:
    if not _ffmpeg_available():
        return "ffmpeg not found. Install ffmpeg: winget install ffmpeg"

    base = os.path.splitext(input_path)[0]
    output_path = f"{base}.{output_format.lstrip('.')}"

    try:
        subprocess.run(
            ["ffmpeg", "-i", input_path, "-y", output_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=300,
        )
        return output_path
    except subprocess.TimeoutExpired:
        return "Conversion timed out."
    except subprocess.CalledProcessError as e:
        return f"Conversion failed: {e.stderr[:200]}"
