"""
@design-guard
role: Composition root that wires implementations to ports and exposes a facade factory.
layer: facade
non_goals:
- Owning business logic (lives in services/facade).
- Performing training or dataset downloads on import.
boundaries:
depends_on_layers: [domain, ports, services, facade]
exposes: [build_facade]
invariants:
- No global singletons; wiring happens per call for testability.
authority:
decides: [which concrete implementations satisfy each port]
delegates: [runtime orchestration to the facade]
extension_policy:
- Add new ports/implementations via wiring here; avoid bypassing ports from ui.
failure_contract:
- Fail fast with clear errors if required dependencies/config are missing.
testing_contract:
- Integration: build_facade returns a working facade using temp directories/fixtures.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from pathlib import Path

from cyberthreatdetect.facade.cyberthreatdetect_facade import CyberThreatDetectFacade
from cyberthreatdetect.ports.trainer import Trainer
from cyberthreatdetect.services.artifacts import FileSystemArtifactStore
from cyberthreatdetect.services.datasets.download import HttpDatasetDownloader
from cyberthreatdetect.services.datasets.registry import DatasetRegistry
from cyberthreatdetect.services.experiment_runner import ExperimentRunner
from cyberthreatdetect.services.metrics import SklearnBinaryClassifierEvaluator
from cyberthreatdetect.services.preprocessing import SklearnTabularPreprocessorFactory
from cyberthreatdetect.services.trainers.rf_trainer import RandomForestTrainer
from cyberthreatdetect.services.trainers.torch_cnn_trainer import TorchCnnTrainer
from cyberthreatdetect.services.trainers.torch_lstm_trainer import TorchLstmTrainer


def build_facade(*, data_dir: Path, artifacts_dir: Path) -> CyberThreatDetectFacade:
    dataset_registry = DatasetRegistry.default(data_dir=data_dir)
    preprocessor_factory = SklearnTabularPreprocessorFactory()
    evaluator = SklearnBinaryClassifierEvaluator()
    artifact_store = FileSystemArtifactStore(root_dir=artifacts_dir)
    dataset_downloader = HttpDatasetDownloader(data_dir=data_dir)

    trainers: dict[str, Trainer] = {
        "rf": RandomForestTrainer(),
        "cnn": TorchCnnTrainer(),
        "lstm": TorchLstmTrainer(),
    }

    runner = ExperimentRunner(
        dataset_registry=dataset_registry,
        preprocessor_factory=preprocessor_factory,
        trainers=trainers,
        evaluator=evaluator,
        artifact_store=artifact_store,
    )

    return CyberThreatDetectFacade(experiment_runner=runner, dataset_downloader=dataset_downloader)
