# ADR 0002: Keep one core and make the plugin a thin distribution layer

- Status: Accepted
- Date: 2026-08-15
- Decision owners: Project maintainers

## Context

The reusable harness previously existed as project files plus a machine-local
creation skill. That split made it unclear whether the product should be a
cloneable starter repository, an interactive project generator, or a Codex
plugin, and it allowed reusable content to drift outside this repository.

Projects also need different values and will legitimately edit installed files.
A reusable source therefore cannot remain authoritative over rendered project
content after installation.

## Options considered

- Make a starter repository the product and ask maintainers to merge future
  changes manually.
- Put templates and installation logic directly in a Codex plugin.
- Keep canonical templates and a deterministic CLI in this repository, with an
  optional plugin that delegates to the same core.
- Maintain equal template copies in the repository, a personal skill, and a
  plugin.

## Decision

`templates/default/` is the only canonical reusable content, and
`swe_harness/` is the only canonical rendering and reconciliation behavior. The
CLI provides interactive initialization plus deterministic non-interactive
operation. `plugins/swe-harness/` contains only the Codex-facing skill and
launcher; the build copies the core and templates into an untracked,
self-contained artifact.

An installed repository becomes authoritative for its rendered files.
`.agents/HARNESS.json` records the template revision and installed checksums only
so that an upgrade can distinguish unchanged generated content from project
edits. A mismatch requires review. Upgrades do not delete retired paths.

The first distribution has no MCP server, external tracker, custom interface,
or marketplace publication. Those would add authority and lifecycle questions
without improving the core initialization workflow.

## Consequences

- The source repository supports both a node-initializer-like workflow and an
  optional native Codex entry point without duplicate editable templates.
- Fresh installs are conflict-blocking and repeatable; upgrades are dry-run
  first and preserve ambiguous project-owned state.
- Personal copies may invoke or install this product, but they are not an
  authority from which repository sources are synchronised.
- Plugin artifacts must be rebuilt when the manifest, skill, core, or template
  changes, and tests must exercise the built artifact.

## Reversal conditions

Reconsider the boundary if the core requires Codex-only runtime APIs, if an
external system becomes an explicit source of truth, or if a separate package
registry becomes the supported delivery mechanism. Any replacement must retain
one canonical editable template and an explicit ownership boundary for rendered
project files.
