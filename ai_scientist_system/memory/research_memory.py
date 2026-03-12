"""Persistent in-memory research records."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

from ai_scientist_system.experiments.experiment_schema import Experiment, ExperimentResult


@dataclass
class MemoryEntry:
    experiment: Dict[str, Any]
    result: Dict[str, Any]
    critic_feedback: str


@dataclass
class ResearchMemory:
    entries: List[MemoryEntry] = field(default_factory=list)

    def store(self, experiment: Experiment, result: ExperimentResult, critic_feedback: str) -> None:
        self.entries.append(
            MemoryEntry(
                experiment=asdict(experiment),
                result=asdict(result),
                critic_feedback=critic_feedback,
            )
        )

    def all_hypotheses(self) -> List[str]:
        return [entry.experiment["hypothesis_text"] for entry in self.entries]

    def top_results(self, metric: str = "f1", k: int = 10) -> List[MemoryEntry]:
        sorted_entries = sorted(
            self.entries,
            key=lambda e: float(e.result["metrics"].get(metric, 0.0)),
            reverse=True,
        )
        return sorted_entries[:k]

    def snapshot(self) -> Dict[str, Any]:
        return {"entries": [asdict(entry) for entry in self.entries]}
