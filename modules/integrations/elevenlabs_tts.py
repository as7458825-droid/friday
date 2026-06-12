import logging
import os
import tempfile

log = logging.getLogger("FRIDAY")

API_KEY = os.getenv("ELEVENLABS_API_KEY", "")


def text_to_speech(
    text: str, voice: str = "Rachel", output_file: str | None = None
) -> str | None:
    if not API_KEY:
        return None
    try:
        VOICE_IDS = {
            "rachel": "21m00Tcm4TlvDq8ikWAM",
            "domi": "AZnzlk1XvdvUeBnXmlld",
            "bella": "EXAVITQu4vrRVnWHkR6N",
            "antoni": "ErXwobaYiN019PkySvjV",
            "elli": "MF3mGyEYCl7XYWbV9V6O",
            "josh": "TxGEqnHWrfWFTfGW9XjX",
            "arnold": "VR6AewLTigWG4xSOGBnG",
            "adam": "pNInz6obpgDQGcFmaJgB",
            "sam": "yoZ06aMxZJJ28mfd3POQ",
        }
        voice_id = VOICE_IDS.get(voice.lower(), "21m00Tcm4TlvDq8ikWAM")
        import requests

        resp = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": API_KEY,
            },
            json={
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
            },
            timeout=30,
        )
        resp.raise_for_status()
        if output_file:
            with open(output_file, "wb") as f:
                f.write(resp.content)
            return output_file
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp.write(resp.content)
        tmp.close()
        return tmp.name
    except Exception as e:
        log.error("ElevenLabs TTS error: %s", e)
        return None


def get_voices() -> list[str]:
    return [
        "Rachel",
        "Domi",
        "Bella",
        "Antoni",
        "Elli",
        "Josh",
        "Arnold",
        "Adam",
        "Sam",
    ]


def set_voice(voice_name: str) -> str:
    voices = [v.lower() for v in get_voices()]
    if voice_name.lower() in voices:
        return f"ElevenLabs voice set to {voice_name}."
    return f"Voice not found. Available: {', '.join(get_voices())}"
