"""
@design-guard
role: Unit tests for evaluator metric computations.
layer: ui
non_goals:
- End-to-end training validation (covered in integration/e2e).
boundaries:
depends_on_layers: [service]
exposes: [tests]
invariants:
- Metrics are computed deterministically for a fixed input.
authority:
decides: [expected metric values on small examples]
delegates: [training concerns to other tests]
extension_policy:
- Add tests when new metrics are introduced.
failure_contract:
- Test failures signal regression in metric computations.
testing_contract:
- Unit.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

import numpy as np

from cyberthreatdetect.services.metrics import SklearnBinaryClassifierEvaluator


def test_metrics_basic_case() -> None:
    y_true = np.asarray([0, 0, 1, 1], dtype=np.int64)
    y_proba = np.asarray([0.1, 0.4, 0.6, 0.9], dtype=np.float32)

    ev = SklearnBinaryClassifierEvaluator()
    m = ev.evaluate(model_id="rf", y_true=y_true, y_proba=y_proba)

    assert m.model_id == "rf"
    assert m.accuracy == 1.0
    assert m.precision == 1.0
    assert m.recall == 1.0
    assert m.f1 == 1.0
    assert m.roc_auc is not None
    assert m.roc_auc == 1.0


def test_metrics_handles_single_class_for_roc_auc() -> None:
    y_true = np.asarray([0, 0, 0, 0], dtype=np.int64)
    y_proba = np.asarray([0.1, 0.2, 0.3, 0.4], dtype=np.float32)

    ev = SklearnBinaryClassifierEvaluator()
    m = ev.evaluate(model_id="rf", y_true=y_true, y_proba=y_proba)
    assert m.roc_auc is None
