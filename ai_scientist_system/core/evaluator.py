"""Experiment evaluator with configurable primary metric thresholding."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ai_scientist_system.experiments.experiment_schema import EvaluationRecord, ExperimentResult


@dataclass
class EvaluationPolicy:
    primary_metric: str = "f1"
    minimum_threshold: float = 0.5


class Evaluator:
    def __init__(self, policy: EvaluationPolicy | None = None) -> None:
        self.policy = policy or EvaluationPolicy()

    def evaluate(self, result: ExperimentResult) -> EvaluationRecord:
        score = float(result.metrics.get(self.policy.primary_metric, 0.0))
        notes: List[str] = []
        if score < self.policy.minimum_threshold:
            notes.append(
                f"Primary metric {self.policy.primary_metric}={score:.4f} below threshold {self.policy.minimum_threshold:.4f}"
            )
        return EvaluationRecord(
            experiment_id=result.experiment_id,
            primary_metric=self.policy.primary_metric,
            primary_score=score,
            passed=score >= self.policy.minimum_threshold,
            notes=notes,
        )
