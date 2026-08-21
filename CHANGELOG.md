# Changelog

All notable changes to `SWE Harness` are recorded here.

## Unreleased

## 0.1.0 - 2026-08-21

### Added

- Added explicit Track, Depends on, and Related to fields for live work cards,
  plus formal branch, worktree, dependency, and ownership metadata for parallel
  lanes.
- Repository-native project harness with intent-specific skills, intake queues,
  and Planning, In progress, and Reviewing boards.
- Canonical workflow and card schema in `.agents/WORKFLOW.md`.
- Project plugin capability policy in `.agents/PLUGINS.md`.
- Repository-authority decision establishing one canonical owner per concern.
- Structural validator for canonical sources, links, placeholders, tracked
  identifiers, WIP limits, and skill names.
- Canonical generic harness under `templates/default/`.
- Interactive and automatable `init`, dry-run-first `upgrade`, and read-only
  `validate` commands.
- Optional skills-only Codex plugin assembled from canonical repository sources.
- Installation provenance with validated paths and checksums for safe upgrades.
- Project-agnostic skills for parallel-lane coordination, read-only candidate
  review, and explicitly authorised integration of reviewed changes.
- Confirmed end-to-end delivery for a selected recorded item, covering its
  lifecycle moves, implementation, checks, and handoff to Reviewing.
- Consent-based cleanup for integrated, handed-off, or deliberately abandoned
  local worktrees and branches, with preservation checks and a durable research
  findings archive.
- Declared skill execution modes with non-recursive, bounded read-only
  delegation for investigation and candidate review, non-self-delegating inline
  workflows, and explicitly requested mutating orchestration.
- MIT licensing for open-source use, modification, and redistribution.

### Changed

- Extended structural validation to enforce the complete card and lane schema,
  live references, dependency cycles, canonical file ownership, and WIP limits.
- Made this repository, rather than a personal skill directory, authoritative
  for reusable harness content and behavior.
- Made concise test output a cross-language default: successful paths stay
  silent and routine commands summarise passes while retaining useful failure
  diagnostics.
- Extended validation to installation metadata and built-plugin integration.
- Standardised the first progress update for routed project and setup skills so
  users can see which skill is active and what job it is performing.
- Made open-ticket and review-queue listing an explicit read-only behavior of
  `manage-project-work`, and narrowed review, coordination, and integration to
  one routed owner each.
- Simplified the README around one plain-language work command, parallel
  worktrees, the current workflow, safe reconciliation, and the optional plugin
  surface.
- Made verified integration and completed research handoffs offer exact local
  cleanup while keeping lifecycle changes, remote deletion, and evidence
  removal separately authorised.
- Defined support for the latest `0.1.x` release alongside the current
  repository state.

### Deprecated

### Removed

### Fixed

- Corrected the MIT copyright holder to Ten Forward Ltd.
- Kept lifecycle tracking checkpoints off pinned implementation branches so
  candidate review and integration use one stable commit identity.
- Defined parallel lanes as parts of one selected card instead of silently
  combining multiple tracked identifiers under the single WIP slot.
- Allowed explicitly authorised local branch removal after a completed handoff
  when an independent durable reference preserves the exact candidate.
- Aligned the README's open-ticket and open-work examples with the canonical
  queue terminology.
- Clarified that acceptance applies to completed items in Reviewing and is the
  explicit action that removes their cards.
- Included the MIT licence notice in self-contained plugin builds and verified
  release-version parity between source and built manifests.

### Security

- Reject symbolic-linked canonical tracking sources before reading card data.
- Added conflict blocking, project-edit preservation, symbolic-link and path
  traversal rejection, atomic replacement, and rollback coverage.
