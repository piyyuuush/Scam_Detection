# ADR 0002: Layered experiment architecture + artifact-first results

## Status
Accepted

## Context
We need a maintainable and scalable framework that can compare multiple models across multiple datasets, while keeping coupling low and enabling strong testability. Results must be reproducible and inspectable without rerunning training.

## Decision
Adopt a layered architecture with explicit ports (interfaces) and a composition root:
- **domain**: pure types for run configuration, dataset specs, results, invariants
- **ports**: Protocols/ABCs for dataset loading, preprocessing, training, evaluation, artifact storage
- **services**: implementations of ports (sklearn preprocessing, torch trainers, metrics, artifact writers)
- **facade**: an application-level facade that orchestrates a run and hides internal wiring
- **ui**: CLI and Streamlit, calling only the facade
- **bootstrap**: composition root wiring concrete implementations to ports

Store every experiment run as an immutable artifact folder:
`artifacts/runs/<run_id>/`
containing at minimum:
- `config.json` (RunConfig)
- `metrics.json` (per model)
- `metrics.csv` (aggregate-friendly)
- plots (confusion matrix, ROC when applicable)
- `SOURCE.json`/`ATTRIBUTION.json` references where needed

## Rationale
- Ports + DI reduce blast radius and enable focused unit/integration tests.
- A facade gives stable public surface for UI and future integrations.
- Artifact-first workflow supports offline analysis, regression checks, and dashboard exploration.

## Consequences
- UI does not directly read raw data or train models; it only uses artifacts or the facade.
- Every code file must include a design-guard to preserve boundaries and prevent layer leaks.

