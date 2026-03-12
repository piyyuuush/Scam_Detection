"""
@design-guard
role: CI guardrail ensuring every src module has a design-guard header.
layer: service
non_goals:
- Deep semantic validation of guards; only checks presence.
boundaries:
depends_on_layers: [service]
exposes: [main]
invariants:
- All Python files under src/cyberthreatdetect must include '@design-guard'.
authority:
decides: [minimum design-guard presence rule]
delegates: [content review to humans/PR review]
extension_policy:
- Extend to enforce schema fields if needed.
failure_contract:
- Exit non-zero with a list of files missing design-guards.
testing_contract:
- Unit: N/A (script is exercised in CI).
references:
- docs/adrs/0002-experiment-architecture-and-artifacts.md
"""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    src_root = repo_root / "src" / "cyberthreatdetect"
    missing: list[Path] = []

    for path in src_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "@design-guard" not in text[:1500]:
            missing.append(path)

    if missing:
        rel = [str(p.relative_to(repo_root)) for p in missing]
        print("Missing @design-guard in:")
        for p in rel:
            print(f"- {p}")
        return 2

    print("Design-guard check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
