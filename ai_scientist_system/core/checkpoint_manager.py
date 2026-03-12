"""Checkpoint manager for resumable autonomous research loops."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable

from ai_scientist_system.experiments.experiment_schema import Experiment, ExperimentResult


class CheckpointManager:
    def __init__(self, checkpoint_dir: Path) -> None:
        self.checkpoint_dir = checkpoint_dir
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, iteration: int) -> Path:
        return self.checkpoint_dir / f"checkpoint_{iteration:04d}.json"

    def save(
        self,
        iteration: int,
        queue_snapshot: list,
        memory_snapshot: Dict[str, Any],
        leaderboard_snapshot: Dict[str, Any],
        graph_snapshot: Dict[str, Any],
        budget_snapshot: Dict[str, Any],
    ) -> Path:
        payload = {
            "iteration": iteration,
            "queue": queue_snapshot,
            "memory": memory_snapshot,
            "leaderboard": leaderboard_snapshot,
            "graph": graph_snapshot,
            "budget": budget_snapshot,
        }
        path = self._path(iteration)
        path.write_text(json.dumps(payload, indent=2))
        return path

    def latest_checkpoint(self) -> Path | None:
        files = sorted(self.checkpoint_dir.glob("checkpoint_*.json"))
        return files[-1] if files else None

    def load_latest(self) -> Dict[str, Any] | None:
        latest = self.latest_checkpoint()
        if not latest:
            return None
        return json.loads(latest.read_text())


def serialize_experiments(experiments: Iterable[Experiment]) -> list:
    return [asdict(exp) for exp in experiments]


def serialize_results(results: Iterable[ExperimentResult]) -> list:
    return [asdict(result) for result in results]
