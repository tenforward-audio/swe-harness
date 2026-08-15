---
name: capture-project-intake
description: "Record a message explicitly framed as a support ticket or feature request in this project's Markdown intake queue. Use when the user says support ticket or feature request, or begins the message with ISSUE, BUG, TASK, or FEATURE. This is capture-only: stop after writing and do not investigate, plan, promote, fix, or implement the item."
---

# Capture Project Intake

[`../../WORKFLOW.md`](../../WORKFLOW.md) is the canonical lifecycle, identifier,
and record-shape contract. This skill owns capture behavior only.

## Record only the request

1. Open only `../../ISSUES.md` for a support ticket, issue, bug, task,
   maintenance, or security report, or `../../FEATURES.md` for a product idea.
2. Use and increment that file's next identifier. Preserve every existing item.
3. Record only details stated by the user. Do not infer priority, root cause,
   solution, scope, or acceptance criteria.
4. Update the queue's date and empty marker as its format requires.
5. Stop after capture. Do not inspect code, investigate, prioritise, plan,
   promote, fix, or implement in the same turn, even if the intake message asks
   for implementation.

A later explicit request must select or promote the item before work begins.

Use the exact issue or feature intake shape in the workflow contract.

Confirm the identifier, summary, and queue in the final response. Do not turn
capture into triage.
