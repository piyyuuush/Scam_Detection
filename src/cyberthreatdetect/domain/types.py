"""
@design-guard
role: Defines core run/dataset/model types and serialization-friendly structures.
layer: domain
non_goals:
- Knowing how to download datasets or train models.
boundaries:
depends_on_layers: [domain]
exposes: [DatasetId, ModelId, ModelSpec, RunConfig, DatasetSplit, Metrics, RunSummary]
invariants:
- RunConfig is JSON-serializable and stable across versions.
- Dataset/task is treated as binary classification for comparability.
authority:
decides: [shape of configs and results persisted in artifacts]
delegates: [execution to facade/services]
extension_policy:
- Extend using new fields with defaults; avoid breaking existing artifacts.
failure_contract:
- Construction should be total; validation is handled by upstream UI/service layer.
testing_contract:
- Unit: round-trip JSON serialization via pydantic.
references:
- docs/domain_model.md
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field

DatasetId = Literal["nsl_kdd", "phiusiil", "fixture_tabular"]
ModelId = Literal["rf", "cnn", "lstm"]


class DatasetSplit(BaseModel):
    kind: Literal["predefined_train_test", "random_stratified_split"]
    test_size: float | None = None


class ModelSpec(BaseModel):
    model_id: ModelId
    max_epochs: int = 5
    batch_size: int = 128
    learning_rate: float = 1e-3
    rf_n_estimators: int = 300
    rf_max_depth: int | None = None


class RunConfig(BaseModel):
    run_id: str
    created_at_utc: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    dataset_id: DatasetId
    split: DatasetSplit
    models: list[ModelSpec]
    seed: int = 1337
    artifacts_root: str = "artifacts"


class Metrics(BaseModel):
    model_id: ModelId
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float | None


class RunSummary(BaseModel):
    run_id: str
    dataset_id: DatasetId
    metrics: list[Metrics]
    artifacts_dir: str
