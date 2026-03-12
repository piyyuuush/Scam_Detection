"""
@design-guard
role: Evaluator implementation producing a consistent set of binary classification metrics.
layer: service
non_goals:
- Plot rendering (separate reporting utilities).
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [SklearnBinaryClassifierEvaluator]
invariants:
- Threshold for class prediction is 0.5 when required.
authority:
decides: [metric definitions and computation approach]
delegates: [model training to trainers; artifact persistence to store]
extension_policy:
- Add metrics only if universally applicable across datasets/models.
failure_contract:
- Raise ValueError on invalid shapes or values.
testing_contract:
- Unit: metrics computed correctly on small known arrays.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from cyberthreatdetect.domain.types import Metrics, ModelId


class SklearnBinaryClassifierEvaluator:
    def evaluate(self, *, model_id: ModelId, y_true: np.ndarray, y_proba: np.ndarray) -> Metrics:
        if y_true.ndim != 1 or y_proba.ndim != 1:
            raise ValueError("Expected 1D arrays for y_true and y_proba.")
        if y_true.shape[0] != y_proba.shape[0]:
            raise ValueError("y_true and y_proba must have the same length.")

        y_pred = (y_proba >= 0.5).astype(int)

        roc_auc: float | None
        try:
            roc_auc_value = float(roc_auc_score(y_true, y_proba))
            roc_auc = roc_auc_value if np.isfinite(roc_auc_value) else None
        except ValueError:
            roc_auc = None

        return Metrics(
            model_id=model_id,
            accuracy=float(accuracy_score(y_true, y_pred)),
            precision=float(precision_score(y_true, y_pred, zero_division=0)),
            recall=float(recall_score(y_true, y_pred, zero_division=0)),
            f1=float(f1_score(y_true, y_pred, zero_division=0)),
            roc_auc=roc_auc,
        )
