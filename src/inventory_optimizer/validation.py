from __future__ import annotations

import numpy as np
import pandas as pd


def walk_forward_validation(series: pd.Series, n_splits: int = 5) -> list[float]:
    n = len(series)
    fold = n // (n_splits + 1)
    scores: list[float] = []
    for i in range(1, n_splits + 1):
        train = series.iloc[: i * fold]
        test = series.iloc[i * fold : (i + 1) * fold]
        pred = float(train.mean())
        scores.append(float(np.mean(np.abs(test - pred))))
    return scores


def purged_cv(series: pd.Series, n_splits: int = 5, gap: int = 5) -> list[float]:
    n = len(series)
    fold = n // (n_splits + 1)
    scores: list[float] = []
    for i in range(1, n_splits + 1):
        train_end = max(0, i * fold - gap)
        test_start = i * fold
        test_end = (i + 1) * fold
        train = series.iloc[:train_end]
        test = series.iloc[test_start:test_end]
        pred = float(train.mean()) if len(train) else float(series.mean())
        scores.append(float(np.mean(np.abs(test - pred))))
    return scores


def population_stability_index(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    eps = 1e-6
    cuts = np.quantile(expected, np.linspace(0, 1, bins + 1))
    e_hist, _ = np.histogram(expected, bins=cuts)
    a_hist, _ = np.histogram(actual, bins=cuts)
    e = e_hist / max(e_hist.sum(), 1)
    a = a_hist / max(a_hist.sum(), 1)
    return float(np.sum((a - e) * np.log((a + eps) / (e + eps))))
