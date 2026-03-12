"""Leaderboard for best-performing statistically valid experiments."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List

from ai_scientist_system.experiments.experiment_schema import ExperimentResult


@dataclass
class LeaderboardEntry:
    experiment_id: str
    model_name: str
    metric: float
    metrics: Dict[str, float]
    passed_statistics: bool


@dataclass
class Leaderboard:
    entries: List[LeaderboardEntry] = field(default_factory=list)
    metric_name: str = "f1"

    def update(self, result: ExperimentResult) -> None:
        score = float(result.metrics.get(self.metric_name, 0.0))
        self.entries.append(
            LeaderboardEntry(
                experiment_id=result.experiment_id,
                model_name=result.model_name,
                metric=score,
                metrics=result.metrics,
                passed_statistics=result.passed_statistics,
            )
        )
        self.entries.sort(key=lambda x: x.metric, reverse=True)

    def top(self, k: int = 10) -> List[LeaderboardEntry]:
        return self.entries[:k]

    def snapshot(self) -> Dict:
        return {"entries": [asdict(e) for e in self.entries], "metric_name": self.metric_name}

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.snapshot(), indent=2))
