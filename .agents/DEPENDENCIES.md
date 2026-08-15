# Dependency policy

- Project licence: not yet selected; do not distribute beyond private project
  use until the owner makes and records this decision.
- Exact versions: package manifests and lockfiles

Prefer the standard library and existing dependencies when they credibly own the
required behavior. Add or replace an external library only for a demonstrated
need.

## Evaluation checklist

Record for every consequential direct dependency:

- package, exact-version source, and runtime or development scope;
- purpose, owner, alternatives considered, and removal condition;
- licence and compatibility with the project and distribution model;
- maintainer activity, provenance, security posture, and advisory handling;
- transitive, native, binary-size, build, platform, privacy, and network impact;
- the boundary used to verify behavior rather than duplicating library state.

Review copied code, fixtures, fonts, models, and bundled executables separately;
a permissive wrapper does not remove their obligations. Preserve attribution and
modification notices. Before distribution, generate required notices and an SBOM
from authoritative lockfiles rather than this summary.

## Adopted dependency record

No dependency evaluations are recorded.

Use this compact entry shape when needed:

```markdown
### Package and version

- Scope and purpose:
- Licence and source:
- Maintenance and security:
- Distribution and platform impact:
- Verification boundary:
- Alternatives and removal condition:
```
