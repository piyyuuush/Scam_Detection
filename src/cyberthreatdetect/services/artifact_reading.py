"""
@design-guard
role: Read experiment run artifacts from the filesystem for comparison and UI display.
layer: service
non_goals:
- Writing artifacts (ArtifactStore responsibility).
- Training or evaluation.
boundaries:
depends_on_layers: [domain, service]
exposes: [list_run_dirs, read_run_config, read_run_metrics_table]
invariants:
- Reading is side-effect free.
authority:
decides: [how artifacts are interpreted into typed configs and tabular metrics]
delegates: [UI presentation to ui layer]
extension_policy:
- Extend by adding new readers for new artifact files.
failure_contract:
- Raise FileNotFoundError for missing run folders/files; ValueError for malformed content.
testing_contract:
- Unit: read functions work against a temp folder with minimal artifacts.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from cyberthreatdetect.domain.types import RunConfig


def list_run_dirs(*, artifacts_root: Path) -> list[Path]:
    runs_dir = artifacts_root / "runs"
    if not runs_dir.exists():
        return []
    return sorted([p for p in runs_dir.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)


def read_run_config(*, run_dir: Path) -> RunConfig:
    config_path = run_dir / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config.json in {run_dir}")
    return RunConfig.model_validate_json(config_path.read_text(encoding="utf-8"))


def read_run_metrics_table(*, run_dir: Path) -> pd.DataFrame:
    metrics_csv = run_dir / "metrics.csv"
    if metrics_csv.exists():
        return pd.read_csv(metrics_csv)

    metrics_json = run_dir / "metrics.json"
    if metrics_json.exists():
        return pd.read_json(metrics_json)

    raise FileNotFoundError(f"Missing metrics.csv/metrics.json in {run_dir}")
