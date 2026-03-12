"""Paper writer agent that drafts concise research summaries."""

from __future__ import annotations

from ai_scientist_system.core.gemini_client import GeminiClient
from ai_scientist_system.memory.research_memory import ResearchMemory


class PaperWriterAgent:
    def __init__(self, llm: GeminiClient) -> None:
        self.llm = llm

    def write(self, goal: str, memory: ResearchMemory) -> str:
        top_entries = memory.top_results(k=5)
        summary_lines = []
        for entry in top_entries:
            score = entry.result["metrics"].get("f1", 0.0)
            summary_lines.append(
                f"- {entry.experiment['experiment_id']} | {entry.experiment['model_name']} | f1={score:.4f}"
            )

        prompt = (
            "Write a compact scientific draft with abstract, method, results, and limitations.\n"
            f"Goal: {goal}\nTop results:\n" + "\n".join(summary_lines)
        )
        return self.llm.generate(prompt)
