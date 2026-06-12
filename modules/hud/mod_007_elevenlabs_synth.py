import tkinter as tk


class SpeechIndicator:
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
        self._speaking = False
        self._draw(False)

    def set_speaking(self, speaking: bool):
        if speaking != self._speaking:
            self._speaking = speaking
            self._draw(speaking)

    def _draw(self, speaking: bool):
        self.canvas.delete("spk")
        color = "#ff00ff" if speaking else "#333355"
        self.canvas.create_text(
            10, 10, text="♪", fill=color, font=("Segoe UI", 12), tags="spk"
        )
