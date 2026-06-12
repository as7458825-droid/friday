import asyncio
import edge_tts
import os
import pygame


async def speak_with_emotion(text, emotion="neutral"):
    """Speak text using Edge-TTS with appropriate voice tone."""
    # Mapping emotions to specific voices/styles
    voice_map = {
        "excited": "en-US-AvaNeural",
        "sad/tired": "en-US-EmmaNeural",
        "angry/stressed": "en-US-GuyNeural",
        "neutral": "en-US-AvaNeural",
    }

    voice = voice_map.get(emotion, "en-US-AvaNeural")
    output_file = "temp_speech.mp3"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

    # Play the audio
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)
    pygame.mixer.music.unload()
    os.remove(output_file)


def run_speak(text, emotion="neutral"):
    asyncio.run(speak_with_emotion(text, emotion))
