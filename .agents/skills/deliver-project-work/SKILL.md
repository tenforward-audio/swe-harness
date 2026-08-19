---
name: deliver-project-work
description: Take an explicitly selected recorded issue or feature from its current queue through confirmation, Planning, In progress, implementation, checks, and Reviewing. Use when the user says to work on, start, or implement an ISSUE-* or FEATURE-* item as one end-to-end action. Do not use for initial intake, listing, planning-only transitions, acceptance, technical review, integration, releases, or unrecorded changes.
---

# Deliver Project Work

## Confirm one execution plan

1. Read the root `AGENTS.md`, the canonical
   [workflow](../../WORKFLOW.md), the
   [contributing guide](../../CONTRIBUTING.md), and the one queue or board that
   contains the selected identifier.
2. Resolve the item's current status. Stop if the identifier is missing,
   duplicated, already Reviewing, or otherwise ambiguous.
3. Prepare one concise confirmation containing:
   - outcome, scope, constraints, and explicit exclusions
   - exit checks and manual acceptance
   - target branch and whether an additional worktree is needed
   - the lifecycle moves needed to reach In progress
4. Ask for explicit confirmation before moving the card, creating a branch or
   worktree, or changing product files. Treat planning-only wording such as
   "promote to Planning" as a lifecycle request owned by
   [`manage-project-work`](../manage-project-work/SKILL.md), not as authority to
   begin implementation.

If another parent card already occupies In progress, do not start a second one.
Offer to leave the selected item in Planning, finish the active card first, or
use explicitly approved parallel lanes when the outcomes can be coordinated
under one parent. Never silently combine independent cards or change the WIP
policy.

## Advance and implement after confirmation

1. Follow [`manage-project-work`](../manage-project-work/SKILL.md) to satisfy
   the promotion and start checks, then move the selected identifier through
   Planning into In progress without copying it.
2. Record the owner branch and next action on the In progress card. Keep
   canonical queue and board changes in the coordinating checkout.
3. Create `codex/<id>-<description>` as the durable implementation branch.
   - For one mutating lane, use one working checkout on that branch. Do not add
     a worktree merely to rename the same checkout.
   - For explicitly requested concurrent mutation, follow
     [`coordinate-parallel-work`](../coordinate-parallel-work/SKILL.md): keep
     one parent card, record bounded lanes and their common base, and give each
     mutating lane a separate worktree checked out on its own branch.
   - Let read-only lanes share a checkout.
4. Follow [`develop-project`](../develop-project/SKILL.md) to implement the
   confirmed scope and run its focused and full verification gates.

Confirmation authorises only the described lifecycle moves, isolation, and
implementation. It does not authorise integration, worktree removal, push,
publication, release, or history rewriting.

## Finish at Reviewing

- If required checks fail or the outcome is incomplete, keep the card In
  progress, record the evidence and one next action, and report the blocker.
- If implementation and required checks pass, follow
  [`manage-project-work`](../manage-project-work/SKILL.md) to move the card to
  Reviewing with the exact candidate commit and observed or unobserved
  evidence.
- Never accept the card automatically. User acceptance, technical review,
  integration, push, and release remain separate explicit actions.
