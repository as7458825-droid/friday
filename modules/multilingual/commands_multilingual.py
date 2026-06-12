"""
FRIDAY — Multi‑lingual Command Mapper
Maps basic command phrases across 50+ languages so users can speak
commands in their native language without translation overhead.
"""

COMMAND_TRANSLATIONS: dict[str, dict[str, list[str]]] = {
    "time": {
        "en": ["time", "what time is it", "tell me the time"],
        "hi": ["समय", "कितने बजे हैं", "टाइम बताओ"],
        "bn": ["সময়", "কটা বাজে", "সময় বলুন"],
        "pa": ["ਸਮਾਂ", "ਕੀ ਵਜੇ ਹਨ", "ਸਮਾਂ ਦੱਸੋ"],
        "te": ["సమయం", "ఇప్పుడు ఎంత సమయం"],
        "ta": ["நேரம்", "இப்போது நேரம் என்ன"],
        "mr": ["वेळ", "किती वाजले"],
        "gu": ["સમય", "કેટલા વાગ્યા"],
        "kn": ["ಸಮಯ", "ಈಗ ಸಮಯ ಎಷ್ಟು"],
        "ml": ["സമയം", "ഇപ്പോൾ എന്ത് സമയം"],
        "ur": ["وقت", "کتنے بجے ہیں"],
        "or": ["ସମୟ", "କେତେ ବାଜିଲା"],
        "es": ["hora", "qué hora es"],
        "fr": ["heure", "quelle heure est-il"],
        "de": ["zeit", "wie spät ist es"],
        "it": ["ora", "che ora è"],
        "pt": ["hora", "que horas são"],
        "ru": ["время", "который час"],
        "ja": ["時間", "今何時"],
        "ko": ["시간", "지금 몇 시"],
        "zh-cn": ["时间", "几点了"],
        "ar": ["وقت", "كم الساعة"],
        "tr": ["saat", "saat kaç"],
        "nl": ["tijd", "hoe laat is het"],
        "pl": ["czas", "która godzina"],
        "sv": ["tid", "vad är klockan"],
        "th": ["เวลา", "กี่โมงแล้ว"],
        "vi": ["giờ", "mấy giờ rồi"],
        "ro": ["timp", "cât e ceasul"],
        "cs": ["čas", "kolik je hodin"],
    },
    "date": {
        "en": ["date", "what is the date", "today's date"],
        "hi": ["तारीख", "आज तारीख क्या है"],
        "bn": ["তারিখ", "আজকের তারিখ কী"],
        "pa": ["ਮਿਤੀ", "ਅੱਜ ਦੀ ਮਿਤੀ ਕੀ ਹੈ"],
        "te": ["తేదీ", "నేటి తేదీ ఏమిటి"],
        "ta": ["தேதி", "இன்றைய தேதி என்ன"],
        "mr": ["तारीख", "आजची तारीख काय"],
        "gu": ["તારીખ", "આજની તારીખ શું છે"],
        "es": ["fecha", "qué fecha es hoy"],
        "fr": ["date", "quelle est la date"],
        "de": ["datum", "welches datum ist heute"],
        "it": ["data", "che data è"],
        "pt": ["data", "qual é a data"],
        "ru": ["дата", "какое сегодня число"],
        "ja": ["日付", "今日は何日"],
        "ko": ["날짜", "오늘 날짜가 뭐야"],
        "zh-cn": ["日期", "今天几号"],
        "ar": ["تاريخ", "ما هو التاريخ اليوم"],
    },
    "help": {
        "en": ["help", "what can you do"],
        "hi": ["मदद", "आप क्या कर सकते हैं"],
        "bn": ["সাহায্য", "আপনি কী করতে পারেন"],
        "es": ["ayuda", "qué puedes hacer"],
        "fr": ["aide", "que peux-tu faire"],
        "de": ["hilfe", "was kannst du tun"],
        "zh-cn": ["帮助", "你能做什么"],
    },
    "exit": {
        "en": ["exit", "quit", "bye", "goodbye"],
        "hi": ["बाहर", "रुको", "अलविदा"],
        "bn": ["প্রস্থান", "বিদায়"],
        "es": ["salir", "adiós", "cerrar"],
        "fr": ["quitter", "au revoir"],
        "de": ["beenden", "tschüss"],
        "zh-cn": ["退出", "再见"],
        "ar": ["خروج", "وداعا"],
    },
    "open": {
        "en": ["open"],
        "hi": ["खोलो"],
        "bn": ["খোলো"],
        "es": ["abrir"],
        "fr": ["ouvrir"],
        "de": ["öffnen"],
    },
    "search": {
        "en": ["search", "find", "look up"],
        "hi": ["खोज", "ढूंढो"],
        "bn": ["অনুসন্ধান", "খুঁজুন"],
        "es": ["buscar", "encontrar"],
        "fr": ["chercher", "trouver"],
        "de": ["suchen", "finden"],
    },
    "chat": {
        "en": ["open chat", "show chat", "chat", "close chat", "hide chat"],
        "hi": ["चैट खोलो", "चैट दिखाओ", "चैट बंद करो"],
        "bn": ["চ্যাট খোলো", "চ্যাট দেখাও"],
        "es": ["abrir chat", "mostrar chat", "cerrar chat"],
        "fr": ["ouvrir le chat", "afficher le chat", "fermer le chat"],
        "de": ["chat öffnen", "chat anzeigen", "chat schließen"],
    },
    "language": {
        "en": ["change language to", "switch language to", "set language to"],
        "hi": ["भाषा बदलो", "भाषा चुनो"],
        "bn": ["भाषा परिवर्तन करें"],
        "es": ["cambiar idioma a"],
        "fr": ["changer la langue en"],
        "de": ["sprache ändern zu"],
    },
    "resume": {
        "en": ["resume", "read resume", "listen to resume", "resumesuno"],
        "hi": ["रिज्यूमे", "बायोडाटा", "रिज्यूमे सुनो", "रिज्यूमे पढ़ो", "resume suno", "resumesuno"],
    },
    }


def match_multilingual_command(text: str) -> tuple[str, str] | None:
    """Match user text against all known commands across all languages.
    Returns (english_command_key, matched_text) or None."""
    text_lower = text.lower().strip()
    for cmd_key, lang_map in COMMAND_TRANSLATIONS.items():
        for lang_code, phrases in lang_map.items():
            for phrase in phrases:
                if text_lower == phrase or text_lower.startswith(phrase + " "):
                    return cmd_key, phrase
    return None
