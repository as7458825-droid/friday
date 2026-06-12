"""
FRIDAY — Chat UI Window
Standalone chat interface using customtkinter (tkinter fallback).
Displays conversation history, accepts text input, and routes commands
through the same handle_command() as the voice system.
"""

import os
import queue
import sys
import threading
import time
from datetime import datetime

from config import FEATURES

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(PROJECT_ROOT, "config.py")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

_HAS_MULTI = FEATURES.get("multi_language", False)
if _HAS_MULTI:
    try:
        from modules.multilingual.translator import (
            translate_text,
            detect_language,
            get_supported_languages,
            get_recognition_locale,
        )
        from core.language import set_language as _set_lang

        _LANG_MAP = get_supported_languages()
    except Exception:
        _HAS_MULTI = False

# ---------------------------------------------------------------------------
# TextVoice — captures speak() calls as text instead of playing audio
# ---------------------------------------------------------------------------


class TextVoice:
    """Duck‑typed replacement for VoiceEngine that buffers speech as text."""

    def __init__(self):
        self._responses: queue.Queue[str] = queue.Queue()

    def speak(self, text: str) -> None:
        self._responses.put(text)

    def listen(self) -> str | None:
        return None

    def get_greeting(self) -> str:
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        return "Good evening"

    def get_response(self, timeout: float = 2.0) -> str | None:
        try:
            return self._responses.get(timeout=timeout)
        except queue.Empty:
            return None

    def drain(self) -> list[str]:
        msgs = []
        while not self._responses.empty():
            try:
                msgs.append(self._responses.get_nowait())
            except queue.Empty:
                break
        return msgs


# ---------------------------------------------------------------------------
# Chat Window
# ---------------------------------------------------------------------------

_CHAT_WINDOW = None
_WINDOW_LOCK = threading.Lock()


def _import_tk():
    """Return customtkinter if available, else tkinter."""
    try:
        import customtkinter as ctk

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        return ctk
    except ImportError:
        import tkinter as tk
        import tkinter.scrolledtext as st

        tk.ScrolledText = st.ScrolledText
        return tk


def show_chat():
    """Launch the chat window (thread‑safe singleton)."""
    global _CHAT_WINDOW
    with _WINDOW_LOCK:
        if _CHAT_WINDOW is not None and _CHAT_WINDOW.is_alive():
            try:
                _CHAT_WINDOW.window.deiconify()
                _CHAT_WINDOW.window.lift()
            except Exception:
                pass
            return
        _CHAT_WINDOW = ChatWindow()


