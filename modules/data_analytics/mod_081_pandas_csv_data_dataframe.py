import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def load_csv(filepath: str) -> pd.DataFrame:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return pd.read_csv(filepath)


def load_excel(filepath: str, sheet_name: str = 0) -> pd.DataFrame:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return pd.read_excel(filepath, sheet_name=sheet_name)


def analyze_dataframe(df: pd.DataFrame) -> dict:
    info = {
        "shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).to_dict(),
        "summary": {},
    }
    for col in df.select_dtypes(include="number").columns:
        info["summary"][col] = {
            "mean": round(df[col].mean(), 2) if not df[col].isna().all() else None,
            "median": round(df[col].median(), 2) if not df[col].isna().all() else None,
            "min": round(df[col].min(), 2) if not df[col].isna().all() else None,
            "max": round(df[col].max(), 2) if not df[col].isna().all() else None,
            "std": round(df[col].std(), 2) if not df[col].isna().all() else None,
        }
    return info


def speak_analysis(info: dict) -> str:
    lines = []
    lines.append(
        f"Dataset has {info['shape']['rows']} rows and {info['shape']['columns']} columns."
    )
    missing_cols = {k: v for k, v in info["missing_values"].items() if v > 0}
    if missing_cols:
        lines.append(
            f"Columns with missing values: {', '.join(f'{k} ({v})' for k, v in missing_cols.items())}"
        )
    else:
        lines.append("No missing values found.")
    for col, stats in info["summary"].items():
        if stats.get("mean") is not None:
            lines.append(
                f"{col}: mean {stats['mean']}, min {stats['min']}, max {stats['max']}"
            )
    return ". ".join(lines)
