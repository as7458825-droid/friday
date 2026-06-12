import datetime
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config import FEATURES

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "output")


def _ensure_output():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_chart(
    data: pd.DataFrame,
    chart_type: str = "line",
    x_column: str = None,
    y_column: str = None,
    title: str = None,
) -> str:
    _ensure_output()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    fig, ax = plt.subplots(figsize=(10, 6))

    x = data[x_column] if x_column else data.index
    y = (
        data[y_column]
        if y_column
        else (data.iloc[:, 0] if data.shape[1] > 0 else data.index)
    )

    try:
        if chart_type == "line":
            ax.plot(x, y, marker="o", linestyle="-", color="#00d4ff")
        elif chart_type == "bar":
            ax.bar(range(len(y)), y, color="#0a84ff")
            if x_column:
                ax.set_xticks(range(len(x)))
                ax.set_xticklabels(x, rotation=45, ha="right")
        elif chart_type == "scatter":
            ax.scatter(x, y, color="#ff6b6b", alpha=0.6)
        elif chart_type == "histogram":
            ax.hist(y, bins=20, color="#00d4ff", edgecolor="white")
        else:
            ax.plot(x, y, marker="s", linestyle="--", color="#00d4ff")
    except Exception as e:
        return f"Chart error: {e}"

    ax.set_xlabel(x_column or "Index")
    ax.set_ylabel(y_column or "Value")
    ax.set_title(title or f"{chart_type.capitalize()} Chart")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    fname = f"chart_{chart_type}_{ts}.png"
    fpath = os.path.join(OUTPUT_DIR, fname)
    fig.savefig(fpath, dpi=150)
    plt.close(fig)
    return f"Chart saved -> {fpath}"


def show_chart_in_hud(image_path: str) -> str:
    if not FEATURES.get("hud_gui"):
        return "HUD not enabled"
    try:
        from modules.hud.mod_001_neon_window import launch_hud

        launch_hud()
        return "Chart can be viewed in HUD"
    except Exception:
        return "HUD unavailable"
