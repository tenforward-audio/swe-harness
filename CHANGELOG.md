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
  `doctor` commands.
- Optional skills-only Codex plugin assembled from canonical repository sources.
- Installation provenance with validated paths and checksums for safe upgrades.

### Changed

- Made this repository, rather than a personal skill directory, authoritative
  for reusable harness content and behavior.
- Extended validation to installation metadata and built-plugin integration.

### Deprecated

### Removed

### Fixed

### Security

- Added conflict blocking, project-edit preservation, symbolic-link and path
  traversal rejection, atomic replacement, and rollback coverage.
