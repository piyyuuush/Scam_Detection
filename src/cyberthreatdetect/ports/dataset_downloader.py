"""
@design-guard
role: Port for downloading raw datasets and writing provenance metadata.
layer: service
non_goals:
- Parsing datasets into model-ready arrays.
boundaries:
depends_on_layers: [domain, ports]
exposes: [DatasetDownloader]
invariants:
- Downloaded data is stored under data/raw/<dataset_id>/.
authority:
decides: [minimum downloader interface used by facade/UI]
delegates: [URL details and IO to implementations]
extension_policy:
- Add new datasets without changing the interface.
failure_contract:
- Raise ValueError for unknown dataset ids; raise OSError/network errors for failures.
testing_contract:
- Unit: unknown id fails; integration tests should not hit network.
references:
- docs/adrs/0003-dataset-handling-and-licensing.md
"""

from __future__ import annotations

from typing import Protocol


class DatasetDownloader(Protocol):
    def download(self, *, dataset_id: str) -> None: ...
