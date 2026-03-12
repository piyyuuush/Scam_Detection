"""
@design-guard
role: Unit tests for preprocessing behavior (fit/transform stability).
layer: ui
non_goals:
- Evaluating model accuracy.
boundaries:
depends_on_layers: [service]
exposes: [tests]
invariants:
- fit_transform/transform preserve sample count and produce float32 arrays.
authority:
decides: [expected preprocessing invariants]
delegates: [dataset parsing to dataset loaders]
extension_policy:
- Add tests when preprocessing policies change.
failure_contract:
- Failures indicate regressions in preprocessing lifecycle.
testing_contract:
- Unit.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

import numpy as np

from cyberthreatdetect.services.preprocessing import SklearnTabularPreprocessorFactory


def test_preprocessor_fit_transform_and_transform_shapes() -> None:
    x_train = np.asarray([[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]], dtype=np.float32)
    x_test = np.asarray([[3.0, 4.0], [4.0, 5.0]], dtype=np.float32)

    factory = SklearnTabularPreprocessorFactory()
    prep = factory.create(dataset_id="fixture_tabular", feature_names=["a", "b"])

    x_train_t = prep.fit_transform(x_train)
    x_test_t = prep.transform(x_test)

    assert x_train_t.shape == x_train.shape
    assert x_test_t.shape == x_test.shape
    assert x_train_t.dtype == np.float32
    assert x_test_t.dtype == np.float32
