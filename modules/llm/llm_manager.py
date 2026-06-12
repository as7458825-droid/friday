import os
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from config import FEATURES


class TaskType(Enum):
    REASONING = "reasoning"
    CODING = "coding"
    VISION = "vision"
    FAST_CONVERSATION = "fast_conversation"
    GENERAL = "general"


@dataclass
class ModelConfig:
    name: str
    provider: str
    model_id: str
    api_key_env: str | None = None
    base_url: str | None = None
    capabilities: set = field(default_factory=lambda: {"text"})
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    context_window: int = 4096
    priority: int = 10


MODEL_REGISTRY: dict[str, ModelConfig] = {
    "openrouter-gpt-4o": ModelConfig(
        "openrouter-gpt-4o",
        "openrouter",
        "openai/gpt-4o",
        capabilities={"text", "vision", "reasoning", "coding"},
        cost_per_1k_input=0.005,
        cost_per_1k_output=0.015,
        context_window=128000,
        priority=1,
    ),
    "openrouter-gpt-4o-mini": ModelConfig(
        "openrouter-gpt-4o-mini",
        "openrouter",
        "openai/gpt-4o-mini",
        capabilities={"text", "vision"},
        cost_per_1k_input=0.00015,
        cost_per_1k_output=0.0006,
        context_window=128000,
        priority=1,
    ),
    "openrouter-claude-3.5-sonnet": ModelConfig(
        "openrouter-claude-3.5-sonnet",
        "openrouter",
        "anthropic/claude-3.5-sonnet",
        capabilities={"text", "reasoning", "coding"},
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        context_window=200000,
        priority=1,
    ),
    "openrouter-claude-opus": ModelConfig(
        "openrouter-claude-opus",
        "openrouter",
        "anthropic/claude-opus",
        capabilities={"text", "reasoning", "coding"},
        cost_per_1k_input=0.015,
        cost_per_1k_output=0.075,
        context_window=200000,
        priority=1,
    ),
    "openrouter-claude-haiku": ModelConfig(
        "openrouter-claude-haiku",
        "openrouter",
        "anthropic/claude-3-haiku",
        capabilities={"text"},
        cost_per_1k_input=0.00025,
        cost_per_1k_output=0.00125,
        context_window=200000,
        priority=1,
    ),
    "openrouter-gemini-pro": ModelConfig(
        "openrouter-gemini-pro",
        "openrouter",
        "google/gemini-pro",
        capabilities={"text", "reasoning"},
        cost_per_1k_input=0.0005,
        cost_per_1k_output=0.0015,
        context_window=32000,
        priority=1,
    ),
    "openrouter-gemini-pro-vision": ModelConfig(
        "openrouter-gemini-pro-vision",
        "openrouter",
        "google/gemini-pro-vision",
        capabilities={"text", "vision"},
        cost_per_1k_input=0.0005,
        cost_per_1k_output=0.0015,
        context_window=32000,
        priority=1,
    ),
    "openrouter-gpt-3.5-turbo": ModelConfig(
        "openrouter-gpt-3.5-turbo",
        "openrouter",
        "openai/gpt-3.5-turbo",
        capabilities={"text"},
        cost_per_1k_input=0.0005,
        cost_per_1k_output=0.0015,
        context_window=16384,
        priority=2,
    ),
    "openai-gpt-4o": ModelConfig(
        "openai-gpt-4o",
        "openai",
        "gpt-4o",
        api_key_env="OPENAI_API_KEY",
        capabilities={"text", "vision", "reasoning", "coding"},
        cost_per_1k_input=0.005,
        cost_per_1k_output=0.015,
        context_window=128000,
        priority=5,
    ),
    "openai-gpt-4o-mini": ModelConfig(
        "openai-gpt-4o-mini",
        "openai",
        "gpt-4o-mini",
        api_key_env="OPENAI_API_KEY",
        capabilities={"text", "vision"},
        cost_per_1k_input=0.00015,
        cost_per_1k_output=0.0006,
        context_window=128000,
        priority=5,
    ),
    "openai-o3-mini": ModelConfig(
        "openai-o3-mini",
        "openai",
        "o3-mini",
        api_key_env="OPENAI_API_KEY",
        capabilities={"text", "reasoning", "coding"},
        cost_per_1k_input=0.0011,
        cost_per_1k_output=0.0044,
        context_window=200000,
        priority=5,
    ),
    "anthropic-claude-sonnet-4": ModelConfig(
        "anthropic-claude-sonnet-4",
        "anthropic",
        "claude-sonnet-4-20250514",
        api_key_env="ANTHROPIC_API_KEY",
        capabilities={"text", "reasoning", "coding"},
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        context_window=200000,
        priority=5,
    ),
    "anthropic-claude-haiku-3": ModelConfig(
        "anthropic-claude-haiku-3",
        "anthropic",
        "claude-3-haiku-20240307",
        api_key_env="ANTHROPIC_API_KEY",
        capabilities={"text"},
        cost_per_1k_input=0.00025,
        cost_per_1k_output=0.00125,
        context_window=200000,
        priority=5,
    ),
    "google-gemini-2.0-flash": ModelConfig(
        "google-gemini-2.0-flash",
        "google",
        "gemini-2.0-flash",
        api_key_env="GOOGLE_API_KEY",
        capabilities={"text", "vision", "reasoning"},
        cost_per_1k_input=0.0001,
        cost_per_1k_output=0.0004,
        context_window=1000000,
        priority=5,
    ),
    "google-gemini-2.0-flash-lite": ModelConfig(
        "google-gemini-2.0-flash-lite",
        "google",
        "gemini-2.0-flash-lite",
        api_key_env="GOOGLE_API_KEY",
        capabilities={"text"},
        cost_per_1k_input=0.000075,
        cost_per_1k_output=0.0003,
        context_window=1000000,
        priority=5,
    ),
    "grok-2": ModelConfig(
        "grok-2",
        "grok",
        "grok-2",
        api_key_env="XAI_API_KEY",
        capabilities={"text", "reasoning"},
        cost_per_1k_input=0.002,
        cost_per_1k_output=0.01,
        context_window=131072,
        priority=5,
    ),
    "grok-2-vision": ModelConfig(
        "grok-2-vision",
        "grok",
        "grok-2-vision",
        api_key_env="XAI_API_KEY",
        capabilities={"text", "vision", "reasoning"},
        cost_per_1k_input=0.002,
        cost_per_1k_output=0.01,
        context_window=131072,
        priority=5,
    ),
    "ollama-llama3": ModelConfig(
        "ollama-llama3",
        "ollama",
        "llama3",
        capabilities={"text"},
        context_window=8192,
        priority=20,
    ),
    "ollama-mistral": ModelConfig(
        "ollama-mistral",
        "ollama",
        "mistral",
        capabilities={"text"},
        context_window=8192,
        priority=20,
    ),
    "ollama-phi": ModelConfig(
        "ollama-phi",
        "ollama",
        "phi",
        capabilities={"text"},
        context_window=2048,
        priority=20,
    ),
    "ollama-gemma": ModelConfig(
        "ollama-gemma",
        "ollama",
        "gemma",
        capabilities={"text"},
        context_window=8192,
        priority=20,
    ),
    "ollama-llama3.2": ModelConfig(
        "ollama-llama3.2",
        "ollama",
        "llama3.2",
        capabilities={"text", "vision"},
        context_window=128000,
        priority=20,
    ),
    "llamacpp": ModelConfig(
        "llamacpp",
        "llama_cpp",
        "",
        capabilities={"text"},
        context_window=4096,
        priority=20,
    ),
    "groq-llama-3.3-70b": ModelConfig(
        "groq-llama-3.3-70b",
        "groq",
        "llama-3.3-70b-versatile",
        api_key_env="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        capabilities={"text", "reasoning", "coding"},
        context_window=131072,
        priority=3,
    ),
    "groq-mixtral": ModelConfig(
        "groq-mixtral",
        "groq",
        "mixtral-8x7b-32768",
        api_key_env="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        capabilities={"text"},
        context_window=32768,
        priority=3,
    ),
    "groq-gemma2-9b": ModelConfig(
        "groq-gemma2-9b",
        "groq",
        "gemma2-9b-it",
        api_key_env="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        capabilities={"text"},
        context_window=8192,
        priority=3,
    ),
    "nvidia-llama-3.1-nemotron": ModelConfig(
        "nvidia-llama-3.1-nemotron",
        "nvidia",
        "nvidia/llama-3.1-nemotron-70b-instruct",
        api_key_env="NVIDIA_API_KEY",
        base_url="https://api.nvapi.ai/v1",
        capabilities={"text", "reasoning", "coding"},
        context_window=131072,
        priority=4,
    ),
    "nvidia-mistral": ModelConfig(
        "nvidia-mistral",
        "nvidia",
        "mistralai/mistral-7b-instruct-v0.3",
        api_key_env="NVIDIA_API_KEY",
        base_url="https://api.nvapi.ai/v1",
        capabilities={"text"},
        context_window=32768,
        priority=4,
    ),
    "deepseek-chat": ModelConfig(
        "deepseek-chat",
        "deepseek",
        "deepseek-chat",
        api_key_env="DEEPSEEK_API_KEY",
        base_url="https://api.deepseek.com",
        capabilities={"text", "reasoning", "coding"},
        cost_per_1k_input=0.00027,
        cost_per_1k_output=0.0011,
        context_window=65536,
        priority=3,
    ),
    "deepseek-coder": ModelConfig(
        "deepseek-coder",
        "deepseek",
        "deepseek-coder",
        api_key_env="DEEPSEEK_API_KEY",
        base_url="https://api.deepseek.com",
        capabilities={"text", "coding"},
        cost_per_1k_input=0.00014,
        cost_per_1k_output=0.00028,
        context_window=65536,
        priority=3,
    ),
    "opencode-ollama": ModelConfig(
        "opencode-ollama",
        "opencode",
        "llama3.2",
        api_key_env="OPENCODE_API_KEY",
        base_url="http://localhost:11434/v1",
        capabilities={"text", "vision"},
        context_window=128000,
        priority=15,
    ),
}

