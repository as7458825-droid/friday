import os
import tkinter as tk
from tkinter import font as tkfont, ttk

from config import FEATURES
from modules.ui.theme_manager import UIFridayTheme


class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, theme_manager: UIFridayTheme):
        super().__init__(parent)
        self._theme_manager = theme_manager
        colors = theme_manager.get_colors()
        self.title("FRIDAY Settings")
        self.geometry("600x500")
        self.configure(bg=colors["bg"])
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()
        self._build(colors)

    def _build(self, colors):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        style = ttk.Style()
        style.theme_use("clam")

        self._features_frame = tk.Frame(notebook, bg=colors["bg"])
        self._api_frame = tk.Frame(notebook, bg=colors["bg"])
        self._voice_frame = tk.Frame(notebook, bg=colors["bg"])
        self._theme_frame = tk.Frame(notebook, bg=colors["bg"])

        notebook.add(self._features_frame, text="Features")
        notebook.add(self._api_frame, text="API Keys")
        notebook.add(self._voice_frame, text="Voice")
        notebook.add(self._theme_frame, text="Appearance")

        self._build_features(colors)
        self._build_api(colors)
        self._build_voice(colors)
        self._build_theme(colors)

    def _build_features(self, colors):
        canvas = tk.Canvas(self._features_frame, bg=colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(
            self._features_frame, orient="vertical", command=canvas.yview
        )
        scroll_frame = tk.Frame(canvas, bg=colors["bg"])
        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._feature_vars = {}
        row = 0
        for key, val in sorted(FEATURES.items()):
            if key.startswith("ui_"):
                continue
            var = tk.BooleanVar(value=val)
            self._feature_vars[key] = var
            cb = tk.Checkbutton(
                scroll_frame,
                text=key,
                variable=var,
                bg=colors["bg"],
                fg=colors["text"],
                font=tkfont.Font(size=9),
                selectcolor=colors["card"],
                activebackground=colors["bg"],
            )
            cb.grid(row=row, column=0, sticky="w", padx=8, pady=1)
            row += 1

        save_btn = tk.Button(
            self._features_frame,
            text="Save Features",
            command=self._save_features,
            bg=colors.get("primary", "#00d4f"),
            fg="#000",
            font=tkfont.Font(size=9, weight="bold"),
            relief="flat",
        )
        save_btn.pack(pady=6)

    def _save_features(self):
        try:
            from config import FEATURES

            for key, var in self._feature_vars.items():
                FEATURES[key] = var.get()
            from modules.hud.mod_001_neon_window import log_message

            log_message("Feature flags updated via settings")
        except Exception:
            pass

    def _build_api(self, colors):
        self._api_entries = {}
        keys = [
            ("OPENROUTER_API_KEY", "OpenRouter"),
            ("OPENAI_API_KEY", "OpenAI"),
            ("ANTHROPIC_API_KEY", "Anthropic"),
            ("GOOGLE_API_KEY", "Google"),
            ("XAI_API_KEY", "xAI (Grok)"),
        ]
        for i, (env_key, label) in enumerate(keys):
            tk.Label(
                self._api_frame,
                text=f"{label}:",
                bg=colors["bg"],
                fg=colors["text"],
                font=tkfont.Font(size=9),
            ).grid(row=i, column=0, sticky="e", padx=4, pady=4)
            entry = tk.Entry(
                self._api_frame,
                width=50,
                show="*",
                bg=colors["card"],
                fg=colors["text"],
                font=tkfont.Font(size=9),
                relief="flat",
            )
            entry.insert(0, os.getenv(env_key, ""))
            entry.grid(row=i, column=1, padx=4, pady=4)
            self._api_entries[env_key] = entry

        save_btn = tk.Button(
            self._api_frame,
            text="Save Keys",
            command=self._save_keys,
            bg=colors.get("primary", "#00d4f"),
            fg="#000",
            font=tkfont.Font(size=9, weight="bold"),
            relief="flat",
        )
        save_btn.grid(row=len(keys), column=0, columnspan=2, pady=12)

    def _save_keys(self):
        env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        for env_key, entry in self._api_entries.items():
            val = entry.get().strip()
            if val:
                os.environ[env_key] = val
                try:
                    lines = []
                    if os.path.isfile(env_path):
                        with open(env_path) as f:
                            lines = f.readlines()
                    found = False
                    for i, line in enumerate(lines):
                        if line.startswith(f"{env_key}="):
                            lines[i] = f"{env_key}={val}\n"
                            found = True
                            break
                    if not found:
                        lines.append(f"{env_key}={val}\n")
                    with open(env_path, "w") as f:
                        f.writelines(lines)
                except Exception:
                    pass

    def _build_voice(self, colors):
        self._voice_female = tk.BooleanVar(value=FEATURES.get("female_voice", True))
        tk.Checkbutton(
            self._voice_frame,
            text="Female Voice",
            variable=self._voice_female,
            bg=colors["bg"],
            fg=colors["text"],
            font=tkfont.Font(size=10),
            selectcolor=colors["card"],
            activebackground=colors["bg"],
        ).pack(anchor="w", padx=8, pady=6)

        tk.Label(
            self._voice_frame,
            text="Speech Rate:",
            bg=colors["bg"],
            fg=colors["text"],
            font=tkfont.Font(size=9),
        ).pack(anchor="w", padx=8)
        self._rate_scale = tk.Scale(
            self._voice_frame,
            from_=100,
            to=300,
            orient="horizontal",
            bg=colors["bg"],
            fg=colors["text"],
            font=tkfont.Font(size=8),
            length=300,
        )
        self._rate_scale.set(180)
        self._rate_scale.pack(anchor="w", padx=8, pady=4)

        tk.Label(
            self._voice_frame,
            text="Language:",
            bg=colors["bg"],
            fg=colors["text"],
            font=tkfont.Font(size=9),
        ).pack(anchor="w", padx=8)
        self._lang_combo = ttk.Combobox(
            self._voice_frame,
            values=["en", "hi", "es", "fr", "de", "zh", "ja", "ar"],
            state="readonly",
            width=10,
        )
        self._lang_combo.set("en")
        self._lang_combo.pack(anchor="w", padx=8, pady=4)

        save_btn = tk.Button(
            self._voice_frame,
            text="Save Voice Settings",
            command=self._save_voice,
            bg=colors.get("primary", "#00d4f"),
            fg="#000",
            font=tkfont.Font(size=9, weight="bold"),
            relief="flat",
        )
        save_btn.pack(anchor="w", padx=8, pady=12)

    def _save_voice(self):
        FEATURES["female_voice"] = self._voice_female.get()
        lang = self._lang_combo.get()
        if lang != "en":
            try:
                from core.language import set_language

                set_language(lang)
            except Exception:
                pass

    def _build_theme(self, colors):
        tk.Label(
            self._theme_frame,
            text="Theme Mode:",
            bg=colors["bg"],
            fg=colors["text"],
            font=tkfont.Font(size=9),
        ).pack(anchor="w", padx=8, pady=4)

        var = tk.StringVar(value="Dark" if self._theme_manager.is_dark else "Light")
        mode_frame = tk.Frame(self._theme_frame, bg=colors["bg"])
        mode_frame.pack(anchor="w", padx=8)

        for mode in ["Dark", "Light"]:
            rb = tk.Radiobutton(
                mode_frame,
                text=mode,
                variable=var,
                value=mode,
                bg=colors["bg"],
                fg=colors["text"],
                font=tkfont.Font(size=9),
                selectcolor=colors["card"],
                command=lambda m=mode.lower(): self._toggle_mode(m.lower()),
            )
            rb.pack(side=tk.LEFT, padx=4)

        tk.Label(
            self._theme_frame,
            text="Accent Color:",
            bg=colors["bg"],
            fg=colors["text"],
            font=tkfont.Font(size=9),
        ).pack(anchor="w", padx=8, pady=(12, 4))

        accent_frame = tk.Frame(self._theme_frame, bg=colors["bg"])
        accent_frame.pack(anchor="w", padx=8)

        for name in self._theme_manager.get_accent_names():
            clr = self._theme_manager.ACCENT_COLORS[name]["primary"]
            btn = tk.Button(
                accent_frame,
                text="",
                width=2,
                height=1,
                bg=clr,
                relief="flat",
                command=lambda n=name: self._set_accent(n),
            )
            btn.pack(side=tk.LEFT, padx=3)

    def _toggle_mode(self, mode: str):
        self._theme_manager.is_dark = mode == "dark"

    def _set_accent(self, name: str):
        self._theme_manager.accent = name
