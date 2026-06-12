import os
import subprocess
import tempfile


def download(url: str, quality: str = "best") -> str:
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-",
                quality,
                "-o",
                f"{tempfile.gettempdir()}/%(title)s.%(ext)s",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.stdout[-200:] or "Download started."
    except FileNotFoundError:
        return "yt-dlp not installed."
    except Exception as e:
        return f"Error: {e}"


def download_audio(url: str) -> str:
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-x",
                "--audio-format",
                "mp3",
                "-o",
                f"{tempfile.gettempdir()}/%(title)s.%(ext)s",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.stdout[-200:] or "Audio download started."
    except Exception:
        return "yt-dlp not installed."


def get_transcript(url: str) -> str:
    try:
        subprocess.run(
            [
                "yt-dlp",
                "--write-auto-subs",
                "--sub-lang",
                "en",
                "--skip-download",
                "-o",
                f"{tempfile.gettempdir()}/%(id)s",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        vtt = [f for f in os.listdir(tempfile.gettempdir()) if f.endswith(".vtt")]
        if vtt:
            vtt.sort(
                key=lambda x: os.path.getmtime(os.path.join(tempfile.gettempdir(), x)),
                reverse=True,
            )
            with open(os.path.join(tempfile.gettempdir(), vtt[0])) as f:
                return f.read()[:500]
        return "No transcript found."
    except Exception:
        return "yt-dlp not installed."


def search(query: str) -> str:
    try:
        result = subprocess.run(
            ["yt-dlp", f"ytsearch5:{query}", "--print", "%(title)s | %(id)s"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout or "No results."
    except Exception:
        return "yt-dlp not installed."