TASK_ROUTES: dict[TaskType, list[str]] = {
    TaskType.REASONING: [
        "openrouter-claude-opus",
        "openrouter-gpt-4o",
        "anthropic-claude-sonnet-4",
        "openai-o3-mini",
        "google-gemini-2.0-flash",
        "deepseek-chat",
        "groq-llama-3.3-70b",
        "nvidia-llama-3.1-nemotron",
        "openrouter-claude-3.5-sonnet",
        "ollama-llama3",
    ],
    TaskType.CODING: [
        "openrouter-claude-3.5-sonnet",
        "openrouter-gpt-4o",
        "anthropic-claude-sonnet-4",
        "openai-o3-mini",
        "deepseek-coder",
        "deepseek-chat",
        "groq-llama-3.3-70b",
        "nvidia-llama-3.1-nemotron",
        "openrouter-gpt-4o-mini",
        "ollama-llama3",
    ],
    TaskType.VISION: [
        "openrouter-gpt-4o",
        "openrouter-gemini-pro-vision",
        "openai-gpt-4o",
        "google-gemini-2.0-flash",
        "grok-2-vision",
        "opencode-ollama",
        "ollama-llama3.2",
    ],
    TaskType.FAST_CONVERSATION: [
        "openrouter-gpt-4o-mini",
        "openrouter-claude-haiku",
        "openai-gpt-4o-mini",
        "google-gemini-2.0-flash-lite",
        "groq-gemma2-9b",
        "groq-mixtral",
        "ollama-mistral",
        "ollama-phi",
    ],
    TaskType.GENERAL: [
        "openrouter-gpt-4o-mini",
        "openrouter-gpt-4o",
        "openrouter-claude-3.5-sonnet",
        "openai-gpt-4o-mini",
        "google-gemini-2.0-flash-lite",
        "deepseek-chat",
        "groq-llama-3.3-70b",
        "nvidia-llama-3.1-nemotron",
        "ollama-llama3",
    ],
}

