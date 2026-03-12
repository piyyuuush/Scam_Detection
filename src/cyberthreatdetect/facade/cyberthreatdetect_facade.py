"""
@design-guard
role: Application facade to run experiments and return summaries for UI consumption.
layer: facade
non_goals:
- Implement training/dataset logic.
boundaries:
depends_on_layers: [domain, ports, service, facade]
exposes: [CyberThreatDetectFacade]
invariants:
- Orchestration is delegated to the ExperimentRunner service.
authority:
decides: [public orchestration surface for UI]
delegates: [execution to ExperimentRunner]
extension_policy:
- Add new public use-cases here; do not expose underlying services.
failure_contract:
- Raise exceptions with user-actionable messages on missing data/config.
testing_contract:
- Integration: run_experiment returns metrics and artifact locations.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from dataclasses import dataclass

from cyberthreatdetect.domain.types import RunConfig, RunSummary
from cyberthreatdetect.ports.dataset_downloader import DatasetDownloader
from cyberthreatdetect.services.experiment_runner import ExperimentRunner


@dataclass(frozen=True)
class CyberThreatDetectFacade:
    experiment_runner: ExperimentRunner
    dataset_downloader: DatasetDownloader

    def run_experiment(self, *, config: RunConfig) -> RunSummary:
        return self.experiment_runner.run(config=config)

    def download_dataset(self, *, dataset_id: str) -> None:
        self.dataset_downloader.download(dataset_id=dataset_id)
