"""Literature review agent for framing research directions."""

from __future__ import annotations

from ai_scientist_system.core.gemini_client import GeminiClient


class LiteratureAgent:
    def __init__(self, llm: GeminiClient) -> None:
        self.llm = llm

    def summarize(self, goal: str) -> str:
        prompt = (
            "You are a rigorous research librarian. Summarize likely modeling baselines, "
            "leakage risks, and statistically robust evaluation practices for this goal:\n"
            f"{goal}"
        )
        return self.llm.generate(prompt)
