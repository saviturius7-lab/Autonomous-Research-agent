"""Global settings for the governed autonomous AI scientist system."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


DEFAULT_GEMINI_KEYS = [
    "AIzaSyAgyLOp3O2KJSDuBzTHIcO3P6u0JnYOy9Y",
    "AIzaSyAZLw-MJuq_FVcAPB-VWeGzF5AMoUQ_S8s",
    "AIzaSyCCi9hVrs_Bd7yHgid962SfpxTpLzvEkjs",
    "AIzaSyBOgiTqWdtu5iMww1a_i5R8x8N1YdC4GQ8",
]


@dataclass
class BudgetLimits:
    """Operational budget constraints that governance enforces."""

    max_experiments: int = 1000
    max_api_calls: int = 5000
    max_runtime_hours: float = 24.0
    max_api_cost_usd: float = 20.0


@dataclass
class NoveltySettings:
    """Settings used to avoid duplicate and low-novelty hypotheses."""

    novelty_threshold: float = 0.25
    min_exploration_ratio: float = 0.20


@dataclass
class StatisticsSettings:
    """Defaults for significance testing and correction."""

    alpha: float = 0.05
    bootstrap_iterations: int = 2000
    correction_method: str = "benjamini-hochberg"


@dataclass
class DataSettings:
    """Dataset paths and column settings."""

    data_dir: Path = Path("data")
    train_file: str = "train.csv"
    validation_file: str = "validation.csv"
    holdout_file: str = "holdout.csv"
    target_column: str = "target"
    id_column: str | None = None


@dataclass
class RuntimeSettings:
    """Runtime and checkpoint settings."""

    max_iterations: int = 50
    checkpoint_dir: Path = Path("artifacts/checkpoints")
    log_dir: Path = Path("artifacts/logs")
    report_dir: Path = Path("artifacts/reports")
    leaderboard_path: Path = Path("artifacts/leaderboard.json")


@dataclass
class ModelSettings:
    """Model family and search defaults."""

    supported_models: List[str] = field(
        default_factory=lambda: [
            "LogisticRegression",
            "RandomForest",
            "GradientBoosting",
            "DecisionTree",
            "KNN",
        ]
    )
    default_trials: int = 15
    random_state: int = 42


@dataclass
class Settings:
    """Top-level settings object."""

    budget: BudgetLimits = field(default_factory=BudgetLimits)
    novelty: NoveltySettings = field(default_factory=NoveltySettings)
    statistics: StatisticsSettings = field(default_factory=StatisticsSettings)
    data: DataSettings = field(default_factory=DataSettings)
    runtime: RuntimeSettings = field(default_factory=RuntimeSettings)
    models: ModelSettings = field(default_factory=ModelSettings)
    gemini_model_name: str = "gemini-1.5-flash"

    @property
    def gemini_keys(self) -> List[str]:
        env_keys = [
            key
            for key in [
                os.getenv("GEMINI_KEY_1"),
                os.getenv("GEMINI_KEY_2"),
                os.getenv("GEMINI_KEY_3"),
                os.getenv("GEMINI_KEY_4"),
            ]
            if key
        ]
        return env_keys or DEFAULT_GEMINI_KEYS


def load_settings() -> Settings:
    """Construct settings and ensure artifact directories exist."""

    settings = Settings()
    for path in [
        settings.runtime.checkpoint_dir,
        settings.runtime.log_dir,
        settings.runtime.report_dir,
    ]:
        path.mkdir(parents=True, exist_ok=True)
    return settings
