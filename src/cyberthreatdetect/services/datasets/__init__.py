"""
@design-guard
role: Dataset-related services (download, parsing, registry).
layer: service
non_goals:
- Model training or evaluation.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [registry]
invariants:
- Raw datasets live under data/raw and are git-ignored.
authority:
decides: [dataset ids and loader selection policy]
delegates: [parsing to dataset-specific loaders]
extension_policy:
- Add new datasets via new loader implementations and registry entries.
failure_contract:
- Raise FileNotFoundError when required files are missing.
testing_contract:
- Integration: fixture dataset loader works without network access.
references:
- docs/adrs/0003-dataset-handling-and-licensing.md
"""
