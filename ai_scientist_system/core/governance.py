"""Governance layer enforcing cost, validity, uniqueness, and integrity constraints."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Set

from ai_scientist_system.config.settings import BudgetLimits
from ai_scientist_system.experiments.experiment_schema import Experiment

logger = logging.getLogger(__name__)


class GovernanceViolation(RuntimeError):
    pass


@dataclass
class BudgetTracker:
    experiments_run: int = 0
    api_calls: int = 0
    runtime_hours: float = 0.0
    api_cost_usd: float = 0.0
    started_at: float = field(default_factory=time.time)

    def update_runtime(self) -> None:
        elapsed = time.time() - self.started_at
        self.runtime_hours = elapsed / 3600.0


class ExperimentGovernance:
    def __init__(self, limits: BudgetLimits) -> None:
        self.limits = limits
        self.tracker = BudgetTracker()
        self._experiment_hashes: Set[str] = set()

    def validate_experiment(self, experiment: Experiment) -> Experiment:
        """Validate a single experiment with all governance checks."""

        self.check_budget()
        self.check_diversity(experiment)
        self.check_dataset_integrity(experiment)
        return experiment

    def validate_batch(self, experiments: Iterable[Experiment]) -> List[Experiment]:
        valid: List[Experiment] = []
        for experiment in experiments:
            try:
                valid.append(self.validate_experiment(experiment))
            except GovernanceViolation as exc:
                logger.warning("Governance rejected %s: %s", experiment.experiment_id, exc)
        return valid

    def check_budget(self) -> None:
        self.tracker.update_runtime()
        if self.tracker.experiments_run >= self.limits.max_experiments:
            raise GovernanceViolation("Max experiments exceeded")
        if self.tracker.api_calls >= self.limits.max_api_calls:
            raise GovernanceViolation("Max API calls exceeded")
        if self.tracker.runtime_hours >= self.limits.max_runtime_hours:
            raise GovernanceViolation("Max runtime hours exceeded")
        if self.tracker.api_cost_usd >= self.limits.max_api_cost_usd:
            raise GovernanceViolation("Max API cost exceeded")

    def check_diversity(self, experiment: Experiment) -> None:
        if not experiment.experiment_hash:
            raise GovernanceViolation("Experiment hash missing")
        if experiment.experiment_hash in self._experiment_hashes:
            raise GovernanceViolation("Duplicate experiment hash detected")

        self._experiment_hashes.add(experiment.experiment_hash)

    def check_dataset_integrity(self, experiment: Experiment) -> None:
        if not experiment.dataset_hash:
            raise GovernanceViolation("Dataset hash missing")
        if experiment.split_name != "train_validation_holdout":
            raise GovernanceViolation("Experiment must use train/validation/holdout protocol")

    def record_experiment_completion(self, runtime_seconds: float) -> None:
        self.tracker.experiments_run += 1
        self.tracker.runtime_hours += runtime_seconds / 3600.0

    def record_api_usage(self, call_count: int, cost_usd: float) -> None:
        self.tracker.api_calls += call_count
        self.tracker.api_cost_usd += cost_usd

    def budget_snapshot(self) -> Dict[str, float]:
        self.tracker.update_runtime()
        return {
            "experiments_run": self.tracker.experiments_run,
            "api_calls": self.tracker.api_calls,
            "runtime_hours": round(self.tracker.runtime_hours, 4),
            "api_cost_usd": round(self.tracker.api_cost_usd, 4),
            "max_experiments": self.limits.max_experiments,
            "max_api_calls": self.limits.max_api_calls,
            "max_runtime_hours": self.limits.max_runtime_hours,
            "max_api_cost_usd": self.limits.max_api_cost_usd,
        }
