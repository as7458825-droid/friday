import os
import glob

from PIL import Image


def add_watermark(
    input_folder: str, watermark_image: str, output_folder: str = "watermarked"
) -> str:
    if not os.path.isdir(input_folder):
        return f"Input folder not found: {input_folder}"
    if not os.path.isfile(watermark_image):
        return f"Watermark image not found: {watermark_image}"

    os.makedirs(output_folder, exist_ok=True)
    watermark = Image.open(watermark_image).convert("RGBA")

    count = 0
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.bmp"):
        for path in glob.glob(os.path.join(input_folder, ext)):
            img = Image.open(path).convert("RGBA")
            wm = watermark.copy()
            wm.thumbnail((img.width // 4, img.height // 4))

            x = img.width - wm.width - 10
            y = img.height - wm.height - 10
            img.paste(wm, (x, y), wm)

            out_path = os.path.join(output_folder, os.path.basename(path))
            img.convert("RGB").save(out_path, quality=95)
            count += 1

    return f"Watermarked {count} images in {output_folder}"
