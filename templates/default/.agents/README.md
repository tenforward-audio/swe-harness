# Project agent harness

This directory is the detailed source of truth behind the automatically loaded
root instructions. Each concern has one canonical owner; other files route to
it instead of restating it. [Harness state](HARNESS.md) records reusable
template parity; `HARNESS.json` contains non-authoritative installation
checksums used only for safe reconciliation.

## Authority map

| Concern | Canonical owner |
| --- | --- |
| Product contract, safety, and intent routing | [`AGENTS.md`](../AGENTS.md) |
| Card schema and lifecycle | [`WORKFLOW.md`](WORKFLOW.md) |
| Unselected work | [`ISSUES.md`](ISSUES.md) and [`FEATURES.md`](FEATURES.md) |
| Selected work status | [`workboard/`](workboard/) |
| Desired plugin capabilities | [`PLUGINS.md`](PLUGINS.md) |
| Reusable template parity | [`HARNESS.md`](HARNESS.md) |
| Durable technical rationale | [`decisions/`](decisions/) |
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
- [Decisions](decisions/0000-template.md): ADR template for durable choices.

Repo-local skills under `skills/` separate intake capture, read-only
investigation, work-state management, mutating development, and release work.
Load the narrowest matching skill; intake queues are not routine context.
