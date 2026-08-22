---
name: map-project-planning
description: Preserve a fuzzy or multi-session planning effort as a repository-native map of precise questions, dependencies, deferred work, fog, and durable resolutions. Use when the user asks for a planning map, names a MAP-* or QUESTION-* record, or actively skips, defers, cannot answer, or wants to revisit a planning question later. Do not use grilling mode, implement the destination, or write repository state while native Plan mode is active.
---

# Map Project Planning

## Execution mode

`inline`

[`../../WORKFLOW.md`](../../WORKFLOW.md) owns planning-record shapes, graph
semantics, counters, and lifecycle. This skill owns the conversational mapping
and persistence procedure.

## Work with native Plan mode

- Use ordinary Plan-mode exploration and questions. Do not invoke or imitate a
  separate grilling workflow.
- Treat “skip”, “defer”, “I don't know”, “I can't answer that”, “I don't care
  yet”, and equivalent replies as deliberate planning decisions. Stop pursuing
  that question in the current conversation.
- If the unknown can be phrased precisely now, add a provisional question. If
  only the shape of a concern is visible, add a provisional fog note instead.
  Never manufacture a precise question from fog merely to create a ticket.
- Infer `Kind`, `Answerable by`, dependencies, relationships, and a concrete
  revisit trigger from available evidence. State material inference briefly so
  the user can correct it; do not turn confirmation into another interview.
- Author only `Depends on`. Derive reverse blockers and never store a second
  `Blocks` field.
- Maintain one compact provisional ledger delta as planning continues. Use
  local handles such as `MAP-new`, `Q1`, and `F1`; native Plan mode is read-only
  and must not reserve repository identifiers.
- A blocking skipped question prevents an implementation-ready plan. Finish
  with a decision-complete map handoff only. Non-blocking deferred questions
  may accompany an implementation-ready plan when its implementation details
  are otherwise complete.

End the plan with one `Planning ledger handoff` section containing:

```yaml
planning_ledger:
  readiness: map-only | implementation-ready
  map: create MAP-new | update MAP-NNN
  destination: one observable planning destination
  questions:
    - ref: Q1
      kind: decision | research | experiment | enabling-task
      question: one precise unanswered question
      answerable_by: user | agent | either
      depends_on: [Q2]
      related_to: []
      origin: F1 | none
      revisit_when: Now | concrete trigger
  fog:
    - ref: F1
      note: in-scope concern not yet precise enough to ask
  resolutions: []
```

Omit empty collections only when the handoff says no planning record change is
needed. The official plan must remain decision-complete for the action its
`readiness` permits.

## Persist after Plan mode

When the user leaves Plan mode and authorises the proposed action:

1. Re-read `../../planning/ACTIVE.md`, `../../planning/LEDGER.md`, and only the
   live work cards named by the handoff. Do not trust provisional identifiers
   or stale counters.
2. Match semantic duplicates before allocating identifiers. Reuse an existing
   record only when its map, precise question, and intended resolution are the
   same; otherwise preserve both.
3. Allocate every new identifier from the owning counter, translate all local
   handles, update counters and the `Updated` date, and preflight the complete
   mutation for missing references, dependency cycles, and delivery blockers.
   If the checkout changed or preflight fails, do not write; report the
   refreshed handoff needed.
4. Apply the complete map mutation as one coherent patch and validate the
   harness before checkpointing it.
5. Checkpoint the validated tracking change on the canonical coordinating
   branch before any separate implementation branch or product mutation.
6. For `map-only`, stop after persistence. For `implementation-ready`, continue
   only within the user's separately authorised implementation scope.

## Revisit and resolve

- Load an existing map at low resolution first: destination, scope, fog,
  resolved pointers, and the derived frontier. Open full question or resolution
  detail only when it can affect the current planning decision.
- The frontier is every open question with `Revisit when: Now` and no open
  prerequisite. A future revisit trigger makes a question deferred, not
  blocked. An open prerequisite makes it blocked.
- Resolve questions through normal Plan-mode discussion or evidence gathering.
  A resolution handoff moves the complete question to `LEDGER.md`, records its
  answer, rationale, evidence, date, and informed artifact, and removes any live
  delivery-card dependency on it in the same patch.
- When a resolution sharpens fog, remove that fog entry and create a question
  whose `Origin` retains the fog identifier. Git history preserves the former
  fog text.
- Keep a consequential architectural decision in an ADR and a material finding
  from deliberately abandoned research in `RESEARCH.md`; the planning ledger
  retains only the summary and canonical pointer rather than duplicate detail.
- Conclude a map only when it has no open child questions or fog, or when the
  user explicitly abandons or redraws its destination. Move concluded maps to
  the ledger; never infer abandonment from inactivity.
