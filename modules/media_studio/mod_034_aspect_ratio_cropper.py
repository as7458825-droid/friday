import os
import subprocess

PLATFORM_DIMS = {
    "instagram": (1080, 1920),
    "tiktok": (1080, 1920),
    "youtube": (1920, 1080),
    "twitter": (1280, 720),
    "linkedin": (1080, 1350),
}


def _ffmpeg_available() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False


def crop_for_platform(video_path: str, platform: str = "instagram") -> str:
    if not _ffmpeg_available():
        return "ffmpeg not found."

    dims = PLATFORM_DIMS.get(platform.lower())
    if dims is None:
        return f"Unknown platform: {platform}. Options: {', '.join(PLATFORM_DIMS)}"

    base, ext = os.path.splitext(video_path)
    output_path = f"{base}_{platform}{ext}"

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                video_path,
                "-v",
                f"crop={dims[0]}:{dims[1]}",
                "-y",
                output_path,
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=300,
        )
        return output_path
    except subprocess.TimeoutExpired:
        return "Cropping timed out."
    except subprocess.CalledProcessError as e:
        return f"Cropping failed: {e.stderr[:200]}"
