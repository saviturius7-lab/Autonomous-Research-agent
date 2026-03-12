"""Cost-aware Gemini client with key rotation and retry logic."""

from __future__ import annotations

import itertools
import json
import logging
import time
import urllib.error
import urllib.parse
import urllib.request
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
    """REST Gemini client with API key rotation and retry logic."""
    """Minimal client wrapper.

    This class is intentionally SDK-agnostic: replace `_invoke_provider` for real API calls.
    """

    def __init__(self, api_keys: Iterable[str], model_name: str) -> None:
        keys = [k for k in api_keys if k]
        if not keys:
            raise GeminiClientError("No Gemini API keys configured")
        self._keys = keys
            logger.warning("No GEMINI_KEY_* variables configured; running in mock mode.")
        self._keys = keys or ["MOCK_KEY"]
        self._key_cycle = itertools.cycle(self._keys)
        self.model_name = model_name
        self.usage = GeminiUsage()

    def _request(self, prompt: str, key: str, timeout_s: int = 30) -> str:
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model_name}:generateContent"
        )
        params = urllib.parse.urlencode({"key": key})
        url = f"{endpoint}?{params}"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code == 429:
                raise GeminiClientError("rate_limited") from exc
            raise GeminiClientError(
                f"gemini_request_failed status={exc.code} body={body[:500]}"
            ) from exc
        except urllib.error.URLError as exc:
            raise GeminiClientError(f"network_error: {exc}") from exc

        response = json.loads(body)
        candidates = response.get("candidates") or []
        if not candidates:
            raise GeminiClientError(f"no_candidates_in_response: {response}")

        parts = candidates[0].get("content", {}).get("parts", [])
        text_parts = [p.get("text", "") for p in parts if isinstance(p, dict)]
        output = "\n".join(part for part in text_parts if part).strip()
        if not output:
            raise GeminiClientError(f"empty_text_response: {response}")
        return output

    def generate(self, prompt: str, max_retries: int = 6) -> str:
        last_error: Optional[Exception] = None

        for attempt in range(max_retries):
            key = next(self._key_cycle)
            try:
                response = self._request(prompt, key)
                self.usage.total_calls += 1
                self.usage.estimated_cost_usd += 0.002
                return response
            except GeminiClientError as exc:
                last_error = exc
                logger.warning("Gemini call failed on attempt %s: %s", attempt + 1, exc)
                time.sleep(min(2.5, 0.5 * (attempt + 1)))
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
