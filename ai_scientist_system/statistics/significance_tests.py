"""Significance tests used by the statistical validator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

import numpy as np
from scipy import stats


@dataclass
class SignificanceResult:
    p_value: float
    statistic: float
    significant: bool


def t_test_against_baseline(
    sample_scores: Iterable[float],
    baseline_scores: Iterable[float],
    alpha: float = 0.05,
) -> SignificanceResult:
    sample = np.asarray(list(sample_scores), dtype=float)
    baseline = np.asarray(list(baseline_scores), dtype=float)
    statistic, p_value = stats.ttest_ind(sample, baseline, equal_var=False)
    return SignificanceResult(
        p_value=float(p_value),
        statistic=float(statistic),
        significant=bool(p_value < alpha),
    )


def bootstrap_confidence_intervals(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    n_iterations: int = 2000,
    confidence: float = 0.95,
) -> Dict[str, Tuple[float, float]]:
    rng = np.random.default_rng(12345)
    n = len(y_true)
    if n == 0:
        return {"accuracy": (0.0, 0.0)}

    metrics = []
    for _ in range(n_iterations):
        idx = rng.choice(n, size=n, replace=True)
        acc = float(np.mean(y_true[idx] == y_pred[idx]))
        metrics.append(acc)

    low = (1 - confidence) / 2
    high = 1 - low
    return {"accuracy": (float(np.quantile(metrics, low)), float(np.quantile(metrics, high)))}
