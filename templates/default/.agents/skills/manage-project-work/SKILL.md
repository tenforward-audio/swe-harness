---
name: manage-project-work
description: List, summarise, promote, start, review, close, or coordinate already-recorded work in this project's Markdown intake queues and Planning, In progress, and Reviewing boards. Use for selected IDs, status overviews, work-cycle transitions, manual acceptance evidence, and parallel lane ownership. Do not use for initial intake capture, engineering implementation, or release work.
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

## Promote and advance deliberately

- Treat requests to list, review, or summarise intake as read-only triage.
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
- After review, record durable outcomes in changelog, documentation, or an ADR
  as appropriate, then remove the card. Return it to Planning if material work
  remains. Close or reject intake only when asked.

## Coordinate parallel work centrally

- Keep status boards canonical in the coordinating checkout. Background
  worktrees must not independently promote cards, rewrite queues, or reconcile
  global state.
- Keep one parent card In progress. Record each lane on it with bounded output,
  read-only or mutating status, common base, dependencies, owned boundaries, and
  review branch when one exists. Do not record machine-specific worktree paths.
- Use the branch as durable owner of reviewable changes and the worktree as its
  isolated checkout. Require each lane to return commits, verification evidence,
  and review notes to the coordinator.
- Move the parent card to Reviewing only after required lanes are reviewed,
  integrated, and the coherent outcome passes its gates. Never integrate
  unreviewed code merely to reconcile tracking.
