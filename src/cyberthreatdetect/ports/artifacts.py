"""
@design-guard
role: Port for persisting run artifacts (config, metrics, plots) in an immutable folder per run.
layer: service
non_goals:
- Rendering UI; artifact reading for dashboard is separate.
boundaries:
depends_on_layers: [domain, ports]
exposes: [ArtifactStore]
invariants:
- Artifact writes are append-only per run_id (no cross-run mutation).
authority:
decides: [minimal operations required to persist experiment outputs]
delegates: [filesystem/cloud specifics to implementations]
extension_policy:
- Add new artifact types via new methods or structured payloads.
failure_contract:
- Raise OSError for IO failures.
testing_contract:
- Integration: write artifacts into a temp directory and validate file presence.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

import matplotlib.figure

from cyberthreatdetect.domain.types import Metrics, RunConfig


class ArtifactStore(Protocol):
    def prepare_run_dir(self, *, run_id: str) -> Path: ...

    def write_config(self, *, run_dir: Path, config: RunConfig) -> None: ...

    def write_metrics(self, *, run_dir: Path, metrics: list[Metrics]) -> None: ...

    def write_plot(
        self, *, run_dir: Path, filename: str, fig: matplotlib.figure.Figure
    ) -> None: ...
