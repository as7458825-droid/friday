import datetime
import os

import numpy as np
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")


def _ensure_output():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def linear_forecast(data: list[float] | pd.Series, periods: int = 5) -> list[float]:
    n = len(data)
    x = np.arange(n)
    y = np.array(data)

    if np.isnan(y).any():
        y = np.nan_to_num(y, nan=0.0)

    A = np.vstack([x, np.ones(n)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]

    future_x = np.arange(n, n + periods)
    predictions = slope * future_x + intercept

    result = list(predictions.round(2))

    _ensure_output()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    df = pd.DataFrame({"period": list(range(1, n + periods + 1))})
    df["value"] = list(y.round(2)) + result
    df.loc[: n - 1, "type"] = "actual"
    df.loc[n:, "type"] = "forecast"
    fpath = os.path.join(OUTPUT_DIR, f"forecast_{ts}.csv")
    df.to_csv(fpath, index=False)

    return result


def moving_average(data: list[float] | pd.Series, window: int = 3) -> list[float]:
    series = pd.Series(data)
    if window < 1:
        window = 1
    smoothed = series.rolling(window=window, min_periods=1).mean()
    return [round(v, 2) for v in smoothed.tolist()]
