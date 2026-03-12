"""Scientist agent that generates hypotheses and translates them to experiments."""

from __future__ import annotations

import itertools
import random
from typing import List

from ai_scientist_system.agents.planner_agent import ResearchDirection
from ai_scientist_system.config.settings import ModelSettings, NoveltySettings
from ai_scientist_system.experiments.experiment_schema import Experiment, Hypothesis
from ai_scientist_system.utils.experiment_hash import experiment_hash
from ai_scientist_system.utils.novelty_metrics import filter_novel_hypotheses


class ScientistAgent:
    def __init__(self, model_settings: ModelSettings, novelty_settings: NoveltySettings) -> None:
        self.model_settings = model_settings
        self.novelty_settings = novelty_settings
        self._exp_counter = itertools.count(1)

    def generate_hypotheses(self, direction: ResearchDirection, n: int = 10) -> List[Hypothesis]:
        hypotheses: List[Hypothesis] = []
        for i in range(n):
            exploration = random.random() < self.novelty_settings.min_exploration_ratio
            text = (
                f"{direction.title}: Hypothesis {i + 1} - "
                f"testing whether targeted feature subset and {direction.objective[:80]}"
            )
            rationale = (
                "Exploration mode" if exploration else "Exploitation mode"
            ) + " generated from planner direction."
            hypotheses.append(
                Hypothesis(
                    text=text,
                    rationale=rationale,
                    exploration=exploration,
                )
            )
        return hypotheses

    def novelty_filter(self, hypotheses: List[Hypothesis], previous_hypotheses: List[str]) -> List[Hypothesis]:
        return filter_novel_hypotheses(
            hypotheses=hypotheses,
            previous_hypotheses=previous_hypotheses,
            threshold=self.novelty_settings.novelty_threshold,
            exploration_ratio=self.novelty_settings.min_exploration_ratio,
        )

    def _feature_subset(self, all_features: List[str], min_size: int = 3) -> List[str]:
        if len(all_features) <= min_size:
            return all_features
        k = random.randint(min_size, max(min_size, len(all_features) - 1))
        subset = random.sample(all_features, k=k)
        subset.sort()
        return subset

    def design_experiments(self, hypotheses: List[Hypothesis], all_features: List[str]) -> List[Experiment]:
        experiments: List[Experiment] = []
        for hypothesis in hypotheses:
            model_name = random.choice(self.model_settings.supported_models)
            feature_set = self._feature_subset(all_features)
            hyperparameters = {}
            exp_id = f"exp_{next(self._exp_counter):06d}"
            exp_hash = experiment_hash(model_name, feature_set, hyperparameters)
            experiments.append(
                Experiment(
                    experiment_id=exp_id,
                    hypothesis_text=hypothesis.text,
                    model_name=model_name,
                    feature_set=feature_set,
                    hyperparameters=hyperparameters,
                    experiment_hash=exp_hash,
                )
            )
        return experiments
