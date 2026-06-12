import tkinter as tk


class OrbitalOrb:
    COLORS = {
        "idle": "#00ff88",
        "thinking": "#ffaa00",
        "error": "#ff0044",
        "listening": "#00aaff",
    }

    def __init__(self, parent, theme):
        self.theme = theme
        self.status = "idle"
        self.phase = 0.0

        self.frame = tk.Frame(parent, bg=theme.get("bg", "#0a0a1a"))
        self.canvas = tk.Canvas(
            self.frame,
            width=80,
            height=80,
            bg=theme.get("bg", "#0a0a1a"),
            highlightthickness=0,
        )
        self.canvas.pack()

        self._animate()

    def set_status(self, status: str):
        self.status = status if status in self.COLORS else "idle"

    def pulse(self):
        self.phase = 1.0

    def _animate(self):
        color = self.COLORS.get(self.status, "#00ff88")
        self.phase = max(0.0, self.phase - 0.05)

        cx = 40
        cy = 40
        r = 12 + 8 * self.phase

        self.canvas.delete("orb")
        self.canvas.create_oval(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            fill="",
            outline=color,
            width=3,
            tags="orb",
        )
        inner = max(2, r - 6)
        alpha = int(60 * (1 - self.phase * 0.5))
        self.canvas.create_oval(
            cx - inner,
            cy - inner,
            cx + inner,
            cy + inner,
            fill=self._hex_with_alpha(color, alpha),
            outline="",
            tags="orb",
        )

        self.frame.after(50, self._animate)

    @staticmethod
    def _hex_with_alpha(hex_color, alpha):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"#{r:02x}{g:02x}{b:02x}"
