"""
@design-guard
role: Preprocessing implementations for tabular cybersecurity datasets using scikit-learn.
layer: service
non_goals:
- Dataset download or parsing.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [SklearnPreprocessor, SklearnTabularPreprocessorFactory]
invariants:
- Fit uses training data only.
- Output is a dense float32 numpy array for compatibility with torch trainers.
authority:
decides: [standard scaling/encoding approach for tabular features]
delegates: [dataset-specific parsing to dataset loaders]
extension_policy:
- Add dataset-specific preprocessing policies via factory branching.
failure_contract:
- Raise ValueError on invalid inputs.
testing_contract:
- Unit: deterministic transformations for a fixed input.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.preprocessing import StandardScaler


@dataclass
class SklearnPreprocessor:
    scaler: StandardScaler

    def fit_transform(self, x_train: np.ndarray) -> np.ndarray:
        x = self.scaler.fit_transform(x_train)
        return np.asarray(x, dtype=np.float32)

    def transform(self, x_test: np.ndarray) -> np.ndarray:
        x = self.scaler.transform(x_test)
        return np.asarray(x, dtype=np.float32)


class SklearnTabularPreprocessorFactory:
    def create(self, *, dataset_id: str, feature_names: list[str]) -> SklearnPreprocessor:
        _ = (dataset_id, feature_names)
        return SklearnPreprocessor(scaler=StandardScaler())
