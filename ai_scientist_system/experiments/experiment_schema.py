"""Experiment and result schemas used across the system."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Hypothesis:
    text: str
    rationale: str
    source: str = "scientist_agent"
    exploration: bool = False
    novelty_score: float = 1.0


@dataclass
class Experiment:
    experiment_id: str
    hypothesis_text: str
    model_name: str
    feature_set: List[str]
    hyperparameters: Dict[str, Any]
    split_name: str = "train_validation_holdout"
    created_at: float = field(default_factory=time.time)
    seed: Optional[int] = None
    model_version: str = "v1"
    dataset_hash: str = ""
    code_version: str = "unknown"
    experiment_hash: str = ""


@dataclass
class ExperimentResult:
    experiment_id: str
    model_name: str
    metrics: Dict[str, float]
    runtime_seconds: float
    feature_importance: Dict[str, float]
    confidence_intervals: Dict[str, Any]
    p_value: float
    passed_statistics: bool
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationRecord:
    experiment_id: str
    primary_metric: str
    primary_score: float
    passed: bool
    notes: List[str] = field(default_factory=list)
