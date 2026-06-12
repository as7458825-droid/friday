import os
import tempfile


def generate(prompt: str, model: str = "veo") -> str:
    try:
        import requests
    except Exception:
        return "requests not available."
    urls = {
        "veo": "https://inference.sh/api/v1/veo",
        "seedance": "https://inference.sh/api/v1/seedance",
        "wan": "https://inference.sh/api/v1/wan",
    }
    url = urls.get(model, urls["veo"])
    try:
        r = requests.post(url, json={"prompt": prompt}, timeout=120)
        path = os.path.join(tempfile.gettempdir(), "friday_gen.mp4")
        with open(path, "wb") as f:
            f.write(r.content)
        os.startfile(path)
        return f"Video saved to {path}"
    except Exception as e:
        return f"Video error: {e}"


def image_to_video(image_path: str, prompt: str = "") -> str:
    return f"Animate {image_path} with prompt: {prompt or 'default'}"


def list_models() -> str:
    return "Models: veo, seedance, wan, happyhorse"
