import tkinter as tk
import math


class HolographicPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FRIDAY Pet")

        # Make window transparent and always on top
        self.root.overrideredirect(True)  # Remove window borders
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#000001")  # Black as transparent
        self.root.config(bg="#000001")

        # Position at bottom right
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"200x200+{screen_width - 220}+{screen_height - 250}")

        self.canvas = tk.Canvas(
            self.root, width=200, height=200, bg="#000001", highlightthickness=0
        )
        self.canvas.pack()

        self.angle = 0
        self.pulse = 0
        self._animate()

    def _animate(self):
        self.canvas.delete("all")

        # Pulsing effect
        self.pulse += 0.1
        pulse_val = (math.sin(self.pulse) + 1) / 2  # 0 to 1

        # Outer Ring
        self.angle += 0.05
        cx, cy = 100, 100
        r_outer = 60 + pulse_val * 5

        self.canvas.create_oval(
            cx - r_outer,
            cy - r_outer,
            cx + r_outer,
            cy + r_outer,
            outline="#00d2ff",
            width=2,
            dash=(10, 5),
        )

        # Rotating segments
        for i in range(3):
            a = self.angle + (i * (2 * math.pi / 3))
            x = cx + math.cos(a) * r_outer
            y = cy + math.sin(a) * r_outer
            self.canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5, fill="#00d2ff", outline=""
            )

        # Inner Core
        r_inner = 30 + pulse_val * 10
        self.canvas.create_oval(
            cx - r_inner,
            cy - r_inner,
            cx + r_inner,
            cy + r_inner,
            fill="#00d2ff",
            outline="",
            stipple="gray50" if pulse_val > 0.5 else "",
        )

        # Glow text
        self.canvas.create_text(
            100, 180, text="FRIDAY CORE", fill="#00d2ff", font=("Consolas", 8, "bold")
        )

        self.root.after(30, self._animate)

    def run(self):
        # Allow dragging
        self.canvas.bind("<Button-1>", self._start_move)
        self.canvas.bind("<B1-Motion>", self._do_move)
        self.root.mainloop()

    def _start_move(self, event):
        self.x = event.x
        self.y = event.y

    def _do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    pet = HolographicPet()
    pet.run()
