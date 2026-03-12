"""
@design-guard
role: Unit tests ensuring trainers can fit and produce probability outputs.
layer: ui
non_goals:
- Validating real-world performance on full datasets.
boundaries:
depends_on_layers: [service]
exposes: [tests]
invariants:
- predict_proba returns shape (n_samples,) with values in [0,1].
authority:
decides: [trainer contract checks]
delegates: [evaluation correctness to evaluator tests]
extension_policy:
- Add tests when new trainers are introduced.
failure_contract:
- Failures indicate trainer contract regression.
testing_contract:
- Unit.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

import numpy as np

from cyberthreatdetect.domain.types import ModelSpec
from cyberthreatdetect.services.trainers.rf_trainer import RandomForestTrainer
from cyberthreatdetect.services.trainers.torch_cnn_trainer import TorchCnnTrainer
from cyberthreatdetect.services.trainers.torch_lstm_trainer import TorchLstmTrainer


def _tiny_dataset() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.asarray(
        [
            [0.0, 1.0, 0.0, 1.0],
            [0.1, 1.1, 0.0, 1.1],
            [1.0, 2.0, 1.0, 2.0],
            [1.1, 2.1, 1.0, 2.1],
        ],
        dtype=np.float32,
    )
    y = np.asarray([0, 0, 1, 1], dtype=np.int64)
    x_test = np.asarray([[0.2, 1.2, 0.0, 1.2], [1.2, 2.2, 1.0, 2.2]], dtype=np.float32)
    return x, y, x_test


def _assert_proba(y_proba: np.ndarray, n: int) -> None:
    assert y_proba.shape == (n,)
    assert np.isfinite(y_proba).all()
    assert (y_proba >= 0.0).all()
    assert (y_proba <= 1.0).all()


def test_random_forest_trainer_contract() -> None:
    x, y, x_test = _tiny_dataset()
    spec = ModelSpec(model_id="rf", rf_n_estimators=20)
    model = RandomForestTrainer().train(x_train=x, y_train=y, spec=spec, seed=1337)
    y_proba = model.predict_proba(x_test)
    _assert_proba(y_proba, n=x_test.shape[0])


def test_torch_cnn_trainer_contract() -> None:
    x, y, x_test = _tiny_dataset()
    spec = ModelSpec(model_id="cnn", max_epochs=1, batch_size=2)
    model = TorchCnnTrainer().train(x_train=x, y_train=y, spec=spec, seed=1337)
    y_proba = model.predict_proba(x_test)
    _assert_proba(y_proba, n=x_test.shape[0])


def test_torch_lstm_trainer_contract() -> None:
    x, y, x_test = _tiny_dataset()
    spec = ModelSpec(model_id="lstm", max_epochs=1, batch_size=2)
    model = TorchLstmTrainer().train(x_train=x, y_train=y, spec=spec, seed=1337)
    y_proba = model.predict_proba(x_test)
    _assert_proba(y_proba, n=x_test.shape[0])
