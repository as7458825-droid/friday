import os

from PIL import Image


def scrub_metadata(file_path: str) -> str:
    if not os.path.isfile(file_path):
        return f"File not found: {file_path}"

    ext = os.path.splitext(file_path)[1].lower()
    base, ext_orig = os.path.splitext(file_path)
    output_path = f"{base}_clean{ext_orig}"

    if ext in (".jpg", ".jpeg", ".png", ".bmp", ".tif"):
        img = Image.open(file_path)
        data = list(img.getdata())
        clean = Image.new(img.mode, img.size)
        clean.putdata(data)
        clean.save(output_path, exif=b"")
        return output_path

    if ext in (".mp4", ".avi", ".mkv", ".mov"):
        import subprocess

        try:
            subprocess.run(
                ["ffmpeg", "-i", file_path, "-map_metadata", "-1", "-y", output_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=120,
            )
            return output_path
        except subprocess.TimeoutExpired:
            return "Metadata scrubbing timed out."
        except subprocess.CalledProcessError as e:
            return f"Metadata scrubbing failed: {e.stderr[:200]}"
        except FileNotFoundError:
            return "ffmpeg not found."

    return f"Unsupported file type: {ext}"