PROVIDER_FEATURE_MAP = {
    "openrouter": "llm_openrouter",
    "openai": "llm_openai",
    "anthropic": "llm_anthropic",
    "google": "llm_google",
    "grok": "llm_grok",
    "groq": "llm_groq",
    "nvidia": "llm_nvidia",
    "deepseek": "llm_deepseek",
    "opencode": "llm_opencode",
    "ollama": "llm_local_ollama",
    "llama_cpp": "llm_local_llama_cpp",
}

_active_model_name = "openrouter-gpt-4o-mini"
_active_model_lock = threading.Lock()
_stream_callbacks: list[Callable[[str], None]] = []


def get_active_model() -> str:
    with _active_model_lock:
        return _active_model_name


def set_active_model(name: str) -> bool:
    if name not in MODEL_REGISTRY:
        return False
    with _active_model_lock:
        _active_model_name = name
    return True


def list_available_models() -> list[dict]:
    result = []
    active = get_active_model()
    for name, cfg in MODEL_REGISTRY.items():
        if not _is_provider_enabled(cfg.provider):
            continue
        key_ok = _check_api_key(cfg.provider)
        result.append(
            {
                "name": name,
                "provider": cfg.provider,
                "model_id": cfg.model_id,
                "capabilities": sorted(cfg.capabilities),
                "is_active": name == active,
                "has_key": key_ok,
                "cost_per_1k_input": cfg.cost_per_1k_input,
                "cost_per_1k_output": cfg.cost_per_1k_output,
                "context_window": cfg.context_window,
            }
        )
    return result


