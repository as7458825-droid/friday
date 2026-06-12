import os
import json
import re

SMART_REPLIES_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "smart_replies.json"
)

try:
    from modules.llm.llm_manager import query_llm, TaskType

    HAS_LLM = True
except Exception:
    HAS_LLM = False


def generate_reply(email_text: str, tone: str = "professional") -> str:
    if not HAS_LLM:
        return "LLM not available for smart reply."
    prompt = (
        f"Generate a {tone} email reply (2-3 sentences max) to: {email_text[:1000]}"
    )
    reply = query_llm(prompt, task_type=TaskType.FAST_CONVERSATION)
    if reply:
        reply = re.sub(
            r"^(Here\'s|Sure|Okay|Of course|Absolutely).*?:", "", reply
        ).strip()
        _save_reply(email_text[:50], reply)
        return reply[:500]
    return "Could not generate reply."


def generate_reply_to_sender(sender: str, tone: str = "professional") -> str:
    if not HAS_LLM:
        return "LLM not available."
    prompt = f"Generate a {tone} email reply to {sender} (2-3 sentences)."
    reply = query_llm(prompt, task_type=TaskType.FAST_CONVERSATION)
    return reply[:500] if reply else "Could not generate reply."


def _save_reply(context: str, reply: str):
    mem = os.path.dirname(SMART_REPLIES_FILE)
    if not os.path.isdir(mem):
        os.makedirs(mem, exist_ok=True)
    data = []
    if os.path.isfile(SMART_REPLIES_FILE):
        with open(SMART_REPLIES_FILE) as f:
            data = json.load(f)
    data.append({"context": context, "reply": reply})
    with open(SMART_REPLIES_FILE, "w") as f:
        json.dump(data[-20:], f, indent=2)


def list_replies() -> str:
    if not os.path.isfile(SMART_REPLIES_FILE):
        return "No saved replies."
    with open(SMART_REPLIES_FILE) as f:
        data = json.load(f)
    if not data:
        return "No saved replies."
    return "Recent replies: " + " | ".join(
        f"To: {d['context'][:30]} -> {d['reply'][:50]}" for d in data[-3:]
    )
