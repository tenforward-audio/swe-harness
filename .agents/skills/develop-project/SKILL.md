---
name: develop-project
description: Implement, fix, refactor, test, or change dependencies after the user explicitly authorises an unrecorded mutation or a bounded In progress lane. Use for code, configuration, behavior-linked documentation, dependency evaluation, and isolated implementation. Do not use to advance a recorded item from intake or Planning, manage lifecycle state, investigate, technically review, integrate, or release.
---

# Develop the Project

For a recorded issue or feature, require an In progress parent card or an
assigned implementation lane. Route a request to work on, start, or implement
an item still in intake or Planning through
[`deliver-project-work`](../deliver-project-work/SKILL.md). Do not independently
move cards or edit canonical queues and boards.

## Implement from the owning boundary

1. Read the root `AGENTS.md`, [contributing guide](../../CONTRIBUTING.md), and
   only the other policies relevant to the change.
2. Inspect current implementation, behavior, and tests before selecting an
   approach. Trace input, state, failures, and output through the owning layer.
3. Implement the smallest complete behavior while preserving unrelated work.
4. Test important success, invalid-input, operational-failure, preservation,
   and supported-compatibility paths at the owning boundary.
5. For interactive or user-visible behavior, exercise it when available and
   report observed and unobserved evidence separately from automated checks.
6. Run focused tests and the affected-layer gate while iterating, then the
   configured full check-and-build gate once for a green checkpoint.

Do not execute unresolved command placeholders. Ask for the missing command only
when verification depends on it.

## Respect actual compatibility obligations

- Follow the compatibility boundary in root instructions. Do not preserve a
  historical shape without a named supported release, current consumer,
  authoritative data set, staged rollout, or explicit constraint. Record the
  scope, failure behavior, and removal condition of a temporary obligation.
- When project instructions mark prototype state disposable, update all current
  producers, consumers, tests, and fixtures together and rebuild or reset it.
- Preserve current-state integrity: validation, atomic updates, crash recovery,
  cache invalidation, and version identifiers are not speculative legacy
  support.

## Work inside assigned isolation

- A mutating lane created by
  [`coordinate-parallel-work`](../coordinate-parallel-work/SKILL.md) must use
  its recorded common base, worktree, branch, dependencies, and owned boundaries.
- Do not expand lane scope, mutate another lane's files or stateful resources,
  or edit canonical queues and status boards from a background worktree.
- Return checkpoint commits, verification evidence, conflicts, and material
  review notes to the coordinator.
- Parallel permission does not authorise merge, branch deletion, history
  rewriting, push, or remote changes.

## Apply engineering governance

- Follow [the style guide](../../STYLE_GUIDE.md) for naming, modules, errors,
  comments, and tests.
- Keep framework glue, domain behavior, and infrastructure boundaries distinct.
  Prefer explicit data and state over speculative abstractions or duplicate
  sources of truth.
- Read [the dependency policy](../../DEPENDENCIES.md) before adding, replacing,
  copying, or bundling external code or assets.
- Read [the plugin capability policy](../../PLUGINS.md) before making an
  external plugin a required or approved project capability.
- Read [the security policy](../../SECURITY.md) for sensitive boundaries,
  permissions, private data, untrusted input, or supply-chain changes.
- Create or supersede an ADR under `../../decisions/` only for a consequential,
  durable choice with credible alternatives and reversal conditions.

Update public documentation, decisions, dependency records, security guidance,
and the Unreleased changelog when their claims change. Finish with the
verification, isolation, staged-diff review, and checkpoint procedure in the
contributing guide.

Return the exact candidate commit, checks, and observed or unobserved evidence
to `deliver-project-work` or `manage-project-work` for the Reviewing transition.
