import os
import sys
import threading
import tkinter as tk
from PIL import Image, ImageTk

# Adjusting to the new structure
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class AnimeAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FRIDAY - Anime Companion")

        # 1. TRANSPARENT FLOATING WINDOW
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "#010101")
        self.config(bg="#010101")

        # Position (Bottom Right)
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"400x500+{screen_w - 420}+{screen_h - 550}")

        self.canvas = tk.Canvas(
            self, width=400, height=500, bg="#010101", highlightthickness=0
        )
        self.canvas.pack()

        # 2. STATE & ASSETS
        self._running = True
        self._thinking = False
        self._mood = "neutral"
        self._last_msg = "Hello Master! I am your FRIDAY."

        # Load Anime Girl GIF
        self.asset_path = os.path.join(PROJECT_ROOT, "data/assets/anime/idle.gi")
        if not os.path.exists(self.asset_path):
            # Fallback to a simple circle if gif missing
            self._has_gif = False
        else:
            self._has_gif = True
            self.gif_frames = []
            self._load_gif()

        self._bind_events()
        self._animate()

        # Start Voice Logic
        self.after(1000, self._start_logic)

    def _load_gif(self):
        try:
            img = Image.open(self.asset_path)
            for i in range(getattr(img, "n_frames", 1)):
                img.seek(i)
                frame = img.convert("RGBA").resize((300, 400), Image.LANCZOS)
                self.gif_frames.append(ImageTk.PhotoImage(frame))
            self.current_frame = 0
        except Exception as e:
            print(f"GIF Load Error: {e}")
            self._has_gif = False

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

    def _draw_ui(self):
        self.canvas.delete("ui")
        cx, cy = 200, 250

        # 3. DRAW ANIME CHARACTER
        if self._has_gif:
            self.canvas.create_image(
                cx, cy, image=self.gif_frames[self.current_frame], tags="ui"
            )
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        else:
            # Fallback Orb
            self.canvas.create_oval(
                cx - 100, cy - 100, cx + 100, cy + 100, fill="#00f2ff", tags="ui"
            )

        # 4. MOOD SYNC AURA
        aura_color = "#00f2ff"  # Neutral/Cyan
        if self._mood == "happy":
            aura_color = "#00ff95"  # Green
        if self._mood == "sad":
            aura_color = "#ff2e2e"  # Red
        if self._thinking:
            aura_color = "#ff00e1"  # Magenta

        self.canvas.create_oval(
            cx - 150,
            cy - 200,
            cx + 150,
            cy + 200,
            outline=aura_color,
            width=2,
            stipple="gray25",
            tags="ui",
        )

        # 5. KAWAII SPEECH BUBBLE
        if self._last_msg:
            msg = (
                self._last_msg[:80] + "..."
                if len(self._last_msg) > 80
                else self._last_msg
            )
            self.canvas.create_rectangle(
                20,
                420,
                380,
                490,
                fill="#111111",
                outline=aura_color,
                width=1,
                tags="ui",
            )
            self.canvas.create_text(
                200,
                455,
                text=msg,
                fill="#ffffff",
                font=("Inter", 10, "italic"),
                width=340,
                tags="ui",
            )

    def _animate(self):
        self._draw_ui()
        delay = 50 if not self._thinking else 30
        if self._running:
            self.after(delay, self._animate)

    def update_state(self, msg=None, mood="neutral", thinking=False):
        if msg:
            self._last_msg = msg
        self._mood = mood
        self._thinking = thinking

    def _start_logic(self):
        def loop():
            from mainbackup import handle_command, detect_mood
            from core.voice import VoiceEngine

            voice_engine = VoiceEngine(female_voice=True)

            class AnimeVoice:
                def __init__(self, owner, original):
                    self.owner = owner
                    self.original = original

                def speak(self, msg, lang="en"):
                    mood = detect_mood(msg)
                    self.owner.after(
                        0, lambda: self.owner.update_state(msg=msg, mood=mood)
                    )
                    if self.original:
                        self.original.speak(msg, lang)

                def listen(self):
                    return None

                def get_greeting(self):
                    return "Hello"

            self.after(0, lambda: self.update_state(msg="System Ready, Master!"))

            while self._running:
                cmd = voice_engine.listen()
                if cmd:
                    mood = detect_mood(cmd)
                    self.after(
                        0,
                        lambda: self.update_state(
                            msg=f"You: {cmd}", mood=mood, thinking=True
                        ),
                    )
                    try:
                        handle_command(cmd, AnimeVoice(self, voice_engine))
                    except Exception:
                        pass
                self.after(0, lambda: self.update_state(thinking=False))

        threading.Thread(target=loop, daemon=True).start()

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = AnimeAssistant()
    app.run()
