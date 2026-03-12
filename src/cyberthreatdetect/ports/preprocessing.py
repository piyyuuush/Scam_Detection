"""
@design-guard
role: Port for preprocessing tabular features in a train/test-safe manner.
layer: service
non_goals:
- Owning dataset loading or model training.
boundaries:
depends_on_layers: [domain, ports]
exposes: [Preprocessor, TabularPreprocessorFactory]
invariants:
- fit happens only on training data; transform applies same mapping to test data.
authority:
decides: [shape and lifecycle of preprocessors]
delegates: [specific algorithms to implementations]
extension_policy:
- Extend by adding new factories rather than specializing callers.
failure_contract:
- Raise ValueError for mismatched feature shapes.
testing_contract:
- Unit: deterministic transform outputs given fixed input.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from typing import Protocol

import numpy as np


class Preprocessor(Protocol):
    def fit_transform(self, x_train: np.ndarray) -> np.ndarray: ...

    def transform(self, x_test: np.ndarray) -> np.ndarray: ...


class TabularPreprocessorFactory(Protocol):
    def create(self, *, dataset_id: str, feature_names: list[str]) -> Preprocessor: ...
