"""
@design-guard
role: Integration tests for running an experiment and producing artifacts.
layer: ui
non_goals:
- Network downloads (must not run in CI).
boundaries:
depends_on_layers: [facade, service]
exposes: [tests]
invariants:
- A run creates config/metrics files and at least a confusion matrix plot per model.
authority:
decides: [minimal artifact contract enforced in CI]
delegates: [unit correctness to unit tests]
extension_policy:
- Extend assertions when new artifact types are added.
failure_contract:
- Failures indicate broken orchestration or artifact writing.
testing_contract:
- Integration.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from pathlib import Path

from cyberthreatdetect.bootstrap import build_facade
from cyberthreatdetect.domain.types import DatasetSplit, ModelSpec, RunConfig


def _write_fixture_csv(*, out_dir: Path) -> None:
    fixtures = out_dir / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    (fixtures / "tabular_binary.csv").write_text(
        "f1,f2,f3,f4,label\n"
        "0.1,1.2,0.0,3.1,0\n"
        "0.2,1.1,0.1,3.0,0\n"
        "0.15,1.3,0.0,3.2,0\n"
        "0.05,1.0,0.2,2.9,0\n"
        "1.1,2.2,1.0,4.1,1\n"
        "1.2,2.1,1.1,4.0,1\n"
        "1.15,2.3,1.0,4.2,1\n"
        "1.05,2.0,1.2,3.9,1\n",
        encoding="utf-8",
    )


def test_facade_run_writes_artifacts_rf(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    artifacts_dir = tmp_path / "artifacts"
    _write_fixture_csv(out_dir=data_dir)

    facade = build_facade(data_dir=data_dir, artifacts_dir=artifacts_dir)
    cfg = RunConfig(
        run_id="test_run_rf",
        dataset_id="fixture_tabular",
        split=DatasetSplit(kind="random_stratified_split", test_size=0.25),
        models=[ModelSpec(model_id="rf", rf_n_estimators=10)],
        seed=1337,
        artifacts_root=str(artifacts_dir),
    )
    summary = facade.run_experiment(config=cfg)
    run_dir = Path(summary.artifacts_dir)

    assert (run_dir / "config.json").exists()
    assert (run_dir / "metrics.csv").exists()
    assert (run_dir / "confusion_matrix_rf.png").exists()


def test_facade_run_writes_artifacts_torch_models(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    artifacts_dir = tmp_path / "artifacts"
    _write_fixture_csv(out_dir=data_dir)

    facade = build_facade(data_dir=data_dir, artifacts_dir=artifacts_dir)
    cfg = RunConfig(
        run_id="test_run_torch",
        dataset_id="fixture_tabular",
        split=DatasetSplit(kind="random_stratified_split", test_size=0.25),
        models=[
            ModelSpec(model_id="cnn", max_epochs=1, batch_size=2),
            ModelSpec(model_id="lstm", max_epochs=1, batch_size=2),
        ],
        seed=1337,
        artifacts_root=str(artifacts_dir),
    )
    summary = facade.run_experiment(config=cfg)
    run_dir = Path(summary.artifacts_dir)

    assert (run_dir / "config.json").exists()
    assert (run_dir / "metrics.csv").exists()
    assert (run_dir / "confusion_matrix_cnn.png").exists()
    assert (run_dir / "confusion_matrix_lstm.png").exists()
