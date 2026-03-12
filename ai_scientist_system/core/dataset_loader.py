"""Dataset loading and integrity checks for scientific validity."""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from ai_scientist_system.config.settings import DataSettings

logger = logging.getLogger(__name__)


@dataclass
class DatasetBundle:
    train: pd.DataFrame
    validation: pd.DataFrame
    holdout: pd.DataFrame
    target_column: str
    dataset_hash: str


class DatasetIntegrityError(ValueError):
    pass


class DatasetLoader:
    def __init__(self, settings: DataSettings) -> None:
        self.settings = settings

    def _path(self, filename: str) -> Path:
        return self.settings.data_dir / filename

    def load_datasets(self) -> DatasetBundle:
        train = pd.read_csv(self._path(self.settings.train_file))
        validation = pd.read_csv(self._path(self.settings.validation_file))
        holdout = pd.read_csv(self._path(self.settings.holdout_file))

        self.validate_splits(train, validation, holdout)
        ds_hash = self.compute_dataset_hash(train, validation, holdout)
        self.detect_leakage(train, validation, holdout)

        logger.info("Loaded datasets with hash %s", ds_hash)
        return DatasetBundle(
            train=train,
            validation=validation,
            holdout=holdout,
            target_column=self.settings.target_column,
            dataset_hash=ds_hash,
        )

    def validate_splits(
        self,
        train: pd.DataFrame,
        validation: pd.DataFrame,
        holdout: pd.DataFrame,
    ) -> None:
        frames = {"train": train, "validation": validation, "holdout": holdout}
        columns = [set(df.columns) for df in frames.values()]
        if not all(col == columns[0] for col in columns[1:]):
            raise DatasetIntegrityError("Dataset splits must have identical columns")

        if self.settings.target_column not in train.columns:
            raise DatasetIntegrityError(
                f"Target column '{self.settings.target_column}' missing from dataset"
            )

        for name, df in frames.items():
            if df.empty:
                raise DatasetIntegrityError(f"{name} split is empty")

    def compute_dataset_hash(
        self,
        train: pd.DataFrame,
        validation: pd.DataFrame,
        holdout: pd.DataFrame,
    ) -> str:
        hasher = hashlib.sha256()
        for df in (train, validation, holdout):
            hasher.update(pd.util.hash_pandas_object(df, index=True).values.tobytes())
        return hasher.hexdigest()

    def detect_leakage(
        self,
        train: pd.DataFrame,
        validation: pd.DataFrame,
        holdout: pd.DataFrame,
    ) -> None:
        """Simple leakage checks using optional id and exact row overlaps."""

        overlap_stats: Dict[str, int] = {}

        if self.settings.id_column and self.settings.id_column in train.columns:
            tid = set(train[self.settings.id_column])
            vid = set(validation[self.settings.id_column])
            hid = set(holdout[self.settings.id_column])
            overlap_stats["train_validation"] = len(tid & vid)
            overlap_stats["train_holdout"] = len(tid & hid)
            overlap_stats["validation_holdout"] = len(vid & hid)
        else:
            signatures = {
                "train": set(pd.util.hash_pandas_object(train, index=False).astype(str)),
                "validation": set(pd.util.hash_pandas_object(validation, index=False).astype(str)),
                "holdout": set(pd.util.hash_pandas_object(holdout, index=False).astype(str)),
            }
            overlap_stats["train_validation"] = len(signatures["train"] & signatures["validation"])
            overlap_stats["train_holdout"] = len(signatures["train"] & signatures["holdout"])
            overlap_stats["validation_holdout"] = len(
                signatures["validation"] & signatures["holdout"]
            )

        leaks = {name: count for name, count in overlap_stats.items() if count > 0}
        if leaks:
            raise DatasetIntegrityError(f"Potential leakage detected: {leaks}")

    def split_xy(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        y = df[self.settings.target_column]
        x = df.drop(columns=[self.settings.target_column])
        return x, y

    def feature_columns(self, train_df: pd.DataFrame) -> List[str]:
        return [col for col in train_df.columns if col != self.settings.target_column]
