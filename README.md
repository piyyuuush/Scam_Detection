# CyberThreatDetect

CyberThreatDetect is an AI-driven cybersecurity analysis platform that studies modern threat detection using Machine Learning and Deep Learning models. It evaluates Random Forest, CNN, and LSTM across intrusion and phishing detection, replacing rule-based approaches with data-driven insights.

## Quickstart (uv)

- Create environment + install deps:

```bash
uv sync
```

- Run tests:

```bash
uv run pytest
```

- Lint + typecheck:

```bash
uv run ruff check .
uv run ruff format .
uv run mypy .
```

## Datasets

Raw datasets are downloaded on-demand into `data/raw/` (ignored by git) and include a `SOURCE.json` for attribution and checksums.

## CLI

Download datasets:

```bash
uv run ctd dataset download nsl_kdd
uv run ctd dataset download phiusiil
```

Run an experiment:

```bash
uv run ctd run --dataset nsl_kdd --models rf cnn lstm --max-epochs 2
```

Compare runs (from artifacts):

```bash
uv run ctd runs list --artifacts-dir artifacts
uv run ctd runs compare --artifacts-dir artifacts
```

## Dashboard (Streamlit)

```bash
uv run streamlit run src/cyberthreatdetect/ui/app_streamlit.py
```

