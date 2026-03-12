# ADR 0003: Dataset download, attribution, and non-committed raw data

## Status
Accepted

## Context
Cybersecurity datasets are often large and have license/attribution requirements. We need reproducible downloads without committing raw data into git.

## Decision
- Datasets are downloaded on-demand into `data/raw/<dataset_id>/`.
- `data/` is ignored by git.
- For each dataset download, write a `SOURCE.json` into the dataset folder containing:
  - dataset name and citation/attribution
  - source URL(s)
  - download timestamp
  - file checksums
- Preprocessed or cached intermediate files (if any) live under `data/derived/<dataset_id>/` and are also git-ignored.

## Rationale
- Keeps the repo small and compliant.
- Makes it easy to reproduce experiments and audit data provenance.

## Consequences
- CLI must provide `ctd dataset download ...` and clearly fail with actionable errors when data is missing.
- CI tests must not depend on downloading full datasets; tests use tiny local fixtures.

