import os

import cv2
import numpy as np


def apply_lut(image_path: str, preset: str = "warm", output_path: str = None) -> str:
    if not os.path.isfile(image_path):
        return f"File not found: {image_path}"

    img = cv2.imread(image_path)
    if img is None:
        return "Could not read image."

    presets = {
        "warm": (1.1, 1.0, 0.9),
        "cool": (0.9, 1.0, 1.1),
        "vintage": (0.8, 0.9, 1.0),
        "vivid": (1.2, 1.1, 1.0),
    }

    factors = presets.get(preset.lower(), (1.0, 1.0, 1.0))
    lut = np.zeros((256, 3), dtype=np.uint8)
    for i in range(256):
        lut[i] = [
            min(int(i * factors[2]), 255),
            min(int(i * factors[1]), 255),
            min(int(i * factors[0]), 255),
        ]

    result = cv2.LUT(img, lut)

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_{preset}{ext}"

    cv2.imwrite(output_path, result)
    return output_path
