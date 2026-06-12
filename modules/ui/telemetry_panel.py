import tkinter as tk
from tkinter import font as tkfont

import psutil


class Gauge(tk.Canvas):
    def __init__(self, parent, label: str, max_val: float = 100, **kwargs):
        self._size = kwargs.pop("size", 80)
        super().__init__(
            parent,
            width=self._size,
            height=self._size,
            bg=kwargs.get("bg", "#0d1117"),
            highlightthickness=0,
            **kwargs,
        )
        self.label = label
        self.max_val = max_val
        self._value = 0.0
        self._target = 0.0
        self._primary = "#00d4ff"
        self._secondary = "#ff00ff"
        self._draw()

    def set_primary(self, color: str):
        self._primary = color
        self._draw()

    def set_secondary(self, color: str):
        self._secondary = color

    def set_target(self, value: float):
        self._target = min(value, self.max_val)

    def animate(self):
        if abs(self._value - self._target) > 0.5:
            self._value += (self._target - self._value) * 0.15
            self._draw()
            return True
        return False

    def _draw(self):
        self.delete("all")
        cx = cy = self._size // 2
        r = self._size // 2 - 6
        angle = 360 * (self._value / self.max_val)
        self.create_arc(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            start=90,
            extent=-angle,
            outline=self._primary,
            width=4,
            style="arc",
        )
        self.create_arc(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            start=90,
            extent=0,
            outline="#30363d",
            width=4,
            style="arc",
        )
        self.create_text(
            cx,
            cy - 4,
            text=f"{int(self._value)}%",
            fill=self._primary,
            font=tkfont.Font(size=9, weight="bold"),
        )
        self.create_text(
            cx, cy + 12, text=self.label, fill="#8b949e", font=tkfont.Font(size=7)
        )


class TelemetryPanel(tk.Frame):
    def __init__(self, parent, theme):
        super().__init__(parent, bg=theme["bg"])
        self._theme = theme
        self._gauges: dict[str, Gauge] = {}
        self._build()

    def _build(self):
        title = tk.Label(
            self,
            text="SYSTEM TELEMETRY",
            bg=self._theme["bg"],
            fg="#8b949e",
            font=tkfont.Font(size=8, weight="bold"),
        )
        title.pack(anchor="w", padx=4)

        frame = tk.Frame(self, bg=self._theme["bg"])
        frame.pack(fill=tk.X, padx=2, pady=2)

        metrics = [("CPU", 100), ("RAM", 100), ("DISK", 100), ("NET", 100)]
        primary = self._theme.get("primary", "#00d4ff")
        for name, mx in metrics:
            g = Gauge(frame, name, mx, bg=self._theme["bg"])
            g.set_primary(primary)
            g.pack(side=tk.LEFT, padx=4, pady=2)
            self._gauges[name.lower()] = g

        self._bat_label = tk.Label(
            frame,
            text="BAT: N/A",
            bg=self._theme["bg"],
            fg="#8b949e",
            font=tkfont.Font(size=7),
        )
        self._bat_label.pack(side=tk.LEFT, padx=6)

    def update(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        net = psutil.net_io_counters()
        net_pct = min(100, (net.bytes_sent + net.bytes_recv) / 1048576)

        self._gauges["cpu"].set_target(cpu)
        self._gauges["ram"].set_target(ram)
        self._gauges["disk"].set_target(disk)
        self._gauges["net"].set_target(net_pct)

        battery = psutil.sensors_battery()
        if battery:
            status = "⚡" if battery.power_plugged else "🔋"
            self._bat_label.config(text=f"BAT: {int(battery.percent)}% {status}")

        for g in self._gauges.values():
            g.animate()

    def set_primary(self, color: str):
        for g in self._gauges.values():
            g.set_primary(color)
