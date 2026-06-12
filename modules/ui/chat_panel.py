import queue
from datetime import datetime
from tkinter import font as tkfont
import tkinter as tk
from tkinter import scrolledtext


class ChatPanel(tk.Frame):
    def __init__(self, parent, theme, on_send_callback=None):
        super().__init__(parent, bg=theme["bg"])
        self._theme = theme
        self._on_send = on_send_callback
        self._command_queue: queue.Queue[str] = queue.Queue()
        self._response_queue: queue.Queue[str] = queue.Queue()
        self._build()

    def _build(self):
        title = tk.Label(
            self,
            text="CHAT",
            bg=self._theme["bg"],
            fg=self._theme.get("primary", "#00d4f"),
            font=tkfont.Font(size=10, weight="bold"),
        )
        title.pack(anchor="w", padx=6, pady=(4, 0))

        self._text_area = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            state="disabled",
            bg=self._theme.get("card", "#161b22"),
            fg=self._theme.get("text", "#e6edf3"),
            font=tkfont.Font(size=10),
            insertbackground=self._theme.get("primary", "#00d4f"),
            relief="flat",
            borderwidth=0,
            padx=6,
            pady=6,
        )
        self._text_area.pack(fill=tk.BOTH, expand=True, padx=4, pady=2)

        input_frame = tk.Frame(self, bg=self._theme["bg"])
        input_frame.pack(fill=tk.X, padx=4, pady=(0, 4))

        self._entry = tk.Entry(
            input_frame,
            bg=self._theme.get("card", "#161b22"),
            fg=self._theme.get("text", "#e6edf3"),
            font=tkfont.Font(size=10),
            insertbackground=self._theme.get("primary", "#00d4f"),
            relief="flat",
            borderwidth=1,
        )
        self._entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self._entry.bind("<Return>", lambda e: self._send())
        self._entry.bind("<Control-Shift-Key-F>", lambda e: self._entry.focus())

        self._send_btn = tk.Button(
            input_frame,
            text="SEND",
            command=self._send,
            bg=self._theme.get("primary", "#00d4f"),
            fg="#000000",
            font=tkfont.Font(size=9, weight="bold"),
            relief="flat",
            padx=10,
            activebackground=self._theme.get("secondary", "#ff00f"),
        )
        self._send_btn.pack(side=tk.RIGHT, padx=(4, 0))

        self._mic_btn = tk.Button(
            input_frame,
            text="🎤",
            command=self._mic_click,
            bg=self._theme.get("card", "#161b22"),
            fg=self._theme.get("primary", "#00d4f"),
            font=tkfont.Font(size=12),
            relief="flat",
            padx=6,
        )
        self._mic_btn.pack(side=tk.RIGHT, padx=(0, 4))

    def _send(self):
        text = self._entry.get().strip()
        if text:
            self._entry.delete(0, tk.END)
            self.add_message("You", text)
            if self._on_send:
                self._on_send(text)

    def _mic_click(self):
        self.add_message("System", "Voice input toggled (implement in main loop)")

    def add_message(self, sender: str, text: str):
        now = datetime.now().strftime("%H:%M")
        self._text_area.config(state="normal")
        tag = (
            "user"
            if sender.lower() == "you"
            else "ai"
            if sender.lower() != "system"
            else "system"
        )
        self._text_area.insert(tk.END, f"[{now}] ", "timestamp")
        self._text_area.insert(tk.END, f"{sender}: ", tag)
        self._text_area.insert(tk.END, f"{text}\n\n")
        self._text_area.config(state="disabled")
        self._text_area.see(tk.END)

    def add_response(self, text: str):
        self.add_message("FRIDAY", text)

    def update_theme(self, theme: dict):
        self._theme = theme
        self.config(bg=theme["bg"])
        for child in self.winfo_children():
            try:
                child.config(bg=theme["bg"])
            except Exception:
                pass
        self._text_area.config(
            bg=theme.get("card", "#161b22"), fg=theme.get("text", "#e6edf3")
        )
        self._entry.config(
            bg=theme.get("card", "#161b22"), fg=theme.get("text", "#e6edf3")
        )
