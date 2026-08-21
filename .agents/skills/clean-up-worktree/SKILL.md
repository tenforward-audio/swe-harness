---
name: clean-up-worktree
description: Safely remove an explicitly named local Git worktree and optionally its local branch after the user authorises cleanup of an integrated or handed-off candidate, or deliberately abandons planning or research. Use only after material work and evidence are preserved. Do not use for integration, inferred lifecycle transitions, remote branch deletion, canonical-checkout removal, or forced loss of unreviewed work or user data.
---

# Clean Up a Worktree

## Execution mode

`inline`

## Confirm the exact local cleanup

1. Read the root `AGENTS.md`, the
   [contributing guide](../../CONTRIBUTING.md), and the canonical
   [workflow](../../WORKFLOW.md). Read the
   [research archive](../../RESEARCH.md) for an abandoned planning or research
   workspace.
2. Require an explicit user request or an unambiguous agreement to a cleanup
   offer that names the local worktree and branch. Classify the outcome as:
   - an accepted reviewed candidate whose integration or handoff is complete,
     or untracked work the user explicitly declared complete; or
   - planning or research the user deliberately chose to abandon.
3. Resolve the exact worktree path, attached branch, current commit,
   coordinating checkout, common base when relevant, and any associated card or
   review evidence. Never select a target from a guessed path, wildcard, or
   stale lane name.
4. State every proposed effect before acting. One confirmation may authorise a
   named lifecycle change, findings record, worktree removal, and local branch
   deletion only when each effect is listed explicitly.

Local cleanup authority never includes push, remote branch deletion, tag,
release, history rewriting, or deletion of durable review evidence. Do not
  offer cleanup merely because review or acceptance completed; acceptance or an
  explicit completion decision and the integration, handoff, or deliberate
  abandonment must all be established.

## Prove that removal will not lose work

- Refuse to remove the coordinating or canonical checkout. Confirm the target
  appears exactly once in Git's worktree inventory and that the named branch is
  checked out only there.
- Inspect tracked, untracked, and ignored content. Do not use forced worktree
  removal to bypass dirtiness, a lock, nested repository state, unreadable
  files, or uncertainty about user data.
- For an integrated candidate, verify that the branch still identifies the
  reviewed commit, the user accepted or explicitly declared the work complete,
  the recorded integration result contains the reviewed scope, and no later or
  unique work exists. Use ancestry for merge or fast-forward integration; for
  squash or cherry-pick, use the recorded commit mapping and patch comparison
  rather than pretending ancestry proves equivalence.
- For completed handoff, verify the recipient preserves the exact pinned
  candidate under a durable reference independent of the local branch and that
  the returned evidence no longer depends on the local worktree.
- For deliberate abandonment, inspect every commit and local change since the
  common base. Summarise what would be discarded and stop unless the user's
  authority clearly covers it.
- Preserve material abandoned findings in the narrowest durable Markdown owner
  in the coordinating checkout. Use project documentation for current claims,
  an ADR for a consequential durable decision, or `../../RESEARCH.md` for a
  useful negative or exploratory result. Checkpoint that record before cleanup.
  If no finding merits retention, say so explicitly rather than creating noise.
- When a tracked card exists, use
  [`manage-project-work`](../manage-project-work/SKILL.md) for the separately
  named close, reject, accept, or return transition. Cleanup authority alone
  does not alter queues or boards.

Stop and report the exact blocker if any identity, preservation, or authority
check fails. Never delete first and investigate afterwards.

## Remove in recoverable order

1. Remove the exact worktree through Git without a force flag, then verify that
   its registration and path are gone.
2. Delete only the explicitly authorised local branch. Prefer normal deletion
   when Git recognises it as merged. Force-delete it only when the completed
   preflight proves a squash or cherry-pick integration, proves a completed
   handoff retains the exact commit under an independent durable reference, or
   proves deliberate abandonment with all material findings and work preserved,
   and the user explicitly authorised that branch's deletion.
3. Do not run broad pruning or delete another stale worktree as a side effect.
   Leave every remote ref untouched.
4. Report the findings record or evidence retained, the exact local worktree
   and branch removed, any partial failure, and that remote branches were not
   changed. State whether recovery still depends on a recorded commit or
   reflog.
