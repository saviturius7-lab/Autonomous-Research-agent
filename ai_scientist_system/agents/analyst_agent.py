"""Analyst agent extracts statistically valid patterns from memory."""

from __future__ import annotations

from collections import Counter
from typing import Dict, List

from ai_scientist_system.memory.research_memory import ResearchMemory


class AnalystAgent:
    def analyze(self, memory: ResearchMemory) -> Dict[str, List[str]]:
        valid_entries = [
            e
            for e in memory.entries
            if bool(e.result.get("passed_statistics", False))
        ]
        feature_counter = Counter()
        model_counter = Counter()
        interactions = Counter()

        for entry in valid_entries:
            model_counter[entry.experiment["model_name"]] += 1
            features = entry.experiment["feature_set"]
            for f in features:
                feature_counter[f] += 1
            for i, feat_a in enumerate(features):
                for feat_b in features[i + 1 :]:
                    interactions[(feat_a, feat_b)] += 1

        return {
            "top_features": [f"{name}:{count}" for name, count in feature_counter.most_common(10)],
            "top_models": [f"{name}:{count}" for name, count in model_counter.most_common(5)],
            "feature_interactions": [
                f"{a}&{b}:{count}" for (a, b), count in interactions.most_common(10)
            ],
        }
