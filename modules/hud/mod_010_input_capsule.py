import tkinter as tk


class InputCapsule:
    def __init__(self, parent, theme):
        self.theme = theme
        self.frame = tk.Frame(parent, bg=theme.get("bg", "#0a0a1a"))

        self.entry = tk.Entry(
            self.frame,
            width=40,
            bg="#111122",
            fg=theme.get("primary", "#00ffff"),
            insertbackground=theme.get("primary", "#00ffff"),
            font=("Consolas", 10),
            relief="flat",
            borderwidth=0,
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 4))
        self.entry.insert(0, "Type command here...")
        self.entry.bind(
            "<FocusIn>",
            lambda e: (
                self.entry.delete(0, tk.END)
                if self.entry.get() == "Type command here..."
                else None
            ),
        )
        self.entry.bind("<Return>", self._submit)

        self.send_btn = tk.Button(
            self.frame,
            text="▶",
            command=self._submit,
            bg=theme.get("secondary", "#ff00ff"),
            fg="#ffffff",
            relief="flat",
            font=("Consolas", 9),
            cursor="hand2",
        )
        self.send_btn.pack(side=tk.LEFT)

        self._callback = None

    def on_submit(self, callback):
        self._callback = callback

    def _submit(self, event=None):
        text = self.entry.get().strip()
        if text and text != "Type command here..." and self._callback:
            self._callback(text)
            self.entry.delete(0, tk.END)
