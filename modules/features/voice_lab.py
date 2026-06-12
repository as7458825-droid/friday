import whisper
import edge_tts
import asyncio
import os
import tempfile
import pygame
import logging
import torch
import speech_recognition as sr

logger = logging.getLogger(__name__)


class AdvancedVoiceLab:
    """Advanced AI Voice & Listening Module for FRIDAY"""

    def __init__(self):
        # Load Whisper model (tiny for speed, can be upgraded to base/small)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.whisper_model = whisper.load_model("tiny", device=device)
        self.recognizer = sr.Recognizer()

    async def speak_advanced(self, text, voice="en-US-AvaNeural"):
        """Uses edge-tts for high-quality natural speech (FREE)"""
        try:
            communicate = edge_tts.Communicate(text, voice)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                await communicate.save(tmp.name)
                tmp_path = tmp.name

            # Play using pygame for smooth playback
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
        try:
            # Save temporary wav for whisper
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
