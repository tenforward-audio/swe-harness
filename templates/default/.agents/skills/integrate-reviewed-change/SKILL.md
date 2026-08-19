---
name: integrate-reviewed-change
description: Integrate an already reviewed candidate into the coordinating checkout after the user explicitly authorises that integration. Use for a pinned commit or branch whose review evidence and common base are known. Do not use for implementation, unreviewed conflict resolution, inferred acceptance, push, release, branch deletion, or worktree removal.
---

# Integrate a Reviewed Change

## Confirm authority and reviewed identity

1. Require an explicit user request to integrate or merge. Review completion or
   acceptance evidence alone is not integration authority.
2. Read the root `AGENTS.md`, the
   [contributing guide](../../CONTRIBUTING.md), the relevant lifecycle card when
   one exists, and the completed review evidence.
3. Resolve the exact reviewed candidate commit, reviewed common base,
   coordinating checkout, target ref, and requested integration method.
4. Verify that a named branch still points to the reviewed commit. If it
   advanced, send the new candidate through
   [`review-project-change`](../review-project-change/SKILL.md) before
   integration.
5. Inspect target dirtiness and unrelated user changes. Stop when the
   integration cannot be isolated without risking them.

If the integration method would materially change history or project behavior
and neither the user nor project instructions selected it, ask before mutating
the target. Do not infer authority for rebase, history rewriting, or a remote
operation.

## Integrate only reviewed scope

- Recheck the candidate diff from its common base and compare it with changes on
  the target since that base. Do not integrate a known failing or incomplete
  candidate.
- Audit root instructions and `.agents/` independently. Reject stale queue,
  board, policy, or evidence copies from a background lane. Apply legitimate
  reviewed canonical-state changes only in the designated coordinating checkout.
- Use the explicitly selected non-history-rewriting integration method. Preserve
  authorship and commit identity where the method allows it.
- Do not improvise substantive conflict resolutions. A conflict that changes
  reviewed behavior creates a new candidate that must return to development and
  review.
- Integration authority does not include push, tag, publication, release,
  branch deletion, worktree removal, or cleanup of preserved evidence.

## Verify and hand off

- Run the configured affected-layer checks and the required full gate after the
  integrated tree is coherent.
- Inspect the resulting diff and history for intended scope, canonical-state
  preservation, and unrelated changes.
- Report the integrated candidate and resulting commit, checks, conflicts or
  deviations, and observed versus unobserved evidence.
- Do not infer acceptance or card closure from integration. Use
  [`manage-project-work`](../manage-project-work/SKILL.md) only when the user
  explicitly requests the corresponding lifecycle transition.
