import numpy as np

try:
    from transformers import pipeline

    _detector = None

    def get_detector():
        global _detector
        if _detector is None:
            _detector = pipeline("object-detection", model="facebook/detr-resnet-50")
        return _detector

    HAS_DETR = True
except ImportError:
    HAS_DETR = False


def find_element(image: np.ndarray, prompt: str) -> list[dict]:
    if not HAS_DETR:
        return [
            {"error": "Install transformers and torch: pip install transformers torch"}
        ]

    from PIL import Image

    pil_image = Image.fromarray(image).convert("RGB")
    detector = get_detector()
    detections = detector(pil_image)

    prompt_lower = prompt.lower()
    results = []
    for det in detections:
        label = det["label"].lower()
        score = det["score"]
        if prompt_lower in label or label in prompt_lower:
            box = det["box"]
            results.append(
                {
                    "label": det["label"],
                    "score": round(score, 3),
                    "box": box,
                    "center": (box["xmin"] + box["xmax"]) // 2,
                    "center_y": (box["ymin"] + box["ymax"]) // 2,
                    "width": box["xmax"] - box["xmin"],
                    "height": box["ymax"] - box["ymin"],
                }
            )

    if not results:
        for det in detections[:3]:
            box = det["box"]
            results.append(
                {
                    "label": det["label"],
                    "score": round(det["score"], 3),
                    "box": box,
                    "center": (box["xmin"] + box["xmax"]) // 2,
                    "center_y": (box["ymin"] + box["ymax"]) // 2,
                    "width": box["xmax"] - box["xmin"],
                    "height": box["ymax"] - box["ymin"],
                }
            )

    return results
