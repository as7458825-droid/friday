import os
import threading

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "")

_bot_thread = None
_bot_instance = None


def start_bot() -> str:
    global _bot_thread, _bot_instance
    if not BOT_TOKEN:
        return "Telegram bot token not set. Add TELEGRAM_BOT_TOKEN to .env"
    try:
        import telebot
    except ImportError:
        return "telebot not installed. Run: pip install pyTelegramBotAPI"
    _bot_instance = telebot.TeleBot(BOT_TOKEN, threaded=False)

    @_bot_instance.message_handler(commands=["start", "help"])
    def send_welcome(message):
        _bot_instance.reply_to(
            message, "FRIDAY Assistant is online! Send /status or a message."
        )

    @_bot_instance.message_handler(commands=["status"])
    def send_status(message):
        import psutil

        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        _bot_instance.reply_to(message, f"FRIDAY Status:\nCPU: {cpu}%\nRAM: {mem}%")

    @_bot_instance.message_handler(func=lambda m: True)
    def echo(message):
        if ALLOWED_CHAT_IDS:
            allowed = [int(x.strip()) for x in ALLOWED_CHAT_IDS.split(",") if x.strip()]
            if message.chat.id not in allowed:
                return
        _bot_instance.reply_to(message, f"Received: {message.text[:200]}")

    def _run():
        _bot_instance.infinity_polling(long_polling_timeout=30)

    _bot_thread = threading.Thread(target=_run, daemon=True)
    _bot_thread.start()
    return "Telegram bot started."


def stop_bot() -> str:
    global _bot_instance
    if _bot_instance:
        try:
            _bot_instance.stop_polling()
        except Exception:
            pass
        _bot_instance = None
    return "Telegram bot stopped."


def bot_status() -> str:
    if _bot_instance and _bot_thread and _bot_thread.is_alive():
        return "Telegram bot is running."
    return "Telegram bot is stopped."
