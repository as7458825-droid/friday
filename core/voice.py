import logging
import os
import platform
import speech_recognition as sr
import pyttsx3
import tempfile
from datetime import datetime
from config import FEATURES

log = logging.getLogger("FRIDAY")


class VoiceEngine:
    def __init__(self, female_voice: bool = True, language: str = "en-IN"):
        self._init_com()
        self.language = language
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # ElevenLabs Setup
        self.el_api_key = os.environ.get("ELEVENLABS_API_KEY")
        self.use_el = FEATURES.get("elevenlabs", False) and self.el_api_key

        self.tts_engine = pyttsx3.init()
        self._select_voice(female_voice)
        self.tts_engine.setProperty("rate", 180)

        # Advanced Voice Lab (Whisper + Edge-TTS)
        try:
            from modules.features.voice_lab import AdvancedVoiceLab

            self.adv_lab = AdvancedVoiceLab()
            self.has_adv = True
        except Exception as e:
            log.warning(f"Advanced Voice Lab failed to init: {e}")
            self.has_adv = False

    @staticmethod
    def _init_com():
        if platform.system() != "Windows":
            return
        try:
            import pythoncom

            pythoncom.CoInitialize()
        except ImportError:
            pass

    def _select_voice(self, female: bool) -> None:
        voices = self.tts_engine.getProperty("voices")
        if not voices:
            return
        if female:
            keywords = ("female", "zira", "girl", "woman", "ella", "lisa")
            for v in voices:
                name = (v.name or "").lower()
                if any(k in name for k in keywords):
                    self.tts_engine.setProperty("voice", v.id)
                    return
        self.tts_engine.setProperty("voice", voices[0].id)

    def speak(self, text: str, language: str = None) -> None:
        if not text:
            return
        log.info(f"FRIDAY: {text}")

        # Try Advanced Edge-TTS (Free & High Quality)
        if self.has_adv:
            try:
                from modules.features.voice_lab import run_async

                # Use a sweet female voice by default
                voice_name = (
                    "en-US-AvaNeural"
                    if "hi" not in (language or "")
                    else "hi-IN-SwaraNeural"
                )
                if run_async(self.adv_lab.speak_advanced(text, voice_name)):
                    return
            except Exception as e:
                log.warning(f"Advanced Speak failed: {e}. Falling back.")

        # Try ElevenLabs for "Premium Voice" if enabled
        if self.use_el:
            try:
                from elevenlabs import generate, play, set_api_key

                set_api_key(self.el_api_key)
                # "Rachel" is a very sweet and natural voice
                audio = generate(
                    text=text, voice="Rachel", model="eleven_multilingual_v2"
                )
                play(audio)
                return
            except Exception as e:
                log.warning(f"ElevenLabs failed: {e}. Falling back.")

        lang = language or self.language
        base_lang = lang.split("-")[0] if "-" in lang else lang

        if base_lang == "en":
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return

        try:
            from gtts import gTTS

            tts = gTTS(text=text, lang=base_lang, slow=False)
            tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            tmp.close()
            tts.save(tmp.name)

            from pydub import AudioSegment
            from pydub.playback import play as pydub_play

            audio = AudioSegment.from_mp3(tmp.name)
            pydub_play(audio)
            os.unlink(tmp.name)
        except Exception:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

    def listen(self, language: str = None) -> str | None:
        lang = language or self.language
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening (Advanced Mode Online)...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                return None

        # Try Advanced Whisper Listening
        if self.has_adv:
            try:
                text = self.adv_lab.listen_advanced(audio)
                if text:
                    print(f"FRIDAY (Whisper) heard: {text}")
                    return text
            except Exception as e:
                log.warning(f"Whisper listening failed: {e}")

        # Fallback to Google Recognition
        try:
            text = self.recognizer.recognize_google(audio, language=lang).lower()
            print(f"You said (Google): {text}")
            return text
        except (sr.UnknownValueError, sr.RequestError):
            return None

    def get_greeting(self) -> str:
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning, friend"
        elif hour < 18:
            return "Good afternoon, partner"
        return "Good evening, buddy"
