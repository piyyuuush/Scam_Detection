"""
@design-guard
role: Defines ports (interfaces) for IO and ML operations to enforce layering and DI.
layer: service
non_goals:
- Implementations of the interfaces (live in services).
boundaries:
depends_on_layers: [domain, ports]
exposes: [dataset_loader, preprocessing, trainer, evaluator, artifacts]
invariants:
- Ports depend only on domain and stdlib typing.
authority:
decides: [stable interface contracts used across services/facade]
delegates: [behavior to services implementations]
extension_policy:
- Add ports when a new responsibility boundary emerges; prefer small interfaces.
failure_contract:
- Ports describe failures via returned Results/exceptions documented at the boundary.
testing_contract:
- Unit: services can be tested against ports using fakes.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""
