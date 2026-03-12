"""
@design-guard
role: E2E smoke test executing the CLI as a subprocess.
layer: ui
non_goals:
- Dataset network downloads.
boundaries:
depends_on_layers: [ui, facade]
exposes: [tests]
invariants:
- CLI returns exit code 0 and writes artifacts for fixture dataset.
authority:
decides: [minimum CLI contract for CI]
delegates: [detailed correctness to unit/integration tests]
extension_policy:
- Add new smoke cases for new commands.
failure_contract:
- Failures indicate broken packaging/entrypoint behavior.
testing_contract:
- E2E.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_cli_run_fixture_dataset(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    artifacts_dir = tmp_path / "artifacts"
    (data_dir / "fixtures").mkdir(parents=True, exist_ok=True)
    (data_dir / "fixtures" / "tabular_binary.csv").write_text(
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

    cmd = [
        sys.executable,
        "-m",
        "cyberthreatdetect.ui.cli",
        "run",
        "--dataset",
        "fixture_tabular",
        "--models",
        "rf",
        "--max-epochs",
        "1",
        "--data-dir",
        str(data_dir),
        "--artifacts-dir",
        str(artifacts_dir),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert res.returncode == 0, f"stdout:\n{res.stdout}\nstderr:\n{res.stderr}"

    runs_dir = artifacts_dir / "runs"
    assert runs_dir.exists()
    run_dirs = [p for p in runs_dir.iterdir() if p.is_dir()]
    assert run_dirs
