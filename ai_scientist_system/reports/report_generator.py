"""Research report generator."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from ai_scientist_system.memory.leaderboard import Leaderboard
from ai_scientist_system.memory.research_memory import ResearchMemory


class ReportGenerator:
    def __init__(self, report_dir: Path) -> None:
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, iteration: int, memory: ResearchMemory, leaderboard: Leaderboard, patterns: Dict) -> Path:
        payload = {
            "iteration": iteration,
            "experiment_count": len(memory.entries),
            "top_leaderboard": [entry.__dict__ for entry in leaderboard.top(10)],
            "patterns": patterns,
        }
        path = self.report_dir / f"report_{iteration:04d}.json"
        path.write_text(json.dumps(payload, indent=2))
        return path
