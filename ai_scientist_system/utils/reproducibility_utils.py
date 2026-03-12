"""Utilities that enforce deterministic, reproducible experiments."""

from __future__ import annotations

import os
import random
import subprocess
from dataclasses import asdict
from typing import Dict

import numpy as np

from ai_scientist_system.experiments.experiment_schema import Experiment


def deterministic_seed(experiment_id: str) -> int:
    """Generate the canonical deterministic seed from experiment id."""

    return hash(experiment_id) % (2**32)


def apply_global_seed(seed: int) -> None:
    """Set seed for random, numpy and hash seed."""

    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)


def current_code_version() -> str:
    """Return short git SHA if available."""

    try:
        result = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        return result.decode("utf-8").strip()
    except Exception:
        return "unknown"


def attach_reproducibility_metadata(experiment: Experiment, dataset_hash: str) -> Experiment:
    """Populate required reproducibility fields on the experiment record."""

    experiment.seed = deterministic_seed(experiment.experiment_id)
    experiment.dataset_hash = dataset_hash
    experiment.code_version = current_code_version()
    return experiment


def reproducibility_record(experiment: Experiment) -> Dict[str, str]:
    """Structured reproducibility payload used in reports and checkpoints."""

    keys = ["seed", "model_version", "dataset_hash", "code_version", "experiment_id"]
    payload = asdict(experiment)
    return {k: str(payload.get(k, "")) for k in keys}
