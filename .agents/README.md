# Project agent harness

This directory is the detailed source of truth behind the automatically loaded
root instructions. Each concern has one canonical owner; other files route to
it instead of restating it. [Harness state](HARNESS.md) records reusable
template parity.

## Authority map

| Concern | Canonical owner |
| --- | --- |
| Reusable generic harness content | [`../templates/default/`](../templates/default/) |
| Install, upgrade, and validation behavior | [`../swe_harness/`](../swe_harness/) |
| Optional Codex plugin surface | [`../plugins/swe-harness/`](../plugins/swe-harness/) |
| Product contract, safety, and intent routing | [`AGENTS.md`](../AGENTS.md) |
| Card schema and lifecycle | [`WORKFLOW.md`](WORKFLOW.md) |
| Unselected work | [`ISSUES.md`](ISSUES.md) and [`FEATURES.md`](FEATURES.md) |
| Selected work status | [`workboard/`](workboard/) |
| Durable abandoned research findings | [`RESEARCH.md`](RESEARCH.md) |
| Desired plugin capabilities | [`PLUGINS.md`](PLUGINS.md) |
| Reusable template parity | [`HARNESS.md`](HARNESS.md) |
| Durable technical rationale | [`decisions/`](decisions/), including [repository authority](decisions/0001-repository-authority.md), [distribution](decisions/0002-distribution-and-reconciliation.md), [skill execution modes](decisions/0003-skill-execution-modes.md), and [structured work-card relationships](decisions/0004-structured-work-card-relationships.md) |
| Delivered user-visible history | [`CHANGELOG.md`](../CHANGELOG.md) |

## Normal context

- [Root instructions](../AGENTS.md): concise project contract, intent routing,
  compatibility boundary, and proportional quality gates.

## Load on demand

- [Planning](workboard/PLANNING.md),
  [in progress](workboard/IN_PROGRESS.md), and
  [reviewing](workboard/REVIEWING.md): selected work split by status.
- [Workflow](WORKFLOW.md): the canonical card schema and lifecycle transitions.
- [Plugins](PLUGINS.md): desired capabilities and external authority limits.
- [Contributing](CONTRIBUTING.md): change and checkpoint workflow.
- [Style guide](STYLE_GUIDE.md): language-neutral engineering conventions.
- [Dependencies](DEPENDENCIES.md): external-library and licence review.
- [Versioning](VERSIONING.md): SemVer, changelog, and releases.
- [Security](SECURITY.md): reporting and security boundaries.
- [Issues](ISSUES.md) and [features](FEATURES.md): intake queues.
- [Research findings](RESEARCH.md): material results retained after deliberate
  abandonment; never live status.
- [Decisions](decisions/0000-template.md): ADR template for durable choices.

Repo-local skills under `skills/` separate intake capture, read-only
investigation, filtered work listing and lifecycle management, confirmed
end-to-end delivery, parallel-lane coordination, mutating development,
candidate review, reviewed integration, local worktree cleanup, and release
work. Each skill declares whether it runs inline, delegates bounded read-only
work automatically, or orchestrates agents only after an explicit parallel
request. The active agent may split broad read-only work among sibling workers;
a delegated worker never delegates again. Load the narrowest matching skill;
intake queues are not routine context.

Run `python3 scripts/check_harness.py` from the repository root after changing
this structure. Run the tests after changing templates, reconciliation, or the
plugin build. The validator enforces links and ownership invariants; it does not
make product decisions.
