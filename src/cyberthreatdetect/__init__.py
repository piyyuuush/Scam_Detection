"""
@design-guard
role: Public package entrypoint and version surface.
layer: domain
non_goals:
- Implementing application logic (lives in facade/services/ui).
boundaries:
depends_on_layers: [domain]
exposes: [__version__]
invariants:
- Importing the package has no side effects (no IO, no global initialization).
authority:
decides: [what is exported as the stable public surface]
delegates: [all runtime behavior to ui/facade layers]
extension_policy:
- Add exports intentionally; avoid re-exporting large dependency graphs.
failure_contract:
- No runtime failures during import; raise only on explicit function calls elsewhere.
testing_contract:
- Unit: import package without side effects.
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

__all__ = ["__version__"]

__version__ = "0.1.0"
