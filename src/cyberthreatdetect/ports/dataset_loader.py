"""
@design-guard
role: Port for loading a dataset into tabular arrays suitable for modeling.
layer: service
non_goals:
- Downloading datasets (separate service).
- Preprocessing/feature scaling (separate port).
boundaries:
depends_on_layers: [domain, ports]
exposes: [TabularDataset, DatasetLoader]
invariants:
- Labels are binary {0,1}.
- Feature matrix is 2D (n_samples, n_features).
authority:
decides: [what a dataset load returns and required shapes]
delegates: [data source specifics to implementations]
extension_policy:
- Add optional metadata fields rather than changing required outputs.
failure_contract:
- Raise FileNotFoundError when raw data is missing.
testing_contract:
- Unit: fake loader returns deterministic arrays.
references:
- docs/adrs/0003-dataset-handling-and-licensing.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


@dataclass(frozen=True)
class TabularDataset:
    x_train: np.ndarray
    y_train: np.ndarray
    x_test: np.ndarray
    y_test: np.ndarray
    feature_names: list[str]


class DatasetLoader(Protocol):
    def load(self) -> TabularDataset: ...
