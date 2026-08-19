---
name: investigate-project
description: Answer, explain, diagnose, research, compare, plan, or audit this project without changing product behavior or work tracking. Use for root-cause analysis, architecture or implementation questions, feasibility and option comparisons, and requested plans. Do not use for a technical review of a defined candidate change, explicitly framed intake, implementation, queue changes, or release actions.
---

# Investigate the Project

## Establish evidence read-only

1. Read the root `AGENTS.md`, then only the files and policies needed for the
   question.
2. State the question, current behavior, and evidence needed to answer it.
3. Inspect code, tests, logs, history, configuration, and generated output with
   read-only commands. Run non-mutating checks when they materially reduce
   uncertainty.
4. Trace the owning boundary and distinguish observed facts, supported
   inferences, assumptions, and unknowns.
5. Report the answer, likely cause, risks, or options with concrete file and
   behavior evidence. For a plan, name outcomes, dependencies, verification, and
   decisions without creating tracking state.

## Keep the boundary strict

- Do not edit files, dependencies, queues, status boards, branches, commits,
  releases, or external systems.
- Do not treat repository history as proof that an old data or API shape needs
  support; identify the concrete current compatibility obligation.
- For audits, lead with actionable correctness, security, data-loss,
  compatibility, concurrency, failure-behavior, and test findings. Say plainly
  when no material issue is found and note residual uncertainty.
- A review of a defined candidate commit, branch, worktree, or patch belongs to
  [`review-project-change`](../review-project-change/SKILL.md).
- If the request explicitly includes implementation, hand the evidence to
  `develop-project` for the authorised change. Explicitly framed support
  tickets and feature requests remain capture-only.
