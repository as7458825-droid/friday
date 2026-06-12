import json
import os

ACCENT_COLORS = {
    "cyan": {
        "primary": "#00f2ff",
        "secondary": "#7000ff",
        "bg": "#060900",
        "card": "#0d1117",
        "text": "#ffffff",
        "glow": "#00f2ff33",
    },
    "magenta": {
        "primary": "#ff00e1",
        "secondary": "#00f2ff",
        "bg": "#060900",
        "card": "#0d1117",
        "text": "#ffffff",
        "glow": "#ff00e133",
    },
    "gold": {
        "primary": "#ffcc00",
        "secondary": "#ff4400",
        "bg": "#060900",
        "card": "#0d1117",
        "text": "#ffffff",
        "glow": "#ffcc0033",
    },
    "green": {
        "primary": "#00ff95",
        "secondary": "#00d4ff",
        "bg": "#060900",
        "card": "#0d1117",
        "text": "#ffffff",
        "glow": "#00ff9533",
    },
    "red": {
        "primary": "#ff2e2e",
        "secondary": "#ffaa00",
        "bg": "#060900",
        "card": "#0d1117",
        "text": "#ffffff",
        "glow": "#ff2e2e33",
    },
    "blue": {
        "primary": "#2e86ff",
        "secondary": "#00ffea",
        "bg": "#060900",
        "card": "#0d1117",
        "text": "#ffffff",
        "glow": "#2e86ff33",
    },
}

LIGHT_OVERRIDES = {
    "bg": "#f0f2f5",
    "card": "#ffffff",
    "text": "#1f2328",
}

CONFIG_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "ui_theme.json"
)


def _load_config() -> dict:
    if os.path.isfile(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_config(data: dict):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


class UIFridayTheme:
    def __init__(self):
        cfg = _load_config()
        self._dark = cfg.get("dark_mode", True)
        self._accent = cfg.get("accent_color", "cyan")
        self._callbacks: list = []

    @property
    def is_dark(self) -> bool:
        return self._dark

    @is_dark.setter
    def is_dark(self, value: bool):
        self._dark = value
        _save_config({"dark_mode": value, "accent_color": self._accent})
        self._notify()

    @property
    def accent(self) -> str:
        return self._accent

    @accent.setter
    def accent(self, value: str):
        if value in ACCENT_COLORS:
            self._accent = value
            _save_config({"dark_mode": self._dark, "accent_color": value})
            self._notify()

    def get_colors(self) -> dict:
        colors = ACCENT_COLORS.get(self._accent, ACCENT_COLORS["cyan"]).copy()
        if not self._dark:
            colors.update(LIGHT_OVERRIDES)
            colors["primary"] = ACCENT_COLORS[self._accent]["primary"]
            colors["secondary"] = ACCENT_COLORS[self._accent]["secondary"]
        return colors

    def get_accent_names(self) -> list[str]:
        return list(ACCENT_COLORS.keys())

    def bind(self, callback):
        self._callbacks.append(callback)

    def unbind(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _notify(self):
        for cb in self._callbacks:
            try:
                cb(self)
            except Exception:
                pass
