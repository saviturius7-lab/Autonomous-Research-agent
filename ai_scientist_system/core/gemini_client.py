"""Cost-aware Gemini client with key rotation and retry logic."""

from __future__ import annotations

import itertools
import logging
import time
from dataclasses import dataclass
from typing import Iterable, Optional

logger = logging.getLogger(__name__)


class GeminiClientError(RuntimeError):
    pass


@dataclass
class GeminiUsage:
    total_calls: int = 0
    estimated_cost_usd: float = 0.0


class GeminiClient:
    """Minimal client wrapper.

    This class is intentionally SDK-agnostic: replace `_invoke_provider` for real API calls.
    """

    def __init__(self, api_keys: Iterable[str], model_name: str) -> None:
        keys = [k for k in api_keys if k]
        if not keys:
            logger.warning("No GEMINI_KEY_* variables configured; running in mock mode.")
        self._keys = keys or ["MOCK_KEY"]
        self._key_cycle = itertools.cycle(self._keys)
        self.model_name = model_name
        self.usage = GeminiUsage()

    def _invoke_provider(self, prompt: str, key: str) -> str:
        """Provider call placeholder.

        In production, integrate google-generativeai and return text response.
        """

        if key == "MOCK_KEY":
            return f"[MOCK GEMINI RESPONSE]\n{prompt[:500]}"
        return f"[SIMULATED GEMINI:{self.model_name}] {prompt[:500]}"

    def generate(self, prompt: str, max_retries: int = 3) -> str:
        last_error: Optional[Exception] = None
        for attempt in range(max_retries):
            key = next(self._key_cycle)
            try:
                response = self._invoke_provider(prompt, key)
                self.usage.total_calls += 1
                self.usage.estimated_cost_usd += 0.002
                return response
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                logger.warning("Gemini call failed on attempt %s: %s", attempt + 1, exc)
                time.sleep(0.5 * (attempt + 1))
                continue

        raise GeminiClientError(f"Failed after {max_retries} attempts: {last_error}")
