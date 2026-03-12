"""
@design-guard
role: Domain package holding pure types and invariants.
layer: domain
non_goals:
- IO, networking, ML training, or persistence.
boundaries:
depends_on_layers: [domain]
exposes: [types]
invariants:
- Domain modules are deterministic and side-effect free.
authority:
decides: [canonical types for configs/results exchanged across layers]
delegates: [implementation behavior to services]
extension_policy:
- Add new dataclasses/Enums; avoid depending on services/ui.
failure_contract:
- Raise ValueError for invalid domain construction only when unavoidable.
testing_contract:
- Unit: pure construction and serialization behavior.
references:
- docs/domain_model.md
"""
