import tkinter as tk


class TelemetryPanel:
    def __init__(self, parent, theme):
        self.theme = theme
        self.frame = tk.Frame(parent, bg=theme.get("bg", "#0a0a1a"))

        self.cpu_bar = self._bar("CPU")
        self.ram_bar = self._bar("RAM")
        self.disk_bar = self._bar("DISK")

    def _bar(self, label):
        row = tk.Frame(self.frame, bg=self.frame["bg"])
        row.pack(fill=tk.X, pady=1)

        lbl = tk.Label(
            row,
            text=label,
            width=5,
            anchor="w",
            bg=row["bg"],
            fg=self.theme.get("primary", "#00ffff"),
            font=("Consolas", 8),
        )
        lbl.pack(side=tk.LEFT)

        canvas = tk.Canvas(
            row, width=200, height=14, bg="#111122", highlightthickness=0
        )
        canvas.pack(side=tk.LEFT, padx=4)

        val = tk.Label(
            row,
            text="0%",
            width=5,
            anchor="e",
            bg=row["bg"],
            fg=self.theme.get("secondary", "#ff00ff"),
            font=("Consolas", 8),
        )
        val.pack(side=tk.LEFT)

        return {"canvas": canvas, "value": val, "bar": None}

    def update(self, cpu, ram, disk):
        self._draw_bar("CPU", cpu)
        self._draw_bar("RAM", ram)
        self._draw_bar("DISK", disk)

    def _draw_bar(self, name, percent):
        bar = (
            self.cpu_bar
            if name == "CPU"
            else self.ram_bar
            if name == "RAM"
            else self.disk_bar
        )
        c = bar["canvas"]
        c.delete("all")
        w = 200
        h = 14
        fill = int(w * percent / 100)
        color = "#00ff88" if percent < 60 else "#ffaa00" if percent < 85 else "#ff0044"
        c.create_rectangle(0, 0, fill, h, fill=color, outline="")
        c.create_rectangle(fill, 0, w, h, fill="#111122", outline="")
        bar["value"].config(text=f"{int(percent)}%")
