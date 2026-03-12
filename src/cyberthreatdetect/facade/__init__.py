"""
@design-guard
role: Facade layer exposing application use-cases to UIs.
layer: facade
non_goals:
- Direct IO or training implementations.
boundaries:
depends_on_layers: [domain, ports, service, facade]
exposes: [CyberThreatDetectFacade]
invariants:
- UI interacts only with the facade (not with services directly).
authority:
decides: [public use-case methods and their stable signatures]
delegates: [details to services via ports]
extension_policy:
- Add new use-cases as new facade methods rather than leaking services to UI.
failure_contract:
- Surface failures as exceptions with actionable messages.
testing_contract:
- Integration: facade orchestrates a run using temp dirs and fixture datasets.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""
