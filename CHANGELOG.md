# Changelog

All notable changes to `SWE Harness` are recorded here.

## Unreleased

### Added

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
- MIT licensing for open-source use, modification, and redistribution.

### Changed

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
- Reworked the README around the current repository-owned workflow, intent
  routing, safe reconciliation model, and optional plugin surface.

### Deprecated

### Removed

### Fixed

### Security

- Added conflict blocking, project-edit preservation, symbolic-link and path
  traversal rejection, atomic replacement, and rollback coverage.
