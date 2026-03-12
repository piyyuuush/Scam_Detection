"""
@design-guard
role: Filesystem artifact store for experiment outputs under artifacts/runs/<run_id>/.
layer: service
non_goals:
- Cloud storage integrations.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [FileSystemArtifactStore]
invariants:
- Writes are confined to the configured root directory.
authority:
decides: [filesystem layout and file formats for artifacts]
delegates: [plot creation to evaluation/reporting services]
extension_policy:
- Add new files with backward-compatible names; avoid changing existing artifact formats.
failure_contract:
- Raise OSError on IO failures.
testing_contract:
- Integration: artifacts created in temp dirs with expected files.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.figure

from cyberthreatdetect.domain.types import Metrics, RunConfig


@dataclass(frozen=True)
class FileSystemArtifactStore:
    root_dir: Path

    def prepare_run_dir(self, *, run_id: str) -> Path:
        run_dir = self.root_dir / "runs" / run_id
        run_dir.mkdir(parents=True, exist_ok=False)
        return run_dir

    def write_config(self, *, run_dir: Path, config: RunConfig) -> None:
        (run_dir / "config.json").write_text(config.model_dump_json(indent=2), encoding="utf-8")

    def write_metrics(self, *, run_dir: Path, metrics: list[Metrics]) -> None:
        (run_dir / "metrics.json").write_text(
            json.dumps([m.model_dump() for m in metrics], indent=2), encoding="utf-8"
        )

        csv_lines = ["model_id,accuracy,precision,recall,f1,roc_auc"]
        for m in metrics:
            csv_lines.append(
                f"{m.model_id},{m.accuracy:.6f},{m.precision:.6f},{m.recall:.6f},{m.f1:.6f},{'' if m.roc_auc is None else f'{m.roc_auc:.6f}'}"
            )
        (run_dir / "metrics.csv").write_text("\n".join(csv_lines) + "\n", encoding="utf-8")

    def write_plot(self, *, run_dir: Path, filename: str, fig: matplotlib.figure.Figure) -> None:
        out_path = run_dir / filename
        fig.savefig(out_path, bbox_inches="tight", dpi=160)
