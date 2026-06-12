import tkinter as tk
from tkinter import font as tkfont


class ToastNotification:
    _instance = None

    @classmethod
    def get_instance(cls, parent=None):
        if cls._instance is None and parent is not None:
            cls._instance = cls(parent)
        return cls._instance

    def __init__(self, parent):
        self.parent = parent
        self._label = None
        self._after_id = None

    def show(self, message: str, duration: int = 3000, is_error: bool = False):
        if self._after_id:
            self.parent.after_cancel(self._after_id)
            self._after_id = None
        if self._label:
            self._label.destroy()

        colors = {"bg": "#ff4444" if is_error else "#2ea043", "fg": "#ffffff"}
        self._label = tk.Label(
            self.parent,
            text=message,
            bg=colors["bg"],
            fg=colors["fg"],
            font=tkfont.Font(size=10, weight="bold"),
            padx=16,
            pady=8,
            relief="flat",
        )
        self._label.place(relx=0.5, rely=0.02, anchor="n")
        self._label.lift()

        self._after_id = self.parent.after(duration, self._clear)

    def _clear(self):
        if self._label:
            self._label.destroy()
            self._label = None
        self._after_id = None

    def info(self, msg: str):
        self.show(msg, duration=3000, is_error=False)

    def error(self, msg: str):
        self.show(msg, duration=5000, is_error=True)

    def success(self, msg: str):
        self.show(msg, duration=3000, is_error=False)
