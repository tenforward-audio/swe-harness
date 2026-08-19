---
name: coordinate-parallel-work
description: Coordinate explicitly requested parallel engineering work across agents, lanes, or Git worktrees. Use to establish one parent outcome, a common base, non-overlapping ownership, dependencies, isolated mutating worktrees, and evidence handoff. Do not use for single-lane development, technical candidate review, integration, worktree removal, or remote actions.
---

# Coordinate Parallel Work

## Establish the coordination boundary

1. Confirm that the user explicitly requested parallel work. Do not introduce
   concurrent mutating lanes merely because a task can be decomposed.
2. Read the root `AGENTS.md`, the canonical
   [workflow](../../WORKFLOW.md), and the
   [contributing guide](../../CONTRIBUTING.md).
3. Require one selected parent card in progress before dispatch. If none exists,
   use [`manage-project-work`](../manage-project-work/SKILL.md) to establish the
   user-selected outcome; do not invent or silently promote an intake item.
4. Resolve the coordinating checkout, canonical ref, exact common-base commit,
   current worktrees, and unrelated working-tree changes before creating lanes.

An explicit parallel-work request authorises only the isolation needed for the
requested lanes. It does not authorise integration, branch or worktree removal,
history rewriting, push, publication, or other remote actions.

## Design and dispatch bounded lanes

- Give each lane a stable name, bounded output, read-only or mutating status,
  owned files or architectural boundary, dependencies, and verification duty.
- Let read-only lanes share a checkout. Give every concurrent mutating lane a
  separate worktree created from the recorded common base and non-overlapping
  ownership. Never check out one branch in multiple worktrees.
- Assign a shared API, schema, generated artifact, migration, or stateful
  resource to one lane, or complete it first as an explicit dependency.
- Create a durable branch before a lane's first checkpoint or review. Do not
  reuse a completed branch for a different change.
- Record the lane names, common base, dependencies, owned boundaries, branch,
  and worktree state on the parent card without machine-specific absolute paths.
- Direct each mutating lane to follow
  [`develop-project`](../develop-project/SKILL.md). Background lanes return
  commits and evidence; they do not change canonical queues or boards.

## Reconcile evidence without integrating

- Collect each lane's exact commit, checks, observed and unobserved evidence,
  conflicts, dependency results, and review notes.
- Audit each lane from the common base for scope overlap and changes to root
  instructions or `.agents/`. Treat stale or unauthorised canonical-state edits
  as a scope leak and keep the coordinating checkout authoritative.
- Quarantine a lane with committed canonical-state drift or unsafe overlap.
  Preserve its evidence and request a clean replacement instead of rebasing,
  merging, or deleting it to hide the problem.
- Send defined candidates through
  [`review-project-change`](../review-project-change/SKILL.md). Keep lane
  worktrees and branches until their evidence is returned and any separately
  authorised integration or handoff is complete.

Coordination completes with a lane inventory and evidence handoff. Use
[`integrate-reviewed-change`](../integrate-reviewed-change/SKILL.md) only after
the user explicitly approves integration.
