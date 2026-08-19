# Work workflow

This file is the canonical definition of card fields, status, and transitions.
The root [`AGENTS.md`](../AGENTS.md) owns intent and safety boundaries; the
intent-specific skills own how an agent performs an action. Queues and boards
contain live state only and must not redefine this contract.

## Authority rules

- A tracked identifier appears in exactly one queue or status board.
- A card's containing file is its status. Do not add a separate status field.
- Move an item; never copy it between lifecycle files.
- Intake order is not priority. Planning order expresses the chosen sequence.
- Keep no completed board. Accepted outcomes belong in Git history, the
  changelog, documentation, or an ADR.
- External trackers and plugins may display or transport work, but these files
  remain canonical unless an ADR explicitly changes that boundary.

## Lifecycle

| State | Canonical location | Entry rule | Exit rule |
| --- | --- | --- | --- |
| Issue intake | [`ISSUES.md`](ISSUES.md) | Explicit ticket, bug, task, maintenance, or security report | User deliberately promotes or closes it |
| Feature intake | [`FEATURES.md`](FEATURES.md) | Explicit product idea | User deliberately promotes or rejects it |
| Planning | [`workboard/PLANNING.md`](workboard/PLANNING.md) | Promoted item has an outcome and observable exit checks | User explicitly starts the card |
| In progress | [`workboard/IN_PROGRESS.md`](workboard/IN_PROGRESS.md) | The WIP slot is free and ownership is clear | Implementation and required checks are complete |
| Reviewing | [`workboard/REVIEWING.md`](workboard/REVIEWING.md) | Evidence and any manual acceptance steps are recorded | User accepts it, requests changes, or rejects it |

## Normal delivery path

A user does not need to request every lifecycle transition. "Work on
`ISSUE-001`", "start `FEATURE-001`", or "implement `ISSUE-001`" selects one
recorded item for the confirmed end-to-end path owned by
[`deliver-project-work`](skills/deliver-project-work/SKILL.md):

1. Resolve the item and present its outcome, scope, checks, and branch or
   worktree plan for confirmation.
2. After confirmation, satisfy the Planning and In progress entry rules and
   begin implementation on the approved branch.
3. Keep failed or incomplete work In progress with evidence and one next
   action.
4. Move a passing candidate to Reviewing with its commit and verification
   evidence.

An explicit request to "promote to Planning" or "start without implementing"
remains a lifecycle-only transition. Acceptance remains a separate user action.
If the WIP slot is occupied, ask whether to leave the item in Planning, finish
the current parent first, or explicitly coordinate compatible parallel lanes;
never create a second parent or combine independent cards silently.

A bounded, explicitly authorised change can be completed without durable card
state. Capture it first when it must survive the current task, compete for
priority, coordinate parallel lanes, or await later acceptance.

## Intake shapes

Issues use this shape:

```markdown
### ISSUE-001 — Short summary

- Reported: YYYY-MM-DD
- Type: bug | task | maintenance | security
- Report: What was observed or requested.
- Expected outcome: Expected behavior, or "Not stated."
- Acceptance notes: Constraints or reproduction details, or "Not stated."
```

Features use this shape:

```markdown
### FEATURE-001 — Short summary

- Reported: YYYY-MM-DD
- User or project benefit: Intended outcome.
- Constraints: Known limits, or "Not stated."
- Open questions: Unknowns, or "Not stated."
```

Identifiers are allocated only by the `Next issue` or `Next feature` counter in
the owning queue and are never reused.

## Selected card shape

A promoted item retains its intake identifier and replaces its intake record
with this card. Omit only fields explicitly marked optional.

```markdown
### ISSUE-001 — Observable outcome

- Source: User request or durable source link
- Outcome: User- or project-visible result
- Scope: Included boundaries and explicit exclusions
- Constraints: Safety, compatibility, dependency, or timing limits
- Exit checks: Observable behavior and configured automated gates
- Manual acceptance: Steps, or "Not applicable"
- Owner: Coordinating checkout or owner branch
- Capabilities: Native tools and approved plugins needed, or "None"
- Next action: The single next transition or review action
```

An In progress card may add `Lanes` for parallel ownership. A Reviewing card
must add `Evidence` with automated results and manual steps labelled `Observed`
or `Not observed`. Do not encode the same facts in a second card or external
tracker.

## Transition checks

### Promote to Planning

- The user deliberately selected the intake identifier.
- Outcome, scope, constraints, exit checks, and acceptance approach are clear.
- The item is removed from its intake queue in the same change.

### Start In progress

- The user selected the card and the WIP limit permits it.
- The owning boundary, branch, and any parallel lanes do not overlap.
- The card is removed from Planning in the same change.

### Move to Reviewing

- Behavior, tests, documentation, and configured gates are complete.
- Evidence names what was observed and what remains unobserved.
- The card is removed from In progress in the same coherent checkpoint.

### Accept, reject, or return

- Accepted cards are removed after their durable outcome is recorded.
- Cards needing material work move back to Planning with one clear next action.
- Rejected work is removed only on explicit user direction, with durable
  rationale recorded when it affects future decisions.
