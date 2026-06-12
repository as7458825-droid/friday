"""
FRIDAY — Startup Cache
Pre-loads common resources in background threads to reduce first-command latency.
"""

import logging
import os
import sys
import threading

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

log = logging.getLogger("FRIDAY")

_cache_ready = threading.Event()
_voice_engine = None


def preload_tts():
    """Pre-initialize pyttsx3 engine in background."""
    global _voice_engine
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty("rate", 180)
        _voice_engine = engine
        log.info("Startup cache: TTS engine pre-loaded")
    except Exception as e:
        log.warning("Startup cache: TTS pre-load failed: %s", e)


def preload_chromadb():
    """Pre-warm ChromaDB connection."""
    try:
        from modules.memory.vector_store import get_client

        client = get_client()
        client.heartbeat()
        log.info("Startup cache: ChromaDB connection warmed")
    except Exception as e:
        log.warning("Startup cache: ChromaDB pre-warm failed: %s", e)


def preload_common_responses():
    """Pre-cache common responses to avoid first-call delay."""
    _common = {
        "help": "I can help with time, date, system commands, and more. Say help for details.",
        "time": "Loading time...",
        "date": "Loading date...",
        "exit": "Goodbye",
    }
    log.info("Startup cache: %d common responses cached", len(_common))
    return _common


def start_background_caches():
    """Launch all pre-load threads."""
    threads = [
        threading.Thread(target=preload_tts, daemon=True, name="cache-tts"),
        threading.Thread(target=preload_chromadb, daemon=True, name="cache-chromadb"),
    ]
    for t in threads:
        t.start()
    _cache_ready.set()
    return threads
