import tkinter as tk


class MicIndicator:
    def __init__(self, parent, theme):
        self.theme = theme
        self.frame = tk.Frame(parent, bg=theme.get("bg", "#0a0a1a"))
        self.canvas = tk.Canvas(
            self.frame,
            width=20,
            height=20,
            bg=theme.get("bg", "#0a0a1a"),
            highlightthickness=0,
        )
        self.canvas.pack()
        self._active = False
        self._draw(False)

    def set_active(self, active: bool):
        if active != self._active:
            self._active = active
            self._draw(active)

    def _draw(self, active: bool):
        self.canvas.delete("mic")
        color = "#00ff88" if active else "#333355"
        self.canvas.create_oval(2, 2, 18, 18, fill=color, outline="", tags="mic")
