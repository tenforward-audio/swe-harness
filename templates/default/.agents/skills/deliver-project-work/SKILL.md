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
   - canonical coordinating branch, implementation branch, and whether an
     additional worktree or confirmed clean branch switches are needed
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

If the request names more than one tracked identifier, ask the user to choose
one as the parent outcome. Do not turn a second tracked identifier into an
implementation lane or move it from its current lifecycle location implicitly.
Parallel lanes are bounded parts of the one selected parent, not extra cards.

## Advance and implement after confirmation

1. Follow [`manage-project-work`](../manage-project-work/SKILL.md) to satisfy
   the promotion and start checks, then move the selected identifier through
   Planning into In progress without copying it. Checkpoint the In progress
   state on the canonical coordinating branch before implementation branches
   diverge.
2. Record the owner branch and next action on the In progress card. Keep
   canonical queue and board changes on the canonical coordinating branch.
3. Create `codex/<id>-<description>` from the exact In progress checkpoint as
   the durable implementation branch.
   - For one mutating lane, the coordinating checkout may switch to that branch
     and later return to the canonical branch when both switches were confirmed
     and the checkout is clean. Do not add a worktree merely to avoid a safe,
     authorised switch.
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
  evidence. The candidate branch must remain pinned to that commit. Return the
  clean coordinating checkout to the canonical branch, or use its already
  separate worktree, and create the Reviewing tracking checkpoint there. Never
  commit the Reviewing transition on the candidate branch.
- If the canonical coordinating branch cannot be restored or updated safely,
  leave its card In progress, keep the candidate branch pinned, and report the
  exact blocker instead of creating ambiguous review state.
- Never accept the card automatically. User acceptance, technical review,
  integration, push, and release remain separate explicit actions.
