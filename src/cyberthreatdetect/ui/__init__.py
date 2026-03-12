"""
@design-guard
role: UI layer containing CLI and Streamlit dashboard.
layer: ui
non_goals:
- Implementing training, preprocessing, or dataset parsing logic.
boundaries:
depends_on_layers: [facade, ui]
exposes: [cli, app_streamlit]
invariants:
- UI calls the facade (or reads artifacts) and does not bypass into services.
authority:
decides: [user-facing commands and presentation]
delegates: [execution to facade; persistence to artifact store via facade/services]
extension_policy:
- Add commands/pages without leaking service internals.
failure_contract:
- Surface user-actionable errors with non-zero exit codes.
testing_contract:
- E2E: subprocess CLI runs on fixture dataset and produces artifacts.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""
