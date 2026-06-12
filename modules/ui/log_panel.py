import logging
import queue
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

LOG_COLORS = {
    "DEBUG": "#8b949e",
    "INFO": "#00d4f",
    "WARNING": "#ffd700",
    "ERROR": "#ff4444",
    "CRITICAL": "#ff0044",
}


class QueueHandler(logging.Handler):
    def __init__(self, log_queue: queue.Queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        try:
            self.log_queue.put(self.format(record))
        except Exception:
            pass


class LogPanel(tk.Frame):
    def __init__(self, parent, theme):
        super().__init__(parent, bg=theme["bg"])
        self._theme = theme
        self._log_queue: queue.Queue[str] = queue.Queue()
        self._filter_var = tk.StringVar(value="ALL")
        self._build()
        self._setup_handler()

    def _build(self):
        header = tk.Frame(self, bg=self._theme["bg"])
        header.pack(fill=tk.X, padx=4, pady=(4, 0))

        title = tk.Label(
            header,
            text="LOGS",
            bg=self._theme["bg"],
            fg=self._theme.get("primary", "#00d4f"),
            font=tkfont.Font(size=9, weight="bold"),
        )
        title.pack(side=tk.LEFT)

        self._filter_combo = ttk.Combobox(
            header,
            textvariable=self._filter_var,
            values=["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            state="readonly",
            width=10,
        )
        self._filter_combo.pack(side=tk.RIGHT, padx=4)
        self._filter_combo.bind("<<ComboboxSelected>>", lambda e: self._filter())
        self._filter_combo.set("ALL")

        clear_btn = tk.Button(
            header,
            text="CLEAR",
            command=self._clear,
            bg="#21262d",
            fg="#8b949e",
            font=tkfont.Font(size=7),
            relief="flat",
            padx=6,
        )
        clear_btn.pack(side=tk.RIGHT, padx=4)

        self._text = tk.Text(
            self,
            wrap=tk.WORD,
            state="disabled",
            bg=self._theme.get("card", "#161b22"),
            fg="#8b949e",
            font=tkfont.Font(size=8),
            relief="flat",
            borderwidth=0,
            padx=4,
            pady=2,
            height=8,
        )
        self._text.pack(fill=tk.BOTH, expand=True, padx=4, pady=2)
        self._text.tag_config("timestamp", foreground="#484f58")
        for level, color in LOG_COLORS.items():
            self._text.tag_config(level, foreground=color)

    def _setup_handler(self):
        handler = QueueHandler(self._log_queue)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
            )
        )
        logging.getLogger("FRIDAY").addHandler(handler)
        logging.getLogger().addHandler(handler)
        self.after(200, self._poll_queue)

    def _poll_queue(self):
        while not self._log_queue.empty():
            try:
                record = self._log_queue.get_nowait()
                self._append(record)
            except queue.Empty:
                break
        self.after(200, self._poll_queue)

    def _append(self, record: str):
        level = self._extract_level(record)
        if self._filter_var.get() != "ALL" and level != self._filter_var.get():
            return
        tag = level if level in LOG_COLORS else None
        self._text.config(state="normal")
        self._text.insert(tk.END, record + "\n", tag)
        self._text.config(state="disabled")
        self._text.see(tk.END)

    def _extract_level(self, record: str) -> str:
        for level in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
            if f"[{level}]" in record:
                return level
        return "INFO"

    def _filter(self):
        pass

    def _clear(self):
        self._text.config(state="normal")
        self._text.delete(1.0, tk.END)
        self._text.config(state="disabled")

    def update_theme(self, theme: dict):
        self._theme = theme
        self.config(bg=theme["bg"])
        self._text.config(bg=theme.get("card", "#161b22"))
