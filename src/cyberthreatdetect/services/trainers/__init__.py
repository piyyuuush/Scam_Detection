"""
@design-guard
role: Model trainer implementations for baseline ML and deep learning models.
layer: service
non_goals:
- Dataset loading or artifact persistence.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [rf_trainer, torch_cnn_trainer, torch_lstm_trainer]
invariants:
- Trainers return a model capable of producing positive-class probabilities.
authority:
decides: [training defaults that are safe on CPU]
delegates: [metric computation to evaluator]
extension_policy:
- Add new trainers without changing the Trainer port; register in bootstrap.
failure_contract:
- Raise RuntimeError for training failures.
testing_contract:
- Unit: each trainer trains on a tiny dataset quickly.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""
