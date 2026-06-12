import threading
import tkinter as tk

import psutil

from modules.hud.mod_002_telemetry_canvas import TelemetryPanel
from modules.hud.mod_003_orbital_orb import OrbitalOrb
from modules.hud.mod_005_embedded_terminal import TerminalPanel
from modules.hud.mod_006_whisper_mic_stream import MicIndicator
from modules.hud.mod_007_elevenlabs_synth import SpeechIndicator
from modules.hud.mod_009_hud_theme_matrix import ThemeManager
from modules.hud.mod_010_input_capsule import InputCapsule

HUD_INSTANCE = None
_hud_lock = threading.Lock()


class HUDApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FRIDAY HUD")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")
        self.root.configure(bg="black")
        self.root.geometry("380x600+50+50")

        self.theme = ThemeManager()
        self.bg_color = "#0a0a1a"
        self.fg_color = self.theme.get("primary", "#00fffff")

        self._build_ui()
        self._bind_shortcuts()
        self._start_updates()

    def _build_ui(self):
        container = tk.Frame(
            self.root,
            bg=self.bg_color,
            highlightthickness=1,
            highlightbackground=self.fg_color,
        )
        container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.orb = OrbitalOrb(container, self.theme)
        self.orb.frame.pack(pady=(8, 4))

        self.telemetry = TelemetryPanel(container, self.theme)
        self.telemetry.frame.pack(fill=tk.X, padx=6, pady=2)

        mic_row = tk.Frame(container, bg=self.bg_color)
        mic_row.pack(fill=tk.X, padx=6, pady=2)
        self.mic_indicator = MicIndicator(mic_row, self.theme)
        self.mic_indicator.frame.pack(side=tk.LEFT, padx=(0, 10))
        self.speech_indicator = SpeechIndicator(mic_row, self.theme)
        self.speech_indicator.frame.pack(side=tk.LEFT)

        self.terminal = TerminalPanel(container, self.theme)
        self.terminal.frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=2)

        self.input_capsule = InputCapsule(container, self.theme)
        self.input_capsule.frame.pack(fill=tk.X, padx=6, pady=(0, 6))

        self.root.bind("<ButtonPress-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._do_drag)

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _do_drag(self, event):
        x = self.root.winfo_x() + event.x - self._drag_x
        y = self.root.winfo_y() + event.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    def _bind_shortcuts(self):
        self.root.bind("<Control-Shift-Key-H>", lambda e: self.toggle_visible())
        self.root.bind("<Control-Shift-Key-T>", lambda e: self.toggle_topmost())
        self.root.bind("<Control-Shift-Key-R>", lambda e: self.root.geometry("+50+50"))

    def toggle_visible(self):
        self.root.withdraw() if self.root.state() == "normal" else self.root.deiconify()

    def toggle_topmost(self):
        current = self.root.attributes("-topmost")
        self.root.attributes("-topmost", not current)

    def _start_updates(self):
        self._update_stats()
        self.root.after(1000, self._start_updates)

    def _update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        self.telemetry.update(cpu, ram, disk)

    def log(self, message: str):
        self.terminal.append(message)
        self.orb.pulse()

    def set_mic_active(self, active: bool):
        self.mic_indicator.set_active(active)

    def set_speaking(self, speaking: bool):
        self.speech_indicator.set_speaking(speaking)

    def set_orb_status(self, status: str):
        self.orb.set_status(status)

    def run(self):
        self.root.mainloop()

    def stop(self):
        self.root.quit()


def launch_hud() -> HUDApp:
    global HUD_INSTANCE
    with _hud_lock:
        if HUD_INSTANCE is None:
            app = HUDApp()
            t = threading.Thread(target=app.run, daemon=True)
            t.start()
            HUD_INSTANCE = app
    return HUD_INSTANCE


def stop_hud():
    global HUD_INSTANCE
    with _hud_lock:
        if HUD_INSTANCE:
            HUD_INSTANCE.stop()
            HUD_INSTANCE = None


def log_message(msg: str):
    if HUD_INSTANCE:
        HUD_INSTANCE.log(msg)
