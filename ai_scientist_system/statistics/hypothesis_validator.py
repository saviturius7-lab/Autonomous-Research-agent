"""Statistical validation orchestration over experiment results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ai_scientist_system.statistics.multiple_test_correction import (
    benjamini_hochberg_correction,
    bonferroni_correction,
)
from ai_scientist_system.statistics.significance_tests import t_test_against_baseline


@dataclass
class ValidationOutcome:
    valid: bool
    p_value: float
    adjusted_p_value: float
    method: str


class StatisticalValidator:
    def __init__(self, alpha: float = 0.05, correction_method: str = "benjamini-hochberg") -> None:
        self.alpha = alpha
        self.correction_method = correction_method
        self.p_values: List[float] = []

    def validate(self, candidate_scores: List[float], baseline_scores: List[float]) -> ValidationOutcome:
        test = t_test_against_baseline(candidate_scores, baseline_scores, alpha=self.alpha)
        self.p_values.append(test.p_value)

        if self.correction_method == "bonferroni":
            correction = bonferroni_correction(self.p_values, alpha=self.alpha)
        else:
            correction = benjamini_hochberg_correction(self.p_values, alpha=self.alpha)

        adjusted_p = correction.adjusted_p_values[-1]
        is_valid = bool(correction.rejected[-1] and test.p_value < self.alpha)
        return ValidationOutcome(
            valid=is_valid,
            p_value=float(test.p_value),
            adjusted_p_value=float(adjusted_p),
            method=correction.method,
        )
