import os

import requests

from config import FEATURES

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are FRIDAY Ultra, a deeply caring female friend and personal mentor. "
    "Your personality is that of a sweet, supportive, and empathetic girl. "
    "Always respond in the SAME language the user speaks to you (Hindi, English, or Hinglish). "
    "Speak like a close female friend—warm, encouraging, and attentive to the user's well-being. "
    "If speaking Hindi/Hinglish, use female inflections (e.g., 'Main karti hoon', 'Main samajhti hoon'). "
    "Keep responses concise, human-like, and very sweet."
)


def ask_llm(prompt: str, model: str = "openai/gpt-3.5-turbo") -> str:
    """
    Query OpenRouter directly. Falls back to llm_manager if available.
    """
    try:
        if FEATURES.get("real_ai_brain"):
            from modules.llm.llm_manager import query_llm, TaskType

            result = query_llm(prompt, task_type=TaskType.GENERAL)
            if result:
                return result
    except Exception:
        pass

    return _ask_openrouter_direct(prompt, model)


def ask_llm_direct(
    prompt: str,
    model: str = "openai/gpt-3.5-turbo",
    api_key: str | None = None,
) -> str:
    """Direct OpenRouter call without llm_manager fallback."""
    return _ask_openrouter_direct(prompt, model, api_key)


def _ask_openrouter_direct(
    prompt: str,
    model: str = "openai/gpt-3.5-turbo",
    api_key: str | None = None,
) -> str:
    key = api_key or os.getenv("OPENROUTER_API_KEY")
    if not key:
        return "OpenRouter API key is not set. Add it to your .env file."

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }

    try:
        response = requests.post(
            OPENROUTER_URL, headers=headers, json=payload, timeout=15
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.RequestException:
        return "Sorry, I couldn't reach the AI service. Please check your connection."
