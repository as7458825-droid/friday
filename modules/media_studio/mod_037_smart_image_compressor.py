import os
import glob

from PIL import Image


def compress_image(image_path: str, quality: int = 85) -> str:
    if not os.path.isfile(image_path):
        return f"File not found: {image_path}"

    img = Image.open(image_path)
    base, ext = os.path.splitext(image_path)
    output_path = f"{base}_compressed{ext or '.jpg'}"

    img.save(output_path, quality=quality, optimize=True)
    return output_path


def compress_all(input_folder: str, quality: int = 85) -> str:
    if not os.path.isdir(input_folder):
        return f"Folder not found: {input_folder}"

    count = 0
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.bmp"):
        for path in glob.glob(os.path.join(input_folder, ext)):
            compress_image(path, quality)
            count += 1

    return f"Compressed {count} images in {input_folder}"
