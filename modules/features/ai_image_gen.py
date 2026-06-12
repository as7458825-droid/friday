import os
import tempfile


def generate(prompt: str, model: str = "flux") -> str:
    try:
        import requests
    except Exception:
        return "requests not available."
    if model == "flux":
        url = "https://inference.sh/api/v1/flux"
    elif model == "grok":
        url = "https://inference.sh/api/v1/grok-imagine"
    elif model == "gemini":
        url = "https://inference.sh/api/v1/gemini-image"
    else:
        url = "https://inference.sh/api/v1/flux"
    try:
        r = requests.post(url, json={"prompt": prompt}, timeout=60)
        path = os.path.join(tempfile.gettempdir(), "friday_gen.png")
        with open(path, "wb") as f:
            f.write(r.content)
        os.startfile(path)
        return f"Image saved to {path}"
    except Exception as e:
        return f"Generation error: {e}"


def edit_image(prompt: str, image_path: str = "") -> str:
    return f"Edit: {prompt} on {image_path or 'clipboard'}"


def upscale(image_path: str = "") -> str:
    return f"Upscale: {image_path or 'last image'}"


def list_models() -> str:
    return "Models: flux, grok, gemini, dall-e"
