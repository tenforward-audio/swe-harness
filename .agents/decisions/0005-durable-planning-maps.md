# ADR 0005: Preserve planning uncertainty before delivery intake

- Status: Accepted
- Date: 2026-08-22
- Decision owners: Project maintainers

## Context

The delivery board deliberately admits only work with a clear outcome, scope,
checks, and acceptance approach. Feature intake can hold one prose `Open
questions` field, but individual unknowns cannot be linked, deferred, resolved,
or used to derive a planning frontier. ADRs own consequential decisions and the
research archive owns findings retained after abandonment; neither owns live
pre-delivery uncertainty.

Native Codex Plan mode is effective for exploring an idea but is intentionally
read-only. Users also need to skip questions they cannot or do not want to
answer yet without losing them when the conversation ends.

## Options considered

- Turn every uncertainty into an issue or feature and mix discovery with
  delivery work.
- Add question fields to delivery cards and allow unclear cards onto the
  Planning board.
- Add a separate repository-native planning map and durable question ledger
  upstream of delivery intake.

## Decision

Use separate `MAP-*`, `QUESTION-*`, and `GNDN-*` records in canonical Markdown.
Precise unanswered points become questions; concerns that cannot yet be phrased
precisely remain GNDN ("goes nowhere, does nothing"). Questions author directed
`Depends on` edges, while reverse blockers and the ready frontier are derived.
Resolved questions and concluded maps move to a permanent ledger.

Native Plan mode maintains a provisional, user-visible ledger handoff without
writing files. After Plan mode ends, the mapping workflow allocates current
identifiers and applies the validated change. A blocking skipped question
produces a map-only handoff rather than an incomplete implementation plan.

Delivery cards remain the only implementation lifecycle. They may depend on an
open planning question, but that dependency must be removed atomically when the
question resolves. A map remains the durable source pointer afterward.

## Consequences

- Users can defer questions without a separate grilling workflow or losing
  planning context between sessions.
- The repository contains a deterministic dependency graph suitable for future
  read-only visualisation without making visualisation part of this change.
- The planning ledger adds a second record family, but it stays upstream of and
  semantically distinct from delivery work.
- Installed generic harnesses advance to template revision `2026-08-22.2`.

## Reversal conditions

Reconsider the separate record family if a concrete consumer demonstrates that
one universal ticket lifecycle is simpler without weakening delivery readiness
or durable history. Any replacement must preserve skipped unknowns, GNDN notes,
dependency direction, Plan-mode read-only behavior, and repository authority.
