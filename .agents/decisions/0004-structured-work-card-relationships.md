# ADR 0004: Record structured relationships on canonical live work cards

- Status: Accepted
- Date: 2026-08-21
- Decision owners: Project maintainers

## Context

Lifecycle files identify where work sits, but prose alone cannot reliably state
which logical workstream owns a card, which live card must finish first, which
cards are related, or how parallel lanes divide ownership. Inferring those facts
from Git history or agent conversations would be ambiguous and would weaken the
repository as the canonical source of work state.

## Options considered

- Keep lifecycle position as the only structured state.
- Record relationships in an external tracker.
- Add a small, validated relationship vocabulary to the canonical Markdown
  cards.

## Decision

Every live card declares `Track`, `Depends on`, and `Related to`. Dependencies
are directed references to other live cards; relationships are undirected and
need to be declared on only one card. An In progress card may additionally
declare a common base and formal lanes with stable identifiers, branches,
worktree state, lane dependencies, and owned boundaries.

The standard-library validator parses the five canonical live tracking files
and rejects duplicate identifiers, missing or malformed references, dependency
cycles, invalid lane metadata, symbolic-linked tracking sources, and violations
of the single-card WIP limit. It does not publish a graph or presentation API.

## Consequences

- Project state remains readable Markdown with one repository-owned source of
  truth.
- Agents and independent read-only tools can consume explicit relationships
  without guessing from prose or Git history.
- Installed generic harnesses gain required card fields and advance to template
  revision `2026-08-21.4`.
- Presentation and visualisation remain outside the SWE Harness product
  boundary.

## Reversal conditions

Reconsider the vocabulary if a concrete consumer needs richer relationship
types or if the workflow no longer benefits from structured parallel lanes.
Any replacement must keep repository files canonical, define validation and
failure behavior, and update producers, consumers, templates, and fixtures
together.
