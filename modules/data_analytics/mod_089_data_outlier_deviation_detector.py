import numpy as np
import pandas as pd


def detect_outliers_zscore(
    data: list[float] | pd.Series, threshold: float = 3
) -> pd.DataFrame:
    series = pd.Series(data).dropna()
    z_scores = np.abs((series - series.mean()) / series.std())

    result = pd.DataFrame(
        {
            "value": series,
            "z_score": z_scores.round(3),
            "is_outlier": z_scores > threshold,
        }
    )

    result[result["is_outlier"]]
    return result


def detect_outliers_iqr(data: list[float] | pd.Series) -> pd.DataFrame:
    series = pd.Series(data).dropna()
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    result = pd.DataFrame(
        {
            "value": series,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "is_outlier": (series < lower_bound) | (series > upper_bound),
        }
    )

    return result
