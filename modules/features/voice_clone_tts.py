import os
import re

try:
    from elevenlabs import generate, play, set_api_key, voices

    _key = os.getenv("ELEVENLABS_API_KEY", "")
    HAS_ELEVEN = bool(_key)
    if _key:
        set_api_key(_key)
except Exception:
    HAS_ELEVEN = False

EMOTION_MAP = {
    "happy": {"stability": 0.3, "similarity": 0.7, "style": 0.5},
    "sad": {"stability": 0.7, "similarity": 0.8, "style": 0.2},
    "angry": {"stability": 0.1, "similarity": 0.5, "style": 0.8},
    "calm": {"stability": 0.8, "similarity": 0.7, "style": 0.3},
    "excited": {"stability": 0.2, "similarity": 0.6, "style": 0.9},
    "sarcastic": {"stability": 0.4, "similarity": 0.7, "style": 0.7},
    "professional": {"stability": 0.8, "similarity": 0.8, "style": 0.3},
}

_voice_id = ""
_current_emotion = "calm"


def set_voice(name: str = "Rachel") -> str:
    global _voice_id
    if not HAS_ELEVEN:
        return "ElevenLabs not configured."
    try:
        all_voices = voices()
        for v in all_voices:
            if name.lower() in v.name.lower():
                _voice_id = v.voice_id
                return f"Voice set to {v.name}."
        return f"Voice '{name}' not found. Available: {', '.join(v.name for v in all_voices[:5])}"
    except Exception as e:
        return f"Voice error: {e}"


def speak(text: str, emotion: str = "") -> str:
    if not HAS_ELEVEN:
        return "ElevenLabs not configured. Add ELEVENLABS_API_KEY to .env"
    if not _voice_id:
        result = set_voice()
        if "error" in result and "not found" in result:
            return result
    if emotion:
        e = emotion.lower()
    else:
        e = _detect_emotion(text)
    params = EMOTION_MAP.get(e, EMOTION_MAP["calm"])
    try:
        audio = generate(
            text=text[:500],
            voice=_voice_id,
            model="eleven_turbo_v2",
            stability=params["stability"],
            similarity_boost=params["similarity"],
            style=params["style"],
        )
        play(audio)
        return f"Speaking in {e} tone."
    except Exception as e:
        return f"TTS error: {e}"


def _detect_emotion(text: str) -> str:
    happy = re.search(
        r"(great|awesome|amazing|fantastic|wonderful|love|excellent|perfect|yay|woohoo|🎉|😊)",
        text,
        re.IGNORECASE,
    )
    sad = re.search(
        r"(sorry|unfortunately|bad|sad|cry|miss|fail|error|😢|😞)", text, re.IGNORECASE
    )
    angry = re.search(
        r"(angry|furious|annoyed|damn|stupid|idiot|💢|😠)", text, re.IGNORECASE
    )
    excited = re.search(
        r"(wow|omg|incredible|unbelievable|exciting|amazing|🎉|🔥|⚡)",
        text,
        re.IGNORECASE,
    )
    sarcastic = re.search(
        r"(obviously|sure|right|whatever|nice|great.*job)", text, re.IGNORECASE
    )

    if excited:
        return "excited"
    if happy:
        return "happy"
    if angry:
        return "angry"
    if sad:
        return "sad"
    if sarcastic:
        return "sarcastic"
    return "professional" if len(text) > 100 else "calm"


def list_emotions() -> str:
    return "Emotions: " + ", ".join(EMOTION_MAP.keys())


def clone_voice(audio_path: str = "") -> str:
    try:
        from elevenlabs import clone

        if not audio_path or not os.path.isfile(audio_path):
            return "Provide path to an audio file (30s+ of speech)."
        voice = clone(
            name="FRIDAY Clone",
            files=[audio_path],
        )
        global _voice_id
        _voice_id = voice.voice_id
        return "Voice cloned! FRIDAY will now speak in that voice."
    except Exception as e:
        return f"Voice clone error: {e}. Requires ElevenLabs API key with voice clone access."


def status() -> str:
    em = _current_emotion
    return f"ElevenLabs: {'connected' if HAS_ELEVEN else 'not configured'}. Voice: {_voice_id or 'default'}. Emotion: {em}."