class ChatWindow:
    def __init__(self):
        self.tk = _import_tk()
        self.window = self.tk.CTk() if hasattr(self.tk, "CTk") else self.tk.Tk()
        self.voice = TextVoice()
        self._build_ui()
        self._running = True
        self._poll_interval = 200

        from mainbackup import handle_command

        self._handle_command = handle_command

        self._start_poller()
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self.window.mainloop()

    def is_alive(self) -> bool:
        return self._running

    def _build_ui(self):
        w = self.window
        is_ctk = hasattr(self.tk, "CTk")
        bg = "#1a1a2e"
        text_bg = "#0d0d1a"
        text_fg = "#e0e0e0"

        if is_ctk:
            w.title("FRIDAY Ultra — Chat")
            w.geometry("740x540+100+100")
            w.configure(fg_color=bg)

            # Language selector toolbar
            toolbar = self.tk.CTkFrame(w, fg_color="#12122a", height=36)
            toolbar.pack(fill="x", padx=8, pady=(6, 0))

            self.tk.CTkLabel(
                toolbar, text="Language:", font=("Segoe UI", 11), text_color="#888"
            ).pack(side="left", padx=(6, 4))
            self._lang_var = self.tk.StringVar(value="English")
            lang_names = sorted(_LANG_MAP.values()) if _HAS_MULTI else ["English"]
            self._lang_menu = self.tk.CTkOptionMenu(
                toolbar,
                values=lang_names,
                variable=self._lang_var,
                font=("Segoe UI", 11),
                command=self._on_language_change,
                fg_color="#1a1a3e",
                button_color="#2a2a5e",
            )
            self._lang_menu.pack(side="left", padx=(0, 10))

            self.chat_area = self.tk.CTkTextbox(
                w,
                wrap="word",
                font=("Segoe UI", 12),
                fg_color=text_bg,
                text_color=text_fg,
                border_width=0,
                state="disabled",
            )
            self.chat_area.pack(fill="both", expand=True, padx=8, pady=(8, 4))

            input_frame = self.tk.CTkFrame(w, fg_color=bg)
            input_frame.pack(fill="x", padx=8, pady=(0, 8))

            self.input_box = self.tk.CTkEntry(
                input_frame,
                font=("Segoe UI", 13),
                fg_color=text_bg,
                text_color=text_fg,
                placeholder_text="Type a message…",
            )
            self.input_box.pack(side="left", fill="x", expand=True, padx=(0, 6))
            self.input_box.bind("<Return>", lambda e: self._send())

            self.send_btn = self.tk.CTkButton(
                input_frame,
                text="Send",
                width=80,
                fg_color="#0a84f",
                hover_color="#0066cc",
                command=self._send,
            )
            self.send_btn.pack(side="left", padx=(0, 4))

            self.voice_btn = self.tk.CTkButton(
                input_frame,
                text="🎤",
                width=40,
                fg_color="#2a2a4a",
                hover_color="#3a3a5a",
                command=self._voice_input,
            )
            self.voice_btn.pack(side="left", padx=(0, 4))

            self.clear_btn = self.tk.CTkButton(
                input_frame,
                text="Clear",
                width=70,
                fg_color="#4a1a1a",
                hover_color="#6a2a2a",
                command=self._clear_chat,
            )
            self.clear_btn.pack(side="left")

        else:
            w.title("FRIDAY Ultra — Chat")
            w.geometry("740x540+100+100")
            w.configure(bg=bg)

            toolbar = self.tk.Frame(w, bg="#12122a", height=36)
            toolbar.pack(fill="x", padx=8, pady=(6, 0))

            self.tk.Label(
                toolbar, text="Lang:", bg="#12122a", fg="#888", font=("Segoe UI", 11)
            ).pack(side="left", padx=(6, 4))
            self._lang_var = self.tk.StringVar(value="English")
            lang_names = sorted(_LANG_MAP.values()) if _HAS_MULTI else ["English"]
            self._lang_menu = self.tk.OptionMenu(
                toolbar, self._lang_var, *lang_names, command=self._on_language_change
            )
            self._lang_menu.config(bg="#1a1a3e", fg="#e0e0e0", relief="flat")
            self._lang_menu.pack(side="left", padx=(0, 10))

            from tkinter import scrolledtext

            self.chat_area = scrolledtext.ScrolledText(
                w,
                wrap="word",
                font=("Segoe UI", 12),
                bg=text_bg,
                fg=text_fg,
                insertbackground=text_fg,
                borderwidth=0,
                state="disabled",
            )
            self.chat_area.pack(fill="both", expand=True, padx=8, pady=(8, 4))

            input_frame = self.tk.Frame(w, bg=bg)
            input_frame.pack(fill="x", padx=8, pady=(0, 8))

            self.input_box = self.tk.Entry(
                input_frame,
                font=("Segoe UI", 13),
                bg=text_bg,
                fg=text_fg,
                insertbackground=text_fg,
                relief="flat",
            )
            self.input_box.pack(side="left", fill="x", expand=True, padx=(0, 6))
            self.input_box.bind("<Return>", lambda e: self._send())

            self.send_btn = self.tk.Button(
                input_frame,
                text="Send",
                width=10,
                bg="#0a84f",
                fg="white",
                relief="flat",
                command=self._send,
            )
            self.send_btn.pack(side="left", padx=(0, 4))

            self.voice_btn = self.tk.Button(
                input_frame,
                text="🎤",
                width=4,
                bg="#2a2a4a",
                fg="white",
                relief="flat",
                command=self._voice_input,
            )
            self.voice_btn.pack(side="left", padx=(0, 4))

            self.clear_btn = self.tk.Button(
                input_frame,
                text="Clear",
                width=8,
                bg="#4a1a1a",
                fg="white",
                relief="flat",
                command=self._clear_chat,
            )
            self.clear_btn.pack(side="left")

        self._append_message(
            "System", "FRIDAY Ultra — Chat UI started. Say 'help' for commands."
        )

    def _append_message(self, sender: str, text: str):
        self.chat_area.configure(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        tag = (
            "user" if sender == "You" else "friday" if sender == "FRIDAY" else "system"
        )
        self.chat_area.insert("end", f"[{ts}] ", "timestamp")
        self.chat_area.insert("end", f"{sender}: ", tag)
        self.chat_area.insert("end", f"{text}\n\n")
        self.chat_area.see("end")
        self.chat_area.configure(state="disabled")

    def _on_language_change(self, lang_name: str):
        if not _HAS_MULTI:
            return
        for code, name in _LANG_MAP.items():
            if name == lang_name:
                _set_lang(code)
                get_recognition_locale(code)
                self._append_message("System", f"Language changed to {name}")
                break

    def _send(self):
        text = self.input_box.get().strip()
        if not text:
            return
        self.input_box.delete(0, "end")
        self._append_message("You", text)

        # Translate non-English input to English before processing
        cmd = text
        if _HAS_MULTI:
            detected = detect_language(text)
            if detected != "en":
                translated = translate_text(
                    text, target_lang="en", source_lang=detected
                )
                if translated:
                    cmd = translated

        try:
            self._handle_command(cmd, self.voice)
        except Exception as e:
            self._append_message("System", f"Error: {e}")

    def _voice_input(self):
        if not FEATURES.get("core_voice"):
            self._append_message("System", "Voice input disabled (core_voice=False).")
            return
        try:
            from core.voice import VoiceEngine

            v = VoiceEngine(female_voice=FEATURES.get("female_voice", True))
            self._append_message("System", "Listening (5s timeout)…")
            cmd = v.listen()
            if cmd:
                self.input_box.insert("end", cmd)
                self._append_message("System", f"Heard: {cmd}")
            else:
                self._append_message("System", "No speech detected.")
        except Exception as e:
            self._append_message("System", f"Mic error: {e}")

    def _clear_chat(self):
        self.chat_area.configure(state="normal")
        self.chat_area.delete("1.0", "end")
        self.chat_area.configure(state="disabled")

    def _on_close(self):
        self._running = False
        try:
            self.window.destroy()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Poll for async responses (FRIDAY replies after processing)
    # ------------------------------------------------------------------
    def _start_poller(self):
        def poll():
            while self._running:
                try:
                    self.window.update_idletasks()
                    self.window.update()
                except Exception:
                    break
                msgs = self.voice.drain()
                for msg in msgs:
                    self._append_message("FRIDAY", msg)
                time.sleep(self._poll_interval / 1000.0)

        t = threading.Thread(target=poll, daemon=True)
        t.start()


# ---------------------------------------------------------------------------
# convenience launcher
# ---------------------------------------------------------------------------


def launch_chat():
    t = threading.Thread(target=show_chat, daemon=True)
    t.start()
    return t


def close_chat():
    global _CHAT_WINDOW
    with _WINDOW_LOCK:
        if _CHAT_WINDOW:
            _CHAT_WINDOW._on_close()
            _CHAT_WINDOW = None


def is_chat_open() -> bool:
    global _CHAT_WINDOW
    return _CHAT_WINDOW is not None and _CHAT_WINDOW.is_alive()
