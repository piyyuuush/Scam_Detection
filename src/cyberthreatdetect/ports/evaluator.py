"""
@design-guard
role: Port for evaluating binary classifiers and producing comparable metrics.
layer: service
non_goals:
- Training models or storing artifacts.
boundaries:
depends_on_layers: [domain, ports]
exposes: [Evaluator]
invariants:
- Input labels are binary {0,1}.
- Probabilities are in [0,1] with shape (n_samples,).
authority:
decides: [standard metric set used across models/datasets]
delegates: [metric implementation details to services]
extension_policy:
- Add metrics carefully to keep comparability.
failure_contract:
- Raise ValueError on invalid shapes.
testing_contract:
- Unit: metric outputs match known values on small arrays.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from typing import Protocol

import numpy as np

from cyberthreatdetect.domain.types import Metrics, ModelId


class Evaluator(Protocol):
    def evaluate(
        self, *, model_id: ModelId, y_true: np.ndarray, y_proba: np.ndarray
    ) -> Metrics: ...
