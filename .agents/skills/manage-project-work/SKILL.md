---
name: manage-project-work
description: List open tickets, list items awaiting review, summarise status, promote, start, record acceptance, return, or close already-recorded work in this project's Markdown intake queues and Planning, In progress, and Reviewing boards. Use for filtered work lists, selected IDs, lifecycle transitions, and manual acceptance evidence. Do not use for initial intake capture, parallel-lane orchestration, technical candidate review, engineering implementation, integration, or release work.
---

# Manage Project Work

Read [`../../WORKFLOW.md`](../../WORKFLOW.md) before changing tracked state. It
is the canonical source for card fields, statuses, and transition checks; this
skill owns the procedure for applying them.

## Load only the requested state

- Use `../../ISSUES.md` and `../../FEATURES.md` for unselected intake.
- Use `../../workboard/PLANNING.md` for selected work not started,
  `../../workboard/IN_PROGRESS.md` for the one active parent card, and
  `../../workboard/REVIEWING.md` for completed candidates awaiting review.
- Open only the relevant source. When status is unknown, search the boards by ID
  and read only the matching file. Load every source only for an explicit
  overview or migration.
- For an overview, return one compact line per item:
  `ID — status — outcome — owner branch (if any) — next review action`.
- Move items and cards rather than copying them. Never reuse an identifier.

## List filtered work read-only

- Treat “open tickets” as every unclosed `ISSUE-*` record across issue intake,
  Planning, In progress, and Reviewing. Treat “open work” as both issue and
  feature records across those live states.
- For “items for review” or equivalent wording, read only `REVIEWING.md` unless
  the user explicitly requests candidates or review assignments in another
  state.
- When the user names a queue, state, type, or identifier, load only the owning
  source. Load all queues and boards only for an explicit cross-lifecycle list.
- Listing is read-only. Do not promote, start, accept, return, close, reorder, or
  rewrite an item unless the user separately requests that transition.
- Return a compact filtered list using the overview format above and say plainly
  when no matching work exists.

## Promote and advance deliberately

- Treat requests to list, inspect, or summarise intake as read-only triage.
  Return readiness to plan or the most important missing detail.
- Promotion requires a deliberate user choice. Move the item to `PLANNING.md`
  using the selected card shape and promotion checks in the workflow contract.
- Start only an explicitly selected card. Keep at most one parent card in
  `IN_PROGRESS.md` unless the user changes the work-in-progress policy.
- Move a completed candidate to `REVIEWING.md` only after the workflow
  contract's completion and evidence checks are satisfied.
- Include a move to Reviewing in the coherent automatic checkpoint after
  working-tree and staged-scope review. If it cannot be isolated safely, leave
  it uncommitted and report why.
- After technical review, record durable outcomes in changelog, documentation,
  or an ADR as appropriate, then remove the card only when the user accepts it.
  Return it to Planning if material work remains. Close or reject intake only
  when asked.

## Keep lifecycle ownership narrow

- [`coordinate-parallel-work`](../coordinate-parallel-work/SKILL.md) owns lane,
  common-base, worktree, dependency, and ownership orchestration.
- [`review-project-change`](../review-project-change/SKILL.md) owns read-only
  technical assessment and returns evidence without changing lifecycle state.
- [`integrate-reviewed-change`](../integrate-reviewed-change/SKILL.md) owns an
  explicitly authorised integration without inferring acceptance or closure.
- Keep status boards canonical in the coordinating checkout. Background lanes
  return commits and evidence but never independently promote cards, rewrite
  queues, or reconcile global state.
