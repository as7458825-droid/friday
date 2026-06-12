import numpy as np
from PIL import Image

try:
    from transformers import pipeline

    _captioner = None

    def get_captioner():
        global _captioner
        if _captioner is None:
            _captioner = pipeline(
                "image-to-text", model="Salesforce/blip-image-captioning-base"
            )
        return _captioner

    HAS_BLIP = True
except ImportError:
    HAS_BLIP = False


def describe_image(image_source: str | np.ndarray) -> str:
    if isinstance(image_source, str):
        image = Image.open(image_source).convert("RGB")
    elif isinstance(image_source, np.ndarray):
        image = Image.fromarray(image_source).convert("RGB")
    else:
        return "Invalid image source."

    try:
        from config import FEATURES

        if FEATURES.get("llm_vision_models") or FEATURES.get("real_ai_brain"):
            from modules.llm.llm_manager import query_llm, TaskType

            result = query_llm(
                "Describe this image in detail. What do you see?",
                task_type=TaskType.VISION,
                image=image,
            )
            if result:
                return result
    except Exception:
        pass

    if not HAS_BLIP:
        return "Image description unavailable. Install transformers and torch: pip install transformers torch"

    try:
        captioner = get_captioner()
        result = captioner(image)
        return result[0]["generated_text"]
    except Exception as e:
        return f"Image description failed: {e}"


def describe_screen(np_array: np.ndarray) -> str:
    return describe_image(np_array)
