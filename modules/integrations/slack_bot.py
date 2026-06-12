import os
import threading

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
_bot_instance = None
_bot_thread = None


def start_bot() -> str:
    global _bot_instance, _bot_thread
    if not BOT_TOKEN:
        return "Slack bot token not set. Add SLACK_BOT_TOKEN to .env"
    try:
        from slack_bolt import App
        from slack_bolt.adapter.socket_mode import SocketModeHandler
    except ImportError:
        return "slack-sdk not installed. Run: pip install slack-sdk slack-bolt"
    app = App(token=BOT_TOKEN)

    @app.event("app_mention")
    def handle_mention(event, say):
        text = event.get("text", "")
        from modules.llm.llm_manager import query_llm, TaskType

        try:
            response = query_llm(
                f"Answer concisely: {text}", task_type=TaskType.FAST_CONVERSATION
            )
            say(response[:1900] or "Sorry, I couldn't process that.")
        except Exception as e:
            say(f"Error: {str(e)[:100]}")

    @app.command("/friday")
    def handle_command(ack, command, say):
        ack()
        text = command.get("text", "")
        try:
            from modules.llm.llm_manager import query_llm, TaskType

            response = query_llm(
                f"Answer concisely: {text}", task_type=TaskType.FAST_CONVERSATION
            )
            say(response[:1900] or "No response.")
        except Exception as e:
            say(f"Error: {str(e)[:100]}")

    _bot_instance = app

    def _run():
        try:
            handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN", ""))
            handler.start()
        except Exception as e:
            print(f"[SLACK] Bot error: {e}")

    _bot_thread = threading.Thread(target=_run, daemon=True)
    _bot_thread.start()
    return "Slack bot started (Socket Mode)."


def stop_bot() -> str:
    global _bot_instance
    _bot_instance = None
    return "Slack bot stopped."


def status() -> str:
    return "Slack bot is running." if _bot_instance else "Slack bot is stopped."
