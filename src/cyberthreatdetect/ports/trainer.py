"""
@design-guard
role: Port for model training given preprocessed features and labels.
layer: service
non_goals:
- Metrics computation (evaluator port).
- Artifact persistence (artifact store port).
boundaries:
depends_on_layers: [domain, ports]
exposes: [TrainedModel, Trainer]
invariants:
- Predict returns probabilities for positive class, shape (n_samples,).
authority:
decides: [minimal interface for trained models and trainers]
delegates: [algorithm specifics to implementations]
extension_policy:
- Add new trainers by implementing this port and registering in bootstrap.
failure_contract:
- Raise ValueError for invalid inputs; surface training failures as RuntimeError.
testing_contract:
- Unit: trainer returns model that can predict with correct shape.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from typing import Protocol

import numpy as np

from cyberthreatdetect.domain.types import ModelSpec


class TrainedModel(Protocol):
    def predict_proba(self, x: np.ndarray) -> np.ndarray: ...


class Trainer(Protocol):
    def train(
        self, *, x_train: np.ndarray, y_train: np.ndarray, spec: ModelSpec, seed: int
    ) -> TrainedModel: ...
