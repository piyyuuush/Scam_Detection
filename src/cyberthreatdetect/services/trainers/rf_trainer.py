"""
@design-guard
role: RandomForest baseline trainer using scikit-learn for tabular threat detection.
layer: service
non_goals:
- Deep learning architectures.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [RandomForestTrainer]
invariants:
- Predict returns positive-class probability for each sample.
authority:
decides: [baseline hyperparameter defaults]
delegates: [evaluation to evaluator]
extension_policy:
- Adjust defaults via ModelSpec fields; avoid adding ad-hoc parameters.
failure_contract:
- Raise ValueError on invalid input shapes.
testing_contract:
- Unit: trains on tiny synthetic data and predicts correct shape.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from cyberthreatdetect.domain.types import ModelSpec


@dataclass(frozen=True)
class _SklearnProbaModel:
    clf: RandomForestClassifier

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        proba = self.clf.predict_proba(x)
        return np.asarray(proba[:, 1], dtype=np.float32)


class RandomForestTrainer:
    def train(
        self, *, x_train: np.ndarray, y_train: np.ndarray, spec: ModelSpec, seed: int
    ) -> _SklearnProbaModel:
        if x_train.ndim != 2 or y_train.ndim != 1:
            raise ValueError("Expected x_train as 2D and y_train as 1D.")
        clf = RandomForestClassifier(
            n_estimators=spec.rf_n_estimators,
            max_depth=spec.rf_max_depth,
            random_state=seed,
            n_jobs=-1,
        )
        clf.fit(x_train, y_train)
        return _SklearnProbaModel(clf=clf)
