import tkinter as tk
import math
import threading
import time

class DummyVoiceEngine:
    def __init__(self):
        pass
    def speak(self, text, language=None):
        print(f"Speaking: {text}")
        time.sleep(2)
    def listen(self, language=None):
        print("Listening...")
        time.sleep(3)
        return "hello"

def get_language():
    return "en"

def handle_command(cmd, voice):
    print(f"Handling: {cmd}")
    voice.speak("I processed your command successfully.")
    return True

class NovaOrb(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FRIDAY - Nova AI")

        # 1. TRANSPARENT FLOATING WINDOW
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "#010101")
        self.config(bg="#010101")

        # Position (Bottom Right)
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"300x400+{screen_w - 320}+{screen_h - 450}")

        self.canvas = tk.Canvas(
            self, width=300, height=400, bg="#010101", highlightthickness=0
        )
        self.canvas.pack()

        # State & variables
        self._running = True
        self._state = "idle"  # idle, listening, thinking, speaking
        self._last_msg = "Hello Master! I am your FRIDAY."
        self.angle_outer = 0.0
        self.angle_inner = 0.0
        self.pulse = 0.0
        self.audio_amplitude = 0.0

        self._bind_events()
        self._animate()

        # Start Voice Logic Thread
        self.after(1000, self._start_logic)

    def _bind_events(self):
        self.canvas.bind("<Button-1>", self._start_move)
        self.canvas.bind("<B1-Motion>", self._do_move)
        self.canvas.bind("<Double-Button-1>", lambda e: self.destroy())

    def _start_move(self, event):
        self.x = event.x
        self.y = event.y

    def _do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def destroy(self):
        self._running = False
        super().destroy()

    def update_state(self, state=None, msg=None, amplitude=0.0):
        if state:
            self._state = state
        if msg:
            self._last_msg = msg
        self.audio_amplitude = amplitude

    def _draw_ui(self):
        self.canvas.delete("all")
        cx, cy = 150, 150

        # Pulsing calculations
        self.pulse += 0.08
        pulse_val = (math.sin(self.pulse) + 1.0) / 2.0  # 0 to 1

        # Select color based on state
        if self._state == "listening":
            color = "#00ff95"      # Bright neon green
            self.angle_outer += 0.08
            self.angle_inner -= 0.12
            self.audio_amplitude = 0.5 + pulse_val * 0.5
        elif self._state == "thinking":
            color = "#ff00e1"      # Flashing magenta
            self.angle_outer += 0.20
            self.angle_inner -= 0.25
            self.audio_amplitude = 0.2
        elif self._state == "speaking":
            color = "#ff7700"      # Pulsing neon orange
            self.angle_outer += 0.04
            self.angle_inner -= 0.06
            self.audio_amplitude = 0.6 + math.sin(self.pulse * 3) * 0.4
        else:  # idle
            color = "#00f2ff"      # Tech cyan
            self.angle_outer += 0.02
            self.angle_inner -= 0.03
            self.audio_amplitude = 0.0

        # Draw Glow Aura (concentric faint circles)
        for r_aura in (100, 110, 120):
            self.canvas.create_oval(
                cx - r_aura, cy - r_aura, cx + r_aura, cy + r_aura,
                outline=color, width=1, dash=(2, 12)
            )

        # Draw Outer Ring (Rotating Arcs)
        r_outer = 80 + (pulse_val * 4 if self._state == "speaking" else 0)
        for i in range(3):
            start_angle = math.degrees(self.angle_outer) + (i * 120)
            self.canvas.create_arc(
                cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer,
                start=start_angle, extent=70, style="arc", outline=color, width=2.5
            )

        # Draw Inner Ring (Rotating Arcs)
        r_inner = 55 - (pulse_val * 3 if self._state == "listening" else 0)
        for i in range(4):
            start_angle = math.degrees(self.angle_inner) + (i * 90)
            self.canvas.create_arc(
                cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner,
                start=start_angle, extent=45, style="arc", outline=color, width=1.5
            )

        # Draw Audio Waveform Visualizer lines/particles (reacting to audio amplitude)
        if self.audio_amplitude > 0.05:
            num_bars = 12
            for i in range(num_bars):
                a = i * (2 * math.pi / num_bars) + (self.angle_outer * 0.5)
                # Randomize height slightly for natural audio wave look
                h_val = self.audio_amplitude * (15.0 + math.sin(self.pulse * 4 + i) * 10.0)
                r1 = r_inner + 5
                r2 = r1 + h_val
                x1 = cx + math.cos(a) * r1
                y1 = cy + math.sin(a) * r1
                x2 = cx + math.cos(a) * r2
                y2 = cy + math.sin(a) * r2
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

        # Draw Center Core
        r_core = 24 + (pulse_val * 5 if self._state in ("speaking", "listening") else pulse_val * 2)
        # Inner core glow outline
        self.canvas.create_oval(
            cx - r_core, cy - r_core, cx + r_core, cy + r_core,
            fill=color, outline=""
        )
        # Central bright white core
        r_white = r_core // 2
        self.canvas.create_oval(
            cx - r_white, cy - r_white, cx + r_white, cy + r_white,
            fill="#ffffff", outline=""
        )

        # Draw State Label
        self.canvas.create_text(
            150, 260, text=self._state.upper(), fill=color, font=("Consolas", 10, "bold")
        )

        # Draw Last Msg Bubble
        if self._last_msg:
            # Wrap text to 35 chars
            wrapped = []
            words = self._last_msg.split()
            current_line = []
            current_len = 0
            for word in words:
                if current_len + len(word) + 1 > 35:
                    wrapped.append(" ".join(current_line))
                    current_line = [word]
                    current_len = len(word)
                else:
                    current_line.append(word)
                    current_len += len(word) + 1
            if current_line:
                wrapped.append(" ".join(current_line))

            display_lines = wrapped[:3]
            if len(wrapped) > 3:
                display_lines[-1] = display_lines[-1][:32] + "..."
            display_text = "\n".join(display_lines)

            # Draw background panel for text
            self.canvas.create_rectangle(
                15, 290, 285, 385,
                fill="#111111", outline=color, width=1
            )
            self.canvas.create_text(
                150, 338, text=display_text, fill="#ffffff",
                font=("Inter", 9, "italic"), justify="center", width=250
            )

    def _animate(self):
        try:
            self._draw_ui()
        except Exception:
            pass
        delay = 40 if self._state == "thinking" else 50
        if self._running:
            self.after(delay, self._animate)

    def _start_logic(self):
        def loop():
            # Initialize VoiceEngine in thread
            voice_engine = DummyVoiceEngine()

            class NovaVoice:
                def __init__(self, owner, original):
                    self.owner = owner
                    self.original = original

                def speak(self, msg, lang=None):
                    self.owner.after(0, lambda: self.owner.update_state(state="speaking", msg=msg))
                    if self.original:
                        self.original.speak(msg, lang)
                    self.owner.after(0, lambda: self.owner.update_state(state="idle"))

                def listen(self, lang=None):
                    self.owner.after(0, lambda: self.owner.update_state(state="listening", msg="Listening..."))
                    res = self.original.listen(lang)
                    if res:
                        self.owner.after(0, lambda: self.owner.update_state(state="thinking", msg=f"You: {res}"))
                    else:
                        self.owner.after(0, lambda: self.owner.update_state(state="idle"))
                    return res

                def get_greeting(self):
                    return "Hello"

            self.after(0, lambda: self.update_state(msg="System Ready, Master!"))
            nova_voice = NovaVoice(self, voice_engine)

            # Speak startup greeting
            cur_lang = get_language() or "en"
            nova_voice.speak("Nova system online. Ready for your commands.", cur_lang)

            # Run loop for 2 cycles then exit in test
            for _ in range(2):
                if not self._running:
                    break
                try:
                    cur_lang = get_language() or "en"
                    cmd = nova_voice.listen(cur_lang)
                    if cmd:
                        self.after(0, lambda: self.update_state(state="thinking"))
                        cont = handle_command(cmd, nova_voice)
                        if not cont:
                            self.after(0, lambda: self.destroy())
                            break
                    else:
                        time.sleep(0.2)
                except Exception as ex:
                    print(f"Exception: {ex}")
                    time.sleep(1)
            
            # Close window after test completes
            print("Test complete, closing window...")
            self.after(0, lambda: self.destroy())

        threading.Thread(target=loop, daemon=True).start()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = NovaOrb()
    app.run()
