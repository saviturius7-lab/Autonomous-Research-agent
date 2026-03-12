"""Optuna-style random hyperparameter search for proposed experiments."""

from __future__ import annotations

import copy
import random
from typing import Dict, List

from ai_scientist_system.config.settings import ModelSettings
from ai_scientist_system.experiments.experiment_schema import Experiment
from ai_scientist_system.utils.experiment_hash import experiment_hash


class ExperimentOptimizer:
    def __init__(self, settings: ModelSettings) -> None:
        self.settings = settings

    def _search_space(self, model_name: str) -> Dict[str, tuple]:
        common = {
            "regularization": (0.0001, 10.0),
            "max_depth": (2, 15),
            "n_estimators": (20, 400),
            "learning_rate": (0.01, 0.4),
        }
        if model_name == "LogisticRegression":
            return {"regularization": common["regularization"]}
        if model_name == "KNN":
            return {"n_neighbors": (3, 35)}
        if model_name == "DecisionTree":
            return {"max_depth": common["max_depth"], "min_samples_split": (2, 30)}
        if model_name == "RandomForest":
            return {
                "n_estimators": common["n_estimators"],
                "max_depth": common["max_depth"],
                "min_samples_split": (2, 20),
            }
        if model_name == "GradientBoosting":
            return {
                "n_estimators": common["n_estimators"],
                "learning_rate": common["learning_rate"],
                "max_depth": (2, 8),
            }
        return {}

    def _sample_params(self, model_name: str, seed: int) -> Dict[str, float]:
        rng = random.Random(seed)
        sampled: Dict[str, float] = {}
        for key, (low, high) in self._search_space(model_name).items():
            if isinstance(low, int) and isinstance(high, int):
                sampled[key] = int(rng.randint(low, high))
            else:
                sampled[key] = float(rng.uniform(low, high))
        return sampled

    def optimize(self, experiments: List[Experiment]) -> List[Experiment]:
        optimized: List[Experiment] = []
        for experiment in experiments:
            candidate = copy.deepcopy(experiment)
            seed = candidate.seed or self.settings.random_state
            candidate.hyperparameters = {
                **candidate.hyperparameters,
                **self._sample_params(candidate.model_name, seed),
            }
            candidate.experiment_hash = experiment_hash(
                candidate.model_name,
                candidate.feature_set,
                candidate.hyperparameters,
            )
            optimized.append(candidate)
        return optimized
