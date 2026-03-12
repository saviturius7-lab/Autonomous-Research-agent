"""Priority queue for governed experiments."""

from __future__ import annotations

import heapq
import itertools
from dataclasses import dataclass, field
from typing import List

from ai_scientist_system.experiments.experiment_schema import Experiment


@dataclass(order=True)
class QueueItem:
    priority: float
    sequence: int
    experiment: Experiment = field(compare=False)


class ExperimentQueue:
    def __init__(self) -> None:
        self._items: List[QueueItem] = []
        self._counter = itertools.count()

    def add(self, experiment: Experiment, priority: float = 1.0) -> None:
        heapq.heappush(
            self._items,
            QueueItem(priority=priority, sequence=next(self._counter), experiment=experiment),
        )

    def extend(self, experiments: List[Experiment], priority: float = 1.0) -> None:
        for experiment in experiments:
            self.add(experiment, priority=priority)

    def pop(self) -> Experiment:
        return heapq.heappop(self._items).experiment

    def __len__(self) -> int:
        return len(self._items)

    def to_dict(self) -> List[dict]:
        return [
            {
                "priority": item.priority,
                "sequence": item.sequence,
                "experiment_id": item.experiment.experiment_id,
            }
            for item in self._items
        ]