def get_model_status() -> str:
    lines = []
    lines.append(f"Active model: {get_active_model()}")
    seen = set()
    for name, cfg in MODEL_REGISTRY.items():
        prov = cfg.provider
        if prov in seen:
            continue
        seen.add(prov)
        if not _is_provider_enabled(prov):
            continue
        key_ok = _check_api_key(prov)
        if prov in ("ollama", "llama_cpp", "opencode"):
            status = "local"
        elif key_ok:
            status = "key set"
        else:
            status = "no key"
        icon = "✓" if key_ok or prov in ("ollama", "llama_cpp", "opencode") else "✗"
        lines.append(f"  {icon} {prov}: {status}")
    return "\n".join(lines)


def register_stream_callback(cb: Callable[[str], None]):
    _stream_callbacks.append(cb)


def unregister_stream_callback(cb: Callable[[str], None]):
    if cb in _stream_callbacks:
        _stream_callbacks.remove(cb)


def _emit_stream_token(token: str):
    for cb in _stream_callbacks:
        try:
            cb(token)
        except Exception:
            pass


def _is_provider_enabled(provider: str) -> bool:
    flag = PROVIDER_FEATURE_MAP.get(provider)
    if flag is None:
        return True
    return FEATURES.get(flag, False)


def _check_api_key(provider: str) -> bool:
    key_map = {
        "openrouter": "OPENROUTER_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
        "grok": "XAI_API_KEY",
        "groq": "GROQ_API_KEY",
        "nvidia": "NVIDIA_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "opencode": "OPENCODE_API_KEY",
    }
    env_var = key_map.get(provider)
    if env_var is None:
        return True
    key = os.getenv(env_var)
    if key:
        return True
    if provider == "google":
        return bool(os.getenv("GEMINI_API_KEY"))
    return False


def _make_cache_key(prompt: str, task_type: TaskType) -> str:
    return f"{task_type.value}::{prompt.strip().lower()[:200]}"


def _check_cache(key: str) -> str | None:
    try:
        from modules.memory.vector_store import search_memory

        results = search_memory(key, top_k=1)
        if results:
            meta = results[0].get("metadata", {})
            if meta.get("cache_hit"):
                return results[0]["text"]
    except Exception:
        pass
    return None


def _save_to_cache(key: str, response: str):
    try:
        from modules.memory.vector_store import add_to_memory

        add_to_memory(response, metadata={"cache_hit": True, "cache_key": key})
    except Exception:
        pass


SYSTEM_PROMPT = (
    "You are FRIDAY, a voice-controlled AI assistant. "
    "Keep responses concise and spoken-word friendly. "
    "Answer in one or two sentences unless asked for detail."
)


