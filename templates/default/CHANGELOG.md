# Changelog

All notable changes to `{{PROJECT_NAME}}` are recorded here.

## Unreleased

### Added

- Track, dependency, relationship, and formal parallel-lane fields for live work
  cards.

### Changed

- Structural validation enforces the canonical card fields, live references,
  dependency cycles, parallel-lane metadata, and WIP limit.

### Deprecated

### Removed

### Fixed

### Security

- Canonical tracking sources are rejected when they are symbolic links.
