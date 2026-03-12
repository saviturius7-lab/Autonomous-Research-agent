"""Critic agent that reviews statistically valid experiments for robustness concerns."""

from __future__ import annotations

from ai_scientist_system.experiments.experiment_schema import Experiment, ExperimentResult


class CriticAgent:
    def review(self, experiment: Experiment, result: ExperimentResult) -> str:
        risks = []
        if result.metrics.get("precision", 0.0) < 0.5:
            risks.append("low precision")
        if result.metrics.get("recall", 0.0) < 0.5:
            risks.append("low recall")
        if result.confidence_intervals.get("accuracy", (0, 0))[0] < 0.5:
            risks.append("weak lower-bound confidence interval")

        if risks:
            return f"Critic concerns for {experiment.experiment_id}: " + ", ".join(risks)
        return f"Experiment {experiment.experiment_id} appears robust under current checks."
