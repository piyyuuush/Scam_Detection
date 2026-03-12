# Domain model

## Core concepts

### DatasetSpec
Identifies a dataset and how to obtain and interpret it.
- `dataset_id`: stable string identifier (e.g., `nsl_kdd`, `phiusiil`)
- `task`: `binary_classification`
- `source`: one or more URLs
- `raw_layout`: expected raw files and formats
- `label_semantics`: how labels map to \{0,1\}

### ModelSpec
Identifies a model family and its training defaults.
- `model_id`: `rf` | `cnn` | `lstm`
- `hyperparams`: model-specific configuration (trees, layers, epochs, etc.)

### RunConfig
All inputs needed to execute an experiment run deterministically.
- `run_id`: generated identifier (timestamp + random suffix)
- `dataset_id`
- `models`: list of `ModelSpec`
- `seed`
- `split`: (train/test strategy; dataset-specific)
- `artifacts_dir`: output root

### RunResult
The immutable outputs of a run.
- `config.json`
- `metrics.json` and `metrics.csv`
- plots (confusion matrix, ROC when applicable)
- optional predictions export

## Invariants
- A run is reproducible given the same config, code version, and dataset snapshot.
- UI reads artifacts; it does not train models.
- Raw datasets are never committed to git; each downloaded dataset includes `SOURCE.json`.

