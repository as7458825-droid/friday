try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    whisper = None
    HAS_WHISPER = False
try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    edge_tts = None
    HAS_EDGE_TTS = False
import asyncio
import os
import tempfile
try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    pygame = None
    HAS_PYGAME = False
import logging
try:
    import torch
    HAS_TORCH = True
except ImportError:
    torch = None
    HAS_TORCH = False
try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    sr = None
    HAS_SR = False

logger = logging.getLogger(__name__)


class AdvancedVoiceLab:
    """Advanced AI Voice & Listening Module for FRIDAY"""

    def __init__(self):
        device = "cuda" if HAS_TORCH and torch.cuda.is_available() else "cpu"
        self.whisper_model = whisper.load_model("tiny", device=device) if HAS_WHISPER else None
        self.recognizer = sr.Recognizer() if HAS_SR else None

    async def speak_advanced(self, text, voice="en-US-AvaNeural"):
        """Uses edge-tts for high-quality natural speech (FREE)"""
        if not HAS_EDGE_TTS:
            return False
        try:
            communicate = edge_tts.Communicate(text, voice)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                await communicate.save(tmp.name)
                tmp_path = tmp.name

            if not HAS_PYGAME:
                return False
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            pygame.mixer.quit()
            os.unlink(tmp_path)
            return True
        except Exception as e:
            logger.error(f"Advanced Speak Error: {e}")
            return False

    def listen_advanced(self, source_audio):
        """Uses OpenAI Whisper for high-accuracy speech-to-text"""
        if not HAS_WHISPER or not self.whisper_model:
            return None
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(source_audio.get_wav_data())
                tmp_path = tmp.name

            result = self.whisper_model.transcribe(tmp_path, fp16=False)
            os.unlink(tmp_path)
            return result["text"].strip().lower()
        except Exception as e:
            logger.error(f"Advanced Listen Error: {e}")
            return None


def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)
