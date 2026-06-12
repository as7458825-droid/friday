import tkinter as tk
from tkinter import scrolledtext


class TerminalPanel:
    def __init__(self, parent, theme):
        self.theme = theme
        self.frame = tk.Frame(parent, bg=theme.get("bg", "#0a0a1a"))

        lbl = tk.Label(
            self.frame,
            text="[ TERMINAL ]",
            bg=theme.get("bg", "#0a0a1a"),
            fg=theme.get("secondary", "#ff00ff"),
            font=("Consolas", 7, "bold"),
        )
        lbl.pack(anchor="w")

        self.text = scrolledtext.ScrolledText(
            self.frame,
            height=6,
            width=44,
            bg="#050510",
            fg="#00ff88",
            font=("Consolas", 8),
            insertbackground="#00ff88",
            state="disabled",
            relief="flat",
            borderwidth=0,
        )
        self.text.pack(fill=tk.BOTH, expand=True)

    def append(self, message: str):
        self.text.config(state="normal")
        self.text.insert(tk.END, f"> {message}\n")
        self.text.see(tk.END)
        self.text.config(state="disabled")
