# ADR 0001: Python + scikit-learn + PyTorch + uv

## Status
Accepted

## Context
CyberThreatDetect needs a reproducible, CPU-friendly baseline framework to compare traditional ML (Random Forest) and deep learning (CNN/LSTM) approaches for intrusion and phishing detection, with strict quality guardrails (typing, linting, tests, CI) from day one.

## Options considered
- Python + scikit-learn + PyTorch, dependency-managed by `uv`.
- Python + scikit-learn + TensorFlow/Keras.
- Non-Python stacks.

## Decision
Use **Python 3.11** with:
- **scikit-learn** for preprocessing, Random Forest baselines, and metrics utilities
- **PyTorch** for CNN and LSTM trainers (CPU-first)
- **Typer** for a structured CLI
- **Streamlit** for a lightweight results dashboard (read-only over artifacts)
- **uv** for virtualenv + dependency + lockfile management

## Rationale
- scikit-learn provides strong baselines and robust preprocessing pipelines.
- PyTorch provides explicit control over training loops, determinism, and CPU-friendly execution.
- Typer/Streamlit provide fast iteration on CLI and UI without introducing a web backend.
- `uv` provides reproducible environments with a lockfile and fast installs.

## Consequences
- The repository will include `pyproject.toml` and `uv.lock`.
- CI will use `uv sync --frozen` to guarantee dependency reproducibility.
- Deep learning training defaults must be CPU-safe and fast; the framework will expose configuration to scale up when needed.

