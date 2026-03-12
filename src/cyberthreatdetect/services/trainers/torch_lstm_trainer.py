"""
@design-guard
role: LSTM trainer treating each feature as a sequence step (seq_len=n_features).
layer: service
non_goals:
- GPU-first training; keep CPU-safe defaults.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [TorchLstmTrainer]
invariants:
- Input features are (n_samples, n_features) float arrays.
- Model returns positive-class probabilities.
authority:
decides: [LSTM architecture and CPU-safe training loop defaults]
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


class _LstmNet(nn.Module):
    def __init__(self, *, hidden_size: int = 32) -> None:
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.lstm(x)
        out_t = cast(torch.Tensor, out)
        last = out_t[:, -1, :]
        y = cast(torch.Tensor, self.fc(last))
        return y.squeeze(1)


@dataclass(frozen=True)
class _TorchProbaModel:
    model: nn.Module

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            xt = torch.from_numpy(x).float().unsqueeze(2)
            logits = self.model(xt)
            proba = torch.sigmoid(logits).cpu().numpy()
        return np.asarray(proba, dtype=np.float32)


class TorchLstmTrainer:
    def train(
        self, *, x_train: np.ndarray, y_train: np.ndarray, spec: ModelSpec, seed: int
    ) -> _TorchProbaModel:
        if x_train.ndim != 2 or y_train.ndim != 1:
            raise ValueError("Expected x_train as 2D and y_train as 1D.")

        torch.manual_seed(seed)
        np.random.seed(seed)

        device = torch.device("cpu")

        model = _LstmNet(hidden_size=32).to(device)
        opt = torch.optim.Adam(model.parameters(), lr=spec.learning_rate)
        loss_fn = nn.BCEWithLogitsLoss()

        xt = torch.from_numpy(x_train).float().unsqueeze(2).to(device)
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
