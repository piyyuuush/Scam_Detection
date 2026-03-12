"""
@design-guard
role: Orchestrates dataset loading, preprocessing, training, evaluation, and artifact persistence for a run.
layer: service
non_goals:
- CLI parsing or Streamlit UI.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [ExperimentRunner]
invariants:
- Fit preprocessing on train only.
- Persist config + metrics per run.
authority:
decides: [execution order and cross-service coordination]
delegates: [details to ports]
extension_policy:
- Add new model families by adding trainers; keep orchestration generic.
failure_contract:
- Raise exceptions when required ports fail; do not swallow errors.
testing_contract:
- Integration: run on fixture dataset creates artifacts and returns summary.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cyberthreatdetect.domain.types import Metrics, RunConfig, RunSummary
from cyberthreatdetect.ports.artifacts import ArtifactStore
from cyberthreatdetect.ports.evaluator import Evaluator
from cyberthreatdetect.ports.preprocessing import TabularPreprocessorFactory
from cyberthreatdetect.ports.trainer import Trainer
from cyberthreatdetect.services.datasets.registry import DatasetRegistry
from cyberthreatdetect.services.reporting import make_confusion_matrix_fig, make_roc_curve_fig


@dataclass(frozen=True)
class ExperimentRunner:
    dataset_registry: DatasetRegistry
    preprocessor_factory: TabularPreprocessorFactory
    trainers: dict[str, Trainer]
    evaluator: Evaluator
    artifact_store: ArtifactStore

    def run(self, *, config: RunConfig) -> RunSummary:
        run_dir = self.artifact_store.prepare_run_dir(run_id=config.run_id)
        self.artifact_store.write_config(run_dir=run_dir, config=config)

        loader = self.dataset_registry.get(dataset_id=config.dataset_id, split=config.split)
        ds = loader.load()

        preprocessor = self.preprocessor_factory.create(
            dataset_id=config.dataset_id, feature_names=ds.feature_names
        )
        x_train = preprocessor.fit_transform(ds.x_train)
        x_test = preprocessor.transform(ds.x_test)

        metrics_list: list[Metrics] = []
        for spec in config.models:
            trainer = self.trainers[spec.model_id]
            model = trainer.train(x_train=x_train, y_train=ds.y_train, spec=spec, seed=config.seed)
            y_proba = model.predict_proba(x_test)
            metrics = self.evaluator.evaluate(
                model_id=spec.model_id, y_true=ds.y_test, y_proba=y_proba
            )
            metrics_list.append(metrics)

            cm_fig = make_confusion_matrix_fig(y_true=ds.y_test, y_proba=y_proba)
            self.artifact_store.write_plot(
                run_dir=run_dir, filename=f"confusion_matrix_{spec.model_id}.png", fig=cm_fig
            )
            roc_fig = make_roc_curve_fig(y_true=ds.y_test, y_proba=y_proba)
            if roc_fig is not None:
                self.artifact_store.write_plot(
                    run_dir=run_dir, filename=f"roc_curve_{spec.model_id}.png", fig=roc_fig
                )

        self.artifact_store.write_metrics(run_dir=run_dir, metrics=metrics_list)

        return RunSummary(
            run_id=config.run_id,
            dataset_id=config.dataset_id,
            metrics=metrics_list,
            artifacts_dir=str(Path(run_dir).resolve()),
        )
