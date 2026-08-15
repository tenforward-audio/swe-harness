# ADR 0001: Keep project authority in the repository

- Status: Accepted
- Date: 2026-08-15
- Decision owners: Project maintainers

## Context

Work cards, workflow rules, plugin capabilities, decisions, and release history
can easily diverge when the same fact is copied into several Markdown files or
split between the repository and an external service. Agents also need a stable
authority boundary that works without a particular account connection.

## Options considered

- Keep one repository-owned canonical source for each concern and treat
  integrations as bounded capabilities.
- Put every concern in one large document.
- Make an external tracker or plugin the authority and mirror selected state
  into the repository.
- Maintain several equal copies and reconcile them with convention or future
  automation.

## Decision

The repository owns normative project state. The authority map in
[`../README.md`](../README.md) assigns one canonical source to each concern.
Queues and boards own live card state; [`../WORKFLOW.md`](../WORKFLOW.md) owns
card structure and transitions; [`../PLUGINS.md`](../PLUGINS.md) owns desired
plugin capabilities and their authority boundaries.

External services may observe, transport, or act on state within declared
permissions. Their installation, connection, and sign-in state are runtime
evidence, not versioned project facts. Changing which system is authoritative
requires a superseding ADR and a migration that preserves identifiers and
history.

## Consequences

- Project policy and work state remain portable, reviewable, and available
  offline.
- Agents can resolve conflicts by following the authority map instead of
  comparing multiple peers.
- Integrations must adapt to repository state and cannot silently create a
  competing tracker.
- Card moves remain explicit repository changes unless a later integration can
  preserve the same invariants safely.
- The structural validator can enforce ownership invariants, but maintainers
  still own product and prioritisation decisions.

## Reversal conditions

Reconsider this decision if the repository can no longer support the required
multi-user coordination or if an external system becomes an explicit product
dependency with reliable identity, access, history, offline, and bidirectional
consistency guarantees. A replacement must name the migration, failure, and
recovery boundaries before authority moves.
