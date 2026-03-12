"""Deterministic hashing utilities for experiments and dataset signatures."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterable


def stable_hash(payload: Any) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def experiment_hash(model: str, features: Iterable[str], hyperparameters: Dict[str, Any]) -> str:
    payload = {
        "model": model,
        "features": sorted(list(features)),
        "hyperparameters": hyperparameters,
    }
    return stable_hash(payload)
