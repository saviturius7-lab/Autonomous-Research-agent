"""Novelty metrics for hypotheses, including diversity safeguards."""

from __future__ import annotations

import math
import random
from collections import Counter
from typing import Iterable, List, Sequence

import numpy as np

from ai_scientist_system.experiments.experiment_schema import Hypothesis


def _token_embedding(text: str, dim: int = 128) -> np.ndarray:
    """Lightweight deterministic text embedding based on hashed token counts."""

    vec = np.zeros(dim, dtype=float)
    tokens = [token.lower() for token in text.split() if token.strip()]
    counts = Counter(tokens)
    for token, count in counts.items():
        index = hash(token) % dim
        vec[index] += float(count)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 1.0
    cosine_sim = float(np.dot(a, b) / denom)
    return 1.0 - max(-1.0, min(1.0, cosine_sim))


def novelty_score(new_hypothesis: str, previous_hypotheses: Sequence[str]) -> float:
    """Score novelty as average cosine distance to previous hypotheses."""

    if not previous_hypotheses:
        return 1.0

    new_vec = _token_embedding(new_hypothesis)
    distances = [cosine_distance(new_vec, _token_embedding(prev)) for prev in previous_hypotheses]
    return float(np.mean(distances))


def filter_novel_hypotheses(
    hypotheses: Sequence[Hypothesis],
    previous_hypotheses: Sequence[str],
    threshold: float,
    exploration_ratio: float,
) -> List[Hypothesis]:
    """Reject low-novelty hypotheses while ensuring exploration budget."""

    accepted: List[Hypothesis] = []
    running_history = list(previous_hypotheses)

    for hyp in hypotheses:
        score = novelty_score(hyp.text, running_history)
        hyp.novelty_score = score
        if score >= threshold:
            accepted.append(hyp)
            running_history.append(hyp.text)

    if not hypotheses:
        return accepted

    minimum_exploration = math.ceil(len(hypotheses) * exploration_ratio)
    exploration_candidates = [h for h in hypotheses if h.exploration and h not in accepted]
    random.shuffle(exploration_candidates)

    current_exploration = sum(1 for h in accepted if h.exploration)
    needed = max(0, minimum_exploration - current_exploration)
    accepted.extend(exploration_candidates[:needed])
    return accepted
