"""
@design-guard
role: Generate plots for evaluation artifacts (confusion matrix, ROC curve).
layer: service
non_goals:
- Persisting artifacts (artifact store responsibility).
- Performing model training or dataset loading.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [make_confusion_matrix_fig, make_roc_curve_fig]
invariants:
- Plots are derived from y_true and y_proba using a fixed threshold of 0.5.
authority:
decides: [visualization formats stored as artifacts]
delegates: [storage to ArtifactStore]
extension_policy:
- Add new plots as new functions; keep signatures stable.
failure_contract:
- Raise ValueError on invalid shapes; ROC may return None if not computable.
testing_contract:
- Unit: functions return matplotlib Figure for small valid inputs.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from sklearn.metrics import confusion_matrix, roc_curve


def make_confusion_matrix_fig(*, y_true: np.ndarray, y_proba: np.ndarray) -> Figure:
    if y_true.ndim != 1 or y_proba.ndim != 1:
        raise ValueError("Expected 1D arrays for y_true and y_proba.")
    y_pred = (y_proba >= 0.5).astype(int)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    ax.imshow(cm, interpolation="nearest")
    ax.set_title("Confusion matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_xticks([0, 1], labels=["0", "1"])
    ax.set_yticks([0, 1], labels=["0", "1"])

    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")

    fig.tight_layout()
    return fig


def make_roc_curve_fig(*, y_true: np.ndarray, y_proba: np.ndarray) -> Figure | None:
    if y_true.ndim != 1 or y_proba.ndim != 1:
        raise ValueError("Expected 1D arrays for y_true and y_proba.")
    try:
        fpr, tpr, _ = roc_curve(y_true, y_proba)
    except ValueError:
        return None

    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    ax.plot(fpr, tpr, label="ROC")
    ax.plot([0, 1], [0, 1], linestyle="--", label="Chance")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("ROC curve")
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig
