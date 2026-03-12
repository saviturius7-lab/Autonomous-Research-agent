"""Visualization helpers for leaderboard and feature insights."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from ai_scientist_system.memory.leaderboard import Leaderboard


def save_leaderboard_plot(leaderboard: Leaderboard, output_path: Path, top_k: int = 10) -> Path:
    entries = leaderboard.top(top_k)
    labels = [e.experiment_id for e in entries]
    values = [e.metric for e in entries]

    if not labels:
        labels = ["none"]
        values = [0.0]

    plt.figure(figsize=(10, 4))
    plt.bar(labels, values)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(leaderboard.metric_name)
    plt.title("Top Experiments")
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    return output_path
