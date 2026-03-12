"""Runs model experiments and computes evaluation metrics on holdout split."""

from __future__ import annotations

import logging
import time
from typing import Dict, Tuple

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from ai_scientist_system.core.dataset_loader import DatasetBundle, DatasetLoader
from ai_scientist_system.experiments.experiment_schema import Experiment, ExperimentResult
from ai_scientist_system.statistics.significance_tests import bootstrap_confidence_intervals
from ai_scientist_system.utils.reproducibility_utils import apply_global_seed

logger = logging.getLogger(__name__)


class ExperimentRunner:
    def __init__(self, dataset_loader: DatasetLoader, datasets: DatasetBundle) -> None:
        self.dataset_loader = dataset_loader
        self.datasets = datasets

    def _build_model(self, experiment: Experiment):
        seed = experiment.seed or 42
        params = dict(experiment.hyperparameters)

        if experiment.model_name == "LogisticRegression":
            c_val = float(params.get("regularization", 1.0))
            return LogisticRegression(C=c_val, random_state=seed, max_iter=1000)
        if experiment.model_name == "RandomForest":
            return RandomForestClassifier(
                n_estimators=int(params.get("n_estimators", 100)),
                max_depth=int(params.get("max_depth", 8)),
                min_samples_split=int(params.get("min_samples_split", 2)),
                random_state=seed,
            )
        if experiment.model_name == "GradientBoosting":
            return GradientBoostingClassifier(
                n_estimators=int(params.get("n_estimators", 100)),
                learning_rate=float(params.get("learning_rate", 0.1)),
                max_depth=int(params.get("max_depth", 3)),
                random_state=seed,
            )
        if experiment.model_name == "DecisionTree":
            return DecisionTreeClassifier(
                max_depth=int(params.get("max_depth", 8)),
                min_samples_split=int(params.get("min_samples_split", 2)),
                random_state=seed,
            )
        if experiment.model_name == "KNN":
            return KNeighborsClassifier(n_neighbors=int(params.get("n_neighbors", 5)))
        raise ValueError(f"Unsupported model: {experiment.model_name}")

    def _feature_importance(self, model, feature_names) -> Dict[str, float]:
        if hasattr(model, "feature_importances_"):
            values = model.feature_importances_
        elif hasattr(model, "coef_"):
            values = np.abs(model.coef_[0])
        else:
            values = np.zeros(len(feature_names))
        return {name: float(val) for name, val in zip(feature_names, values)}

    def run(self, experiment: Experiment) -> ExperimentResult:
        apply_global_seed(experiment.seed or 42)
        t0 = time.time()

        train_x, train_y = self.dataset_loader.split_xy(self.datasets.train)
        val_x, val_y = self.dataset_loader.split_xy(self.datasets.validation)
        holdout_x, holdout_y = self.dataset_loader.split_xy(self.datasets.holdout)

        feature_set = experiment.feature_set or list(train_x.columns)
        train_x = train_x[feature_set]
        val_x = val_x[feature_set]
        holdout_x = holdout_x[feature_set]

        model = self._build_model(experiment)
        model.fit(train_x, train_y)

        _ = model.predict(val_x)

        holdout_pred = model.predict(holdout_x)
        holdout_prob = None
        if hasattr(model, "predict_proba"):
            holdout_prob = model.predict_proba(holdout_x)[:, 1]

        metrics = {
            "accuracy": float(accuracy_score(holdout_y, holdout_pred)),
            "precision": float(precision_score(holdout_y, holdout_pred, zero_division=0)),
            "recall": float(recall_score(holdout_y, holdout_pred, zero_division=0)),
            "f1": float(f1_score(holdout_y, holdout_pred, zero_division=0)),
            "roc_auc": float(roc_auc_score(holdout_y, holdout_prob)) if holdout_prob is not None else 0.5,
        }

        ci = bootstrap_confidence_intervals(
            y_true=holdout_y.to_numpy(),
            y_pred=holdout_pred,
            n_iterations=500,
        )

        runtime = time.time() - t0
        importance = self._feature_importance(model, feature_set)

        logger.info(
            "Experiment %s completed in %.2fs with f1=%.4f",
            experiment.experiment_id,
            runtime,
            metrics["f1"],
        )

        return ExperimentResult(
            experiment_id=experiment.experiment_id,
            model_name=experiment.model_name,
            metrics=metrics,
            runtime_seconds=runtime,
            feature_importance=importance,
            confidence_intervals=ci,
            p_value=1.0,
            passed_statistics=False,
            metadata={"feature_set": feature_set},
        )
