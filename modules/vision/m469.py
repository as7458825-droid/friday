import numpy as np
from PIL import Image, ImageDraw


def overlay_boxes(
    image: np.ndarray, detections: list[dict], output_path: str = "detection_output.png"
) -> str:
    pil_image = Image.fromarray(image).convert("RGB")
    draw = ImageDraw.Draw(pil_image)

    for det in detections:
        if "box" not in det:
            continue
        box = det["box"]
        label = det.get("label", "object")
        score = det.get("score", 0)

        x1, y1 = box["xmin"], box["ymin"]
        x2, y2 = box["xmax"], box["ymax"]
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1 - 12), f"{label} {score:.2f}", fill="red")

    pil_image.save(output_path)
    return output_path


def draw_debug_grid(image: np.ndarray, output_path: str = "debug_grid.png") -> str:
    pil_image = Image.fromarray(image).convert("RGB")
    pil_image.save(output_path)
    return output_path
