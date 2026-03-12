"""
@design-guard
role: Service layer implementing ports for datasets, preprocessing, training, evaluation, and artifacts.
layer: service
non_goals:
- UI rendering or CLI argument parsing.
boundaries:
depends_on_layers: [domain, ports, service]
exposes: [experiment_runner, datasets, preprocessing, trainers, metrics, artifacts]
invariants:
- Services obey ports and avoid depending on ui.
authority:
decides: [implementation details behind stable ports]
delegates: [orchestration to facade/runner]
extension_policy:
- Add new implementations behind ports; keep responsibilities small.
failure_contract:
- Surface IO errors and training errors as explicit exceptions.
testing_contract:
- Unit: each service tested in isolation; integration tests cover runner end-to-end on fixtures.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""
