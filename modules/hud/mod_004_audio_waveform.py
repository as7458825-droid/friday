import tkinter as tk


class WaveformDisplay:
    def __init__(self, parent, theme):
        self.frame = tk.Frame(parent, bg=theme.get("bg", "#0a0a1a"))
        self.canvas = tk.Canvas(
            self.frame, width=200, height=40, bg="#050510", highlightthickness=0
        )
        self.canvas.pack()
        self.points = [0] * 50
        self._animating = False

    def start(self):
        self._animating = True
        self._draw()

    def stop(self):
        self._animating = False

    def feed_sample(self, value: float):
        self.points.append(value)
        if len(self.points) > 50:
            self.points.pop(0)

    def _draw(self):
        if not self._animating:
            return
        self.canvas.delete("wav")
        w = 200
        h = 40
        w // 2
        cy = h // 2

        for i in range(len(self.points) - 1):
            x1 = i * 4
            x2 = (i + 1) * 4
            y1 = cy + self.points[i] * 15
            y2 = cy + self.points[i + 1] * 15
            self.canvas.create_line(x1, y1, x2, y2, fill="#00ffff", width=1, tags="wav")

        self.frame.after(50, self._draw)
