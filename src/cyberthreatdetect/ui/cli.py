"""
@design-guard
role: Typer CLI for dataset download and running experiments.
layer: ui
non_goals:
- Implementing dataset parsing/training; must delegate to facade/services.
boundaries:
depends_on_layers: [domain, facade, ui]
exposes: [app, main]
invariants:
- CLI remains thin; it constructs RunConfig and delegates.
authority:
decides: [CLI flags and defaults]
delegates: [execution to facade]
extension_policy:
- Add new commands that map to facade use-cases.
failure_contract:
- Exit non-zero on errors; show actionable messages.
testing_contract:
- E2E: CLI run on fixture dataset writes artifacts.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from secrets import token_hex
from typing import Annotated, cast

import pandas as pd
import typer

from cyberthreatdetect.bootstrap import build_facade
from cyberthreatdetect.domain.types import DatasetId, DatasetSplit, ModelId, ModelSpec, RunConfig
from cyberthreatdetect.services.artifact_reading import (
    list_run_dirs,
    read_run_config,
    read_run_metrics_table,
)

app = typer.Typer(add_completion=False, no_args_is_help=True)
dataset_app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(dataset_app, name="dataset")
runs_app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(runs_app, name="runs")

DEFAULT_DATA_DIR = Path("data")
DEFAULT_ARTIFACTS_DIR = Path("artifacts")
DEFAULT_MODELS: tuple[str, ...] = ("rf", "cnn", "lstm")


def _generate_run_id() -> str:
    ts = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{ts}_{token_hex(4)}"


def _parse_dataset_id(dataset: str) -> DatasetId:
    allowed: set[str] = {"nsl_kdd", "phiusiil", "fixture_tabular"}
    if dataset not in allowed:
        raise typer.BadParameter(f"Unknown dataset '{dataset}'. Allowed: {sorted(allowed)}")
    return cast(DatasetId, dataset)


def _parse_model_ids(models: list[str]) -> list[ModelId]:
    allowed: set[str] = {"rf", "cnn", "lstm"}
    bad = [m for m in models if m not in allowed]
    if bad:
        raise typer.BadParameter(f"Unknown models {bad}. Allowed: {sorted(allowed)}")
    return [cast(ModelId, m) for m in models]


@dataset_app.command("download")
def dataset_download(
    dataset_id: Annotated[str, typer.Argument()],
    data_dir: Annotated[Path, typer.Option()] = DEFAULT_DATA_DIR,
    artifacts_dir: Annotated[Path, typer.Option()] = DEFAULT_ARTIFACTS_DIR,
) -> None:
    facade = build_facade(data_dir=data_dir, artifacts_dir=artifacts_dir)
    facade.download_dataset(dataset_id=dataset_id)


@app.command("run")
def run(
    dataset: Annotated[str, typer.Option("--dataset")],
    models: Annotated[list[str] | None, typer.Option("--models")] = None,
    model_args: Annotated[list[str] | None, typer.Argument()] = None,
    max_epochs: Annotated[int, typer.Option("--max-epochs")] = 2,
    seed: Annotated[int, typer.Option("--seed")] = 1337,
    data_dir: Annotated[Path, typer.Option()] = DEFAULT_DATA_DIR,
    artifacts_dir: Annotated[Path, typer.Option()] = DEFAULT_ARTIFACTS_DIR,
) -> None:
    run_id = _generate_run_id()
    dataset_id = _parse_dataset_id(dataset)
    selected_models = list(models or []) + list(model_args or [])
    model_ids = _parse_model_ids(selected_models or list(DEFAULT_MODELS))
    split = (
        DatasetSplit(kind="predefined_train_test")
        if dataset_id == "nsl_kdd"
        else DatasetSplit(kind="random_stratified_split", test_size=0.25)
    )
    model_specs = [ModelSpec(model_id=m, max_epochs=max_epochs) for m in model_ids]
    config = RunConfig(
        run_id=run_id,
        dataset_id=dataset_id,
        split=split,
        models=model_specs,
        seed=seed,
        artifacts_root=str(artifacts_dir),
    )
    facade = build_facade(data_dir=data_dir, artifacts_dir=artifacts_dir)
    summary = facade.run_experiment(config=config)

    typer.echo(f"run_id: {summary.run_id}")
    typer.echo(f"dataset: {summary.dataset_id}")
    typer.echo(f"artifacts: {summary.artifacts_dir}")
    for m in summary.metrics:
        typer.echo(
            f"{m.model_id}: acc={m.accuracy:.4f} f1={m.f1:.4f} roc_auc={m.roc_auc if m.roc_auc is not None else 'n/a'}"
        )


@runs_app.command("list")
def runs_list(
    artifacts_dir: Annotated[Path, typer.Option()] = DEFAULT_ARTIFACTS_DIR,
) -> None:
    run_dirs = list_run_dirs(artifacts_root=artifacts_dir)
    if not run_dirs:
        typer.echo("No runs found.")
        return
    for rd in run_dirs:
        try:
            cfg = read_run_config(run_dir=rd)
            typer.echo(f"{rd.name}\tdataset={cfg.dataset_id}")
        except Exception:
            typer.echo(f"{rd.name}\t(unreadable config)")


@runs_app.command("compare")
def runs_compare(
    artifacts_dir: Annotated[Path, typer.Option()] = DEFAULT_ARTIFACTS_DIR,
    out_csv: Annotated[Path | None, typer.Option("--out-csv")] = None,
) -> None:
    run_dirs = list_run_dirs(artifacts_root=artifacts_dir)
    if not run_dirs:
        raise typer.Exit(code=1)

    rows = []
    for rd in run_dirs:
        cfg = read_run_config(run_dir=rd)
        df = read_run_metrics_table(run_dir=rd)
        df = df.copy()
        df.insert(0, "run_id", rd.name)
        df.insert(1, "dataset_id", cfg.dataset_id)
        rows.append(df)

    all_df = pd.concat(rows, ignore_index=True)
    typer.echo(all_df.to_string(index=False))

    if out_csv is not None:
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        all_df.to_csv(out_csv, index=False)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
