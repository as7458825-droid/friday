import os
import subprocess


def _ffmpeg_available() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False


def video_to_gif(video_path: str, output_path: str = None, fps: int = 10) -> str:
    if not _ffmpeg_available():
        return "ffmpeg not found."

    if output_path is None:
        base = os.path.splitext(video_path)[0]
        output_path = f"{base}.gi"

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-v",
                f"fps={fps},scale=480:-1:flags=lanczos",
                "-y",
                output_path,
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        return output_path
    except subprocess.TimeoutExpired:
        return "Conversion timed out."
    except subprocess.CalledProcessError as e:
        return f"GIF conversion failed: {e.stderr[:200]}"
