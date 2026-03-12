"""Multiple hypothesis correction methods for large-scale experimentation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

import numpy as np


@dataclass
class CorrectionResult:
    method: str
    adjusted_alpha: float
    rejected: List[bool]
    adjusted_p_values: List[float]


def bonferroni_correction(p_values: Sequence[float], alpha: float = 0.05) -> CorrectionResult:
    n = max(1, len(p_values))
    adjusted_alpha = alpha / n
    rejected = [p < adjusted_alpha for p in p_values]
    adjusted_p = [min(1.0, p * n) for p in p_values]
    return CorrectionResult(
        method="bonferroni",
        adjusted_alpha=adjusted_alpha,
        rejected=rejected,
        adjusted_p_values=adjusted_p,
    )


def benjamini_hochberg_correction(
    p_values: Sequence[float], alpha: float = 0.05
) -> CorrectionResult:
    n = len(p_values)
    if n == 0:
        return CorrectionResult("benjamini-hochberg", alpha, [], [])

    pvals = np.asarray(p_values, dtype=float)
    order = np.argsort(pvals)
    sorted_p = pvals[order]

    thresholds = np.array([(i + 1) / n * alpha for i in range(n)])
    passed = sorted_p <= thresholds

    rejected_sorted = np.zeros(n, dtype=bool)
    if np.any(passed):
        max_i = np.where(passed)[0].max()
        rejected_sorted[: max_i + 1] = True

    adjusted = np.empty(n, dtype=float)
    cumulative = 1.0
    for i in range(n - 1, -1, -1):
        rank = i + 1
        cumulative = min(cumulative, sorted_p[i] * n / rank)
        adjusted[i] = cumulative

    rejected = np.zeros(n, dtype=bool)
    rejected[order] = rejected_sorted
    adjusted_original = np.zeros(n, dtype=float)
    adjusted_original[order] = adjusted

    return CorrectionResult(
        method="benjamini-hochberg",
        adjusted_alpha=alpha,
        rejected=rejected.tolist(),
        adjusted_p_values=adjusted_original.tolist(),
    )
