"""
@design-guard
role: Registry mapping dataset ids to loader factories and download metadata.
layer: service
non_goals:
- Performing model training or evaluation.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [DatasetRegistry]
invariants:
- Registry is the only entry point for selecting dataset loaders by id.
authority:
decides: [supported datasets and their loader selection rules]
delegates: [loading logic to DatasetLoader implementations]
extension_policy:
- Add new dataset via a new loader and register it here.
failure_contract:
- Raise KeyError for unknown dataset ids.
testing_contract:
- Unit: registry returns the expected loader for each dataset id.
references:
- docs/adrs/0003-dataset-handling-and-licensing.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cyberthreatdetect.domain.types import DatasetId, DatasetSplit
from cyberthreatdetect.ports.dataset_loader import DatasetLoader
from cyberthreatdetect.services.datasets.stub_loaders import (
    FixtureTabularDatasetLoader,
    NslKddDatasetLoader,
    PhiUsiilDatasetLoader,
)


@dataclass(frozen=True)
class DatasetRegistry:
    data_dir: Path

    @classmethod
    def default(cls, *, data_dir: Path) -> DatasetRegistry:
        return cls(data_dir=data_dir)

    def get(self, *, dataset_id: DatasetId, split: DatasetSplit) -> DatasetLoader:
        _ = split
        match dataset_id:
            case "nsl_kdd":
                return NslKddDatasetLoader(data_dir=self.data_dir)
            case "phiusiil":
                return PhiUsiilDatasetLoader(data_dir=self.data_dir)
            case "fixture_tabular":
                return FixtureTabularDatasetLoader(data_dir=self.data_dir)
        raise KeyError(f"Unknown dataset_id: {dataset_id}")