def query_llm(
    prompt: str,
    task_type: TaskType = TaskType.GENERAL,
    stream: bool = False,
    image: Any = None,
    system_override: str | None = None,
    max_tokens: int = 1024,
) -> str | None:
    cached = _check_cache(_make_cache_key(prompt, task_type))
    if cached:
        return cached

    active = get_active_model()
    chain = _build_fallback_chain(active, task_type)

    errors: list[str] = []
    for model_name in chain:
        cfg = MODEL_REGISTRY.get(model_name)
        if not cfg:
            errors.append(f"{model_name}: unknown")
            continue
        if not _is_provider_enabled(cfg.provider):
            errors.append(f"{model_name}: provider disabled")
            continue

        if image is not None and "vision" not in cfg.capabilities:
            continue
        if task_type == TaskType.CODING and "coding" not in cfg.capabilities:
            continue
        if task_type == TaskType.REASONING and "reasoning" not in cfg.capabilities:
            continue

        result = _try_model(cfg, prompt, stream, image, system_override, max_tokens)
        if result is not None:
            if not stream:
                _save_to_cache(_make_cache_key(prompt, task_type), result)
            return result

        errors.append(f"{model_name}: failed")

    return None


def _build_fallback_chain(active: str, task_type: TaskType) -> list[str]:
    preferred = TASK_ROUTES.get(task_type, TASK_ROUTES[TaskType.GENERAL])
    chain = [active]
    for m in preferred:
        if m != active and m not in chain:
            chain.append(m)
    for name in MODEL_REGISTRY:
        if name not in chain:
            chain.append(name)
    return chain


