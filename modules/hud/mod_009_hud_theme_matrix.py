THEMES = {
    "cyan": {"primary": "#00ffff", "secondary": "#ff00ff", "bg": "#0a0a1a"},
    "magenta": {"primary": "#ff00ff", "secondary": "#00ffff", "bg": "#1a0a1a"},
    "gold": {"primary": "#ffd700", "secondary": "#ff4500", "bg": "#1a1400"},
    "green": {"primary": "#00ff88", "secondary": "#00aaf", "bg": "#0a1a0a"},
    "red": {"primary": "#ff0044", "secondary": "#ff8800", "bg": "#1a0a0a"},
    "blue": {"primary": "#4488f", "secondary": "#00ffcc", "bg": "#0a0a1a"},
}


class ThemeManager:
    def __init__(self, initial: str = "cyan"):
        self._current = initial
        self._colors = THEMES.get(initial, THEMES["cyan"])

    def get(self, key: str, default: str = "#00fffff") -> str:
        return self._colors.get(key, default)

    def set_theme(self, name: str) -> bool:
        if name.lower() in THEMES:
            self._current = name.lower()
            self._colors = THEMES[self._current]
            return True
        return False

    def get_theme_names(self) -> list[str]:
        return list(THEMES.keys())

    def get_current(self) -> str:
        return self._current
