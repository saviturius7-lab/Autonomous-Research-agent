"""Planning agent that proposes focused experimental directions."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from ai_scientist_system.core.gemini_client import GeminiClient


@dataclass
class ResearchDirection:
    title: str
    objective: str


class PlannerAgent:
    def __init__(self, llm: GeminiClient) -> None:
        self.llm = llm

    def plan(self, goal: str, literature_summary: str) -> ResearchDirection:
        prompt = (
            "Given the research goal and summary, produce one high-value direction "
            "that is testable and low-bias.\n"
            f"Goal: {goal}\nSummary: {literature_summary[:1200]}"
        )
        response = self.llm.generate(prompt)
        title = random.choice(
            [
                "Feature stability exploration",
                "Model class comparison",
                "Interaction discovery",
                "Regularization sensitivity",
            ]
        )
        return ResearchDirection(title=title, objective=response[:1000])