def _try_model(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    image: Any,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    try:
        if cfg.provider == "openrouter":
            return _query_openrouter(cfg, prompt, stream, system_override, max_tokens)
        elif cfg.provider == "openai":
            return _query_openai(
                cfg, prompt, stream, image, system_override, max_tokens
            )
        elif cfg.provider == "anthropic":
            return _query_anthropic(cfg, prompt, stream, system_override, max_tokens)
        elif cfg.provider == "google":
            return _query_google(
                cfg, prompt, stream, image, system_override, max_tokens
            )
        elif cfg.provider == "grok":
            return _query_grok(cfg, prompt, stream, system_override, max_tokens)
        elif cfg.provider in ("groq", "nvidia", "deepseek", "opencode"):
            return _query_openai_compat(
                cfg, prompt, stream, image, system_override, max_tokens
            )
        elif cfg.provider == "ollama":
            return _query_ollama(cfg, prompt, stream, system_override, max_tokens)
        elif cfg.provider == "llama_cpp":
            return _query_llamacpp(cfg, prompt, stream, system_override, max_tokens)
    except Exception:
        return None
    return None


def _query_openrouter(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    import requests

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None

    system = system_override or SYSTEM_PROMPT
    payload = {
        "model": cfg.model_id,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "stream": stream,
    }

    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
        stream=stream,
    )
    resp.raise_for_status()

    if stream:
        return _handle_stream_openai_style(resp)
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


def _query_openai(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    image: Any,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    try:
        from openai import OpenAI
    except ImportError:
        return None

    api_key = os.getenv(cfg.api_key_env) if cfg.api_key_env else None
    if not api_key:
        return None

    client = OpenAI(api_key=api_key)
    system = system_override or SYSTEM_PROMPT

    messages: list[dict] = [{"role": "system", "content": system}]
    if image is not None and "vision" in cfg.capabilities:
        import base64

        if isinstance(image, str):
            image_url = image
        else:
            import numpy as np
            from PIL import Image
            import io

            if isinstance(image, np.ndarray):
                pil_img = Image.fromarray(image)
            else:
                pil_img = image
            buf = io.BytesIO()
            pil_img.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            image_url = f"data:image/png;base64,{b64}"
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        )
    else:
        messages.append({"role": "user", "content": prompt})

    kwargs = {
        "model": cfg.model_id,
        "messages": messages,
        "max_tokens": max_tokens,
        "stream": stream,
    }
    resp = client.chat.completions.create(**kwargs)

    if stream:
        return _handle_stream_openai_sdk(resp)
    return resp.choices[0].message.content.strip()


def _query_anthropic(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    try:
        import anthropic
    except ImportError:
        return None

    api_key = os.getenv(cfg.api_key_env) if cfg.api_key_env else None
    if not api_key:
        return None

    client = anthropic.Anthropic(api_key=api_key)
    system = system_override or SYSTEM_PROMPT

    kwargs = {
        "model": cfg.model_id,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
        "stream": stream,
    }
    resp = client.messages.create(**kwargs)

    if stream:
        return _handle_stream_anthropic(resp)

    return resp.content[0].text.strip()


def _query_google(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    image: Any,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    try:
        import google.generativeai as genai
    except ImportError:
        return None

    api_key = os.getenv(cfg.api_key_env) if cfg.api_key_env else None
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        cfg.model_id,
        system_instruction=system_override or SYSTEM_PROMPT,
    )

    contents: Any = prompt
    if image is not None and "vision" in cfg.capabilities:
        contents = [prompt, image]

    kwargs = {"stream": stream} if stream else {}
    resp = model.generate_content(
        contents,
        generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens),
        **kwargs,
    )

    if stream:
        return _handle_stream_gemini(resp)
    return resp.text.strip()


def _query_grok(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    try:
        from openai import OpenAI
    except ImportError:
        return None

    api_key = os.getenv(cfg.api_key_env) if cfg.api_key_env else None
    if not api_key:
        return None

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )
    system = system_override or SYSTEM_PROMPT

    kwargs = {
        "model": cfg.model_id,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "stream": stream,
    }
    resp = client.chat.completions.create(**kwargs)

    if stream:
        return _handle_stream_openai_sdk(resp)
    return resp.choices[0].message.content.strip()


def _query_openai_compat(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    image: Any,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    try:
        from openai import OpenAI
    except ImportError:
        return None

    api_key = os.getenv(cfg.api_key_env) if cfg.api_key_env else None
    if not api_key:
        return None

    base_url = cfg.base_url or "https://api.openai.com/v1"
    client = OpenAI(api_key=api_key, base_url=base_url)
    system = system_override or SYSTEM_PROMPT

    messages: list[dict] = [{"role": "system", "content": system}]
    if image is not None and "vision" in cfg.capabilities:
        import base64

        if isinstance(image, str):
            image_url = image
        else:
            import numpy as np
            from PIL import Image
            import io

            if isinstance(image, np.ndarray):
                pil_img = Image.fromarray(image)
            else:
                pil_img = image
            buf = io.BytesIO()
            pil_img.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            image_url = f"data:image/png;base64,{b64}"
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        )
    else:
        messages.append({"role": "user", "content": prompt})

    kwargs = {
        "model": cfg.model_id,
        "messages": messages,
        "max_tokens": max_tokens,
        "stream": stream,
    }
    resp = client.chat.completions.create(**kwargs)

    if stream:
        return _handle_stream_openai_sdk(resp)
    return resp.choices[0].message.content.strip()


def _query_ollama(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    try:
        import ollama
    except ImportError:
        return _query_ollama_http(cfg, prompt, stream, system_override, max_tokens)

    system = system_override or SYSTEM_PROMPT
    kwargs = {
        "model": cfg.model_id,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "options": {"num_predict": max_tokens},
        "stream": stream,
    }
    resp = ollama.chat(**kwargs)

    if stream:
        return _handle_stream_ollama(resp)
    return resp["message"]["content"].strip()


def _query_ollama_http(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    import requests

    system = system_override or SYSTEM_PROMPT
    payload = {
        "model": cfg.model_id,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "options": {"num_predict": max_tokens},
        "stream": stream,
    }
    try:
        resp = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=30,
            stream=stream,
        )
        resp.raise_for_status()
    except requests.ConnectionError:
        return None

    if stream:
        return _handle_stream_ollama_http(resp)
    data = resp.json()
    return data["message"]["content"].strip()


def _query_llamacpp(
    cfg: ModelConfig,
    prompt: str,
    stream: bool,
    system_override: str | None,
    max_tokens: int,
) -> str | None:
    try:
        from llama_cpp import Llama
    except ImportError:
        return None

    model_path = os.getenv("LLAMACPP_MODEL_PATH", "")
    if not model_path:
        return None

    llm = Llama(
        model_path=model_path,
        n_ctx=cfg.context_window,
        verbose=False,
    )
    system = system_override or SYSTEM_PROMPT
    full_prompt = f"<s>[INST] <<SYS>>\n{system}\n<</SYS>>\n\n{prompt} [/INST]"

    kwargs = {
        "prompt": full_prompt,
        "max_tokens": max_tokens,
        "stream": stream,
        "echo": False,
    }
    resp = llm(**kwargs)

    if stream:
        return _handle_stream_llamacpp(resp)

    return resp["choices"][0]["text"].strip()


# --- Stream handlers ---


def _handle_stream_openai_style(resp) -> str:
    collected = []
    for line in resp.iter_lines():
        if line:
            decoded = line.decode("utf-8", errors="ignore")
            if decoded.startswith("data: "):
                import json

                try:
                    data = json.loads(decoded[6:])
                    token = (
                        data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    )
                    if token:
                        collected.append(token)
                        _emit_stream_token(token)
                except (json.JSONDecodeError, KeyError, IndexError):
                    pass
    return "".join(collected)


def _handle_stream_openai_sdk(resp) -> str:
    collected = []
    for chunk in resp:
        token = chunk.choices[0].delta.content or ""
        if token:
            collected.append(token)
            _emit_stream_token(token)
    return "".join(collected)


def _handle_stream_anthropic(resp) -> str:
    collected = []
    for event in resp:
        if event.type == "content_block_delta":
            token = event.delta.text or ""
            if token:
                collected.append(token)
                _emit_stream_token(token)
    return "".join(collected)


def _handle_stream_gemini(resp) -> str:
    collected = []
    for chunk in resp:
        if chunk.text:
            collected.append(chunk.text)
            _emit_stream_token(chunk.text)
    return "".join(collected)


def _handle_stream_ollama(resp) -> str:
    collected = []
    for chunk in resp:
        token = chunk.get("message", {}).get("content", "")
        if token:
            collected.append(token)
            _emit_stream_token(token)
    return "".join(collected)


def _handle_stream_ollama_http(resp) -> str:
    collected = []
    for line in resp.iter_lines():
        if line:
            import json

            try:
                data = json.loads(line.decode("utf-8", errors="ignore"))
                token = data.get("message", {}).get("content", "")
                if token:
                    collected.append(token)
                    _emit_stream_token(token)
                if data.get("done"):
                    break
            except json.JSONDecodeError:
                pass
    return "".join(collected)


def _handle_stream_llamacpp(resp) -> str:
    collected = []
    for chunk in resp:
        token = chunk["choices"][0]["text"]
        if token:
            collected.append(token)
            _emit_stream_token(token)
    return "".join(collected)


# --- Ollama manager ---


class OllamaManager:
    @staticmethod
    def list_models() -> list[dict]:
        try:
            import ollama

            return [
                {"name": m["name"], "size": m.get("size", 0)}
                for m in ollama.list()["models"]
            ]
        except ImportError:
            import requests

            try:
                resp = requests.get("http://localhost:11434/api/tags", timeout=5)
                resp.raise_for_status()
                return [
                    {"name": m["name"], "size": m.get("size", 0)}
                    for m in resp.json().get("models", [])
                ]
            except Exception:
                return []

    @staticmethod
    def pull_model(name: str) -> str:
        try:
            import ollama

            ollama.pull(name)
            return f"Model {name} downloaded successfully."
        except ImportError:
            import requests

            try:
                resp = requests.post(
                    "http://localhost:11434/api/pull",
                    json={"name": name},
                    stream=True,
                    timeout=300,
                )
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line:
                        _emit_stream_token(".")
                return f"Model {name} downloaded."
            except Exception as e:
                return f"Failed to download {name}: {e}"

    @staticmethod
    def delete_model(name: str) -> str:
        try:
            import ollama

            ollama.delete(name)
            return f"Model {name} deleted."
        except Exception as e:
            return f"Failed to delete {name}: {e}"


# --- LlamaCPP manager ---


class LlamaCPPManager:
    @staticmethod
    def get_model_path() -> str:
        return os.getenv("LLAMACPP_MODEL_PATH", "")

    @staticmethod
    def set_model_path(path: str):
        os.environ["LLAMACPP_MODEL_PATH"] = path

    @staticmethod
    def is_available() -> bool:
        if not os.getenv("LLAMACPP_MODEL_PATH"):
            return False
        import importlib.util

        return importlib.util.find_spec("llama_cpp") is not None


# --- Compatibility wrapper ---


def ask_llm(prompt: str, model: str | None = None) -> str:
    if model:
        old = get_active_model()
        set_active_model(model)
        result = query_llm(prompt, task_type=TaskType.GENERAL)
        set_active_model(old)
        return result or "Sorry, I couldn't process that request."
    result = query_llm(prompt, task_type=TaskType.GENERAL)
    return result or "Sorry, I couldn't process that request."
