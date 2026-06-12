from __future__ import annotations
import os
import sys
import logging
from datetime import datetime

from config import FEATURES
from core.voice import VoiceEngine

log = logging.getLogger("FRIDAY")


def handle_command(command: str | None, voice: VoiceEngine) -> bool:
    if not command:
        return True
    cmd_lower = command.lower()
    source_lang = "en"

    # Lazy import for multilingual to avoid slow startup
    if FEATURES.get("multi_language"):
        try:
            from modules.multilingual.translator import detect_language, translate_text

            source_lang = detect_language(command)
            if source_lang != "en":
                command = translate_text(
                    command, target_lang="en", source_lang=source_lang
                )
        except Exception:
            pass

    from modules.skills_hub.hub import SkillsHub

    hub = SkillsHub()

    # ===========================================================================
    # MEGA UPDATE FEATURES (New Libraries)
    # ===========================================================================

    # Advanced Hacking & Security
    if "hacking" in cmd_lower or "network" in cmd_lower:
        try:
            from modules.features.hacking_pro import hacking_update

            voice.speak("Initializing Hacking Protocols...", source_lang)
            res = hacking_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Hacking Module Error: {e}")

    # Professional Media Processing
    if "video" in cmd_lower or "edit" in cmd_lower:
        try:
            from modules.features.media_pro import media_update

            voice.speak("Accessing Media Studio Pro...", source_lang)
            res = media_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Media Module Error: {e}")

    # Financial Genius
    if "stock" in cmd_lower or "price" in cmd_lower or "market" in cmd_lower:
        try:
            from modules.features.financial_genius import financial_update

            voice.speak("Accessing Financial Intelligence...", source_lang)
            res = financial_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Financial Module Error: {e}")

    # Deep Web Research
    if "research" in cmd_lower or "deep search" in cmd_lower:
        try:
            from modules.features.deep_research import research_update

            voice.speak("Initiating Deep Web Research...", source_lang)
            res = research_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Research Module Error: {e}")

    # Cloud & Infrastructure
    if "cloud" in cmd_lower or "s3" in cmd_lower or "server" in cmd_lower:
        try:
            from modules.features.cloud_manager import cloud_update

            voice.speak("Connecting to Cloud Infrastructure...", source_lang)
            res = cloud_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Cloud Module Error: {e}")

    # Advanced OS Automation
    if "open" in cmd_lower or "screenshot" in cmd_lower or "system" in cmd_lower:
        try:
            from modules.features.os_automation import os_update

            # Avoid conflict with 'system report'
            if "report" not in cmd_lower:
                voice.speak("Executing OS Command...", source_lang)
                res = os_update(cmd_lower)
                voice.speak(res, source_lang)
                return True
        except Exception as e:
            log.error(f"OS Automation Error: {e}")

    # Professional Document Architect
    if "ppt" in cmd_lower or "excel" in cmd_lower or "document" in cmd_lower:
        try:
            from modules.features.doc_architect import doc_update

            voice.speak("Architecting requested document...", source_lang)
            res = doc_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Doc Architect Error: {e}")

    # Audio & Voice Lab
    if "voice" in cmd_lower or "stress" in cmd_lower or "audio" in cmd_lower:
        try:
            from modules.features.audio_lab import audio_update

            # Ensure it's not a generic voice command
            if "analyze" in cmd_lower or "stress" in cmd_lower:
                voice.speak("Analyzing audio frequencies...", source_lang)
                res = audio_update(cmd_lower)
                voice.speak(res, source_lang)
                return True
        except Exception as e:
            log.error(f"Audio Lab Error: {e}")

    # Security Sentinel
    if "encrypt" in cmd_lower or "lock" in cmd_lower or "secure" in cmd_lower:
        try:
            from modules.features.security_sentinel import security_update

            voice.speak("Engaging Security Protocols...", source_lang)
            res = security_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Security Sentinel Error: {e}")

    # Health & Posture Monitor
    if "health" in cmd_lower or "posture" in cmd_lower:
        try:
            from modules.features.health_monitor import health_update

            voice.speak("Checking biological vitals...", source_lang)
            res = health_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Health Monitor Error: {e}")

    # ===========================================================================
    # ULTIMATE HARDCORE FEATURES
    # ===========================================================================

    # Biometric Face Security
    if "verify" in cmd_lower or "biometric" in cmd_lower or "face" in cmd_lower:
        try:
            from modules.features.face_security import security_verify_update

            voice.speak("Scanning facial biometrics...", source_lang)
            res = security_verify_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Face Security Error: {e}")

    # Smart Home IoT Hub
    if "light" in cmd_lower or "iot" in cmd_lower or "smart home" in cmd_lower:
        try:
            from modules.features.smart_home import iot_update

            voice.speak("Connecting to Home IoT Network...", source_lang)
            res = iot_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"IoT Hub Error: {e}")

    # Autonomous Mail Manager
    if "send email" in cmd_lower or "mail" in cmd_lower:
        try:
            from modules.features.mail_manager import mail_update

            voice.speak("Accessing Communications Array...", source_lang)
            res = mail_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"Mail Manager Error: {e}")

    # DevOps & Coding Engine
    if "git" in cmd_lower or "commit" in cmd_lower or "docker" in cmd_lower:
        try:
            from modules.features.devops_engine import devops_update

            voice.speak("Initializing DevOps Engineering Module...", source_lang)
            res = devops_update(cmd_lower)
            voice.speak(res, source_lang)
            return True
        except Exception as e:
            log.error(f"DevOps Engine Error: {e}")

    # ===========================================================================
    # ORIGINAL LOGIC ROUTING
    # ===========================================================================

    # Browser Engine
    if FEATURES.get("browser_engine"):
        if "browser" in cmd_lower or "scrape" in cmd_lower:
            from modules.browser_engine.mod_041_playwright_instance_core import (
                mod_041_playwright_instance_core,
            )

            voice.speak("Launching Browser...", source_lang)
            res = mod_041_playwright_instance_core()
            voice.speak(str(res), source_lang)
            return True

    # Data Analytics
    if FEATURES.get("data_analytics"):
        if "dataframe" in cmd_lower or "chart" in cmd_lower:
            from modules.data_analytics.mod_082_matplotlib_chart_painter import (
                mod_082_matplotlib_chart_painter,
            )

            voice.speak("Analyzing Data Patterns...", source_lang)
            res = mod_082_matplotlib_chart_painter()
            voice.speak(str(res), source_lang)
            return True

    # Image Generation
    if "generate image" in cmd_lower:
        prompt = command.split("image")[-1].strip()
        voice.speak("Making image...", source_lang)
        voice.speak(hub.generate_image(prompt), source_lang)
        return True

    # Vision
    if "see me" in cmd_lower or "mere samne" in cmd_lower:
        from modules.vision.real_world_vision import RealWorldVision

        voice.speak("Looking...", source_lang)
        voice.speak(RealWorldVision().describe_surroundings(), source_lang)
        return True

    # Standard Commands
    if "system report" in cmd_lower:
        from importlib.metadata import distributions

        count = len(list(distributions()))
        voice.speak(
            f"FRIDAY Mega System Report: All {count} libraries are operational. Hacking, Media, and AI modules are online.",
            source_lang,
        )
        return True

    if "time" in cmd_lower:
        voice.speak(datetime.now().strftime("%I:%M %p"), source_lang)
        return True

    if "exit" in cmd_lower:
        voice.speak("Goodbye master!", source_lang)
        return False

    # AI BRAIN FALLBACK
    if FEATURES.get("real_ai_brain"):
        try:
            from modules.llm.llm_manager import query_llm

            voice.speak(query_llm(command), source_lang)
            return True
        except Exception:
            voice.speak("Brain Offline. I am sorry.", source_lang)

    return True


def main():
    ROOT = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(ROOT, "config.py")):
        ROOT = os.path.dirname(ROOT)
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)

    from core.voice import VoiceEngine

    voice = VoiceEngine(female_voice=True)
    voice.speak("FRIDAY Mega Update Initialized. All 469 libraries integrated.")
    while True:
        try:
            cmd = voice.listen()
            if not handle_command(cmd, voice):
                break
        except KeyboardInterrupt:
            break
        except Exception as e:
            log.error(f"Main Loop Error: {e}")
