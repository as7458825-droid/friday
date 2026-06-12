"""
FRIDAY — Language Preference Manager
Persists the user's preferred language to memory_db/user_lang.json.
"""

import json
import os
import logging

log = logging.getLogger("FRIDAY")

LANG_FILE = os.path.join(os.path.dirname(__file__), "..", "memory_db", "user_lang.json")

_DEFAULT_LANG = "en"
_current_lang: str | None = None


def _load() -> str:
    if not os.path.isfile(LANG_FILE):
        return _DEFAULT_LANG
    try:
        with open(LANG_FILE) as f:
            data = json.load(f)
            return data.get("language", _DEFAULT_LANG)
    except Exception:
        return _DEFAULT_LANG


def _save(lang: str):
    os.makedirs(os.path.dirname(LANG_FILE), exist_ok=True)
    with open(LANG_FILE, "w") as f:
        json.dump({"language": lang}, f)


def set_language(lang_code: str) -> str:
    global _current_lang
    _current_lang = lang_code
    _save(lang_code)
    log.info("Language set to %s", lang_code)
    return lang_code


def get_language() -> str:
    global _current_lang
    if _current_lang is None:
        _current_lang = _load()
    return _current_lang


def reset_language():
    global _current_lang
    _current_lang = _DEFAULT_LANG
    _save(_DEFAULT_LANG)
