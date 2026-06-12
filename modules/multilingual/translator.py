"""
FRIDAY — Multi‑language Translator
Provides language detection, translation, and a list of 50+ supported languages.
"""

import logging

log = logging.getLogger("FRIDAY")

try:
    from deep_translator import GoogleTranslator

    _translator = GoogleTranslator()
    HAS_TRANSLATOR = True
except ImportError:
    _translator = None
    HAS_TRANSLATOR = False

try:
    from langdetect import detect, DetectorFactory

    DetectorFactory.seed = 0
    HAS_LANGDETECT = True
except ImportError:
    HAS_LANGDETECT = False

LANGUAGES = {
    "a": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "as": "Assamese",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "my": "Burmese",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "ny": "Chichewa",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "iw": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "rw": "Kinyarwanda",
    "ko": "Korean",
    "ku": "Kurdish",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "mn": "Mongolian",
    "ne": "Nepali",
    "no": "Norwegian",
    "or": "Odia",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sm": "Samoan",
    "gd": "Scots Gaelic",
    "sr": "Serbian",
    "st": "Sesotho",
    "sn": "Shona",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tg": "Tajik",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "ug": "Uyghur",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu",
}

LANG_RECOGNITION = {
    "en": "en-IN",
    "es": "es-ES",
    "fr": "fr-FR",
    "de": "de-DE",
    "it": "it-IT",
    "pt": "pt-BR",
    "ru": "ru-RU",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh-cn": "zh-CN",
    "ar": "ar-SA",
    "hi": "hi-IN",
    "bn": "bn-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "mr": "mr-IN",
    "gu": "gu-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
    "pa": "pa-IN",
    "ur": "ur-IN",
    "th": "th-TH",
    "vi": "vi-VN",
    "tr": "tr-TR",
    "nl": "nl-NL",
    "pl": "pl-PL",
    "sv": "sv-SE",
    "ro": "ro-RO",
    "cs": "cs-CZ",
    "el": "el-GR",
    "da": "da-DK",
    "fi": "fi-FI",
    "hu": "hu-HU",
    "id": "id-ID",
    "ms": "ms-MY",
}


def detect_language(text: str) -> str:
    if not HAS_LANGDETECT:
        return "en"
    try:
        return detect(text)
    except Exception:
        return "en"


def translate_text(
    text: str, target_lang: str = "en", source_lang: str = "auto"
) -> str:
    if not HAS_TRANSLATOR:
        return text
    if target_lang == source_lang or source_lang == target_lang:
        return text
    if target_lang == "en" and source_lang == "auto":
        pass
    try:
        t = GoogleTranslator(source=source_lang, target=target_lang)
        return t.translate(text)
    except Exception:
        return text


def get_supported_languages() -> dict[str, str]:
    return dict(LANGUAGES)


def get_recognition_locale(lang_code: str) -> str:
    return LANG_RECOGNITION.get(lang_code, "en-IN")
