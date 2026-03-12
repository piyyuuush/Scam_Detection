"""
@design-guard
role: 1D-CNN trainer treating tabular features as a length-n_features signal.
layer: service
non_goals:
- GPU-first training; keep CPU-safe defaults.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [TorchCnnTrainer]
invariants:
- Input features are (n_samples, n_features) float arrays.
- Model returns positive-class probabilities.
authority:
decides: [CNN architecture and CPU-safe training loop defaults]
delegates: [evaluation to evaluator; artifact storage to store]
extension_policy:
- Extend architecture via ModelSpec fields only if broadly useful.
failure_contract:
- Raise RuntimeError for torch failures.
testing_contract:
- Unit: trains for 1 epoch on tiny data and predicts correct shape.
references:
- docs/adrs/0001-tech-stack-python-sklearn-pytorch.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import numpy as np
import torch
from torch import nn

from cyberthreatdetect.domain.types import ModelSpec


class _CnnNet(nn.Module):
    def __init__(self, *, n_features: int) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(32, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = cast(torch.Tensor, self.net(x))
        return y.squeeze(1)


@dataclass(frozen=True)
class _TorchProbaModel:
    model: nn.Module

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            xt = torch.from_numpy(x).float().unsqueeze(1)
            logits = self.model(xt)
            proba = torch.sigmoid(logits).cpu().numpy()
        return np.asarray(proba, dtype=np.float32)


class TorchCnnTrainer:
    def train(
        self, *, x_train: np.ndarray, y_train: np.ndarray, spec: ModelSpec, seed: int
    ) -> _TorchProbaModel:
        if x_train.ndim != 2 or y_train.ndim != 1:
            raise ValueError("Expected x_train as 2D and y_train as 1D.")

        torch.manual_seed(seed)
        np.random.seed(seed)

        device = torch.device("cpu")
        n_features = x_train.shape[1]

        model = _CnnNet(n_features=n_features).to(device)
        opt = torch.optim.Adam(model.parameters(), lr=spec.learning_rate)
        loss_fn = nn.BCEWithLogitsLoss()

        xt = torch.from_numpy(x_train).float().unsqueeze(1).to(device)
        yt = torch.from_numpy(y_train.astype(np.float32)).to(device)

        batch_size = max(1, int(spec.batch_size))
        n = xt.shape[0]
        for _epoch in range(max(1, int(spec.max_epochs))):
            model.train()
            perm = torch.randperm(n)
            for i in range(0, n, batch_size):
                idx = perm[i : i + batch_size]
                xb = xt[idx]
                yb = yt[idx]
                opt.zero_grad(set_to_none=True)
                logits = model(xb)
                loss = loss_fn(logits, yb)
                loss.backward()
                opt.step()

        return _TorchProbaModel(model=model)
