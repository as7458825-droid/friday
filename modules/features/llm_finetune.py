import json
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "finetuned_models")


def _ensure_dir():
    os.makedirs(MODEL_DIR, exist_ok=True)


def prepare_data(output: str = "finetune_data.jsonl") -> str:
    try:
        from modules.memory.vector_store import get_all_conversations

        conversations = get_all_conversations()
    except Exception:
        return "Could not load conversations from memory."
    if not conversations:
        return "No conversation data available."
    path = os.path.join(MODEL_DIR, output)
    with open(path, "w", encoding="utf-8") as f:
        for conv in conversations[-1000:]:
            f.write(json.dumps({"text": conv}) + "\n")
    return f"Prepared {min(len(conversations), 1000)} conversations for fine-tuning."


def list_models() -> str:
    _ensure_dir()
    models = [
        d for d in os.listdir(MODEL_DIR) if os.path.isdir(os.path.join(MODEL_DIR, d))
    ]
    if not models:
        return "No fine-tuned models. Run prepare_data first."
    return "Models: " + ", ".join(models)


def get_status() -> str:
    _ensure_dir()
    models = [
        d for d in os.listdir(MODEL_DIR) if os.path.isdir(os.path.join(MODEL_DIR, d))
    ]
    return f"{len(models)} fine-tuned models. Data dir: {MODEL_DIR}"
